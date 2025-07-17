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
ms.date: 07/17/2025
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

1. Import the `` package from the Python Package Index (PyPI).

    ```bash
    pip install 
    ```

1. Create the **app.py** file.

## Object model

| | Description |
| --- | --- |
| **``** | |
| **``** | |
| **``** | |

## Code examples

- [Authenticate client](#authenticate-client)
- [Upsert data](#upsert-data)
- [Read data](#read-data)
- [Query data](#query-data)

### Authenticate client

Start by authenticating the client using the credentials gathered earlier in this guide.

1. Open the **app.py** file in your integrated development environment (IDE).

1. Import `` and `` from the `` module.

1. TODO

1. TODO

    ```python
    
    ```

1. TODO

    ```python
    
    ```

1. TODO

    ```python
    
    ```

1. TODO

    ```python
    
    ```

1. TODO

    ```python
    
    ```

### Upsert data

Next, upsert new data into a table. Upserting ensures that the data is created or replaced appropriately depending on whether the same data already exists in the table.

1. TODO

1. TODO

    ```python
    
    ```

1. TODO

    ```python
    
    ```

1. TODO

    ```python
    
    ```

1. TODO

    ```python
    
    ```

1. TODO

    ```python
    
    ```

### Read data

Then, read data that was previously upserted into the table.

1. TODO

1. TODO

    ```python
    
    ```

1. TODO

    ```python
    
    ```

1. TODO

    ```python
    
    ```

1. TODO

    ```python
    
    ```

1. TODO

    ```python
    
    ```

### Query data

Finally, use a query to find all data that matches a specific filter in the table.

1. TODO

1. TODO

    ```python
    
    ```

1. TODO

    ```python
    
    ```

1. TODO

    ```python
    
    ```

1. TODO

    ```python
    
    ```

1. TODO

    ```python
    
    ```

## Run the code

Run the newly created application using a terminal in your application directory.

```bash
python app.py
```

## Clean up resources

[!INCLUDE[Section - Quickstart cleanup](includes/section-quickstart-credentials.md)]

## Next step

> [!div class="nextstepaction"]
> [Overview of Azure Cosmos DB for Apache Cassandra](introduction.md)
