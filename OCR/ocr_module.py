from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_image(image_path, as_list=False, lang='eng'):
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img, lang=lang)
        
        if as_list:
            words = text.split()
            return words
        return text.strip()
    
    except Exception as e:
        print(f"Error processing image: {e}")
        return None