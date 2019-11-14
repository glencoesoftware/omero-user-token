#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 Glencoe Software, Inc. All rights reserved.
#
# This software is distributed under the terms described by the LICENSE.txt
# file you can find at the root of the distribution bundle.  If the file is
# missing please request a copy by contacting info@glencoesoftware.com

import os

import omero
import omero.all

from configparser import ConfigParser

from omero.rtypes import unwrap


def assert_and_get_token_dir():
    home = os.path.expanduser('~')
    token_dir = os.path.join(home, '.omero_user_token')
    if not os.path.exists(token_dir):
        os.makedirs(token_dir)
    os.chmod(token_dir, 0700)
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
    client = omero.client(server.encode('utf-8'), port)
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


def getter():
    token_path = assert_and_get_token_path()
    if os.path.exists(token_path):
        with open(token_path, 'r') as token_file:
            return token_file.read()
