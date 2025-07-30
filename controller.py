from enum import Enum, auto
from OCR.ocr_module import extract_text_from_image
from Braille.braille_module import BrailleConverter

class State(Enum):
    PENDING = auto()
    PROCESSING = auto()
    DISPLAYING = auto()

class Controller:
    def __init__(self):
        self.state = State.PENDING
        self.converter = BrailleConverter()
        self.braille_pages = []
        self.current_page = 0
        print(f"[INIT] State = {self.state.name}")

    def run(self):
        """
        Main loop that polls for input.
        Later we will replace input() with GPIO / hardware input polling.
        """
        while True:
            if self.state == State.PENDING:
                print("[PENDING] Waiting for command...")
                command = input(">> ").strip()

                if command.startswith("process "):
                    image_path = command.split("process ", 1)[1].strip()
                    self.state = State.PROCESSING
                    self.handle_processing(image_path)
                else:
                    print("[WARN] Invalid command. Use: process <image_path>")

            elif self.state == State.PROCESSING:
                print("[PROCESSING] ... busy ... no input allowed.")

            elif self.state == State.DISPLAYING:
                self.display_current_page()
                command = input("Navigate (left/right/down): ").strip().lower()

                if command == "left":
                    self.current_page = max(0, self.current_page - 1)
                elif command == "right":
                    self.current_page = min(len(self.braille_pages) - 1, self.current_page + 1)
                elif command == "down":
                    print("[RESET] Returning to PENDING state.")
                    self.state = State.PENDING
                    self.braille_pages = []
                    self.current_page = 0
                else:
                    print("[WARN] Unknown navigation command.")

    def handle_processing(self, image_path):
        print(f"[PROCESSING] Running OCR on {image_path}...")
        text = extract_text_from_image(image_path)

        if not text:
            print("[ERROR] No text extracted. Returning to PENDING.")
            self.state = State.PENDING
            return

        self.converter(text)  # convert the OCR scanned text to braille
        self.braille_pages = self.converter.paginate(page_size=20)  # display 20 braille cells per page
        self.current_page = 0
        print(f"[PROCESSING DONE] Extracted text and converted to braille. Total pages: {len(self.braille_pages)}")
        self.state = State.DISPLAYING

    def braille_to_str(self, braille_char):
        closed = "●"
        open_ = "○"
        return ''.join([closed if dot else open_ for dot in braille_char])

    def render_grid(self, braille_chars):
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
        return "\n".join(rows)



    def display_current_page(self):
        def braille_cell_to_str(cell):
            return self.converter.decodeBrailleCell(cell)
        
        print(f"\n[DISPLAYING] Page {self.current_page + 1}/{len(self.braille_pages)}")

        # Get current page
        page = self.braille_pages[self.current_page]
        plain_str = ''.join(braille_cell_to_str(b) for b in page).upper()
        print(f"\nBraille grid for page {self.current_page + 1} out of {len(self.braille_pages)}: '{plain_str}'")
        print(self.render_grid(page))







