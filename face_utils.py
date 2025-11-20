import random

def generate_fake_embedding():
    return ",".join(str(random.random()) for _ in range(128))

def compare_embeddings(e1, e2):
    return random.choice([True, False])
