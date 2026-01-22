---
title: Enable and use DiskANN
description: This article describes how to enable DiskANN for improved semantic similarity search for Retrieval Augmented Generation (RAG) on an Azure Database for PostgreSQL flexible server.
author: abeomor
ms.author: abeomorogbe
ms.reviewer: maghan
ms.date: 01/25/2025
ms.service: azure-database-postgresql
ms.subservice: extensions
ms.topic: how-to
ms.custom:
  - build-2025
# customer intent: As a user, I want to learn how to enable and use DiskANN extension in an Azure Database for PostgreSQL.
---

# Enable and use DiskANN extension

DiskANN is a scalable approximate nearest neighbor search algorithm for efficient vector search at any scale. It offers high recall, high queries per second, and low query latency, even for billion-point datasets. Those characteristics make it a powerful tool for handling large volumes of data.

To learn more about DiskANN, see [DiskANN: Vector Search for Web Scale Search and Recommendation](https://www.microsoft.com/research/project/project-akupara-approximate-nearest-neighbor-search-for-large-scale-semantic-search/).

The `pg_diskann` extension adds support for using DiskANN for efficient vector indexing and searching.

## Enable pg_diskann

To use the `pg_diskann` extension on your Azure Database for PostgreSQL flexible server instance, you need to [allow the extension](../extensions/how-to-allow-extensions.md#allow-extensions) at the instance level. Then you need to [create the extension](../extensions/how-to-create-extensions.md) on each database in which you want to use the functionality provided by the extension.

Because `pg_diskann` has a dependency on the [`vector`](../extensions/concepts-extensions-versions.md#vector) extension, either you [allow](../extensions/how-to-allow-extensions.md#allow-extensions) and [create](../extensions/how-to-create-extensions.md) the `vector` extension in the same database, and the run the following command:
 
```sql
CREATE EXTENSION IF NOT EXISTS pg_diskann;
```

Or you can skip explicitly allowing and creating the `vector` extension, and run instead the previous command appending the `CASCADE` clause. That clause PostgreSQL to implicitly run CREATE EXTENSION on the extension that it depends. To do so, run the following command:

```sql
CREATE EXTENSION IF NOT EXISTS pg_diskann CASCADE;
```

To drop the extension from the database to which you're currently connected, run the following command:
 
```sql
DROP EXTENSION IF EXISTS pg_diskann;
```

## Use the diskann index access method

Once the extension is installed, you can create a `diskann` index on a table column that contains vector data. For example, to create an index on the `embedding` column of the `demo` table, use the following command:

```sql
CREATE TABLE demo (
 id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
 embedding public.vector(3)
 -- other columns
);

-- insert dummy data
INSERT INTO demo (embedding) VALUES
('[1.0, 2.0, 3.0]'),
('[4.0, 5.0, 6.0]'),
('[7.0, 8.0, 9.0]');

-- create a diskann index by using Cosine distance operator
CREATE INDEX demo_embedding_diskann_idx ON demo USING diskann (embedding vector_cosine_ops)
```

Once the index is created, you can run queries to find the nearest neighbors.

Following query finds the 5 nearest neighbors to the vector `[2.0, 3.0, 4.0]`:

```sql
SELECT id, embedding
FROM demo
ORDER BY embedding <=> '[2.0, 3.0, 4.0]'
LIMIT 5;
```

Postgres automatically decides when to use the DiskANN index. If it chooses not to use the index in a scenario in which you want it to use it, execute the following command:

```sql
-- Explicit Transcation block to force use for DiskANN index.

BEGIN;
SET LOCAL enable_seqscan TO OFF;
-- Similarity search queries
COMMIT;
```

> [!IMPORTANT]
> Setting `enable_seqscan` to off, it discourages the planner from using the query planner's use of sequential scan plan if there are other methods available. Because it's disable using the `SET LOCAL` command, the setting takes effect for only the current transaction. After a COMMIT or ROLLBACK, the session level setting takes effect again. Notice that if the query involves other tables, the setting also discourages the use of sequential scans in all of them.

## Scale efficiently with Quantization (Preview)

DiskANN uses product quantization (PQ) to dramatically reduce the memory footprint of the vectors. Unlike other quantization techniques, the PQ algorithm can compress vectors more effectively, significantly improving performance.  DiskANN using PQ can keep more data in memory, reducing the need to access slower storage, as well as using less compute when comparing compressed vectors. **This results in better performance and significant cost savings when working with larger amounts of data (> 1 million rows)**. 

> [!IMPORTANT]
> Product quantization support in DiskANN is available starting from **pg_diskann v0.6 and above**.

To reduce the size of your index and fit more data into memory, you can utilize PQ:
```sql
CREATE INDEX demo_embedding_diskann_idx ON demo USING diskann(embedding vector_cosine_ops) 
WITH(
    product_quantized=true
    );    
```

### Improve accuracy when using PQ with vector reranking
Reranking with full vectors is a technique used in approximate nearest neighbor (ANN) search systems like DiskANN with Product Quantization (PQ) to improve result accuracy by reordering the top-N retrieved candidates using the original, uncompressed (full-precision) vectors. This reranking technique is based purely on exact vector similarity metrics (e.g., cosine similarity or Euclidean distance). This technique is **not** the same as [reranking using a ranking model](https://techcommunity.microsoft.com/blog/adforpostgresql/introducing-the-semantic-ranking-solution-for-azure-database-for-postgresql/4298781).

To balance speed and precision in vector similarity search, a two-step reranking strategy can be implemented when querying with DiskANN and product quantization to improve accuracy.

1. **Initial Approximate Search**: The inner query uses DiskANN to retrieve the top 50 approximate nearest neighbors based on cosine distance between the stored embeddings and the query vector. This step is fast and efficient, leveraging DiskANN’s indexing capabilities.

2. **Precise Reranking**: The outer query reorders those 50 results by their actual computed distance and returns the top 10 most relevant matches:

Here is an example of reranking using this 2 step approach:
```sql
SELECT id
FROM (
    SELECT id, embedding <=> %s::vector AS distance
    FROM demo
    ORDER BY embedding <=> %s::vector asc
    LIMIT 50
) AS t
ORDER BY t.distance
LIMIT 10;
```
> [!NOTE]
> **%s** should be replace by the query vector. You can use [azure_ai](../azure-ai/generative-ai-azure-openai.md) to create a query vector directly in Postgres.

This approach balances speed (via approximate search) and accuracy (via full vector reranking), ensuring high-quality results without scanning the entire dataset. 

### Support for high dimension embeddings
Advanced Generative AI applications often rely on high-dimensional embedding models such as *text-embedding-3-large* to achieve superior accuracy. However, traditional indexing methods like [HNSW in pgvector](https://github.com/pgvector/pgvector?tab=readme-ov-file#hnsw) are limited to vectors with up to 2,000 dimensions, which restricts the use of these powerful models.

Starting in pg_diskann v0.6 and above, DiskANN now supports indexing vectors with up to 16,000 dimensions, significantly expanding the scope for high-accuracy AI workloads.

> [!IMPORTANT]
> Product Quantization must be turned on to leverage high-dimensional support.

**Recommended settings:**
- `product_quantized`: Set to true
- `pq_param_num_chunks`: Set to one-third of the embedding dimension for optimal performance.
- `pq_param_training_samples`: Automatically determined based on table size unless explicitly set.

This enhancement enables scalable, efficient search across large vector datasets while maintaining high recall and precision.

## Speed up index build
There are a few ways we recommend to improve your index build times.

### Using more memory
To speed up the creation of the index, you can increase the memory allocated on your Postgres instance for the index build. The memory usage can be specified through the [`maintenance_work_mem`](https://www.postgresql.org/docs/current/runtime-config-resource.html#GUC-MAINTENANCE-WORK-MEM) parameter. 

```sql
-- Set the parameters
SET maintenance_work_mem = '8GB'; -- Depending on your resources
```

Then, `CREATE INDEX` command uses the specified work memory, depending on the available resources, to build the index.

```sql
CREATE INDEX demo_embedding_diskann_idx ON demo USING diskann (embedding vector_cosine_ops)
```

> [!TIP] 
> You can scale up your memory resources during index build to improve indexing speed, then scale back down when indexing is complete.

### Using parallelization
To speed up the creation of the index, you can use parallel workers. The number of workers can be specified through the `parallel_workers` storage parameter of the [`CREATE TABLE`](https://www.postgresql.org/docs/current/sql-createtable.html#RELOPTION-PARALLEL-WORKERS) statement, when creating the table. And it can be adjusted later using the `SET` clause of the [`ALTER TABLE`](https://www.postgresql.org/docs/current/sql-altertable.html#SQL-ALTERTABLE-DESC-SET-STORAGE-PARAMETER) statement.

```sql
CREATE TABLE demo (
	id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	embedding public.vector(3)
) WITH (parallel_workers = 4);
ALTER TABLE demo SET (parallel_workers = 8);
```

Then, `CREATE INDEX` command uses the specified number of parallel workers, depending on the available resources, to build the index.

```sql
CREATE INDEX demo_embedding_diskann_idx ON demo USING diskann (embedding vector_cosine_ops)
```

> [!IMPORTANT]
> The leader process cannot participate in parallel index builds.

If you want to create the index by using parallel workers, you also need to set `max_parallel_workers`, `max_worker_processes`, and `max_parallel_maintenance_workers` parameters accordingly. For more information about these parameters, see [parameters that control resource usages and asynchronous behavior](../server-parameters/concepts-server-parameters.md#resource-usage--asynchronous-behavior).


You can set these parameters at different granularity levels. For example, to set them at session level, you can run the following statements:

```sql
-- Set the parameters
SET max_parallel_workers = 8;
SET max_worker_processes = 8; -- Note: Requires server restart
SET max_parallel_maintenance_workers = 4;
```

To learn about other options to configure these parameters in Azure Database for PostgreSQL flexible server, see [Configure server parameters](../server-parameters/how-to-server-parameters-list-all.md).

> [!NOTE] 
> The max_worker_processes parameter requires a server restart to take effect.

If the configuration of those parameters and the available resources on the server don't permit launching the parallel workers, PostgreSQL automatically falls back to create the index in the nonparallel mode.

## Configuration parameters

When creating a `diskann` index, you can specify various parameters to control its behavior. 

### Index parameters

- `max_neighbors`: Maximum number of edges per node in the graph (Defaults to 32). A higher value can improve the recall up to a certain point.
- `l_value_ib`: Size of the search list during index build (Defaults to 100). A higher value makes the build slower, but the index would be of higher quality.
- `product_quantized`: Enables product quantization for more efficient search (Defaults to false).
- `pq_param_num_chunks`: Number of chunks for product quantization (Defaults to 0). 0 means it is determined automatically, based on embedding dimensions. It is recommended to use 1/3 of the original embedding dimensions.
- `pq_param_training_samples`: Number of vectors to train the PQ pivot table on (Defaults to 0). 0 means it is determined automatically, based on table size.

```sql
CREATE INDEX demo_embedding_diskann_custom_idx ON demo USING diskann (embedding vector_cosine_ops)
WITH (
 max_neighbors = 48,
 l_value_ib = 100,
 product_quantized=true, 
 pq_param_num_chunks = 0,
 pq_param_training_samples = 0
 );
```

### Extension parameters

* `diskann.iterative_search`: Controls the search behavior.

    Configurations for `diskann.iterative_search`:

    - `relaxed_order` (default): Lets diskann iteratively search the graph in batches of `diskann.l_value_is`, until the desired number of tuples, possibly limited by `LIMIT` clause, are yielded. Might cause the results to be out of order. 

    - `strict_order`: Similar to `relaxed_order`, lets diskann iteratively search the graph, until the desired number of tuples are yielded. However, it ensures that the results are returned in strict order sorted by distance. 

    - `off`: Uses noniterative search functionality, which means that it attempts to fetch `diskann.l_value_is` tuples in one step. Noniterative search can only return a maximum of `diskann.l_value_is` vectors for a query, regardless of the `LIMIT` clause or the number of tuples that match the query.

    To change the search behavior to` strict_order`, for all queries executed in the current session, run the following statement:

    ```sql
    SET diskann.iterative_search TO 'strict_order';
    ```

    To change it so that it only affects all queries executed in the current transaction, run the following statement:

    ```sql
    BEGIN;
    SET LOCAL diskann.iterative_search TO 'strict_order';
    -- All your queries
    COMMIT;
    ```


* `diskann.l_value_is`: L value for index scanning (Defaults to 100). Increasing the value improves recall but might slow down queries.

    To change the L value for index scanning to 20, for all queries executed in the current session, run the following statement:

    ```sql
    SET diskann.l_value_is TO 20;
    ```

    To change it so that it only affects all queries executed in the current transaction, run the following statement:

    ```sql
    BEGIN;
    SET LOCAL diskann.l_value_is TO 20;
    -- All your queries
    COMMIT;
    ```

### Recommended configuration of parameters

| Dataset size (rows)| Parameter type | Name | Recommended value |
| --- | --- | --- | --- |
| <1M | Index build | `l_value_ib` | 100 |
| <1M | Index build | `max_neighbors` | 32 |
| <1M | Query time | `diskann.l_value_is` | 100 |
|  | | | |
| 1M-50M | Index build | `l_value_ib` | 100 |
| 1M-50M | Index build | `max_neighbors` | 64 |
| 1M-50M | Index build | `product_quantized` | true |
| 1M-50M | Query time | `diskann.l_value_is` | 100 |
|  | | | |
| >50M | Index build | `l_value_ib` | 100 |
| >50M | Index build | `max_neighbors` | 96 |
| >50M | Index build | `product_quantized` | true |
| >50M | Query time | `diskann.l_value_is` | 100 |

> [!NOTE]
> These parameters might vary depending on the specific dataset and use case. Users might have to experiment with different parameter values, to find the optimal settings for their particular scenario.

## CREATE INDEX and REINDEX progress

With PostgreSQL 12 and newer, you can use [`pg_stat_progress_create_index`](https://www.postgresql.org/docs/current/progress-reporting.html#CREATE-INDEX-PROGRESS-REPORTING) to check the progress of the CREATE INDEX or REINDEX operations.

```sql
SELECT phase, round(100.0 * blocks_done / nullif(blocks_total, 0), 1) AS "%" FROM pg_stat_progress_create_index;
```

To learn more about the possible phases through which a CREATE INDEX or REINDEX operation goes through, see [CREATE INDEX phases](https://www.postgresql.org/docs/current/progress-reporting.html#CREATE-INDEX-PHASES). 

### Selecting the index access function

The vector type allows you to perform three types of searches on the stored vectors. You need to select the correct access function for your index, so that the database can consider your index when executing your queries.

`pg_diskann` supports following distance operators
- `vector_l2_ops`: `<->` Euclidean distance
- `vector_cosine_ops`: `<=>` Cosine distance
- `vector_ip_ops`: `<#>` Inner Product

## Troubleshooting

**Error: `assertion left == right failed left: 40 right: 0`**:
- DiskANN GA version, **v0.6.x introduces breaking changes** in the index metadata format. Indexes created with **v0.5.x are not forward-compatible** with v0.6.x insert operations. Attempting to insert into a table with an outdated index will result in an error, even if the index appears valid.

- When you encounter this error, **you can resolve by:**
    - **Option 1:** Executing `REINDEX` or `REDINDEX CONCURRENTLY` statement on the index. 
    - **Option 2:** Rebuild the Index

        ```sql
        DROP INDEX your_index_name;
        CREATE INDEX your_index_name ON your_table USING diskann(your_vector_column vector_cosine_ops);

        ```

**Error: `diskann index needs to be upgraded to version 2...`**:

- When you encounter this error, you can resolve by:
    - **Option 1:** Executing `REINDEX` or `REDINDEX CONCURRENTLY` statement on the index. 
    - **Option 2:** Because `REINDEX` might take a long time, the extension also provides a user-defined function called `upgrade_diskann_index()`, which upgrades your index faster, when possible.

        To upgrade your index, run the following statement:

        ```sql
        SELECT upgrade_diskann_index('demo_embedding_diskann_custom_idx');
        ```

        To upgrade all diskann indexes in the database to the current version, run the following statement:

        ```sql
        SELECT upgrade_diskann_index(pg_class.oid)
        FROM pg_class
        JOIN pg_am ON (pg_class.relam = pg_am.oid)
        WHERE pg_am.amname = 'diskann';
        ```

## Related content

- [Enable and use pgvector in Azure Database for PostgreSQL flexible server](how-to-use-pgvector.md).
- [Manage PostgreSQL extensions](../extensions/how-to-allow-extensions.md).
