# syntax=docker/dockerfile:1
FROM python:3.10-slim

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir flask requests

EXPOSE 8080
EXPOSE 5000

CMD ["python", "web_app.py"]
