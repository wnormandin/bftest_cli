# Basic command-line interface to manage docker containers which will use an
# image stored in a dockerhub registry - 'pokeybill/bftest'

import click
import docker
import sys
import json
import time

this = sys.modules[__name__]
BASE_URL = 'unix://var/run/docker.sock'
REGISTRY = 'pokeybill/bftest'

@click.group()
def default():
    pass

@click.command()
@click.argument('container')
def run(container):

    """ attempts to start the docker container specified """

    try:
        this.client = fetch_client()
        this.client.pull(REGISTRY,stream=True)
        start_container(container)
        result = health_check(container)
    except docker.errors.APIError as e:
        click.echo('[!] Docker API Error: {}'.format(e[0]))

@click.command()
@click.argument('container')
def stop(container):

    """ attempts to stop the docker container specified """

    try:
        this.client = fetch_client()
        this.client.stop(container)
        this.client.prune_containers()
    except docker.errors.APIError as e:
        click.echo('[!] Error stopping container: {}'.format(e[0]))

default.add_command(run)
default.add_command(stop)

# Functions start here
def health_check(inst_name):

    def __check_state():
        cont_state = this.client.inspect_container(inst_name)['State']
        if cont_state['Status']=='running':
            return cont_state['Health']['Status']
        else:
            click.echo('[!] Container is not running!')

    repeat = 0
    while True:
        cont_status = __check_state()
        if cont_status == 'healthy':
            click.echo('[*] Your app is running on http://127.0.0.1:8888')
            return True
        elif cont_status == 'starting':
            if repeat > 6:
                return
            time.sleep(1)
            repeat += 1
        else:
            click.echo('[!] Container status: {}'.format(cont_status))
            return

def start_container(inst_name):
    this.client.create_container(
                        REGISTRY,
                        detach=False,
                        name=inst_name,
                        ports=[8888]
                        )
    this.client.start(inst_name)

def fetch_client(base_url=BASE_URL):
    return docker.APIClient(base_url=base_url, version='1.25')

if __name__=="__main__":
    default()
