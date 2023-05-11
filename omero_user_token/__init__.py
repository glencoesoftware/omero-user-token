#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 Glencoe Software, Inc. All rights reserved.
#
# This software is distributed under the terms described by the LICENSE.txt
# file you can find at the root of the distribution bundle.  If the file is
# missing please request a copy by contacting info@glencoesoftware.com

import os
import stat
import sys

import omero
import omero.all

from configparser import ConfigParser

from omero.rtypes import unwrap


def assert_and_get_token_dir():
    token_dir = os.getenv('OMERO_USER_TOKEN_DIR', default=None)
    if token_dir is None:
        home = os.path.expanduser('~')
        token_dir = os.path.join(home, '.omero_user_token')
    if not os.path.exists(token_dir):
        os.makedirs(token_dir)
    os.chmod(token_dir, stat.S_IRWXU)
    return token_dir


def assert_and_get_token_path():
    token_dir = assert_and_get_token_dir()
    return os.path.join(token_dir, 'token')


def assert_and_get_config_path():
    token_dir = assert_and_get_token_dir()
    return os.path.join(token_dir, 'config')


CONFIG = ConfigParser()
CONFIG.read(assert_and_get_config_path())

if not CONFIG.has_section('server'):
    CONFIG.add_section('server')
    CONFIG.set('server', 'host', 'localhost')
    CONFIG.set('server', 'port', '4064')


def setter(server, port, user, password, time_to_idle):
    client = omero.client(server, port)
    try:
        session = client.createSession(user, password)
        admin_service = session.getAdminService()
        session_service = session.getSessionService()
        ec = admin_service.getEventContext()
        token = '%s@%s:%s' % (unwrap(session_service.createUserSession(
            0,  # timeToLiveMilliseconds
            time_to_idle,  # timetoIdleMilliseconds
            ec.groupName  # defaultGroup
        ).uuid), server, port)
        with open(assert_and_get_token_path(), 'w') as token_file:
            token_file.write(token)
        return token
    finally:
        client.closeSession()


def get_token():
    """
    Returns the current user token
    Raises FileNotFoundError if the token file does not exist
    """
    with open(assert_and_get_token_path(), 'r') as token_path:
        return token_path.read().strip()


def login(token):
    """
    Returns an omero.client object from a valid token.  The
    session the token refers to has had a join attempt made upon it.
    """
    omero_session_key = token[:token.find('@')]
    host, port = token[token.find('@') + 1:].split(':')
    client = omero.client(host, int(port))
    try:
        session = client.joinSession(omero_session_key)
        session.detachOnDestroy()
    except Exception:
        pass
    return client


def getter():
    try:
        token = get_token()
        client = login(token)
        try:
            client.getSession()
        except Exception:
            sys.exit('ERROR: Token is invalid!')
        finally:
            client.closeSession()
        return token
    except FileNotFoundError:
        sys.exit('ERROR: No token available, `omero_user_token set` required!')
