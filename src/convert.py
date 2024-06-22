import os
import uuid
from pdf2image import convert_from_path
from src.config import POPPLER, RESULTS, DPI

class ConvertPDF2img:
    def __init__(self):
        self.DPI = DPI
        self.results = RESULTS
        self.POPPLER = POPPLER
        
    def pdf2img(self, path: str = None):
        if not os.path.exists(self.results):
            os.makedirs(os.path.abspath(self.results), exist_ok=True)
        datas = convert_from_path(path, self.DPI, poppler_path=self.POPPLER)

        pages = []
        for i, image in enumerate(datas):
            fname = f'{self.results}/image_{uuid.uuid4()}.png'
            image.save(fname, "PNG")
            pages.append(fname)
        return pages
