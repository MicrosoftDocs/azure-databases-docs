---
title: Migrate SSIS Packages to SQL Managed Instance
titleSuffix: Azure Database Migration Service
description: Learn how to migrate SQL Server Integration Services (SSIS) packages and projects to an Azure SQL Managed Instance using the Azure Database Migration Service or the Data Migration Assistant.
author: abhims14
ms.author: abhishekum
ms.reviewer: randolphwest
ms.date: 10/28/2025
ms.service: azure-database-migration-service
ms.topic: how-to
ms.collection:
  - sql-migration-content
ms.custom:
  - sfi-image-nochange
---

# Migrate SQL Server Integration Services packages to an Azure SQL Managed Instance

[!INCLUDE [deprecation-announcement-dms-classic-sql](includes/deprecation-announcement-dms-classic-sql.md)]

If you use SQL Server Integration Services (SSIS) and want to migrate your SSIS projects/packages from the source SSISDB hosted by SQL Server to the destination SSISDB hosted by an Azure SQL Managed Instance, you can use Azure Database Migration Service.

If the version of SSIS you use is earlier than 2012 or you use non-SSISDB package store types, before migrating your SSIS projects/packages, you need to convert them by using the Integration Services Project Conversion Wizard, which can also be launched from SQL Server Management Studio (SSMS). For more information, see the article [Converting projects to the project deployment model](/sql/integration-services/packages/deploy-integration-services-ssis-projects-and-packages#convert).

> [!NOTE]  
> Azure Database Migration Service (DMS) currently doesn't support Azure SQL Database as a target migration destination. To redeploy SSIS projects/packages to Azure SQL Database, see the article [Redeploy SSIS packages to Azure SQL Database with Azure Database Migration Service](how-to-migrate-ssis-packages.md).

In this article, you learn how to:

> [!div class="checklist"]
> - Assess source SSIS projects/packages.
> - Migrate SSIS projects/packages to Azure.

## Prerequisites

To complete these steps, you need:

- To create a Microsoft Azure Virtual Network for the Azure Database Migration Service by using the Azure Resource Manager deployment model, which provides site-to-site connectivity to your on-premises source servers by using either [ExpressRoute](/azure/expressroute/expressroute-introduction) or [VPN](/azure/vpn-gateway/vpn-gateway-about-vpngateways). For more information, see the article [Network topologies for SQL Managed Instance migrations using Azure Database Migration Service]( https://aka.ms/dmsnetworkformi). For more information about creating a virtual network, see the [Virtual Network Documentation](/azure/virtual-network/), and especially the quickstart articles with step-by-step details.

- To ensure that your virtual network Network Security Group (NSG) rules don't block the outbound port 443 of ServiceTag for ServiceBus, Storage and AzureMonitor. For more detail on virtual network NSG traffic filtering, see the article [Filter network traffic with network security groups](/azure/virtual-network/virtual-network-vnet-plan-design-arm).

- To configure your [Windows Firewall for source database engine access](/sql/database-engine/configure-windows/configure-a-windows-firewall-for-database-engine-access).

- To open your Windows Firewall to allow the Azure Database Migration Service to access the source SQL Server, which by default is TCP port 1433.

- If you're running multiple named SQL Server instances using dynamic ports, you might wish to enable the SQL Browser Service and allow access to UDP port 1434 through your firewalls so that the Azure Database Migration Service can connect to a named instance on your source server.

- If you're using a firewall appliance in front of your source databases, you might need to add firewall rules to allow the Azure Database Migration Service to access the source databases for migration, and files via SMB port 445.

- A SQL Managed Instance to host SSISDB. If you need to create one, follow the detail in the article [Create a Azure SQL Managed Instance](/azure/azure-sql/managed-instance/instance-create-quickstart).

- To ensure that the logins used to connect the source SQL Server and target managed instance are members of the sysadmin server role.

- To verify that SSIS is provisioned in Azure Data Factory (ADF) containing Azure-SSIS Integration Runtime (IR) with the destination SSISDB hosted by a SQL Managed Instance (as described in the article [Create the Azure-SSIS integration runtime in Azure Data Factory](/azure/data-factory/create-azure-ssis-integration-runtime)).

## Assess source SSIS projects/packages

Your SSIS projects/packages are assessed/validated as they're redeployed to the destination SSISDB hosted on an Azure SQL Managed Instance.

## Register the Microsoft.DataMigration resource provider

1. Sign in to the Azure portal, select **All services**, and then select **Subscriptions**.

   :::image type="content" source="media/how-to-migrate-ssis-packages-mi/portal-select-subscriptions.png" alt-text="Screenshot of Show portal subscriptions." lightbox="media/how-to-migrate-ssis-packages-mi/portal-select-subscriptions.png":::

1. Select the subscription in which you want to create the instance of Azure Database Migration Service, and then select **Resource providers**.

   :::image type="content" source="media/how-to-migrate-ssis-packages-mi/portal-select-resource-provider.png" alt-text="Screenshot of Show resource providers." lightbox="media/how-to-migrate-ssis-packages-mi/portal-select-resource-provider.png":::

1. Search for migration, and then to the right of **Microsoft.DataMigration**, select **Register**.

   :::image type="content" source="media/how-to-migrate-ssis-packages-mi/portal-register-resource-provider.png" alt-text="Screenshot of Register resource provider." lightbox="media/how-to-migrate-ssis-packages-mi/portal-register-resource-provider.png":::

## Create an Azure Database Migration Service instance

1. In the Azure portal, select + **Create a resource**, search for **Azure Database Migration Service**, and then select **Azure Database Migration Service** from the dropdown list.

   :::image type="content" source="media/how-to-migrate-ssis-packages-mi/portal-marketplace.png" alt-text="Screenshot of Azure Marketplace." lightbox="media/how-to-migrate-ssis-packages-mi/portal-marketplace.png":::

1. On the **Azure Database Migration Service** screen, select **Create**.

   :::image type="content" source="media/how-to-migrate-ssis-packages-mi/dms-create1.png" alt-text="Screenshot of Create Azure Database Migration Service instance." lightbox="media/how-to-migrate-ssis-packages-mi/dms-create1.png":::

1. On the **Create Migration Service** screen, specify a name for the service, the subscription, and a new or existing resource group.

1. Select the location in which you want to create the instance of DMS.

1. Select an existing virtual network or create one.

   The virtual network provides Azure Database Migration Service with access to the source SQL Server and target Azure SQL Managed Instance.

   For more information on how to create a virtual network in Azure portal, see the article [Create a virtual network using the Azure portal](/azure/virtual-network/quick-create-portal).

1. Select a pricing tier.

   For more information on costs and pricing tiers, see the [pricing page](https://aka.ms/dms-pricing).

   :::image type="content" source="media/how-to-migrate-ssis-packages-mi/dms-create-service2.png" alt-text="Screenshot of Create DMS Service.":::

1. Select **Create** to create the service.

## Create a migration project

After an instance of the service is created, locate it within the Azure portal, open it, and then create a new migration project.

1. In the Azure portal, select **All services**, search for Azure Database Migration Service, and then select **Azure Database Migration Services**.

   :::image type="content" source="media/how-to-migrate-ssis-packages-mi/dms-search.png" alt-text="Screenshot of Locate all instances of the Azure Database Migration Service.":::

1. On the **Azure Database Migration Service** screen, search for the name of the instance that you created, and then select the instance.

1. Select + **New Migration Project**.

1. On the **New migration project** screen, specify a name for the project, in the **Source server type** text box, select **SQL Server**, in the **Target server type** text box, select **Azure SQL Managed Instance**, and then for **Choose type of activity**, select **SSIS package migration**.

   :::image type="content" source="media/how-to-migrate-ssis-packages-mi/dms-create-project2.png" alt-text="Screenshot of Create DMS Project.":::

1. Select **Create** to create the project.

## Specify source details

1. On the **Migration source detail** screen, specify the connection details for the source SQL Server.

1. If you haven't installed a trusted certificate on your server, select the **Trust server certificate** check box.

   When a trusted certificate isn't installed, SQL Server generates a self-signed certificate when the instance is started. This certificate is used to encrypt the credentials for client connections.

   > [!CAUTION]  
   > TLS connections that are encrypted using a self-signed certificate doesn't provide strong security. They're susceptible to man-in-the-middle attacks. You shouldn't rely on TLS using self-signed certificates in a production environment or on servers that are connected to the internet.

   :::image type="content" source="media/how-to-migrate-ssis-packages-mi/dms-source-details1.png" alt-text="Screenshot of Source Details." lightbox="media/how-to-migrate-ssis-packages-mi/dms-source-details1.png":::

1. Select **Save**.

## Specify target details

1. On the **Migration target details** screen, specify the connection details for the target.

   :::image type="content" source="media/how-to-migrate-ssis-packages-mi/dms-target-details2.png" alt-text="Screenshot of Target details." lightbox="media/how-to-migrate-ssis-packages-mi/dms-target-details2.png":::

1. Select **Save**.

## Review the migration summary

1. On the **Migration summary** screen, in the **Activity name** text box, specify a name for the migration activity.

1. For the **SSIS projects and environments overwrite** option, specify whether to overwrite or ignore existing SSIS projects and environments.

   :::image type="content" source="media/how-to-migrate-ssis-packages-mi/dms-project-summary2.png" alt-text="Screenshot of Migration project summary." lightbox="media/how-to-migrate-ssis-packages-mi/dms-project-summary2.png":::

1. Review and verify the details associated with the migration project.

## Run the migration

- Select **Run migration**.

## Related content

- [Database Migration Guide](/data-migration/)
