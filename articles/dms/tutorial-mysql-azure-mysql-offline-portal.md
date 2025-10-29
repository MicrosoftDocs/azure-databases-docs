---
title: "Tutorial: Migrate MySQL to Azure Database for MySQL Offline Using DMS"
titleSuffix: Azure Database Migration Service
description: Learn to perform an offline migration from MySQL on-premises to Azure Database for MySQL by using Azure Database Migration Service.
author: saikondapalli11
ms.author: skondapalli
ms.reviewer: arthiaga, randolphwest
ms.date: 10/28/2025
ms.service: azure-database-migration-service
ms.topic: tutorial
ms.collection:
  - sql-migration-content
ms.custom:
  - sfi-image-nochange
---

# Tutorial: Migrate MySQL to Azure Database for MySQL offline using DMS

You can use Azure Database Migration Service to perform a seamless migration from your external MySQL instance to [Azure Database for MySQL](../mysql/index.yml) with high speed data migration capability. In this tutorial, we migrate a sample database from an on-premises instance of MySQL 5.7 to Azure Database for MySQL (v5.7) by using an offline migration activity in Azure Database Migration Service. Although the articles assume the source to be a MySQL database instance and target to be Azure Database for MySQL, it can be used to migrate from one Azure Database for MySQL to another just by changing the source server name and credentials. Also, migration from lower version MySQL servers (v5.6 and later versions) to higher versions is also supported.

> [!NOTE]  
> For a PowerShell-based scriptable version of this migration experience, see [scriptable offline migration to Azure Database for MySQL](migrate-mysql-to-azure-mysql-powershell.md).

Amazon Relational Database Service (RDS) for MySQL and Amazon Aurora (MySQL-based) are also supported as sources for migration.

In this tutorial, you learn how to:

> [!div class="checklist"]
> - Create a DMS instance.
> - Create a MySQL migration project in DMS.
> - Migrate a MySQL schema using DMS.
> - Run the migration.
> - Monitor the migration.

## Prerequisites

To complete this tutorial, you need to:

- Have an Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/free).

- Have an on-premises MySQL database with version 5.7. If not, then download and install [MySQL community edition](https://dev.mysql.com/downloads/mysql/) 5.7.

- Create a Microsoft Azure Virtual Network for Azure Database Migration Service by using Azure Resource Manager deployment model, which provides site-to-site connectivity to your on-premises source servers by using either [ExpressRoute](/azure/expressroute/expressroute-introduction) or [VPN](/azure/vpn-gateway/vpn-gateway-about-vpngateways). For more information about creating a virtual network, see the [Virtual Network Documentation](/azure/virtual-network/), and especially the quickstart articles with step-by-step details.

  During virtual networkNet setup, if you use ExpressRoute with network peering to Microsoft, add the following service [endpoints](/azure/virtual-network/virtual-network-service-endpoints-overview) to the subnet in which the service will be provisioned:

  - Target database endpoint (for example, SQL endpoint, Azure Cosmos DB endpoint, and so on)
  - Storage endpoint
  - Service bus endpoint

  This configuration is necessary because Azure Database Migration Service lacks internet connectivity.

- Ensure that your virtual network Network Security Group rules don't block the outbound port 443 of ServiceTag for ServiceBus, Storage, and AzureMonitor. For more detail on virtual network NSG traffic filtering, see the article [Filter network traffic with network security groups](/azure/virtual-network/virtual-network-vnet-plan-design-arm).

- Open Windows Firewall to allow connections from Virtual Network for Azure Database Migration Service to access the source MySQL Server, which by default is TCP port 3306.

- When using a firewall appliance in front of your source databases, you might need to add firewall rules to allow connections from Virtual Network for Azure Database Migration Service to access the source databases for migration.

- Create a server-level [firewall rule](/azure/azure-sql/database/firewall-configure) or [configure virtual network service endpoints](../mysql/howto-manage-vnet-using-portal.md) for target Azure Database for MySQL to allow Virtual Network for Azure Database Migration Service access to the target databases.

- The source MySQL must be on supported MySQL community edition. To determine the version of MySQL instance, in the MySQL utility or MySQL Workbench, run the following command:

  ```sql
  SELECT @@VERSION;
  ```

- Azure Database for MySQL supports only InnoDB tables. To convert MyISAM tables to InnoDB, see the article [Converting Tables from MyISAM to InnoDB](https://dev.mysql.com/doc/refman/5.7/en/converting-tables-to-innodb.html)
- The user must have the privileges to read data on the source database.
- To complete a schema migration successfully, on the source server, the user performing the migration requires the following privileges:
  - [SELECT](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#priv_select) privilege at the server level on the source.
  - If migrating views, user must have the [SHOW VIEW](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#priv_show-view) privilege on the source server and the [CREATE VIEW](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#priv_create-view) privilege on the target server.
  - If migrating triggers, user must have the [TRIGGER](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#priv_trigger) privilege on the source and target server.
  - If migrating routines (procedures and/or functions), the user must have the [CREATE ROUTINE](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#priv_create-routine) and [ALTER ROUTINE](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#priv_alter-routine) privileges granted at the server level on the target.
  - If migrating events, the user must have the [EVENT](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#priv_event) privilege on the source and target server.
  - If migrating users/logins, the user must have the [CREATE USER](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#priv_create-user) privilege on the target server.
  - [DROP](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#priv_drop) privilege at the server level on the target, in order to drop tables that might already exist. For example, when retrying a migration.
  - [REFERENCES](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#priv_references) privilege at the server level on the target, in order to create tables with foreign keys.
  - If migrating to MySQL 8.0, the user must have the [SESSION_VARIABLES_ADMIN](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#priv_session-variables-admin) privilege on the target server.
  - [CREATE](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#priv_create) privilege at the server level on the target.
  - [INSERT](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#priv_insert) privilege at the server level on the target.
  - [UPDATE](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#priv_update) privilege at the server level on the target.
  - [DELETE](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#priv_delete) privilege at the server level on the target.

<a id="sizing-the-target-azure-database-for-mysql-instance"></a>

## Size the target Azure Database for MySQL instance

To prepare the target Azure Database for MySQL server for faster data loads using the Azure Database Migration Service, the following server parameters and configuration changes are recommended.

- `max_allowed_packet` – set to 1073741824 (that is, 1 GB) to prevent any connection issues due to large rows.

- `slow_query_log` – set to `OFF` to turn off the slow query log. This eliminates the overhead caused by slow query logging during data loads.

- `query_store_capture_mode` – set to `NONE` to turn off the Query Store. This eliminates the overhead caused by sampling activities by Query Store.

- `innodb_buffer_pool_size` – Innodb_buffer_pool_size can only be increased by scaling up compute for Azure Database for MySQL server. Scale up the server to 64 vCore General Purpose SKU from the Pricing tier of the portal during migration to increase the `innodb_buffer_pool_size`.

- `innodb_io_capacity` and `innodb_io_capacity_max` - Change to `9000` from the Server parameters in Azure portal to improve the IO utilization to optimize for migration speed.

- `innodb_write_io_threads` and `innodb_write_io_threads` - Change to `4` from the Server parameters in Azure portal to improve the speed of migration.

- Scale up Storage tier – The IOPs for Azure Database for MySQL server increases progressively with the increase in storage tier.
  - In the Flexible Server deployment option, we recommend you can scale (increase or decrease) IOPS irrespective of the storage size.
  - Storage size can only be scaled up, not down.

- Select the compute size and compute tier for the target flexible server based on the source MySQL server's configuration.

  <sup>1</sup> For the migration, as a best practice, select General Purpose 16 vCores compute or higher for the target flexible server for faster migrations. Scale back to the desired compute size for the target server after migration is complete.

Once the migration is complete, you can revert back the server parameters and configuration to values required by your workload.

## Set up DMS

With your target flexible server deployed and configured, you next need to set up DMS to migrate your MySQL server to a flexible server.

### Register the resource provider

To register the Microsoft.DataMigration resource provider, perform the following steps.

1. Before you create your first DMS instance, sign in to the Azure portal, and then search for and select **Subscriptions**.

   :::image type="content" source="media/tutorial-azure-mysql-single-to-flex-online/1-subscriptions.png" alt-text="Screenshot of a Select subscriptions from Azure Marketplace." lightbox="media/tutorial-azure-mysql-single-to-flex-online/1-subscriptions.png":::

1. Select the subscription that you want to use to create the DMS instance, and then select **Resource providers**.

   :::image type="content" source="media/tutorial-azure-mysql-single-to-flex-online/2-resource-provider.png" alt-text="Screenshot of a Select Resource Provider." lightbox="media/tutorial-azure-mysql-single-to-flex-online/2-resource-provider.png":::

1. Search for the term "Migration", and then, for **Microsoft.DataMigration**, select **Register**.

   :::image type="content" source="media/tutorial-azure-mysql-single-to-flex-online/3-register.png" alt-text="Screenshot of a Register your resource provider.":::

## Create a Database Migration Service instance

1. In the Azure portal, select + **Create a resource**, search for Azure Database Migration Service, and then select **Azure Database Migration Service** from the dropdown list.

   :::image type="content" source="media/tutorial-mysql-to-azure-mysql-offline-portal/03-dms-portal-marketplace.png" alt-text="Screenshot of Azure Marketplace." lightbox="media/tutorial-mysql-to-azure-mysql-offline-portal/03-dms-portal-marketplace.png":::

1. On the **Azure Database Migration Service** screen, select **Create**.

   :::image type="content" source="media/tutorial-mysql-to-azure-mysql-offline-portal/04-dms-portal-marketplace-create.png" alt-text="Screenshot of Create Azure Database Migration Service instance." lightbox="media/tutorial-mysql-to-azure-mysql-offline-portal/04-dms-portal-marketplace-create.png":::

1. On the **Create Migration Service** screen, specify a name for the service, the subscription, and a new or existing resource group.

1. Select a pricing tier and move to the networking screen. Offline migration capability is available only on the Premium pricing tier.

   For more information on costs and pricing tiers, see the [pricing page](https://aka.ms/dms-pricing).

   :::image type="content" source="media/tutorial-mysql-to-azure-mysql-offline-portal/05-dms-portal-create-basic.png" alt-text="Screenshot of Configure Azure Database Migration Service basic settings." lightbox="media/tutorial-mysql-to-azure-mysql-offline-portal/05-dms-portal-create-basic.png":::

1. Select an existing virtual network from the list or provide the name of new virtual network to be created. Move to the review + create screen. Optionally you can add tags to the service using the tags screen.

   The virtual network provides Azure Database Migration Service with access to the source SQL Server and the target Azure SQL Database instance.

   :::image type="content" source="media/tutorial-mysql-to-azure-mysql-offline-portal/06-dms-portal-create-networking.png" alt-text="Screenshot of Configure Azure Database Migration Service network settings." lightbox="media/tutorial-mysql-to-azure-mysql-offline-portal/06-dms-portal-create-networking.png":::

   For more information about how to create a virtual network in the Azure portal, see the article [Create a virtual network using the Azure portal](/azure/virtual-network/quick-create-portal).

1. Review the configurations and select **Create** to create the service.

   :::image type="content" source="media/tutorial-mysql-to-azure-mysql-offline-portal/07-dms-portal-create-submit.png" alt-text="Screenshot of Azure Database Migration Service create." lightbox="media/tutorial-mysql-to-azure-mysql-offline-portal/07-dms-portal-create-submit.png":::

## Create a migration project

After the service is created, locate it within the Azure portal, open it, and then create a new migration project.

1. In the Azure portal, select **All services**, search for Azure Database Migration Service, and then select **Azure Database Migration Services**.

   :::image type="content" source="media/tutorial-mysql-to-azure-mysql-offline-portal/08-01-dms-portal-search-service.png" alt-text="Screenshot of Locate all instances of Azure Database Migration Service." lightbox="media/tutorial-mysql-to-azure-mysql-offline-portal/08-01-dms-portal-search-service.png":::

1. Select your migration service instance from the search results and select + **New Migration Project**.

   :::image type="content" source="media/tutorial-mysql-to-azure-mysql-offline-portal/08-02-dms-portal-new-project.png" alt-text="Screenshot of Create a new migration project." lightbox="media/tutorial-mysql-to-azure-mysql-offline-portal/08-02-dms-portal-new-project.png":::

1. On the **New migration project** screen, specify a name for the project, in the **Source server type** selection box, select **MySQL**, in the **Target server type** selection box, select **Azure Database For MySQL** and in the **Migration activity type** selection box, select **Data migration**. Select **Create and run activity**.

   :::image type="content" source="media/tutorial-mysql-to-azure-mysql-offline-portal/09-dms-portal-project-mysql-create.png" alt-text="Screenshot of Create Database Migration Service Project." lightbox="media/tutorial-mysql-to-azure-mysql-offline-portal/09-dms-portal-project-mysql-create.png":::

   Alternately, you can choose **Create project only** to create the migration project now and execute the migration later.

## Configure migration project

1. On the **Select source** screen, specify the connection details for the source MySQL instance, and select **Next: Select target >>**

   :::image type="content" source="media/tutorial-mysql-to-azure-mysql-offline-portal/10-dms-portal-project-mysql-source.png" alt-text="Screenshot of Add source details screen." lightbox="media/tutorial-mysql-to-azure-mysql-offline-portal/10-dms-portal-project-mysql-source.png":::

1. On the **Select target** screen, specify the connection details for the target Azure Database for MySQL instance, and select **Next: Select databases >>**

   :::image type="content" source="media/tutorial-mysql-to-azure-mysql-offline-portal/11-dms-portal-project-mysql-target.png" alt-text="Screenshot of Add target details screen." lightbox="media/tutorial-mysql-to-azure-mysql-offline-portal/11-dms-portal-project-mysql-target.png":::

1. On the **Select databases** screen, map the source and the target database for migration, and select **Next: Configure migration settings >>**. You can select the **Make Source Server Read Only** option to make the source as read-only, but be cautious that this is a server level setting. If selected, it sets the entire server to read-only, not just the selected databases.

   If the target database contains the same database name as the source database, Azure Database Migration Service selects the target database by default.

   :::image type="content" source="media/tutorial-mysql-to-azure-mysql-offline-portal/12-dms-portal-project-mysql-select-db.png" alt-text="Screenshot of Select database details screen." lightbox="media/tutorial-mysql-to-azure-mysql-offline-portal/12-dms-portal-project-mysql-select-db.png":::

1. On the **Configure migration settings** screen, select the tables to be part of migration, and select **Next: Summary >>**. If the target tables have any data, they aren't selected by default but you can explicitly select them and they're truncated before starting the migration.

   :::image type="content" source="media/tutorial-mysql-to-azure-mysql-offline-portal/13-dms-portal-project-mysql-select-tbl.png" alt-text="Screenshot of Select tables screen." lightbox="media/tutorial-mysql-to-azure-mysql-offline-portal/13-dms-portal-project-mysql-select-tbl.png":::

1. On the **Summary** screen, in the **Activity name** text box, specify a name for the migration activity and review the summary to ensure that the source and target details match what you previously specified.

   :::image type="content" source="media/tutorial-mysql-to-azure-mysql-offline-portal/14-dms-portal-project-mysql-activity-summary.png" alt-text="Screenshot of Migration project summary." lightbox="media/tutorial-mysql-to-azure-mysql-offline-portal/14-dms-portal-project-mysql-activity-summary.png":::

1. Select **Start migration**. The migration activity window appears, and the **Status** of the activity is **Initializing**. The **Status** changes to **Running** when the table migrations start.

   :::image type="content" source="media/tutorial-mysql-to-azure-mysql-offline-portal/15-dms-portal-project-mysql-running.png" alt-text="Screenshot of Running migration." lightbox="media/tutorial-mysql-to-azure-mysql-offline-portal/15-dms-portal-project-mysql-running.png":::

## Monitor the migration

1. On the migration activity screen, select **Refresh** to update the display and see progress about number of tables completed.

1. You can select the database name on the activity screen to see the status of each table as they're getting migrated. Select **Refresh** to update the display.

   :::image type="content" source="media/tutorial-mysql-to-azure-mysql-offline-portal/16-dms-portal-project-mysql-monitor.png" alt-text="Screenshot of Monitoring migration." lightbox="media/tutorial-mysql-to-azure-mysql-offline-portal/16-dms-portal-project-mysql-monitor.png":::

## Complete the migration

1. On the migration activity screen, select **Refresh** to update the display until the **Status** of the migration shows as **Complete**.

   :::image type="content" source="media/tutorial-mysql-to-azure-mysql-offline-portal/17-dms-portal-project-mysql-complete.png" alt-text="Screenshot of Complete migration." lightbox="media/tutorial-mysql-to-azure-mysql-offline-portal/17-dms-portal-project-mysql-complete.png":::

## Post migration activities

Migration cutover in an offline migration is an application dependent process that is out of scope for this document, but the following post-migration activities are prescribed:

1. Create logins, roles, and permissions as per the application requirements.
1. Recreate all the triggers on the target database as extracted during the premigration step.
1. Perform sanity testing of the application against the target database to certify the migration.

## Clean up resources

If you're not going to continue to use the Database Migration Service, then you can delete the service with the following steps:

1. In the Azure portal, select **All services**, search for Azure Database Migration Service, and then select **Azure Database Migration Services**.

   :::image type="content" source="media/tutorial-mysql-to-azure-mysql-offline-portal/08-01-dms-portal-search-service.png" alt-text="Screenshot of Locate all instances of DMS." lightbox="media/tutorial-mysql-to-azure-mysql-offline-portal/08-01-dms-portal-search-service.png":::

1. Select your migration service instance from the search results and select **Delete Service**.

   :::image type="content" source="media/tutorial-mysql-to-azure-mysql-offline-portal/18-dms-portal-delete.png" alt-text="Screenshot of Delete the migration service." lightbox="media/tutorial-mysql-to-azure-mysql-offline-portal/18-dms-portal-delete.png":::

1. On the confirmation dialog, type in the name of the service in the **TYPE THE DATABASE MIGRATION SERVICE NAME** textbox and select **Delete**.

   :::image type="content" source="media/tutorial-mysql-to-azure-mysql-offline-portal/19-dms-portal-deleteconfirm.png" alt-text="Screenshot of Confirm migration service delete.":::

## Related content

- [Troubleshoot common Azure Database Migration Service (classic) issues and errors](known-issues-troubleshooting-dms.md)
- [Troubleshoot DMS errors when connecting to source databases](known-issues-troubleshooting-dms-source-connectivity.md)
- [What is Azure Database Migration Service?](dms-overview.md)
- [What is Azure Database for MySQL?](../mysql/overview.md)
- [Migrate MySQL to Azure Database for MySQL offline with PowerShell & Azure Database Migration Service](migrate-mysql-to-azure-mysql-powershell.md)
