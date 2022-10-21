## dockerhub-tags

#### Install
[Pipx](https://pypa.github.io/pipx/) recommended:
```
git clone https://github.com/yolabingo/dockerhub-tags 
pipx install dockerhub-tags/dist/dockerhubtags-0.1.0-py3-none-any.whl
```

else install in a Python virtualenv:
```
python3 -m venv dockerhubtags
cd dockerhubtags 
. bin/activate
git clone https://github.com/yolabingo/dockerhub-tags 
pip install dockerhub-tags/dist/dockerhubtags-0.1.0-py3-none-any.whl
```

#### Sample command
```
dockertags bitnami python --exclude-substrings debian --min_version 3.9 --max_version 3.10
3.9-prod
3.9
3.9.1-prod
3.9.1
3.9.2
3.9.2-prod
3.9.3
3.9.3-prod
3.9.4...
```
#### Usage
```
usage: dockertags [-h] [--exclude-substrings EXCLUDE_SUBSTRINGS [EXCLUDE_SUBSTRINGS ...]] [--include-substrings INCLUDE_SUBSTRINGS [INCLUDE_SUBSTRINGS ...]]
                  [--min_version MIN_VERSION] [--max_version MAX_VERSION] [--max_results MAX_RESULTS]
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
  --min_version MIN_VERSION, -v MIN_VERSION
                        Minimum included version number
  --max_version MAX_VERSION, -w MAX_VERSION
                        Maximum included version number
  --max_results MAX_RESULTS, -m MAX_RESULTS
                        Maximum number of results to pull, default=5000
```
