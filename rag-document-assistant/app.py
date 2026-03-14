import streamlit as st
import os
import time
from utils.document_processor import DocumentProcessor
from utils.embedding import Embedder
from utils.vector_store import EndeeStore
from utils.rag_engine import RAGEngine

st.set_page_config(
    page_title="Document Assistant - RAG with Endee",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📚 Document Assistant")
st.markdown("*Powered by Endee Vector Database*")

@st.cache_resource
def initialize_components():
    """Initialize all components with caching"""
    try:
        embedder = Embedder()
        store = EndeeStore()  # Endee vector store
        rag_engine = RAGEngine(embedder, store)
        doc_processor = DocumentProcessor()
        return embedder, store, rag_engine, doc_processor
    except Exception as e:
        st.error(f"❌ Failed to initialize Endee Vector Database: {str(e)}")
        st.error("🔧 Endee server must be running on localhost:8080")
        st.info("💡 Please start Endee server first:")
        st.code("cd .. && ./run.sh")
        return None, None, None, None

def main():
    embedder, store, rag_engine, doc_processor = initialize_components()
    
    if not all([embedder, store, rag_engine, doc_processor]):
        st.error("❌ Cannot proceed without Endee Vector Database")
        st.error("🔧 Endee is required for this project")
        st.info("📖 Setup instructions:")
        st.markdown("""
        1. **Build Endee:**
           ```bash
           cd ..
           ./install.sh --release --avx2
           ```
        
        2. **Start Endee Server:**
           ```bash
           ./run.sh
           ```
        
        3. **Verify Endee is running:**
           - Check that server is on localhost:8080
           - You should see "Successfully connected" message
        """)
        st.stop()

    with st.sidebar:
        st.header("📚 Document Management")
        
        uploaded_files = st.file_uploader(
            "Upload Documents",
            type=['txt', 'pdf', 'docx', 'md', 'rtf'],
            accept_multiple_files=True,
            help="Supported formats: TXT, PDF, DOCX, MD, RTF"
        )
        
        if uploaded_files and st.button("📥 Process Documents", type="primary"):
            process_documents(uploaded_files, doc_processor, embedder, store)
        
        st.divider()
        
        if st.button("🗑️ Clear All Documents", type="secondary"):
            clear_documents(store)
        
        st.divider()
        
        collection_info = get_collection_info(store)
        if collection_info:
            st.metric("📄 Documents Indexed", collection_info.get('document_count', 0))
            st.metric("🔍 Chunks Stored", collection_info.get('chunk_count', 0))

    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("🔍 Semantic Search")
        
        search_query = st.text_input(
            "Search for similar content:",
            placeholder="Enter keywords or phrases...",
            key="search_query"
        )
        
        if st.button("🔎 Search", type="primary", key="search_btn"):
            if search_query:
                with st.spinner("🔍 Searching documents..."):
                    perform_semantic_search(search_query, rag_engine)
            else:
                st.warning("Please enter a search query")
    
    with col2:
        st.header("🤖 Ask Questions (RAG)")
        
        question = st.text_input(
            "Ask about your documents:",
            placeholder="What would you like to know?",
            key="question"
        )
        
        if st.button("💬 Get Answer", type="primary", key="ask_btn"):
            if question:
                with st.spinner("🤖 Thinking..."):
                    perform_rag_query(question, rag_engine)
            else:
                st.warning("Please enter a question")

def process_documents(uploaded_files, doc_processor, embedder, store):
    """Process uploaded documents and store in Endee"""
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        all_chunks = []
        all_metadata = []
        
        for i, file in enumerate(uploaded_files):
            status_text.text(f"Processing {file.name}...")
            
            with st.spinner(f"Extracting text from {file.name}..."):
                text = doc_processor.extract_text(file)
            
            if not text:
                st.warning(f"No text extracted from {file.name}")
                continue
            
            with st.spinner(f"Chunking {file.name}..."):
                chunks = doc_processor.chunk_text(text)
            
            with st.spinner(f"Creating embeddings for {file.name}..."):
                embeddings = embedder.encode(chunks)
            
            for j, chunk in enumerate(chunks):
                metadata = {
                    'text': chunk,
                    'source': file.name,
                    'chunk_id': j,
                    'total_chunks': len(chunks)
                }
                all_chunks.append(embeddings[j])
                all_metadata.append(metadata)
            
            progress_bar.progress((i + 1) / len(uploaded_files))
        
        if all_chunks:
            with st.spinner("Storing in Endee vector database..."):
                store.insert_data("docs_collection", all_chunks, all_metadata)
            
            st.success(f"✅ Successfully processed {len(uploaded_files)} documents!")
            st.info(f"📊 Total chunks stored: {len(all_chunks)}")
        else:
            st.error("❌ No content was processed")
            
    except Exception as e:
        st.error(f"❌ Error processing documents: {str(e)}")
    
    finally:
        progress_bar.empty()
        status_text.empty()

def perform_semantic_search(query, rag_engine):
    """Perform semantic search and display results"""
    try:
        results = rag_engine.semantic_search(query, top_k=5)
        
        if not results:
            st.info("🔍 No relevant content found")
            return
        
        st.subheader(f"🎯 Found {len(results)} relevant results:")
        
        for i, result in enumerate(results, 1):
            with st.expander(f"Result {i} (Score: {result.score:.4f}) - {result.payload.get('source', 'Unknown')}"):
                st.write(result.payload.get('text', ''))
                st.caption(f"Source: {result.payload.get('source', 'Unknown')} | Chunk {result.payload.get('chunk_id', 0) + 1}")
                
    except Exception as e:
        st.error(f"❌ Search error: {str(e)}")

def perform_rag_query(question, rag_engine):
    """Perform RAG query and display answer"""
    try:
        answer, context, sources = rag_engine.answer_question(question)
        
        if not answer:
            st.info("🤖 I couldn't find relevant information to answer your question")
            return
        
        st.subheader("💬 Answer")
        st.write(answer)
        
        if sources:
            st.subheader("📚 Sources")
            for i, source in enumerate(sources[:3], 1):
                with st.expander(f"Source {i} (Score: {source.score:.4f})"):
                    st.write(source.payload.get('text', '')[:500] + "..." if len(source.payload.get('text', '')) > 500 else source.payload.get('text', ''))
                    st.caption(f"From: {source.payload.get('source', 'Unknown')}")
        
        st.subheader("🔍 Retrieved Context")
        with st.expander("View Full Context"):
            st.write(context)
            
    except Exception as e:
        st.error(f"❌ Query error: {str(e)}")

def clear_documents(store):
    """Clear all documents from the collection"""
    try:
        store.create_collection("docs_collection", 384)  # Recreate collection
        st.success("✅ All documents cleared!")
        st.rerun()
    except Exception as e:
        st.error(f"❌ Error clearing documents: {str(e)}")

def get_collection_info(store):
    """Get information about the current collection"""
    try:
        # Try to get collection info - this is a simplified version
        # In a real implementation, you'd query Endee for collection stats
        return {"document_count": 0, "chunk_count": 0}
    except:
        return None

if __name__ == "__main__":
    main()