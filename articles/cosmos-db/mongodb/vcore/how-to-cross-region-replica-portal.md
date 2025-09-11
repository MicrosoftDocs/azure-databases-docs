---
title: Create and use a cross-region or same region replica cluster 
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: Create a new Azure Cosmos DB for MongoDB vCore replica cluster in another or same region for disaster recovery (DR) and read scaling purposes.
author: niklarin
ms.author: nlarin
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.custom:
- ignite-2024
- sfi-image-nochange
ms.topic: how-to
ms.date: 08/09/2025
appliesto:
- ✅ MongoDB vCore
---

# Create and use a cross-region replica cluster or same region replica cluster in Azure Cosmos DB for MongoDB vCore

In this guide, you will create a **replica cluster** in either a different Azure region or the same region for an **Azure Cosmos DB for MongoDB vCore** cluster. A cross-region replica cluster can be used for **disaster recovery (DR)** and **read scalability**, while a replica cluster in the same region is primarily intended for **read scalability**.

The replica cluster stores a copy of all your MongoDB resources—**databases**, **collections**, and **documents**—in another or the same Azure region. The replica cluster provides a **unique endpoint** for various tools and SDKs to connect to. It can be **promoted to accept writes** if the primary region experiences an outage.

## Prerequisites

[!INCLUDE[Prerequisite - Azure subscription](includes/prereq-azure-subscription.md)]

[!INCLUDE[Prerequisite - Mongo shell](includes/prereq-shell.md)]

## Create a new cluster and its replica in another or the same region

Create a MongoDB cluster with a cluster read replica by using Azure Cosmos DB for MongoDB vCore.

> [!TIP]
> For this guide, we recommend using the resource group name ``msdocs-cosmos-quickstart-rg``.

1. Sign in to the [Azure portal](https://portal.azure.com).

1. From the Azure portal menu or the **Home page**, select **Create a resource**.

1. On the **New** page, search for and select **Azure Cosmos DB**.

1. On the **Which API best suits your workload?** page, select the **Create** option within the **Azure Cosmos DB for MongoDB** section. 

   :::image type="content" source="media/quickstart-portal/select-api-option.png" lightbox="media/quickstart-portal/select-api-option.png" alt-text="Screenshot of the select API option page for Azure Cosmos DB.":::

1. On the **Which type of resource?** page, select the **Create** option within the **vCore cluster** section. For more information, see [overview of the vCore architecture in Azure Cosmos DB for MongoDB](introduction.md).

    :::image type="content" source="media/quickstart-portal/select-resource-type.png" alt-text="Screenshot of the select resource type option page for Azure Cosmos DB for MongoDB.":::

1. On the **Create Azure Cosmos DB for MongoDB cluster** page, select the **Configure** option within the **Cluster tier** section.

    :::image type="content" source="media/quickstart-portal/select-cluster-option.png" alt-text="Screenshot of the cluster configuration option for a new Azure Cosmos DB for MongoDB cluster.":::

1. On the **Scale** page, leave the options set to their default values:

    | Setting | Value |
    | --- | --- |
    | **Shard count** | 1 shard |
    | **Cluster tier** | M30 Tier, 2 vCores, 8 GiB RAM |
    | **Storage** | 128 GiB |

1. Unselect the **High availability** option. In the high availability (HA) acknowledgment section, select **I understand**. Finally, select **Save** to persist your changes to the cluster configuration.

    In-region high availability provides an in-region solution where a copy of data from each shard in a cluster is streamed to its standby counterpart located in the same region but in a different availability zone (AZ). High availability uses synchronous replication with zero data loss and automatic failure detection and failover while preserving the connection string intact after failover. High availability might be enabled on the primary cluster for an additional layer of protection from failures.

    :::image type="content" source="media/quickstart-portal/configure-scale.png" alt-text="Screenshot of cluster tier and scale options for a cluster.":::

1. Back on the cluster page enter the following information:

    | Setting | Value | Description |
    | --- | --- | --- |
    | Subscription | Subscription name | Select the Azure subscription that you wish to use for this Azure Cosmos DB for MongoDB cluster and its replica cluster. |
    | Resource group | Resource group name | Select a resource group, or select **Create new**, then enter a unique name for the new resource group. |
    | Cluster name | A globally unique name | Enter a name to identify your Azure Cosmos DB for MongoDB cluster. The name is used as part of a fully qualified domain name (FQDN) with a suffix of *mongodbcluster.cosmos.azure.com*, so the name must be globally unique. The name can only contain lowercase letters, numbers, and the hyphen (-) character. The name must also be between 3 and 40 characters in length. |
    | Location | The region closest to your users | Select a geographic location to host your Azure Cosmos DB for MongoDB cluster with read and write capabilities, the primary cluster. Use the location that is closest to your users to give them the fastest access to the data. |
    | MongoDB version | Version of MongoDB to run on your cluster |  This value is set to a default of the most recent MongoDB version available. |
    | Admin username | Provide a username to access the cluster | This user is created on the cluster as a user administrator. |
    | Password | Use a unique password to pair with the username | Password must be at least 8 characters and at most 128 characters. |

    :::image type="content" source="media/how-to-cross-region-replication-portal/configure-cluster.png" alt-text="Screenshot of various configuration options for a cluster.":::

1. Select **Next: Networking**.

1. On the **Networking** tab, select **Add current client IP address** to create a firewall rule with the public IP address of your computer, as perceived by the Azure system.

    :::image type="content" source="media/how-to-cross-region-replication-portal/networking-adding-firewall-rule.png" alt-text="Screenshot of the networking settings for a cluster.":::

Verify your IP address before saving this configuration. In some situations, the IP address observed by Azure portal differs from the IP address used when accessing the Internet and Azure services. Thus, you may need to change the start IP and end IP to make the rule function as expected. Use a search engine or other online tool to check your own IP address. For example, search for *what is my IP*.

   :::image type="content" source="media/how-to-cross-region-replication-portal/what-is-my-ip.png" alt-text="Screenshot of a web search result for the current host's public IP address.":::

You can also select `Add 0.0.0.0 - 255.255.255.255` firewall rule to allow not just your IP, but the whole Internet to access the cluster. In this situation, clients still must log in with the correct username and password to use the cluster. Nevertheless, it's best to allow worldwide access for only short periods of time and for only non-production databases.

1. Select **Next: Global distribution**.

1. On the **Global distribution** tab, select **Enable** for **Cluster replica** to create a cluster read replica as a part of this new primary cluster provisioning.

1. In the **Read replica name** field, enter a name for the cluster read replica. It should be a globally unique cluster name.

1. Select a value from the **Read replica region** drop-down list.

    :::image type="content" source="media/how-to-cross-region-replication-portal/global-distribution-tab.png" alt-text="Screenshot of the global distribution tab in cluster provisioning.":::

1. Select **Review + create**.

1. Review the settings you provided, and then select **Create**. It takes a few minutes to create the cluster. Wait for the portal page to display **Your deployment is complete** before moving on.

1. Select **Go to resource** to go to the Azure Cosmos DB for MongoDB cluster page.

    :::image type="content" source="media/quickstart-portal/deployment-complete.png" alt-text="Screenshot of the deployment page for a cluster.":::

## Connect to primary cluster and ingest data

Get the connection string you need to connect to the primary (read-write) cluster in the Azure portal.

1. From the Azure Cosmos DB for MongoDB vCore primary cluster page, select the **Connection strings** navigation menu option under **Settings**.

    :::image type="content" source="media/how-to-cross-region-replication-portal/select-connection-strings-option.png" alt-text="Screenshot of the connection strings page in the cluster properties.":::

1. Copy the value from the **Self (always this cluster)** field.

1. In command line, use the MongoDB shell to connect to the primary cluster using the connection string.

```shell
mongosh "mongodb+srv://<user>@<primary_cluster_name>.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000"
```

### Ingest data

Create a *my_script.js* script file to run it from the MongoDB shell.

```javascript
let dogDocs = [
  {
    name: "pooch",
    breed: "poodle",
    weight: "6 lbs"
  },
  {
    name: "mutt",
    breed: "bulldog",
    weight: "10 lbs"
  }
];

let catDocs = [
  {
    name: "minni", 
    breed: "persian",
    color: "white"
  },
  {
    name: "tinkle",
    breed: "bombay",
    color: "black"
  }
];

let dogIndex = { name : 1 };
let catIndex = { name : 1 };

let collInfoObjs = [ 
  { coll: "dogs", data: dogDocs, index: dogIndex }, 
  { coll: "cats", data: catDocs, index: catIndex } 
];

for (obj of collInfoObjs) {
    db[obj.coll].insertMany(obj.data);
    db[obj.coll].createIndex(obj.index);
}
```

This script file creates two collections and inserts documents with data into those collections.
Save my_script.js file in a folder accessible to the MongoDB shell session.

Run the script from the MongoDB shell connected to the primary MongoDB cluster.

```mongodb
load(my_script.js);
```

In the MongoDB shell connected to the primary MongoDB cluster, read data from the database.

```mongodb
db.dogs.find();
db.cats.find();
```

## Enable access to replica cluster

> [!IMPORTANT]
> Replica clusters are always created with networking access disabled. You should add firewall rules or create private endpoints on the replica cluster after it's created to enable read operations.

1. From the Azure Cosmos DB for MongoDB vCore *primary* cluster page, select the **Global distribution** page under **Settings**.

    :::image type="content" source="media/how-to-cross-region-replication-portal/global-distribution-page-on-primary-cluster.png" alt-text="Screenshot of the global distribution page in the primary cluster properties.":::

1. Select *replica cluster name* in the **Read replica** field to open the replica cluster properties in the Azure portal.

1. On the MongoDB vCore replica cluster page, under **Settings**, select **Networking**.

1. On the **Networking** page, select **Add current client IP address** to create a firewall rule with the public IP address of your computer, as perceived by the Azure system.

    :::image type="content" source="media/how-to-cross-region-replication-portal/cluster-networking-adding-firewall-rule.png" alt-text="Screenshot of the networking page on read replica cluster.":::
  
    Verify your IP address before saving this configuration. In some situations, the IP address observed by Azure portal differs from the IP address used when accessing the Internet and Azure services. You can also select `Add 0.0.0.0 - 255.255.255.255` firewall rule to allow not just your IP, but the whole Internet to access the cluster. In this situation, clients still must log in with the correct username and password to use the cluster.

1. Select **Save** on the toolbar to save the settings. It might take a few minutes for the updated networking settings to become effective.

## Connect to read replica cluster in another region or the same region and read data

Get the connection string for the replica cluster.

1. On the replica cluster sidebar, under **Cluster management**, select **Connection strings**.

1. Copy the value from the **Connection string** field.

    > [!IMPORTANT]
    > The connection string of the read replica cluster contains unique *replica cluster name* that you selected during replica creation. The username and password values for the read replica cluster are always the same as the ones on its primary cluster.

1. In command line, use the MongDB shell to connect to the read replica cluster using its connection string.

    ```shell
    mongosh "mongodb+srv://<user>@<cluster_replica_name>.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000"
    ```

### Read data from replica cluster

In the MongoDB shell connected to the replica cluster, read data from the database.

```mongodb
db.dogs.find();
db.cats.find();
```

## Promote replica cluster

To promote a cluster read replica to a read-write cluster, follow these steps:

1. Select the *read replica cluster* in the portal.

1. On the cluster sidebar, under **Cluster management**, select **Global distribution**.

1. On the **Global distribution** page, select **Promote** on the toolbar to initiate read replica promotion to read-write cluster. 

    :::image type="content" source="media/how-to-cross-region-replication-portal/replica-cluster-promotion.png" alt-text="Screenshot of the read replica cluster global distribution page with the promote button.":::

1. In the **Promote cluster** pop-up window, confirm that you understand how replica promotion works, and select **Promote**. Replica promotion might take a few minutes to complete.

    :::image type="content" source="media/how-to-cross-region-replication-portal/replica-cluster-promotion-confirmation.png" alt-text="Screenshot of the read replica cluster global distribution page with the promote confirmation pop-up window.":::

### Write to promoted cluster replica

Once replica promotion is completed, the promoted replica becomes available for writes and the former primary cluster is set to read-only.

Use the MongDB shell in command line to connect to *the promoted replica cluster* using its connection string.

```shell
mongosh "mongodb+srv://<user>@<promoted_replica_cluster_name>.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000"
```

In the MongoDB shell session, perform a write operation.

```mongodb
db.createCollection('foxes')
```

Use the MongDB shell in command line to connect to *the new replica cluster* (former primary cluster) using its connection string. You can use self connection string or the global read-write connection string.

```shell
mongosh "mongodb+srv://<user>@<new_replica_cluster_name>.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000"
```

In the MongoDB shell, confirm that writes are now disabled on the new replica (former primary cluster).

```mongodb
db.createCollection('bears')
```

## Related content

- [Learn about cross-region and same region replication in Azure Cosmos DB for MongoDB vCore](./cross-region-replication.md)
- [Migrate data to Azure Cosmos DB for MongoDB vCore](./migration-options.md)
