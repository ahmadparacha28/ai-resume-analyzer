import PyPDF2
import docx

def extract_text_from_pdf(file):
    text = ""
    pdf_reader = PyPDF2.PdfReader(file)

    for page in pdf_reader.pages:
        text += page.extract_text()

    return text


def extract_text_from_docx(file):
    text = ""
    doc = docx.Document(file)

    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"

    return text