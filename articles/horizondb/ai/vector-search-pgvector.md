---
title: Implement Vector Search in Azure HorizonDB Using the Pgvector Extension
description: Implement vector search in Azure HorizonDB using the pgvector extension to enable semantic similarity search over embeddings for AI and retrieval workloads.
#customer intent: As a user, I want to enable the pgvector extension in Azure HorizonDB, so that I can store and query vector embeddings.
author: shreyaaithal
ms.author: shaithal
ms.reviewer: maghan
ms.date: 07/07/2026
ms.service: azure-horizondb
ms.subservice: ai-search
ms.topic: how-to
ms.collection: ce-skilling-ai-copilot
ms.update-cycle: 180-days
---

# Implement vector search with the pgvector extension in Azure HorizonDB (Preview)

[!INCLUDE [Introduction to `pgvector`](~/reusable-content/ce-skilling/azure/includes/cosmos-db/postgresql/includes/pgvector-introduction.md)]

## Enable extension

Before you can enable `pgvector` on your Azure HorizonDB instance, add it to your allow list as described in [how to use PostgreSQL extensions](../extensions/how-to-allow-extensions.md#allow-extensions-in-azure-horizondb-preview). Check if it's correctly added by running `SHOW azure.extensions;`.

> [!IMPORTANT]  
> Although the PostgreSQL community tends to refer to this extension as pgvector, the name of the binary and the extension itself is simply `vector`. Take that name into consideration, because it's the name you must use to allow list it or to create it on any database via the CREATE EXTENSION command.

Then you can install the extension by connecting to your target database and running the [CREATE EXTENSION](https://www.postgresql.org/docs/current/sql-createextension.html) command. You need to repeat the command separately for every database you want the extension to be available in.

```sql
CREATE EXTENSION vector;
```

> [!NOTE]  
> To remove the extension from the currently connected database, use `DROP EXTENSION vector;`.

[!INCLUDE [`pgvector`](~/reusable-content/ce-skilling/azure/includes/cosmos-db/postgresql/includes/pgvector-basics.md)]

## Related content

- [Optimize performance when using pgvector in Azure HorizonDB (Preview)](optimize-pgvector-performance.md)
- [Scalable vector indexing with DiskANN (Preview)](vector-index-diskann.md)
- [Choose the right vector index for your workload in Azure HorizonDB (Preview)](vector-index-selection-guide.md)
