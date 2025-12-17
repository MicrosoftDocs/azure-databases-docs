---
title: Rotate keys
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

[!INCLUDE[Note - ROPC and Entra ID authentication](includes/note-credentials-entra-authentication.md)]

Azure Cosmos DB for NoSQL allows you to rotate primary and secondary keys to maintain security. This article explains how to regenerate keys while ensuring continuous application access to your database.

> [!NOTE]
> Key regeneration can take anywhere from one minute to multiple hours depending on the size of the Azure Cosmos DB for NoSQL account. Ensure your application is consistently using either the primary key or the secondary key before starting the rotation process.

## Prerequisites

- An existing Azure Cosmos DB for NoSQL account

- Application currently using either primary or secondary key consistently

## Rotate keys using account key usage metadata
> [!IMPORTANT]
> Account key usage metadata feature is in private preview. This feature is provided without a service-level agreement, and we don't recommend it for production workloads. For more information, see [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/)

Azure Cosmos DB now offers additional feature to ensure safe key rotation or disabling local authentication with Account Key Usage Metadata. This feature is designed to provide extra visibility into when an account key was last used, allowing teams to make informed decisions before rotating or migrating to Entra ID.

![Screenshot showing account key usage metadata in a Azure Cosmos DB account.](media/how-to-rotate-keys/safe-key-rotation.png)

### Why is it important?

- **Helps with disabling local authentication**: Provides confidence that keys are no longer in use before turning off local auth. 
- **Prevents Outages or disruption to your applications**: Avoids accidental rotation of actively used keys.
- **Improve Security Hygiene**: Encourages safe and intentional key rotation.

This is especially valuable for:
- Customers currently using keys but planning to migrate fully to Entra ID.
- Infrequently used keys: Monthly or yearly jobs that still depend on keys.
- Shared Keys across teams: Where visibility is often limited.

> [!NOTE]
> Customers interested in early access using [sign up form](https://aka.ms/SafeKeyRotationSignUp) or reach out to us on cosmosdb-sec-feature@microsoft.com

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
