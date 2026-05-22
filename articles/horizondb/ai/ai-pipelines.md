---
title: Implement AI Pipelines in Azure HorizonDB
description: Define and run AI data pipelines directly in Azure HorizonDB with built-in support for chunking, embeddings, extraction, retrieval, and reranking, backed by reliable execution with state, retries, and crash recovery.
author: abeomor
ms.author: abeomorogbe
ms.reviewer: maghan
ms.date: 06/02/2026
ai-usage: ai-assisted
ms.service: azure-database-postgresql
ms.subservice: ai-vector-search
ms.topic: concept-article
ms.collection:
  - ce-skilling-ai-copilot
ms.update-cycle: 180-days
ms.custom:
  - build-2026
# customer intent: As a user, I want to understand how to implement durable AI pipelines for chunking, embedding, extraction, and retrieval.
---

# Implement durable AI pipelines in Azure HorizonDB (Preview)

AI pipelines in Azure HorizonDB let you describe an AI workflow (chunking, embedding, extraction, generation, ranking, human approval) declaratively in SQL, and run it as a fault-tolerant pipeline that lives inside the database. The pipeline definition is just a row in a system catalog. The execution is durable: it survives crashes, retries failed steps, checkpoints incremental work, and resumes long-running jobs from the last completed step.

AI pipelines are part of the `azure_ai` extension. The `ai.*` functions and views used throughout this article are provided by `azure_ai` and built on top of [pg_durable](../development/durable-functions.md). Where `pg_durable` gives you a general durable-execution engine, the `ai.*` pipeline API gives you a higher-level, AI-shaped surface - sources, steps, sinks, and triggers - that compiles down to a durable graph automatically.

> [!NOTE]  
> AI pipelines is in **public preview**.

## Why pipelines belong in the database

The most common pattern for getting data into a vector store today is a service in the application tier that reads source rows, calls an embedding API, and writes chunks back to Postgres. That pattern works, but it has predictable failure modes:

- The embedding service hits a transient API failure mid-batch, and there's no shared checkpoint between the application and the database that says which rows are done.
- A worker crashes after writing some chunks but before committing the parent row's "processed" flag, leaving the index in an inconsistent state.
- The embedding model changes, and now there's no clean way to re-embed exactly the rows that need it.

AI pipelines move that logic into HorizonDB itself. The source, the steps, the sink, and the run history are all SQL. The database is already where your data lives, where your transactions commit, and where backups and PITR already protect you - so it's the natural place for the embedding pipeline to live too.

## Pipeline anatomy

A pipeline has four parts:

1. **Source** - where rows come from. Today, a `table_source(...)` over a HorizonDB table, optionally with an `incremental_column` (so the pipeline can skip rows it's already processed).
1. **Steps** - the AI operations that transform each row, in order. Each step appends columns to the in-flight batch.
1. **Sink** *(optional)* - where the resulting rows are written.
1. **Trigger** - `'on_change'` (run automatically when source rows change) or `'manual'` (run only when you call `ai.run()`).

### Step types

| Step | Purpose |
| --- | --- |
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

You also need an embedding (and optionally a generation) model that `azure_ai` can call. You have two options:

### Option 1: AI Model Management (recommended)

If [AI Model Management in Azure HorizonDB (Preview)](ai-model-management.md) is enabled on your HorizonDB instance, models are provisioned and registered in the model registry automatically. There's no endpoint or key to manage. AI functions use the Managed Models by default:

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

The smallest useful AI pipeline takes a source table of documents, chunks the body, generates embeddings, and writes the result to a sink table:

> [!IMPORTANT]  
> The output sink table needs to be defined with the following five columns: `doc_id`, `chunk_index`, `chunk_text`, `embedding`, `metadata`.

```sql
-- You need to define the output sink table with the right columns
CREATE TABLE rag_pipeline_output (
    doc_id      INT,
    chunk_index INT,
    chunk_text  TEXT,
    embedding   vector(1536),
    metadata    JSONB
);

CREATE TABLE documents (
    id          SERIAL PRIMARY KEY,
    title       TEXT NOT NULL,
    content     TEXT NOT NULL,
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

SELECT ai.create_pipeline(
    name   => 'rag_pipeline',
    source => ai.table_source(
        table_name         => 'documents'
    ),
    steps  => ARRAY[
        ai.chunk(input => 'content',
                 chunk_size   => 512, --Optional, default = 512
                 overlap      => 64   --Optional, default = 64
                 ),
        ai.embed(model        => 'default-embedding',
                 input => 'chunk_text', -- This column is from the output for the chunk step.
                 dimensions   => 1536)
    ],
    trigger => 'on_change',
    sink   => ai.table_sink('rag_pipeline_output')
);
```

`ai.create_pipeline()` registers the definition. It doesn't run anything yet. Inspect the compiled execution plan with `ai.explain()`:

```sql
SELECT ai.explain('rag_pipeline');
```

Behind the scenes, `ai.run()` translates the definition into a `pg_durable` graph and submits it via [Durable functions with pg_durable in Azure HorizonDB (Preview)](../development/durable-functions.md). Each AI step becomes a durable node, so a failure in `ai.embed()` doesn't re-run `ai.chunk()`.

> [!TIP]  
> Once the sink table is populated, you can build a [Scalable vector indexing with DiskANN (Preview)](vector-indexing-diskann.md) on the `embedding` column and use it directly in [hybrid-search](hybrid-search.md) queries.

## Run, monitor, and retry

Trigger a run and wait for it:

```sql
SELECT ai.run('rag_pipeline');
```

Inspect the output table.

```sql
SELECT doc_id, chunk_index, left(chunk_text, 80) AS preview
FROM rag_pipeline_output
ORDER BY doc_id, chunk_index;
```

Status, history, and the underlying durable instance are queryable from SQL:

```sql
SELECT * FROM ai.status('rag_pipeline');
SELECT * FROM ai.list_pipelines();

-- Drop down to the durable function instance for full execution history, to check if your run is pending, completed, or failed
SELECT di.id AS instance_id, di.label, di.status AS df_status, di.created_at
FROM df.instances di
WHERE di.label = 'ai-pipeline:rag_pipeline'
ORDER BY di.created_at DESC
LIMIT 5;
```

Failed steps are retried automatically by the durable engine. The `azure_ai` extension absorbs transient errors from the embedding endpoint internally; persistent failures surface in `ai.status()` and in the `pg_durable` instance history.

To pause and resume change-triggered runs:

```sql
SELECT ai.pause('rag_pipeline');
SELECT ai.resume('rag_pipeline');
```

## Re-embed when the model changes

Embedding models change. Dimensions change. Chunk sizes change. AI pipelines treat that as a first-class operation: you change the pipeline definition (or the sink schema), then call `ai.backfill()` to reprocess every row from scratch:

```sql
-- After dropping and recreating the pipeline with a new model or dimensions:
TRUNCATE rag_pipeline_output;
SELECT ai.backfill('rag_pipeline');
```

The backfill runs as a single durable instance. If the database restarts mid-backfill, it resumes from the last checkpointed batch. You don't restart from row zero.

## Cost controls

Embedding and LLM calls cost money. AI pipelines give you a few practical levers to keep that cost predictable:

- `incremental_column` ensures you only embed new or changed rows on subsequent runs.
- `ai.pause()` stops the change trigger from launching new runs while you're tuning.
- **`ai.backfill()` is explicit.** Re-embedding everything only happens when you ask for it.

## Compared to one-shot `azure_ai` calls

The `azure_ai` extension can also call models from SQL. The two surfaces solve different problems:

| Concepts | One-shot `azure_ai` calls | AI pipelines |
| --- | --- | --- |
| Shape | Single SQL function call (`azure_openai.create_embeddings(...)`) | Declarative pipeline with source, steps, sink |
| Durability | None. Fails the calling statement | Durable: retries, resume after crash, checkpoints |
| Best for | Ad hoc embedding of a few rows; using AI inside a query | Bulk ingestion, ongoing change-driven embedding, multi-step workflows |
| Backfill | Manual `UPDATE ... SET embedding = ...` | `ai.backfill()` |

Use one-shot calls for interactive queries and small jobs. Use a pipeline whenever the work is large enough, long enough, or important enough that you'd otherwise build a service tier for it.

## Limitations during preview

- Sources are HorizonDB tables. To ingest from blob storage or external systems, land the content in a staging table first; the pipeline handles chunking, embedding, checkpointing, and sink writes from there.
- Pipelines run on the primary. Read replicas can query `ai.*` views but don't execute pipelines.
- Pipeline state isn't portable across major versions of `pg_durable` during preview. Drain or pause running pipelines before upgrading.

## Related content

- [Durable functions with pg_durable in Azure HorizonDB (Preview)](../development/durable-functions.md)
- [Generate vector embeddings using the create_embeddings() AI function (Preview)](generate-vector-embeddings.md)
- [AI functions in the azure_ai extension for Azure HorizonDB (Preview)](ai-functions.md)
