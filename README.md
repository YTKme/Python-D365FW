# Python Microsoft Dynamic 365 Application Programming Interface
Python Microsoft Dynamic 365 Application Programming Interface

[![Python Version](https://img.shields.io/badge/python-3.7-blue.svg)][python-version]

[python-version]: https://www.python.org/

A basic Python REST API client built for Python 3.0+.
This framework provide an integration to the [Microsoft Dynamics 365 Web API](https://docs.microsoft.com/en-us/powerapps/developer/common-data-service/webapi/overview) resources.

## Table of Contents
* [Authentication](#authentication)

## Authentication

```python
# Create an instance of Access object
access = Access(hostname=hostname,
                client_id=client_id,
                client_secret=client_secret,
                tenant_id=tenant_id)

# Use the Access object to login
access_token = access.login()

# You can also do it all in one step
# Create an instance of Access object and login
access = Access(hostname=hostname,
                client_id=client_id,
                client_secret=client_secret,
                tenant_id=tenant_id).login()
```