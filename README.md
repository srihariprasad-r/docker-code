Below command will have to be run on top of folder which has 'Dockerfile' in it.

```console
$ docker build --network host .
```

When you execute docker with docker run command, it runs in attached mode, terminal will be running in foreground.
Note: adding '-d' argument before container will change this to detached mode.

```console
$ docker run `<#container-id>`

arguments:
-d -> detached mode (default is attached mode)
-p -> port example localhost:<port> on your browser
-i -> interactive
-t -> Allow psuedo TTY terminal
```

To attach console back to the container when run on detach mode, use below

```console
$ docker attach <#container-id>
```

Rather, docker start will run process in background(detached mode)
Note: adding '-a' argument before container will change this to attached mode.

```console
$ docker start <#container-id>

arguments:
-a -> attached
-i -> Allow STDIN
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

-f -> this argument will convert the logs to keep listening for changes(behaves as attached mode)
```

To list the images available

```console
$ docker images
```

To remove containers use,

```console
$ docker rm <#container-id>
```

To remove images use,

```console
$ docker rmi <#image-id>
```

To remove unused images, use

```console
$ docker images prune
```

To remove mutiple images at a time with TAG=`<none>`, 

```console
$ docker images | grep none | awk '${print $3}' | xargs docker rmi
```

To remove container when exited, use 

```console
$ docker run -p port -d --rm <#container-id>

arguments:
--rm -> This will remove this container when this container is stopped using docker stop
```

To copy files into container

```console
$ docker cp <folder/file to be copied> <#container-id>:/<target-folder>

Note: If target-folder is not present, this would be created
```


