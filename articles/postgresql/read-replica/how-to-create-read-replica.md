---
title: Create a Read Replica in Azure Database for PostgreSQL Flexible Server
description: This article describes how to create a read replica of an Azure Database for PostgreSQL flexible server.
#customer intent: As a user, I want to create a read replica of my Azure Database for PostgreSQL flexible server, so that I can offload read-only queries from my source server.
author: gkasar
ms.author: gkasar
ms.reviewer: maghan
ms.date: 07/13/2026
ms.service: azure-database-postgresql
ms.subservice: replication
ms.topic: how-to
---

# Create a read replica in Azure Database for PostgreSQL flexible server

This article provides step-by-step instructions to create a read replica of an Azure Database for PostgreSQL flexible server.

> [!NOTE]  
> When you deploy read replicas for persistent heavy write-intensive workloads, the replication lag can continue to grow and might never catch up with the source server of the read replica. It might also increase storage usage at the source server as the WAL files are only deleted once all read replicas fed by one source server receive them.

> [!IMPORTANT]  
> Review the [considerations](concepts-read-replicas.md#considerations) when using read replicas.
>  
> Before you increase the values of the following parameters on a source server, increase them on its read replicas: `max_connections`, `max_prepared_transactions`, `max_locks_per_transaction`, `max_wal_senders`, `max_worker_processes`. And before you decrease them on a read replica, decrease them on its source.
>
> Attempting to change any of these parameters in the wrong order raises error code `ReadReplicaServerParameterLessThanSourceServer`, and the following message: `Replica server parameter should be greater than or equal to source server parameter. Parameter <parameter_name> value '<parameter_value>' setting on source server <source_server> should be less than its replica server <replica_server> value '<parameter_value_on_replica>'.`

Before setting up a read replica for your Azure Database for PostgreSQL flexible server, ensure its source server is configured to meet the necessary prerequisites. Specific settings on the source server can affect the ability to create replicas.

**Storage autogrow**: You're responsible for guaranteeing that the storage autogrow configuration on the source server and its read replicas follows the specific guidelines provided in [Storage autogrow with read replicas](concepts-read-replicas.md#storage-autogrow). These rules ensure consistency and prevent replication disruptions.

## Steps to create a read replica

### [Portal](#tab/portal-create-read-replica)

Use the [Azure portal](https://portal.azure.com/):

1. Select the Azure Database for PostgreSQL flexible server that you want to use as the source server of the replica.

1. In the resource menu, under the **Settings** section, select **Replication**.

    :::image type="content" source="./media/how-to-read-replicas/replication.png" alt-text="Screenshot showing the Replication page." lightbox="./media/how-to-read-replicas/replication.png":::

1.  In the **Replicas** section, select **Create replica**.

    :::image type="content" source="./media/how-to-read-replicas/create-replica.png" alt-text="Screenshot showing the location of the Create replica button in the Replication page." lightbox="./media/how-to-read-replicas/create-replica.png":::

1. You're redirected to the **Add read replica to Azure Database for PostgreSQL** wizard, where you can configure settings for the new read replica.

    :::image type="content" source="./media/how-to-read-replicas/add-read-replica-wizard.png" alt-text="Screenshot showing the Add read replica to Azure Database for PostgreSQL wizard." lightbox="./media/how-to-read-replicas/add-read-replica-wizard.png":::

1. Use the following table to understand the meaning of the different fields available in the **Basics** page, and as guidance to fill the page.

    | Section | Setting | Suggested value | Description | Can be changed after server creation |
    | --- | --- | --- | --- | --- |
    | **Project details** | | | | |
    | | **Subscription** | The name of the [subscription](/microsoft-365/enterprise/subscriptions-licenses-accounts-and-tenants-for-microsoft-cloud-offerings#subscriptions) in which you want to create the resource. | A subscription is an agreement with Microsoft to use one or more Microsoft cloud platforms or services. Charges accrue based on either a per-user license fee or on cloud-based resource consumption. | You can move an existing Azure Database for PostgreSQL flexible server to a different subscription from the one it was originally created in. For more information, see Move [Azure resources to a new resource group or subscription](/azure/azure-resource-manager/management/move-resource-group-and-subscription). |
    | | **Resource group** | The [resource group](/azure/azure-resource-manager/management/manage-resource-groups-portal#what-is-a-resource-group) in the selected subscription, in which you want to create the resource. It can be an existing resource group, or you can select **Create new**, and provide a name in that subscription that is unique among the existing resource group names. | A resource group is a container that holds related resources for an Azure solution. The resource group can include all the resources for the solution, or only those resources that you want to manage as a group. You decide how you want to allocate resources to resource groups based on what makes the most sense for your organization. Generally, add resources that share the same lifecycle to the same resource group so you can easily deploy, update, and delete them as a group. | You can move an existing Azure Database for PostgreSQL flexible server to a different subscription from the one you originally created. For more information, see Move [Azure resources to a new resource group or subscription](/azure/azure-resource-manager/management/move-resource-group-and-subscription). |
    | **Server details** | | | | |
    | | **Source server name** | The name of the source server for which you're trying to create a read replica. | A unique name that identifies your Azure Database for PostgreSQL flexible server. The domain name `postgres.database.azure.com` is appended to the server name you provide, to conform the fully qualified host name by which you can use a Domain Naming System server to resolve the IP address of your server. | |
    | | **Server name** | The name that you want to assign to the new read replica. | A unique name that identifies your Azure Database for PostgreSQL flexible server. The domain name `postgres.database.azure.com` is appended to the server name you provide, to conform the fully qualified host name by which you can use a Domain Naming System server to resolve the IP address of your server. | Although you can't change the server name after server creation, you can use the [point in time recovery](../backup-restore/concepts-backup-restore.md#point-in-time-recovery) feature to restore the server under a different name. An alternative approach to continue using the existing server, but being able to refer to it using a different server name, is to use the [virtual endpoints](concepts-read-replicas-virtual-endpoints.md) to create a writer endpoint with the new desired name. With this approach, you can refer to the server by its original name, or that assigned to the write virtual endpoint. |
    | | **Location** | The name of one of the [regions in which the service is supported](../overview.md#azure-regions). Point in time restore only supports the deployment of the new server in the same region in which the source server exists. | Compliance, data residency, pricing, proximity to your users, or availability of other services in the same region, are some of the requirements you should use when choosing the region. | The service doesn't offer a feature to automatically and transparently relocate a server to a different region. |
    | | **Compute + storage** | Assigns the same type and size of compute and same size of storage, as the ones used by the source server at the time the backup is restored. However, if you select the **Configure server** link, you can change the type of storage allocated to the new server, and whether or not it should be provisioned with geo-redundant backups. | | After the new server is deployed, its compute options can be scaled up or down. |
    | | **Availability zone** | Your preferred [availability zone](/azure/reliability/availability-zones-overview). | You can choose in which availability zone you want your server to be deployed. Being able to choose the availability zone in which your server is deployed, is useful to colocate it with your application. If you choose *No preference*, a default availability zone is automatically assigned to your server during its creation. | Although you can't change the availability zone after server creation, you can use the [point in time recovery](../backup-restore/concepts-backup-restore.md#point-in-time-recovery) feature to restore the server under a different name on a different availability zone. |
    | | **Authentication** | These settings are informational only. All settings related to authentication used by the read replica are inherited from their source server. | | Can be changed on the primary server and is replicated to downstream read replicas. |

1. If you want to change the compute tier, processor, or size automatically assigned to the new server, or if you want to change some of the storage settings of the read replica, select **Configure server**.

    :::image type="content" source="./media/how-to-read-replicas/configure-server-button.png" alt-text="Screenshot showing the location of the Configure server link." lightbox="./media/how-to-read-replicas/configure-server-button.png":::

1. The **Compute + storage** page opens to show compute and storage options for the new server.

    :::image type="content" source="./media/how-to-read-replicas/configure-server-page.png" alt-text="Screenshot showing the Compute + storage page." lightbox="./media/how-to-read-replicas/configure-server-page.png":::

1. Use the following table to understand the meaning of the different fields available in the **Compute + storage** page, and as guidance to fill the page.

    | Section | Setting | Suggested value | Description | Can be changed after read replica creation |
    | --- | --- | --- | --- | --- |
    | **Compute** | | | | |
    | | **Compute tier** | By default, it's automatically set to the same tier assigned to the source server. However, you can set it to any other compute tier on which read replicas are supported. | Possible values are **General Purpose** (typically used for production environments with most common workloads), and **Memory Optimized** (typically used for production environments running workloads that require a high memory to CPU ratio). For more information, see [Compute options in Azure Database for PostgreSQL](../compute-storage/concepts-compute.md). | Can be changed after the read replica is created. However, if you're using some functionality that is only supported on certain tiers and change the current tier to one in which the feature isn't supported, the feature stops being available or gets disabled. |
    | | **Compute processor** | On regions on which multiple processor types are available, you can select any of the two available values (**AMD** or **Intel**), to filter the list of values shown in the **Compute size** combobox to those matching the processor type selected. | Can be changed after read replica creation. |
    | | **Compute size** | By default, it's automatically set to the same compute size assigned to the source server. However, you can set it to any other compute size, as long as it has the same or a higher number of vCores as the source server. | The list of supported values might vary across regions, depending on the hardware available on each region. For more information, see [Compute options in Azure Database for PostgreSQL](../compute-storage/concepts-compute.md). | Can be changed after read replica creation. |
    | **Storage** | | | | |
    | | **Storage type** | Leave it as **Premium SSD**. | Setting the type of storage to a value different than that of the source server isn't supported. The wizard automatically sets this property to match the type of storage assigned to the source server. | Can't be changed after the read replica is created. |
    | | **Storage size** | By default, it's set to the same value as the storage size of the source server. However, you can set it to any higher value. | | Can be changed after the read replica server is created. You can only increase it. Manual or automatic shrinking of storage isn't supported. |
    | | **Performance tier** | By default, it's automatically set to the same value as the source server. However, you can change it to a different value. | Performance of Premium solid-state drives (SSD) is set when you create the disk, in the form of their performance tier. When setting the provisioned size of the disk, a performance tier is automatically selected. This performance tier determines the IOPS and throughput of your managed disk. For Premium SSD disks, you can change this tier at deployment or afterwards, without changing the size of the disk, and without downtime. Changing the tier allows you to prepare for and meet higher demand without using your disk's bursting capability. Depending on how long the extra performance is necessary, it can be more cost-effective to change your performance tier rather than rely on bursting. This change is ideal for events that temporarily require a consistently higher level of performance. Events like holiday shopping, performance testing, or running a training environment. To handle these events, you can switch a disk to a higher performance tier without downtime, for as long as you need the extra performance. You can then return to the original tier without downtime when the extra performance is no longer necessary. | Can be changed after the server is created. |
    | | **IOPS (operations/sec)** | Not available for servers with Premium SSD storage type. | Can be changed after the server is created. |
    | | **Throughput (MB/sec)** | Not available for servers with Premium SSD storage type. | Can be changed after the server is created. |

1.  Continue to the **Networking**, **Security**, or **Tags** tabs, if you need to change any of the settings that are allowed to differ from the source server. Once the new replica is configured to your needs, select **Review + create**.

    :::image type="content" source="./media/how-to-read-replicas/review-and-create.png" alt-text="Screenshot showing the location of the Review + create button." lightbox="./media/how-to-read-replicas/review-and-create.png":::

7.  Review that all configurations for the new deployment are correct, and select **Create**.

    :::image type="content" source="./media/how-to-read-replicas/create.png" alt-text="Screenshot showing the location of the Create button." lightbox="./media/how-to-read-replicas/create.png":::

8.  A new deployment is launched to create your new Azure Database for PostgreSQL flexible server and make it a read replica of the source server.
    
    :::image type="content" source="./media/how-to-read-replicas/create-replica-deployment-progress.png" alt-text="Screenshot showing the deployment in progress to create your new Azure Database for PostgreSQL flexible server." lightbox="./media/how-to-read-replicas/create-replica-deployment-progress.png":::

9. When the deployment completes, select **Go to resource** to start using your new Azure Database for PostgreSQL flexible server.

    :::image type="content" source="./media/how-to-read-replicas/create-replica-deployment-completed.png" alt-text="Screenshot showing the deployment successfully completed of your Azure Database for PostgreSQL flexible server." lightbox="./media/how-to-read-replicas/create-replica-deployment-completed.png":::

10. You arrive at the **Overview** page of the replica server.

    :::image type="content" source="./media/how-to-read-replicas/read-replica-overview.png" alt-text="Screenshot showing the Overview page of the read replica." lightbox="./media/how-to-read-replicas/read-replica-overview.png":::

11. In the resource menu, under the **Settings** section, select **Replication**. Under **Replicas**, find the list of servers that conform the replication set, and the role that each server takes.

    :::image type="content" source="./media/how-to-read-replicas/list-replicas-from-replica.png" alt-text="Screenshot showing the list of servers that conform a replication set from the perspective of an intermediate or first level replica." lightbox="./media/how-to-read-replicas/list-replicas-from-replica.png":::

12. If your replication set supports [Cascade replicas](./concepts-read-replicas.md#create-cascading-read-replicas), you can select any of the intermediate or first level read replicas, and create a read replica from it. For replication sets that have cascade replicas, the replication set topology shows a tree with an extra nesting level.

    :::image type="content" source="./media/how-to-read-replicas/list-replicas-from-cascade-replica.png" alt-text="Screenshot showing the list of servers that conform a replication set from the perspective of the cascade replica." lightbox="./media/how-to-read-replicas/list-replicas-from-cascade-replica.png":::

### [CLI](#tab/cli-create-read-replica)

Use the [`az postgres flexible-server replica create`](/cli/azure/postgres/flexible-server/replica#az-postgres-flexible-server-replica-create) command to create a read replica for your Azure PostgreSQL flexible server. 

```azurecli-interactive
az postgres flexible-server replica create \
  --name <replica_name> \
  --resource-group <resource_group> \
  --source-server <source_server> \
  --location <location>
```

Use the [`az postgres flexible-server replica list`](/cli/azure/postgres/flexible-server/replica#az-postgres-flexible-server-replica-list) command to list the read replicas of an Azure PostgreSQL flexible server. 

```azurecli-interactive
az postgres flexible-server replica list \
  --name <replica_name> \
  --resource-group <resource_group>
```

```output
[
  {
    "administratorLogin": null,
    "administratorLoginPassword": null,
    "authConfig": null,
    "availabilityZone": null,
    "backup": {
      "backupRetentionDays": null,
      "earliestRestoreDate": null,
      "geoRedundantBackup": "Disabled"
    },
    "cluster": null,
    "createMode": null,
    "dataEncryption": {
      "geoBackupEncryptionKeyStatus": null,
      "geoBackupKeyUri": null,
      "geoBackupUserAssignedIdentityId": null,
      "primaryEncryptionKeyStatus": null,
      "primaryKeyUri": null,
      "primaryUserAssignedIdentityId": null,
      "type": "SystemManaged"
    },
    "fullyQualifiedDomainName": null,
    "highAvailability": null,
    "id": "/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourceGroups/rg-production-flexible-server/providers/Microsoft.DBforPostgreSQL/flexibleServers/production-flexible-server-replica",
    "identity": null,
    "location": "canadacentral",
    "maintenanceWindow": {
      "customWindow": "Disabled",
      "dayOfWeek": 0,
      "startHour": 0,
      "startMinute": 0
    },
    "minorVersion": null,
    "name": "production-flexible-server-replica",
    "network": {
      "delegatedSubnetResourceId": null,
      "privateDnsZoneArmResourceId": null,
      "publicNetworkAccess": "Disabled"
    },
    "pointInTimeUtc": null,
    "privateEndpointConnections": null,
    "replica": {
      "capacity": null,
      "promoteMode": null,
      "promoteOption": null,
      "replicationState": "Active",
      "role": "AsyncReplica"
    },
    "replicaCapacity": null,
    "replicationRole": "AsyncReplica",
    "resourceGroup": "rg-production-flexible-server",
    "sku": {
      "name": "",
      "tier": null
    },
    "sourceServerResourceId": "/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourceGroups/rg-production-flexible-server/providers/Microsoft.DBforPostgreSQL/flexibleServers/production-flexible-server",
    "state": "Ready",
    "storage": {
      "autoGrow": "Disabled",
      "iops": null,
      "storageSizeGb": 0,
      "throughput": null,
      "tier": null,
      "type": null
    },
    "systemData": {
      "createdAt": "2026-06-12T00:00:00.000000+00:00",
      "createdBy": null,
      "createdByType": null,
      "lastModifiedAt": null,
      "lastModifiedBy": null,
      "lastModifiedByType": null
    },
    "tags": null,
    "type": "Microsoft.DBforPostgreSQL/flexibleServers",
    "version": null
  }
]
```

---


## Related content

- [Read replicas](concepts-read-replicas.md).
- [Create virtual endpoints](how-to-create-virtual-endpoints.md).
- [Switch over read replica to primary](how-to-switch-over-replica-to-primary.md).
- [Promote read replica to standalone server](how-to-promote-replica-to-standalone.md).
- [Delete a read replica](how-to-delete-read-replica.md).
