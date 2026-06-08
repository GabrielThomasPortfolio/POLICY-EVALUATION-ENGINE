from dotenv import load_dotenv
import pypdf
from docx import Document

def extract_text_from_file(uploaded_file):
    """Securely extract text based on the file extension."""
    file_ext = uploaded_file.name.split('.')[-1].lower()
    
    if file_ext == "txt":
        raw_bytes = uploaded_file.read()
        try:
            return raw_bytes.decode("utf-8")
        except UnicodeDecodeError:
            try:
                return raw_bytes.decode("utf-8-sig")
            except UnicodeDecodeError:
                return raw_bytes.decode("cp1252", errors="replace")
                
    elif file_ext == "pdf":
        reader = pypdf.PdfReader(uploaded_file)
        # Extract text and filter out any None values from blank pages
        return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
        
    elif file_ext == "docx":
        doc = Document(uploaded_file)
        return "\n".join([para.text for para in doc.paragraphs])
        
    return ""