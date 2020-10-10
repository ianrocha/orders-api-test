FROM python:3.8
ENV PYTHONUNBUFFERED=1
RUN mkdir /order-api
WORKDIR /order-api
COPY requirements.txt /order-api/
RUN pip install -r requirements.txt
COPY . /order-api/