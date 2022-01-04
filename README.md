# Python Microsoft Dynamic 365 Application Programming Interface
Python Microsoft Dynamic 365 Application Programming Interface

[![Python Version](https://img.shields.io/badge/python-3.7-blue.svg)][python-version]

[python-version]: https://www.python.org/

The Microsoft Dynamics 365 Application Programming Interface is a basic
REpresentational State Transfer (REST) framework. It provides 
integration to
[Microsoft Dataverse Web API](https://docs.microsoft.com/en-us/powerapps/developer/data-platform/webapi/overview)
resources.

## Table of Contents
* [Quick Start](#quick-start)
* [Authentication](#authentication)
* [Usage](#usage)

## Quick Start

### Installation

D365API can be installed with

```bash
python -m pip install d365api
```

or

```bash
pip install d365api
```

Import the module

```python
from D365API.D365API import D365API
```

## Authentication

The `D365API` framework allows user to authenticate the system using
[OAuth](https://en.wikipedia.org/wiki/OAuth). It accepts a fix list of
valid credentials to login to the system.

* **hostname:** the unique organization name for the environment
* **client_id:** the client (application) ID of the Azure registered application
* **client_secret:** the client secret (key) of the Azure registered application
* **tenant_id:** the tenant (directory) ID of the environment

```python
# Create an instance of D365API object and login
d365api = D365API(hostname=hostname,
                  client_id=client_id,
                  client_secret=client_secret,
                  tenant_id=tenant_id)
```

## Usage

### Create

```python
# Create payload
payload = {
    # Account Name
    'name': f'Microsoft Dynamics'
}

# Make a request to create the Account
# Get the return unique identifier (ID)
# The payload need to be serialized to JSON formatted str (json.dumps)
account_id = d365api.accounts.create(json.dumps(payload))
```

### Read

```python
# Make a request to read the Account
read_account = d365api.accounts.read(account_id)
```

### Update

```python
# Create payload
payload = {
    # Account Name
    'name': f'Power Platform'
}

# Make a request to update the Account with unique identifier (ID)
# Update the Account Name with the newly generated Account Name
update_account = d365api.accounts.update(account_id, json.dumps(payload))
```

### Delete

```python
# Make a request to delete the Account with unique identifier (ID)
delete_account = d365api.accounts.delete(account_id)
```