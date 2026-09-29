    from tavily import TavilyClient
    from langchain_core.tools import tool
    import chromadb 
    from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    import os 
    import faiss
    import torch
    from langchain_huggingface.embeddings import HuggingFaceEmbeddings
    from sava_momry import get_long_term

    client = TavilyClient( "api_key")


    @tool
    def web_search(question: str):
        """
        Search the internet for information that requires up-to-date,
        current, or external web-based knowledge.

        Use this tool when:
        - The user asks about recent or current information.
        - The user asks about news, current events, prices, or live information.
        - The answer may have changed since the model's knowledge cutoff.
        - The user explicitly asks you to search the web.
        - The required information is not available in the local documents.

        Do not use this tool for general questions that can be answered
        reliably without external information.

        Input:
        question: The user's question or search query.
        """
        
        if not question.strip():
            return "Search query is empty."

        if question.strip().startswith("site:"):
            return "Please provide actual search terms, not only a site: operator."

        response = client.search(
            query=question,
            include_answer="basic",
            search_depth="basic",
            max_results=1
        )


        ret = ""

        for i in response["results"]:
            ret += i["content"] + "\nمرجع: " + i["url"] + "\n"

        return ret



    import math

    @tool

    def calculator(expression: str):
        """
        Evaluate mathematical expressions and return the calculated result.

        Use this tool when the user asks for a mathematical calculation,
        numerical computation, or evaluation of a mathematical expression.

        Supported operations and functions include:
        +, -, *, /, sqrt, sin, cos, tan, log, log10,
        pi, e, abs, round, and pow.

        The input must be a valid mathematical expression as a string.
        """
        try:
            allowed = {
                "sqrt": math.sqrt,
                "sin": math.sin,
                "cos": math.cos,
                "tan": math.tan,
                "log": math.log,
                "log10": math.log10,
                "pi": math.pi,
                "e": math.e,
                "abs": abs,
                "round": round,
                "pow": pow,
            }

            return eval(expression, {"__builtins__": {}}, allowed)

        except Exception as e:
            return f"Error: {str(e)}"


    embedding_function = SentenceTransformerEmbeddingFunction(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    client2 = chromadb.PersistentClient(path="./nvidia")

    collection  = client2.get_or_create_collection(name="collection" ,embedding_function=embedding_function  )
    @tool

    def local_search(question: str):
        """
        Search the local NVIDIA documents for relevant information.

        Use this tool when the user's question can be answered
        using information from the local NVIDIA document collection.

        Do not use this tool for general knowledge, calculations,
        or information that requires an internet search.

        Input:
            question: A natural-language question about the NVIDIA documents.

        Returns:
            The most relevant passages retrieved from the local documents.
        """

        result = collection.query(
            query_texts=[question],
            n_results=5
        )

        documents = result["documents"][0]

        if not documents:
            return "No relevant information was found in the local documents."

        return "\n\n".join(documents)


    # Model configuration
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    hf_embeddings = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs={"device": "cpu"}, # or "cuda", "mps"
    encode_kwargs={"normalize_embeddings": True}
    )


    @tool
    def long_term_memory(query: str):
        """
        Search the user's long-term memory for previously stored
        personal information that may be relevant to the current question.

        Use this tool when the user asks about information they may
        have explicitly shared in previous conversations, such as:
        - Their name or identity
        - Education, university, faculty, major, or academic year
        - Job or occupation
        - Skills or technologies they are learning
        - Long-term goals or projects
        - Stable preferences and interests
        - Important relationships
        - Other persistent personal information

        Do not use this tool for information contained in the
        current conversation or for general knowledge.

        Input:
        query: A concise semantic search query describing the personal
        information that should be retrieved from long-term memory.
        """

        text = [item["memory"] for item in get_long_term()]

        if not text:
            return "No long-term memories are stored."

        embed = torch.tensor(
            hf_embeddings.embed_documents(text),
            dtype=torch.float32
        )

        index = faiss.IndexFlatL2(embed.shape[1])
        index.add(embed.numpy())

        k = min(3, len(text))

        query_embedding = torch.tensor(
            hf_embeddings.embed_query(query),
            dtype=torch.float32
        ).reshape(1, -1)

        _, indices = index.search(
            query_embedding.numpy(),
            k
        )

        results = [
            text[i]
            for i in indices[0]
            if i != -1
            
        ]

        if not results:
            return "No relevant long-term memory was found."

        return "\n".join(
            f"- {memory}"
            for memory in results
        )
