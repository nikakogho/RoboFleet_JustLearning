FROM python:3.11-slim

WORKDIR /code

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY ./server /code/server

EXPOSE 8000

WORKDIR /code/server

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]