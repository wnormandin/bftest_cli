# Basic command-line interface to manage docker containers which will use an
# image stored in a dockerhub registry - 'pokeybill/bftest'

import click
from click.testing import CliRunner
import docker
import sys
import time
import requests

this = sys.modules[__name__]
BASE_URL = 'unix://var/run/docker.sock'
REGISTRY = 'pokeybill/bftest'
DIGEST = 'sha256:79215d32e5896c1ccd3f57d22ee6aaa7c9d79c9c87737f2b96673186de6ab060'

@click.group()
def default():
    """ A basic docker container management wrapper """
    pass

@click.command()
@click.argument('container')
def run(container):

    """ attempts to start the docker container specified """

    try:
        this.client = fetch_client()
        this.client.pull(REGISTRY)
        start_container(container)
        result = health_check(container)
    except docker.errors.APIError as e:
        click.echo('[!] Docker API Error: {}'.format(e[0]))
        raise
        sys.exit(1)

@click.command()
@click.argument('container')
def stop(container):

    """ attempts to stop the docker container specified """

    try:
        this.client = fetch_client()
        this.client.stop(container)
        this.client.remove_container(container)
    except docker.errors.APIError as e:
        click.echo('[!] Error stopping container: {}'.format(e[0]))
        sys.exit(1)


@click.command()
def test():

    """ basic functional test to ensure containers can be managed """

    click.echo('[*] Testing docker container creation/removal')
    cont_name = 'funky_aardvark'

    try:
        runner = CliRunner()

        # Test the RUN command
        result = runner.invoke(run, [cont_name])
        result_txt = result.output.strip('\n')
        assert result.exit_code == 0, '[!] Application START failed: {}'.format(result_txt)
        assert 'Your app is running on' in result.output, \
               '[!] Unexpected output: {}'.format(result.output)
        click.echo(result_txt)

        # Test container access
        click.echo('[*] Ensuring we can communicate with the containerized application')
        result = requests.get('http://127.0.0.1:8888/hello')
        assert result.status_code == 200, \
               '[!] Unexpected HTTP response: {}'.format(result.status_code)
        click.echo('\t{}'.format(result.text))

        # Test the STOP command
        result = runner.invoke(stop, [cont_name])
        result_txt = result.output.strip('\n')
        assert result.exit_code == 0, '[!] Application STOP failed: {}'.format(result_txt)
        click.echo('[*] Container {} stopped'.format(cont_name))
    except requests.exceptions.ConnectionError as e:
        click.echo('[!] Failed to communicate with the application')
        click.echo(e[0])
    except AssertionError as e:
        click.echo('[*] Test failed - {}'.format(e))
    else:
        click.echo('[*] Test succeeded')

default.add_command(run)
default.add_command(stop)
default.add_command(test)

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
                        ports=[8888],
                        host_config=this.client.create_host_config(
                            port_bindings={8888: ('127.0.0.1',8888)}
                            ),
                        )
    this.client.start(inst_name)

def fetch_client(base_url=BASE_URL):
    this.client = docker.APIClient(base_url=base_url, version='1.24')
    try:
        this.client.version()
    except requests.exceptions.ConnectionError as e:
        click.echo('[!] Unable to connect to Docker daemon @ {}'.format(BASE_URL))
        sys.exit(1)

if __name__=="__main__":
    default()
