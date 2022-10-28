FROM python:3.10.6

COPY requirements.txt car_price/requirements.txt

WORKDIR /car_price

RUN apt-get update
RUN pip install -r requirements.txt

COPY . /car_price

EXPOSE 8501

CMD ["streamlit", "run", "car_price.py", "--logger.level=debug"]