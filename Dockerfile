# syntax=docker/dockerfile:1

FROM python:3.10.9

WORKDIR /shortner

ADD . /shortner

RUN pip install -r requirements.txt

CMD ["flask", "run"]
