import re
from typing import List, Tuple, Optional

class SearchResult:
    """Container for search results with score and payload"""
    def __init__(self, score: float, payload: dict):
        self.score = score
        self.payload = payload

class RAGEngine:
    """Retrieval Augmented Generation Engine using Endee"""
    
    def __init__(self, embedder, vector_store):
        self.embedder = embedder
        self.vector_store = vector_store
        self.collection_name = "docs_collection"
    
    def semantic_search(self, query: str, top_k: int = 5) -> List[SearchResult]:
        """
        Perform semantic search on the document collection
        
        Args:
            query: Search query string
            top_k: Number of top results to return
            
        Returns:
            List of SearchResult objects
        """
        try:
            # Create query embedding
            query_embedding = self.embedder.encode([query])[0]
            
            # Search in vector store
            raw_results = self.vector_store.search(
                self.collection_name, 
                query_embedding, 
                limit=top_k
            )
            
            # Convert to SearchResult objects
            search_results = []
            for result in raw_results:
                if hasattr(result, 'score') and hasattr(result, 'payload'):
                    search_results.append(SearchResult(result.score, result.payload))
                elif isinstance(result, dict):
                    search_results.append(SearchResult(result.get('score', 0.0), result.get('payload', {})))
            
            return search_results
            
        except Exception as e:
            print(f"Search error: {str(e)}")
            return []
    
    def answer_question(self, question: str, top_k: int = 3) -> Tuple[str, str, List[SearchResult]]:
        """
        Answer a question using RAG approach
        
        Args:
            question: User's question
            top_k: Number of relevant chunks to retrieve
            
        Returns:
            Tuple of (answer, context, sources)
        """
        try:
            # Retrieve relevant documents
            search_results = self.semantic_search(question, top_k)
            
            if not search_results:
                return "", "No relevant information found.", []
            
            # Combine context from top results
            context_chunks = []
            sources = []
            
            for result in search_results:
                text = result.payload.get('text', '').strip()
                if text:
                    context_chunks.append(text)
                    sources.append(result)
            
            if not context_chunks:
                return "", "No readable content found in retrieved documents.", search_results
            
            context = "\n\n---\n\n".join(context_chunks)
            
            # Generate answer based on context
            answer = self._generate_answer(question, context, search_results)
            
            return answer, context, sources[:3]  # Return top 3 sources
            
        except Exception as e:
            print(f"RAG error: {str(e)}")
            return "", f"Error processing question: {str(e)}", []
    
    def _generate_answer(self, question: str, context: str, sources: List[SearchResult]) -> str:
        """
        Generate an answer based on the question and retrieved context
        
        Args:
            question: User's question
            context: Retrieved context text
            sources: List of search results with scores
            
        Returns:
            Generated answer string
        """
        if not context.strip():
            return "I couldn't find relevant information to answer your question."
        
        # Simple answer generation - in a real implementation, you'd use an LLM
        # For this demo, we'll extract relevant sentences and provide context
        answer = self._extract_relevant_info(question, context)
        
        # Add confidence based on source scores
        if sources:
            avg_score = sum(s.score for s in sources) / len(sources)
            confidence = "high" if avg_score > 0.8 else "medium" if avg_score > 0.6 else "low"
            answer += f"\n\n*Confidence: {confidence} (based on similarity scores: {[f'{s.score:.3f}' for s in sources[:3]]})*"
        
        return answer
    
    def _extract_relevant_info(self, question: str, context: str) -> str:
        """
        Extract relevant information from context based on the question
        
        Args:
            question: User's question
            context: Retrieved context text
            
        Returns:
            Relevant information string
        """
        # Split context into sentences
        sentences = re.split(r'[.!?]+', context)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # Extract keywords from question
        question_words = set(re.findall(r'\b\w+\b', question.lower()))
        
        # Score sentences based on keyword overlap
        scored_sentences = []
        for sentence in sentences:
            sentence_words = set(re.findall(r'\b\w+\b', sentence.lower()))
            overlap = len(question_words.intersection(sentence_words))
            scored_sentences.append((overlap, sentence))
        
        # Sort by score and take top sentences
        scored_sentences.sort(reverse=True, key=lambda x: x[0])
        
        if not scored_sentences or scored_sentences[0][0] == 0:
            return "Based on the provided documents, I found relevant information but couldn't extract a specific answer. Here's the context:\n\n" + context[:500] + "..." if len(context) > 500 else context
        
        # Take top 3-5 sentences
        top_sentences = [s[1] for s in scored_sentences[:5] if s[0] > 0]
        
        if not top_sentences:
            return "I found some information that might be related to your question:\n\n" + context[:300] + "..." if len(context) > 300 else context
        
        answer = "Based on the documents, here's what I found:\n\n"
        answer += ". ".join(top_sentences[:3]) + "."
        
        return answer
    
    def get_collection_stats(self) -> dict:
        """Get statistics about the current collection"""
        try:
            # This is a placeholder - in a real implementation, 
            # you'd query Endee for collection statistics
            return {
                "collection_name": self.collection_name,
                "document_count": 0,  # Would be populated from Endee
                "total_chunks": 0,   # Would be populated from Endee
                "embedding_dimension": self.embedder.dimension
            }
        except Exception as e:
            return {"error": str(e)}
    
    def health_check(self) -> bool:
        """Check if the RAG engine is properly connected"""
        try:
            # Try a simple search to verify connection
            test_results = self.semantic_search("test", limit=1)
            return True
        except Exception as e:
            print(f"Health check failed: {str(e)}")
            return False
