import sys
from PIL import Image, ImageFilter
import cv2
from matplotlib import pyplot as plt
import pytesseract
import numpy as np
from scipy.ndimage import interpolation as inter

# Set tesseract path (Windows only)
if sys.platform.startswith("win"):
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
elif sys.platform == "darwin":
    # Common Homebrew install location for macOS
    pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"

def correct_skew(image, delta=1, limit=5):
    def determine_score(arr, angle):
        data = inter.rotate(arr, angle, reshape=False, order=0)
        histogram = np.sum(data, axis=1, dtype=float)
        score = np.sum((histogram[1:] - histogram[:-1]) ** 2, dtype=float)
        return histogram, score

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1] 

    scores = []
    angles = np.arange(-limit, limit + delta, delta)
    for angle in angles:
        histogram, score = determine_score(thresh, angle)
        scores.append(score)

    best_angle = angles[scores.index(max(scores))]

    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, best_angle, 1.0)
    corrected = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, \
            borderMode=cv2.BORDER_REPLICATE)

    return best_angle, corrected

from PIL import Image, ImageFilter
import cv2
import numpy as np

from PIL import Image, ImageFilter
import cv2
import numpy as np

def preprocess_image(image_path, show=True):
    """
    1. Load image with OpenCV.
    2. Correct skew.
    3. Find and crop to contour area.
    4. Convert to PIL.
    5. Grayscale, resize to 2000px height, and apply unsharp mask.
    6. Optionally display processed image.
    7. Return processed PIL image ready for Tesseract OCR.
    """
    try:
        # Step 1: Load and correct skew
        image = cv2.imread(image_path)
        angle, corrected = correct_skew(image)

        # Step 2: Find contours
        gray = cv2.cvtColor(corrected, cv2.COLOR_BGR2GRAY)
        contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            print("found contours")
            # Find bounding box around all contours
            x_min, y_min, x_max, y_max = np.inf, np.inf, -np.inf, -np.inf
            for cnt in contours:
                x, y, w, h = cv2.boundingRect(cnt)
                x_min = min(x_min, x)
                y_min = min(y_min, y)
                x_max = max(x_max, x + w)
                y_max = max(y_max, y + h)

            # Crop to the bounding box
            corrected = corrected[int(y_min):int(y_max), int(x_min):int(x_max)]

        # Step 3: Convert to PIL (after cropping)
        corrected_rgb = cv2.cvtColor(corrected, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(corrected_rgb)

        # Step 4: Grayscale
        pil_img = pil_img.convert("L")

        # Step 5: Resize to height = 2000 (maintain aspect ratio)
        target_height = 2000
        scale_factor = target_height / pil_img.height
        new_width = int(pil_img.width * scale_factor)
        pil_img = pil_img.resize((new_width, target_height), resample=Image.LANCZOS)

        # Step 6: Apply Unsharp Mask
        pil_img = pil_img.filter(ImageFilter.UnsharpMask(radius=6.8, percent=269, threshold=0))

        # Step 7: Show result if requested
        if show:
            pil_img.show(title="Preprocessed Image")

        return pil_img

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

        text = pytesseract.image_to_string(img, nice=1, lang=lang)

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
