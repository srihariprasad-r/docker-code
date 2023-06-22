# base image
FROM alpine:3.14

# set vault version
ENV VAULT_VERSION 1.8.2

# create a new directory
RUN mkdir /vault

# download dependencies
RUN apk --no-cache add \
    bash \
    ca-certificates \
    wget \
    curl \
    vim

# download and set up vault
RUN wget --quiet --output-document=/tmp/vault.zip https://releases.hashicorp.com/vault/${VAULT_VERSION}/vault_${VAULT_VERSION}_linux_amd64.zip && \
    unzip /tmp/vault.zip -d /vault && \
    rm -f /tmp/vault.zip && \
    chmod +x /vault

# update PATH
ENV PATH="PATH=$PATH:$PWD/vault"
ENV VAULT_ADDR=http://vault-demo:8200
ENV VAULT_API_ADDR=http://127.0.0.1:8200
ENV PSQL_ADDR=http://vault_db_1:5432

# add the config file
COPY ./config/vault-config.json /vault/config/vault-config.json

# expose port 8200
EXPOSE 8200

# run vault
ENTRYPOINT ["vault"]