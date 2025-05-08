---
title: What is the Apache AGE extension?
description: Overview of Apache AGE and its capabilities in Azure Database for PostgreSQL.
author: jojohnso-msft
ms.author: jojohnso
ms.reviewer: maghan
ms.date: 05/19/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: conceptual
ms.custom:
  - build-2025
# customer intent: As a user, I want to understand what the Apache AGE extension is and how to enable it in Azure Database for PostgreSQL flexible server.
---

# Overview of AGE Extension with Azure Database for PostgreSQL

## Unlocking Graph Data Capabilities with Apache AGE

### Introduction to Apache AGE

Apache AGE (A Graph Extension) is a powerful PostgreSQL extension designed to seamlessly integrate graph database functionalities into the PostgreSQL ecosystem. Developed under the Apache Incubator project, AGE enables users to store and query graph data with efficiency and expressiveness by supporting the intuitive openCypher query language. It bridges the gap between relational and graph data, allowing developers to manage complex relationships and uncover insights that traditional databases might struggle to reveal.

Graph data, represented through nodes (entities) and edges (relationships), is increasingly recognized as essential for applications such as social networks, recommendation systems, fraud detection, network analysis, and knowledge graphs. Apache AGE provides a robust solution for handling such interconnected data, enabling advanced analyses and streamlined data management.

### Key Features of Apache AGE

- **Graph and Relational Data Integration**: AGE allows seamless interaction between graph data and relational data within PostgreSQL.
- **openCypher Query Language**: AGE supports this widely recognized query language for graph databases, simplifying query writing and maintenance.
- **Scalability and Reliability**: Built on PostgreSQL’s proven architecture, AGE inherits its scalability and enterprise-grade robustness.

### Why Use a Graph Database?

Graph databases excel at representing and querying complex and highly interconnected relationships. Unlike relational databases, which require multiple joins or document databases that aren't optimized for deep relationship traversal, graph databases naturally model relationships between entities. For example, querying “friends of friends” or the “shortest path between two points” is both more intuitive and efficient in a graph database.

AGE leverages PostgreSQL’s ACID-compliant transactional system, ensuring reliability and atomicity for graph queries. This integration facilitates advanced applications like Knowledge Graphs, which support AI-driven search and data generation by structuring facts and concepts as nodes and their interconnections as edges.

### How Azure Customers Can Enable AGE

Azure Database for PostgreSQL Flexible Server includes Apache AGE as an extension. Follow these steps to enable the extension in your instance:

#### 1. Access Server Parameters

Within the Azure Portal, navigate to the PostgreSQL Flexible Server instance and select the Server Parameters option. Adjust the following settings:

- **azure.extensions**: In the parameter filter, search for and enable AGE among the available extensions.

 :::image type="content" source="./media/generative-ai-age-overview/enable-age-extension.png" alt-text="Screenshot showing the server parameters for Azure Database for Postgres with the AGE extension selected." lightbox="./media/generative-ai-age-overview/enable-age-extension.png"::: 

 
- **shared_preload_libraries**: In the parameter filter, search for and enable AGE.

:::image type="content" source="./media/generative-ai-age-overview/enable-age-shared-preload-libraries.png" alt-text="Screenshot showing the shared preload libraries settings for Azure Database for PostgreSQL with AGE selected." lightbox="./media/generative-ai-age-overview/enable-age-shared-preload-libraries.png"::: 

Click Save to apply these changes. The server will restart automatically to activate the AGE extension.

*Note*: Failure to enable the shared_preload_libraries will result in the following error when you attempt to use the AGE schema in a query: “ERROR: unhandled cypher(cstring) function call error on first cypher query”

#### 2. Enable AGE Within PostgreSQL

Once the server restart is complete, connect to the PostgreSQL instance using the psql interpreter. Execute the following command to enable AGE:

```sql
CREATE EXTENSION IF NOT EXISTS AGE CASCADE;
```

Once successful, you will see `CREATE EXTENSION` as the query output. 

You can also query the pg_extension catalog table to confirm that AGE was enabled and check the version of the extension. 

```sql
SELECT * FROM pg_extension WHERE extname = 'age';
```


#### 3. Configure Schema Paths

AGE adds a schema called `ag_catalog`, which is essential for handling graph data. Ensure this schema is included in the search path by executing:

```sql
SET search_path=ag_catalog,"$user",public;
```

For Python you can set the schema path by executing:

```python
import psycopg as pg
with pg.Connection.connect(con_str + " options='-c search_path=ag_catalog,\"$user\",public'") as con:
```

Alternatively, this can be configured programmatically in your application.

By following these steps, you ensure that your PostgreSQL instance is properly configured to leverage the capabilities of the AGE extension, providing advanced graph database capabilities directly within PostgreSQL. This setup allows seamless integration of graph queries into your applications, unlocking powerful data relationships and insights. With the AGE extension enabled and configured, you are now ready to explore the full potential of graph analytics within your PostgreSQL environment.

## Important Tables in the ag_catalog Schema

- ag_graph
- ag__label

### `ag_graph`

The ag_graph table within the ag_catalog schema of Apache AGE serves as a repository for metadata related to graphs created within PostgreSQL via the `ag_catalog.create_graph` function. Specifically, it maintains details such as the graph's name and its associated namespace, which acts as a schema in PostgreSQL. This namespace organizes the graph’s structure and contains tables for storing vertex and edge data.

```sql
\d+ ag_graph
                                          Table "ag_catalog.ag_graph"
  Column   |     Type     | Collation | Nullable | Default | Storage | Compression | Stats target | Description
-----------+--------------+-----------+----------+---------+---------+-------------+--------------+-------------
 graphid   | oid          |           | not null |         | plain   |             |              |
 name      | name         |           | not null |         | plain   |             |              |
 namespace | regnamespace |           | not null |         | plain   |             |              |
Indexes:
    "ag_graph_graphid_index" UNIQUE, btree (graphid)
    "ag_graph_name_index" UNIQUE, btree (name)
    "ag_graph_namespace_index" UNIQUE, btree (namespace)
Referenced by:
    TABLE "ag_label" CONSTRAINT "fk_graph_oid" FOREIGN KEY (graph) REFERENCES ag_graph(graphid)
Access method: heap
```

### `ag_label`
The ag_label table stores metadata about lables used in AGE graphs. The ag_label table keeps track of these labels, associating them with their respective graphs and defining whether they represent vertices or edges. The entry includes the label's unique ID, the associated graph, any indexes, and the underlying PostgreSQL table that stores the data. 

```sql
\d+ ag_label
                                         Table "ag_catalog.ag_label"
  Column  |    Type    | Collation | Nullable | Default | Storage | Compression | Stats target | Description
----------+------------+-----------+----------+---------+---------+-------------+--------------+-------------
 name     | name       |           | not null |         | plain   |             |              |
 graph    | oid        |           | not null |         | plain   |             |              |
 id       | label_id   |           |          |         | plain   |             |              |
 kind     | label_kind |           |          |         | plain   |             |              |
 relation | regclass   |           | not null |         | plain   |             |              |
 seq_name | name       |           | not null |         | plain   |             |              |
Indexes:
    "ag_label_graph_oid_index" UNIQUE, btree (graph, id)
    "ag_label_name_graph_index" UNIQUE, btree (name, graph)
    "ag_label_relation_index" UNIQUE, btree (relation)
    "ag_label_seq_name_graph_index" UNIQUE, btree (seq_name, graph)
Foreign-key constraints:
    "fk_graph_oid" FOREIGN KEY (graph) REFERENCES ag_graph(graphid)
Access method: heap
```