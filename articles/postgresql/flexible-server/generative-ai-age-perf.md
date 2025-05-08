---
title: Apache AGE Performance Best Practices
description: Best practices for improving queries in Apache Age with Azure Database for PostgreSQL.
author: jojohnso-msft
ms.author: jojohnso
ms.reviewer: maghan
ms.date: 05/19/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: conceptual
ms.custom:
  - build-2025
# customer intent: As a user, I want to understand how to improve performance of my graph queries in Azure Database for PostgreSQL flexible server.
---

# Best Practices: Indexing, AGE EXPLAIN, and Data Load Benchmarks

## Introduction
Apache AGE supported by Azure Database for PostgreSQL, provides support for advanced graph processing and querying. However, achieving optimal query performance requires a thoughtful strategy for indexing and data loading. This guide outlines some best practices based on recent benchmarking results and technical insights.

## Indexing in Apache AGE
Indexing is pivotal for improving query performance, especially in graph databases. Below are the key recommendations to maximize the benefits of indexing.

### Default Indexing Behavior
By default, Apache AGE does not create indexes for newly created graphs. This necessitates explicit creation of indexes based on the nature of your queries and dataset.

### WHERE Clause
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
Unlike standard SQL, the EXPLAIN keyword in Cypher queries requires a different query format.

### Query:
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

### Result:
```
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

### Result:
```
QUERY PLAN
---------------------------------------------------------------
Seq Scan on "Customer" n (cost=0.00..396.56 rows=9 width=32)
Filter: (properties @> '{"Name": "Alice"}'::agtype)
```

## Common Index Types
- **BTREE Index**: Effective for exact matches and range queries. Recommended for use with columns like id, start_id, and end_id in edge and vertex tables.
- **GIN Index**: Useful for JSON fields, enabling efficient searches for key-value pairs in the properties column.

### Creating Common Indexes
Use the following commands to create indexes for vertex and edge tables:

#### Vertex Table:
```sql
CREATE INDEX ON graph_name."VLABEL" USING BTREE (id);
CREATE INDEX ON graph_name."VLABEL" USING GIN (properties);
```

#### Edge Table:
```sql
CREATE INDEX ON graph_name."ELABEL" USING BTREE (start_id);
CREATE INDEX ON graph_name."ELABEL" USING BTREE (end_id);
```

### Indexing a Specific Key-Value in Properties
For targeted queries, a smaller, more efficient BTREE index can be created for specific keys within the properties column:
```sql
CREATE INDEX ON graph_name.label_name USING BTREE (agtype_access_operator(VARIADIC ARRAY[properties, '"KeyName"'::agtype]));
```
This approach avoids indexing unnecessary data, improving efficiency.

## Query Plan Insights via EXPLAIN
The EXPLAIN keyword reveals how queries utilize indexes. Not all queries automatically leverage indexes, particularly those issued without a WHERE clause. Use EXPLAIN to verify index usage and optimize queries accordingly.

## Benchmarking Observations
Recent tests highlight the impact of indexing on query performance.

### Indexed vs. Non-indexed Queries
- Sequential scans outperform index scans for queries retrieving entire tables.
- Indexing significantly improves performance for join queries (e.g., relationship counts).

## Data Loading Best Practices
Efficient data loading is crucial for large datasets. The AGEFreighter library offers a streamlined process for data ingestion.

### Data Loading Using AGEFreighter
#### Environment Setup:
- Created an Azure Database for PostgreSQL flexible server with AGE enabled.
- Python dependency management tool such as Poetry is recommended. Python 3.9 or later must be installed.
- The AGEFreighter library (AGEFreighter PyPi) must be installed as a dependency:
```bash
poetry add agefreighter
```

#### CSV Data Format (Used in Benchmarking):
Since the dataset used consists of legal cases and relationships between them, I structured my input CSV file as follows:
```
id,CaseID,start_vertex_type,end_CaseID,end_vertex_type
1,1005631,Case,5030916,Case
2,1005631,Case,5028652,Case
3,1005631,Case,996512,Case
4,1005631,Case,3413065,Case
5,1005631,Case,4912975,Case
```
Each row represents a relationship between two cases. CaseID refers to the starting case node, while end_CaseID refers to the connected case.

#### Data Loading Script (Used in Benchmarking):
The following Python script was used to load my dataset into AGE. You may also refer to “Usage of CSVFreighter” section in AGEFreighter PyPi for a different example.
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

### Alternative Data Sources:
AGEFreighter supports other formats such as MultiCSV, Avro, Parquet, Azure Storage etc. which can be adapted based on data format requirements. You can get more information here: ['AGEFreighter PyPi'](https://pypi.org/project/agefreighter/)

## Data Loading Performance Benchmarks
- Dataset size: 725K cases, 2.8M relationships.
- Loading time: 83 seconds.

While suitable for large files, this process may be less effective for smaller datasets due to preparation time.

## Conclusion
Indexing and data loading strategies are critical for maximizing the performance of Apache AGE on Azure Database for PostgreSQL. Use EXPLAIN to analyze query execution plans, implement appropriate indexes, and leverage AGEFreighter for efficient data ingestion. Continuous benchmarking and query optimization based on real-world workloads will further enhance application performance.

