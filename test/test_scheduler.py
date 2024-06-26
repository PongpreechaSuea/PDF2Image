import schedule
import time
import threading
from src.convert import ConvertPDF2Image

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

# ใน main application หรือ FastAPI startup event
convert = ConvertPDF2Image()
schedule.every(1).minutes.do(convert.cleanup_old_files, max_age_minutes=5)

# เริ่ม scheduler ในthread แยก
scheduler_thread = threading.Thread(target=run_scheduler)
scheduler_thread.start()