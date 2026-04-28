---
title: azure_ai extension in Azure Database for PostgreSQL
description: Introduction to the azure_ai extension in Azure Database for PostgreSQL, which enables you to use LLMs hosted in Microsoft Foundry and invoke Foundry tools from within the database.
author: shreyaaithal
ms.author: shaithal
ms.reviewer: maghan
ms.date: 04/28/2026
ms.service: azure-database-postgresql
ms.subservice: ai-azure
ms.topic: how-to
ms.collection:
  - ce-skilling-ai-copilot
ms.update-cycle: 180-days
ms.custom:
  - ignite-2023
  - build-2024
  - build-2025
---

# azure_ai extension in Azure Database for PostgreSQL

The azure_ai extension in Azure Database for PostgreSQL enables in-database use of large language models (LLMs) to build generative AI applications. It allows the database to call into [Azure OpenAI in Microsoft Foundry models](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure#azure-openai-in-microsoft-foundry-models), [Azure OpenAI Service](/azure/ai-services/openai/overview), [Azure Cognitive Services (Azure Language in Foundry Tools)](https://learn.microsoft.com/azure/ai-services/language-service/), and [Azure Machine Learning Services](https://learn.microsoft.com/azure/machine-learning/), simplifying development through seamless integration with these services.

## Enable the azure_ai extension

### Allowlist the extension

Add `azure_ai` to your Azure Database for PostgreSQL flexible server's allowlist as described in [how to use PostgreSQL extensions](../extensions/how-to-allow-extensions.md). Verify that it has been added correctly by running the `SHOW azure.extensions;` query.

### Install the extension

Connect to your database and run the [`CREATE EXTENSION`](https://www.postgresql.org/docs/current/static/sql-createextension.html) command:

  ```sql
  CREATE EXTENSION IF NOT EXISTS azure_ai;
  ```
Repeat this command for each database where the extension is required.

Installing azure_ai creates the following schemas:
- azure_ai: principal schema for configuration and related functions
- azure_openai: functions and types for Azure OpenAI Service and OpenAI models in Microsoft Foundry
- azure_cognitive: functions and types for Azure Cognitive Services (Azure Language in Foundry Tools)
- azure_ml: functions and types for Azure Machine Learning Services

> [!TIP]
> You may also want to enable the [`pgvector` extension](../extensions/../extensions/how-to-use-pgvector.md) as it is commonly used with `azure_ai`.


> [!NOTE]  
> To remove the extension from the current database, run `DROP EXTENSION azure_ai;`.


## Configure the azure_ai extension

To configure the extension, provide endpoints and authentication details (API key or Managed Identity) for the Azure AI services you want to use. These values are stored using the `azure_ai.set_setting` configuration function with various configuration keys.

### Permissions

The extension defines a role `azure_ai_settings_manager` that allows reading and writing configuration settings using the `azure_ai.set_getting` and `azure_ai.set_setting` functions. Only superusers and members of this role can invoke these functions. In Azure Database for PostgreSQL Flexible Server, the role is granted by default to the `azure_pg_admin` role.

### Configuration functions

#### `azure_ai_set_setting`

Used to set the azure_ai configuration.

**Usage:**

```sql
-- Syntax
azure_ai.set_setting(key TEXT, value TEXT)

-- Usage example: Set the Endpoint and an API Key for Azure OpenAI
select azure_ai.set_setting('azure_openai.endpoint','https://<endpoint>.openai.azure.com');
select azure_ai.set_setting('azure_openai.subscription_key', '<API Key>');
```

**List of supported configuration keys and values:**

| **`key`**  | **`value`** |
| --------------------------------------- | ------------------------------ |
| `azure_openai.endpoint` | Supported OpenAI endpoint (for example, `https://example.openai.azure.com`). |
| `azure_openai.auth_type` | `subscription-key` or `managed-identity` |
| `azure_openai.subscription_key` | A subscription key for an OpenAI resource. |
| `azure_cognitive.endpoint` | Supported Cognitive Services endpoint (for example, `https://example.cognitiveservices.azure.com`) |
| `azure_cognitive.auth_type` | `subscription-key` or `managed-identity` |
| `azure_cognitive.subscription_key` | A subscription key for a Cognitive Services resource. |
| `azure_ml.scoring_endpoint`| Supported Azure Machine Learning online endpoint URI. |
| `azure_ml.auth_type` | `subscription-key` or `managed-identity` |
| `azure_ml.endpoint_key`| An endpoint key for an Azure ML endpoint. |


#### `azure_ai.get_setting`

Used to obtain current configuration values for a given `key` (see supported keys above). Returns `TEXT` representing the current value of the selected setting.

**Usage:**

```sql
-- Syntax
azure_ai.get_setting(key TEXT)

-- Usage example: Get the Endpoint and API Key for Azure OpenAI
select azure_ai.get_setting('azure_openai.endpoint');
select azure_ai.get_setting('azure_openai.subscription_key');
```


#### `azure_ai.version`

Returns `TEXT` representing the current version of the `azure_ai` extension.

**Usage:**

```sql
SELECT azure_ai.version()
```

### Enable managed identity authentication

The azure_ai extension for Azure Database for PostgreSQL supports System Assigned Managed Identity (SAMI) which offers enhanced security benefits. By using Microsoft Entra ID, users can authenticate without access keys, reducing the risk of unauthorized access and simplifying credential management.

To enable managed identity authentication, see [this how-to guide](generative-ai-enable-managed-identity-azure-ai.md).

## Capabilities of the `azure_ai` extension

### AI functions

The azure_ai extension enables in-database calls to models hosted in Microsoft Foundry and Azure OpenAI through the following **AI functions (Preview)**:

- [`azure_openai.create_embeddings()`](generative-ai-azure-openai.md): Creates vector embeddings for a given input text.
- [`azure_ai.generate()`](generative-ai-azure-ai-functions.md#azure_aigenerate): Generates text or structured output using Large Language Models (LLMs).
- [`azure_ai.is_true()`](generative-ai-azure-ai-functions.md#azure_aiis_true): Evaluates the likelihood that a given statement is true.
- [`azure_ai.extract()`](generative-ai-azure-ai-functions.md#azure_aiextract): Extracts structured features or entities from text.
- [`azure_ai.rank()`](generative-ai-azure-ai-functions.md#azure_airank): Reranks a list of documents based on relevance to a given query.

### Additional capabilities 

The extension also supports invoking
- [Azure Language in Foundry Tools](generative-ai-azure-cognitive.md): Enables tasks such as sentiment analysis directly within the database.
- [Azure Machine Learning online endpoints](generative-ai-azure-machine-learning.md): Allows you to call models from the Azure Machine Learning catalog or custom-trained deployments.


## Upgrade the Azure AI extension

To check the installed version and available upgrades, run:

```sql
SELECT * FROM pg_available_extensions
WHERE name = 'azure_ai'
```

To update the extension to the latest supported version, run:

```sql
ALTER EXTENSION azure_ai UPDATE;
```

## Related content

- [AI functions in the azure_ai extension (Preview)](generative-ai-azure-ai-functions.md)
- [Generate vector embeddings with Azure OpenAI in Azure Database for PostgreSQL](generative-ai-azure-openai.md)
- [Enable and use pgvector in Azure Database for PostgreSQL](../extensions/../extensions/how-to-use-pgvector.md)
- [Create a semantic search with Azure Database for PostgreSQL and Azure OpenAI](generative-ai-semantic-search.md)
- [Integrate Azure Database for PostgreSQL with Azure Machine Learning Services](generative-ai-azure-machine-learning.md)

