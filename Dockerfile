FROM python:3.8
ENV PYTHONUNBUFFERED=1
RUN mkdir /orders-api-test
WORKDIR /orders-api-test
COPY requirements.txt /orders-api-test/
RUN pip install -r requirements.txt
COPY . /orders-api-test/