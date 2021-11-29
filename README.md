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

## Example usage

### Bash:
```bash
if omero_user_token get; then
    echo "Found valid token\n"
    token=$(omero_user_token get)
    key=$(echo "${token}" | cut -d "@" -f 1)
    server_details=$(echo "${token}" | cut -d "@" -f 2)
    host=$(echo "${server_details}" | cut -d ":" -f 1)
    port=$(echo "${server_details}" | cut -d ":" -f 2)
    echo "Connecting to ${host}:${port} with key ${key}"
else
    echo "No valid token found"
    exit -1
fi
```

### Python:
```python
import subprocess
import sys

command = ['omero_user_token', 'get']

completed = subprocess.run(
    command, timeout=60,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE)
if completed.returncode != 0:
    print("Non-zero return code " + str(completed.returncode))
    sys.exit(completed.stderr.decode('utf8'))
token = completed.stdout.decode('utf8')
host, port = token[token.find('@') + 1:].split(':')
port = int(port)
key = token[:token.find('@')]
print(f"Connecting to {host}:{port} with key {key}")
```

## License

The iSyntax converter is distributed under the terms of the BSD license.
Please see `LICENSE.txt` for further details.

