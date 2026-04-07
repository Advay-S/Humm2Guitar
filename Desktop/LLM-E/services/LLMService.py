import httpx

OLLAMA_HOST = "http://localhost:11434"
DEFAULT_MODEL = "llama3.2"

class LLM:
    def __init__(self, model:str = DEFAULT_MODEL , host: str = OLLAMA_HOST):
        self.model = model
        self.host = host
        self._url = f"{self.host}/api/generate"


    def answer(self, question:str , compressed_context:str)-> str:
        if not question or not question.strip():
            raise ValueError("Question cannot be empty.")
        if not compressed_context:
            raise ValueError("No context provided.")

        prompt = self._build_prompt(question, compressed_context)
        print(f"🤖 Sending prompt to Ollama ({self.model})...")
        return self._call_ollama(prompt)


    def _build_prompt(self, question: str, compressed_context: str) -> str:
        return f"""You are a senior financial analyst writing a detailed research report.
        Answer the question below using only the context provided.
            Your answer must be a well-structured paragraph of at least 4-5 sentences.
                Include specific numbers, percentages, and figures from the context.
                Explain the significance of the numbers, not just state them.Also make sure to 
                    Do not make up information. If the answer is not in the context say "I don't have enough information to answer this."
"

                                Context:
                                {compressed_context}
                                
                                Question: {question}
                                
                                Answer:"""


    def _call_ollama(self , prompt:str) ->str:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_ctx": 8192
            }
        }

        try:
            response = httpx.post(self._url, json=payload, timeout=600)
            response.raise_for_status()
        except httpx.ConnectError:
            raise RuntimeError(
                f"Could not connect to Ollama at {self.host}. "
                "Is Ollama running? Try: `ollama serve`"
            )
        except httpx.TimeoutException:
            raise RuntimeError("Ollama timed out. Try a shorter context.")

        data = response.json()

        if "response" not in data:
            raise RuntimeError(f"Unexpected Ollama response: {data}")

        return data["response"]





