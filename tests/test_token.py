#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2023 Glencoe Software, Inc. All rights reserved.
#
# This software is distributed under the terms described by the LICENSE.txt
# file you can find at the root of the distribution bundle.  If the file is
# missing please request a copy by contacting info@glencoesoftware.com


from omero_user_token import assert_and_get_token_dir
from omero_user_token import assert_and_get_token_path
from omero_user_token import get_token
from omero_user_token import getter
from omero_user_token import login

import omero
import os
import pytest
import uuid


class TestUserToken:

    @pytest.fixture(autouse=True)
    def set_up_token_dir(self, monkeypatch, tmpdir):
        self.token_dir = str(tmpdir / ".omero_user_token")
        monkeypatch.setenv("OMERO_USER_TOKEN_DIR", self.token_dir)
        self.token_path = str(tmpdir / ".omero_user_token" / "token")

    def write_token(self, token):
        os.makedirs(self.token_dir)
        with open(self.token_path, 'w') as f:
            f.write(token)

    def test_assert_and_get_token_dir(self):
        token_dir = assert_and_get_token_dir()
        assert token_dir == self.token_dir
        assert os.path.exists(token_dir)
        assert os.path.isdir(token_dir)

    def test_assert_and_get_token_path(self):
        token_path = assert_and_get_token_path()
        assert token_path == self.token_path
        assert os.path.exists(os.path.dirname(token_path))

    def test_get_token(self):
        token = "%s@localhost:4064" % uuid.uuid4()
        self.write_token(token)
        assert get_token() == token

    def test_get_token_file_not_found(self):
        with pytest.raises(FileNotFoundError):
            get_token()

    def test_login(self):
        token = "%s@localhost:4064" % uuid.uuid4()
        self.write_token(token)
        client = login(get_token())
        assert isinstance(client, omero.clients.BaseClient)

    @pytest.mark.parametrize("invalidtoken", (
        "%s", "%s@", "%s@localhost"))
    def test_login_invalid_token(self, invalidtoken):
        token = invalidtoken % uuid.uuid4()
        self.write_token(token)
        with pytest.raises(ValueError):
            login(get_token())

    def test_getter(self, monkeypatch):
        token = "%s@localhost:4064" % uuid.uuid4()
        self.write_token(token)
        monkeypatch.setattr(
            omero.clients.BaseClient, "getSession", lambda x: True)
        assert getter() == token

    def test_getter_invalid_session(self):
        token = "%s@localhost:4064" % uuid.uuid4()
        self.write_token(token)
        with pytest.raises(SystemExit):
            getter()
