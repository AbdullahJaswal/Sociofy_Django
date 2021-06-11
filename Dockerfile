FROM python:latest
ENV PYTHONUNBUFFERED=1
WORKDIR /usr/src/sociofy/backend/
COPY requirements.txt ./
RUN apt-get update
RUN pip install -r requirements.txt