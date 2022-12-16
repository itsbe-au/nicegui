FROM python:3.11-slim

LABEL maintainer="Zauberzeug GmbH <info@zauberzeug.com>"

WORKDIR /app

ADD . .
RUN pip install -e .
RUN pip install itsdangerous

EXPOSE 8080

CMD python3 main.py
