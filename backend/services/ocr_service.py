import pytesseract
from PIL import Image
import tempfile
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
def extract_text(file):
    with tempfile.NamedTemporaryFile(delete=False) as temp:
        temp.write(file.file.read())
        temp_path=temp.name

    try:
        image=Image.open(temp_path)
        text=pytesseract.image_to_string(image)
    except:
        text=""
        
    finally:
        import os
        os.remove(temp_path)
    return text