FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PROJECT_PATH /app

RUN apt-get update && apt-get install -y \
    netcat-traditional \
    pkg-config \
    default-libmysqlclient-dev  \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR ${PROJECT_PATH}

COPY *requirements.txt ${PROJECT_PATH}/

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . ${PROJECT_PATH}

RUN chmod +x ./entrypoint.sh
ENTRYPOINT ./entrypoint.sh