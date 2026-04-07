import pytesseract
from PIL import Image
import io

# Force path to Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text(file):
    try:
        image = Image.open(io.BytesIO(file))

        text = pytesseract.image_to_string(image)

        print("OCR TEXT:", text)

        if text.strip() == "":
            return "EMPTY_OCR"

        return text

    except Exception as e:
        print("OCR ERROR:", str(e))
        return "ERROR"