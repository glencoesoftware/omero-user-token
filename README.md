# OMERO user token

Python package that creates long running user tokens for use with the OMERO
API under non-interactive, headless conditions.

## Requirements

* OMERO 5.4.0 or later


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

The iSyntax converter is distributed under the terms of the BSD license.
Please see `LICENSE.txt` for further details.

