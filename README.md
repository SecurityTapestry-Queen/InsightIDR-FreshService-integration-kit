# InsightIDR + FreshService Helpdesk Integration Kit

## V2.0.7 - as of 6/17/23

## Status

[![CodeQL](https://github.com/SecurityTapestry-Queen/is-fs-integration-st/actions/workflows/codeql.yml/badge.svg?branch=main)](https://github.com/SecurityTapestry-Queen/is-fs-integration-st/actions/workflows/codeql.yml)

[![Pylint](https://github.com/SecurityTapestry-Queen/is-fs-integration-st/actions/workflows/pylint.yml/badge.svg?branch=main)](https://github.com/SecurityTapestry-Queen/is-fs-integration-st/actions/workflows/pylint.yml)

[![Investigations](https://github.com/SecurityTapestry-Queen/is-fs-integration-st/actions/workflows/Investigations.yml/badge.svg?branch=main)](https://github.com/SecurityTapestry-Queen/is-fs-integration-st/actions/workflows/Investigations.yml)

### Licensed under GPL v3.0

### Notice

> This is for use by the Security Tapestry Threat Hunting Team, and is written for compatibility with **InsightIDR** as an Alerts Platform, and **FreshService Helpdesk**.

## Important Files

1. [config.json](config.json) - Includes Configuration data for each client
    
    - 'enabled' - Denotes whether or not to activate alerts for this client.
    - 'api' - API Key symbol per client.
    - 'email' - Mail Email Address Alerts are to be directed to per client.
    - 'ccs' - Email Addresses to CC upon Investigation creation per client.
    - 'time' - Time in UTC of last bot check-in per client.

2. [insight_functions.py](insight_functions.py) - Contains all Functions called by [investigations_to_fs.py](investigations_to_fs.py)

3. [investigations_to_fs.py](investigations_to_fs.py) - Main script to be run, contains statement:
```python
from insight_functions import *
```

4. [Investigations.yml](.github/workflows/Investigations.yml) - Main Workflow file for Github Actions, calls all API Keys and [investigations_to_fs.py](investigations_to_fs.py) every 15 minutes via cronjob.
