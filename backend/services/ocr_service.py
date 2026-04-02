import pytesseract
from PIL import image
import tempfile

def extract_text(file):
    with tempfile.NamedTemporaryFile(delete=False) as temp:
        temp.write(file.file.read())
        temp_path=temp.name

    try:
        image=Image.open(temp_path)
        text=pytesseract.image_to_string(image)
    finally:
        import os
        os.remove(temp_path)
    return text