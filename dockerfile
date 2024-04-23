FROM python:3.10.12
COPY . /code
WORKDIR /code
EXPOSE 5000
RUN pip install -r requirements.txt
