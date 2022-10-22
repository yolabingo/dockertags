## dockertags

#### Install
[Pipx](https://pypa.github.io/pipx/) recommended:
```
git clone https://github.com/yolabingo/dockertags 
pipx install dockertags/dist/dockertags-0.1.0-py3-none-any.whl
dockertags --help
```
else, install in a Python virtualenv:
```
python3 -m venv dockertags
cd dockertags 
. bin/activate
git clone https://github.com/yolabingo/dockertags 
pip install dockertags/dist/dockertags-0.1.0-py3-none-any.whl
dockertags --help
```
else, run `src/dockertags/cli.py` directly, requires only [python requests library](https://requests.readthedocs.io/en/latest/)

#### Sample commands
Note: use namespace `library` for Official repos like [redis](https://hub.docker.com/_/redis)

`dockertags library redis --exclude-substrings alpine rc --min-version 7.0.4`
```
7.0.4
7.0.4-bullseye
7.0.5
7.0.5-bullseye
latest
...
```
`dockertags bitnami python --exclude-substrings debian --min-version 3.9 --max-version 3.10`
```
3.9-prod
3.9
3.9.1-prod
...
```
#### Usage
Note - by default ``--max-results` is a relatively modest 2k as Docker Hub API appears to have conservative rate limits.

```
usage: dockerhub.py [-h] [--exclude-substrings EXCLUDE_SUBSTRINGS [EXCLUDE_SUBSTRINGS ...]] [--include-substrings INCLUDE_SUBSTRINGS [INCLUDE_SUBSTRINGS ...]] [--min-version MIN_VERSION] [--max-version MAX_VERSION]
                    [--max-results MAX_RESULTS]
                    namespace repository

Gets Tags for a Docker Hub repository

positional arguments:
  namespace             Docker Hub namespace
  repository            Docker Hub repository

options:
  -h, --help            show this help message and exit
  --exclude-substrings EXCLUDE_SUBSTRINGS [EXCLUDE_SUBSTRINGS ...], -x EXCLUDE_SUBSTRINGS [EXCLUDE_SUBSTRINGS ...]
                        Tags containing these substrings will be excluded, e.g. 'SNAPSHOT test'
  --include-substrings INCLUDE_SUBSTRINGS [INCLUDE_SUBSTRINGS ...], -i INCLUDE_SUBSTRINGS [INCLUDE_SUBSTRINGS ...]
                        Tags containing these substrings will be included, e.g. 'lts debian'
  --min-version MIN_VERSION, -v MIN_VERSION
                        Minimum included version number
  --max-version MAX_VERSION, -w MAX_VERSION
                        Maximum included version number
  --max-results MAX_RESULTS, -m MAX_RESULTS
                        Maximum number of results to pull, default=2000
```
