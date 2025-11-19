import random

def generate_fake_embedding():
    """Returns a fake 128-length embedding string."""
    return ",".join(str(random.random()) for _ in range(128))

def compare_embeddings(emb1, emb2):
    """Fake comparison — returns True if first 5 numbers match."""
    a = emb1.split(",")
    b = emb2.split(",")
    return a[:5] == b[:5]
