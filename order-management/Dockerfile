FROM python:3.11-slim

WORKDIR /code

COPY requirements.txt /code/

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8002

ENV MONGO_URI=mongodb://mongodb-service:27017/YaEC

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002","--reload"]

