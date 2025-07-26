from OCR.ocr_module import extract_text_from_image


image_path = "IMG_4160.jpg"

# Get full text
text = extract_text_from_image(image_path)
print("Full Text:\n", text)

# Get words as list
word_list = extract_text_from_image(image_path, as_list=True)
print("Words List:\n", word_list)