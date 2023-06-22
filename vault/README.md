## Instructions

### Pre-requisite
- Docker desktop
- Python 3.7+
- VS Code (recommended)

Open a terminal to execute vault image, this will be interative image

```sh
cd src/dev/
sh start_vault.sh 
```

Open VSCode(IDE) Terminal, (3 terminals may be needed)

```sh
cd src/dev/
docker build -t vault-app .
```

Then, run below command

```sh
cd src/database/
docker build -t vault-db .
```

and

```sh
cd ../../
docker-compose up -d db

# once above command is complete,  proceed executing below command
# docker-compose up -d app
```

Open another terminal,

```sh
# running python image manually instead of docker-compose as python container exits upon start
docker run --name vault_app_1 --network vault_dev-network -it vault-app /bin/sh
export PSQL_ADDR=http://vault_db_1:5432
```
Open another terminal,

```sh
# running python image manually instead of docker-compose as python container exits upon start
docker exec -it <vault-image-container#> /bin/sh
# create db credetials secrets in vault
sh database-setup.sh 
```

