---
title: DiskANN on Azure Database for PostgreSQL
description: Enable diskANN for improved semantic similarity search for Retrieval Augmented Generation (RAG) on Azure Database for PostgreSQL.
author: abeomor
ms.author: abeomorogbe
ms.reviewer: maghan
ms.date: 09/27/2024
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
# customer intent: As a user, I want to understand the overview and how to use diskann extension for Azure Database for PostgreSQL - Flexible Server.
---

# How to enable and use diskann extension for Azure Database for PostgreSQL - Flexible Server (Preview)

DiskANN is a scalable approximate nearest neighbor search algorithm for efficient vector search at any scale. It offers high recall, high queries per second (QPS), and low query latency, even for billion-point datasets. This makes it a powerful tool for handling large volumes of data. [Learn more about DiskANN from Microsoft](https://www.microsoft.com/en-us/research/project/project-akupara-approximate-nearest-neighbor-search-for-large-scale-semantic-search/)

The `pg_diskann` extension for Azure Database for PostgreSQL flexible server adds support for using the DiskANN for efficient vector indexing and searching.

## Enroll in the `pg_diskann` Preview Feature
`pg_diskann` for Azure Database for PostgreSQL - Flexible Server requires users to sign up via our Preview form. Follow the below steps to register:

1. Open the [preview form](https://aka.ms/pg-diskann-form)
2. Fill out all relevant details. We will need your Azure subscription ID for enablement.

> [!NOTE]
> After fill out the preview form it will take some time for your request to be approved. Confirmation will be sent to your email.

## Enable `pg_diskann` extension

Before you can enable `pg_diskann` on your Azure Database for PostgreSQL flexible server instance, you need to add it to your allowlist as described in [how to use PostgreSQL extensions](../extensions/how-to-allow-extensions.md#allow-extensions), and check if correctly added by running `SHOW azure.extensions;`.

:::image type="content" source="media/how-to-use-pgdiskann/select-diskann-azure-extension.png" alt-text="Screenshot of selecting pg_diskann in server parameters." lightbox="media/how-to-use-pgdiskann/select-diskann-azure-extension.png":::

> [!IMPORTANT]
> This preview feature is only available for newly deployed Azure Database for PostgreSQL Flexible Server instances.

Then, you can install the extension by connecting to your target database and running the [CREATE EXTENSION](https://www.postgresql.org/docs/current/static/sql-createextension.html) command. You need to repeat the command separately for every database in which you want the extension to be available.

```sql
CREATE EXTENSION IF NOT EXISTS pg_diskann CASCADE;
```
*This command enables `pgvector` if it hasn't already been installed in your PostgreSQL database.*

> [!NOTE]
> To remove the extension from the currently connected database use `DROP EXTENSION vector;`.

## Using `diskann` Index Access Method

Once the extension is installed, you can create a `diskann` index on a table column that contains vector data. For example, to create an index on the `embedding` column of the `my_table` table, use the following command:

```sql
CREATE TABLE my_table (
 id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
 embedding public.vector(3)
 -- other columns
);
-- insert dummy data
INSERT INTO my_table (embedding) VALUES
('[1.0, 2.0, 3.0]'),
('[4.0, 5.0, 6.0]'),
('[7.0, 8.0, 9.0]');
-- create a diskann index by using Cosine distance operator
CREATE INDEX my_table_embedding_diskann_idx ON my_table USING diskann (embedding vector_cosine_ops)
```

## Index options

When creating an index with `diskann`, you can specify various parameters to control its behavior. Here are the options that we currently have:

- `max_neighbors`: Maximum number of edges per node in the graph. (Defaults to 32)
- `l_value_ib`: The size of the search list during index build (Defaults to 50)

```sql
CREATE INDEX my_table_embedding_diskann_custom_idx ON my_table USING diskann (embedding vector_cosine_ops)
WITH (
 max_neighbors = 48,
 l_value_ib = 100
 );
```

The L value for index scanning (`l_value_is`) can be set for the whole connection or per transaction (using `SET LOCAL` within a transaction block):

```sql
SET diskann.l_value_is = 100;
SELECT * FROM my_table ORDER BY embedding <=> '[1,2,3]' LIMIT 5; -- uses 100 candidates
```

Postgres will automatically decide when to use the DiskANN index. If there are scenarios you always want to use the index, use the following command:
```sql
SET LOCAL enable_seqscan TO OFF;
SELECT * FROM my_table ORDER BY embedding <=> '[1,2,3]' LIMIT 5; -- forces the use of index
```

## Indexing progress

With PostgreSQL 12 and newer, you can use `pg_stat_progress_create_index` to check indexing progress.

```sql
SELECT phase, round(100.0 * blocks_done / nullif(blocks_total, 0), 1) AS "%" FROM pg_stat_progress_create_index;
```

Phases for building DiskANN indexes are:
1. `initializing`
1. `loading tuples`

> [!WARNING]
> Users may experience slow index build times in some cases.

### Selecting the index access function

The vector type allows you to perform three types of searches on the stored vectors. You need to select the correct access function for your index so the database can consider your index when executing your queries.

`pg_diskann` supports following distance operators
- `vector_l2_ops`: `<->` Euclidean distance
- `vector_cosine_ops`: `<=>` Cosine distance
- `vector_ip_ops`: `<#>` Inner Product

[Share your suggestions and bugs with the Azure Database for PostgreSQL product team](https://aka.ms/pgfeedback).

## Related content

- [Enable and use pgvector in Azure Database for PostgreSQL - Flexible Server](how-to-use-pgvector.md).
- [Manage PostgreSQL extensions in Azure Database for PostgreSQL - Flexible Server](../extensions/how-to-allow-extensions.md).
