---
title: Automigrations of Azure Database for PostgreSQL - Single Server with Private End Points
description: This article describes how to configure private end points for an automigrated Azure Database for PostgreSQL Flexible Server instance.
author: shriramm
ms.author: shriramm
ms.reviewer: hariramt, maghan
ms.date: 03/28/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: conceptual
ms.custom: "Remove in June 2025"
---

# Automigrations of Azure Database for PostgreSQL - Single Server with private end points

[!INCLUDE [applies-to-postgresql-single-server](../includes/applies-to-postgresql-single-server.md)]

[!INCLUDE [single-server-retired](includes/single-server-retired.md)]

**Automigration** is a service-initiated migration that occurs during a planned maintenance window for a single server deployment. After the migration, a flexible server is created with the same name as the original single server deployment, with all data copied over. Additionally, existing connection strings automatically point to the newly migrated Flexible Server. [Learn More](./automigration-single-to-flexible-postgresql.md)

Workloads on a single server deployment after March 28, 2025, poses security risks. The platform no longer receives security updates, bug fixes, or live support. To safeguard your workloads, single server deployments are **force-migrated** to flexible server instances using automigration.

## Eligibility for force migration of single server deployments with Private End Points

- single server deployments with **Deny Public Network Access** set to **No** → Eligible for force migration.
- single server deployments with **Deny Public Network Access** set to **Yes** → Not Eligible for force migration.

## Handling Private End Points

Certain advanced features, such as Private Endpoints, can't be force-migrated automatically. This means:
- Private Endpoints aren't enabled on the automigrated Flexible Server.
- You must manually configure Private Endpoints on the migrated Flexible Server to maintain business continuity. Follow these steps to configure a Private Endpoint on your Flexible Server with the same settings as your single server deployment.

## Steps to configure Private End Points for an Automigrated Flexible Server

1. Confirm that the flexible server deployment has the same name as the single server deployment in the same subscription and resource group. This confirmation indicates that the automigration was successful. (Refer to the attached screenshots from Azure portal for reference).

    :::image type="content" source="media/automigration-private-end-point/automigration-single-server.png" alt-text="Diagram that shows single server deployment which was automigrated." lightbox="media/automigration-private-end-point/automigration-single-server.png":::
    
    :::image type="content" source="media/automigration-private-end-point/automigration-flexible-server.png" alt-text="Diagram that shows automigrated Flexible Server." lightbox="media/automigration-private-end-point/automigration-flexible-server.png":::

1. Delete the private endpoint associated with the single server deployment using [Azure CLI](/cli/azure/postgres/server/private-endpoint-connection#az-postgres-server-private-endpoint-connection-delete) or by following steps in Azure portal.

    :::image type="content" source="media/automigration-private-end-point/single-server-private-endpoint-setup.png" alt-text="Diagram that shows private end point on single server deployment." lightbox="media/automigration-private-end-point/single-server-private-endpoint-setup.png":::
    
    :::image type="content" source="media/automigration-private-end-point/single-server-private-endpoint-delete.png" alt-text="Diagram that shows delete option on private end point on single server deployment." lightbox="media/automigration-private-end-point/single-server-private-endpoint-delete.png":::
    
    :::image type="content" source="media/automigration-private-end-point/private-endpoint-deletion.png" alt-text="Diagram that shows the deletion of private end point on single server deployment." lightbox="media/automigration-private-end-point/private-endpoint-deletion.png":::
    
    > [!IMPORTANT]  
    > Ensure that the private endpoint associated with single server deployment is deleted before proceeding with the next steps.
    
1. Create a Private Endpoint on the automigrated Flexible Server using the same name and Private DNS zone as the single server deployment. Use [Azure CLI](../flexible-server/how-to-networking-servers-deployed-public-access-add-private-endpoint.md?tabs=cli-add-private-endpoint-connection) or [Azure portal](../flexible-server/how-to-networking-servers-deployed-public-access-add-private-endpoint.md?tabs=portal-add-private-endpoint-connections).

    > [!NOTE]  
    > You might see your Flexible Server in an **Updating** state when attempting to create a Private Endpoint. This issue occurs if the DNS record of your single server deployment hasn't been released yet. One such cause is the Private Endpoint on the single server deployment isn't deleted. If Private Endpoint on single server deployment is still active, delete it.
    > In some cases, even after deletion, the DNS record might take up to 5 hours to be fully released, especially in heavy regions like West Europe and East US. Wait for the Private Endpoint to be created successfully before retrying.
    
1. Ensure that the deployment completes successfully and that the private endpoint is attached to the Flexible server.

    :::image type="content" source="media/automigration-private-end-point/flexible-server-private-endpoint.png" alt-text="Diagram that shows private end point attached to Flexible Server." lightbox="media/automigration-private-end-point/flexible-server-private-endpoint.png":::
    
1. After configuration, you should be able to connect to automigrated flexible server using the same connection strings as single server deployment via the private endpoint.

    :::image type="content" source="media/automigration-private-end-point/flexible-server-connectivity.png" alt-text="Diagram successful connection via private end point on Flexible Server." lightbox="media/automigration-private-end-point/flexible-server-connectivity.png":::
    
## Related content

- [Automigration of Azure Database for PostgreSQL single server deployment to Flexible Server](../migrate/automigration-single-to-flexible-postgresql.md)
- [Manage an Azure Database for postgresql - Flexible Server using the Azure portal.](../flexible-server/how-to-manage-server-portal.md)
