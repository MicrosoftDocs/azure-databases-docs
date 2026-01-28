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
ms.date: 07/22/2025
ai-usage: ai-generated
---

# Quickstart: Azure Cosmos DB for Apache Gremlin client library for Python

[!INCLUDE[Quickstart developer selector](includes/selector-quickstart-developer.md)]

[!INCLUDE[Note - Recommended services](includes/note-recommended-services.md)]

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
- [Insert data](#insert-data)
- [Read data](#read-data)
- [Query data](#query-data)

### Authenticate client

Start by authenticating the client using the credentials gathered earlier in this guide.

1. Open the *app.py* file in your integrated development environment (IDE).

1. Import the following types from the `gremlin_python.driver` library:

    - `gremlin_python.driver.client`
    - `gremlin_python.driver.serializer`

    ```python
    from gremlin_python.driver import client, serializer
    ```

1. Create string variables for the credentials collected earlier in this guide. Name the variables `hostname` and `primary_key`.

    ```python
    hostname = "<host>"
    primary_key = "<key>"
    ```

1. Create a `Client` object using the credentials and configuration variables created in the previous steps. Name the variable `client`.

    ```python
    client = client.Client(
        url=f"wss://{hostname}.gremlin.cosmos.azure.com:443/",
        traversal_source="g",
        username="/dbs/cosmicworks/colls/products",
        password=f"{primary_key}",
        message_serializer=serializer.GraphSONSerializersV2d0()
    )
    ```

### Insert data

Next, insert new vertex and edge data into the graph. Before creating the new data, clear the graph of any existing data.

1. Run the `g.V().drop()` query to clear all vertices and edges from the graph.

    ```python
    client.submit("g.V().drop()").all().result()
    ```

1. Create a Gremlin query that adds a vertex.

    ```python
    insert_vertex_query = (
        "g.addV('product')"
        ".property('id', prop_id)"
        ".property('name', prop_name)"
        ".property('category', prop_category)"
        ".property('quantity', prop_quantity)"
        ".property('price', prop_price)"
        ".property('clearance', prop_clearance)"
    )
    ```

1. Add a vertex for a single product.

    ```python
    client.submit(
        message=insert_vertex_query,
        bindings={
            "prop_id": "aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb",
            "prop_name": "Yamba Surfboard",
            "prop_category": "gear-surf-surfboards",
            "prop_quantity": 12,
            "prop_price": 850.00,
            "prop_clearance": False,
        },
    ).all().result()
    ```

1. Add two more vertices for two extra products.

    ```python
    client.submit(
        message=insert_vertex_query,
        bindings={
            "prop_id": "bbbbbbbb-1111-2222-3333-cccccccccccc",
            "prop_name": "Montau Turtle Surfboard",
            "prop_category": "gear-surf-surfboards",
            "prop_quantity": 5,
            "prop_price": 600.00,
            "prop_clearance": True,
        },
    ).all().result()

    client.submit(
        message=insert_vertex_query,
        bindings={
            "prop_id": "cccccccc-2222-3333-4444-dddddddddddd",
            "prop_name": "Noosa Surfboard",
            "prop_category": "gear-surf-surfboards",
            "prop_quantity": 31,
            "prop_price": 1100.00,
            "prop_clearance": False,
        },
    ).all().result()
    ```

1. Create another Gremlin query that adds an edge.

    ```python
    insert_edge_query = (
        "g.V([prop_partition_key, prop_source_id])"
        ".addE('replaces')"
        ".to(g.V([prop_partition_key, prop_target_id]))"
    )
    ```

1. Add two edges.

    ```python
    client.submit(
        message=insert_edge_query,
        bindings={
            "prop_partition_key": "gear-surf-surfboards",
            "prop_source_id": "bbbbbbbb-1111-2222-3333-cccccccccccc",
            "prop_target_id": "aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb",
        },
    ).all().result()

    client.submit(
        message=insert_edge_query,
        bindings={
            "prop_partition_key": "gear-surf-surfboards",
            "prop_source_id": "bbbbbbbb-1111-2222-3333-cccccccccccc",
            "prop_target_id": "cccccccc-2222-3333-4444-dddddddddddd",
        },
    ).all().result()
    ```

### Read data

Then, read data that was previously inserted into the graph.

1. Create a query that reads a vertex using the unique identifier and partition key value.

    ```python
    read_vertex_query = "g.V([prop_partition_key, prop_id])"
    ```

1. Then, read a vertex by supplying the required parameters.

    ```python
    matched_item = client.submit(
        message=read_vertex_query,
        bindings={
            "prop_partition_key": "gear-surf-surfboards",
            "prop_id": "aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb"
        }
    ).one()
    ```

### Query data

Finally, use a query to find all data that matches a specific traversal or filter in the graph.

1. Create a query that finds all vertices that traverse out from a specific vertex.

    ```python
    find_vertices_query = (
        "g.V().hasLabel('product')"
        ".has('category', prop_partition_key)"
        ".has('name', prop_name)"
        ".outE('replaces').inV()"
    )
    ```

1. Execute the query specifying the `Montau Turtle Surfboard` product.

    ```python
    find_results = client.submit(
        message=find_vertices_query,
        bindings={
            "prop_partition_key": "gear-surf-surfboards",
            "prop_name": "Montau Turtle Surfboard",
        },
    ).all().result()
    ```

1. Iterate over the query results.

    ```python
    for result in find_results:
        # Do something here with each result
    ```

## Run the code

Run the newly created application using a terminal in your application directory.

```bash
python app.py
```

## Clean up resources

[!INCLUDE[Section - Quickstart cleanup](includes/section-quickstart-cleanup.md)]
