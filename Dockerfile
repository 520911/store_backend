FROM python:3.8-buster

WORKDIR /usr/src/shop

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD python manage.py migrate