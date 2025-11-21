FROM python:3.11-slim

WORKDIR /myapp

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
# COPY .env .env

EXPOSE 8000

CMD ["uvicorn", "src.api.routes.prediction:app", "--host", "0.0.0.0", "--port", "8000"]