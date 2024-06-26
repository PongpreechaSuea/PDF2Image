import requests
import os

def chunked_upload(file_path, chunk_size=1024*1024):  # 1MB chunks
    file_name = os.path.basename(file_path)
    
    # Start upload
    response = requests.post("http://localhost:3511/v1/api/chunked/start_upload", params={"file_name": file_name})
    upload_id = response.json()["upload_id"]
    
    # Upload chunks
    with open(file_path, "rb") as f:
        chunk = f.read(chunk_size)
        chunk_number = 1
        while chunk:
            files = {"chunk": (f"chunk{chunk_number}", chunk)}
            response = requests.post(f"http://localhost:3511/v1/api/chunked/upload_chunk/{upload_id}", files=files)
            print(response.json()["message"])
            chunk = f.read(chunk_size)
            chunk_number += 1
    
    # Finish upload and convert
    response = requests.post(f"http://localhost:3511/v1/api/chunked/finish_upload/{upload_id}")
    return response.json()

result = chunked_upload("./data/Business Function v1.0.0.pdf")
print(result)