---
title: 'Quickstart: Python library'
titleSuffix: Azure Cosmos DB for Apache Gremlin
description: Create a new Azure Cosmos DB for Apache Gremlin account and connect using the Python library in this quickstart.
author: seesharprun
ms.author: sidandrews
ms.service: azure-cosmos-db
ms.subservice: apache-gremlin
ms.topic: quickstart-sdk
ms.devlang: python
ms.custom: devx-track-python, sfi-ropc-nochange
ms.date: 07/21/2025
ai-usage: ai-generated
---

# Quickstart: Azure Cosmos DB for Apache Gremlin client library for Python

[!INCLUDE[Quickstart developer selector](includes/selector-quickstart-developer.md)]

Get started with the Azure Cosmos DB for Apache Gremlin client library for Python to store, manage, and query unstructured data. Follow the steps in this guide to create a new account, install a Python client library, connect to the account, perform common operations, and query your final sample data.

[Library source code](https://github.com/apache/tinkerpop/tree/master/gremlin-python/src/main/python) | [Package (PyPi)](https://pypi.org/project/gremlinpython/)

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

1. Import the `gremlinpython` package from Python Package Index (PyPI).

    ```bash
    pip install gremlinpython
    ```

1. Create the **app.py** file.

## Object model

| | Description |
| --- | --- |
| **`GremlinClient`** | Represents the client used to connect and interact with the Gremlin server |
| **`GraphTraversalSource`** | Used to construct and execute Gremlin traversals |

## Code examples

- [Authenticate client](#authenticate-client)
- [Upsert data](#upsert-data)
- [Read data](#read-data)
- [Query data](#query-data)

### Authenticate client

Start by authenticating the client using the credentials gathered earlier in this guide.

1. Open the *app.py* file in your integrated development environment (IDE).

1. Import the following types from the `gremlin_python.driver` and `gremlin_python.process.graph_traversal` modules:
    - `GremlinClient`, `Client`
    - `GraphTraversalSource`, `g`, `__`

    ```python
    from gremlin_python.driver import client, serializer
    from gremlin_python.process.graph_traversal import __
    from gremlin_python.process.anonymous_traversal import traversal
    from gremlin_python.structure.graph import Graph
    ```

1. Create string variables for the credentials collected earlier in this guide. Name the variables `hostname`, `port`, and `primary_key`.

    ```python
    hostname = "<endpoint>"
    port = 443
    primary_key = "<key>"
    ```

1. Create a Gremlin client using the credentials and configuration variables created in the previous steps.

    ```python
    gremlin_client = client.Client(
        f'wss://{hostname}:{port}/gremlin',
        'g',
        username='/dbs/cosmicworks/colls/products',
        password=primary_key,
        message_serializer=serializer.GraphSONSerializersV2d0()
    )
    ```

### Upsert data

Next, upsert new data into the graph. Upserting ensures that the data is created or replaced appropriately depending on whether the same data already exists in the graph.

1. Add a vertex (upsert data) for a product:

    ```python
    add_vertex_query = """
    g.addV('product').property('id', 'surfboard1').property('name', 'Kiama classic surfboard').property('category', 'surf').property('price', 699.99)
    """
    gremlin_client.submitAsync(add_vertex_query).result()
    ```

1. Add another product vertex:

    ```python
    add_vertex_query2 = """
    g.addV('product').property('id', 'surfboard2').property('name', 'Montau Turtle Surfboard').property('category', 'surf').property('price', 799.99)
    """
    gremlin_client.submitAsync(add_vertex_query2).result()
    ```

1. Create an edge between the two products:

    ```python
    add_edge_query = """
    g.V('surfboard2').addE('replaces').to(g.V('surfboard1'))
    """
    gremlin_client.submitAsync(add_edge_query).result()
    ```

### Read data

Then, read data that was previously upserted into the graph.

1. Read a vertex by ID:

    ```python
    read_vertex_query = """
    g.V('surfboard1')
    """
    result = gremlin_client.submitAsync(read_vertex_query).result()
    for item in result:
        print(item)
    ```

1. Read all vertices:

    ```python
    read_all_query = """
    g.V()
    """
    result = gremlin_client.submitAsync(read_all_query).result()
    for item in result:
        print(item)
    ```

### Query data

Finally, use a query to find all data that matches a specific traversal or filter in the graph.

1. Query for all products in the 'surf' category:

    ```python
    query_products = """
    g.V().hasLabel('product').has('category', 'surf')
    """
    result = gremlin_client.submitAsync(query_products).result()
    for item in result:
        print(item)
    ```

1. Query for all products that replace another product:

    ```python
    query_replaces = """
    g.V().hasLabel('product').outE('replaces').inV()
    """
    result = gremlin_client.submitAsync(query_replaces).result()
    for item in result:
        print(item)
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
> [Overview of Azure Cosmos DB for Apache Gremlin](introduction.md)
