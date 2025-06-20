---
title: Managed identities
description: Learn about Managed identities in Azure Database for PostgreSQL flexible server.
author: kabharati
ms.author: kabharati
ms.reviewer: maghan
ms.date: 01/12/2024
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: conceptual
ms.custom: sfi-image-nochange
#customer intent: As a user, I want to learn about how can I use the different types of managed identities in an Azure Database for PostgreSQL flexible server.
---

# Managed identities

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

A common challenge for developers is the management of secrets, credentials, certificates, and keys used to secure communication between services. Managed identities eliminate the need for developers to manage these credentials.

While developers can securely store the secrets in Azure Key Vault, services need a way to access Azure Key Vault. Managed identities provide an automatically managed identity in Microsoft Entra ID for applications to use when connecting to resources that support Microsoft Entra authentication. Applications can use managed identities to obtain Microsoft Entra tokens without having to manage any credentials.

Here are some of the benefits of using managed identities:

- You don't need to manage credentials. Credentials aren't even accessible to you.
- You can use managed identities to authenticate to any resource that supports Microsoft Entra authentication including your own applications.
- Managed identities can be used at no extra cost.

## Types of managed identities available in Azure

There are two types of managed identities:

- **System assigned**: Some Azure resource types, such as Azure Database for PostgreSQL flexible server, allow you to enable a managed identity directly on the resource. They're referred to as system assigned managed identities. When you enable a system assigned managed identity: 
    - A service principal of a special type is created in Microsoft Entra ID for the identity. The service principal is tied to the lifecycle of that Azure resource. When the Azure resource is deleted, Azure automatically deletes the service principal for you.
    - By design, only that Azure resource can use this identity to request tokens from Microsoft Entra ID.
    - You can authorize the service principal associated to the managed identity to have access to one or more services.
    - The name assigned to the service principal associated to the managed identity is always the same as the name of the Azure resource for which it's created.    

- **User assigned**: Some Azure resource types also support the assignment of managed identities created by the user as independent resources. The lifecycle of these identities is independent from the lifecycle of the resources to which they're assigned. They can be assigned to multiple resources. When you enable a user assigned managed identity:
    - A service principal of a special type is created in Microsoft Entra ID for the identity. The service principal is managed separately from the resources that use it. 
    - Multiple resources can utilize user assigned identities.
    - You authorize the managed identity to have access to one or more services.

## Uses of managed identities in Azure Database for PostgreSQL flexible server

**System assigned managed identity** for an Azure Database for PostgreSQL flexible server is used by:

- [azure_storage extension](concepts-storage-extension.md), when configured to access a storage account using the `managed-identity` authentication type. For more information, see how to [configure the azure_storage extension to use authorization with Microsoft Entra ID](how-to-use-pg-azure-storage.md#to-use-authorization-with-microsoft-entra-id).
- [Microsoft Fabric mirrored databases from Azure Database for PostgreSQL flexible server (preview)](https://techcommunity.microsoft.com/blog/adforpostgresql/mirroring-azure-database-for-postgresql-flexible-server-in-microsoft-fabric---pr/4251876) uses the credentials of the system assigned managed identity to sign the requests that your instance of flexible server sends to the Azure DataLake service in Microsoft Fabric to mirror your designated databases.

**User assigned managed identities** configured for an Azure Database for PostgreSQL flexible server can be used for:

- [Data encryption with customer managed keys](concepts-data-encryption.md).

## Related content

- [Configure system or user assigned managed identities in Azure Database for PostgreSQL flexible server](how-to-configure-managed-identities.md).
- [Firewall rules in Azure Database for PostgreSQL flexible server](concepts-firewall-rules.md).
- [Public access and private endpoints in Azure Database for PostgreSQL flexible server](concepts-networking-public.md).
- [Virtual network integration in Azure Database for PostgreSQL flexible server](concepts-networking-private.md).
