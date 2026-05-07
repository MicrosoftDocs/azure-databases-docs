---
title: azure_ai Extension in Azure HorizonDB
description: Introduction to the azure_ai extension in Azure HorizonDB, which enables you to invoke models hosted in Microsoft Foundry from within the database.
author: shreyaaithal
ms.author: shaithal
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-database-postgresql
ms.subservice: ai-azure
ms.topic: concept-article
ms.collection:
  - ce-skilling-ai-copilot
ms.update-cycle: 180-days
ms.custom:
  - build-2026
# customer intent: As a user, I want to understand how to use the azure_ai extension to invoke Foundry models from within the database.
---

# azure_ai Extension in Azure HorizonDB

Azure HorizonDB extension for Azure AI enables you to use large language models (LLMS) and build rich generative AI applications within the database. The Azure AI extension enables the database to call into various Microsoft Foundry tools including [Azure OpenAI](/azure/ai-services/openai/overview) and [Azure Cognitive Services](https://azure.microsoft.com/products/ai-services/cognitive-search/) simplifying the development process allowing seamless integration into those services.

## Enable the azure_ai extension

Before you can enable `azure_ai` on your Azure HorizonDB instance, you need to add it to your allowlist as described in [how to use PostgreSQL extensions](../extensions/how-to-allow-extensions.md) and check if correctly added by running `SHOW azure.extensions;`.

> [!TIP]  
> You might also want to enable the [Enable and use pgvector in Azure HorizonDB](../extensions/how-to-use-pgvector.md) as it's commonly used with `azure_ai`.

Then you can install the extension, by connecting to your target database and running the [CREATE EXTENSION](https://www.postgresql.org/docs/current/sql-createextension.html) command. You need to repeat the command separately for every database you want the extension to be available in.

```sql
CREATE EXTENSION IF NOT EXISTS azure_ai;
```

> [!NOTE]  
> To remove the extension from the currently connected database use `DROP EXTENSION azure_ai;`.

Installing the extension `azure_ai` creates the following three schemas:

- `azure_ai`: principal schema where the configuration table resides and functions to interact with it.
- `azure_openai`: functions and composite types related to OpenAI.
- `azure_cognitive`: functions and composite types related to Cognitive Services.

The extension also allows calling Azure OpenAI and Azure Cognitive Services.

## Configure the azure_ai extension

Configuring the extension requires you to provide the endpoints to connect to the Foundry tools and the API keys required for authentication. Service settings are stored using following functions:

### Permissions

Your Azure AI access keys are similar to a root password for your account. Always be careful to protect your access keys. Use Azure Key Vault to manage and rotate your keys securely.
To manage service keys used by the extension, users require the `azure_ai_settings_manager` role granted to them. The following functions require the role:
- azure_ai.set_setting
- azure_ai.get_setting

The `azure_ai_settings_manager` role is by default granted to the `azure_pg_admin` role.

### `azure_ai.set_setting`

Used to set configuration options.

```sql
azure_ai.set_setting(key TEXT, value TEXT)
```

#### Arguments

##### `key`

Name of a configuration option. Valid values for the `key` are:
- `azure_openai.endpoint`: Supported OpenAI endpoint (for example, `https://example.openai.azure.com`).
- `azure_openai.subscription_key`: A subscription key for an OpenAI resource.
- `azure_cognitive.endpoint`: Supported Cognitive Services endpoint (for example, `https://example.cognitiveservices.azure.com`).
- `azure_cognitive.subscription_key`: A subscription key for a Cognitive Services resource.

##### `value`

`TEXT` representing the desired value of the selected setting.

### `azure_ai.get_setting`

Used to obtain current values of configuration options.

```sql
azure_ai.get_setting(key TEXT)
```

#### Arguments

##### Key

Name of a configuration option. Valid values for the `key` are:
- `azure_openai.endpoint`: Supported OpenAI endpoint (for example, `https://example.openai.azure.com`).
- `azure_openai.subscription_key`: A subscription key for an OpenAI resource.
- `azure_cognitive.endpoint`: Supported Cognitive Services endpoint (for example, `https://example.cognitiveservices.azure.com`).
- `azure_cognitive.subscription_key`: A subscription key for a Cognitive Services resource.

#### Return type

`TEXT` representing the current value of the selected setting.

### `azure_ai.version`

```sql
azure_ai.version()
```

#### Return type

`TEXT` representing the current version of the Azure AI extension.

### Examples

#### Set the Endpoint and an API Key for Azure OpenAI

```sql
select azure_ai.set_setting('azure_openai.endpoint','https://<endpoint>.openai.azure.com');
select azure_ai.set_setting('azure_openai.subscription_key', '<API Key>');
```

#### Get the Endpoint and API Key for Azure OpenAI

```sql
select azure_ai.get_setting('azure_openai.endpoint');
select azure_ai.get_setting('azure_openai.subscription_key');
```

#### Check the Azure AI extension version

```sql
select azure_ai.version();
```

## Permissions

The `azure_ai` extension defines a role called `azure_ai_settings_manager`, which enables reading and writing of settings related to the extension. Only superusers and members of the `azure_ai_settings_manager` role can invoke the `azure_ai.get_settings` and `azure_ai.set_settings` functions. In Azure HorizonDB, all admin users have the `azure_ai_settings_manager` role assigned.

## Upgrade the Azure AI extension

Newer versions of the extension can introduce new functionality and in-place upgrades of the extension are allowed. You can compare the currently installed version to the newest version allowed by using the SQL command:

```sql
SELECT * FROM pg_available_extensions
WHERE name = 'azure_ai'
```

To update an installed extension to the latest available version supported by Azure, use the following SQL command:

```sql
ALTER EXTENSION azure_ai UPDATE;
```

## Related content

- [Integrate Azure HorizonDB with Azure Cognitive Services](generative-ai-azure-cognitive.md)
- [Integrate Azure HorizonDB with Azure Machine Learning Services](generative-ai-azure-machine-learning.md)
- [Generate vector embeddings with Azure OpenAI in Azure HorizonDB](generative-ai-azure-openai.md)
- [Generative AI in Azure HorizonDB](generative-ai-overview.md)
- [Tutorial: Create a recommendation system with Azure OpenAI in Azure HorizonDB](generative-ai-recommendation-system.md)
- [Tutorial: Create a semantic search with Azure OpenAI in Azure HorizonDB](generative-ai-semantic-search.md)
- [Enable and use pgvector in Azure HorizonDB](../extensions/how-to-use-pgvector.md)
