Below command will have to be run on top of folder which has 'Dockerfile' in it.

```console
$ docker build --network host .
```

When you execute docker with docker run command, it runs in attached mode, terminal will be running in foreground.
Note: adding '-d' argument before container will change this to detached mode.

```console
$ docker run <#container-id>

arguments:
-d detached mode (default is attached mode)
-p port example localhost:<port> on your browser
```

To attach console back to the container when run on detach mode, use below

```console
$ docker attach <#container-id>
```

Rather, docker start will run process in background(detached mode)
Note: adding '-a' argument before container will change this to attached mode.

```console
$ docker start <#container-id>
```

To list only running containers use docker ps, and to know all containers use docker ps -a instead

```console
$ docker ps

$ docker ps -a
```

To stop a running container use below 

```console
$ docker stop <#container-id>
```

Below command captures logs on a container(useful for container running on detached mode)

```console
$ docker logs <#container-id>

arguments:

-f this argument will convert the logs to keep listening for changes(behaves as attached mode)
```
