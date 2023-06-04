FROM ubuntu:20.04

WORKDIR /daily-shuffle

COPY src .
COPY requirements.txt .

RUN apt-get update && apt-get install -y python3-pip
RUN pip install -r requirements.txt --no-cache-dir

EXPOSE 15015

CMD ["python3",  "main.py"]
