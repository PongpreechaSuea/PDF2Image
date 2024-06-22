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

app.include_router(seting_router)
app.include_router(convert_router)

if __name__ in "__main__":
  print("http://localhost:3000/docs")
  import uvicorn
  uvicorn.run(app, host=HOST, port=PORT)