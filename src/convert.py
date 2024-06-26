import os
import uuid
import logging
from datetime import datetime, timedelta
from pdf2image import convert_from_path
from src.config import POPPLER, RESULTS, DPI

class ConvertPDF2img:
    def __init__(self):
        self.DPI = DPI
        self.results = RESULTS
        self.POPPLER = POPPLER

        log_file = 'ConvertPDF2Image.log'
        logging.basicConfig(filename=log_file, level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            encoding='utf-8')
        logging.info(f"Initialized ConvertPDF2Image. Results directory: {self.results}")

        
    def pdf2img(self, path: str = None):
        logging.info(f"===========================================================================")
        logging.info(f"Starting image extraction from PDF: {path}")
        if not os.path.exists(self.results):
            os.makedirs(os.path.abspath(self.results), exist_ok=True)
            logging.info(f"Created directory: {self.results}")
        datas = convert_from_path(path, self.DPI, poppler_path=self.POPPLER)

        pages = []
        for i, image in enumerate(datas):
            fname = f'{self.results}/image_{uuid.uuid4()}.png'
            logging.info(f"Create file pdf : {fname}")
            image.save(fname, "PNG")
            pages.append(fname)

        logging.info(f"Total pages in PDF: {len(pages)}")
        return pages

    def cleanup_old_files(self, max_age_minutes=7):
        logging.info(f"<<<<<>>>>>")
        logging.info(f"Starting cleanup of old files. Max age: {max_age_minutes} minutes")
        current_time = datetime.now()
        removed_count = 0
        total_files = 0

        for filename in os.listdir(self.RESULTS_DIR):
            total_files += 1
            file_path = os.path.join(self.RESULTS_DIR, filename)
            if os.path.isfile(file_path):
                file_modified_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                file_age = current_time - file_modified_time
                if file_age > timedelta(minutes=max_age_minutes):
                    try:
                        os.remove(file_path)
                        removed_count += 1
                        logging.info(f"Removed old file: {filename} (Age: {file_age})")
                    except Exception as e:
                        logging.error(f"Error removing file {filename}: {str(e)}")
                else:
                    logging.debug(f"Kept file: {filename} (Age: {file_age})")

        logging.info(f"Cleanup completed. Removed {removed_count} out of {total_files} files.")
