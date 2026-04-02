import pytesseract
from PIL import image
import tempfile

def extract_text(file):
    with tempfile.NamedTemporaryFile(delete=False) as temp:
        