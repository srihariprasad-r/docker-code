## Instructions

### Pre-requisite
- Docker desktop
- Python 3.7+
- VS Code (recommended)

## Pull and run a vault/python/postgres images through docker compose and add to network

Open a terminal to execute docker commands

```sh
cd vault/
sh bootup-script.sh 

```

## Vault container 

Open another terminal,

```sh
# running python image manually instead of docker-compose as python container exits upon start
$ docker ps # check container-id for running containers
$ docker exec vault-demo /bin/sh -c './vault/database-setup.sh'
$ docker exec vault-demo /bin/sh -c './vault/transit-secret-engine.sh'
$ docker exec -it vault-demo /bin/sh
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

## Python container(CLI/API)

Open VSCode terminal

```sh
$ cd ../vault
$ docker run --name vault_app_1 --network vault_dev-network --port 5000:5000 -it vault-app /bin/sh
# NOTE: bootup-script will already be running container, if you need to get into that container, use below:
# $ docker exec -it <container id> /bin/sh
# you should see python files
$ ls
# Table encryption
$ python demo.py --type table
# go back to postgres container
# check if status is complete and do below, there will be one seed record
# postgres=# select * from customers;
# in python container, run below to proceed encryption
$ python demo.py --type table --apply encrypt
# next is decryption, this will display rows which were encrypted in above step with actual PII values
$ python demo.py --type table --apply decrypt

# File encryption - supports CSV, Avro, JSON, Parquet

# CSV file encrytion
# --csvdelimiter is optional, if not provided, ',' will be delimiter
$ python demo.py --type file --filetype csv --filepath /src/files # [--csvdelimiter ',']
$ cd /src/files
# you should see csv file
$ cd ../dev
$ python demo.py --type file --filetype csv --filepath /src/files --apply encrypt
# you should see encrypted_xxx.csv file in /src/files

# JSON file encrytion
$ python demo.py --type file --filetype json --filepath /src/files
$ cd /src/files
# you should see json file
$ cd ../dev
$ python demo.py --type file --filetype json --filepath /src/files --apply encrypt
# you should see encrypted_xxx.json file in /src/files

# Avro file encrytion
$ python demo.py --type file --filetype avro --filepath /src/files
$ cd /src/files
# you should see avro file
$ cd ../dev
$ python demo.py --type file --filetype avro --filepath /src/files --apply encrypt
# you should see encrypted_xxx.avro file in /src/files

# Parquet file encrytion
$ python demo.py --type file --filetype parquet --filepath /src/files
$ cd /src/files
# you should see parquet file
$ cd ../dev
$ python demo.py --type file --filetype parquet --filepath /src/files --apply encrypt
# you should see encrypted_xxx.parquet file in /src/files

# if you still need to access API commands using flask
$ cd flask
$ flask run --host='0.0.0.0' --port=5000
# This will spin up flask API server in backend. To get localhost IP to access UI,
# go to Docker Toolbox and run : docker-machine ip
# Go to chrome: http://<docker-ip>:5000, UI screen to appear
```

## Python container for API commands
```sh
# assuming you are in python container
$ docker run -d -p 5000:5000 --name vault_app_1 --network vault_dev-network  vault-app
# NOTE: bootup-script will already be running container, if you need to get into that container, use below:
# $ docker exec -it <container id> /bin/sh
# This will spin up flask API server in backend. To get localhost IP to access UI,
# go to Docker Toolbox and run : docker-machine ip
# Go to chrome: http://<docker-ip>:5000, UI screen to appear
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
ce414f2bb83b        vault_app_1         0.01%               55.27MiB / 3.856GiB   1.40%               34.4kB / 41.2kB     0B / 0B             1 
cc417aee3e86        vault_db_1          0.00%               13.28MiB / 3.856GiB   0.34%               20.6kB / 16.6kB     16.1MB / 35.7MB     10
7cb8c1824a25        vault-demo          0.39%               32.68MiB / 3.856GiB   0.83%               257kB / 322kB       248MB / 246MB       9
```

# docker system df

```sh
TYPE                TOTAL               ACTIVE              SIZE                RECLAIMABLE  
Images              12                  3                   3.128GB             2.253GB (72%)
Containers          3                   3                   289.5MB             0B (0%)      
Local Volumes       288                 2                   43.4MB              43.4MB (100%)
Build Cache         0                   0                   0B                  0B
```


