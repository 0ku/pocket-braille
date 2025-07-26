from PIL import Image, ImageFilter
import pytesseract

# Set tesseract path (Windows only)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def preprocess_image(image_path, show=True):
    """
    Load, grayscale, scale up, and apply unsharp mask.
    Optionally display the processed image.
    """
    try:
        img = Image.open(image_path)

        # Convert to grayscale
        img = img.convert("L")

        # Resize to at least height 2000px (keep aspect ratio)
        target_height = 2000
        scale_factor = target_height / img.height
        new_width = int(img.width * scale_factor)
        img = img.resize((new_width, target_height), resample=Image.LANCZOS)

        # Apply Unsharp Mask
        img = img.filter(ImageFilter.UnsharpMask(radius=6.8, percent=269, threshold=0))

        if show:
            img.show(title="Preprocessed Image")

        return img
    except Exception as e:
        print(f"Error during preprocessing: {e}")
        return None

def extract_text_from_image(image_path, as_list=False, lang='eng', show_image=True):
    """
    Perform OCR on a preprocessed image. Optionally show it.
    """
    try:
        img = preprocess_image(image_path, show=show_image)
        if img is None:
            return None

        text = pytesseract.image_to_string(img, lang=lang)

        if as_list:
            return text.split()
        return text.strip()

    except Exception as e:
        print(f"Error processing image: {e}")
        return None

# Optional CLI usage
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python ocr_module.py <image_path>")
    else:
        result = extract_text_from_image(sys.argv[1], show_image=True)
        print("Extracted Text:\n", result)
