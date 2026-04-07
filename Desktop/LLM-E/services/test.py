import time
from QueryInput import QueryInput
from Compressor import Compressor
from LLMService import LLM

def run_pipeline(question: str):
    print(f"\n{'='*60}")
    print(f"💬 Question: {question}")
    print(f"{'='*60}")

    # 1. retrieve
    start = time.time()
    query_service = QueryInput()
    chunks = query_service.search(question)
    retrieval_time = time.time() - start
    print(f"⏱️  Retrieval time: {retrieval_time:.2f}s")

    # 2. compress
    start = time.time()
    compressor = Compressor()
    compressed_context = compressor.compress(question, chunks)
    compression_time = time.time() - start
    print(f"⏱️  Compression time: {compression_time:.2f}s")

    # 3. answer
    start = time.time()
    llm = LLM()
    answer = llm.answer(question, compressed_context)
    llm_time = time.time() - start
    print(f"⏱️  LLM time: {llm_time:.2f}s")

    # 4. print results
    print(f"\n📝 Answer: {answer}")
    print(f"\n📊 Pipeline Summary:")
    print(f"   Retrieval:   {retrieval_time:.2f}s")
    print(f"   Compression: {compression_time:.2f}s")
    print(f"   LLM:         {llm_time:.2f}s")
    print(f"   Total:       {retrieval_time + compression_time + llm_time:.2f}s")


if __name__ == "__main__":
    questions = [
        "What was Pfizer's total revenue in 2022?",
        "What were Pfizer's COVID-19 product sales in 2022?",
        "What is Pfizer's revenue forecast for 2023?",
    ]

    for question in questions:
        run_pipeline(question)
