---
title: Create and use a cross-region or same region replica cluster 
description: Create an Azure DocumentDB replica cluster in another or the same region for disaster recovery (DR) and read scalability. Learn how to set up and use it.
author: seesharprun
ms.author: sidandrews
ms.reviewer: nlarin
ms.topic: how-to
ms.date: 09/29/2025
ms.custom:
  - ignite-2024
  - sfi-image-nochange
ai-usage: ai-assisted
---

# Create and use a replica cluster in another or the same Azure region in Azure DocumentDB

In this guide, you create a **replica cluster** in either a different Azure region or the same region for an **Azure DocumentDB** cluster. A cross-region replica cluster can be used for **disaster recovery (DR)** and **read scalability**, while a replica cluster in the same region is primarily intended for **read scalability**.

The replica cluster stores a copy of all your DocumentDB resources **databases**, **collections**, and **documents** in another or the same Azure region. The replica cluster provides a **unique endpoint** for various tools and drivers to connect to. It can be **promoted to accept writes** if the primary region experiences an outage.

## Prerequisites

[!INCLUDE[Prerequisite - Azure subscription](includes/prerequisite-azure-subscription.md)]

- [MongoDB shell](https://www.mongodb.com/try/download/shell)

## Create a new cluster and its replica in another or the same region

To get started, you first need to create an Azure DocumentDB cluster with replication.

1. Sign in to the **Azure portal** (<https://portal.azure.com>).

1. From the Azure portal menu or the **Home page**, select **Create a resource**.

1. On the **New** page, search for and select **Azure DocumentDB**.

1. On the **Create Azure DocumentDB cluster** page and within the **Basics** section, select the **Configure** option within the **Cluster tier** section.

1. On the **Scale** page, configure these options and then select **Save** to persist your changes to the cluster tier.

    | | Value |
    | --- | --- |
    | **Cluster tier** | `M30 tier, 2 vCores, 8-GiB RAM` |
    | **Storage per shard** | `128 GiB` |
    | **High availability** | *Disable* |
    | **Shards** | `1` |

    > [!TIP]
    > The settings recommended here are the minimum needed for replication. For extra protection, you can enable in-region high availability. This feature streams a copy of data from each shard to a standby counterpart in the same region but in a different availability zone (AZ). High availability uses synchronous replication to ensure zero data loss. It also includes automatic failure detection and failover. After a failover, the connection string remains unchanged. Enabling high availability on the primary cluster adds an extra layer of protection against failures.

1. Back in the **Basics** section, configure the following options:

    | | Value |
    | --- | --- |
    | **Subscription** | Select your Azure subscription |
    | **Resource group** | Create a new resource group or select an existing resource group |
    | **Cluster name** | 	Provide a globally unique name |
    | **Location** | Select a supported Azure region for your subscription |
    | **MongoDB version** | Select `8.0` |
    | **Admin username** | Create a username to access the cluster as a user administrator |
    | **Password** | Use a unique password associated with the username |

    > [!TIP]
    > Record the values you use for **username** and **password**. These values are used later in this guide. For more information about valid values, see [cluster limitations](limitations.md).

1. Select **Next: Networking**.

1. In the **Firewall rules** section on the **Networking** tab, configure these options:

    | | Value |
    | --- | --- |
    | **Connectivity method** | `Public access` |
    | **Allow public access from Azure services and resources within Azure to this cluster** | *Enabled* |

1. Add a firewall rule for your current client device to grant access to the cluster by selecting **+ Add current client IP address**.

    > [!TIP]
    > In many corporate environments, developer machine IP addresses are hidden due to a VPN or other corporate network settings. In these cases, you can temporarily allow access to all IP addresses by adding the `0.0.0.0` - `255.255.255.255` IP address range as a firewall rule. Use this firewall rule only temporarily as a part of connection testing and development.

1. Select **Next: Global distribution**.

1. On the **Global distribution** tab, configure the following settings:

    | | Value |
    | --- | --- |
    | **Read replica in another region** | `Enable` |
    | **Read replica name** | Provide a globally unique name |
    | **Read replica region** | Select a supported Azure region for your subscription that's distinct from the primary region |

1. Select **Review + create**.

1. Review the settings you provide, and then select **Create**. It takes a few minutes to create the cluster. Wait for the resource deployment is complete.

1. Finally, select **Go to resource** to navigate to the Azure DocumentDB cluster in the portal.

## Connect to primary cluster and ingest data

Get the connection string you need to connect to the primary (read-write) cluster in the Azure portal.

1. From the Azure DocumentDB primary cluster page, select the **Connection strings** navigation menu option under **Settings**.

    :::image type="content" source="media/how-to-cross-region-replication-portal/select-connection-strings-option.png" alt-text="Screenshot of the connection strings page in the cluster properties.":::

1. Copy the value from the **Self (always this cluster)** field.

1. In command line, use the MongoDB shell to connect to the primary cluster using the connection string.

```console
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
    breed: "shorthair",
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
> Replica clusters are created with networking access disabled. Add firewall rules or create private endpoints on the replica cluster after creation to enable read operations.

1. From the Azure DocumentDB *primary* cluster page, select the **Global distribution** page under **Settings**.

    :::image type="content" source="media/how-to-cross-region-replication-portal/global-distribution-page-on-primary-cluster.png" alt-text="Screenshot of the global distribution page in the primary cluster properties.":::

1. Select *replica cluster name* in the **Read replica** field to open the replica cluster properties in the Azure portal.

1. On the replica cluster page, under **Settings**, select **Networking**.

1. On the **Networking** page, select **Add current client IP address** to create a firewall rule with the public IP address of your computer, as perceived by the Azure system.

    :::image type="content" source="media/how-to-cross-region-replication-portal/cluster-networking-adding-firewall-rule.png" alt-text="Screenshot of the networking page on replica cluster.":::
  
    Verify your IP address before saving this configuration. In some situations, the IP address observed by Azure portal differs from the IP address used when accessing the Internet and Azure services. You can also select `Add 0.0.0.0 - 255.255.255.255` firewall rule to allow not just your IP, but the whole Internet to access the cluster. In this situation, clients still must sign in with the correct username and password to use the cluster.

1. Select **Save** on the toolbar to save the settings. It might take a few minutes for the updated networking settings to become effective.

## Connect to read replica cluster in another region or the same region and read data

Get the connection string for the replica cluster.

1. On the replica cluster sidebar, under **Cluster management**, select **Connection strings**.

1. Copy the value from the **Connection string** field.

    > [!IMPORTANT]
    > The connection string of the replica cluster contains unique *replica cluster name* that you selected during replica creation. The username and password values for the replica cluster are always the same as the ones on its primary cluster.

1. In command line, use the MongDB shell to connect to the replica cluster using its connection string.

    ```console
    mongosh "mongodb+srv://<user>@<cluster_replica_name>.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000"
    ```

### Read data from replica cluster

In the MongoDB shell connected to the replica cluster, read data from the database.

```mongodb
db.dogs.find();
db.cats.find();
```

## Promote replica cluster

To promote a replica cluster to a read-write cluster, follow these steps:

1. Select the *replica cluster* in the portal.

1. On the cluster sidebar, under **Cluster management**, select **Global distribution**.

1. On the **Global distribution** page, select **Promote** on the toolbar to initiate replica cluster promotion to read-write cluster. 

    :::image type="content" source="media/how-to-cross-region-replication-portal/replica-cluster-promotion.png" alt-text="Screenshot of the  replica cluster's global distribution page with the promote button.":::

1. In the **Promote cluster** pop-up window, confirm that you understand how replica promotion works, and select **Promote**. Replica promotion might take a few minutes to complete.

    :::image type="content" source="media/how-to-cross-region-replication-portal/replica-cluster-promotion-confirmation.png" alt-text="Screenshot of the replica cluster's global distribution page with the promotion confirmation pop-up window.":::

### Write to promoted cluster replica

Once replica promotion is completed, the promoted replica becomes available for writes and the former primary cluster is set to read-only.

To connect to *the promoted replica cluster* using its connection string, use the MongDB shell in command line.

```console
mongosh "mongodb+srv://<user>@<promoted_replica_cluster_name>.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000"
```

In the MongoDB shell session, perform a write operation.

```mongodb
db.createCollection('foxes')
```

Use the MongDB shell in command line to connect to *the new replica cluster* (former primary cluster) using its connection string. You can use self connection string or the global read-write connection string.

```console
mongosh "mongodb+srv://<user>@<new_replica_cluster_name>.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000"
```

In the MongoDB shell, confirm that writes are now disabled on the new replica (former primary cluster).

```mongodb
db.createCollection('bears')
```

## Related content

- [Learn about cross-region and same region replication in Azure DocumentDB](./cross-region-replication.md)
- [Migrate data to Azure DocumentDB](./migration-options.md)
