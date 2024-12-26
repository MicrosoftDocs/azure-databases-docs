---
title: Emulator (Docker/local)
titleSuffix: Azure Cosmos DB
description: Use the Azure Cosmos DB local or docker-based emulator to test your applications against multiple API endpoints.
author: sajeetharan
ms.author: sasinnat
ms.service: azure-cosmos-db
ms.custom:
  - ignite-2024
ms.topic: concept-article
ms.date: 11/07/2024
# CustomerIntent: As a developer, I want to use the Azure Cosmos DB emulator so that I can develop my application against a database during development.
---

# What is the Azure Cosmos DB emulator?

The Azure Cosmos DB emulator provides a local environment that emulates the Azure Cosmos DB service designed for development purposes. Using the emulator, you can develop and test your application locally, without creating an Azure subscription or incurring any service costs. When you're satisfied with how your application is working with the emulator, you can transition to using an Azure Cosmos DB account with minimal friction.

> [!IMPORTANT]
> We do not recommend the use of the emulator for production workloads.

> [!TIP]
> Visit our new **[Samples Gallery](https://aka.ms/AzureCosmosDB/Gallery)** for the latest samples for building new apps

## Differences between the emulator and cloud service

The emulator provides an environment on your developer workspace that isn't capable of emulating every aspect of the Azure Cosmos DB service. Here are a few key differences in functionality between the emulator and the equivalent cloud service.

> [!IMPORTANT]
> The Linux emulator currently doesn't support developer machines running on Apple silicon series or Microsoft ARM chips. A temporary workaround is to install a Windows virtual machine and run the emulator on that platform.
>
> Alternatively, you can used the new [Linux-based Azure Cosmos DB emulator (preview)](emulator-linux.md).

- The emulator's **Data Explorer** pane is only supported in the API for NoSQL and API for MongoDB.
- The emulator only supports **provisioned throughput**. The emulator doesn't support **serverless** throughput.
- The emulator uses a well-known key when it starts. You can't regenerate the key for the running emulator. To use a different key, you must [start the emulator with the custom key specified](#authentication).
- The emulator can't be replicated across geographical regions or multiple instances. Only a single running instance of the emulator is supported. The emulator can't be scaled out.
- The emulator ideally supports up to 10 fixed-size containers at 400 RU/s or 5 unlimited-size containers. Theoretically, you can create more containers, but you could experience performance degradation with the emulator.
- The emulator only supports the [Session](consistency-levels.md#session-consistency) and [Strong](consistency-levels.md#strong-consistency) consistency levels. The emulator isn't a scalable service and doesn't actually implement the consistency levels. The emulator only flags the configured consistency level for testing purposes.
- The emulator constraints the unique identifier of items to a size of **254** characters.
- The emulator supports a maximum of five `JOIN` statements per query.

The emulator's features may lag behind the pace of new features for the cloud service. There could potentially be new features and changes in the cloud service that have a small delay before they're available in the emulator.

## Authentication

Every request made against the emulator must be authenticated using a key over TLS/SSL. The emulator ships with a single account configured to use a well-known authentication key. By default, these credentials are the only credentials permitted for use with the emulator:

| | Value |
| --- | --- |
| **Endpoint** | `localhost:8081` |
| **Key** | `C2y6yDjf5/R+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw/Jw==` |
| **Connection string** | `AccountEndpoint=https://localhost:8081/;AccountKey=C2y6yDjf5/R+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw/Jw==;` |

> [!TIP]
> With the Windows (local) emulator, you can also customize the key used by the emulator. For more information, see [Windows emulator arguments](emulator-windows-arguments.md).

## Import emulator certificate

In some cases, you may wish to manually import the TLS/SS certificate from the emulator's running container into your host machine. This step avoids bad practices like disabling TLS/SSL validation in the SDK. For more information, see [import certificate](how-to-develop-emulator.md#import-the-emulators-tlsssl-certificate).

## Related content

- [Linux-based Azure Cosmos DB emulator (preview)](emulator-linux.md)

## Next step

> [!div class="nextstepaction"]
> [Get started using the Azure Cosmos DB emulator for development](how-to-develop-emulator.md)
