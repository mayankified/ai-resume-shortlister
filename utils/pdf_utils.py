import fitz  # PyMuPDF

def extract_text_from_pdf(uploaded_file) -> str:
    text = ""

    # Streamlit file → bytes
    pdf_bytes = uploaded_file.read()

    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    for page in doc:
        text += page.get_text("text") + "\n"

    return text.strip()
