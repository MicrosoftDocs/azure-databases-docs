---
title: 'Quickstart: Python library'
titleSuffix: Azure Cosmos DB for Apache Cassandra
description: Create a new Azure Cosmos DB for Apache Cassandra account and connect using the Python library in this quickstart.
author: seesharprun
ms.author: sidandrews
ms.service: azure-cosmos-db
ms.subservice: apache-cassandra
ms.topic: quickstart-sdk
ms.devlang: python
ms.custom: devx-track-python, sfi-ropc-nochange
ms.date: 07/18/2025
---

# Quickstart: Azure Cosmos DB for Apache Cassandra client library for Python

[!INCLUDE[Quickstart developer selector](includes/selector-quickstart-developer.md)]

Get started with the Azure Cosmos DB for Apache Cassandra client library for Python to store, manage, and query unstructured data. Follow the steps in this guide to create a new account, install a Python client library, connect to the account, perform common operations, and query your final sample data.

[API reference documentation](https://docs.datastax.com/en/developer/python-driver/index.html) | [Library source code](https://github.com/datastax/python-driver) | [Package (PyPI)](https://pypi.org/project/cassandra-driver/)

## Prerequisites

[!INCLUDE[Prerequisites - Quickstart developer](../includes/prerequisites-quickstart-developer.md)]

- Python 3.12 or later

## Setting up

First, set up the account and development environment for this guide. This section walks you through the process of creating an account, getting its credentials, and then preparing your development environment.

### Create an account

[!INCLUDE[Section - Setting up](includes/section-quickstart-provision.md)]

### Get credentials

[!INCLUDE[Section - Get credentials](includes/section-quickstart-credentials.md)]

### Prepare development environment

Then, configure your development environment with a new project and the client library. This step is the last required prerequisite before moving on to the rest of this guide.

1. Start in an empty folder.

1. Import the `cassandra-driver` package from the Python Package Index (PyPI).

    ```bash
    pip install cassandra-driver
    ```

1. Create the *app.py* file.

## Object model

| | Description |
| --- | --- |
| **`Cluster`** | Represents a specific connection to a cluster |

## Code examples

- [Authenticate client](#authenticate-client)
- [Upsert data](#upsert-data)
- [Read data](#read-data)
- [Query data](#query-data)

### Authenticate client

Start by authenticating the client using the credentials gathered earlier in this guide.

1. Open the *app.py* file in your integrated development environment (IDE).

1. Import the following types from the `cassandra-driver` module:

    - `cassandra.cluster.Cluster`
    - `cassandra.auth.PlainTextAuthProvider`

    ```python
    from cassandra.cluster import Cluster
    from cassandra.auth import PlainTextAuthProvider
    ```

1. Import the following types from the `ssl` module:

    - `ssl.PROTOCOL_TLS_CLIENT`
    - `ssl.SSLContext`
    - `ssl.CERT_NONE`

    ```python
    from ssl import PROTOCOL_TLS_CLIENT, SSLContext, CERT_NONE
    ```

1. Create string variables for the credentials collected earlier in this guide. Name the variables `username`, `password`, and `contactPoint`.

    ```python
    username = "<username>"
    password = "<password>"
    contactPoint = "<contact-point>"
    ```

1. Configure the `SSLContext` by creating a new variable named `ssl_context`, setting the protocol to `PROTOCOL_TLS_CLIENT`, disabling the hostname check, and setting the verification mode to `CERT_NONE`.

    ```python
    ssl_context = SSLContext(PROTOCOL_TLS_CLIENT)
    ssl_context.check_hostname = False
    ssl_context.verify_mode = CERT_NONE
    ```

1. Create a new `PlainTextAuthProvider` object with the credentials specified in the previous steps. Store the result in a variable named `auth_provider`.

    ```python
    auth_provider = PlainTextAuthProvider(username=username, password=password)
    ```

1. Create a `Cluster` object using the credential and configuration variables created in the previous steps. Store the result in a variable named `cluster`.

    ```python
    cluster = Cluster([contactPoint], port=10350, auth_provider=auth_provider, ssl_context=ssl_context)
    ```

1. Connect to the cluster.

    ```python
    session = cluster.connect("cosmicworks")
    ```

### Upsert data

Next, upsert new data into a table. Upserting ensures that the data is created or replaced appropriately depending on whether the same data already exists in the table.

1. Create a new string variable named `insertQuery` with the Cassandra Query Language (CQL) query for inserting a new row.

    ```python
    insertQuery = """
    INSERT INTO
        product (id, name, category, quantity, price, clearance)
    VALUES
        (%(id)s, %(name)s, %(category)s, %(quantity)s, %(price)s, %(clearance)s)
    """
    ```

1. Create a new object with various properties of a new product and store it in a variable named `params`.

    ```python
    params = {
        "id": "aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb",
        "name": "Yamba Surfboard",
        "category": "gear-surf-surfboards",
        "quantity": 12,
        "price": 850.00,
        "clearance": False
    }
    ```

1. Use the `execute` function to run the query with the specified parameters.

    ```python
    session.execute(insertQuery, params)
    ```

### Read data

Then, read data that was previously upserted into the table.

1. Create a new string variable named `readQuery` with a CQL query that matches items with the same `id` field.

    ```python
    readQuery = "SELECT * FROM product WHERE id = %s"
    ```

1. Create a string variable named `id` with the same value as the product created earlier in this guide.

    ```python
    id = "aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb"
    ```

1. Use the `execute` function to run the query stored in `readQuery` passing in the `id` variable as an argument. Store the result in a variable named `readResults`.

    ```python
    readResults = session.execute(readQuery, (id,))
    ```

1. Use the `one` function get the expected single result. Store this single result in a variable named `matchedProduct`.

    ```python
    matchedProduct = readResults.one()
    ```

### Query data

Finally, use a query to find all data that matches a specific filter in the table.

1. Create string variables named `findQuery` and `category` with the CQL query and required parameter.

    ```python
    findQuery = "SELECT * FROM product WHERE category = %s ALLOW FILTERING"
    category = "gear-surf-surfboards"
    ```

1. Use the two string variables and the `execute` function to query multiple results. Store the result of this query in a variable named `findResults`.

    ```python
    findResults = session.execute(findQuery, (category,))
    ```

1. Use a `for` loop to iterate over the query results.

    ```python
    for row in findResults:
        # Do something here with each result
    ```

## Run the code

Run the newly created application using a terminal in your application directory.

```bash
python app.py
```

## Clean up resources

[!INCLUDE[Section - Quickstart cleanup](includes/section-quickstart-cleanup.md)]

## Next step

> [!div class="nextstepaction"]
> [Overview of Azure Cosmos DB for Apache Cassandra](introduction.md)
