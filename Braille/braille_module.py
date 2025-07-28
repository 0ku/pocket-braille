class BrailleConverter:
    # Basic Braille encoding for lowercase English letters (a-z) and some punctuation
    BRAILLE_MAP = {
        'a': (1,0,0,0,0,0),
        'b': (1,1,0,0,0,0),
        'c': (1,0,0,1,0,0),
        'd': (1,0,0,1,1,0),
        'e': (1,0,0,0,1,0),
        'f': (1,1,0,1,0,0),
        'g': (1,1,0,1,1,0),
        'h': (1,1,0,0,1,0),
        'i': (0,1,0,1,0,0),
        'j': (0,1,0,1,1,0),
        'k': (1,0,1,0,0,0),
        'l': (1,1,1,0,0,0),
        'm': (1,0,1,1,0,0),
        'n': (1,0,1,1,1,0),
        'o': (1,0,1,0,1,0),
        'p': (1,1,1,1,0,0),
        'q': (1,1,1,1,1,0),
        'r': (1,1,1,0,1,0),
        's': (0,1,1,1,0,0),
        't': (0,1,1,1,1,0),
        'u': (1,0,1,0,0,1),
        'v': (1,1,1,0,0,1),
        'w': (0,1,0,1,1,1),
        'x': (1,0,1,1,0,1),
        'y': (1,0,1,1,1,1),
        'z': (1,0,1,0,1,1),
        ' ': (0,0,0,0,0,0),
        '.': (0,1,0,0,1,1),  # period
        ',': (0,1,0,0,0,0),  # comma
        '!': (0,1,1,0,1,0),  # exclamation
    }

    def __init__(self, text: str):
        self.text = text.lower()
        self.words = self.text.split(' ')
        self.braille = self._convert_to_braille(self.text)

    def _convert_to_braille(self, text: str):
        # Convert each character to its braille representation
        braille_list = []
        for char in text:
            braille_char = self.BRAILLE_MAP.get(char, (0,0,0,0,0,0))  # Unknown chars as blank
            braille_list.append(braille_char)
        return braille_list

    def paginate(self, page_size: int):
        # Paginate without splitting words
        pages = []
        current_page = []
        current_len = 0

        for word in self.words:
            word_braille = [self.BRAILLE_MAP.get(c, (0,0,0,0,0,0)) for c in word]
            # Add space after word except last word
            if word != self.words[-1]:
                word_braille.append(self.BRAILLE_MAP[' '])
            word_len = len(word_braille)

            if current_len + word_len > page_size and current_page:
                pages.append(current_page)
                current_page = []
                current_len = 0

            current_page.extend(word_braille)
            current_len += word_len

        if current_page:
            pages.append(current_page)
        return pages

    def get_braille(self):
        return self.braille

    def get_text(self):
        return self.text