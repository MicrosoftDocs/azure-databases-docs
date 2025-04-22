---
title: Microsoft Entra ID authentication for Azure Cosmos DB for MongoDB vCore
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: Learn about the concepts of Microsoft Entra ID authentication with Azure Cosmos DB for MongoDB vCore.
author: niklarin
ms.author: nlarin
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: concept-article
ms.date: 04/20/2025
appliesto:
  - ✅ MongoDB vCore
---

# Microsoft Entra ID authentication with Azure Cosmos DB for MongoDB vCore

> [!IMPORTANT]
> Microsoft Entra ID authentication in Azure Cosmos DB for MongoDB vCore is currently in preview.
> This preview version is provided without a service level agreement, and it's not recommended
> for production workloads. Certain features might not be supported or might have constrained
> capabilities.

Azure Cosmos DB for MongoDB vCore supports integration with Microsoft Entra ID and native DocumentDB authentication. Each Azure Cosmos DB for MongoDB vCore cluster is created with native DocumentDB authentication enabled and one built-in administrative user.

You can enable Microsoft Entra ID (formerly Azure Active Directory) authentication on a cluster in addition to the native DocumentDB authentication method or instead of it. You can configure authentication methods on each Azure Cosmos DB for MongoDB vCore cluster independently. If you need to change authentication method, you can do it at any time after cluster provisioning is completed. Changing authentication methods doesn't require cluster restart.

## Microsoft Entra ID authentication

[Microsoft Entra ID](/entra/fundamentals/whatis) authentication is a mechanism of connecting to Azure Cosmos DB  for MongoDB vCore using identities defined in Microsoft Entra ID. With Microsoft Entra ID authentication, you can manage database user identities and other Microsoft services in a central location, which simplifies permission management and identity services compliance enforcement.

Benefits of using Microsoft Entra ID include:

- Authentication of users across Azure services in a uniform way
- Management of password policies and password rotation in a single place
- Multiple forms of authentication supported by Microsoft Entra ID, which can eliminate the need to store passwords
- Support of token-based authentication for applications connecting to Azure Cosmos DB for MongoDB vCore clusters

Interoperability with MongoDB drivers is provided via [OpenID Connect (OIDC) support in Microsoft Entra ID](/entra/identity-platform/v2-protocols-oidc). OIDC is an authentication protocol based on the OAuth2 protocol used for authorization. OIDC uses the standardized message flows from OAuth2 to provide identity services. When a security principal needs to authenticate to the database on an Azure Cosmos DB for MongoDB vCore cluster via Entra ID, OIDC identification and Entra ID security token should be provided.

### Administrative and non-administrative access for Microsoft Entra ID principals

When Microsoft Entra ID authentication is enabled on an Azure Cosmos DB for MongoDB vCore cluster, you can add one or more Microsoft Entra ID principals as *administrator users* to that cluster. The Microsoft Entra ID administrator can be a Microsoft Entra ID user, a service principal, or a managed identity. Multiple Microsoft Entra ID administrators can be configured at any time. 

Additionally, one or more non-administrative Microsoft Entra ID users can be added to a cluster at any time once Microsoft Entra ID authentication is enabled. Non-administrative users are often used for ongoing production tasks that don't require administrative privileges.

## Considerations

- Microsoft Entra ID can be the only authentication method enabled on a cluster.
- Multiple Microsoft Entra ID principals (a user, service principal, or managed identity) can be configured as Microsoft Entra ID administrator for an Azure Cosmos DB for MongoDB vCore cluster at any time.
- If a Microsoft Entra ID principal is deleted from Microsoft Entra ID service, it still remains as a PostgreSQL role on the cluster, but it's no longer able to acquire new access token. In this case, although the matching role still exists in the Postgres database it's unable to authenticate to the cluster nodes. Database administrators need to transfer ownership and drop such roles manually.

> [!NOTE]  
> Login with the deleted Microsoft Entra ID user can still be done until the token expires (up to 90 minutes from token issuing).  If you also remove the user from Azure Cosmos DB for PostgreSQL cluster this access are revoked immediately.

- Azure Cosmos DB for PostgreSQL matches access tokens to the database role using the user’s unique Microsoft Entra ID user ID, as opposed to using the username. If a Microsoft Entra ID user is deleted and a new user is created with the same name, Azure Cosmos DB for PostgreSQL considers that a different user. Therefore, if a user is deleted from Microsoft Entra ID and a new user is added with the same name the new user would be unable to connect with the existing role.

## Next steps

- Learn how to manage [authentication and Entra ID users in Azure Cosmos DB for MongoDB vCore](./how-to-configure-authentication.md)
- Review [Microsoft Entra ID fundamentals](/entra/fundamentals/whatis)
- Learn more about [Open ID Connect (OIDC) support in Microsoft Entra ID](/entra/architecture/auth-oidc)