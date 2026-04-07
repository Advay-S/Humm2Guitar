import psycopg2
from pgvector.psycopg2 import register_vector

from Embedder import DocEmbedder

DATABASE_PARAMS = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "PASSWORD",
    "host": "localhost",  # change this
    "port": "5432"
}

class QueryInput:

    def __init__(self, db_params: dict = DATABASE_PARAMS, top_k: int = 5):
        self.dbparams = db_params
        self.top_k = top_k
        self.embedder = DocEmbedder()



    def search(self, query:str) -> list[str]:

        if not query or not query.strip():
            raise ValueError("Query cannot be empty")

        print("Embedding question")
        chunks = self.embedder.embed_single(query)

        conn = self._get_connectionz()

        try :
            with conn.cursor() as curr:
                curr.execute(
                    """
                    SELECT content
                    FROM document_chunks
                    WHERE length(content) > 200
                    ORDER BY embedding <=> %s::vector
                    LIMIT %s
                    """
                , (chunks, self.top_k)
                )
                rows = curr.fetchall()


        finally:
            conn.close()

        chunkz = [row[0] for row in rows]
        print(f"✅ Found {len(chunkz)} relevant chunks.")
        return chunkz



    def _get_connectionz(self):
        conn = psycopg2.connect(**self.dbparams)
        register_vector(conn)
        return conn
