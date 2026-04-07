from PIL import Image
import pytesseract
import cv2
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text(file):
    # Convert to OpenCV format
    image = Image.open(file).convert("RGB")
    img = np.array(image)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply threshold (VERY IMPORTANT)
    thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]

    # OCR with better config
    text = pytesseract.image_to_string(thresh, config="--psm 6")

    return text