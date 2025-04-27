---
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: include
ms.date: 04/27/2025
---

In this guide, you build a Rust console application to connect to an existing Azure Cosmos DB for MongoDB vCore cluster. This guide covers the required steps to configure the cluster for Microsoft Entra authentication and then to connect to the same cluster using the identity that you're currently signed-in with.

After authenticating, you can use this library to interact with Azure Cosmos DB for MongoDB vCore using the same methods and classes you would typically use to interact with any other MongoDB or DocumentDB instance.