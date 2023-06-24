cname=$(docker inspect --format="{{.Id}}" vault-demo)
docker cp ./config/vault-config.json vault-demo:/vault/config/vault-config.json
docker cp ./database-setup.sh vault-demo:/vault/database-setup.sh
docker cp ./transit-secret-engine.sh vault-demo:/vault/transit-secret-engine.sh
docker cp ./transform-fpe-api-setup.sh vault-demo:/vault/transform-fpe-api-setup.sh
docker cp ./transform-mask-api-setup.sh vault-demo:/vault/transform-mask-api-setup.sh