FROM python:3.9
# ENV VAULT_ADDR=http://vault-demo:8200
# ENV VAULT_API_ADDR=http://127.0.0.1:8200
# ENV PSQL_ADDR=http://vault_db_1:5432
# RUN apt-get update && apt-get install -y vim
# wget sudo curl
# RUN wget -qO - https://raw.githubusercontent.com/yarnpkg/releases/gh-pages/debian/pubkey.gpg | sudo apt-key add -
# RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add 
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
COPY ./config.ini ./flask/config.ini
ENV FLASK_APP=/src/dev/flask/app.py
CMD [ "flask", "run", "--host=0.0.0.0"]


# FROM python:3
# ENV VAULT_ADDR=http://vault-demo:8200
# ENV VAULT_API_ADDR=http://127.0.0.1:8200
# ENV PSQL_ADDR=http://vault-db-1:5432
# # ENV GPG_KEY 0D96DF4D4110E5C43FBFB17F2D347EA6AA65421D
# # RUN apt-key adv --keyserver hkp://pool.sks-keyservers.net:80 --recv-keys AA8E81B4331F7F50 && \
# #     apt-key adv --keyserver hkp://pool.sks-keyservers.net:80 --recv-keys 7638D0442B90D010
# # RUN apt-get update
# # RUN  apt-get install -y vim
# # RUN wget -qO- https://get.docker.com/gpg | sudo apt-key add -
# # RUN sudo install -m 0755 -d /etc/apt/keyrings
# # RUN curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
# # RUN sudo chmod a+r /etc/apt/keyrings/docker.gpg

# # RUN pip install --upgrade pip
# # RUN \
# #     apk add --no-cache postgresql-libs && \
# #     apk add --no-cache --virtual .build-deps gcc postgresql-dev && \
# #     apk add --no-cache musl-dev cargo libffi-dev openssl-dev && \
# #     apk del \
# #     openssl-dev \
# #     musl-dev 
# WORKDIR /src/dev
# COPY ./requirements.txt /src/dev/requirements.txt
# RUN pip install -r /src/dev/requirements.txt
# COPY ./vaultClass.py /src/dev/vaultClass.py
# COPY ./dbc.py /src/dev/dbc.py
# COPY ./fileHandler.py /src/dev/fileHandler.py
# COPY ./files_config.json /src/dev/fileconfig.json
# COPY ./demo.py  /src/dev/demo.py
# COPY ./prepareCustomfiles.py /src/dev/prepareCustomfiles.py
# COPY ./config.ini /src/dev/config.ini
# RUN mkdir -p /src/dev/flask
# # COPY ./flask/__init__.py ./flask/__init__.py
# COPY ./flask/static/ ./flask/static
# COPY ./flask/template/ ./flask/templates
# COPY ./flask/app.py ./flask/app.py
# COPY ./config.ini ./flask/config.ini
# ENV FLASK_APP=/src/dev/flask/app.py
# CMD [ "flask", "run", "--host=0.0.0.0"]