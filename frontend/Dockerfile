FROM python:3.11-slim 

WORKDIR /code 

COPY requirements.txt /code/

RUN pip install --no-cache-dir -r requirements.txt 

COPY . .

EXPOSE 8004

CMD ["streamlit", "run", "main.py", "--server.port", "8004", "--server.address", "0.0.0.0"]
