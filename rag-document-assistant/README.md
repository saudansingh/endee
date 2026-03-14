Document Assistant (RAG + Endee)

Project Overview and Problem Statement

This project addresses the challenge of efficiently searching and extracting information from large document collections. Traditional keyword-based search often fails to understand context and semantic meaning, making it difficult to find relevant information across multiple documents. 

The solution is a Retrieval Augmented Generation (RAG) system that uses Endee vector database to enable semantic search and intelligent question answering. Users can upload documents in various formats, search using natural language queries, and receive context-aware answers with source attribution.

System Design and Technical Approach

The system follows a modular architecture with clear separation of concerns:

Core Components
- Document Processing Layer: Handles multi-format file ingestion and text extraction
- Embedding Layer: Converts text chunks into 384-dimensional vectors using SentenceTransformers
- Vector Database Layer: Uses Endee for persistent storage and similarity search
- Application Layer: Streamlit-based web interface for user interaction
- RAG Pipeline: Coordinates retrieval and answer generation

Data Flow Architecture
1. Document Upload → Format Validation → Text Extraction
2. Text Extraction → Chunking Strategy (500 chars, 50 overlap) → Vector Embedding
3. Vector Embedding → Endee Storage with Metadata
4. User Query → Embedding → Vector Search in Endee → Context Retrieval
5. Context Retrieval → Answer Generation → Response with Sources

Technology Stack
- Frontend: Streamlit for responsive web interface
- Text Processing: PyPDF2, python-docx, striprtf for multi-format support
- Embeddings: SentenceTransformers (all-MiniLM-L6-v2, 384 dimensions)
- Vector Database: Endee for high-performance storage and retrieval
- Chunking: LangChain text splitters for intelligent document segmentation

Endee Integration Explanation

Endee serves as the core vector database component:

Collection Management
- Creates named collections for document organization
- Handles vector dimension specifications (384-dim)
- Supports collection deletion and recreation

Vector Operations
- Stores document embeddings with metadata
- Performs cosine similarity search
- Returns ranked results with similarity scores
- Manages persistent storage across sessions

Search Capabilities
- Real-time semantic search using vector embeddings
- Top-k retrieval with configurable limits
- Context-aware matching across document collections
- Efficient similarity calculations

Clear Setup and Execution Instructions

Prerequisites
- Python 3.8 or higher
- Endee vector database server running on localhost:8080
- Git for repository cloning

Installation Steps

Step 1: Project Setup
```bash
git clone <repository-url>
cd rag-document-assistant
```

Step 2: Dependencies
```bash
pip install -r requirements.txt
```

Step 3: Endee Server
```bash
cd ..
docker run -p 8080:8080 endeeio/endee-server:latest
```

Step 4: Application Launch
```bash
streamlit run app.py
```

Access the application at http://localhost:8501

Usage Instructions

Document Upload
1. Open the web interface
2. Use the file uploader to add documents (PDF, DOCX, TXT, MD, RTF)
3. Monitor processing progress and validation
4. Documents are automatically chunked and embedded

Semantic Search
1. Enter search queries in natural language
2. System converts queries to vector embeddings
3. Searches Endee for semantically similar content
4. Results are ranked by similarity score

Question Answering
1. Ask questions in the Q&A interface
2. System retrieves relevant document chunks from Endee
3. Generates context-aware answers
4. Responses include source attribution and confidence scores

Project Structure

```
rag-document-assistant/
├── app.py                    # Main Streamlit application
├── requirements.txt           # Python dependencies
├── utils/
│   ├── embedding.py          # Text embedding functionality
│   ├── vector_store.py       # Endee integration
│   ├── document_processor.py # Multi-format processing
│   └── rag_engine.py         # RAG pipeline
├── data/                     # Document storage
├── sample_documents/         # Example files for testing
└── README.md                # This documentation
```

Key Features

Multi-Format Support
- Text files (.txt, .md)
- PDF documents (.pdf)
- Word documents (.docx)
- Rich Text Format (.rtf)
- Automatic format detection and validation

Search Capabilities
- Vector similarity search with cosine similarity
- Real-time retrieval with similarity scores
- Top-k results with configurable limits
- Cross-document semantic matching

Answer Generation
- Context-aware response generation
- Source attribution with document references
- Confidence scoring for result quality
- Support for follow-up questions

System Requirements

Minimum Requirements
- Python 3.8+
- 4GB RAM (8GB recommended)
- 2GB available disk space
- Network access to Endee server

Recommended Setup
- Python 3.9+
- 8GB+ RAM
- SSD storage for optimal performance
- Dedicated Endee server instance

Troubleshooting

Common Issues and Solutions
- Endee Connection: Ensure Docker container is running on port 8080
- Memory Errors: Reduce document size or adjust chunking parameters
- Slow Search: Check Endee server performance and network connectivity
- File Processing: Verify document format and file integrity

Debug Mode
- Enable verbose logging in the application
- Monitor Endee server logs for connection issues
- Check system resource utilization

This project provides a complete solution for document processing, semantic search, and question answering using Endee as the foundational vector database component.
