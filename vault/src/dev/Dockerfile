FROM python:3.7
ENV VAULT_ADDR=http://vault-demo:8200
ENV VAULT_API_ADDR=http://127.0.0.1:8200
ENV PSQL_ADDR=http://vault_db_1:5432
RUN apt-get update && apt-get install -y vim
WORKDIR /src/dev
COPY ./requirements.txt /src/dev/requirements.txt
RUN pip install -r /src/dev/requirements.txt
COPY ./hvac.py /src/dev/hvac.py
COPY ./dbc.py /src/dev/dbc.py
COPY ./hvac-demo.py /src/dev/hvac-demo.py
COPY ./config.ini /src/dev/config.ini