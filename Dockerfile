FROM python:3.7.7

ADD requirements.txt .

RUN pip install -r requirements.txt
