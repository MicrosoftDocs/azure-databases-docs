---
title: Add and assign user roles
titleSuffix: Azure Cosmos DB for NoSQL
description: Learn how to add and assign user roles for Azure Cosmos DB for NoSQL accounts. Follow step-by-step instructions to configure role-based access control and secure your database resources.
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

# Add and assign user roles for Azure Cosmos DB for NoSQL

[!INCLUDE[Note - ROPC and Entra ID authentication](includes/note-credentials-entra-authentication.md)]

Azure Cosmos DB for NoSQL allows you to assign roles to control access to your database resources. This article explains how to grant account reader access to users, groups, or service principals to ensure secure resource management.

> [!NOTE]
> Role assignments require subscription owner permissions. Ensure you have the appropriate permissions before attempting to assign roles to your Azure Cosmos DB for NoSQL account.

## Prerequisites

- An existing Azure Cosmos DB for NoSQL account

- Subscription owner permissions or sufficient access control permissions

## Assign account reader role

To grant Azure Cosmos DB for NoSQL account reader access to a user, group, or service principal, you need to configure role assignments through Access control (IAM).

1. Sign in to the Azure portal (<https://portal.azure.com>).

1. Navigate to your Azure Cosmos DB for NoSQL account.

1. Select **Access control (IAM)** from the navigation menu.

1. Select **Add** > **Add role assignment** to open the role assignment configuration.

1. Configure the role assignment with the following settings:

   | Setting | Value |
   | --- | --- |
   | **Role** | Cosmos DB Account Reader |
   | **Assign access to** | User, group, or service principal |
   | **Members** | The user, group, or application in your directory |

1. Select **Review + assign** to complete the role assignment.

The assigned entity can now read Azure Cosmos DB for NoSQL resources in your account.

## Related content

- [Azure Cosmos DB for NoSQL security overview](security.md)
- [Use role-based access control and Microsoft Entra ID authentication in Azure Cosmos DB for NoSQL](how-to-connect-role-based-access-control.md)