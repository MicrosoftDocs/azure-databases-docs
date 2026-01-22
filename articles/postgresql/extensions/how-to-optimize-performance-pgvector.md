---
title: Optimize performance of vector data on Azure Database for PostgreSQL deployed with pgvector.
description: Best practices to optimize performance pgvector enabled vector database queries and indexes on Azure Database for PostgreSQL.
author: mulander
ms.author: adamwolk
ms.reviewer: maghan
ms.date: 04/27/2024
ms.update-cycle: 180-days
ms.service: azure-database-postgresql
ms.subservice: extensions
ms.topic: how-to
ms.collection: ce-skilling-ai-copilot
ms.custom:
  - build-2023
  - ignite-2023
---

# Optimize performance when using pgvector in Azure Database for PostgreSQL 

The `pgvector` extension adds an open-source vector similarity search to Azure Database for PostgreSQL flexible server.

This article explores the limitations and tradeoffs of [`pgvector`](https://github.com/pgvector/pgvector) and shows how to use partitioning, indexing, and search settings to improve performance.

For more on the extension itself, see [basics of `pgvector`](how-to-use-pgvector.md). You might also want to refer to the official [README](https://github.com/pgvector/pgvector/blob/master/README.md) of the project.

[!INCLUDE [Performance](~/reusable-content/ce-skilling/azure/includes/cosmos-db/postgresql/includes/pgvector-performance.md)]

## Related content

- [Generate vector embeddings with Azure OpenAI on Azure Database for PostgreSQL flexible server](../azure-ai/generative-ai-azure-openai.md).
