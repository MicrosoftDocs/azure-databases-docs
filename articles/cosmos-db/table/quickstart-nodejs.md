---
title: Quickstart - Node.js client library
titleSuffix: Azure Cosmos DB for Table
description: Deploy a Node.js web application that uses the Azure SDK for Table to interact with Azure Cosmos DB for Table data in this quickstart.
author: seesharprun
ms.author: sidandrews
ms.reviewer: sasinnat
ms.service: azure-cosmos-db
ms.subservice: table
ms.devlang: typescript
ms.topic: quickstart-sdk
ms.date: 10/23/2024
ms.custom: devx-track-js, devx-track-ts, devx-track-extended-azdevcli
zone_pivot_groups: azure-devlang-nodejs
# CustomerIntent: As a developer, I want to learn the basics of the Node.js library so that I can build applications with Azure Cosmos DB for Table.
---

# Quickstart: Azure Cosmos DB for Table library for Node.js

[!INCLUDE[Table](../includes/appliesto-table.md)]

[!INCLUDE[Developer Quickstart selector](includes/quickstart/dev-selector.md)]

This quickstart shows how to get started with the Azure Cosmos DB for Table from a Node.js application. The Azure Cosmos DB for Table is a schemaless data store allowing applications to store structured table data in the cloud. You learn how to create tables, rows, and perform basic tasks within your Azure Cosmos DB resource using the Azure SDK for Node.js.

[API reference documentation](/javascript/api/%40azure/data-tables) | [Library source code](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/tables/data-tables) | [Package (npm)](https://www.npmjs.com/package/@azure/data-tables) | [Azure Developer CLI](/azure/developer/azure-developer-cli/overview)

## Prerequisites

- An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/free/?WT.mc_id=A261C142F).
- [Azure Developer CLI](/azure/developer/azure-developer-cli/install-azd)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Node.js 22 or newer](https://nodejs.org/)

## Initialize the project

Use the Azure Developer CLI (`azd`) to create an Azure Cosmos DB for Table account and deploy a containerized sample application. The sample application uses the client library to manage, create, read, and query sample data.

1. Open a terminal in an empty directory.

1. If you're not already authenticated, authenticate to the Azure Developer CLI using `azd auth login`. Follow the steps specified by the tool to authenticate to the CLI using your preferred Azure credentials.

    ```azurecli
    azd auth login
    ```

1. Use `azd init` to initialize the project.

    ```azurecli
    azd init --template cosmos-db-table-nodejs-quickstart
    ```

1. During initialization, configure a unique environment name.

1. Deploy the Azure Cosmos DB account using `azd up`. The Bicep templates also deploy a sample web application.

    ```azurecli
    azd up
    ```

1. During the provisioning process, select your subscription, desired location, and target resource group. Wait for the provisioning process to complete. The process can take **approximately five minutes**.

1. Once the provisioning of your Azure resources is done, a URL to the running web application is included in the output.

    ```output
    Deploying services (azd deploy)
    
      (✓) Done: Deploying service web
    - Endpoint: <https://[container-app-sub-domain].azurecontainerapps.io>
    
    SUCCESS: Your application was provisioned and deployed to Azure in 5 minutes 0 seconds.
    ```

1. Use the URL in the console to navigate to your web application in the browser. Observe the output of the running app.

    :::image type="content" source="media/quickstart/dev-web-application.png" alt-text="Screenshot of the running web application.":::

### Install the client library

The client library is available through npm, as the `@azure/data-tables` package.

::: zone pivot="programming-language-ts"

1. Open a terminal and navigate to the `/src/ts` folder.

    ```bash
    cd ./src/ts
    ```

1. If not already installed, install the `@azure/data-tables` package using `npm install`.

    ```bash
    npm install --save @azure/data-tables
    ```

1. Open and review the **src/ts/package.json** file to validate that the `@azure/data-tables` entry exists.

::: zone-end

::: zone pivot="programming-language-js"

1. Open a terminal and navigate to the `/src/js` folder.

    ```bash
    cd ./src/js
    ```

1. If not already installed, install the `@azure/data-tables` package using `npm install`.

    ```bash
    npm install --save @azure/data-tables
    ```

1. Open and review the **src/js/package.json** file to validate that the `@azure/data-tables` entry exists.

::: zone-end

## Object model

| Name | Description |
| --- | --- |
| [`TableServiceClient`](/javascript/api/@azure/data-tables/tableserviceclient) | This type is the primary client type and is used to manage account-wide metadata or databases. |
| [`TableClient`](/javascript/api/@azure/data-tables/tableclient) | This type represents the client for a table within the account. |

## Code examples

TODO

## Clean up resources

When you no longer need the sample application or resources, remove the corresponding deployment and all resources.

```azurecli
azd down
```

## Related content

- [.NET Quickstart](quickstart-dotnet.md)
- [Python Quickstart](quickstart-python.md)
- [Java Quickstart](quickstart-java.md)
- [Go Quickstart](quickstart-go.md)
