import httpx
from typing import List

OLLAMA_DEFAULT_HOST = "http://localhost:11434"
OLLAMA_DEFAULT_ENDPOINT = "/api/embeddings"
DEFAULT_MODEL = "nomic-embed-text"
EXPECTED_DIMENSIONS = 768

class DocEmbedder :

    def __init__(self, model_name:str = DEFAULT_MODEL, host : str = OLLAMA_DEFAULT_HOST, timeout : int = 60):
        self.model_name = model_name
        self.host = host.rstrip("/")
        self.timeout = timeout
        self._url = f"{self.host}{OLLAMA_DEFAULT_ENDPOINT}"
        self.verify_connection()


    def embed_single(self , text:str) -> List[float] :
        if not text or not text.strip():
            raise ValueError("Cannot embed empty or whitespace-only text.")
        return self._call_ollama(text)

    def embed_chunks(self , texts:List[str]) -> List[float]:
        if not texts :
            raise ValueError("Cannot embed empty or whitespace-only text.")

        vectors = []
        for i, text in enumerate(texts):
            if not text or not text.strip():
                print(f"  ⚠️  Skipping empty chunk at index {i}")
                continue
            vectors.append(self._call_ollama(text))

        return vectors

    def _call_ollama(self, text:str)->List[float]:
        payload={"model": self.model_name,
            "prompt": text}

        try:
         response = httpx.post(self._url, json=payload, timeout=self.timeout)
         response.raise_for_status()

        except httpx.ConnectError:
            raise RuntimeError(
                f"Could not connect to Ollama at {self.host}. "
                "Is Ollama running? Try: `ollama serve`"
            )
        except httpx.HTTPStatusError as e:
            raise RuntimeError(
                f"Ollama returned HTTP {e.response.status_code}: {e.response.text}"
            )
        except httpx.TimeoutException:
            raise RuntimeError(
                f"Ollama timed out after {self.timeout}s. "
                "Model may not be loaded. Try: `ollama pull nomic-embed-text`"
            )

        data = response.json()

        if "embedding" not in data:
            raise RuntimeError(f"Unexpected Ollama response — 'embedding' key missing. Got: {data}")

        vector = data["embedding"]

        if len(vector) != EXPECTED_DIMENSIONS:
            print(
                f"Warning: expected {EXPECTED_DIMENSIONS} dims, "
                f"got {len(vector)}. Check your model."
            )

        return vector

    def verify_connection(self):
        try :
            response = httpx.get(f"{self.host}/api/tags", timeout=5)
            response.raise_for_status()
            print(f"✅ Embedder ready — Ollama @ {self.host} | model: {self.model_name}")
        except Exception as e:
            raise RuntimeError(
                f"Could not reach Ollama at {self.host}. "
                f"Start it first with `ollama serve`. Detail: {e}"
            )


