FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y poppler-utils
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

EXPOSE 3000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "3000"]


# Build Docker image
# docker build -t pdf2image .

# Run Docker container
# docker run -p 3511:3511 -v $(pwd)/src:/app/src -v $(pwd)/temp:/app/temp -e CLASS_MODEL=PDF2IMAGE -e RESULTS=/app/temp/pdf -e HOST=0.0.0.0 -e PORT=3511 -e BASE_URL=http://localhost:3511/static/ pdf2image