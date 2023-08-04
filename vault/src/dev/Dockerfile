FROM python:3.7
ENV VAULT_ADDR=http://vault-demo:8200
ENV VAULT_API_ADDR=http://127.0.0.1:8200
ENV PSQL_ADDR=http://vault_db_1:5432
RUN apt-get update && apt-get install -y vim
WORKDIR /src/dev
COPY ./requirements.txt /src/dev/requirements.txt
RUN pip install -r /src/dev/requirements.txt
COPY ./vaultClass.py /src/dev/vaultClass.py
COPY ./dbc.py /src/dev/dbc.py
COPY ./fileHandler.py /src/dev/fileHandler.py
COPY ./files_config.json /src/dev/fileconfig.json
COPY ./demo.py  /src/dev/demo.py
COPY ./prepareCustomfiles.py /src/dev/prepareCustomfiles.py
COPY ./config.ini /src/dev/config.ini
RUN mkdir -p /src/dev/flask
# COPY ./flask/__init__.py ./flask/__init__.py
COPY ./flask/static/ ./flask/static
COPY ./flask/template/ ./flask/templates
COPY ./flask/app.py ./flask/app.py
ENV FLASK_APP=/src/dev/flask/app.py
CMD [ "flask", "run", "--host=0.0.0.0"]