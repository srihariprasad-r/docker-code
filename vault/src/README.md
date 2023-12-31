
### Manual steps ###

## Install docker ##

## If any certs issue, run below. Else proceed to next step ##
```console
$ docker-machine regenerate-certs --client-certs
```

## Step into DockerFile path and run below ##
```console
$ docker build -t vault-poc .
$ docker-compose up -d vault-filesystem

$ docker ps

$ docker exec -it vault_vault-filesystem_1 /bin/sh
/ # vault status
/ # vault operator init

<!--- note down root token (very important!) with five unseal keys - it won't be available -->

<!--- try with three different unseal keys -->

/ # vault operator unseal
/ # vault operator unseal
/ # vault operator unseal

/ # vault login

/ # exit

<!--- get ip to access web UI of vault -->

$ docker inspect -f \
> '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' <name of container>
```

## login back to container for Transit  ##
```console
docker exec -it vault_vault-filesystem_1 /bin/sh
/ # vault secrets enable transit
/ # vault write transit/keys/demo-key type=aes256-gcm96
/ # vault write transit/encrypt/demo-key plaintext=$(base64 << "my secret key")
```

## execute python container  ##
```console
$ docker-compose up -d app
$ docker run -it --entrypoint=/bin/bash vault_app
```

# packages to update files in docker
```console
$ apt-get update
$ apt-get install apt-file
$ apt-file update
$ apt-get install vim  
```