from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text(file):
    try:
        image = Image.open(file)

        # 🔥 CRITICAL IMPROVEMENT
        image = image.convert("L")  # grayscale

        # Improve contrast (IMPORTANT)
        import numpy as np
        image = np.array(image)
        image = (image > 150) * 255  # thresholding
        image = Image.fromarray(image.astype('uint8'))

        text = pytesseract.image_to_string(image)

        print("OCR DEBUG:", text)  # DEBUG

        return text

    except Exception as e:
        print("OCR error:", e)
        return ""