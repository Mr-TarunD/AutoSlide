import pdfplumber
import io

def extract_text_from_pdf(pdf_file_object):
    """
    Extracts text from an uploaded PDF file object.

    Args:
        pdf_file_object: A file-like object (e.g., from st.file_uploader).

    Returns:
        A string containing all extracted text.
    
    Raises:
        Exception: If the PDF is password-protected or unreadable.
    """
    text = ""
    try:
        # pdfplumber.open() can handle file-like objects directly
        with pdfplumber.open(pdf_file_object) as pdf:
            if not pdf.pages:
                raise ValueError("PDF has no pages.")
                
            for i, page in enumerate(pdf.pages):
                page_text = page.extract_text()
                if page_text:
                    text += f"--- Page {i+1} ---\n"
                    text += page_text + "\n\n"
        
        if not text:
             raise ValueError("Could not extract any text. The PDF might be image-based (scanned).")
             
        return text

    except Exception as e:
        # Catch specific pdfplumber exceptions if known, else general
        if "password" in str(e).lower():
            raise Exception("Cannot read password-protected PDF.")
        else:
            raise Exception(f"Error reading PDF: {e}")