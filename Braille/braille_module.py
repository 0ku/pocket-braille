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
    
    BRAILLE_REVERSE_MAP = {
        (1, 0, 0, 0, 0, 0): 'a',
        (1, 1, 0, 0, 0, 0): 'b',
        (1, 0, 0, 1, 0, 0): 'c',
        (1, 0, 0, 1, 1, 0): 'd',
        (1, 0, 0, 0, 1, 0): 'e',
        (1, 1, 0, 1, 0, 0): 'f',
        (1, 1, 0, 1, 1, 0): 'g',
        (1, 1, 0, 0, 1, 0): 'h',
        (0, 1, 0, 1, 0, 0): 'i',
        (0, 1, 0, 1, 1, 0): 'j',
        (1, 0, 1, 0, 0, 0): 'k',
        (1, 1, 1, 0, 0, 0): 'l',
        (1, 0, 1, 1, 0, 0): 'm',
        (1, 0, 1, 1, 1, 0): 'n',
        (1, 0, 1, 0, 1, 0): 'o',
        (1, 1, 1, 1, 0, 0): 'p',
        (1, 1, 1, 1, 1, 0): 'q',
        (1, 1, 1, 0, 1, 0): 'r',
        (0, 1, 1, 1, 0, 0): 's',
        (0, 1, 1, 1, 1, 0): 't',
        (1, 0, 1, 0, 0, 1): 'u',
        (1, 1, 1, 0, 0, 1): 'v',
        (0, 1, 0, 1, 1, 1): 'w',
        (1, 0, 1, 1, 0, 1): 'x',
        (1, 0, 1, 1, 1, 1): 'y',
        (1, 0, 1, 0, 1, 1): 'z',
        (0, 0, 0, 0, 0, 0): '_', # Map space to _ for debugging clarity
        (0, 1, 0, 0, 1, 1): '.',
        (0, 1, 0, 0, 0, 0): ',',
        (0, 1, 1, 0, 1, 0): '!',
    }

    def __init__(self, text: str):
        text = text.replace('\n', ' ')
        text = text.replace('\r', ' ')
        text = text.replace('\t', ' ')
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

    def decodeBrailleCell(self, brailleCell):
        # Convert braille cell to character
        return self.BRAILLE_REVERSE_MAP.get(tuple(brailleCell), '?')  # Use '?' for unknown patterns

    def paginate(self, page_size: int):
      return self.paginateSplit(page_size)

    def paginateNoSplit(self, page_size: int):
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

            space_len = len(current_page) - 1 if current_page else 0
            if current_len + word_len + space_len > page_size and current_page:
                pages.append(current_page)
                current_page = []
                current_len = 0

            current_page.extend(word_braille)
            current_len += word_len

        if current_page:
            pages.append(current_page)
        return pages

    def paginateSplit(self, page_size: int):
      # Paginate with character-level splitting and spaces between words only
      pages = []
      current_page = []
      current_len = 0

      for i, word in enumerate(self.words):
          space_braille = self.BRAILLE_MAP.get(' ', (0,0,0,0,0,0))
          for c in word:
              char_braille = self.BRAILLE_MAP.get(c, (0,0,0,0,0,0))
              if current_len + 1 > page_size:
                  pages.append(current_page)
                  current_page = []
                  current_len = 0
              current_page.append(char_braille)
              current_len += 1

          # Add space after word, unless it's the last word
          if i != len(self.words) - 1:
              if current_len + 1 > page_size:
                  pages.append(current_page)
                  current_page = []
                  current_len = 0
              current_page.append(space_braille)
              current_len += 1

      if current_page:
        while current_len + 1 <= page_size:
          current_page.append(space_braille)
          current_len +=1
        pages.append(current_page)
      return pages

    def get_braille(self):
        return self.braille

    def get_text(self):
        return self.text