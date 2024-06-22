# PDF to Image Converter API

This project provides a FastAPI-based web service to convert PDF files to images using the `pdf2image` library and `poppler` for PDF rendering.

## Features

- Convert PDF files to PNG images.
- Update DPI setting dynamically via API.
- Generate unique filenames using UUID.

## Requirements

- Python 3.9.16
- FastAPI
- pdf2image
- Poppler

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/PongpreechaSuea/PDF2Image.git
    cd PDF2Image
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages (`requirements.txt`):
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

Update the `src/config.py` file with your desired settings:

```python
POPPLER = ...
RESULTS = ...
DPI = ...
HOST = "localhost"
PORT = ...
BASE_URL = f"http://{HOST}:{PORT}/static/"
```

## Usage
### Running the Server
Start the FastAPI server:

```cmd
python ./app.py # http://localhost:3000/docs
or
uvicorn src.main:app --host localhost --port 3000
```

## API Endpoints

### Convert PDF to Images

- Endpoint: /convert/pdf2image
- Method: POST
- Description: Converts a PDF file to PNG images.
- Request: multipart/form-data
  - file: The PDF file to convert.
- Response: 
    ```json
    {
        "message": "File converted successfully",
        "file_name": "example.pdf",
        "file_content_type": "application/pdf",
        "file_urls": [
            "http://localhost:3000/static/image_<uuid1>.png",
            "http://localhost:3000/static/image_<uuid2>.png"
        ]
    }
    ```

### Update DPI Setting
- Endpoint: /setting/dpi
- Method: PUT
- Description: Updates the DPI setting used for PDF to image conversion.
- Request: URL query parameter
  - dpi: The new DPI value.
- Response:
  ```json
  {
      "message": "DPI updated successfully",
      "new_dpi": 300
  }
  ```
