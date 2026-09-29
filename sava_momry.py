import sqlite3
import json

conn = sqlite3.connect("memory.db" ,     check_same_thread=False
)

cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS long_term_memory3 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL UNIQUE
)
""")

conn.commit()

cursor.execute("""
CREATE TABLE IF NOT EXISTS messegs(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role TEXT,
    content TEXT
)
""")    
conn.commit()


def save_long_term(state):

    memories = state["memories"]

    for item in memories:

        memory = item["memory"].strip()

        if not memory:
            continue

        cursor.execute(
            """
            SELECT 1
            FROM long_term_memory3
            WHERE content = ?
            LIMIT 1
            """,
            (memory,)
        )

        if cursor.fetchone():
            continue

        cursor.execute(
            """
            INSERT INTO long_term_memory3 (content)
            VALUES (?)
            """,
            (memory,)
        )

    conn.commit()
def get_long_term():

    cursor.execute("""
        SELECT content
        FROM long_term_memory3
        ORDER BY id
    """)

    data = cursor.fetchall()

    return [
        {"memory": content}
        for (content,) in data
    ]


def save_short_term(role, content):

    cursor.execute(
        """
        SELECT 1
        FROM messegs
        WHERE role = ? AND content = ?
        """,
        (role, content)
    )

    if cursor.fetchone() is None:
        cursor.execute(
            """
            INSERT INTO messegs (role, content)
            VALUES (?, ?)
            """,
            (role, content)
        )

        conn.commit()

def get_short_term(limit=20):

    cursor.execute(
        """
        SELECT role, content
        FROM messegs
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,)
    )

    data = cursor.fetchall()
    data.reverse()

    return [
        {"role": role, "content": content}
        for role, content in data
    ]