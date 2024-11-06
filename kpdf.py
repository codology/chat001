import pdfplumber


class PDFReader:

    TEXT = "_text"
    WORDS = "_words"
    TABLES = "_tables"
    IMAGES = "_images"
    DICT = "_dict"

    def __init__(self, file_obj):
        self._file = file_obj
        self._text = []
        self._words = []
        self._tables = []
        self._images = []
        self._dict = {}

    def extract_all_data(self):
        with pdfplumber.open(self._file) as pdf:
            for p in pdf.pages:
                self._text.append(p.extract_text())
                # self._words.append(p.extract_words())
                # self._tables.append(p.extract_tables())
                # self._dict.update(p.to_dict())

    def get_data(self, data_type: str):
        return getattr(self, data_type)
