import psycopg2
import json
from pgvector.psycopg2 import register_vector
from Embedder import DocEmbedder

DATABASE_PARAMS = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "PASSWORD",
    "host": "localhost",  # change this
    "port": "5432"
}


class VectorStore:
    def __init__(self, db_params: dict = DATABASE_PARAMS):
        self.db_params = db_params
        self.embedder = DocEmbedder();

    def ingest(self, doc_name: str, chunks: list[str]):

        if not chunks:
            raise ValueError("chunks list is empty")

        conn = self._get_connection()
        inserted = 0;

        try:
            with conn.cursor() as cursor:
                for i, chunk in enumerate(chunks):
                    if not chunk or not chunk.strip():
                        print(f"  ⚠️  Skipping empty chunk at index {i}")
                        continue

                    vector = self.embedder.embed_single(chunk)

                    cursor.execute(
                        """ INSERT INTO document_chunks(document_name, chunk_type, content, metadata, embedding) VALUES(%s,%s,%s,%s,%s)""",
                        (doc_name, "text", chunk, json.dumps({"chunk_index": i}), vector))

                    inserted += 1
                conn.commit()
                print(f"✅ Inserted {inserted} chunks into PostgreSQL.")

        except Exception as e:
            conn.rollback()
            raise RuntimeError(...)

        finally:
            conn.close()

    def _get_connection(self):
        conn = psycopg2.connect(**self.db_params)
        register_vector(conn)
        return conn

