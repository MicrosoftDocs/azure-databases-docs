---
title: Use Azure Cosmos DB Change Feed with Azure Functions
description: Use Azure Functions to connect to Azure Cosmos DB change feed. Later you can create reactive Azure functions that are triggered on every new event.
author: markjbrown
ms.author: mjbrown
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.custom: build-2023
ms.topic: how-to
ms.date: 07/02/2025
---

# Serverless event-based architectures with Azure Cosmos DB and Azure Functions
[!INCLUDE[NoSQL](../includes/appliesto-nosql.md)]

Azure Functions provides the simplest way to connect to the [change feed](../change-feed.md). You can create small, reactive Azure Functions that are automatically triggered on each new event in your Azure Cosmos DB container's change feed.

:::image type="content" source="./media/change-feed-functions/functions.png" alt-text="Diagram of serverless event-based functions working with the Azure Functions trigger for Azure Cosmos DB.":::

With the [Azure Functions trigger for Azure Cosmos DB](/azure/azure-functions/functions-bindings-cosmosdb-v2-trigger), you can use the [change feed processor's](change-feed-processor.md) scaling and reliable event detection functionality without the need to maintain any [worker infrastructure](change-feed-processor.md). Just focus on your Azure Function's logic without worrying about the rest of the event-sourcing pipeline. You can even mix the trigger with any other [Azure Functions bindings](/azure/azure-functions/functions-triggers-bindings#supported-bindings).

> [!NOTE]
> The Azure Functions trigger uses [latest version change feed mode](change-feed-modes.md#latest-version-change-feed-mode). Currently, the Azure Functions trigger for Azure Cosmos DB is supported for use with the API for NoSQL only.

## Requirements

To implement a serverless event-based flow, you need:

* **The monitored container**: The monitored container is the Azure Cosmos DB container being monitored, and it stores the data from which the change feed is generated. Any inserts or updates to the monitored container are reflected in the change feed of the container.
* **The lease container**: The lease container maintains state across multiple and dynamic serverless Azure Function instances and enables dynamic scaling. You can create the lease container automatically with the Azure Functions trigger for Azure Cosmos DB. You can also create the lease container manually. To automatically create the lease container, set the *CreateLeaseContainerIfNotExists* property in the [configuration](/azure/azure-functions/functions-bindings-cosmosdb-v2-trigger?tabs=extensionv4&pivots=programming-language-csharp#attributes). Partitioned lease containers are required to have a `/id` partition key definition.

## Create your Azure Functions trigger for Azure Cosmos DB

Creating your Azure Function with an Azure Functions trigger for Azure Cosmos DB is now supported across all Azure Functions IDE and CLI integrations:

* [Visual Studio extension](/azure/azure-functions/functions-develop-vs) for Visual Studio users
* [Visual Studio Code extension](/azure/developer/javascript/tutorial-vscode-serverless-node-01) for Visual Studio Code users
* [Core CLI tooling](/azure/azure-functions/functions-run-local#create-func) for a cross-platform IDE agnostic experience

## Run your trigger locally

You can run your [Azure Function locally](/azure/azure-functions/functions-develop-local) with the [Azure Cosmos DB emulator](../emulator.md) to create and develop your serverless event-based flows without an Azure Subscription or incurring any costs.

## Next steps

You can now continue to learn more about change feed in the following articles:

* [Overview of change feed](../change-feed.md)
* [Reading Azure Cosmos DB change feed](read-change-feed.md)
* [Change feed processor in Azure Cosmos DB](change-feed-processor.md)
* [Serverless database computing using Azure Cosmos DB and Azure Functions](serverless-computing-database.md)
