import pdfplumber
import pytesseract

from PIL import Image


pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def extract_text(filepath: str):

    if filepath.lower().endswith(".pdf"):
        return extract_pdf(filepath)

    elif filepath.lower().endswith(
        (".png", ".jpg", ".jpeg")
    ):
        return extract_image(filepath)

    return ""


def extract_pdf(filepath: str):
    text = ""

    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()

            if extracted:
                text += extracted + "\n"

    return text


def extract_image(filepath: str):
    image = Image.open(filepath)

    return pytesseract.image_to_string(image)