FROM python:3.10.6

COPY requirements.txt app/requirements.txt

WORKDIR /app

RUN apt-get update
RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8000

CMD ["uvicorn", "run", "main:app", ", "--host", "0.0.0.0", "--port", "8000" , "--reload"]