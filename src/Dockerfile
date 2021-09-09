FROM python:latest

RUN mkdir usr/main
WORKDIR usr/main

COPY . .

RUN pip install -r requirements.txt

CMD python main.py