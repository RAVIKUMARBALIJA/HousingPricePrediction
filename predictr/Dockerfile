FROM python:3.6-slim

WORKDIR /app

ENV PYTHONUNBUFFERED 1
ENV DISPLAY=:99

# Install apt dependencies
RUN apt update

# Install requirements
COPY requirement.txt requirement.txt
RUN pip install -r requirement.txt

COPY . /app

ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
RUN export JAVA_HOME


#ENTRYPOINT python fake_stream.py
ENTRYPOINT spark-submit --jars spark-streaming-kafka-0-8-assembly_2.11-2.4.8.jar transformer.py