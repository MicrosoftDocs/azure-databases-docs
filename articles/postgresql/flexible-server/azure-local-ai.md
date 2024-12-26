---
title: Create in-database embeddings with azure_local_ai extension
description: Enable RAG patterns with in-database embeddings and vectors on Azure Database for PostgreSQL - Flexible Server.
author: jojohnso-msft
ms.author: jojohnso
ms.reviewer: maghan
ms.date: 12/08/2024
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: overview
ms.custom:
  - build-2024
# customer intent: As a user, I want to understand the overview and use cases of the azure_local_ai extension for Azure Database for PostgreSQL - Flexible Server.
---

# Azure Local AI extension for Azure Database for PostgreSQL - Flexible Server (Preview)

The `azure_local_ai` extension for Azure Database for PostgreSQL flexible server allows you to use registered, pretrained, open-source models deployed locally to your Azure Database for PostgreSQL server. These models can be used to create text embeddings that can provide context to your Retrieval Augmented Generation (RAG) pattern as you build rich generative AI applications. The `azure_local_ai` extension enables the database to call locally deployed models to create vector embeddings from text data, simplifying the development process and reducing latency by removing the need to make more remote API calls to AI embedding models hosted outside of the PostgreSQL boundary. In this release, the extension deploys a single model, [multilingual-e5-small](https://huggingface.co/intfloat/multilingual-e5-small), to your Azure Database for PostgreSQL Flexible Server instance. Other open-source models might become available for installation on an ongoing basis.

> [!NOTE]  
> Enabling Azure Local AI will deploy the [multilingual-e5-small](https://huggingface.co/intfloat/multilingual-e5-small) model to your Azure Database for PostgreSQL Flexible Server instance. The linked documentation provides licensing terms from the e5 team.
> Additional third-party open-source models might become available for installation on an ongoing basis.


Local embeddings help customers:
- Reduce latency of embedding creation.
- Use embedding models at a predictable cost.
- Keep data within their database eliminating the need to transmit data to a remote endpoint.
  
During public preview, the `azure_local_ai` extension is only available in these Azure regions:
 
- Australia East
- East US
- France Central
- Japan East
- UK South
- West Europe
- West US

This preview feature is also only available for newly deployed Azure Database for PostgreSQL Flexible Server instances.

> [!IMPORTANT]
> The `azure_local_ai` extension is currently in preview. Microsoft's Open-source AI models for installation through the Azure Local AI extension are deemed Non-Microsoft Products under the Microsoft Product Terms. Customer's use of open-source AI models is governed by the separate license terms provided in product documentation associated with such models made available through the azure_local_ai extension. [Supplemental Terms of Use: Limited Access AI Services (Previews)](https://azure.microsoft.com/support/legal/preview-supplemental-terms/)

[Share your suggestions and bugs with the Azure Database for PostgreSQL product team](https://aka.ms/pgfeedback).

## Related content

- [Enable and use azure_local_ai extension](generative-ai-azure-local-ai.md).
- [Enable and use pgvector extension](how-to-use-pgvector.md).
