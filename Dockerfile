FROM python:3.10.7

Run pip install --upgrade pip

EXPOSE 5000

WORKDIR /docker-app

ADD . /docker-app

RUN pip --no-cache-dir install -r requirements.txt

CMD python app.py

