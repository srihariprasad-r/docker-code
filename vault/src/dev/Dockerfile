FROM python:3.7
WORKDIR /src/dev
COPY ./requirements.txt /src/dev/requirements.txt
RUN pip install -r /src/dev/requirements.txt
COPY ./hvac-demo.py /src/dev/app.py