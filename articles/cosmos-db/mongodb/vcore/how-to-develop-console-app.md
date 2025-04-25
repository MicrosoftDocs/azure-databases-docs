---
title: Develop a console app
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: Connect to an Azure Cosmos DB for MongoDB (vCore) cluster by using a console application in your preferred developer language.
author: seesharprun
ms.author: sidandrews
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: how-to
ms.date: 04/25/2025
ms.custom: devx-track-js, devx-track-python, devx-track-dotnet, devx-track-extended-azdevcli
zone_pivot_groups: programming-languages-set-documentdb
appliesto:
  - ✅ MongoDB (vCore)
# Customer Intent: As a database owner, I want to use Mongo Shell to connect to and query my database and collections.
---

# Develop a console app to connect to Azure Cosmos DB for MongoDB vCore

In this guide, you build a console application to connect to an Azure Cosmos DB for MongoDB vCore cluster. This guide covers the required steps to connect using Microsoft Entra authentication from your signed-in identity.

:::zone pivot="programming-language-csharp"

This guide uses the open-source `MongoDB.Driver` library from NuGet.

:::zone-end
:::zone pivot="programming-language-ts"
:::zone-end
:::zone pivot="programming-language-python"
:::zone-end

After authenticating, you can use this library to interact with Azure Cosmos DB for MongoDB vCore using the same methods and classes you would typically use to interact with any other MongoDB or DocumentDB instance.

## Prerequisites

- An existing Azure Cosmos DB for MongoDB (vCore) cluster.
- The latest version of the [Azure CLI](/cli/azure) in [Azure Cloud Shell](/azure/cloud-shell).
  - If you prefer to run CLI reference commands locally, sign in to the Azure CLI by using the [`az login`](/cli/azure/reference-index#az-login) command.
:::zone pivot="programming-language-csharp"
- [.NET](/dotnet).
:::zone-end
:::zone pivot="programming-language-ts"
- Latest version of [TypeScript](https://www.typescriptlang.org)
:::zone-end
:::zone pivot="programming-language-python"
- Latest version of [Python](https://www.python.org)
:::zone-end

## Grant your identity access

First, get the unique identifier for your currently signed-in identity. Then, use the Azure CLI to configure your existing cluster to support Microsoft Entra authentication directly with your identity.

1. Get the details for the currently logged-in account using `az ad signed-in-user`.

    ```azurecli-interactive
    az ad signed-in-user show
    ```    

1. The command outputs a JSON response containing various fields. 

    ```json
    {
      "@odata.context": "<https://graph.microsoft.com/v1.0/$metadata#users/$entity>",
      "businessPhones": [],
      "displayName": "Kai Carter",
      "givenName": "Kai",
      "id": "aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb",
      "jobTitle": "Senior Sales Representative",
      "mail": "<kai@adventure-works.com>",
      "mobilePhone": null,
      "officeLocation": "Redmond",
      "preferredLanguage": null,
      "surname": "Carter",
      "userPrincipalName": "<kai@adventure-works.com>"
    }
    ```

1. Record the value of the `id` field. This is the unique identifier for your principal and is sometimes referred to as the **principal ID**. You use this value in the next series of steps.

1. 

> [!TIP]
> These same steps can be followed to configure Microsoft Entra authentication for a managed identity, workload identity, application identity, or service principal.

## Configure your console application

Next, create a new console application project and import the necessary libraries to authenticate to your cluster.

:::zone pivot="programming-language-csharp"

1. In an empty directory, create a new .NET console application.

    ```dotnetcli
    dotnet new console
    ```

1. Import the `Azure.Identity` package from NuGet.

    ```dotnetcli
    dotnet add package Azure.Identity
    ```

1. Next, import the `MongoDB.Driver` package.

    ```dotnetcli
    dotnet add package MongoDB.Driver
    ```

1. Build the .NET project

    ```dotnetcli
    dotnet build
    ```

:::zone-end
:::zone pivot="programming-language-ts"
:::zone-end
:::zone pivot="programming-language-python"
:::zone-end

## Connect to the cluster

Now, use the `Azure.Identity` library to get a `TokenCredential` to use to connect to your cluster. The official MongoDB driver has a special interface that must be implemented to obtain tokens from Microsoft Entra for use when connecting to the cluster.

:::zone pivot="programming-language-csharp"

1. 

:::zone-end
:::zone pivot="programming-language-ts"
:::zone-end
:::zone pivot="programming-language-python"
:::zone-end

## Perform common operations

Finally, use the official `MongoDB.Driver` library to perform common tasks with databases, collections, and documents. Here, you use the same classes and methods you would use to interact with MongoDB or DocumentDB to manage your collections and items.

:::zone pivot="programming-language-csharp"

1. 

:::zone-end
:::zone pivot="programming-language-ts"
:::zone-end
:::zone pivot="programming-language-python"
:::zone-end

## Related content

- [Entra authentication overview](entra-authentication.md)
:::zone pivot="programming-language-csharp"
- [Deploy a .NET web application template](quickstart-dotnet.md)
:::zone-end
:::zone pivot="programming-language-ts"
:::zone-end
:::zone pivot="programming-language-python"
:::zone-end
