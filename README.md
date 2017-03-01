## dockcli installation and usage

### Requirements
```
docker-engine version 1.12+ is required for HEALTHCHECK
sudo access may be required when invoking the docker API depending on user permissions
```

### Installation
Installation is recommended within virtualenv
```
$ git clone https://github.com/wnormandin/bftest_cli.git
$ cd bftest_cli
$ virtualenv venv && . venv/bin/activate
(venv)$ pip install -e .
```

### Usage
```
Usage: dockcli COMMAND CONTAINER

Options:
  --help  Show this message and exit.

Commands:
  run   attempts to start the docker container...
  stop  attempts to stop the docker container...
  test  basic functional test to ensure containers...
```
### Starting/Stopping a Container
```
$ dockcli run funky_aardvark
[*] Your app is running on http://127.0.0.1:8888
$ docker ps -a
CONTAINER ID        IMAGE               COMMAND                  CREATED              STATUS                        PORTS               NAMES
33e22e6b868c        pokeybill/bftest    "/bin/sh -c 'pytho..."   About a minute ago   Up About a minute (healthy)   8888/tcp            funky_aardvark

$ dockcli stop funky_aardvark
$ docker ps -a
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES

$ dockcli test
[*] Testing docker container creation/removal
[*] Your app is running on http://127.0.0.1:8888
[*] Ensuring we can communicate with the containerized application
        {"result": "hello world"}
[*] Container funky_aardvark stopped
[*] Test succeeded
```
