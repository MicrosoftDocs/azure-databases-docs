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

In this guide, you build a console application to connect to an Azure Cosmos DB for MongoDB vCore cluster. This guide will cover the required steps to connect using Microsoft Entra authentication from your signed-in identity.

::: zone pivot="programming-language-csharp"

This guide will use the open-source `MongoDB.Driver` library from NuGet.

:::zone-end
::: zone pivot="programming-language-ts"
:::zone-end
::: zone pivot="programming-language-python"
:::zone-end

After authenticating, you can use this library to interact with Azure Cosmos DB for MongoDB vCore using the same methods and classes you would typically use to interact with any other MongoDB or DocumentDB instance.

## Prerequisites

- An existing Azure Cosmos DB for MongoDB (vCore) cluster.

::: zone pivot="programming-language-csharp"

- .NET 9.0 or later

:::zone-end
::: zone pivot="programming-language-ts"
:::zone-end
::: zone pivot="programming-language-python"
:::zone-end

## Grant your identity access



## Connect to the cluster



## Perform common operations

