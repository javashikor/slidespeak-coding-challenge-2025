FROM python:3.11-slim

WORKDIR /app

RUN mkdir -p /app/tmp && chmod 777 /app/tmp

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]