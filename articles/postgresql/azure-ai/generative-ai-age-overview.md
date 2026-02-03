---
title: Apache AGE Extension
description: Overview of Apache AGE and its capabilities in Azure Database for PostgreSQL.
author: shreyaaithal
ms.author: shaithal
ms.reviewer: maghan
ms.date: 01/20/2026
ms.service: azure-database-postgresql
ms.subservice: ai-graph
ms.topic: concept-article
ms.collection:
  - ce-skilling-ai-copilot
ms.update-cycle: 180-days
ms.custom:
  - build-2025
# customer intent: As a user, I want to understand what the Apache AGE extension is and how to enable it in Azure Database for PostgreSQL flexible server instances.
---

# AGE extension with Azure Database for PostgreSQL

Apache AGE (a graph extension) is a powerful PostgreSQL extension designed to seamlessly integrate graph database functionalities into the PostgreSQL ecosystem. AGE enables users to store and query graph data efficiently and expressively by supporting the intuitive openCypher query language, when developed under the Apache Incubator project. It bridges the gap between relational and graph data, allowing developers to manage complex relationships and uncover insights that traditional databases might struggle to reveal.

Graph data, represented through nodes (entities) and edges (relationships), is increasingly recognized as essential for applications such as social networks, recommendation systems, fraud detection, network analysis, and knowledge graphs. Apache AGE provides a robust solution for handling such interconnected data, enabling advanced analyses and streamlined data management.

## Unlocking graph data capabilities with Apache AGE

Unlocking graph data capabilities with Apache AGE empowers developers to harness the full potential of interconnected data within PostgreSQL. Apache AGE enables seamless exploration and analysis of complex relationships by integrating graph database functionality directly into the relational database. This capability is valuable for applications requiring deep insights into data connections, such as social networks, fraud detection, and recommendation systems. With its support for the openCypher query language and robust PostgreSQL foundation, Apache AGE provides a scalable and efficient solution for managing and querying graph data.

## Key features of Apache AGE

- **Graph and Relational Data Integration**: AGE allows seamless interaction between graph and relational data within PostgreSQL.
- **openCypher Query Language**: AGE supports this widely recognized query language for graph databases, simplifying query writing and maintenance.
- **Scalability and Reliability**: Under PostgreSQL's proven architecture, AGE inherits its scalability and enterprise-grade robustness.

## Why use a graph database?

Graph databases excel at representing and querying complex and highly interconnected relationships. Unlike relational databases, which require multiple joins or document databases that aren't optimized for deep relationship traversal, graph databases naturally model relationships between entities. For example, querying "friends of friends" or the "shortest path between two points" is more intuitive and efficient in a graph database.

AGE uses PostgreSQL's ACID-compliant transactional system, ensuring reliability and atomicity for graph queries. This integration facilitates advanced applications like Knowledge Graphs, which support AI-driven search and data generation by structuring facts and concepts as nodes and their interconnections as edges.

## Azure customers can enable the AGE extension

Azure Database for PostgreSQL includes Apache AGE as an extension.

These steps help you to enable the extension in your flexible server instance:

### Access server parameters

Within the Azure portal, navigate to the PostgreSQL flexible server instance and select the Server Parameters option.

Adjust the following settings:

- **azure.extensions**: Search for and enable AGE among the available extensions in the parameter filter.
- **shared_preload_libraries**: Search for and enable AGE in the parameter filter.

Select Save to apply these changes. The server restarts automatically to activate the AGE extension.

> [!NOTE]  
> Failure to enable the `shared_preload_libraries` results in the following error when you attempt to use the AGE schema in a query: "ERROR: unhandled cipher(cstring) function call error on first cipher query"

### Enable AGE in PostgreSQL

Once the server restarts, connect to the PostgreSQL instance using the psql interpreter. Execute the following command to enable AGE:

```sql
CREATE EXTENSION IF NOT EXISTS AGE CASCADE;
```

Once successful, you see `CREATE EXTENSION` as the query output.

You can also query the pg_extension catalog table to confirm that AGE was enabled and check the extension's version.

```sql
SELECT * FROM pg_extension WHERE extname = 'age';
```

### Configure schema paths

AGE adds a schema called `ag_catalog`, essential for handling graph data. Ensure this schema is included in the search path by executing:

```sql
SET search_path=ag_catalog,"$user",public;
```

For Python, you can set the schema path by executing:

```python
import psycopg as pg
with pg.Connection.connect(con_str + " options='-c search_path=ag_catalog,\"$user\",public'") as con:
```

It can also be configured programmatically in your application.

By following these steps, you ensure that your PostgreSQL instance is properly configured to use the AGE extension's capabilities. The AGE extension provides advanced graph database capabilities directly within PostgreSQL. This setup allows seamless integration of graph queries into your applications, unlocking powerful data relationships, and insights. With the AGE extension enabled and configured, you're now ready to explore the full potential of graph analytics within your PostgreSQL environment.

## Important tables in the ag_catalog schema

- `ag_graph`
- `ag_label`

### ag_graph

The ag_graph table within the ag_catalog schema of Apache AGE serves as a repository for metadata related to graphs created within PostgreSQL via the `ag_catalog.create_graph` function. Specifically, it maintains details such as the graph's name and associated namespace, which acts as a schema in PostgreSQL. This namespace organizes the graph's structure and contains tables for storing vertex and edge data.

```sql
\d+ ag_graph
```

```output
                                          Table "ag_catalog.ag_graph"
 Column   |     Type | Collation | Nullable | Default | Storage | Compression | Stats target | Description
-----------+--------------+-----------+----------+---------+---------+-------------+--------------+-------------
 graphid   | oid |           | not null |         | plain   |             |              |
 name | name |           | not null |         | plain   |             |              |
 namespace | regnamespace |           | not null |         | plain   |             |              |
Indexes:
    "ag_graph_graphid_index" UNIQUE, btree (graphid)
    "ag_graph_name_index" UNIQUE, btree (name)
    "ag_graph_namespace_index" UNIQUE, btree (namespace)
Referenced by:
    TABLE "ag_label" CONSTRAINT "fk_graph_oid" FOREIGN KEY (graph) REFERENCES ag_graph(graphid)
Access method: heap
```

### ag_label

The ag_label table stores metadata about labels used in AGE graphs. It keeps track of these labels, associating them with their respective graphs and defining whether they represent vertices or edges. The entry includes the label's unique ID, the associated graph, any indexes, and the underlying PostgreSQL table that stores the data.

```sql
\d+ ag_label
```

```output
                                   Table "ag_catalog.ag_label"
 Column  |    Type | Collation | Nullable | Default | Storage | Compression | Stats target | Description
----------+------------+-----------+----------+---------+---------+-------------+--------------+-------------
 name | name |           | not null |         | plain   |             |              |
 graph    | oid |           | not null |         | plain   |             |              |
 id       | label_id   |           |          |         | plain   |             |              |
 kind     | label_kind |           |          |         | plain   |             |              |
 relation | regclass   |           | not null |         | plain   |             |              |
 seq_name | name |           | not null |         | plain   |             |              |
Indexes:
"ag_label_graph_oid_index" UNIQUE, btree (graph, id)
"ag_label_name_graph_index" UNIQUE, btree (name, graph)
"ag_label_relation_index" UNIQUE, btree (relation)
"ag_label_seq_name_graph_index" UNIQUE, btree (seq_name, graph)
Foreign-key constraints:
- `fk_graph_oid` FOREIGN KEY (graph) REFERENCES ag_graph(graphid)
Access method: heap
```

## Related content

- [Azure Database for PostgreSQL documentation](../overview.md)
- [PostgreSQL extension for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-ossdata.vscode-postgresql)
- [GitHub Copilot extension](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot)
- [GitHub Copilot Chat extension](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot-chat)
- [MSSQL extension for Visual Studio Code?](/sql/tools/visual-studio-code-extensions/mssql/mssql-extension-visual-studio-code)
