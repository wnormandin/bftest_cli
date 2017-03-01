## dockcli installation and usage

### Installation
```
$ git clone https://github.com/wnormandin/bftest_cli.git
$ cd bftest_cli
$ pip install -e .
```

### Usage
```
Usage: dockcli COMMAND CONTAINER

Options:
  --help  Show this message and exit.

Commands:
  run   attempts to start the docker container...
  stop  attempts to stop the docker container...
```
### Starting/Stopping a Container
```
$ dockcli run funky_aardvark
[*] Your app is running on http://127.0.0.1:8888
$ docker ps -a
CONTAINER ID        IMAGE               COMMAND                  CREATED              STATUS                        PORTS               NAMES
33e22e6b868c        pokeybill/bftest    "/bin/sh -c 'pytho..."   About a minute ago   Up About a minute (healthy)   8888/tcp            funky_aardvark

$ python dockcli.py stop funky_aardvark
$ docker ps -a
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
```
