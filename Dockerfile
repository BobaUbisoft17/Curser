FROM python:3.12.4-alpine

WORKDIR /app

COPY requirements.txt ./

RUN python -m pip install -U pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
WORKDIR /app
ENTRYPOINT sh entrypoint.sh
