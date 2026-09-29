from fastapi import HTTPException 
from security import hash_password , verify_password  , create_access_token
from schema import  reg_user , login_user
import sqlite3

def register_user(user: reg_user):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                city TEXT,
                street TEXT,
                building INTEGER
            )
        """)

        cursor.execute("""
            INSERT INTO users (
                name,
                age,
                email,
                password,
                city,
                street,
                building
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            user.name,
            user.age,
            user.email,
            hash_password(user.password),
            user.address.city,
            user.address.street,
            user.address.building
        ))

        conn.commit()

        return {
            "message": "تم التسجيل بنجاح",
            "username": user.name
        }

    except sqlite3.IntegrityError:
        return {
            "message": "البريد الإلكتروني مستخدم بالفعل"
        }

    finally:
        conn.close()

def login_users(email: str, password: str):

    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, email, password
        FROM users
        WHERE email = ?
    """, (email,))

    user = cursor.fetchone()

    conn.close()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(password, user["password"]):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_access_token(user["id"])

    return {
        "access_token": token,
        "token_type": "bearer"
    }


     