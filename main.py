from OCR.ocr_module import extract_text_from_image
from Braille.braille_module import BrailleConverter
import sys

def display_braille_grid(pages, converter):
    # Main program loop
    if pages == 0:
      print("OCR failed to detect text\n")
      return
    
    closed = "●"
    open_ = "○"

    def braille_cell_to_str(cell):
        return converter.decodeBrailleCell(cell)

    def render_grid(braille_chars):
        rows = []
        for row in range(3):
            line = []
            for braille_char in braille_chars:
                left = closed if braille_char[row] else open_
                right = closed if braille_char[row+3] else open_
                line.append(left + " " + right)
            rows.append("  ".join(line))
        return "\n".join(rows)

    total_pages = len(pages)
    current_page = 0

    while True:
        page = pages[current_page]
        plain_str = ''.join(braille_cell_to_str(b) for b in page).upper()

        print(f"\nBraille grid for page {current_page + 1} out of {total_pages}: '{plain_str}'")
        print(render_grid(page))

        cmd = input("\nEnter 'n' for next, 'p' for previous, or 'q' to quit: ").strip().lower()
        if cmd == 'n':
            if current_page < total_pages - 1:
                current_page += 1
            else:
                print("You are already on the last page.")
        elif cmd == 'p':
            if current_page > 0:
                current_page -= 1
            else:
                print("You are already on the first page.")
        elif cmd == 'q':
            print("Exiting.")
            break
        else:
            print("Invalid input. Please enter 'n', 'p', or 'q'.")

def braille_to_str(braille_char):
    # Represent braille dots as string, e.g. "100000"
    return ''.join(str(dot) for dot in braille_char)

if __name__ == "__main__":
  image_path = sys.argv[1] if len(sys.argv) > 1 else "images.jpg"

  # Get full text
  text = extract_text_from_image(image_path)
  print("Full Text:\n", text)

  # Get words as list
  word_list = extract_text_from_image(image_path, as_list=True)
  print("Words List:\n", word_list)

  # Test BrailleConverter
  converter = BrailleConverter(text)
  braille = converter.get_braille()


  print("\nBraille Representation (per character):")
  for char, braille_char in zip(text, braille):
      print(f"'{char}': {braille_to_str(braille_char)}")

  # Test pagination
  page_size = 8
  pages = converter.paginate(page_size)
  print(f"\nPaginated Braille (page size {page_size}):")
  for i, page in enumerate(pages):
      page_str = ' '.join(braille_to_str(b) for b in page)
      print(f"Page {i+1}:\n{page_str}")
      # debug
      plain_str = ''.join(converter.decodeBrailleCell(b) for b in page)
      print(f"{plain_str}\n")

  display_braille_grid(pages, converter)

  # if word_list:
  #     first_word = word_list[0]
  #     print(f"\nBraille grid for word: '{first_word}'")

  #     # Use converter to get braille for the word
  #     braille_chars = converter._convert_to_braille(first_word.lower())

  #     closed = "●"
  #     open_ = "○"

  #     rows = []
  #     for row in range(3):
  #         line = []
  #         for braille_char in braille_chars:
  #             left = closed if braille_char[row] else open_
  #             right = closed if braille_char[row+3] else open_
  #             line.append(left + " " + right)
  #         rows.append("  ".join(line))

  #     print("\n".join(rows))