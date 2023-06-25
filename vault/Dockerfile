# base image
FROM vault:latest

# download dependencies
RUN apk --no-cache add \
    bash \
    ca-certificates \
    wget \
    curl \
    vim

# update PATH
ENV PATH="PATH=$PATH:$PWD/vault"
ENV VAULT_ADDR=http://vault-demo:8200
ENV VAULT_TOKEN=root
ENV VAULT_NAMESPACE=dev
ENV VAULT_API_ADDR=http://127.0.0.1:8200
ENV PSQL_ADDR=http://vault_db_1:5432

# add the config file
COPY ./config/vault-config.json /vault/config/vault-config.json
COPY ./database-setup.sh  /vault/src/database-setup.sh
COPY ./start_vault.sh  /vault/src/start_vault.sh
COPY ./transform-fpe-api-setup.sh  /vault/src/transform-fpe-api-setup.sh
COPY ./transform-mask-api-setup.sh  /vault/src/transform-mask-api-setup.sh
COPY ./transit-secret-engine.sh  /vault/src/transit-secret-engine.sh

# expose port 8200
EXPOSE 8200

# run vault
# ENTRYPOINT ["vault"]