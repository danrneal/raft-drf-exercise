FROM python:buster

COPY ./ /app
WORKDIR /app

RUN pip install -U pip
RUN pip install -r requirements.txt

ENTRYPOINT [ "gunicorn", "upload.wsgi:application" ]