## Instructions

### Pre-requisite
- Docker desktop
- Python 3.7+
- VS Code (recommended)

## Pull and run a vault image through docker compose and add to network

Open a terminal to execute vault image, this will be interative image

```sh
cd src/dev/
sh start_vault.sh 

# Once you see dev server is running, open a terminal to copy files into above container
sh copy_vault.sh

```
## Build python image through docker compose and add to network

Open VSCode(IDE) Terminal, (3 terminals may be needed)

```sh
cd src/dev/
docker build -t vault-app .
```

## Pull postgres image through docker compose and add to network

```sh
cd ../../
docker-compose up -d db
# once above command is complete,  proceed executing below command
# docker-compose up -d app
```

## Vault container 

Open another terminal,

```sh
# running python image manually instead of docker-compose as python container exits upon start
docker ps # check container-id for running containers
docker exec -it <vault-image-container#> /bin/sh
# to execute vault API's, we need below env variables
$ export VAULT_ADDR=http://localhost:8200
$ export VAULT_TOKEN=root
$ export VAULT_NAMESPACE=dev
# check status of vault
$ vault status
# you should see something as below

# Key             Value
# ---             -----
# Seal Type       shamir
# Initialized     true
# Sealed          false
# Total Shares    1
# Threshold       1
# Version         1.13.3
# Build Date      2023-06-06T18:12:37Z
# Storage Type    inmem
# Cluster Name    vault-cluster-14e8f07e
# confirm if files are copied inside vault/ folder
$ cd vault 
# there should be four shell scripts
# create db credetials secrets in vault
sh database-setup.sh 

# Success! Disabled the secrets engine (if it existed) at: data_protection/database/
# Success! Enabled the database secrets engine at: data_protection/database/
# Success! Data written to: data_protection/database/config/postgres
# Success! Data written to: data_protection/database/roles/vault-demo-app
# Key                Value
# ---                -----
# lease_id           data_protection/database/creds/vault-demo-app/Tum01p4dXPrSQa4nyrt5fnwk
# lease_duration     1h
# lease_renewable    true
# password           bbb9s3Gs-nv6iF4xyVQw
# username           v-token-vault-de-XBDQKwV5ysFhznjUGrWU-1687686820
$ sh transit-secret-engine.sh

# Enabling the vault transit secrets engine...
# Success! Disabled the secrets engine (if it existed) at: data_protection/transit/
# Success! Enabled the transit secrets engine at: data_protection/transit/
# Success! Data written to: data_protection/transit/keys/customer-key
# Key            Value
# ---            -----
# ciphertext     vault:v1:GJm+i6VdMCtHKSSu6bBkH2pVfDc2k0Xvtd+kVw==
# key_version    1

# confirm is secrets are added to vault
$ vault secrets list

# Path                         Type         Accessor              Description
# ----                         ----         --------              -----------
# cubbyhole/                   cubbyhole    ...                    per-token private secret storage
# data_protection/database/    database     ...                    n/a
# data_protection/transit/     transit      ...                    n/a
# identity/                    identity     identity_303a43a4     identity store
# secret/                      kv           kv_047e9e66           key/value secret storage
# sys/                         system       system_eb63d317       system endpoints used for control, policy and debugging

```
## Postgres container 

Open VSCode terminal

```sh
$ cd ../vault
$ docker ps
$ docker exec -it <container-id> psql -U postgres

# psql (14.1 (Debian 14.1-1.pgdg110+1))
# Type "help" for help.

# postgres=# \d
```

## Python container

Open VSCode terminal

```sh
$ cd ../vault
$ docker run --name vault_app_1 --network vault_dev-network -it vault-app /bin/sh
$ ls
# you should see python files

```

## Python container 
```sh
# assuming you are in python container
$ ls
$ python dbc.py
# check if status is complete
#
```

## Postgres container 
```sh
# assuming you are in postgres container
$ ls
postgres=# \d
# check if status is complete
postgres=# \l
# you should see below rows
postgres=# select * from customers;
#  cust_no |                          birth_date                           | first_name | last_name |        create_date         |                    social_security_number                     |                            credit_card_number                             |                              address
#                |                          salary
# ---------+---------------------------------------------------------------+------------+-----------+----------------------------+---------------------------------------------------------------+---------------------------------------------------------------------------+-------------------------------------------------------------------+-----------------------------------------------------------
#        1 | 2023-03-10                                                    | Larry      | Johnson   | 2020-01-01T14:49:12.301977 | 360-56-6750
#                                | 3600-5600-6750-0000                                                       | Tyler, Texas
#                | 7000000
#        2 | vault:v1:j0Mwm21QmSNckrQy2q9PnGwmAuftOGtG7aOsu2PMQrO//exaCgI= | Larry      | Johnson   | 2020-01-01T14:49:12.301977 | vault:v1:0XFPrrAyNM+C1dxkYLd+NjRFQ0bEQzIpawupNSSXa1vecEHgz3ON | vault:v1:yDBDDbuS2HLkvRPifQ0p9jK77aB/Xlyi4lrZAQQtyS6MR6GWI4P3ylHCvLpIiZs= | vault:v1:IUKZjL4WAqjWhuq9d15IzvM7/SGztYX5fMsxVXmKe5iTHtC2x8GWFg== | vault:v1:cMCwJ1d6EoW537y6hdWDRQmpPbz20XlfUkQS3bRgJ/89RIw=
#
```

# docker stats

```sh
CONTAINER ID        NAME                CPU %               MEM USAGE / LIMIT     MEM %               NET I/O             BLOCK I/O           PIDS
35712dcddeeb        vault_app_1         0.00%               2.508MiB / 3.856GiB   0.06%               2.1kB / 154B        29MB / 0B           1   
b6be9fa77770        vault-demo          1.57%               30.09MiB / 3.856GiB   0.76%               3.08kB / 1.74kB     247MB / 246MB       9   
27518d035749        vault_db_1          0.00%               10.98MiB / 3.856GiB   0.28%               3.27kB / 1.94kB     7.93MB / 229kB      10
```


