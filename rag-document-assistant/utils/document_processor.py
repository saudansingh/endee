import io
import PyPDF2
import docx
import striprtf
from langchain_text_splitters import RecursiveCharacterTextSplitter

class DocumentProcessor:
    """Multi-format document processor for text extraction and chunking"""
    
    def __init__(self, chunk_size=500, chunk_overlap=50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
    
    def extract_text(self, file):
        """Extract text from various file formats"""
        if file is None:
            return ""
        
        file_extension = file.name.lower().split('.')[-1]
        
        try:
            if file_extension == 'txt':
                return self._extract_from_txt(file)
            elif file_extension == 'md':
                return self._extract_from_txt(file)  # Markdown is treated as text
            elif file_extension == 'pdf':
                return self._extract_from_pdf(file)
            elif file_extension == 'docx':
                return self._extract_from_docx(file)
            elif file_extension == 'rtf':
                return self._extract_from_rtf(file)
            else:
                raise ValueError(f"Unsupported file format: {file_extension}")
        except Exception as e:
            raise Exception(f"Error extracting text from {file.name}: {str(e)}")
    
    def _extract_from_txt(self, file):
        """Extract text from TXT and MD files"""
        try:
            # Reset file pointer to beginning
            file.seek(0)
            content = file.read()
            
            # Handle both string and bytes
            if isinstance(content, bytes):
                content = content.decode('utf-8', errors='ignore')
            
            return content.strip()
        except Exception as e:
            raise Exception(f"Error reading text file: {str(e)}")
    
    def _extract_from_pdf(self, file):
        """Extract text from PDF files"""
        try:
            # Reset file pointer to beginning
            file.seek(0)
            
            # Create a PDF reader object
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
            
            # Extract text from all pages
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + "\n"
            
            return text.strip()
        except Exception as e:
            raise Exception(f"Error reading PDF file: {str(e)}")
    
    def _extract_from_docx(self, file):
        """Extract text from DOCX files"""
        try:
            # Reset file pointer to beginning
            file.seek(0)
            
            # Create a document object
            doc = docx.Document(io.BytesIO(file.read()))
            
            # Extract text from all paragraphs
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            return text.strip()
        except Exception as e:
            raise Exception(f"Error reading DOCX file: {str(e)}")
    
    def _extract_from_rtf(self, file):
        """Extract text from RTF files"""
        try:
            # Reset file pointer to beginning
            file.seek(0)
            
            # Read RTF content
            rtf_content = file.read()
            
            # Handle both string and bytes
            if isinstance(rtf_content, bytes):
                rtf_content = rtf_content.decode('utf-8', errors='ignore')
            
            # Strip RTF formatting
            text = striprtf.rtf_to_text(rtf_content)
            
            return text.strip()
        except Exception as e:
            raise Exception(f"Error reading RTF file: {str(e)}")
    
    def chunk_text(self, text):
        """Split text into chunks for processing"""
        if not text or not text.strip():
            return []
        
        try:
            chunks = self.text_splitter.split_text(text)
            return [chunk.strip() for chunk in chunks if chunk.strip()]
        except Exception as e:
            raise Exception(f"Error chunking text: {str(e)}")
    
    def get_supported_formats(self):
        """Get list of supported file formats"""
        return ['txt', 'md', 'pdf', 'docx', 'rtf']
    
    def validate_file(self, file):
        """Validate if file is supported"""
        if file is None:
            return False, "No file provided"
        
        file_extension = file.name.lower().split('.')[-1]
        supported_formats = self.get_supported_formats()
        
        if file_extension not in supported_formats:
            return False, f"Unsupported format: {file_extension}. Supported formats: {', '.join(supported_formats)}"
        
        # Check file size (limit to 50MB)
        if hasattr(file, 'size') and file.size > 50 * 1024 * 1024:
            return False, "File size exceeds 50MB limit"
        
        return True, "File is valid"
