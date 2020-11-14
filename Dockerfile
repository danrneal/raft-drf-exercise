FROM python:buster

COPY ./ /app
WORKDIR /app

RUN pip install -U pip
RUN pip install -r requirements.txt

ENTRYPOINT [ "gunicorn", "-b", ":8000", "upload.wsgi:application" ]