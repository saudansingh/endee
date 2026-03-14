from utils.working_endee_client import WorkingEndeeClient

class EndeeStore:
    def __init__(self, host="localhost", port=8080):
        # Use working Endee client that demonstrates real integration
        self.client = WorkingEndeeClient(host, port)
        print(f"Successfully connected using: {self.client.__class__.__name__}")

    def create_collection(self, name, dim):
        # Create collection using working Endee client
        return self.client.create_collection(name, dim)

    def insert_data(self, name, vectors, payloads):
        # Insert data using working Endee client
        return self.client.insert(name, vectors, payloads)

    def search(self, name, query_vector, limit=3):
        # Search using working Endee client
        return self.client.search(name, query_vector, limit)