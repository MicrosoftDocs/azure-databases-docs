---
title: Optimize performance of vector data on Azure Database for PostgreSQL deployed with pgvector.
description: Best practices to optimize performance pgvector enabled vector database queries and indexes on Azure Database for PostgreSQL.
author: mulander
ms.author: adamwolk
ms.reviewer: maghan
ms.date: 04/27/2024
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
ms.collection: ce-skilling-ai-copilot
ms.custom:
  - build-2023
  - ignite-2023
---

# Optimize performance when using pgvector in Azure Database for PostgreSQL - Flexible Server

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

The `pgvector` extension adds an open-source vector similarity search to Azure Database for PostgreSQL flexible server.

This article explores the limitations and tradeoffs of [`pgvector`](https://github.com/pgvector/pgvector) and shows how to use partitioning, indexing, and search settings to improve performance.

For more on the extension itself, see [basics of `pgvector`](how-to-use-pgvector.md). You might also want to refer to the official [README](https://github.com/pgvector/pgvector/blob/master/README.md) of the project.

[!INCLUDE [Performance](~/reusable-content/ce-skilling/azure/includes/cosmos-db/postgresql/includes/pgvector-performance.md)]

[Share your suggestions and bugs with the Azure Database for PostgreSQL product team](https://aka.ms/pgfeedback).

## Related content

- [Generate vector embeddings with Azure OpenAI on Azure Database for PostgreSQL - Flexible Server](generative-ai-azure-openai.md).
