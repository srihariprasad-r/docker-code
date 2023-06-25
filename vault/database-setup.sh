#!/bin/sh

# Note: This script requires that the VAULT_ADDR, VAULT_TOKEN, and MYSQL_ENDPOINT environment variables be set.
# Example:
export VAULT_ADDR=http://localhost:8200
export VAULT_TOKEN=root
export PSQL_ENDPOINT=vault_db_1:5432
export VAULT_NAMESPACE=


#create namespace dev
vault namespace delete dev/
vault namespace create dev
# Enable the database secrets engine
export VAULT_NAMESPACE=dev
vault secrets disable data_protection/database
vault secrets enable -path=data_protection/database database

# Configure the database secrets engine to talk to MySQL
vault write data_protection/database/config/postgres \
    plugin_name=postgresql-database-plugin \
    connection_url=postgresql://"{{username}}:{{password}}@${PSQL_ENDPOINT}?sslmode=disable" \
    allowed_roles="vault-demo-app" \
    username="postgres" \
    password="postgres"

vault write data_protection/database/roles/vault-demo-app \
    db_name="postgres" \
    creation_statements="CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}'; \
        GRANT ALL ON ALL TABLES IN SCHEMA public TO \"{{name}}\" ;\
        GRANT SELECT, UPDATE, USAGE ON ALL SEQUENCES IN SCHEMA public TO \"{{name}}\"; "\
    default_ttl="1h" \
    max_ttl="24h"

vault read data_protection/database/creds/vault-demo-app