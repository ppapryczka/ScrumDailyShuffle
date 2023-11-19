FROM ubuntu:20.04

WORKDIR /scrum_daily_shuffle

COPY requirements.txt .

RUN apt-get update && apt-get install -y python3-pip
RUN pip install -r requirements.txt --no-cache-dir

RUN mkdir scrum_daily_shuffle

COPY src/scrum_daily_shuffle scrum_daily_shuffle

EXPOSE 15015

CMD ["python3",  "scrum_daily_shuffle/main.py"]