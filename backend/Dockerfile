# backend/Dockerfile
FROM python:3.9

COPY requirements.txt requirements.txt

# Create and activate virtual enviroment
RUN python3 -m venv venv && \
    . venv/bin/activate && \
    pip install -r requirements.txt

COPY . .

# Ensure uvicorn is in the PATH
ENV PATH="/app/venv/bin:$PATH"

# Start the aplication
CMD ["sh", "-c", ". venv/bin/activate && exec uvicorn main:app --host 0.0.0.0 --port 8000"]