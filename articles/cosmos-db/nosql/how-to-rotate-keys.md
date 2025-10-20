---
title: Rotate keys
titleSuffix: Azure Cosmos DB for NoSQL
description: Learn how to rotate primary and secondary keys for Azure Cosmos DB for NoSQL accounts to maintain database security. Step-by-step guide included.
author: seesharprun
ms.author: sidandrews
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: how-to
ms.date: 10/20/2025
ms.custom:
  - sfi-image-nochange
  - sfi-ropc-nochange
ai-usage: ai-generated
applies-to:
  - ✅ NoSQL
  - ✅ MongoDB
  - ✅ Apache Cassandra
  - ✅ Apache Gremlin
  - ✅ Table
---

# Rotate keys for Azure Cosmos DB for NoSQL

[!INCLUDE[Note - ROPC and Entra ID authentication](includes/note-ropc-entra-authentication.md)]

Azure Cosmos DB for NoSQL allows you to rotate primary and secondary keys to maintain security. This article explains how to regenerate keys while ensuring continuous application access to your database.

> [!NOTE]
> Key regeneration can take anywhere from one minute to multiple hours depending on the size of the Azure Cosmos DB for NoSQL account. Ensure your application is consistently using either the primary key or the secondary key before starting the rotation process.

## Prerequisites

- An existing Azure Cosmos DB for NoSQL account

- Application currently using either primary or secondary key consistently

## Rotate keys when using the primary key

If your application is currently using the primary key, follow these steps to rotate to the secondary key and regenerate the primary key.

1. Sign in to the Azure portal (<https://portal.azure.com>).

1. Navigate to your Azure Cosmos DB for NoSQL account.

1. Select **Keys** from the navigation menu.

1. Select **Regenerate Secondary Key** from the ellipsis menu next to your secondary key.

1. Validate that the new secondary key works consistently against your Azure Cosmos DB for NoSQL account.

1. Update your application to use the secondary key instead of the primary key.

1. Return to the **Keys** section and select **Regenerate Primary Key** from the ellipsis menu next to your primary key.

## Rotate keys when using the secondary key

If your application is currently using the secondary key, follow these steps to rotate to the primary key and regenerate the secondary key.

1. In the **Keys** section of your Azure Cosmos DB for NoSQL account, select **Regenerate Primary Key** from the ellipsis menu next to your primary key.

1. Validate that the new primary key works consistently against your Azure Cosmos DB for NoSQL account.

1. Update your application to use the primary key instead of the secondary key.

1. Return to the **Keys** section and select **Regenerate Secondary Key** from the ellipsis menu next to your secondary key.

## Related content

- [Azure Cosmos DB for NoSQL security overview](security.md)
- [Use role-based access control and Microsoft Entra ID authentication in Azure Cosmos DB for NoSQL](how-to-connect-role-based-access-control.md)
