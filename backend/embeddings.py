import hashlib
import math

async def generate_embedding(text: str) -> list[float]:
    embedding = []
    for i in range(1536):
        hash_input = f"{text}_{i}".encode("utf-8")
        hash_val = int(hashlib.sha256(hash_input).hexdigest(), 16)
        val = (hash_val % 1000000) / 500000.0 - 1.0
        embedding.append(val)
    magnitude = math.sqrt(sum(x**2 for x in embedding))
    if magnitude > 0:
        embedding = [x / magnitude for x in embedding]
    return embedding