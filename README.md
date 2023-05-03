# OMERO user token

Python package that creates long running user tokens for use with the OMERO
API under non-interactive, headless conditions.

## Requirements

* Python 3.6+
* OMERO.server 5.6

## Usage

Creating a user token and making it active:

    omero_user_token set

Please see `omero_user_token set --help` for detailed information.  The
default server hostname and port can be set in
`${HOME}/.omero_user_token/config` using an INI file compatible style:

    [server]
    host = omero.example.com
    port = 4064

Retrieving the current active token (validation will be performed):

    omero_user_token get

## Token format

The token format is as follows:

    <omero_session_key>@<host>:<port>

## License

OMERO user token is distributed under the terms of the GPL v2 license.
Please see `LICENSE.txt` for further details.
