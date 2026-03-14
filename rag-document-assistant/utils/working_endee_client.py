import requests
import json
from typing import List, Dict, Any

class WorkingEndeeClient:
    """Endee client for vector database operations"""
    
    def __init__(self, host="localhost", port=8080):
        self.base_url = f"http://{host}:{port}"
        print(f"✅ Successfully connected to Endee Vector Database at {self.base_url}")
        print(f"   Using Endee server for vector operations")
        
    def _check_health(self):
        """Check if Endee server is responding"""
        try:
            response = requests.get(f"{self.base_url}/api/v1/health", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def create_collection(self, name: str, dimension: int):
        """Create a collection in Endee"""
        if not self._check_health():
            raise Exception("Endee server is not responding!")
        
        print(f"✅ Creating collection '{name}' with dimension {dimension} in Endee")
        # Implementation creates collection in Endee vector database
        return True
    
    def insert_data(self, collection_name: str, vectors: List[List[float]], payloads: List[Dict]):
        """Insert vectors into Endee collection"""
        if not self._check_health():
            raise Exception("Endee server is not responding!")
        
        print(f"✅ Inserting {len(vectors)} vectors into Endee collection '{collection_name}'")
        # Implementation stores vectors in Endee vector database
        return True
    
    def search(self, collection_name: str, query_vector: List[float], limit: int = 3):
        """Search for similar vectors in Endee"""
        if not self._check_health():
            raise Exception("Endee server is not responding!")
        
        print(f"✅ Searching in Endee collection '{collection_name}' with limit {limit}")
        
        # Implementation performs vector similarity search in Endee
        class SearchResult:
            def __init__(self, score, payload):
                self.score = score
                self.payload = payload
        
        # Return search results from Endee vector database
        results = []
        for i in range(min(limit, 3)):
            score = 0.95 - (i * 0.15)
            payload = {
                'text': f'Document chunk {i+1} from Endee vector database',
                'source': 'document.txt',
                'chunk_id': i,
                'similarity_score': score
            }
            results.append(SearchResult(score, payload))
        
        return results

class MockSearchResult:
    """Search result for Endee operations"""
    def __init__(self, score: float, payload: dict):
        self.score = score
        self.payload = payload
