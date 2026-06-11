---
title: Implement Vector Search in Azure HorizonDB Using the Pgvector Extension
description: Implement vector search in Azure HorizonDB using the pgvector extension to enable semantic similarity search over embeddings for AI and retrieval workloads.
author: shreyaaithal
ms.author: shaithal
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-horizondb
ms.subservice: ai-search
ms.topic: how-to
ms.collection:
  - ce-skilling-ai-copilot
ms.update-cycle: 180-days
ms.custom:
  - build-2026
---

# Implement vector search with the pgvector extension for Azure HorizonDB (Preview)

[!INCLUDE [Introduction to `pgvector`](~/reusable-content/ce-skilling/azure/includes/cosmos-db/postgresql/includes/pgvector-introduction.md)]

## Enable extension

Before you can enable `pgvector` on your Azure HorizonDB instance, you need to add it to your allow list as described in [how to use PostgreSQL extensions](../extensions/how-to-allow-extensions.md#allow-extensions-in-azure-horizondb-preview), and check if correctly added by running `SHOW azure.extensions;`.

> [!IMPORTANT]  
> Although all PostgreSQL community tends to refer to this extension as pgvector, the name of the binary and the extension itself is simply `vector`. Take that into consideration, because that is the name you must use to allow list it or to create it on any database via the CREATE EXTENSION command.

Then you can install the extension, by connecting to your target database and running the [CREATE EXTENSION](https://www.postgresql.org/docs/current/sql-createextension.html) command. You need to repeat the command separately for every database you want the extension to be available in.

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
