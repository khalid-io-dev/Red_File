import faiss
import numpy as np
import pickle
from typing import List, Tuple, Optional
from pathlib import Path

class FAISSService:
    def __init__(self, dimension: int = 384, index_path: Optional[str] = None):
        self.dimension = dimension
        self.index_path = index_path
        
        if index_path and Path(index_path).exists():
            self.load(index_path)
        else:
            self.index = faiss.IndexFlatL2(dimension)
            self.ids = []
    
    def add(self, embeddings: np.ndarray, ids: List[int]):
        if embeddings.shape[1] != self.dimension:
            raise ValueError(f"Embedding dimension {embeddings.shape[1]} != {self.dimension}")
        
        self.index.add(embeddings.astype('float32'))
        self.ids.extend(ids)
    
    def search(self, query_embedding: np.ndarray, k: int = 5) -> List[Tuple[int, float]]:
        if query_embedding.ndim == 1:
            query_embedding = query_embedding.reshape(1, -1)
        
        distances, indices = self.index.search(query_embedding.astype('float32'), k)
        
        results = []
        for idx, dist in zip(indices[0], distances[0]):
            if idx < len(self.ids):
                results.append((self.ids[idx], float(dist)))
        
        return results
    
    def save(self, path: str):
        faiss.write_index(self.index, f"{path}.index")
        with open(f"{path}.ids", 'wb') as f:
            pickle.dump(self.ids, f)
    
    def load(self, path: str):
        self.index = faiss.read_index(f"{path}.index")
        with open(f"{path}.ids", 'rb') as f:
            self.ids = pickle.load(f)
    
    def size(self) -> int:
        return self.index.ntotal
