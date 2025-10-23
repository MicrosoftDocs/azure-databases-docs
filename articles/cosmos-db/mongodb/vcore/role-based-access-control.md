---
title: Role-based access control (RBAC)
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: Learn about the concepts of role-based access control in Azure Cosmos DB for MongoDB vCore.
author: niklarin
ms.author: nlarin
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: concept-article
ms.date: 10/21/2025
appliesto:
  - ✅ MongoDB (vCore)
---

# Role-based access control (RBAC) in Azure Cosmos DB for MongoDB vCore

Access control is a critical part of securing Azure Cosmos DB for MongoDB vCore clusters. Azure role-based access control (RBAC) provides a centralized mechanism to assign and enforce permissions through Microsoft Entra ID, ensuring that only authorized identities can perform operations on your clusters. Instead of relying on manual credential management, RBAC enables fine-grained, role-based assignments that scale with your environment. This approach simplifies governance, supports least-privilege principles, and makes auditing straightforward—helping organizations maintain operational integrity and compliance as deployments grow.

Managing access in Azure Cosmos DB for MongoDB vCore involves two distinct levels:

- [Managing permissions for the cluster as an Azure resource](#azure-role-based-access-control-rbac-for-clusters-as-azure-resources).
- [Managing permissions for databases and operations within the cluster](#role-based-access-control-rbac-for-the-database).

## Azure role-based access control (RBAC) for clusters as Azure resources

[Azure role-based access control (RBAC)](/azure/role-based-access-control/overview) is essential for managing access to Azure Cosmos DB for MongoDB vCore clusters. It provides a unified, secure, and scalable way to govern who can perform operations on your clusters. Through its integration with Microsoft Entra ID, RBAC provides centralized control over identities and access across Azure resources, helping maintain compliance with enterprise security standards. This approach eliminates the risks of unmanaged credentials and manual user provisioning, while offering fine-grained permissions for administrative, read-write, and read-only roles. For organizations running mission-critical workloads, RBAC delivers key benefits: enhanced security through least-privilege access, operational consistency across environments, and simplified governance for large-scale deployments. As your data estate grows, RBAC ensures that access policies remain consistent, auditable, and aligned with regulatory requirements—helping teams collaborate confidently without compromising data integrity.

Azure Cosmos DB for MongoDB vCore supports Azure RBAC for `mongoCluster` resource type. The following [actions](/azure/role-based-access-control/role-definitions#actions) for `mongoCluster` resource type are available in Azure RBAC for individual assignments and [custom RBAC role creation](/azure/role-based-access-control/custom-roles).

> [!div class="mx-tableFixed"]
> | Action | Description |
> | --- | --- |
> | Microsoft.DocumentDB/mongoClusters/read | Reads a `mongoCluster` resource or list all `mongoCluster` resources. |
> | Microsoft.DocumentDB/mongoClusters/write | Create or Update the properties or tags of the specified `mongoCluster` resource. |
> | Microsoft.DocumentDB/mongoClusters/delete | Deletes the specified `mongoCluster` resource. |
> | Microsoft.DocumentDB/mongoClusters/PrivateEndpointConnectionsApproval/action | Manage a private endpoint connection of `mongoCluster` resource |
> | Microsoft.DocumentDB/mongoClusters/listConnectionStrings/action | List connection strings for a given `mongoCluster` resource |
> | Microsoft.DocumentDB/mongoClusters/firewallRules/read | Reads a firewall rule or lists all firewall rules for the specified `mongoCluster` resource. |
> | Microsoft.DocumentDB/mongoClusters/firewallRules/write | Create or Update a firewall rule on a specified `mongoCluster` resource. |
> | Microsoft.DocumentDB/mongoClusters/firewallRules/delete | Deletes an existing firewall rule for the specified `mongoCluster` resource. |
> | Microsoft.DocumentDB/mongoClusters/privateEndpointConnectionProxies/read | Reads a private endpoint connection proxy for the specified `mongoCluster` resource. |
> | Microsoft.DocumentDB/mongoClusters/privateEndpointConnectionProxies/write | Create or Update a private endpoint connection proxy on a specified `mongoCluster` resource. |
> | Microsoft.DocumentDB/mongoClusters/privateEndpointConnectionProxies/delete | Deletes an existing private endpoint connection proxy for the specified `mongoCluster` resource. |
> | Microsoft.DocumentDB/mongoClusters/privateEndpointConnectionProxies/validate/action | Validates private endpoint connection proxy for the specified `mongoCluster` resource. |
> | Microsoft.DocumentDB/mongoClusters/privateEndpointConnections/read | Reads a private endpoint connection or lists all private endpoint connection for the specified `mongoCluster` resource. |
> | Microsoft.DocumentDB/mongoClusters/privateEndpointConnections/write | Create or Update a private endpoint connection on a specified `mongoCluster` resource. |
> | Microsoft.DocumentDB/mongoClusters/privateEndpointConnections/delete | Deletes an existing private endpoint connection for the specified `mongoCluster` resource. |
> | Microsoft.DocumentDB/mongoClusters/privateLinkResources/read | Reads a private link resource or lists all private link resource for the specified `mongoCluster` resource. |
> | Microsoft.DocumentDB/mongoClusters/users/read | Reads a user or lists all users for the specified `mongoCluster` resource. |
> | Microsoft.DocumentDB/mongoClusters/users/write | Create or Update a user on a specified `mongoCluster` resource. |
> | Microsoft.DocumentDB/mongoClusters/users/delete | Deletes an existing user for the specified `mongoCluster` resource. |

## Role-based access control (RBAC) for the database

Native DocumentDB administrative built-in user and [Entra ID administrative users](./entra-authentication.md#administrative-and-nonadministrative-access-for-microsoft-entra-id-principals) on the cluster have full read-write permissions on the cluster including full user management privileges. 

[Native DocumentDB non-administrative users](./secondary-users.md) and [Entra ID non-administrative users and security principals](./entra-authentication.md#administrative-and-nonadministrative-access-for-microsoft-entra-id-principals) are created and granted privileges at the cluster level for all databases on that cluster. The **readWriteAnyDatabase** and **clusterAdmin** roles together grant full read-write permissions on the cluster, including privileges for database management and database operations. The **readAnyDatabase** role is used to grant read-only permissions on the cluster.

 > [!NOTE]
>  Only full read-write users with database management and database operations privileges are supported. You can't assign **readWriteAnyDatabase** and **clusterAdmin** roles separately.

Non-administrative (secondary) users and security principals are granted the following limited *user management* permissions on the cluster:

| Security provider | Role | CreateUser | DeleteUser | UpdateUser | ListUser |
| --- | --- | --- | --- | --- | --- | 
| Entra ID | Read-write (readWriteAnyDatabase, clusterAdmin) | :x: | :x: | :x: | :heavy_check_mark: | 
| Entra ID | Read-only (readAnyDatabase) | :x: | :x: | :x: | :heavy_check_mark: | 
| Native DocumentDB | Read-write (readWriteAnyDatabase, clusterAdmin) | :x: | :x: | Only to change their own password | :heavy_check_mark: |
| Native DocumentDB | Read-only (readAnyDatabase) | :x: | :x: | Only to change their own password | :heavy_check_mark: |

## Related content

- Learn [how to enable Microsoft Entra ID and manage Entra ID users on clusters](./how-to-configure-entra-authentication.md)
- Learn [how to manage non-administrative (secondary) native DocumentDB users on clusters](./secondary-users.md)
