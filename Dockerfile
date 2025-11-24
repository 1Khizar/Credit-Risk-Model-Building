FROM python:3.11-slim

WORKDIR /myapp

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project (including models from GitHub Actions artifacts)
COPY . .

# Accept secrets as build arguments
ARG DATABASE_URL
ARG ANOTHER_SECRET

# Set secrets as environment variables inside container
ENV DATABASE_URL=$DATABASE_URL
ENV ANOTHER_SECRET=$ANOTHER_SECRET

EXPOSE 8000

# Run FastAPI app
CMD ["uvicorn", "src.api.routes.prediction:app", "--host", "0.0.0.0", "--port", "8000"]
