---
title: Automigrations of PostgreSQL Single Servers with Private End Points
description: This article describes how to configure private end points for an automigrated Azure Database for PostgreSQL Flexible Server instance.
author: shriramm
ms.author: shriramm
ms.reviewer: hariramt, maghan
ms.date: 02/07/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: overview
ms.custom:
  - mvc
  - mode-api
---

# Automigrations of PostgreSQL single servers with private end points

[!INCLUDE [applies-to-postgresql-single-server](../includes/applies-to-postgresql-single-server.md)]

**Automigration** is a service-initiated migration that occurs during a planned maintenance window for a single server. After the migration, a flexible server is created with the same name as the original single server, with all data copied over. Additionally, existing connection strings automatically point to the newly migrated Flexible Server. [Learn More](./automigration-single-to-flexible-postgresql.md)

Running workloads on Single Server after March 28, 2025, poses security risks. The platform no longer receives security updates, bug fixes, or live support. To safeguard your workloads, Single Servers are **force-migrated** to Flexible Server instances in a phased manned using automigration.

## Eligibility for Force Migration of Single Servers with Private End Points

 - Single Servers with **Deny Public Network Access** set to **No** → Eligible for force migration. 
 - Single Servers with **Deny Public Network Access** set to **Yes** → Not Eligible for force migration.

## Handling Private End Points
Certain advanced features, such as Private Endpoints, can't be force-migrated automatically. This means:
 - Private Endpoints are not enabled on the automigrated Flexible Server.
 - You must manually configure Private Endpoints on the migrated Flexible Server to maintain business continuity. Follow these steps to configure a Private Endpoint on your Flexible Server with the same settings as your Single Server.

## Steps to configure Private End Points for an Automigrated Flexible Server
 1. Confirm that Flexible server with the same name as single server exists in the same subscription and resource group. This confirmation indicates that the automigration was successful. (Refer to the attached screenshots from Azure portal for reference).
 
 :::image type="content" source="media/automigration-private-end-point/automigration-singleserver.png" alt-text="Diagram that shows Single Server which was automigrated." lightbox="media/automigration-private-end-point/automigration-singleserver.png":::
 
 :::image type="content" source="media/automigration-private-end-point/automigration-flexibleserver.png" alt-text="Diagram that shows automigrated Flexible Server." lightbox="media/automigration-private-end-point/automigration-flexibleserver.png":::

 2. Delete the private end point associated with the Single Server using [Azure CLI](https://learn.microsoft.com/cli/azure/postgres/server/private-endpoint-connection?view=azure-cli-latest#az-postgres-server-private-endpoint-connection-delete) or by following steps in Azure portal.
 
 :::image type="content" source="media/automigration-private-end-point/singleserver-privateendpoint-setup.png" alt-text="Diagram that shows private end point on Single Server." lightbox="media/automigration-private-end-point/singleserver-privateendpoint-setup.png":::
 
 :::image type="content" source="media/automigration-private-end-point/singleserver-privateendpoint-delete.png" alt-text="Diagram that shows delete option on private end point on Single Server." lightbox="media/automigration-private-end-point/singleserver-privateendpoint-delete.png":::

 :::image type="content" source="media/automigration-private-end-point/privateendpoint-deletion.png" alt-text="Diagram that shows the deletion of private end point on Single Server." lightbox="media/automigration-private-end-point/privateendpoint-deletion.png":::

> [!IMPORTANT]  
> Ensure that the private end point associated with Single Server is deleted before proceeding with the next steps.

 3. Create a Private Endpoint on the automigrated Flexible Server using the same name and Private DNS zone as the Single Server. Use [Azure CLI](../flexible-server/how-to-networking-servers-deployed-public-access-add-private-endpoint.md?tabs=cli-add-private-endpoint-connection) or [Azure portal](../flexible-server/how-to-networking-servers-deployed-public-access-add-private-endpoint.md?tabs=portal-add-private-endpoint-connections). 

> [!NOTE]  
> You may see your Flexible Server in an **Updating** state when attempting to create a Private Endpoint. This issue occurs if the DNS record of your Single Server hasn't been released yet. One such cause is the Private Endpoint on the Single Server isn't deleted. If Private End Point on Single Server is still active, delete it.
> In some cases, even after deletion, the DNS record may take up to 5 hours to be fully released, especially in heavy regions like West Europe and East US. Please wait for the Private Endpoint to be created successfully before retrying.

 4. Ensure that the deployment completes successfully and that the private end point is attached to the Flexible server.

 :::image type="content" source="media/automigration-private-end-point/flexibleserver-privateendpoint.png" alt-text="Diagram that shows private end point attached to Flexible Server." lightbox="media/automigration-private-end-point/flexibleserver-privateendpoint.png":::

 5. After configuration, you should be able to connect to automigrated flexible server using the same connection strings as single server via the private end point. 

 :::image type="content" source="media/automigration-private-end-point/flexibleserver-connectivity.png" alt-text="Diagram successful connection via private end point on Flexible Server." lightbox="media/automigration-private-end-point/flexibleserver-connectivity.png":::

## Related content

- [Automigration of Azure Database for PostgreSQL Single Server to Flexible Server](../migrate/automigration-single-to-flexible-postgresql.md)  
- [Manage an Azure Database for postgresql - Flexible Server using the Azure portal.](../flexible-server/how-to-manage-server-portal.md)
