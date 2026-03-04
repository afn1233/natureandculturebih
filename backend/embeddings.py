# embeddings.py - Generates vector embeddings for text
# Embeddings are numerical representations of text that capture meaning
# Similar texts will have similar embeddings, enabling semantic search
# We use sentence-transformers which runs locally - completely free, no API key needed!

from sentence_transformers import SentenceTransformer

# Load the model once when the app starts
# all-MiniLM-L6-v2 is fast, lightweight and produces 384-dimensional vectors
model = SentenceTransformer('all-MiniLM-L6-v2')


async def generate_embedding(text: str) -> list[float]:
    """
    Convert text into a vector embedding.
    
    Example: "Stari Most bridge in Mostar" becomes [0.123, -0.456, 0.789, ...]
    These numbers capture the meaning of the text so we can find
    similar content later using cosine similarity search.
    """
    try:
        # encode() returns a numpy array, we convert to Python list for storage
        embedding = model.encode(text)
        return embedding.tolist()
    except Exception as e:
        raise Exception(f"Failed to generate embedding: {str(e)}")