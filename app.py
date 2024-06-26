from fastapi import FastAPI, File, Query, UploadFile, APIRouter, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from src.convert import ConvertPDF2img
from src.config import HOST, PORT, RESULTS, BASE_URL
import tempfile
import os


convert = ConvertPDF2img()
app = FastAPI()
app.mount("/static", StaticFiles(directory=RESULTS), name="static")
app.add_middleware(
    CORSMiddleware,allow_origins=['*'],allow_credentials=True,allow_methods=['*'],allow_headers=['*'],
)

seting_router = APIRouter(prefix="/setting", tags=['setting'])
@seting_router.put("/dpi")
async def update_dpi(dpi: int = Query(..., description="The new DPI value")):
    if dpi <= 0:
        raise HTTPException(status_code=400, detail="DPI must be a positive integer")
    
    convert.DPI = dpi
    return JSONResponse(content={
        "message": "DPI updated successfully",
        "new_dpi": convert.DPI
    })


convert_router = APIRouter(prefix="/convert", tags=['convert'])
@convert_router.post("/pdf2image")
async def pdf2image(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name
    datas = convert.pdf2img(tmp_path)
    file_urls = [BASE_URL + os.path.basename(data) for data in datas]
    return JSONResponse(content={
        "message": "File converted successfully",
        "file_name": file.filename,
        "file_content_type": file.content_type,
        "file_urls": file_urls,
    })


###########################################################################################################################################
###########################################################################################################################################
# Chunked Upload:

chunked_router = APIRouter(prefix="/v1/api/chunked", tags=['chunked_upload'])

upload_sessions = {}
@chunked_router.post("/start_upload")
async def start_upload(file_name: str):
    upload_id = str(uuid.uuid4())
    temp_file_path = os.path.join(RESULTS, f"{upload_id}.pdf")
    upload_sessions[upload_id] = {
        "file_name": file_name,
        "temp_file_path": temp_file_path,
        "chunks_received": 0
    }
    return {"upload_id": upload_id}

@chunked_router.post("/upload_chunk/{upload_id}")
async def upload_chunk(upload_id: str, chunk: UploadFile = File(...)):
    if upload_id not in upload_sessions:
        raise HTTPException(status_code=404, detail="Upload session not found")
    
    session = upload_sessions[upload_id]
    chunk_data = await chunk.read()
    
    with open(session["temp_file_path"], "ab") as f:
        f.write(chunk_data)
    
    session["chunks_received"] += 1
    
    return {"message": f"Chunk {session['chunks_received']} uploaded successfully"}

@chunked_router.post("/finish_upload/{upload_id}", response_model=ConvertResponse)
async def finish_upload(upload_id: str):
    if upload_id not in upload_sessions:
        raise HTTPException(status_code=404, detail="Upload session not found")
    
    session = upload_sessions[upload_id]
    
    try:
        datas = convert.extract_images(session["temp_file_path"])
        file_urls = [BASE_URL + os.path.basename(data) for data in datas]
        
        # ลบไฟล์ชั่วคราว
        os.remove(session["temp_file_path"])
        
        # ลบข้อมูล session
        del upload_sessions[upload_id]
        
        return {
            "service": CLASS_MODEL,
            "message": "File converted successfully",
            "file_name": session["file_name"],
            "file_content_type": "application/pdf",
            "file_urls": file_urls,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
    

###########################################################################################################################################
###########################################################################################################################################

scheduler_thread = None
stop_flag = threading.Event()

def run_scheduler():
    while not stop_flag.is_set():
        schedule.run_pending()
        time.sleep(1)

@app.on_event("startup")
async def startup_event():
    global scheduler_thread
    schedule.every(1).minutes.do(convert.cleanup_old_files, max_age_minutes=7)
    
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.start()

@app.on_event("shutdown")
async def shutdown_event():
    global scheduler_thread, stop_flag
    if scheduler_thread:
        # ส่งสัญญาณให้ thread หยุดทำงาน
        stop_flag.set()
        
        # รอให้ thread หยุดทำงาน (กำหนด timeout 5 วินาที)
        scheduler_thread.join(timeout=5)
        
        if scheduler_thread.is_alive():
            print("Warning: Scheduler thread did not stop gracefully")
        else:
            print("Scheduler thread stopped successfully")


###########################################################################################################################################
###########################################################################################################################################

app.include_router(seting_router)
app.include_router(convert_router)
app.include_router(chunked_router)

if __name__ in "__main__":
  print("http://localhost:3000/docs")
  import uvicorn
  uvicorn.run(app, host=HOST, port=PORT)