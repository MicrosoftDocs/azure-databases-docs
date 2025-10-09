---
title: Role-based access control (RBAC)
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: Learn about the concepts of role-based access control in Azure Cosmos DB for MongoDB vCore.
author: niklarin
ms.author: nlarin
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: concept-article
ms.date: 09/23/2025
appliesto:
  - ✅ MongoDB (vCore)
---

# Role-based access control (RBAC) in Azure Cosmos DB for MongoDB vCore

Azure Cosmos DB for MongoDB vCore supports integration with Microsoft Entra ID and native DocumentDB authentication. Each Azure Cosmos DB for MongoDB vCore cluster is created with native DocumentDB authentication enabled and one built-in administrative user.

You can enable Microsoft Entra ID authentication on a cluster in addition to the native DocumentDB authentication method or instead of it. You can configure authentication methods on each Azure Cosmos DB for MongoDB vCore cluster independently. If you need to change authentication method, you can do it at any time after cluster provisioning is completed. Changing authentication methods doesn't require cluster restart.

## Azure role-based access control (RBAC)

[Microsoft Entra ID](/entra/fundamentals/whatis) authentication is a mechanism of connecting to Azure Cosmos DB  for MongoDB vCore using identities defined in Microsoft Entra ID. With Microsoft Entra ID authentication, you can manage database user identities and other Microsoft services in a central location, which simplifies permission management and identity services compliance enforcement.

Benefits of using Microsoft Entra ID for authentication include:

- Authentication of users across Azure services in a uniform way

- Management of password policies and password rotation in a single place

- Multiple forms of authentication supported by Microsoft Entra ID, which can eliminate the need to store passwords

- Support of token-based authentication for applications connecting to Azure Cosmos DB for MongoDB vCore clusters


## User management role-based access control (RBAC)

When Microsoft Entra ID authentication is enabled on an Azure Cosmos DB for MongoDB vCore cluster, you can add one or more Microsoft Entra ID principals as *administrator users* to that cluster. The Microsoft Entra ID administrator can be a Microsoft Entra ID user, a service principal, or a managed identity. Multiple Microsoft Entra ID administrators can be configured at any time. 

Administrative Entra ID users are created as Azure entities under Microsoft.DocumentDB/mongoClusters/users and are replicated to the database.

Additionally, one or more nonadministrative Microsoft Entra ID users can be added to a cluster at any time once Microsoft Entra ID authentication is enabled. Nonadministrative users are often used for ongoing production tasks that don't require administrative privileges.


## Related content

- Lean [how to enable Microsoft Entra ID and manage Entra ID users on clusters](./how-to-configure-entra-authentication.md)
- Learn [how to manage secondary native DocumentDB users on clusters](./secondary-users.md)
