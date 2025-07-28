from OCR.ocr_module import extract_text_from_image
from Braille.braille_module import BrailleConverter

image_path = "images.jpg"

# Get full text
text = extract_text_from_image(image_path)
print("Full Text:\n", text)

# Get words as list
word_list = extract_text_from_image(image_path, as_list=True)
print("Words List:\n", word_list)

# Test BrailleConverter
converter = BrailleConverter(text)
braille = converter.get_braille()

def braille_to_str(braille_char):
    # Represent braille dots as string, e.g. "100000"
    return ''.join(str(dot) for dot in braille_char)

print("\nBraille Representation (per character):")
for char, braille_char in zip(text, braille):
    print(f"'{char}': {braille_to_str(braille_char)}")

# Test pagination
page_size = 12
pages = converter.paginate(page_size)
print(f"\nPaginated Braille (page size {page_size}):")
for i, page in enumerate(pages):
    page_str = ' '.join(braille_to_str(b) for b in page)
    print(f"Page {i+1}:\n{page_str}\n")

if word_list:
    first_word = word_list[0]
    print(f"\nBraille grid for word: '{first_word}'")

    # Use converter to get braille for the word
    braille_chars = converter._convert_to_braille(first_word.lower())

    closed = "●"
    open_ = "○"

    rows = []
    for row in range(3):
        line = []
        for braille_char in braille_chars:
            left = closed if braille_char[row] else open_
            right = closed if braille_char[row+3] else open_
            line.append(left + " " + right)
        rows.append("  ".join(line))

    print("\n".join(rows))