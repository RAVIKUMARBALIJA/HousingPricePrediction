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


# install Java
USER root
RUN echo "deb http://security.debian.org/debian-security stretch/updates main" >> /etc/apt/sources.list                                                   
RUN mkdir -p /usr/share/man/man1 && \
    apt-get update -y && \
    apt-get install -y openjdk-8-jdk

RUN apt-get install unzip -y && \
    apt-get autoremove -y


ENTRYPOINT spark-submit --jars spark-streaming-kafka-0-8-assembly_2.11-2.4.8.jar wsgi.py