import random
import time
from typing import List, Dict, Any

class MockSearchResult:
    """Mock search result for testing without Endee"""
    def __init__(self, score: float, payload: dict):
        self.score = score
        self.payload = payload

class MockEndeeStore:
    """Mock Endee store for testing when Endee server is not available"""
    
    def __init__(self, host="localhost", port=8080):
        self.host = host
        self.port = port
        self.collections = {}
        print(f"🔧 Using Mock Endee Store (server not required)")
        print(f"   This is for demonstration purposes")
    
    def create_collection(self, name: str, dim: int):
        """Create a mock collection"""
        self.collections[name] = {
            'vectors': [],
            'payloads': [],
            'dimension': dim
        }
        print(f"✅ Created mock collection: {name} (dimension: {dim})")
    
    def insert_data(self, name: str, vectors: List[List[float]], payloads: List[Dict[str, Any]]):
        """Insert mock data"""
        if name not in self.collections:
            self.create_collection(name, len(vectors[0]) if vectors else 384)
        
        collection = self.collections[name]
        collection['vectors'].extend(vectors)
        collection['payloads'].extend(payloads)
        print(f"✅ Inserted {len(vectors)} vectors into {name}")
    
    def search(self, name: str, query_vector: List[float], limit: int = 3) -> List[MockSearchResult]:
        """Mock search with random similarity scores"""
        if name not in self.collections:
            return []
        
        collection = self.collections[name]
        if not collection['payloads']:
            return []
        
        # Return random results with decreasing similarity scores
        results = []
        available_payloads = collection['payloads']
        
        for i in range(min(limit, len(available_payloads))):
            score = 0.9 - (i * 0.1) - random.uniform(0, 0.1)  # Decreasing scores with some randomness
            score = max(0.1, score)  # Ensure score is positive
            
            # Select a random payload
            payload = available_payloads[i % len(available_payloads)]
            results.append(MockSearchResult(score, payload))
        
        return results

def get_vector_store():
    """Get either real Endee store or mock store"""
    try:
        # Try to import and use real Endee store
        from utils.vector_store import EndeeStore
        store = EndeeStore()
        # Test connection
        store.create_collection("test", 384)
        return store
    except Exception as e:
        print(f"⚠️  Endee server not available: {str(e)}")
        print("🔄 Using mock store for demonstration")
        return MockEndeeStore()
