from llmlingua import PromptCompressor

class Compressor:

    def __init__(self):
        print("⚙️ Loading compression model...")
        self.compressor = PromptCompressor(
            model_name="microsoft/llmlingua-2-bert-base-multilingual-cased-meetingbank",
            use_llmlingua2=True,
            device_map="cpu"
        )
        print("✅ Compressor ready.")

    def compress(self, question: str, chunks: list[str]) -> str:
        if not chunks:
            raise ValueError("No chunks to compress.")

        print(f"🗜️ Compressing {len(chunks)} chunks...")

        context = "\n\n".join(chunks)

        result = self.compressor.compress_prompt(
            context,
            rate=0.75,
            force_tokens=['\n', '.', '!', '?', ',']
        )

        compressed_text = result["compressed_prompt"]
        original_tokens = result["origin_tokens"]
        compressed_tokens = result["compressed_tokens"]

        print(f"📉 Compressed {original_tokens} tokens → {compressed_tokens} tokens")
        return compressed_text
