from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Union
from functools import lru_cache

class EmbeddingService:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.dimension = 384
    
    def embed(self, text: str) -> np.ndarray:
        return self.model.encode(text, convert_to_numpy=True)
    
    def embed_documents(self, texts: List[str], batch_size: int = 32) -> np.ndarray:
        return self.model.encode(texts, batch_size=batch_size, convert_to_numpy=True)
    
    @lru_cache(maxsize=1000)
    def embed_cached(self, text: str) -> np.ndarray:
        return self.embed(text)
