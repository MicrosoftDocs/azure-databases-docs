---
title: Scalable vector indexing with DiskANN
description: Use the pg_diskann extension to enable scalable, high-performance vector indexing in Azure HorizonDB for efficient semantic similarity search in large datasets, with advanced filtering for combined vector and metadata queries.
author: abeomor
ms.author: abeomorogbe
ms.reviewer: maghan
ms.date: 05/08/2026
ms.service: azure-database-postgresql
ms.subservice: ai-vector-search
ms.topic: how-to
ms.collection:
  - ce-skilling-ai-copilot
ms.update-cycle: 180-days
ms.custom:
  - build-2026
# customer intent: As a user, I want to learn how to enable and use DiskANN extension in an Azure HorizonDB for efficient semantic similarity search in large datasets.
---

# Scalable vector indexing with DiskANN

DiskANN is Microsoft's scalable approximate nearest neighbor search algorithm for efficient vector search at any scale. It offers high recall, high queries per second, and low query latency, even for billion-point datasets - which is why **DiskANN is the recommended default vector index for production AI workloads on Azure HorizonDB**. It accepts in-place inserts and updates, scales to billions of vectors, supports up to 16,000 dimensions, and is the only vector index in HorizonDB that supports [advanced filtering](#filter-your-search-with-advanced-filtering) for combined vector + metadata queries.

If you're not sure which vector index fits your workload, see [Choose the right vector index for your workload in Azure HorizonDB](vector-index-selection-guide.md).

To learn more about the DiskANN algorithm, see [DiskANN: Vector Search for Web Scale Search and Recommendation](https://www.microsoft.com/research/project/project-akupara-approximate-nearest-neighbor-search-for-large-scale-semantic-search).

The `pg_diskann` extension adds support for using DiskANN for efficient vector indexing and searching.

## Enable pg_diskann

To use the `pg_diskann` extension on your Azure HorizonDB instance, you need to [allow the extension](../extensions/how-to-allow-extensions.md#allow-extensions-in-azure-horizondb) at the instance level. Then you need to [create the extension](../extensions/how-to-create-extensions.md) on each database in which you want to use the functionality provided by the extension.

Because `pg_diskann` has a dependency on the [`vector`](../extensions/concepts-extensions-versions.md#vector) extension, either you [allow](../extensions/how-to-allow-extensions.md#allow-extensions-in-azure-horizondb) and [create](../extensions/how-to-create-extensions.md) the `vector` extension in the same database, and the run the following command:

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
> Setting `enable_seqscan` to off, it discourages the planner from using the query planner's use of sequential scan plan if there are other methods available. Because it's disabled using the `SET LOCAL` command, the setting takes effect for only the current transaction. After a COMMIT or ROLLBACK, the session level setting takes effect again. If the query involves other tables, the setting also discourages the use of sequential scans in all of them.

## Filter your search with advanced filtering

> [!NOTE]  
> Advanced filtering for DiskANN in Azure HorizonDB is in **public preview**.

Most real-world retrieval queries combine vector similarity with structured filters - by tenant, category, date range, price, status, language, or any other metadata column. Advanced filtering on HorizonDB pushes those metadata predicates into the DiskANN index itself, so the index keeps walking the graph until your `LIMIT` is satisfied with rows that pass the `WHERE` clause. The result is low-latency, high-recall vector search even with selective filters over millions of vectors - in a single SQL query, with no application-side post-filtering, no over-fetching, and no separate vector database.

Advanced filtering is what makes DiskANN the right index for agentic applications, recommendation engines, multitenant AI search, and enterprise retrieval. It runs natively inside your HorizonDB instance next to your relational data, so you keep transactional consistency and familiar PostgreSQL SQL. It also composes with the rest of the HorizonDB AI retrieval stack - [Implement vector search in Azure HorizonDB using the pgvector extension](vector-search-pgvector.md), the [AI functions in the azure_ai extension](ai-functions.md), [Full-text search with pg_fts in Azure HorizonDB](full-text-search-pgfts.md), and [hybrid search](hybrid-search.md).

### How it differs from other indexes

| Index | Behavior with `WHERE` clause |
| --- | --- |
| `ivfflat` / `hnsw` | Returns top-K candidates from the ANN search, then filters - with a selective predicate, most candidates are discarded and recall drops. You typically have to over-fetch and re-rank in the application. |
| `diskann` (advanced filtering) | Predicate is evaluated inside the index walk. The index keeps fetching matching candidates until `LIMIT` is satisfied. Recall and latency stay stable as filters get more selective. |

### Use advanced filtering

There's no special syntax. Add metadata columns to your table, create the DiskANN index, and write a normal `SELECT` that combines `WHERE` with the vector ordering operator. The planner uses advanced filtering automatically when a DiskANN index is available.

```sql
-- Add metadata columns alongside the embedding
CREATE TABLE products (
    id          INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    tenant_id   INT NOT NULL,
    category    TEXT NOT NULL,
    price       NUMERIC(10,2) NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    embedding   public.vector(1536)
);

-- Create the DiskANN index on the vector column
CREATE INDEX products_embedding_diskann_idx
    ON products USING diskann (embedding vector_cosine_ops);

-- Vector search filtered by tenant, category, price, and date
SELECT id, category, price
FROM products
WHERE tenant_id = 42
  AND category = 'kitchen'
  AND price BETWEEN 20 AND 200
  AND created_at > now() - INTERVAL '30 days'
ORDER BY embedding <=> :query_embedding
LIMIT 10;
```

> [!TIP]  
> Add a btree index on the columns you filter on most often (for example `tenant_id`, `category`). The planner uses both indexes together for the best plan.

### Recall and `LIMIT`

Advanced filtering tunes itself based on the `LIMIT` clause. With very small `LIMIT` values and a highly selective filter, the index might walk further into the graph to satisfy the limit - increasing latency slightly. If recall is more important than latency, raise `diskann.l_value_is` for the session or transaction. See [Configuration parameters](#configuration-parameters).

### Limitations during preview

- Predicates must reference columns of the same table as the indexed vector. Joins are evaluated after the vector search completes.
- Predicates that the planner can't push into the index (for example, opaque function calls on the filtered column) fallback to post-filtering with the standard recall caveats.
- Index rebuild isn't required when adding metadata columns; the existing DiskANN index continues to work.

## Scale efficiently with spherical quantization (Preview)

DiskANN uses **spherical quantization** to dramatically reduce the memory footprint of vectors. Spherical quantization compresses vectors more effectively than traditional quantization techniques, letting DiskANN keep more data in memory, reducing the need to access slower storage, and using less compute when comparing compressed vectors. **The result is better performance and significant cost savings when working with larger datasets (> 1 million rows).**

> [!IMPORTANT]  
> Spherical quantization in DiskANN is in **public preview**. Available in `pg_diskann` and above.

To reduce the size of your index and fit more data into memory, enable spherical quantization when creating the index:

```sql
CREATE INDEX demo_embedding_diskann_idx ON demo USING diskann(embedding vector_cosine_ops)
WITH (
    spherical_quantized = true
);
```

### Support for high dimension embeddings

Advanced generative AI applications often rely on high-dimensional embedding models such as *text-embedding-3-large* to achieve superior accuracy. Traditional indexing methods like [HNSW in pgvector](https://github.com/pgvector/pgvector?tab=readme-ov-file#hnsw) are limited to vectors with up to 2,000 dimensions, which restricts the use of these powerful models.

DiskANN supports indexing vectors with up to 16,000 dimensions, significantly expanding the scope for high-accuracy AI workloads.

> [!IMPORTANT]  
> Spherical quantization must be enabled to use high-dimensional support.

**Recommended settings:**

- `spherical_quantized`: Set to `true`.

This enhancement enables scalable, efficient search across large vector datasets while maintaining high recall and precision.

## Speed up index build

There are a few ways we recommend improving your index build times.

<a id="using-more-memory"></a>

### Use more memory

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

<a id="using-parallelization"></a>

### Use parallelization

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
> The leader process can't participate in parallel index builds.

If you want to create the index by using parallel workers, you also need to set `max_parallel_workers`, `max_worker_processes`, and `max_parallel_maintenance_workers` parameters accordingly. For more information about these parameters, see [parameters that control resource usages and asynchronous behavior](../server-parameters/concepts-server-parameters.md#resource-usage--asynchronous-behavior).

You can set these parameters at different granularity levels. For example, to set them at session level, you can run the following statements:

```sql
-- Set the parameters
SET max_parallel_workers = 8;
SET max_worker_processes = 8; -- Note: Requires server restart
SET max_parallel_maintenance_workers = 4;
```

To learn about other options to configure these parameters in Azure HorizonDB, see [Parameters in Azure HorizonDB](../server-parameters/concepts-server-parameters.md).

> [!NOTE]  
> The max_worker_processes parameter requires a server restart to take effect.

If the configuration of those parameters and the available resources on the server don't permit launching the parallel workers, PostgreSQL automatically falls back to create the index in the nonparallel mode.

## Configuration parameters

When creating a `diskann` index, you can specify various parameters to control its behavior.

### Index parameters

- `max_neighbors`: Maximum number of edges per node in the graph (Defaults to 32). A higher value can improve the recall up to a certain point.
- `l_value_ib`: Size of the search list during index build (Defaults to 100). A higher value makes the build slower, but the index would be of higher quality.
- `spherical_quantized`: Enables spherical quantization for more efficient search (Defaults to false).

```sql
CREATE INDEX demo_embedding_diskann_custom_idx ON demo USING diskann (embedding vector_cosine_ops)
WITH (
    max_neighbors = 48,
    l_value_ib = 100,
    spherical_quantized = true
);
```

### Extension parameters

- `diskann.iterative_search`: Controls the search behavior.

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

- `diskann.l_value_is`: L value for index scanning (Defaults to 100). Increasing the value improves recall but might slow down queries.

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

| Dataset size (rows) | Parameter type | Name | Recommended value |
| --- | --- | --- | --- |
| <1M | Index build | `l_value_ib` | 100 |
| <1M | Index build | `max_neighbors` | 32 |
| <1M | Query time | `diskann.l_value_is` | 100 |
| | | | |
| 1M-50M | Index build | `l_value_ib` | 100 |
| 1M-50M | Index build | `max_neighbors` | 64 |
| 1M-50M | Index build | `spherical_quantized` | true |
| 1M-50M | Query time | `diskann.l_value_is` | 100 |
| | | | |
| >50M | Index build | `l_value_ib` | 100 |
| >50M | Index build | `max_neighbors` | 96 |
| >50M | Index build | `spherical_quantized` | true |
| >50M | Query time | `diskann.l_value_is` | 100 |

> [!NOTE]  
> These parameters might vary depending on the specific dataset and use case. Users might have to experiment with different parameter values, to find the optimal settings for their particular scenario.

## CREATE INDEX and REINDEX progress

With PostgreSQL 12 and newer, you can use [`pg_stat_progress_create_index`](https://www.postgresql.org/docs/current/progress-reporting.html#CREATE-INDEX-PROGRESS-REPORTING) to check the progress of the CREATE INDEX or REINDEX operations.

```sql
SELECT phase, round(100.0 * blocks_done / nullif(blocks_total, 0), 1) AS "%" FROM pg_stat_progress_create_index;
```

To learn more about the possible phases through which a CREATE INDEX or REINDEX operation goes through, see [CREATE INDEX phases](https://www.postgresql.org/docs/current/progress-reporting.html#CREATE-INDEX-PHASES).

<a id="selecting-the-index-access-function"></a>

### Select the index access function

The vector type allows you to perform three types of searches on the stored vectors. You need to select the correct access function for your index, so that the database can consider your index when executing your queries.

`pg_diskann` supports following distance operators
- `vector_l2_ops`: `<->` Euclidean distance
- `vector_cosine_ops`: `<=>` Cosine distance
- `vector_ip_ops`: `<#>` Inner Product

<a id="troubleshooting"></a>

## Troubleshoot

**Error: `assertion left == right failed left: 40 right: 0`**:
- DiskANN GA version, **v0.6.x introduces breaking changes** in the index metadata format. Indexes created with **v0.5.x aren't forward-compatible** with v0.6.x insert operations. Attempting to insert into a table with an outdated index will result in an error, even if the index appears valid.

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

- [Choose the right vector index for your workload in Azure HorizonDB](vector-index-selection-guide.md)
- [Hybrid search in Azure HorizonDB](hybrid-search.md)
- [Implement vector search in Azure HorizonDB using the pgvector extension](vector-search-pgvector.md)
- [Allow extensions in Azure HorizonDB](../extensions/how-to-allow-extensions.md)
