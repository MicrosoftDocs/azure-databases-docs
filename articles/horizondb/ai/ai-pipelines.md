---
title: Implement durable AI pipelines in Azure HorizonDB
description: Define and run durable AI data pipelines directly in Azure HorizonDB with built-in support for chunking, embeddings, extraction, retrieval, and re-ranking, backed by reliable execution with state, retries, and crash recovery.
author: abeomor
ms.author: abeomorogbe
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-database-postgresql
ms.subservice: ai-vector-search
ms.topic: concept-article
ms.collection:
  - ce-skilling-ai-copilot
ms.update-cycle: 180-days
ms.custom:
  - build-2026
# customer intent: As a user, I want to understand how to implement durable AI pipelines for chunking, embedding, extract and retrieval.
---

# Implement durable AI pipelines in Azure HorizonDB

AI pipelines in Azure HorizonDB let you describe an AI workflow — chunking, embedding, extraction, generation, ranking, human approval — declaratively in SQL, and run it as a fault-tolerant pipeline that lives inside the database. The pipeline definition is just a row in a system catalog. The execution is durable: it survives crashes, retries failed steps, checkpoints incremental work, and resumes long-running jobs from the last completed step.

AI pipelines are built on top of [pg_durable](../development/pg-durable.md). Where `pg_durable` gives you a general durable-execution engine, the `ai.*` pipeline API gives you a higher-level, AI-shaped surface — sources, steps, sinks, and triggers — that compiles down to a durable graph automatically.

> [!NOTE]  
> AI pipelines and the `pg_durable` runtime they depend on are in **public preview**.

## Why pipelines belong in the database

The most common pattern for getting data into a vector store today is a service in the application tier that reads source rows, calls an embedding API, and writes chunks back to Postgres. That pattern works, but it has predictable failure modes:

- The embedding service hits a transient API failure mid-batch, and there's no shared checkpoint between the application and the database that says which rows are done.
- A worker crashes after writing some chunks but before committing the parent row's "processed" flag, leaving the index in an inconsistent state.
- The embedding model changes, and now there's no clean way to re-embed exactly the rows that need it.
- Cost tracking lives in application logs, not next to the data.

AI pipelines move that logic into HorizonDB itself. The source, the steps, the sink, and the run history are all SQL. The database is already where your data lives, where your transactions commit, and where backups and PITR already protect you — so it's the natural place for the embedding pipeline to live too.

## Pipeline anatomy

A pipeline has four parts:

1. **Source** — where rows come from. Today, a `table_source(...)` over a HorizonDB table, optionally with an `incremental_column` (so the pipeline can skip rows it's already processed) and a row `filter`.
2. **Steps** — the AI operations that transform each row, in order. Each step appends columns to the in-flight batch.
3. **Sink** *(optional)* — where the resulting rows are written. If you don't specify one, the pipeline auto-creates `<pipeline_name>_output`.
4. **Trigger** — `'on_change'` (run automatically when source rows change) or `'manual'` (run only when you call `ai.run()`).

### Step types

| Step | Purpose |
|---|---|
| `ai.chunk()` | Split a long text column into overlapping chunks. |
| `ai.embed()` | Generate vector embeddings for a column. |
| `ai.extract()` | Extract structured fields from text using an LLM. |
| `ai.generate()` | Generate text from a prompt template using an LLM. |
| `ai.rank()` | Score or rank documents against a query. |

## Prerequisites

Enable the required extensions:

```sql
CREATE EXTENSION IF NOT EXISTS pg_durable;
CREATE EXTENSION IF NOT EXISTS azure_ai;
CREATE EXTENSION IF NOT EXISTS vector;
```

`pg_durable` must also be in `shared_preload_libraries` and the database restarted. See [Durable execution with pg_durable](../development/pg-durable.md#enable-pg_durable) for the full setup.

You also need an embedding (and optionally a generation) model that `azure_ai` can call. You have two options:

### Option 1: AI Model Management (recommended)

If [AI Model Management](ai-model-management.md) is enabled on your HorizonDB instance, models are provisioned and registered in the model registry automatically — there's no endpoint or key to manage. AI functions use the Managed Models by default:

```sql
-- No endpoint configuration needed; AI Model Management handles it.
-- Uses the default-embedding Managed Model when no model alias is specified.
SELECT azure_openai.create_embeddings(input => 'hello world');
```

### Option 2: Manually register a model in the model registry

If you're not using AI Model Management, deploy your own model through [Microsoft Foundry](/azure/ai-foundry/quickstarts/get-started-code#start-with-a-project-and-model) and register it in the model registry:

```sql
SELECT model_registry.model_add(
    'my-embedding',                          -- a unique alias for your model
    'https://YOUR_RESOURCE.openai.azure.com/', -- your Azure OpenAI endpoint
    'text-embedding-3-small',                -- deployment name
    'text-embedding-3-small',                -- model name
    NULL,                                    -- API version (NULL for latest)
    'subscription-key',                      -- auth type
    'YOUR_API_KEY'                           -- endpoint key
);
```

For complete details on model registration, see [Manual setup with model registry](ai-functions.md#option-2-manual-setup-with-model-registry).

The pipeline examples in this article work the same way under either option.

## Define a pipeline

The smallest useful AI pipeline takes a source table of documents, chunks the body, generates embeddings, and writes the result to an auto-created sink:

```sql
CREATE TABLE documents (
    id          SERIAL PRIMARY KEY,
    title       TEXT NOT NULL,
    content     TEXT NOT NULL,
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

SELECT ai.create_pipeline(
    name   => 'rag_pipeline',
    source => ai.table_source(
        table_name         => 'documents',
        incremental_column => 'updated_at'
    ),
    steps  => ARRAY[
        ai.chunk(input_column => 'content',
                 chunk_size   => 512,
                 overlap      => 64),
        ai.embed(model        => 'my-embedding',
                 input_column => 'chunk_text',
                 dimensions   => 1536)
    ],
    trigger => 'on_change'
);
```

`ai.create_pipeline()` registers the definition. It does not run anything yet. Inspect the compiled execution plan with `ai.explain()`:

```sql
SELECT ai.explain('rag_pipeline');
```

Behind the scenes, `ai.run()` translates the definition into a `pg_durable` graph and submits it via `df.start()`. Each AI step becomes a durable node, so a failure in `ai.embed()` doesn't re-run `ai.chunk()`.

## Run, monitor, and retry

Trigger a run, wait for it, and inspect the output table:

```sql
SELECT ai.run('rag_pipeline');
SELECT ai.wait_for_completion('rag_pipeline', 300);

SELECT doc_id, chunk_index, left(chunk_text, 80) AS preview
FROM rag_pipeline_output
ORDER BY doc_id, chunk_index;
```

Status, history, and the underlying durable instance are queryable from SQL:

```sql
SELECT * FROM ai.status('rag_pipeline');
SELECT * FROM ai.list_pipelines();

-- Drop down to the durable instance for full execution history
SELECT pr.pipeline_name, pr.instance_id, df.status(pr.instance_id) AS df_status
FROM ai.pipeline_runs pr
WHERE pr.pipeline_name = 'rag_pipeline'
ORDER BY pr.started_at DESC
LIMIT 5;
```

Failed steps are retried automatically by the durable engine. The `azure_ai` extension absorbs transient errors from the embedding endpoint internally; persistent failures surface in `ai.status()` and in the `pg_durable` instance history.

To pause and resume change-triggered runs:

```sql
SELECT ai.pause('rag_pipeline');
SELECT ai.resume('rag_pipeline');
```

## Use an explicit sink

Auto-created `<pipeline>_output` tables are convenient for getting started, but most production pipelines want a stable, indexable target table they own:

```sql
CREATE TABLE document_vectors (
    doc_id       INT,
    chunk_index  INT,
    chunk_text   TEXT,
    embedding    vector(1536),
    metadata     JSONB,
    PRIMARY KEY (doc_id, chunk_index)
);

SELECT ai.create_pipeline(
    name   => 'document_ingestion',
    source => ai.table_source('documents', incremental_column => 'updated_at'),
    steps  => ARRAY[
        ai.chunk(input_column => 'content', chunk_size => 768, overlap => 96),
        ai.embed(model => 'my-embedding',
                 input_column => 'chunk_text',
                 dimensions => 1536)
    ],
    sink    => ai.table_sink('document_vectors'),
    trigger => 'on_change'
);
```

Once the sink exists, you can build a [DiskANN vector index](vector-indexing-diskann.md) on `document_vectors.embedding` and use it directly in [hybrid-search](hybrid-search.md) queries.

## Re-embed when the model changes

Embedding models change. Dimensions change. Chunk sizes change. AI pipelines treat that as a first-class operation: you change the pipeline definition (or the sink schema), then call `ai.backfill()` to reprocess every row from scratch:

```sql
-- After dropping and recreating the pipeline with a new model or dimensions:
TRUNCATE document_vectors;
SELECT ai.backfill('document_ingestion');
SELECT ai.wait_for_completion('document_ingestion', 600);
```

The backfill runs as a single durable instance. If the database restarts mid-backfill, it resumes from the last checkpointed batch — you don't restart from row zero.

## Cost controls

Embedding and LLM calls cost money. AI pipelines give you a few practical levers to keep that cost predictable:

- **`incremental_column`** ensures you only embed new or changed rows on subsequent runs.
- **`filter`** on `ai.table_source(...)` lets you scope the pipeline to rows you care about (for example, `status = 'published'`) instead of the whole table.
- **`ai.pause()`** stops the change trigger from launching new runs while you're tuning.
- **`ai.backfill()` is explicit.** Re-embedding everything only happens when you ask for it.

## Compared to one-shot `azure_ai` calls

The `azure_ai` extension can also call models from SQL. The two surfaces solve different problems:

| | One-shot `azure_ai` calls | AI pipelines |
|---|---|---|
| Shape | Single SQL function call (`azure_openai.create_embeddings(...)`) | Declarative pipeline with source, steps, sink |
| Durability | None — fails the calling statement | Durable: retries, resume after crash, checkpoints |
| Best for | Ad-hoc embedding of a few rows; using AI inside a query | Bulk ingestion, ongoing change-driven embedding, multi-step workflows |
| Backfill | Manual `UPDATE ... SET embedding = ...` | `ai.backfill()` |

Use one-shot calls for interactive queries and small jobs. Use a pipeline whenever the work is large enough, long enough, or important enough that you'd otherwise build a service tier for it.

## Limitations during preview

- Sources are HorizonDB tables. To ingest from blob storage or external systems, land the content in a staging table first; the pipeline handles chunking, embedding, checkpointing, and sink writes from there.
- Pipeline definitions are static. Multi-model routing (for example, send "simple" rows to a cheap model and "complex" rows to a stronger one) is expressed as multiple pipelines over the same source with different `filter` clauses.
- Pipelines run on the primary. Read replicas can query `ai.*` views but don't execute pipelines.
- Pipeline state is not portable across major versions of `pg_durable` during preview. Drain or pause running pipelines before upgrading.

## Related content

- [Durable execution with pg_durable](../development/pg-durable.md)
- [Generate vector embeddings in SQL](generate-vector-embeddings.md)
- [Vector indexing with DiskANN](vector-indexing-diskann.md)
- [Hybrid search](hybrid-search.md)
- [Choose a vector index](vector-index-selection-guide.md)
- [AI functions (azure_ai)](ai-functions.md)
