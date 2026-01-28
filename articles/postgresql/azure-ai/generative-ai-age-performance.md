---
title: Apache AGE Performance Best Practices
description: Best practices for improving queries in Apache Age with Azure Database for PostgreSQL.
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
# customer intent: As a user, I want to understand how to improve performance of my graph queries in Azure Database for PostgreSQL.
---

# Best practices: indexing, AGE EXPLAIN, and data load benchmarks

Apache AGE supported by Azure Database for PostgreSQL, provides support for advanced graph processing and querying. However, achieving optimal query performance requires a thoughtful strategy for indexing and data loading. This guide outlines some best practices based on recent benchmarking results and technical insights.

## Indexing in Apache AGE

Indexing is pivotal for improving query performance, especially in graph databases.

### Default behavior

By default, Apache AGE doesn't create indexes for newly created graphs. This necessitates explicit creation of indexes based on the nature of your queries and dataset.

### WHERE clause

In Apache AGE, the following queries are evaluated differently:

```sql
SELECT * FROM cypher('graph_name',
 $$
 MATCH (n:Customer {Name:'Alice'}) RETURN n
 $$)
AS (n agtype);
```

```sql
SELECT * FROM cypher('graph_name',
 $$
 MATCH (n:Customer) WHERE n.Name='Alice' RETURN n
 $$)
AS (n agtype);
```

To take full advantage of indexing, you must understand which types of indexes are utilized by queries with and without a WHERE clause.

## EXPLAIN in Apache AGE

Unlike standard SQL, the EXPLAIN keyword in Cipher queries requires a different query format.

```sql
SELECT * FROM cypher('graph_name',
 $$
 EXPLAIN
 MATCH (n:Customer)
 WHERE n.Name='Alice'
 RETURN n
 $$)
AS (plan text);
```

```output
QUERY PLAN
--------------------------------------------------------------------------------------------------------------
Seq Scan on "Customer" n (cost=0.00..418.51 rows=43 width=32)
Filter: (agtype_access_operator(VARIADIC ARRAY[properties, '"Name"'::agtype]) = '"Alice"'::agtype)
```

To see the differences of query plans without WHERE clause:

```sql
SELECT * FROM cypher('graph_name',
 $$
 MATCH (n:Customer {Name:'Alice'}) RETURN n
 $$)
AS (n agtype);
```

```output
QUERY PLAN
---------------------------------------------------------------
Seq Scan on "Customer" n (cost=0.00..396.56 rows=9 width=32)
Filter: (properties @> '{"Name": "Alice"}'::agtype)
```

## Common index types

- **BTREE Index**: Effective for exact matches and range queries. Recommended for use with columns like ID, start_id, and end_id in edge and vertex tables.
- **GIN Index**: Useful for JSON fields, enabling efficient searches for key-value pairs in the properties column.

Use the following commands to create indexes for vertex and edge tables:

- Vertex table:

  ```sql
  CREATE INDEX ON graph_name."VLABEL" USING BTREE (id);
  CREATE INDEX ON graph_name."VLABEL" USING GIN (properties);
  ```

- Microsoft Edge table:

  ```sql
  CREATE INDEX ON graph_name."ELABEL" USING BTREE (id);
  CREATE INDEX ON graph_name."ELABEL" USING GIN (properties);
  ```

  ```sql
  CREATE INDEX ON graph_name."ELABEL" USING BTREE (start_id);
  CREATE INDEX ON graph_name."ELABEL" USING BTREE (end_id);
  ```

### Indexing a specific key-value in properties

For targeted queries, a smaller, more efficient BTREE index can be created for specific keys within the properties column:

```sql
CREATE INDEX ON graph_name.label_name USING BTREE (agtype_access_operator(VARIADIC ARRAY[properties, '"KeyName"'::agtype]));
```

This approach avoids indexing unnecessary data, improving efficiency.

## Query plan insights with EXPLAIN

The EXPLAIN keyword reveals how queries utilize indexes. Not all queries automatically use indexes, particularly those issued without a WHERE clause. Use EXPLAIN to verify index usage and optimize queries accordingly.

## Benchmark observations

Recent tests highlight the impact of indexing on query performance.

### Indexed vs. nonindexed queries

This section discusses the performance differences between indexed and nonindexed queries.

- Sequential scans outperform index scans for queries retrieving entire tables.
- Indexing significantly improves performance for join queries (for example, relationship counts).

## Data loading best practices

Efficient data loading is crucial for large datasets.

The AGEFreighter library offers a streamlined process for data ingestion.

### Data loading with AGEFreighter

AGEFreighter is a Python library designed to facilitate the loading of data into Apache AGE. It supports various data formats, including CSV, Avro, and Parquet, and provides a simple interface for loading data into AGE graphs.

#### Environment setup

- Created an Azure Database for PostgreSQL flexible server instance with AGE enabled.
- Python dependency management tool such as Poetry is recommended. Python 3.9 or later must be installed.
- The AGEFreighter library (AGEFreighter PyPi) must be installed as a dependency:

```bash
poetry add agefreighter
```

#### Use the CSV data format for benchmarks

For the benchmarks, I used a CSV file to load data into AGE. The CSV format is widely supported and easy to work with, making it a good choice for data loading tasks.

Since the dataset used consists of legal cases and relationships between them, I structured my input CSV file as follows:

```csv
id,CaseID,start_vertex_type,end_CaseID,end_vertex_type
1,1005631,Case,5030916,Case
2,1005631,Case,5028652,Case
3,1005631,Case,996512,Case
4,1005631,Case,3413065,Case
5,1005631,Case,4912975,Case
```

Each row represents a relationship between two cases. CaseID refers to the starting case node, while end_CaseID refers to the connected case.

#### Use the data loading script for benchmarks

The following Python script was used to load my dataset into AGE. You might also refer to "Usage of CSVFreighter" section in AGEFreighter PyPi for a different example.

```python
await instance.load(
 graph_name="CaseGraphFull",
 start_v_label="Case",
 start_id="CaseID",
 start_props=[],
 edge_type="REF",
 edge_props=[],
 end_v_label="Case",
 end_id="end_CaseID",
 end_props=[],
 csv_path="./cases.csv",
 use_copy=True,
 drop_graph=True,
 create_graph=True,
 progress=True,
)
```
As you can see, the graph_name and fields in the provided csv file is defined here. The use_copy=True parameter ensures efficient data loading. The drop_graph=True and create_graph=True parameters ensure a fresh start before loading new data.

### Other data sources

AGEFreighter supports other formats such as MultiCSV, Avro, Parquet, Azure Storage, etc. which can be adapted based on data format requirements. You can get more information here: ['AGEFreighter PyPi'](https://pypi.org/project/agefreighter/)

## Data loading performance benchmarks

- Dataset size: 725K cases, 2.8M relationships.
- Loading time: 83 seconds.

Efficient data loading is essential for handling large datasets effectively.

> [!NOTE]  
> While suitable for large files, this process might be less effective for smaller datasets due to preparation time.

## Related content

- [Azure Database for PostgreSQL documentation](../overview.md)
- [PostgreSQL extension for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-ossdata.vscode-postgresql)
- [GitHub Copilot extension](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot)
- [GitHub Copilot Chat extension](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot-chat)
- [MSSQL extension for Visual Studio Code?](/sql/tools/visual-studio-code-extensions/mssql/mssql-extension-visual-studio-code)
