### 

Each subdirectory is used to build a single application in its own container.
The code has been tested with Docker, but we can add a Vagrant version if so
desired.

Once Docker is installed (see below), run this command:

```
# sh <subdirectory>/docker-build.sh
```

For example, to build elegant:

```
sh elegant/docker-build.sh
```

This will create an Docker image called radiasoft/<directory>, e.g. radiasoft/elegant.

To run the image, you become root:

```
# sh <subdirectory>/docker-run.sh
```

This will create a new container if one doesn't exist. Otherwise, it will
create a new container.

For example, to run elegant:

```
sh elegant/docker-run.sh
```

When you exit the shell, it will stop the container. You can restart the
container (and pick up where you left off) by re-executing `run.sh`.

### Install Docker

On a CentOS, you install docker this way:

```
sh install-centos-docker.sh
```

This will download the latest docker and start the docker daemon.
