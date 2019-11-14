# encoding: utf-8
#
# Copyright (c) 2019 Glencoe Software, Inc. All rights reserved.
#
# This software is distributed under the terms described by the LICENCE file
# you can find at the root of the distribution bundle.
# If the file is missing please request a copy by contacting
# support@glencoesoftware.com.

import getpass

import click

from .. import CONFIG, getter, setter


@click.group()
def cli():
    pass


@click.command()
@click.option(
    '-s', '--server', default=CONFIG.get('server', 'host'), show_default=True,
    help="OMERO server hostname"
)
@click.option(
    '-p', '--port', default=CONFIG.getint('server', 'port'), type=int,
    show_default=True,
    help="OMERO server port"
)
@click.option(
    '-u', '--user', default=getpass.getuser(), show_default=True,
    help="OMERO username"
)
@click.option(
    '--time_to_idle', default=2**31 - 1, type=int,
    help="Number of seconds to set the timeToIdle value to; "
         "defaults to maximum allowed"
)
def _set(server, port, user, time_to_idle):
    password = getpass.getpass("Password: ")
    token = setter(server, port, user, password, time_to_idle)
    print('Successfuly set token: %s' % token)


@click.command()
def _get():
    token = getter()
    if token is not None:
        print(token)


cli.add_command(_set, name='set')
cli.add_command(_get, name='get')


def main():
    cli()
