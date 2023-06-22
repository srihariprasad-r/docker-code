#!/bin/sh
#stop and remove vault containers if already running
docker stop vault-demo
docker rm vault-demo
#start Vault in dev mode on port 8200
docker run --name vault-demo --network vault_dev-network -p 8220:8220 hashicorp/vault-enterprise:1.4.0_ent server -dev -dev-root-token-id="root" &