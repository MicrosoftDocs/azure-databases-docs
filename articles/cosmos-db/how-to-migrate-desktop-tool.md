---
title: Migrate Data Using the Data Migration Tool
description: Use the Azure Cosmos DB Data Migration Tool to migrate data from JSON, MongoDB, SQL Server, and many other databases and file formats to Azure Cosmos DB.
author: sandeepsnairms
ms.author: sandnair
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: how-to
ms.date: 01/20/2026
ms.custom: sfi-ropc-blocked
# CustomerIntent: As a database owner, I want to use a tool to perform migration to Azure Cosmos DB so that I can streamline large and complex migrations.
appliesto:
  - ✅ NoSQL
  - ✅ MongoDB
  - ✅ Table
---

# Migrate data using the Data Migration Tool

The [Azure Cosmos DB Data Migration Tool](https://github.com/azurecosmosdb/data-migration-desktop-tool) is an open-source command-line application to import or export data from Azure Cosmos DB. The tool is built on an extension model for source and sink objects to migrate data.

## Supported extensions

- [Azure Cosmos DB for NoSQL](https://github.com/AzureCosmosDB/data-migration-desktop-tool/blob/main/Extensions/Cosmos/README.md)
- [JSON](https://github.com/AzureCosmosDB/data-migration-desktop-tool/blob/main/Extensions/Json/README.md)
- [MongoDB](https://github.com/AzureCosmosDB/data-migration-desktop-tool/blob/main/Extensions/Mongo/README.md)
- [SQL Server](https://github.com/AzureCosmosDB/data-migration-desktop-tool/blob/main/Extensions/SqlServer/README.md)
- [PostgreSQL](https://github.com/AzureCosmosDB/data-migration-desktop-tool/blob/main/Extensions/PostgreSQL/README.md)
- [Azure Blob Storage](https://github.com/AzureCosmosDB/data-migration-desktop-tool/blob/main/Extensions/AzureBlob/README.md)
- [Parquet](https://github.com/AzureCosmosDB/data-migration-desktop-tool/blob/main/Extensions/Parquet/README.md)
- [CSV](https://github.com/AzureCosmosDB/data-migration-desktop-tool/blob/main/Extensions/Csv/README.md)
- [AWS S3](https://github.com/AzureCosmosDB/data-migration-desktop-tool/blob/main/Extensions/AwsS3/README.md)
- [Azure AI Search (Cognitive Search)](https://github.com/AzureCosmosDB/data-migration-desktop-tool/blob/main/Extensions/CognitiveSearch/README.md)
- [Azure Cosmos DB for Table](https://github.com/AzureCosmosDB/data-migration-desktop-tool/blob/main/Extensions/AzureTableAPI/README.md)

## Prerequisites

- An existing Azure Cosmos DB for NoSQL account.
  - If you have an Azure subscription, [create a new account](how-to-create-account.md?tabs=azure-portal).
  - If you don't have an Azure subscription, create a [free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) before you begin.
- [.NET 8.0](https://dotnet.microsoft.com/download/dotnet/8.0) or later on your local machine.
- Optional [Docker Desktop](https://docs.docker.com/get-started/get-docker/)

## Using the prebuilt Docker image

The easiest way to use the container is to pull the prebuilt image from Microsoft Container Registry. [Docker Desktop](https://docs.docker.com/get-started/get-docker/) is required.

> [!NOTE]
> The Data Migration Tool can also be configured to run in any containerized environment or as part of a GitHub Action. See [Run in a Docker Container](https://github.com/AzureCosmosDB/data-migration-desktop-tool?tab=readme-ov-file#docker-container) for more details.

1. Pull the latest version of the container from the registry.

   ```shell
   docker pull mcr.microsoft.com/azurecosmosdb/linux/azure-cosmos-dmt:latest
   ```

1. Configure the migration settings. See [Configure migration settings](#configure-migration-settings)

```shell
docker run -v $(pwd)/config:/config -v $(pwd)/data:/data mcr.microsoft.com/azurecosmosdb/linux/azure-cosmos-dmt:latest run --settings /config/migrationsettings.json
```

## Using from command line

1. In your browser, navigate to the [**Releases** section of the repository](https://github.com/azurecosmosdb/data-migration-desktop-tool/releases).

1. Download the latest compressed folder for your platform. There are compressed folders for win-x64, win-arm64, mac-x64, mac-arm64, linux-x64, and linux-arm64 platforms.

1. Extract the files to an install location on your local machine.

1. (Optional) Add the Data Migration Tool to the `PATH` environment variable of your local machine.

1. Configure the migration settings. See [Configure migration settings](#configure-migration-settings)

1. Run the Data Migration Tool using the `dmt` command from a terminal.

    ```terminal
    dmt
    ```

    > [!NOTE]
    > If you didn't add the installation path to your `PATH` environment variable, you might need to specify the full path to the `dmt` executable.

1. The tool outputs the sources and sinks used by the migration.

    ```output
    Using JSON Source
    Using Cosmos-nosql Sink
    ```

## Configure migration settings

The Data Migration Tool uses a migrationsettings.json to define the source and sink settings for the data to be copied. See [Supported Extension](#supported-extensions) for details on each extensions migration settings.

Here's an example for migrating a [sample JSON file](https://github.com/AzureCosmosDB/data-migration-desktop-tool/blob/main/data/sample-data.json) to the Cosmos DB emulator.

```json
{
    "Source": "JSON",
    "Sink": "Cosmos-nosql",
    "SourceSettings": {
        "FilePath": "C:\\dmt\\data\\simple_json.json"
    },
    "SinkSettings": {
        "ConnectionString": "AccountEndpoint=https://localhost:8081/;AccountKey=C2y6yDj...",
        "Database": "datamigration",
        "Container": "sample",
        "PartitionKeyPath": "/id",
        "RecreateContainer": false,
        "IncludeMetadataFields": false
    }
}
```

### Migrate multiple sources

The migrationsettings.json can also be configured to execute multiple data transfer operations with a single run command with an *Operations* property consisting of an array of objects that include SourceSettings and SinkSettings for the extensions referenced in the *Source* and *Sink* properties.

Here's an example:

```json
{
  "Source": "json",
  "Sink": "cosmos-nosql",
  "SinkSettings": {
    "ConnectionString": "AccountEndpoint=https://localhost:8081/;AccountKey=C2y6yDj..."
  },
  "Operations": [
    {
      "SourceSettings": {
        "FilePath": "products.json"
      },
      "SinkSettings": {
        "Database": "ShoppingCartDB",
        "Container": "products",
        "PartitionKeyPath": "/categoryId"
      }
    },
    {
      "SourceSettings": {
        "FilePath": "customers.json"
      },
      "SinkSettings": {
        "Database": "ShoppingCartDB",
        "Container": "customers",
        "PartitionKeyPath": "/customerId"
      }
    },
    {
      "SourceSettings": {
        "FilePath": "orders.json"
      },
      "SinkSettings": {
        "Database": "ShoppingCartDB",
        "Container": "customers",
        "PartitionKeyPath": "/customerId"
      }
    }
  ]
}
```

### Query support

Some extensions have support for queries as well on the source settings. See the documentation for each extension for details.

Here's an example:

```json
{
  "Source": "cosmos-nosql",
  "Sink": "cosmos-nosql",
  "SourceSettings": {
    "ConnectionString": "AccountEndpoint=https://...",
    "Database": "ShoppingCartDB",
    "Container": "customers",
    "Query": "SELECT * FROM c WHERE c.type='order'"
  },
  "SinkSettings": {
    "ConnectionString": "AccountEndpoint=https://...",
    "Database": "orders",
    "PartitionKeyPath": "/customerId"
  }
}
```
