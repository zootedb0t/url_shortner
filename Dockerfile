# syntax=docker/dockerfile:1

FROM python:3.10.9

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

# --host 0.0.0.0 is important for accessing container outside
CMD ["flask", "run", "--host", "0.0.0.0"]
