---
title: "Tutorial: Migrate MongoDB Offline to Azure Cosmos DB for MongoDB"
titleSuffix: Azure Database Migration Service
description: Migrate from MongoDB on-premises to Azure Cosmos DB for MongoDB offline via Azure Database Migration Service.
author: sandeepsnairms
ms.author: sandnair
ms.reviewer: sidandrews, randolphwest
ms.date: 10/16/2025
ms.service: azure-database-migration-service
ms.topic: tutorial
ms.collection:
  - sql-migration-content
ms.custom:
  - ignite-2023
  - sfi-image-nochange
---

# Tutorial: Migrate MongoDB to Azure Cosmos DB for MongoDB offline using Azure Database Migration Service

[!INCLUDE [appliesto-mongodb-api](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb.md)]

This MongoDB migration guide is part of series on MongoDB migration. The critical MongoDB migration steps are [pre-migration](../cosmos-db/mongodb-pre-migration.md), migration, and [post-migration](../cosmos-db/mongodb-post-migration.md), as shown below.

:::image type="content" source="~/reusable-content/ce-skilling/azure/media/cosmos-db/overall-migration-steps.png" alt-text="Diagram of migration steps.":::

## Overview of offline data migration from MongoDB to Azure Cosmos DB using DMS

Use Azure Database Migration Service to perform an offline, one-time migration of databases from an on-premises or cloud instance of MongoDB to Azure Cosmos DB for MongoDB.

In this tutorial, you learn how to:
> [!div class="checklist"]
> - Create an instance of Azure Database Migration Service.
> - Create a migration project by using Azure Database Migration Service.
> - Run the migration.
> - Monitor the migration.

In this tutorial, you migrate a dataset in MongoDB that is hosted in an Azure virtual machine. By using Azure Database Migration Service, you migrate the dataset to Azure Cosmos DB for MongoDB. If you don't have a MongoDB source set up already, see [Install and configure MongoDB on a Windows VM in Azure](/previous-versions/azure/virtual-machines/windows/install-mongodb).

## Prerequisites

To complete this tutorial, you need to:

- [Complete the pre-migration](../cosmos-db/mongodb-pre-migration.md) steps, such as estimating throughput and choosing a partition key.
- [Create an account for the Azure Cosmos DB for MongoDB](https://portal.azure.com/#create/Microsoft.DocumentDB).

  > [!NOTE]  
  > DMS is currently not supported if you're migrating to an Azure Cosmos DB for MongoDB account that is provisioned with serverless mode.

- Create a Microsoft Azure Virtual Network for Azure Database Migration Service by using Azure Resource Manager. This deployment model provides site-to-site connectivity to your on-premises source servers by using either [Azure ExpressRoute](/azure/expressroute/expressroute-introduction) or [VPN](/azure/vpn-gateway/vpn-gateway-about-vpngateways). For more information about creating a virtual network, see the [Azure Virtual Network documentation](/azure/virtual-network/), especially the "quickstart" articles with step-by-step details.

  During virtual network setup, if you use ExpressRoute with network peering to Microsoft, add the following service [endpoints](/azure/virtual-network/virtual-network-service-endpoints-overview) to the subnet in which the service will be provisioned:

  - Target database endpoint (for example, SQL endpoint or Azure Cosmos DB endpoint)
  - Storage endpoint
  - Service bus endpoint

  This configuration is necessary because Azure Database Migration Service lacks internet connectivity.

- Ensure that your network security group (NSG) rules for your virtual network don't block the following communication ports: 53, 443, 445, 9354, and 10000-20000. For more information, see [Filter network traffic with network security groups](/azure/virtual-network/virtual-network-vnet-plan-design-arm).
- Open your Windows Firewall to allow Azure Database Migration Service to access the source MongoDB server, which by default is TCP port 27017.
- When you're using a firewall appliance in front of your source database, you might need to add firewall rules to allow Azure Database Migration Service to access the source database for migration.

## Configure the Server Side Retry feature

You can benefit from resource governance capabilities if you migrate from MongoDB to Azure Cosmos DB. With these capabilities, you can make full use of your provisioned request units (RU/s) of throughput. Azure Cosmos DB might throttle a particular Database Migration Service request in the course of migration, if that request exceeds the container-provisioned RU/s. Then that request needs to be retried.

Database Migration Service is capable of performing retries. It's important to understand that the round-trip time involved in the network hop between Database Migration Service and Azure Cosmos DB affects the overall response time of that request. Improving response time for throttled requests can shorten the total time needed for migration.

The Server Side Retry feature of Azure Cosmos DB allows the service to intercept throttle error codes and retry with a much lower round-trip time, dramatically improving request response times.

To use Server Side Retry, in the Azure Cosmos DB portal, select **Features** > **Server Side Retry**.

:::image type="content" source="~/reusable-content/ce-skilling/azure/media/dms/mongo-server-side-retry-feature.png" alt-text="Screenshot that shows where to find the Server Side Retry feature.":::

If the feature is disabled, select **Enable**.

:::image type="content" source="~/reusable-content/ce-skilling/azure/media/dms/mongo-server-side-retry-enable.png" alt-text="Screenshot that shows how to enable Server Side Retry.":::

[!INCLUDE [resource-provider-register](includes/database-migration-service-resource-provider-register.md)]

## Create an instance

1. In the Azure portal, select + **Create a resource**, search for Azure Database Migration Service, and then select **Azure Database Migration Service** from the dropdown list.

   :::image type="content" source="media/tutorial-mongodb-to-cosmosdb/portal-marketplace.png" alt-text="Screenshot that shows Azure Marketplace." lightbox="media/tutorial-mongodb-to-cosmosdb/portal-marketplace.png":::

1. On the **Azure Database Migration Service** screen, select **Create**.

   :::image type="content" source="media/tutorial-mongodb-to-cosmosdb/dms-create1.png" alt-text="Screenshot that shows how to create an instance of Azure Database Migration Service." lightbox="media/tutorial-mongodb-to-cosmosdb/dms-create1.png":::

1. On **Create Migration Service**, specify a name for the service, the subscription, and a new or existing resource group.

1. Select the location in which you want to create the instance of Azure Database Migration Service.

1. Select an existing virtual network or create a new one.

   The virtual network provides Azure Database Migration Service with access to the source MongoDB instance and the target Azure Cosmos DB account.

   For more information about how to create a virtual network in the Azure portal, see [Create a virtual network by using the Azure portal](/azure/virtual-network/quick-create-portal).

1. Select a pricing tier.

   For more information on costs and pricing tiers, see the [pricing page](https://aka.ms/dms-pricing).

   :::image type="content" source="media/tutorial-mongodb-to-cosmosdb/dms-settings2.png" alt-text="Screenshot that shows configuration settings for the instance of Azure Database Migration Service.":::

1. Select **Create** to create the service.

## Create a migration project

After you create the service, locate it within the Azure portal, and open it. Then create a new migration project.

1. In the Azure portal, select **All services**, search for Azure Database Migration Service, and then select **Azure Database Migration Services**.

   :::image type="content" source="media/tutorial-mongodb-to-cosmosdb/dms-search.png" alt-text="Screenshot that shows how to locate all instances of Azure Database Migration Service.":::

1. On the **Azure Database Migration Services** screen, search for the name of Azure Database Migration Service instance that you created, and then select the instance.

1. Select **+ New Migration Project**.

1. On **New migration project**, specify a name for the project, and in the **Source server type** text box, select **MongoDB**. In the **Target server type** text box, select **Azure Cosmos DB for NoSQL**, and then for **Choose type of activity**, select **Offline data migration**.

   :::image type="content" source="media/tutorial-mongodb-to-cosmosdb/dms-create-project.png" alt-text="Screenshot that shows project options.":::

1. Select **Create and run activity** to create the project and run the migration activity.

## Specify source details

1. On the **Source details** screen, specify the connection details for the source MongoDB server.

   > [!IMPORTANT]  
   > Azure Database Migration Service doesn't support Azure Cosmos DB as a source.

   There are three modes to connect to a source:

   - **Standard mode**, which accepts a fully qualified domain name or an IP address, port number, and connection credentials.

   - **Connection string mode**, which accepts a MongoDB connection string as described in [Connection String URI Format](https://www.mongodb.com/docs/manual/reference/connection-string).

   - **Data from Azure storage**, which accepts a blob container SAS URL. Select **Blob contains BSON dumps** if the blob container has BSON dumps produced by the MongoDB [bsondump tool](https://www.mongodb.com/docs/database-tools/bsondump). Don't select this option if the container contains JSON files.

     If you select this option, be sure that the storage account connection string appears in the following format:

     ```output
     https://blobnameurl/container?SASKEY
     ```

     You can find this blob container SAS connection string in Azure Storage explorer. Creating the SAS for the concerned container provides you with the URL in the requested format.

     Also, based on the type dump information in Azure Storage, keep the following in mind:

     - For BSON dumps, the data within the blob container must be in the bsondump format. Place data files into folders named after the containing databases in the format *collection.bson*. Name any metadata files by using the format *collection.metadata.json*.

     - For JSON dumps, the files in the blob container must be placed into folders named after the containing databases. Within each database folder, data files must be placed in a subfolder called *data*, and named by using the format *collection.json*. Place any metadata files in a subfolder called *metadata*, and named by using the same format, *collection.json*. The metadata files must be in the same format as produced by the MongoDB bsondump tool.

     > [!IMPORTANT]  
     > We don't recommend that you use a self-signed certificate on the MongoDB server. If you must use one, connect to the server by using the connection string mode, and ensure that your connection string has quotation marks ("").
     >  
     > ```output
     > &sslVerifyCertificate=false
     > ```

   You can also use the IP address for situations in which DNS name resolution isn't possible.

   :::image type="content" source="media/tutorial-mongodb-to-cosmosdb/dms-specify-source.png" alt-text="Screenshot that shows specifying source details.":::

1. Select **Save**.

## Specify target details

1. On the **Migration target details** screen, specify the connection details for the target Azure Cosmos DB account. This account is the pre-provisioned Azure Cosmos DB for MongoDB account to which you're migrating your MongoDB data.

   :::image type="content" source="media/tutorial-mongodb-to-cosmosdb/dms-specify-target.png" alt-text="Screenshot that shows specifying target details.":::

1. Select **Save**.

## Map to target databases

1. On the **Map to target databases** screen, map the source and the target database for migration.

   If the target database contains the same database name as the source database, Azure Database Migration Service selects the target database by default.

   If **Create** appears next to the database name, it indicates that Azure Database Migration Service didn't find the target database, and the service will create the database for you.

   At this point in the migration, you can [provision throughput](../cosmos-db/set-throughput.md). In Azure Cosmos DB, you can provision throughput either at the database level or individually for each collection. Throughput is measured in [request units](../cosmos-db/request-units.md). Learn more about [Azure Cosmos DB pricing](https://azure.microsoft.com/pricing/details/cosmos-db/).

   :::image type="content" source="media/tutorial-mongodb-to-cosmosdb/dms-map-target-databases.png" alt-text="Screenshot that shows mapping to target databases." lightbox="media/tutorial-mongodb-to-cosmosdb/dms-map-target-databases.png":::

1. Select **Save**.

1. On the **Collection setting** screen, expand the collections listing, and then review the list of collections that will be migrated.

   Azure Database Migration Service automatically selects all the collections that exist on the source MongoDB instance that don't exist on the target Azure Cosmos DB account. If you want to remigrate collections that already include data, you need to explicitly select the collections on this pane.

   You can specify the number of RUs that you want the collections to use. Azure Database Migration Service suggests smart defaults based on the collection size.

   > [!NOTE]  
   > Perform the database migration and collection in parallel. If necessary, you can use multiple instances of Azure Database Migration Service to speed up the run.

   You can also specify a shard key to take advantage of [partitioning in Azure Cosmos DB](../cosmos-db/partitioning-overview.md) for optimal scalability. Review the [best practices for selecting a shard/partition key](../cosmos-db/partitioning-overview.md).

   :::image type="content" source="media/tutorial-mongodb-to-cosmosdb/dms-collection-setting.png" alt-text="Screenshot that shows selecting collections tables." lightbox="media/tutorial-mongodb-to-cosmosdb/dms-collection-setting.png":::

1. Select **Save**.

1. On the **Migration summary** screen, in the **Activity name** text box, specify a name for the migration activity.

   :::image type="content" source="media/tutorial-mongodb-to-cosmosdb/dms-migration-summary.png" alt-text="Screenshot that shows the migration summary." lightbox="media/tutorial-mongodb-to-cosmosdb/dms-migration-summary.png":::

## Run the migration

Select **Run migration**. The migration activity window appears, and the status of the activity is **Not started**.

:::image type="content" source="media/tutorial-mongodb-to-cosmosdb/dms-activity-status.png" alt-text="Screenshot that shows the activity status.":::

## Monitor the migration

On the migration activity screen, select **Refresh** to update the display until the status of the migration shows as **Completed**.

> [!NOTE]  
> You can select the activity to get details of database- and collection-level migration metrics.

:::image type="content" source="media/tutorial-mongodb-to-cosmosdb/dms-activity-completed.png" alt-text="Screenshot that shows the activity status completed.":::

## Verify data in Azure Cosmos DB

After the migration finishes, you can check your Azure Cosmos DB account to verify that all the collections were migrated successfully.

:::image type="content" source="media/tutorial-mongodb-to-cosmosdb/dms-cosmosdb-data-explorer.png" alt-text="Screenshot that shows where to check your Azure Cosmos DB account to verify that all the collections were migrated successfully." lightbox="media/tutorial-mongodb-to-cosmosdb/dms-cosmosdb-data-explorer.png":::

## Post-migration optimization

After you migrate the data stored in MongoDB database to the Azure Cosmos DB for MongoDB, you can connect to Azure Cosmos DB and manage the data. You can also perform other post-migration optimization steps. These might include optimizing the indexing policy, updating the default consistency level, or configuring global distribution for your Azure Cosmos DB account. For more information, see [Post-migration optimization](../cosmos-db/mongodb-post-migration.md).

## Additional resources

Trying to do capacity planning for a migration to Azure Cosmos DB?

- If all you know is the number of vCores and servers in your existing database cluster, read about [estimating request units using vCores or vCPUs](../cosmos-db/convert-vcore-to-request-unit.md)
- If you know typical request rates for your current database workload, read about [estimating request units using Azure Cosmos DB capacity planner](../cosmos-db/mongodb/estimate-ru-capacity-planner.md)

## Related content

- [Azure Database Migration Guide](/data-migration/)
