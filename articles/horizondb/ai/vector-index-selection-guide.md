---
title: Choose the right vector index for your workload in Azure HorizonDB
description: Compare flat, IVFFlat, HNSW, and DiskANN vector indexes in Azure HorizonDB and choose the right one based on dataset size, recall target, update rate, and filter selectivity.
author: abeomor
ms.author: abeomorogbe
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-database-postgresql
ms.subservice: ai-vector-search
ms.topic: concept-article
ms.collection: ce-skilling-ai-copilot
ms.update-cycle: 180-days
ms.custom: build-2026
# customer intent: As a developer choosing a vector index, I want to compare flat, IVFFlat, HNSW, and DiskANN so that I can pick the index that meets my recall, latency, and cost targets.
---

# Choose the right vector index for your workload in Azure HorizonDB

Azure HorizonDB supports four ways to run vector similarity search: an exact (flat) scan and three approximate nearest-neighbor (ANN) indexes - IVFFlat, HNSW, and DiskANN. The right choice depends on how many vectors you have, how often they change, what recall you need, how much memory you can spend, and how often you filter by metadata.

For most production AI workloads on HorizonDB, **DiskANN is the recommended default**. It's Microsoft's high-performance vector index, scales from thousands to billions of vectors, supports up to 16,000 dimensions, accepts inserts and updates in place, and is the only option in HorizonDB that supports [advanced filtering](#advanced-filtering-and-diskann) - combining vector similarity with metadata predicates without losing recall or latency. The other index types remain useful for specific cases (small or static datasets, in-memory-only workloads), which this guide covers.

This article gives you a single decision point so you don't have to read four extension docs to answer "which index should I use?". For step-by-step usage, follow the links at the end of each section.

## How the four options differ

All four options return the nearest neighbors of a query vector. They differ in **how** they search:

- **Flat (no index)** - Compares the query vector against every row. Always 100% recall. Cost grows linearly with row count.
- **IVFFlat** - Partitions the vector space into lists during a one-time training pass, then searches only the closest lists at query time. Fast to build, smaller index, lower recall than graph indexes for the same speed.
- **HNSW** - Builds a multi-layer graph of vectors. High recall and low latency on in-memory datasets, but the index must fit in RAM for good performance and pgvector caps it at 2,000 dimensions.
- **DiskANN** - Microsoft's graph-based vector index, designed to stay fast when most of the data is on SSD instead of RAM. Scales to billions of vectors, supports up to 16,000 dimensions, accepts in-place updates, and is the only option in HorizonDB that supports advanced filtering. The recommended default for production AI workloads on HorizonDB.

All four are exposed through the `vector` (pgvector) extension; DiskANN additionally requires the `pg_diskann` extension.

## At-a-glance comparison

| Property | Flat | IVFFlat | HNSW | DiskANN |
| --- | --- | --- | --- | --- |
| Algorithm | Exact scan | Inverted file (partitioned) | Hierarchical graph | SSD-optimized graph |
| Recall | 100% | Low-medium | High | High |
| Query latency on 10M+ rows | High | Medium | Low (if in RAM) | Low |
| Build time | None | Fast | Slow | Medium |
| Memory footprint | None (sequential I/O) | Small | Large - index must fit in RAM | Small - most data stays on SSD |
| Update / insert cost | None | Recall degrades; periodic rebuild needed | Per-insert cost; in place | Per-insert cost; in place |
| Max dimensions | 16,000 (vector type) | 2,000 | 2,000 | 16,000 |
| Filtered query behavior | Always correct | Post-filter - recall drops with selective filters | Post-filter - recall drops with selective filters | Advanced filtering on HorizonDB - metadata predicates pushed into the index |
| Best for | < 100K rows or correctness checks | Static datasets, modest recall needs | Medium datasets that fit in RAM | Large or growing datasets, high dimensions, filtered queries |

## Decision tree

Start at the top and stop at the first match.

1. **Fewer than 100,000 vectors and latency isn't critical?** Use a flat (no index) scan. You get exact results with no tuning.
1. **More than 16,000 dimensions, or need to combine vector similarity with metadata filters at high recall?** Use **DiskANN**. It's the only option that supports both, through advanced filtering on HorizonDB.
1. **Dataset will exceed RAM, or rows added continuously, or expected to grow past ~10M?** Use **DiskANN**. It's designed to stay fast when most vectors live on SSD.
1. **Dataset is mostly static, fits comfortably in RAM, and recall must be high?** Use **HNSW**.
1. **Dataset is mostly static, fits in RAM, and you can tolerate lower recall in exchange for very fast builds?** Use **IVFFlat**.
1. **Anything else?** Default to **DiskANN**. It's the recommended index for new HorizonDB workloads at scale.

<a id="sizing-examples"></a>

## Size examples

These examples illustrate the tradeoffs. Always benchmark with your own data, queries, and recall target.

### One million vectors, 1,536 dimensions, mostly read-only

Either HNSW or DiskANN works. Pick HNSW if the index fits comfortably in RAM and the dataset is stable; pick DiskANN if you expect the dataset to keep growing or you plan to run filtered queries.

### Ten million vectors, 1,536 dimensions, daily inserts

Use **DiskANN** with `max_neighbors = 64`. Periodic large rebuilds aren't needed; updates are applied in place. See [Recommended configuration of parameters](vector-indexing-diskann.md#recommended-configuration-of-parameters).

### 100 million+ vectors, high-dimensional embeddings (3,072+)

Use **DiskANN**. HNSW and IVFFlat aren't viable at this dimensionality. See [Scalable vector indexing with DiskANN](vector-indexing-diskann.md) for the exact parameters.

### Up to 100,000 vectors used as a correctness baseline

Use a flat scan. It's the fastest way to validate that an ANN index is returning the right neighbors before you commit to one.

## Advanced filtering and DiskANN

Most production retrieval queries combine vector similarity with structured `WHERE` clauses - by tenant, category, date range, price, status, or any other metadata column. The index you pick determines whether those filtered queries stay fast and accurate.

- IVFFlat and HNSW apply predicates **after** the ANN search returns candidates. With a selective filter, most candidates are thrown away and recall collapses, often forcing you to over-fetch and rerank in the application.
- **DiskANN supports advanced filtering on HorizonDB** (public preview), which pushes metadata predicates into the index itself. The index keeps walking the graph until your `LIMIT` is satisfied with rows that pass the filter - so you get low-latency, high-recall results in a single SQL query, even with selective predicates over millions of vectors.

Advanced filtering is what makes DiskANN the right index for agentic applications, recommendation engines, multitenant AI search, and any retrieval workload where filtering is part of the query. It runs natively inside HorizonDB next to your relational data, so you keep transactional consistency, familiar PostgreSQL SQL, and a single store - no separate vector database or external search service. It works with `pgvector`, the Azure AI integrations, BM25 full-text search, and the rest of the HorizonDB AI retrieval stack.

If filtered queries are part of your workload, choose DiskANN. See [Filter your search with DiskANN](vector-indexing-diskann.md) for query examples and the index parameters that control this behavior.

## Update and rebuild cost

- **IVFFlat** - Trained on a sample of the data. Recall degrades as new rows are inserted because the partitions become unbalanced. Rebuild periodically.
- **HNSW** - Inserts are applied to the graph in place. No rebuild required, but inserts are more expensive than IVFFlat.
- **DiskANN** - Inserts are applied in place. The index also supports parallel builds and `REINDEX CONCURRENTLY` for one-shot rebuilds.

For large initial loads, build the index after the bulk insert and use `maintenance_work_mem` plus parallel workers to speed up build time. See [Speed up index build](vector-indexing-diskann.md#speed-up-index-build).

## Migrate between index types

You can change index types without changing your application. The query SQL stays the same - only the `CREATE INDEX` statement changes.

```sql
-- Drop the old index
DROP INDEX IF EXISTS demo_embedding_idx;

-- Build the new one (DiskANN shown)
CREATE INDEX demo_embedding_idx
ON demo USING diskann (embedding vector_cosine_ops);
```

To avoid a service window, use `CREATE INDEX CONCURRENTLY` to build the new index, then drop the old one.

## Distance operators

All four options support the same distance operators from pgvector. Choose the operator that matches your embedding model:

- `<->` - Euclidean (L2) distance - `vector_l2_ops`
- `<=>` - Cosine distance - `vector_cosine_ops`
- `<#>` - Negative inner product - `vector_ip_ops`

The operator must match the index access method's operator class. Cosine distance is the default for most embedding models, including Azure OpenAI's `text-embedding-3-*` family.

## Related content

- [Implement vector search using the pgvector extension](vector-search-pgvector.md)
- [Scalable vector indexing with DiskANN](vector-indexing-diskann.md)
- [Optimize performance when using pgvector](optimize-pgvector-performance.md)
