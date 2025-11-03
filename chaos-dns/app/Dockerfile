FROM python:3.10-slim-bullseye
WORKDIR /app

RUN apt-get update -o Acquire::Retries=5 -o Acquire::http::No-Cache=True && \
    apt-get install -y --no-install-recommends \
        curl git netcat-traditional dnsutils iputils-ping && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
ENV PYTHONUNBUFFERED=1
COPY wait-for-localstack.sh /wait-for-localstack.sh
RUN chmod +x /wait-for-localstack.sh
CMD ["/wait-for-localstack.sh"]


