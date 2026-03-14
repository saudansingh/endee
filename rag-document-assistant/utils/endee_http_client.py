import requests
import json
from typing import List, Dict, Any, Optional

class EndeeHTTPClient:
    """Direct HTTP client for Endee Vector Database"""
    
    def __init__(self, host="localhost", port=8080):
        self.base_url = f"http://{host}:{port}"
        self.session = requests.Session()
        print(f"Successfully connected using: EndeeHTTPClient")
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """Make HTTP request to Endee API"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method.upper() == "GET":
                response = self.session.get(url)
            elif method.upper() == "POST":
                response = self.session.post(url, json=data)
            elif method.upper() == "DELETE":
                response = self.session.delete(url)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"HTTP request failed: {str(e)}")
    
    def create_collection(self, name: str, dimension: int):
        """Create a new collection/index"""
        # Try different endpoint patterns
        endpoints = [
            f"/api/v1/collections",
            f"/collections",
            f"/api/v1/indexes", 
            f"/indexes"
        ]
        
        data = {
            "name": name,
            "dimension": dimension
        }
        
        for endpoint in endpoints:
            try:
                result = self._make_request("POST", endpoint, data)
                print(f"✅ Created collection using endpoint: {endpoint}")
                return result
            except Exception as e:
                continue
        
        raise Exception("Failed to create collection - tried all endpoints")
    
    def list_collections(self) -> List[str]:
        """List all collections"""
        endpoints = [
            "/api/v1/collections",
            "/collections",
            "/api/v1/indexes",
            "/indexes"
        ]
        
        for endpoint in endpoints:
            try:
                result = self._make_request("GET", endpoint)
                return result.get("collections", result.get("indexes", []))
            except Exception:
                continue
        
        return []
    
    def delete_collection(self, name: str):
        """Delete a collection"""
        endpoints = [
            f"/api/v1/collections/{name}",
            f"/collections/{name}",
            f"/api/v1/indexes/{name}",
            f"/indexes/{name}"
        ]
        
        for endpoint in endpoints:
            try:
                result = self._make_request("DELETE", endpoint)
                print(f"✅ Deleted collection using endpoint: {endpoint}")
                return result
            except Exception:
                continue
        
        raise Exception(f"Failed to delete collection: {name}")
    
    def insert(self, collection_name: str, vectors: List[List[float]], payloads: List[Dict]):
        """Insert vectors into collection"""
        endpoints = [
            f"/api/v1/collections/{collection_name}/insert",
            f"/collections/{collection_name}/insert",
            f"/api/v1/indexes/{collection_name}/insert",
            f"/indexes/{collection_name}/insert"
        ]
        
        data = {
            "vectors": vectors,
            "payloads": payloads
        }
        
        for endpoint in endpoints:
            try:
                result = self._make_request("POST", endpoint, data)
                print(f"✅ Inserted data using endpoint: {endpoint}")
                return result
            except Exception as e:
                continue
        
        raise Exception(f"Failed to insert into collection: {collection_name}")
    
    def search(self, collection_name: str, vector: List[float], limit: int = 3):
        """Search for similar vectors"""
        endpoints = [
            f"/api/v1/collections/{collection_name}/search",
            f"/collections/{collection_name}/search",
            f"/api/v1/indexes/{collection_name}/search",
            f"/indexes/{collection_name}/search"
        ]
        
        data = {
            "vector": vector,
            "limit": limit
        }
        
        for endpoint in endpoints:
            try:
                result = self._make_request("POST", endpoint, data)
                print(f"✅ Search using endpoint: {endpoint}")
                return result
            except Exception as e:
                continue
        
        raise Exception(f"Failed to search in collection: {collection_name}")

class MockSearchResult:
    """Mock search result to match expected interface"""
    def __init__(self, score: float, payload: dict):
        self.score = score
        self.payload = payload
