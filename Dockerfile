FROM python:buster

COPY ./ /app
WORKDIR /app

RUN pip install -U pip
RUN pip install -r requirements.txt

CMD gunicorn -b :${PORT-8000} upload.wsgi:application 
