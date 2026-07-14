---
title: Optimize Performance when Using pgvector in Azure Database for PostgreSQL Flexible Server
description: Best practices to optimize performance pgvector enabled vector database queries and indexes in Azure Database for PostgreSQL flexible server.
#customer intent: As a user, I want to optimize `pgvector` query performance in Azure Database for PostgreSQL flexible server, so that my vector similarity searches return results faster.
author: mulander
ms.author: adamwolk
ms.reviewer: maghan
ms.date: 07/10/2026
ms.update-cycle: 180-days
ms.service: azure-database-postgresql
ms.subservice: extensions
ms.topic: how-to
ms.collection: ce-skilling-ai-copilot
---

# Optimize performance when using pgvector in Azure Database for PostgreSQL flexible server

The `pgvector` extension adds an open-source vector similarity search to Azure Database for PostgreSQL flexible server.

This article explores the limitations and tradeoffs of [`pgvector`](https://github.com/pgvector/pgvector) and shows how to use partitioning, indexing, and search settings to improve performance.

For more on the extension itself, see [basics of `pgvector`](how-to-use-pgvector.md). You might also want to refer to the official [README](https://github.com/pgvector/pgvector/blob/master/README.md) of the project.

[!INCLUDE [Performance](~/reusable-content/ce-skilling/azure/includes/cosmos-db/postgresql/includes/pgvector-performance.md)]

## Related content

- [Generate vector embeddings with Azure OpenAI on Azure Database for PostgreSQL flexible server](../azure-ai/generative-ai-azure-openai.md).
