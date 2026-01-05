---
title: Vector search on Azure Database for PostgreSQL
description: Enable semantic similarity search for Retrieval Augmented Generation (RAG) on Azure Database for PostgreSQL with pgvector database extension.
author: AvijitkGupta
ms.author: avijitgupta
ms.reviewer: kabharati, maghan
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

# Enable and use pgvector in Azure Database for PostgreSQL 

[!INCLUDE [Introduction to `pgvector`](~/reusable-content/ce-skilling/azure/includes/cosmos-db/postgresql/includes/pgvector-introduction.md)]

## Enable extension

Before you can enable `pgvector` on your Azure Database for PostgreSQL flexible server instance, you need to add it to your allowlist as described in [how to use PostgreSQL extensions](../extensions/how-to-allow-extensions.md#allow-extensions), and check if correctly added by running `SHOW azure.extensions;`.

> [!IMPORTANT]
> Notice that although all PostgreSQL community tends to refer to this extension as pgvector, the name of the binary and the extension itself is simply `vector`. Take that into consideration, because that is the name you must use to allowlist it or to create it on any database via the CREATE EXTENSION command.

Then you can install the extension, by connecting to your target database and running the [CREATE EXTENSION](https://www.postgresql.org/docs/current/static/sql-createextension.html) command. You need to repeat the command separately for every database you want the extension to be available in.

```sql
CREATE EXTENSION vector;
```

> [!Note]
> To remove the extension from the currently connected database use `DROP EXTENSION vector;`.

[!INCLUDE [`pgvector`](~/reusable-content/ce-skilling/azure/includes/cosmos-db/postgresql/includes/pgvector-basics.md)]

## Related content

- [Optimize performance when using pgvector in Azure Database for PostgreSQL flexible server](how-to-optimize-performance-pgvector.md).
- [Integrate Azure Database for PostgreSQL flexible server with Azure Cognitive Services](../azure-ai/generative-ai-azure-cognitive.md).
- [Generate vector embeddings in Azure Database for PostgreSQL flexible server with locally deployed LLM (Preview)](../azure-ai/generative-ai-overview.md).
- [Integrate Azure Database for PostgreSQL with Azure Machine Learning Services](../azure-ai/generative-ai-azure-machine-learning.md).
- [Generate vector embeddings with Azure OpenAI in Azure Database for PostgreSQL flexible server](../azure-ai/generative-ai-azure-openai.md).
- [Azure AI extension in Azure Database for PostgreSQL flexible server](../azure-ai/generative-ai-azure-overview.md).
- [Generative AI with Azure Database for PostgreSQL flexible server](../azure-ai/generative-ai-overview.md).
- [Recommendation System with Azure Database for PostgreSQL flexible server and Azure OpenAI](../azure-ai/generative-ai-recommendation-system.md).
- [Semantic Search with Azure Database for PostgreSQL flexible server and Azure OpenAI](../azure-ai/generative-ai-semantic-search.md).
- [Enable and use pgvector in Azure Database for PostgreSQL flexible server](how-to-use-pgvector.md).
