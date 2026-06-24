---
title: Restore to custom restore point
description: This article describes how to restore to custom restore point an Azure Database for PostgreSQL flexible server.
author: akashraokm
ms.author: akashrao
ms.reviewer: maghan
ms.date: 06/09/2026
ms.service: azure-database-postgresql
ms.subservice: backup-restore
ms.topic: how-to
#customer intent: As a user, I want to learn how to restore to custom restore point an Azure Database for PostgreSQL flexible server.
---

# Restore to custom restore point

This article provides step-by-step instructions to restore an Azure Database for PostgreSQL flexible server to a custom restore point.

## Steps to restore to custom restore point

### [Portal](#tab/portal-restore-custom-point)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

1. In the resource menu, select **Overview**.

    :::image type="content" source="./media/how-to-restore-server/overview.png" alt-text="Screenshot showing the Overview page." lightbox="./media/how-to-restore-server/overview.png":::

1. Select the **Restore** button.

    :::image type="content" source="./media/how-to-restore-server/restore-button.png" alt-text="Screenshot showing the location of the Restore button in the Overview page." lightbox="./media/how-to-restore-server/restore-button.png":::

1. You're redirected to the **Create Azure Database for PostgreSQL flexible server - Restore server** wizard, where you can configure settings for the new server. After the new server is deployed, the most recent snapshot of the source server data disk is restored. In the **Point-in-time-restore (PITR)** section, select **Select a custom restore point**.

    :::image type="content" source="./media/how-to-restore-server/custom-restore-point.png" alt-text="Screenshot showing the Select a custom restore point radio button selected." lightbox="./media/how-to-restore-server/custom-restore-point.png":::

1. In **Custom restore point (UTC)**, select a date from the calendar control, and specify a time in the time text box.

    :::image type="content" source="./media/how-to-restore-server/custom-restore-point-date-time.png" alt-text="Screenshot showing the date picker and time textbox, available to configure the custom restore point." lightbox="./media/how-to-restore-server/custom-restore-point-date-time.png":::

    > [!NOTE]
    > Selectable dates in the calendar control are restricted to the range from the day in which the oldest available backup was taken until now.
    > If you select a time that falls outside the period ranging from the earliest restore point and the time (UTC) at which you landed in the **Create Azure Database for PostgreSQL flexible Server - Restore server** wizard, an error asks you to adjust the value.
    
1. Use the following table to understand the meaning of the different fields available in the **Basics** page, and as guidance to fill the page:

    | Section | Setting | Suggested value | Description | Can be changed after server creation |
    | --- | --- | --- | --- | --- |
    | **Project details** | | | | |
    | | **Subscription** | The name of the [subscription](/microsoft-365/enterprise/subscriptions-licenses-accounts-and-tenants-for-microsoft-cloud-offerings#subscriptions) in which you want to create the resource. | A subscription is an agreement with Microsoft to use one or more Microsoft cloud platforms or services. Charges accrue based on either a per-user license fee or on cloud-based resource consumption. | You can move an existing Azure Database for PostgreSQL flexible server server to a different subscription from the one it was originally created in. For more information, see Move [Azure resources to a new resource group or subscription](/azure/azure-resource-manager/management/move-resource-group-and-subscription). |
    | | **Resource group** | The [resource group](/azure/azure-resource-manager/management/manage-resource-groups-portal#what-is-a-resource-group) in the selected subscription, in which you want to create the resource. It can be an existing resource group, or you can select **Create new**, and provide a name in that subscription which is unique among the existing resource group names. | A resource group is a container that holds related resources for an Azure solution. The resource group can include all the resources for the solution, or only those resources that you want to manage as a group. You decide how you want to allocate resources to resource groups based on what makes the most sense for your organization. Generally, add resources that share the same lifecycle to the same resource group so you can easily deploy, update, and delete them as a group. | You can move an existing Azure Database for PostgreSQL flexible server server to a different subscription from the one it was originally created in. For more information, see Move [Azure resources to a new resource group or subscription](/azure/azure-resource-manager/management/move-resource-group-and-subscription). |
    | **Source details** | | | | |
    | | **Source server** | The name of the server whose backup you want to restore on the newly deployed server. | | |
    | | **Geo-redundant restore** | If the source server was created with [geo-redundant backups](concepts-backup-restore.md#geo-redundant-backup-and-restore), this option is enabled. If it's enabled, you can restore a backup kept in the storage account of the paired region to create a new server in that other region. | | |
    | | **Earliest restore point** | The oldest backup of the source server available to restore from. The server whose backup you want to restore on the newly deployed server. Backups are automatically deleted, based on the backup retention period configured on the source server. | | |
    | | **Point-in-time-restore (PITR)** | Possible options are **Latest restore point (Now)**, **Custom restore point**, and **Fast restore point (Restore using full backup only)**. | To restore to a custom restore point, select **Custom restore point**. | |
    | **Server details** | | | | |
    | | **Name** | The name that you want to assign to the newly deployed server, on top of which a backup of the source is restored. | A unique name that identifies your Azure Database for PostgreSQL flexible server server. The domain name `postgres.database.azure.com` is appended to the server name you provide, to conform the fully qualified host name by which you can use a Domain Naming System server to resolve the IP address of your server. | Although the server name can't be changed after server creation, you can use the [point in time recovery](concepts-backup-restore.md#point-in-time-recovery) feature to restore the server under a different name. An alternative approach to continue using the existing server, but being able to refer to it using a different server name, is to use the [virtual endpoints](../read-replica/../read-replica/../read-replica/concepts-read-replicas-virtual-endpoints.md) to create a writer endpoint with the new desired name. With this approach, you can refer to the server by its original name, or that assigned to the write virtual endpoint. |
    | | **Location** | The name of one of the [regions in which the service is supported](../overview.md#azure-regions). Point in time restore only supports the deployment of the new server in the same region in which the source server exists. | Compliance, data residency, pricing, proximity to your users, or availability of other services in the same region, are some of the requirements you should use when choosing the region. | The service doesn't offer a feature to automatically and transparently relocate a server to a different region. |
    | | **PostgreSQL version** | The version selected by default. | Point in time restore only supports the deployment of the new server with the exact same major version used by the source server. Currently those versions are: **[!INCLUDE [major-versions-ascending](../includes/major-versions-ascending.md)]** | Azure Database for PostgreSQL flexible server supports in-place upgrade, via [major version upgrade](../configure-maintain/how-to-perform-major-version-upgrade.md). |
    | | **Availability zone** | Your preferred [availability zone](/azure/reliability/availability-zones-overview). | You can choose in which availability zone you want your server to be deployed. Being able to choose the availability zone in which your server is deployed, is useful to colocate it with your application. If you choose *No preference*, a default availability zone is automatically assigned to your server during its creation. | Although the availability zone in which a server is deployed can't be changed after its creation, you can use the [point in time recovery](concepts-backup-restore.md#point-in-time-recovery) feature to restore the server under a different name on a different availability zone. |
    | | **Compute + storage** | Assigns the same type and size of compute and same size of storage, as the ones used by the source server at the time the backup is restored. However, if you select the **Configure server** link, you can change the type of storage allocated to the new server, and whether or not it should be provisioned with geo-redundant backups. | | After the new server is deployed, its compute options can be scaled up or down. |

1. If you want to change the type of storage assigned to the new server, or if you want to deploy it with geo-redundant backups, select **Configure server**:

    :::image type="content" source="./media/how-to-restore-server/configure-server-custom-button.png" alt-text="Screenshot showing the location of the Configure server link." lightbox="./media/how-to-restore-server/configure-server-custom-button.png":::

1. The **Compute + storage** page opens to show compute and storage options for the new server:

    :::image type="content" source="./media/how-to-restore-server/configure-server-page.png" alt-text="Screenshot showing the Compute + storage page." lightbox="./media/how-to-restore-server/configure-server-page.png":::

1. Use the following table to understand the meaning of the different fields available in the **Compute + storage** page, and as guidance to fill the page:

    | Section | Setting | Suggested value | Description | Can be changed after server creation |
    | --- | --- | --- | --- | --- |
    | **Compute** | | | | |
    | | **Compute tier** | Can't be changed. It's automatically set to the same value as the source server. | Possible values are **Burstable** (typically used for development environments in which workloads don't need the full capacity of the CPU continuously), **General Purpose** (typically used for production environments with most common workloads), and **Memory Optimized** (typically used for production environments running workloads that require a high memory to CPU ratio). For more information, see [Compute options in Azure Database for PostgreSQL flexible server](../compute-storage/concepts-compute.md). | Can be changed after the server is created. However, if you're using some functionality which is only supported on certain tiers and change the current tier to one in which the feature isn't supported, the feature stops being available or gets disabled. |
    | | **Compute size** | Can't be changed. It's automatically set to the same value as the source server. | The list of supported values might vary across regions, depending on the hardware available on each region. For more information, see [Compute options in Azure Database for PostgreSQL flexible server](../compute-storage/concepts-compute.md). | Can be changed after server is created. |
    | **Storage** | | | | |
    | | **Storage type** | Select **Premium SSD**. | The list of allowed values might vary depending on which other features you selected. For more information, see [Storage options in Azure Database for PostgreSQL flexible server](../extensions/concepts-storage.md). | Can't be changed after the server is created. |
    | | **Storage size** | Can't be changed and is automatically set to the same value as the source server. | The list of supported values might vary across regions, depending on the hardware available on each region. For more information, see [Compute options in Azure Database for PostgreSQL flexible server](../compute-storage/concepts-compute.md). | Can be changed after the server is created. It can only be increased. Manual or automatic shrinking of storage isn't supported. Acceptable values depend on the type of storage assigned to the server. |
    | | **Performance tier** | Can't be changed and is automatically set to the same value as the source server. | Performance of Premium solid-state drives (SSD) is set when you create the disk, in the form of their performance tier. When setting the provisioned size of the disk, a performance tier is automatically selected. This performance tier determines the IOPS and throughput of your managed disk. For Premium SSD disks, you can change this tier at deployment or afterwards, without changing the size of the disk, and without downtime. Changing the tier allows you to prepare for and meet higher demand without using your disk's bursting capability. It can be more cost-effective to change your performance tier rather than rely on bursting, depending on how long the extra performance is necessary. This option is ideal for events that temporarily require a consistently higher level of performance. Events like holiday shopping, performance testing, or running a training environment. To handle these events, you can switch a disk to a higher performance tier without downtime, for as long as you need the extra performance. You can then return to the original tier without downtime when the extra performance is no longer necessary. | Can be changed after the server is created. |
    | | **Storage autogrow** | Can't be changed and is automatically set to the same value as the source server. | This option might not be supported for some storage types, and it might not be honored for certain storage sizes. For more information, see [Configure storage autogrow in an Azure Database for PostgreSQL flexible server](../scale/how-to-auto-grow-storage.md). | Can be changed after the server is created, as long as the storage type supports this feature. |
    | **Backups** | | | | |
    | | **Backup retention period (in days)** | Can't be changed and is automatically set to the same value as the source server. | The default backup retention period is 7 days, but you can extend the period to a maximum of 35 days. | Can be changed after server is created. |
    | | **Geo-redundancy** | Leave this option disabled. | Geo-redundancy in backups is only supported on servers deployed in any of the [Azure paired regions](/azure/reliability/cross-region-replication-azure). For more information, see [Geo-redundant backup and restore in Azure Database for PostgreSQL flexible server](concepts-backup-restore.md#geo-redundant-backup-and-restore)| Can't be changed after server is created. |

1. Once you configure the new server, select **Review + create**.

    :::image type="content" source="./media/how-to-restore-server/restore-point-custom-review-create.png" alt-text="Screenshot showing the location of the Review + create button." lightbox="./media/how-to-restore-server/restore-point-custom-review-create.png":::

1. Review that all configurations for the new deployment are correct, and select **Create**.

    :::image type="content" source="./media/how-to-restore-server/restore-point-custom-create.png" alt-text="Screenshot showing the location of the Create button." lightbox="./media/how-to-restore-server/restore-point-custom-create.png":::

1. A new deployment is launched to create your new Azure Database for PostgreSQL flexible server and restore the most recent data available on the source server at the time of restore:

    :::image type="content" source="./media/how-to-restore-server/restore-point-deployment-progress.png" alt-text="Screenshot that shows the deployment in progress to create your new Azure Database for PostgreSQL Flexible server, on which the most recent data available on the source server is restored." lightbox="./media/how-to-restore-server/restore-point-deployment-progress.png":::

1. When the deployment completes, select **Go to resource**. You're taken to the **Overview** page of your new Azure Database for PostgreSQL flexible server, and you can start using it:

    :::image type="content" source="./media/how-to-restore-server/restore-point-deployment-completed.png" alt-text="Screenshot that shows the deployment successfully completed of your Azure Database for PostgreSQL Flexible server." lightbox="./media/how-to-restore-server/restore-point-deployment-completed.png":::

### [CLI](#tab/cli-restore-custom-point)

Use the [az postgres flexible-server restore](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-restore) command to restore a server backup to the latest restore point.

```azurecli-interactive
az postgres flexible-server restore \
  --resource-group <resource_group> \
  --name <server> \
  --source-server <source_server> \
  --restore-time 2026-06-26T02:10:00+00:00
```

> [!NOTE]
> - The value you pass to the `--restore-time` parameter represents the point in time, in UTC, to restore from (ISO8601 format).
> - If you don't include the `--restore-time` parameter, the command uses the current time in the system where you run the command.
> - If you enter a future value, the backend service that receives the request normalizes it to the current date and time.
> - If you enter a value that's earlier than the earliest restore point available on the source server, you receive an InternalServerError.

---

## Related content

- [Restore to latest restore point](how-to-restore-latest-restore-point.md).
- [Restore full backup (fast restore)](how-to-restore-full-backup.md).
- [Restore to paired region (geo-restore)](how-to-restore-paired-region.md).
- [Restore a deleted server](how-to-restore-deleted-server.md).
