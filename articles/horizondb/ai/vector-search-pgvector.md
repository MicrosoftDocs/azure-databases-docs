---
title: Implement vector search in Azure HorizonDB using the pgvector extension
description: Implement vector search in Azure HorizonDB using the pgvector extension to enable semantic similarity search over embeddings for AI and retrieval workloads.
author: shreyaaithal
ms.author: shaithal
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-database-postgresql
ms.subservice: ai-vector-search
ms.topic: how-to
ms.collection:
  - ce-skilling-ai-copilot
ms.update-cycle: 180-days
ms.custom:
  - build-2026
---

# Implement vector search in Azure HorizonDB using the pgvector extension

[!INCLUDE [Introduction to `pgvector`](~/reusable-content/ce-skilling/azure/includes/cosmos-db/postgresql/includes/pgvector-introduction.md)]

## Enable extension

Before you can enable `pgvector` on your Azure HorizonDB instance, you need to add it to your allowlist as described in [how to use PostgreSQL extensions](../extensions/how-to-allow-extensions.md#allow-extensions-in-azure-horizondb), and check if correctly added by running `SHOW azure.extensions;`.

> [!IMPORTANT]  
> Although all PostgreSQL community tends to refer to this extension as pgvector, the name of the binary and the extension itself is simply `vector`. Take that into consideration, because that is the name you must use to allowlist it or to create it on any database via the CREATE EXTENSION command.

Then you can install the extension, by connecting to your target database and running the [CREATE EXTENSION](https://www.postgresql.org/docs/current/sql-createextension.html) command. You need to repeat the command separately for every database you want the extension to be available in.

```sql
CREATE EXTENSION vector;
```

> [!NOTE]  
> To remove the extension from the currently connected database use `DROP EXTENSION vector;`.

[!INCLUDE [`pgvector`](~/reusable-content/ce-skilling/azure/includes/cosmos-db/postgresql/includes/pgvector-basics.md)]

## Related content

- [Retrieval foundations: vector, full-text, and hybrid search](ai-search-overview.md)
- [Optimize performance when using pgvector](optimize-pgvector-performance.md)
- [Vector indexing with DiskANN](vector-indexing-diskann.md)
- [Choose the right vector index](vector-index-selection-guide.md)
- [Generate vector embeddings](generate-vector-embeddings.md)
- [Build a semantic search application](build-semantic-search-app.md)
- [Hybrid search](hybrid-search.md)
- [AI functions in the azure_ai extension](ai-functions.md)
- [AI overview for Azure HorizonDB](overview.md)