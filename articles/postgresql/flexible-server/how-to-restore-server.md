---
title: Restore a server
description: This article describes how to perform restore operations in Azure Database for PostgreSQL - Flexible Server.
author: akashraokm
ms.author: akashrao
ms.reviewer: maghan
ms.date: 01/10/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
#customer intent: As a user, I want to learn the different restore options available to restore backups of an Azure Database for PostgreSQL flexible server.
---

# Restore a server

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

This article provides step-by-step instructions to perform the different types of restore of available backups of an Azure Database for PostgreSQL flexible server.

Existing servers can be restored to their latest restore point, to a custom restore point, or to a full backup (snapshot) among the ones available, taking into account your configured backup retention period.

If your source server is configured with geo-redundant backup, you can restore its backups to its corresponding [paired region](/azure/reliability/cross-region-replication-azure).

Restore of backups to the paired region, fetches backups from the physical copies in the paired region of the [geo-redundant storage](/azure/storage/common/storage-redundancy#geo-redundant-storage).

Backups of the server are first stored to the physical location in its region, and then they're asynchronously copied to the geo-redundant storage. As a consequence, if you initiate a point in time restore of the server in the same region and another point in time restore of the same server to its paired region, and you set the time to some instant close to the present, the server that is restored on the paired region might not include some recent data that is available on the server that is restored in the primary region.
<!-- Deleted servers can also be restored. Restore of deleted servers is possible as long as the restore operation is initiated within five days from the time the server was deleted. This recovery is based on the last full backup (snapshot) available when the server was dropped. Therefore, this operation can result in data loss. The data loss is limited to changes that came into the server after the most recent full backup. -->

<!-- When you issue a request to delete an Azure Database for flexible server, it isn't immediately deleted. Instead, an asynchronous process triggers to remove everything from that server, except for the server's specifications and the most recent full back. That process can take around five minutes. If you try to recover the deleted server and the deletion process isn't completed yet, the ReviveDropped operation might fail. The reason for the failure is because the server still exists, and doesn't attempt the recovery from the tombstone server. To avoid this issue, we recommend you to increase the time interval to 10 or 15 minutes, to allow for the deletion process to complete. -->

## Restore to the latest restore point

### [Portal](#tab/portal-restore-latest-point)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

2. In the resource menu, select **Overview**.

    :::image type="content" source="./media/how-to-restore-server/overview.png" alt-text="Screenshot showing the Overview page." lightbox="./media/how-to-restore-server/overview.png":::

3. Select the **Restore** button.

    :::image type="content" source="./media/how-to-restore-server/restore-button.png" alt-text="Screenshot showing the location of the Restore button in the Overview page." lightbox="./media/how-to-restore-server/restore-button.png":::

4. You're redirected to the **Create Azure Database for PostgreSQL Flexible server - Restore server** wizard, from where you can configure some settings for the new server that is created. After the new server is deployed, the most recent snapshot of the source server data disk is restored. In the **Point-in-time-restore (PITR)** section, select **Latest restore point (Now)**.

    :::image type="content" source="./media/how-to-restore-server/latest-restore-point.png" alt-text="Screenshot showing the Latest restore point (Now) radio button selected." lightbox="./media/how-to-restore-server/latest-restore-point.png":::

5. Use the following table to understand the meaning of the different fields available in the **Basics** page, and as guidance to fill the page:

    | Section | Setting | Suggested value | Description | Can be changed after instance creation |
    | --- | --- | --- | --- | --- |
    | **Project details** | | | | |
    | | **Subscription** | The name of the [subscription](/microsoft-365/enterprise/subscriptions-licenses-accounts-and-tenants-for-microsoft-cloud-offerings#subscriptions) in which you want to create the resource. | A subscription is an agreement with Microsoft to use one or more Microsoft cloud platforms or services, for which charges accrue based on either a per-user license fee or on cloud-based resource consumption. | An existing Azure Database for PostgreSQL flexible server instance can be moved to a different subscription from the one it was originally created. For more information, see Move [Azure resources to a new resource group or subscription](/azure/azure-resource-manager/management/move-resource-group-and-subscription). |
    | | **Resource group** | The [resource group](/azure/azure-resource-manager/management/manage-resource-groups-portal#what-is-a-resource-group) in the selected subscription, in which you want to create the resource. It can be an existing resource group, or you can select **Create new**, and provide a name in that subscription which is unique among the existing resource group names. | A resource group is a container that holds related resources for an Azure solution. The resource group can include all the resources for the solution, or only those resources that you want to manage as a group. You decide how you want to allocate resources to resource groups based on what makes the most sense for your organization. Generally, add resources that share the same lifecycle to the same resource group so you can easily deploy, update, and delete them as a group | An existing Azure Database for PostgreSQL flexible server instance can be moved to a different subscription from the one it was originally created. For more information, see Move [Azure resources to a new resource group or subscription](/azure/azure-resource-manager/management/move-resource-group-and-subscription). |
    | **Source details** | | | | |
    | | **Source server** | The name of the server whose backup you want to restore on the newly deployed server. | | |
    | | **Geo-redundant restore** | If the source server was created with [geo-redundant backups](concepts-backup-restore.md#geo-redundant-backup-and-restore), this option would be enabled. If it's enabled, you could restore a backup kept in the storage account of the paired region to create a new server in that other region. | | |
    | | **Earliest restore point** | The oldest backup of the source server available to restore from. the server whose backup you want to restore on the newly deployed server. Backups are automatically deleted, based on the backup retention period configured on the source server. | | |
    | | **Point-in-time-restore (PITR)** | Possible options are **Latest restore point (Now)**, **Select a custom restore point**, and **Select Fast restore point (Restore using full backup only)**. | To restore to latest restore point, select **Latest restore point (Now)**. | |
    | **Server details** | | | | |
    | | **Name** | The name that you want to assign to the newly deployed server, on top of which a backup of the source is restored. | A unique name that identifies your Azure Database for PostgreSQL flexible server instance. The domain name `postgres.database.azure.com` is appended to the server name you provide, to conform the fully qualified host name by which you can use a Domain Naming System server to resolve the IP address of your instance. | Although the server name can't be changed after server creation, you can use the [point in time recovery](concepts-backup-restore.md#point-in-time-recovery) feature, to restore the server under a different name. An alternative approach to continue using the existing server, but being able to refer to it using a different server name, would use the [virtual endpoints](concepts-read-replicas-virtual-endpoints.md) to create a writer endpoint with the new desired name. With this approach, you could refer to the instance by its original name, or that assigned to the write virtual endpoint. |
    | | **Location** | The name of one of the [regions in which the service is supported](overview.md#azure-regions). Point in time restore only supports the deployment of the new server in the same region in which the source server exists. | Compliance, data residency, pricing, proximity to your users, or availability of other services in the same region, are some of the requirements you should use when choosing the region. | The service doesn't offer a feature to automatically and transparently relocate an instance to a different region. |
    | | **PostgreSQL version** | The version selected by default. | Point in time restore only supports the deployment of the new server with the exact same major version used by the source server. Currently those versions are: **[!INCLUDE [major-versions-ascending](includes/major-versions-ascending.md)]** | Azure Database for PostgreSQL - Flexible Server supports in-place upgrade, via [major version upgrade](how-to-perform-major-version-upgrade.md). |
    | | **Availability zone** | Your preferred [availability zone](/azure/reliability/availability-zones-overview). | You can choose in which availability zone you want your server to be deployed. Being able to choose the availability zone in which your instance is deployed, is useful to colocate it with your application. If you choose *No preference*, a default availability zone is automatically assigned to your instance during its creation. | Although the availability zone in which an instance is deployed can't be changed after its creation, you can use the [point in time recovery](concepts-backup-restore.md#point-in-time-recovery) feature to restore the server under a different name on a different availability zone. |
    | | **Compute + storage** | Assigns the same type and size of compute and same size of storage, as the ones used by the source server at the time the backup is restored. However, if you select the **Configure server** link, you can change the type of storage allocated to the new server, and whether or not it should be provisioned with geo-redundant backups. | | After the new server is deployed, its compute options can be scaled up or down. |

6. If you want to change the type of storage assigned to the new server, or if you want to deploy it with geo-redundant backups, select **Configure server**:

    :::image type="content" source="./media/how-to-restore-server/configure-server-button.png" alt-text="Screenshot showing the location of the Configure server link." lightbox="./media/how-to-restore-server/configure-server-button.png":::

7. The **Compute + storage** opens to show compute and storage options for the new server:

    :::image type="content" source="./media/how-to-restore-server/configure-server-page.png" alt-text="Screenshot showing the Compute + storage page." lightbox="./media/how-to-restore-server/configure-server-page.png":::

8. Use the following table to understand the meaning of the different fields available in the **Compute + storage** page, and as guidance to fill the page:

    | Section | Setting | Suggested value | Description | Can be changed after instance creation |
    | --- | --- | --- | --- | --- |
    | **Compute** | | | | |
    | | **Compute tier** | Can't be changed and is automatically set to the same value as the source server. | Possible values are **Burstable** (typically used for development environments in which workloads don't need the full capacity of the CPU continuously) and **General Purpose** (typically used for production environments with most common workloads), and **Memory Optimized** (typically used for production environments running workloads that require a high memory to CPU ratio). For more information, see [Compute options in Azure Database for PostgreSQL - Flexible Server](concepts-compute.md). | Can be changed after the server is created. However, if you're using some functionality which is only supported on certain tiers and change the current tier to one in which the feature isn't supported, the feature stops being available or gets disabled. |
    | | **Compute size** | Can't be changed and is automatically set to the same value as the source server. | Notice that the list of supported values might vary across regions, depending on the hardware available on each region. For more information, see [Compute options in Azure Database for PostgreSQL - Flexible Server](concepts-compute.md). | Can be changed after instance is created. |
    | **Storage** | | | | |
    | | **Storage type** | Select **Premium SSD**. | Notice that the list of allowed values might vary depending on which other features you selected. For more information, see [Storage options in Azure Database for PostgreSQL - Flexible Server](concepts-storage.md). | Can't be changed after the instance is created. |
    | | **Storage size** | Can't be changed and is automatically set to the same value as the source server. | Notice that the list of supported values might vary across regions, depending on the hardware available on each region. For more information, see [Compute options in Azure Database for PostgreSQL - Flexible Server](concepts-compute.md). | Can be changed after the instance is created. It can only be increased. Manual or automatic shrinking of storage isn't supported. Acceptable values depend on the type of storage assigned to the instance. |
    | | **Performance Tier** | Can't be changed and is automatically set to the same value as the source server. | Performance of Premium solid-state drives (SSD) is set when you create the disk, in the form of their performance tier. When setting the provisioned size of the disk, a performance tier is automatically selected. This performance tier determines the IOPS and throughput of your managed disk. For Premium SSD disks, this tier can be changed at deployment or afterwards, without changing the size of the disk, and without downtime. Changing the tier allows you to prepare for and meet higher demand without using your disk's bursting capability. It can be more cost-effective to change your performance tier rather than rely on bursting, depending on how long the extra performance is necessary. This is ideal for events that temporarily require a consistently higher level of performance. Events like holiday shopping, performance testing, or running a training environment. To handle these events, you can switch a disk to a higher performance tier without downtime, for as long as you need the extra performance. You can then return to the original tier without downtime when the extra performance is no longer necessary. | Can be changed after the instance is created. |
    | | **Storage Auto-growth** | Can't be changed and is automatically set to the same value as the source server. | Notice that this option might not be supported for some storage types, and it might not be honored for certain storage sizes. For more information, see [Configure storage autogrow in an Azure Database for PostgreSQL flexible server](how-to-auto-grow-storage.md). | Can be changed after the instance is created, as long as the storage type supports this feature. |
    | **Backups** | | | | |
    | | **Backup retention period (in days)** | Can't be changed and is automatically set to the same value as the source server. | The default backup retention period is 7 days, but you can extend the period to a maximum of 35 days. | Can be changed after instance is created. |
    | | **Backup Redundancy Options** | Automatically selected for you, based on the configuration of high availability and geo-redundancy of backups. | Possible values are **Locally redundant** (provides at least 99.999999999% durability of backup objects over a year), **Zone redundant** (provides at least 99.9999999999% durability of backup objects over a year), and **Geo-Redundant** (provides at least 99.99999999999999% durability of backup objects over a year). When **Geo-redundancy** is enabled for the backup, then the backup redundancy option is set to **Geo-Redundant**. Otherwise, if high availability is set to **Disabled** or **Same zone**, then backup redundancy is set to **Locally redundant**. And if high availability is set to **Zone redundant**, then backup redundancy is set to **Zone redundant**. For more information, see [Backup redundancy options in Azure Database for PostgreSQL - Flexible Server](concepts-backup-restore.md#backup-redundancy-options). | Can't be changed after instance is created. |
    | | **Geo-redundancy** | Leave this option disabled. | Geo-redundancy in backups is only supported on instances deployed in any of the [Azure paired regions](/azure/reliability/cross-region-replication-azure). For more information, see [Geo-redundant backup and restore in Azure Database for PostgreSQL - Flexible Server](concepts-backup-restore.md#geo-redundant-backup-and-restore)| Can't be changed after instance is created. |

9. Once all the new server is configured to your needs, select **Review + create**.

    :::image type="content" source="./media/how-to-restore-server/restore-point-review-create.png" alt-text="Screenshot showing the location of the Review + create button." lightbox="./media/how-to-restore-server/restore-point-review-create.png":::

10. Review that all configurations for the new deployment are correctly set, and select **Create**.

    :::image type="content" source="./media/how-to-restore-server/restore-point-create.png" alt-text="Screenshot showing the location of the Create button." lightbox="./media/how-to-restore-server/restore-point-create.png":::

11. A new deployment is launched to create your new Azure Database for PostgreSQL flexible server and restore the most recent data available on the source server at the time of restore:

    :::image type="content" source="./media/how-to-restore-server/restore-point-deployment-progress.png" alt-text="Screenshot that shows the deployment in progress to create your new Azure Database for PostgreSQL Flexible server, on which the most recent data available on the source server is restored." lightbox="./media/how-to-restore-server/restore-point-deployment-progress.png":::

12. When the deployment completes, you can select **Go to resource**, to get you to the **Overview** page of your new Azure Database for PostgreSQL flexible server, and start using it:

    :::image type="content" source="./media/how-to-restore-server/restore-point-deployment-completed.png" alt-text="Screenshot that shows the deployment successfully completed of your Azure Database for PostgreSQL Flexible server." lightbox="./media/how-to-restore-server/restore-point-deployment-completed.png":::

### [CLI](#tab/cli-restore-latest-point)

You can restore a backup of a server to the latest restore point via the [az postgres flexible-server restore](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-restore) command.

```azurecli-interactive
az postgres flexible-server restore --resource-group <resource_group> --name <server> --source-server <source_server>
```

> [!NOTE]
> The `az postgres flexible-server restore` command accepts a `--restore-time` parameter. That parameter can be passed a value that represents the point in time, in UTC, to restore from (ISO8601 format). One example valid value would be `2025-04-26T02:10:00+00:00`. However, when that parameter isn't present, its value defaults to the current time in the system from where the command is executed.

---

## Restore to a custom restore point

### [Portal](#tab/portal-restore-custom-point)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

2. In the resource menu, select **Overview**.

    :::image type="content" source="./media/how-to-restore-server/overview.png" alt-text="Screenshot showing the Overview page." lightbox="./media/how-to-restore-server/overview.png":::

3. Select the **Restore** button.

    :::image type="content" source="./media/how-to-restore-server/restore-button.png" alt-text="Screenshot showing the location of the Restore button in the Overview page." lightbox="./media/how-to-restore-server/restore-button.png":::

4. You're redirected to the **Create Azure Database for PostgreSQL Flexible server - Restore server** wizard, from where you can configure some settings for the new server that is created. After the new server is deployed, the most recent snapshot of the source server data disk is restored. In the **Point-in-time-restore (PITR)** section, select **Select a custom restore point**.

    :::image type="content" source="./media/how-to-restore-server/custom-restore-point.png" alt-text="Screenshot showing the Select a custom restore point radio button selected." lightbox="./media/how-to-restore-server/custom-restore-point.png":::

5. In **Custom restore point (UTC)**, select a date from the calendar control, and specify a time in the time text box.

    :::image type="content" source="./media/how-to-restore-server/custom-restore-point-date-time.png" alt-text="Screenshot showing the date picker and time textbox, available to configure the custom restore point." lightbox="./media/how-to-restore-server/custom-restore-point-date-time.png":::

> [!NOTE]
> Selectable dates in the calendar control are restricted to the ones covering the range from the day in which the oldest available backup was taken until now.
> If you select a time which, when combined with the selected date, falls outside the period ranging from the earliest restore point and the time (UTC) at which you landed in the **Create Azure Database for PostgreSQL Flexible Server - Restore server** wizard, and error asks you to adjust the value.

6. Use the following table to understand the meaning of the different fields available in the **Basics** page, and as guidance to fill the page:

    | Section | Setting | Suggested value | Description | Can be changed after instance creation |
    | --- | --- | --- | --- | --- |
    | **Project details** | | | | |
    | | **Subscription** | The name of the [subscription](/microsoft-365/enterprise/subscriptions-licenses-accounts-and-tenants-for-microsoft-cloud-offerings#subscriptions) in which you want to create the resource. | A subscription is an agreement with Microsoft to use one or more Microsoft cloud platforms or services, for which charges accrue based on either a per-user license fee or on cloud-based resource consumption. | An existing Azure Database for PostgreSQL flexible server instance can be moved to a different subscription from the one it was originally created. For more information, see Move [Azure resources to a new resource group or subscription](/azure/azure-resource-manager/management/move-resource-group-and-subscription). |
    | | **Resource group** | The [resource group](/azure/azure-resource-manager/management/manage-resource-groups-portal#what-is-a-resource-group) in the selected subscription, in which you want to create the resource. It can be an existing resource group, or you can select **Create new**, and provide a name in that subscription which is unique among the existing resource group names. | A resource group is a container that holds related resources for an Azure solution. The resource group can include all the resources for the solution, or only those resources that you want to manage as a group. You decide how you want to allocate resources to resource groups based on what makes the most sense for your organization. Generally, add resources that share the same lifecycle to the same resource group so you can easily deploy, update, and delete them as a group | An existing Azure Database for PostgreSQL flexible server instance can be moved to a different subscription from the one it was originally created. For more information, see Move [Azure resources to a new resource group or subscription](/azure/azure-resource-manager/management/move-resource-group-and-subscription). |
    | **Source details** | | | | |
    | | **Source server** | The name of the server whose backup you want to restore on the newly deployed server. | | |
    | | **Geo-redundant restore** | If the source server was created with [geo-redundant backups](concepts-backup-restore.md#geo-redundant-backup-and-restore), this option would be enabled. If it's enabled, you could restore a backup kept in the storage account of the paired region to create a new server in that other region. | | |
    | | **Earliest restore point** | The oldest backup of the source server available to restore from. the server whose backup you want to restore on the newly deployed server. Backups are automatically deleted, based on the backup retention period configured on the source server. | | |
    | | **Point-in-time-restore (PITR)** | Possible options are **Latest restore point (Now)**, **Select a custom restore point**, and **Select Fast restore point (Restore using full backup only)**. | To restore to latest restore point, select **Latest restore point (Now)**. | |
    | **Server details** | | | | |
    | | **Name** | The name that you want to assign to the newly deployed server, on top of which a backup of the source is restored. | A unique name that identifies your Azure Database for PostgreSQL flexible server instance. The domain name `postgres.database.azure.com` is appended to the server name you provide, to conform the fully qualified host name by which you can use a Domain Naming System server to resolve the IP address of your instance. | Although the server name can't be changed after server creation, you can use the [point in time recovery](concepts-backup-restore.md#point-in-time-recovery) feature, to restore the server under a different name. An alternative approach to continue using the existing server, but being able to refer to it using a different server name, would use the [virtual endpoints](concepts-read-replicas-virtual-endpoints.md) to create a writer endpoint with the new desired name. With this approach, you could refer to the instance by its original name, or that assigned to the write virtual endpoint. |
    | | **Location** | The name of one of the [regions in which the service is supported](overview.md#azure-regions). Point in time restore only supports the deployment of the new server in the same region in which the source server exists. | Compliance, data residency, pricing, proximity to your users, or availability of other services in the same region, are some of the requirements you should use when choosing the region. | The service doesn't offer a feature to automatically and transparently relocate an instance to a different region. |
    | | **PostgreSQL version** | The version selected by default. | Point in time restore only supports the deployment of the new server with the exact same major version used by the source server. Currently those versions are: **[!INCLUDE [major-versions-ascending](includes/major-versions-ascending.md)]** | Azure Database for PostgreSQL - Flexible Server supports in-place upgrade, via [major version upgrade](how-to-perform-major-version-upgrade.md). |
    | | **Availability zone** | Your preferred [availability zone](/azure/reliability/availability-zones-overview). | You can choose in which availability zone you want your server to be deployed. Being able to choose the availability zone in which your instance is deployed, is useful to colocate it with your application. If you choose *No preference*, a default availability zone is automatically assigned to your instance during its creation. | Although the availability zone in which an instance is deployed can't be changed after its creation, you can use the [point in time recovery](concepts-backup-restore.md#point-in-time-recovery) feature to restore the server under a different name on a different availability zone. |
    | | **Compute + storage** | Assigns the same type and size of compute and same size of storage, as the ones used by the source server at the time the backup is restored. However, if you select the **Configure server** link, you can change the type of storage allocated to the new server, and whether or not it should be provisioned with geo-redundant backups. | | After the new server is deployed, its compute options can be scaled up or down. |

7. If you want to change the type of storage assigned to the new server, or if you want to deploy it with geo-redundant backups, select **Configure server**:

    :::image type="content" source="./media/how-to-restore-server/configure-server-button.png" alt-text="Screenshot showing the location of the Configure server link." lightbox="./media/how-to-restore-server/configure-server-button.png":::

8. The **Compute + storage** opens to show compute and storage options for the new server:

    :::image type="content" source="./media/how-to-restore-server/configure-server-page.png" alt-text="Screenshot showing the Compute + storage page." lightbox="./media/how-to-restore-server/configure-server-page.png":::

9. Use the following table to understand the meaning of the different fields available in the **Compute + storage** page, and as guidance to fill the page:

    | Section | Setting | Suggested value | Description | Can be changed after instance creation |
    | --- | --- | --- | --- | --- |
    | **Compute** | | | | |
    | | **Compute tier** | Can't be changed and is automatically set to the same value as the source server. | Possible values are **Burstable** (typically used for development environments in which workloads don't need the full capacity of the CPU continuously) and **General Purpose** (typically used for production environments with most common workloads), and **Memory Optimized** (typically used for production environments running workloads that require a high memory to CPU ratio). For more information, see [Compute options in Azure Database for PostgreSQL - Flexible Server](concepts-compute.md). | Can be changed after the server is created. However, if you're using some functionality which is only supported on certain tiers and change the current tier to one in which the feature isn't supported, the feature stops being available or gets disabled. |
    | | **Compute size** | Can't be changed and is automatically set to the same value as the source server. | Notice that the list of supported values might vary across regions, depending on the hardware available on each region. For more information, see [Compute options in Azure Database for PostgreSQL - Flexible Server](concepts-compute.md). | Can be changed after instance is created. |
    | **Storage** | | | | |
    | | **Storage type** | Select **Premium SSD**. | Notice that the list of allowed values might vary depending on which other features you selected. For more information, see [Storage options in Azure Database for PostgreSQL - Flexible Server](concepts-storage.md). | Can't be changed after the instance is created. |
    | | **Storage size** | Can't be changed and is automatically set to the same value as the source server. | Notice that the list of supported values might vary across regions, depending on the hardware available on each region. For more information, see [Compute options in Azure Database for PostgreSQL - Flexible Server](concepts-compute.md). | Can be changed after the instance is created. It can only be increased. Manual or automatic shrinking of storage isn't supported. Acceptable values depend on the type of storage assigned to the instance. |
    | | **Performance Tier** | Can't be changed and is automatically set to the same value as the source server. | Performance of Premium solid-state drives (SSD) is set when you create the disk, in the form of their performance tier. When setting the provisioned size of the disk, a performance tier is automatically selected. This performance tier determines the IOPS and throughput of your managed disk. For Premium SSD disks, this tier can be changed at deployment or afterwards, without changing the size of the disk, and without downtime. Changing the tier allows you to prepare for and meet higher demand without using your disk's bursting capability. It can be more cost-effective to change your performance tier rather than rely on bursting, depending on how long the extra performance is necessary. This is ideal for events that temporarily require a consistently higher level of performance. Events like holiday shopping, performance testing, or running a training environment. To handle these events, you can switch a disk to a higher performance tier without downtime, for as long as you need the extra performance. You can then return to the original tier without downtime when the extra performance is no longer necessary. | Can be changed after the instance is created. |
    | | **Storage Auto-growth** | Can't be changed and is automatically set to the same value as the source server. | Notice that this option might not be supported for some storage types, and it might not be honored for certain storage sizes. For more information, see [Configure storage autogrow in an Azure Database for PostgreSQL flexible server](how-to-auto-grow-storage.md). | Can be changed after the instance is created, as long as the storage type supports this feature. |
    | **Backups** | | | | |
    | | **Backup retention period (in days)** | Can't be changed and is automatically set to the same value as the source server. | The default backup retention period is 7 days, but you can extend the period to a maximum of 35 days. | Can be changed after instance is created. |
    | | **Backup Redundancy Options** | Automatically selected for you, based on the configuration of high availability and geo-redundancy of backups. | Possible values are **Locally redundant** (provides at least 99.999999999% durability of backup objects over a year), **Zone redundant** (provides at least 99.9999999999% durability of backup objects over a year), and **Geo-Redundant** (provides at least 99.99999999999999% durability of backup objects over a year). When **Geo-redundancy** is enabled for the backup, then the backup redundancy option is set to **Geo-Redundant**. Otherwise, if high availability is set to **Disabled** or **Same zone**, then backup redundancy is set to **Locally redundant**. And if high availability is set to **Zone redundant**, then backup redundancy is set to **Zone redundant**. For more information, see [Backup redundancy options in Azure Database for PostgreSQL - Flexible Server](concepts-backup-restore.md#backup-redundancy-options). | Can't be changed after instance is created. |
    | | **Geo-redundancy** | Leave this option disabled. | Geo-redundancy in backups is only supported on instances deployed in any of the [Azure paired regions](/azure/reliability/cross-region-replication-azure). For more information, see [Geo-redundant backup and restore in Azure Database for PostgreSQL - Flexible Server](concepts-backup-restore.md#geo-redundant-backup-and-restore)| Can't be changed after instance is created. |

10. Once all the new server is configured to your needs, select **Review + create**.

    :::image type="content" source="./media/how-to-restore-server/restore-point-review-create.png" alt-text="Screenshot showing the location of the Review + create button." lightbox="./media/how-to-restore-server/restore-point-review-create.png":::

11. Review that all configurations for the new deployment are correctly set, and select **Create**.

    :::image type="content" source="./media/how-to-restore-server/restore-point-create.png" alt-text="Screenshot showing the location of the Create button." lightbox="./media/how-to-restore-server/restore-point-create.png":::

12. A new deployment is launched to create your new Azure Database for PostgreSQL flexible server and restore the most recent data available on the source server at the time of restore:

    :::image type="content" source="./media/how-to-restore-server/restore-point-deployment-progress.png" alt-text="Screenshot that shows the deployment in progress to create your new Azure Database for PostgreSQL Flexible server, on which the most recent data available on the source server is restored." lightbox="./media/how-to-restore-server/restore-point-deployment-progress.png":::

13. When the deployment completes, you can select **Go to resource**, to get you to the **Overview** page of your new Azure Database for PostgreSQL flexible server, and start using it:

    :::image type="content" source="./media/how-to-restore-server/restore-point-deployment-completed.png" alt-text="Screenshot that shows the deployment successfully completed of your Azure Database for PostgreSQL Flexible server." lightbox="./media/how-to-restore-server/restore-point-deployment-completed.png":::

### [CLI](#tab/cli-restore-custom-point)

You can restore a backup of a server to the latest restore point via the [az postgres flexible-server restore](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-restore) command.

```azurecli-interactive
az postgres flexible-server restore --resource-group <resource_group> --name <server> --source-server <source_server> --restore-time 2025-04-26T02:10:00+00:00
```

> [!NOTE]
> - The value passed to the `--restore-time` parameter represents the point in time, in UTC, to restore from (ISO8601 format).
> - If the `--restore-time` parameter isn't present, its value defaults to the current time in the system from where the command is executed.
> - If the value passed is in the future, the backend service that receives the request normalizes it to the current date and time.
> - If the value passed is earlier than the earliest restore point available on the source server, you receive an InternalServerError.

---

## Restore of a full backup (fast restore)

### [Portal](#tab/portal-restore-full-backup)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

2. In the resource menu, select **Overview**.

    :::image type="content" source="./media/how-to-restore-server/overview.png" alt-text="Screenshot showing the Overview page." lightbox="./media/how-to-restore-server/overview.png":::

3. Select the **Restore** button.

    :::image type="content" source="./media/how-to-restore-server/restore-button.png" alt-text="Screenshot showing the location of the Restore button in the Overview page." lightbox="./media/how-to-restore-server/restore-button.png":::

4. You're redirected to the **Create Azure Database for PostgreSQL Flexible server - Restore server** wizard, from where you can configure some settings for the new server that is created. After the new server is deployed, the most recent snapshot of the source server data disk is restored. In the **Point-in-time-restore (PITR)** section, select **Select Fast restore point (Restore using full backup only)**.

    :::image type="content" source="./media/how-to-restore-server/fast-restore-point.png" alt-text="Screenshot showing the Select Fast restore point (Restore using full backup only) radio button selected." lightbox="./media/how-to-restore-server/fast-restore-point.png":::

5. In **Fast Restore point (UTC)**, select the timestamp of any of the full backups available to restore. The list includes the full backups that the service takes automatically, and any [on-demand backups](how-to-operate-on-demand-backups.md) taken by the user.

    :::image type="content" source="./media/how-to-restore-server/fast-restore-point-selection.png" alt-text="Screenshot showing the Fast Restore point (UTC) combobox, available to select fast restore points." lightbox="./media/how-to-restore-server/fast-restore-point-selection.png":::

6. Use the following table to understand the meaning of the different fields available in the **Basics** page, and as guidance to fill the page:

    | Section | Setting | Suggested value | Description | Can be changed after instance creation |
    | --- | --- | --- | --- | --- |
    | **Project details** | | | | |
    | | **Subscription** | The name of the [subscription](/microsoft-365/enterprise/subscriptions-licenses-accounts-and-tenants-for-microsoft-cloud-offerings#subscriptions) in which you want to create the resource. | A subscription is an agreement with Microsoft to use one or more Microsoft cloud platforms or services, for which charges accrue based on either a per-user license fee or on cloud-based resource consumption. | An existing Azure Database for PostgreSQL flexible server instance can be moved to a different subscription from the one it was originally created. For more information, see Move [Azure resources to a new resource group or subscription](/azure/azure-resource-manager/management/move-resource-group-and-subscription). |
    | | **Resource group** | The [resource group](/azure/azure-resource-manager/management/manage-resource-groups-portal#what-is-a-resource-group) in the selected subscription, in which you want to create the resource. It can be an existing resource group, or you can select **Create new**, and provide a name in that subscription which is unique among the existing resource group names. | A resource group is a container that holds related resources for an Azure solution. The resource group can include all the resources for the solution, or only those resources that you want to manage as a group. You decide how you want to allocate resources to resource groups based on what makes the most sense for your organization. Generally, add resources that share the same lifecycle to the same resource group so you can easily deploy, update, and delete them as a group | An existing Azure Database for PostgreSQL flexible server instance can be moved to a different subscription from the one it was originally created. For more information, see Move [Azure resources to a new resource group or subscription](/azure/azure-resource-manager/management/move-resource-group-and-subscription). |
    | **Source details** | | | | |
    | | **Source server** | The name of the server whose backup you want to restore on the newly deployed server. | | |
    | | **Geo-redundant restore** | If the source server was created with [geo-redundant backups](concepts-backup-restore.md#geo-redundant-backup-and-restore), this option would be enabled. If it's enabled, you could restore a backup kept in the storage account of the paired region to create a new server in that other region. | | |
    | | **Earliest restore point** | The oldest backup of the source server available to restore from. the server whose backup you want to restore on the newly deployed server. Backups are automatically deleted, based on the backup retention period configured on the source server. | | |
    | | **Point-in-time-restore (PITR)** | Possible options are **Latest restore point (Now)**, **Select a custom restore point**, and **Select Fast restore point (Restore using full backup only)**. | To restore to latest restore point, select **Latest restore point (Now)**. | |
    | **Server details** | | | | |
    | | **Name** | The name that you want to assign to the newly deployed server, on top of which a backup of the source is restored. | A unique name that identifies your Azure Database for PostgreSQL flexible server instance. The domain name `postgres.database.azure.com` is appended to the server name you provide, to conform the fully qualified host name by which you can use a Domain Naming System server to resolve the IP address of your instance. | Although the server name can't be changed after server creation, you can use the [point in time recovery](concepts-backup-restore.md#point-in-time-recovery) feature, to restore the server under a different name. An alternative approach to continue using the existing server, but being able to refer to it using a different server name, would use the [virtual endpoints](concepts-read-replicas-virtual-endpoints.md) to create a writer endpoint with the new desired name. With this approach, you could refer to the instance by its original name, or that assigned to the write virtual endpoint. |
    | | **Location** | The name of one of the [regions in which the service is supported](overview.md#azure-regions). Point in time restore only supports the deployment of the new server in the same region in which the source server exists. | Compliance, data residency, pricing, proximity to your users, or availability of other services in the same region, are some of the requirements you should use when choosing the region. | The service doesn't offer a feature to automatically and transparently relocate an instance to a different region. |
    | | **PostgreSQL version** | The version selected by default. | Point in time restore only supports the deployment of the new server with the exact same major version used by the source server. Currently those versions are: **[!INCLUDE [major-versions-ascending](includes/major-versions-ascending.md)]** | Azure Database for PostgreSQL - Flexible Server supports in-place upgrade, via [major version upgrade](how-to-perform-major-version-upgrade.md). |
    | | **Availability zone** | Your preferred [availability zone](/azure/reliability/availability-zones-overview). | You can choose in which availability zone you want your server to be deployed. Being able to choose the availability zone in which your instance is deployed, is useful to colocate it with your application. If you choose *No preference*, a default availability zone is automatically assigned to your instance during its creation. | Although the availability zone in which an instance is deployed can't be changed after its creation, you can use the [point in time recovery](concepts-backup-restore.md#point-in-time-recovery) feature to restore the server under a different name on a different availability zone. |
    | | **Compute + storage** | Assigns the same type and size of compute and same size of storage, as the ones used by the source server at the time the backup is restored. However, if you select the **Configure server** link, you can change the type of storage allocated to the new server, and whether or not it should be provisioned with geo-redundant backups. | | After the new server is deployed, its compute options can be scaled up or down. |

7. If you want to change the type of storage assigned to the new server, or if you want to deploy it with geo-redundant backups, select **Configure server**:

    :::image type="content" source="./media/how-to-restore-server/configure-server-button.png" alt-text="Screenshot showing the location of the Configure server link." lightbox="./media/how-to-restore-server/configure-server-button.png":::

8. The **Compute + storage** opens to show compute and storage options for the new server:

    :::image type="content" source="./media/how-to-restore-server/configure-server-page.png" alt-text="Screenshot showing the Compute + storage page." lightbox="./media/how-to-restore-server/configure-server-page.png":::

9. Use the following table to understand the meaning of the different fields available in the **Compute + storage** page, and as guidance to fill the page:

    | Section | Setting | Suggested value | Description | Can be changed after instance creation |
    | --- | --- | --- | --- | --- |
    | **Compute** | | | | |
    | | **Compute tier** | Can't be changed and is automatically set to the same value as the source server. | Possible values are **Burstable** (typically used for development environments in which workloads don't need the full capacity of the CPU continuously) and **General Purpose** (typically used for production environments with most common workloads), and **Memory Optimized** (typically used for production environments running workloads that require a high memory to CPU ratio). For more information, see [Compute options in Azure Database for PostgreSQL - Flexible Server](concepts-compute.md). | Can be changed after the server is created. However, if you're using some functionality which is only supported on certain tiers and change the current tier to one in which the feature isn't supported, the feature stops being available or gets disabled. |
    | | **Compute size** | Can't be changed and is automatically set to the same value as the source server. | Notice that the list of supported values might vary across regions, depending on the hardware available on each region. For more information, see [Compute options in Azure Database for PostgreSQL - Flexible Server](concepts-compute.md). | Can be changed after instance is created. |
    | **Storage** | | | | |
    | | **Storage type** | Select **Premium SSD**. | Notice that the list of allowed values might vary depending on which other features you selected. For more information, see [Storage options in Azure Database for PostgreSQL - Flexible Server](concepts-storage.md). | Can't be changed after the instance is created. |
    | | **Storage size** | Can't be changed and is automatically set to the same value as the source server. | Notice that the list of supported values might vary across regions, depending on the hardware available on each region. For more information, see [Compute options in Azure Database for PostgreSQL - Flexible Server](concepts-compute.md). | Can be changed after the instance is created. It can only be increased. Manual or automatic shrinking of storage isn't supported. Acceptable values depend on the type of storage assigned to the instance. |
    | | **Performance Tier** | Can't be changed and is automatically set to the same value as the source server. | Performance of Premium solid-state drives (SSD) is set when you create the disk, in the form of their performance tier. When setting the provisioned size of the disk, a performance tier is automatically selected. This performance tier determines the IOPS and throughput of your managed disk. For Premium SSD disks, this tier can be changed at deployment or afterwards, without changing the size of the disk, and without downtime. Changing the tier allows you to prepare for and meet higher demand without using your disk's bursting capability. It can be more cost-effective to change your performance tier rather than rely on bursting, depending on how long the extra performance is necessary. This is ideal for events that temporarily require a consistently higher level of performance. Events like holiday shopping, performance testing, or running a training environment. To handle these events, you can switch a disk to a higher performance tier without downtime, for as long as you need the extra performance. You can then return to the original tier without downtime when the extra performance is no longer necessary. | Can be changed after the instance is created. |
    | | **Storage Auto-growth** | Can't be changed and is automatically set to the same value as the source server. | Notice that this option might not be supported for some storage types, and it might not be honored for certain storage sizes. For more information, see [Configure storage autogrow in an Azure Database for PostgreSQL flexible server](how-to-auto-grow-storage.md). | Can be changed after the instance is created, as long as the storage type supports this feature. |
    | **Backups** | | | | |
    | | **Backup retention period (in days)** | Can't be changed and is automatically set to the same value as the source server. | The default backup retention period is 7 days, but you can extend the period to a maximum of 35 days. | Can be changed after instance is created. |
    | | **Backup Redundancy Options** | Automatically selected for you, based on the configuration of high availability and geo-redundancy of backups. | Possible values are **Locally redundant** (provides at least 99.999999999% durability of backup objects over a year), **Zone redundant** (provides at least 99.9999999999% durability of backup objects over a year), and **Geo-Redundant** (provides at least 99.99999999999999% durability of backup objects over a year). When **Geo-redundancy** is enabled for the backup, then the backup redundancy option is set to **Geo-Redundant**. Otherwise, if high availability is set to **Disabled** or **Same zone**, then backup redundancy is set to **Locally redundant**. And if high availability is set to **Zone redundant**, then backup redundancy is set to **Zone redundant**. For more information, see [Backup redundancy options in Azure Database for PostgreSQL - Flexible Server](concepts-backup-restore.md#backup-redundancy-options). | Can't be changed after instance is created. |
    | | **Geo-redundancy** | Leave this option disabled. | Geo-redundancy in backups is only supported on instances deployed in any of the [Azure paired regions](/azure/reliability/cross-region-replication-azure). For more information, see [Geo-redundant backup and restore in Azure Database for PostgreSQL - Flexible Server](concepts-backup-restore.md#geo-redundant-backup-and-restore)| Can't be changed after instance is created. |

10. Once all the new server is configured to your needs, select **Review + create**.

    :::image type="content" source="./media/how-to-restore-server/restore-point-review-create.png" alt-text="Screenshot showing the location of the Review + create button." lightbox="./media/how-to-restore-server/restore-point-review-create.png":::

11. Review that all configurations for the new deployment are correctly set, and select **Create**.

    :::image type="content" source="./media/how-to-restore-server/restore-point-create.png" alt-text="Screenshot showing the location of the Create button." lightbox="./media/how-to-restore-server/restore-point-create.png":::

12. A new deployment is launched to create your new Azure Database for PostgreSQL flexible server and restore the most recent data available on the source server at the time of restore:

    :::image type="content" source="./media/how-to-restore-server/restore-point-deployment-progress.png" alt-text="Screenshot that shows the deployment in progress to create your new Azure Database for PostgreSQL Flexible server, on which the most recent data available on the source server is restored." lightbox="./media/how-to-restore-server/restore-point-deployment-progress.png":::

13. When the deployment completes, you can select **Go to resource**, to get you to the **Overview** page of your new Azure Database for PostgreSQL flexible server, and start using it:

    :::image type="content" source="./media/how-to-restore-server/restore-point-deployment-completed.png" alt-text="Screenshot that shows the deployment successfully completed of your Azure Database for PostgreSQL Flexible server." lightbox="./media/how-to-restore-server/restore-point-deployment-completed.png":::

### [CLI](#tab/cli-restore-full-backup)

First, you need to identify the backup that you want to restore, and fetch the exact date and time when it completed. For that, you can use the [az postgres flexible-server backup list](/cli/azure/postgres/flexible-server/backup#az-postgres-flexible-server-backup-list) command.

```azurecli-interactive
az postgres flexible-server backup list --resource-group <resource_group> --name <server> --query sort_by([].{name:name, backupType:backupType, completedTime:completedTime, source:source}, &completedTime) --output table
```

Once you have the completion time of the full backup that you want to restore, you can restore the backup via the [az postgres flexible-server restore](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-restore) command.

```azurecli-interactive
az postgres flexible-server restore --resource-group <resource_group> --name <server> --source-server <source_server> --restore-time <backup_completed_time>
```

> [!NOTE]
> - The value passed to the `--restore-time` parameter represents the point in time, in UTC, to restore from (ISO8601 format).
> - If the `--restore-time` parameter isn't present, its value defaults to the current time in the system from where the command is executed.
> - If the value passed is in the future, the backend service that receives the request normalizes it to the current date and time.
> - If the value passed is earlier than the earliest restore point available on the source server, you receive an InternalServerError.

---

## Restore to a paired region (geo-restore)

When you create a server with geo-redundant backup enabled, it can take up to one hour to create the initial backup and asynchronously transfer the physical copy to the paired region.

If you attempt to perform a geo-restore while there's not even one backup available in the paired region, you receive the following error:
```output
Error: Unable to geo-restore server <server> as its geo-backups aren't available yet.
```

If the server whose backups you're trying to restore is configured with [Private access (VNET Integration)](concepts-networking-private.md) networking mode, you can only restore to another virtual network in the remote region. You can restore your server into an existing virtual network or you can create a new virtual network.

### [Portal](#tab/portal-restore-geo-restore)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

2. In the resource menu, select **Overview**.

    :::image type="content" source="./media/how-to-restore-server/overview.png" alt-text="Screenshot showing the Overview page." lightbox="./media/how-to-restore-server/overview.png":::

3. Select the **Restore** button.

    :::image type="content" source="./media/how-to-restore-server/restore-button.png" alt-text="Screenshot showing the location of the Restore button in the Overview page." lightbox="./media/how-to-restore-server/restore-button.png":::

4. You're redirected to the **Create Azure Database for PostgreSQL Flexible server - Restore server** wizard, from where you can configure some settings for the new server that is created. After the new server is deployed, the most recent snapshot of the source server data disk is restored. In the **Geo-redundant restore** section, select **Restore to paired region (<paired_region>)**.

    :::image type="content" source="./media/how-to-restore-server/geo-redundant-restore.png" alt-text="Screenshot showing the Geo-redundant restore option selected." lightbox="./media/how-to-restore-server/geo-redundant-restore.png":::

> [!NOTE]
> Geo-redundant restore from the portal doesn't support setting the time that defines the recovery point objective. It automatically configures that value to the time at which you landed in the **Create Azure Database for PostgreSQL Flexible server - Restore server** wizard.

5. Use the following table to understand the meaning of the different fields available in the **Basics** page, and as guidance to fill the page:

    | Section | Setting | Suggested value | Description | Can be changed after instance creation |
    | --- | --- | --- | --- | --- |
    | **Project details** | | | | |
    | | **Subscription** | The name of the [subscription](/microsoft-365/enterprise/subscriptions-licenses-accounts-and-tenants-for-microsoft-cloud-offerings#subscriptions) in which you want to create the resource. | A subscription is an agreement with Microsoft to use one or more Microsoft cloud platforms or services, for which charges accrue based on either a per-user license fee or on cloud-based resource consumption. | An existing Azure Database for PostgreSQL flexible server instance can be moved to a different subscription from the one it was originally created. For more information, see Move [Azure resources to a new resource group or subscription](/azure/azure-resource-manager/management/move-resource-group-and-subscription). |
    | | **Resource group** | The [resource group](/azure/azure-resource-manager/management/manage-resource-groups-portal#what-is-a-resource-group) in the selected subscription, in which you want to create the resource. It can be an existing resource group, or you can select **Create new**, and provide a name in that subscription which is unique among the existing resource group names. | A resource group is a container that holds related resources for an Azure solution. The resource group can include all the resources for the solution, or only those resources that you want to manage as a group. You decide how you want to allocate resources to resource groups based on what makes the most sense for your organization. Generally, add resources that share the same lifecycle to the same resource group so you can easily deploy, update, and delete them as a group | An existing Azure Database for PostgreSQL flexible server instance can be moved to a different subscription from the one it was originally created. For more information, see Move [Azure resources to a new resource group or subscription](/azure/azure-resource-manager/management/move-resource-group-and-subscription). |
    | **Source details** | | | | |
    | | **Source server** | The name of the server whose backup you want to restore on the newly deployed server. | | |
    | | **Geo-redundant restore** | If the source server was created with [geo-redundant backups](concepts-backup-restore.md#geo-redundant-backup-and-restore), this option would be enabled. If it's enabled, you could restore a backup kept in the storage account of the paired region to create a new server in that other region. | | |
    | **Server details** | | | | |
    | | **Name** | The name that you want to assign to the newly deployed server, on top of which a backup of the source is restored. | A unique name that identifies your Azure Database for PostgreSQL flexible server instance. The domain name `postgres.database.azure.com` is appended to the server name you provide, to conform the fully qualified host name by which you can use a Domain Naming System server to resolve the IP address of your instance. | Although the server name can't be changed after server creation, you can use the [point in time recovery](concepts-backup-restore.md#point-in-time-recovery) feature, to restore the server under a different name. An alternative approach to continue using the existing server, but being able to refer to it using a different server name, would use the [virtual endpoints](concepts-read-replicas-virtual-endpoints.md) to create a writer endpoint with the new desired name. With this approach, you could refer to the instance by its original name, or that assigned to the write virtual endpoint. |
    | | **Location** | The name of one of the [regions in which the service is supported](overview.md#azure-regions). Point in time restore only supports the deployment of the new server in the same region in which the source server exists. | Compliance, data residency, pricing, proximity to your users, or availability of other services in the same region, are some of the requirements you should use when choosing the region. | The service doesn't offer a feature to automatically and transparently relocate an instance to a different region. |
    | | **PostgreSQL version** | The version selected by default. | Point in time restore only supports the deployment of the new server with the exact same major version used by the source server. Currently those versions are: **[!INCLUDE [major-versions-ascending](includes/major-versions-ascending.md)]** | Azure Database for PostgreSQL - Flexible Server supports in-place upgrade, via [major version upgrade](how-to-perform-major-version-upgrade.md). |
    | | **Availability zone** | Your preferred [availability zone](/azure/reliability/availability-zones-overview). | You can choose in which availability zone you want your server to be deployed. Being able to choose the availability zone in which your instance is deployed, is useful to colocate it with your application. If you choose *No preference*, a default availability zone is automatically assigned to your instance during its creation. | Although the availability zone in which an instance is deployed can't be changed after its creation, you can use the [point in time recovery](concepts-backup-restore.md#point-in-time-recovery) feature to restore the server under a different name on a different availability zone. |
    | | **Compute + storage** | Assigns the same type and size of compute and same size of storage, as the ones used by the source server at the time the backup is restored. However, if you select the **Configure server** link, you can change the type of storage allocated to the new server, and whether or not it should be provisioned with geo-redundant backups. | | After the new server is deployed, its compute options can be scaled up or down. |

6. If you want to change the type of storage assigned to the new server, or if you want to deploy it with geo-redundant backups, select **Configure server**:

    :::image type="content" source="./media/how-to-restore-server/configure-server-button.png" alt-text="Screenshot showing the location of the Configure server link." lightbox="./media/how-to-restore-server/configure-server-button.png":::

7. The **Compute + storage** opens to show compute and storage options for the new server:

    :::image type="content" source="./media/how-to-restore-server/configure-server-page.png" alt-text="Screenshot showing the Compute + storage page." lightbox="./media/how-to-restore-server/configure-server-page.png":::

8. Use the following table to understand the meaning of the different fields available in the **Compute + storage** page, and as guidance to fill the page:

    | Section | Setting | Suggested value | Description | Can be changed after instance creation |
    | --- | --- | --- | --- | --- |
    | **Compute** | | | | |
    | | **Compute tier** | Can't be changed and is automatically set to the same value as the source server. | Possible values are **Burstable** (typically used for development environments in which workloads don't need the full capacity of the CPU continuously) and **General Purpose** (typically used for production environments with most common workloads), and **Memory Optimized** (typically used for production environments running workloads that require a high memory to CPU ratio). For more information, see [Compute options in Azure Database for PostgreSQL - Flexible Server](concepts-compute.md). | Can be changed after the server is created. However, if you're using some functionality which is only supported on certain tiers and change the current tier to one in which the feature isn't supported, the feature stops being available or gets disabled. |
    | | **Compute size** | Can't be changed and is automatically set to the same value as the source server. | Notice that the list of supported values might vary across regions, depending on the hardware available on each region. For more information, see [Compute options in Azure Database for PostgreSQL - Flexible Server](concepts-compute.md). | Can be changed after instance is created. |
    | **Storage** | | | | |
    | | **Storage type** | Select **Premium SSD**. | Notice that the list of allowed values might vary depending on which other features you selected. For more information, see [Storage options in Azure Database for PostgreSQL - Flexible Server](concepts-storage.md). | Can't be changed after the instance is created. |
    | | **Storage size** | Can't be changed and is automatically set to the same value as the source server. | Notice that the list of supported values might vary across regions, depending on the hardware available on each region. For more information, see [Compute options in Azure Database for PostgreSQL - Flexible Server](concepts-compute.md). | Can be changed after the instance is created. It can only be increased. Manual or automatic shrinking of storage isn't supported. Acceptable values depend on the type of storage assigned to the instance. |
    | | **Performance Tier** | Can't be changed and is automatically set to the same value as the source server. | Performance of Premium solid-state drives (SSD) is set when you create the disk, in the form of their performance tier. When setting the provisioned size of the disk, a performance tier is automatically selected. This performance tier determines the IOPS and throughput of your managed disk. For Premium SSD disks, this tier can be changed at deployment or afterwards, without changing the size of the disk, and without downtime. Changing the tier allows you to prepare for and meet higher demand without using your disk's bursting capability. It can be more cost-effective to change your performance tier rather than rely on bursting, depending on how long the extra performance is necessary. This is ideal for events that temporarily require a consistently higher level of performance. Events like holiday shopping, performance testing, or running a training environment. To handle these events, you can switch a disk to a higher performance tier without downtime, for as long as you need the extra performance. You can then return to the original tier without downtime when the extra performance is no longer necessary. | Can be changed after the instance is created. |
    | | **Storage Auto-growth** | Can't be changed and is automatically set to the same value as the source server. | Notice that this option might not be supported for some storage types, and it might not be honored for certain storage sizes. For more information, see [Configure storage autogrow in an Azure Database for PostgreSQL flexible server](how-to-auto-grow-storage.md). | Can be changed after the instance is created, as long as the storage type supports this feature. |
    | **Backups** | | | | |
    | | **Backup retention period (in days)** | Can't be changed and is automatically set to the same value as the source server. | The default backup retention period is 7 days, but you can extend the period to a maximum of 35 days. | Can be changed after instance is created. |
    | | **Backup Redundancy Options** | Automatically selected for you, based on the configuration of high availability and geo-redundancy of backups. | Possible values are **Locally redundant** (provides at least 99.999999999% durability of backup objects over a year), **Zone redundant** (provides at least 99.9999999999% durability of backup objects over a year), and **Geo-Redundant** (provides at least 99.99999999999999% durability of backup objects over a year). When **Geo-redundancy** is enabled for the backup, then the backup redundancy option is set to **Geo-Redundant**. Otherwise, if high availability is set to **Disabled** or **Same zone**, then backup redundancy is set to **Locally redundant**. And if high availability is set to **Zone redundant**, then backup redundancy is set to **Zone redundant**. For more information, see [Backup redundancy options in Azure Database for PostgreSQL - Flexible Server](concepts-backup-restore.md#backup-redundancy-options). | Can't be changed after instance is created. |
    | | **Geo-redundancy** | Leave this option disabled. | Geo-redundancy in backups is only supported on instances deployed in any of the [Azure paired regions](/azure/reliability/cross-region-replication-azure). For more information, see [Geo-redundant backup and restore in Azure Database for PostgreSQL - Flexible Server](concepts-backup-restore.md#geo-redundant-backup-and-restore)| Can't be changed after instance is created. |

9. Once all the new server is configured to your needs, select **Review + create**.

    :::image type="content" source="./media/how-to-restore-server/restore-point-review-create.png" alt-text="Screenshot showing the location of the Review + create button." lightbox="./media/how-to-restore-server/restore-point-review-create.png":::

10. Review that all configurations for the new deployment are correctly set, and select **Create**.

    :::image type="content" source="./media/how-to-restore-server/restore-point-create.png" alt-text="Screenshot showing the location of the Create button." lightbox="./media/how-to-restore-server/restore-point-create.png":::

11. A new deployment is launched to create your new Azure Database for PostgreSQL flexible server and restore the most recent data available on the source server at the time of restore:

    :::image type="content" source="./media/how-to-restore-server/restore-point-deployment-progress.png" alt-text="Screenshot that shows the deployment in progress to create your new Azure Database for PostgreSQL Flexible server, on which the most recent data available on the source server is restored." lightbox="./media/how-to-restore-server/restore-point-deployment-progress.png":::

12. When the deployment completes, you can select **Go to resource**, to get you to the **Overview** page of your new Azure Database for PostgreSQL flexible server, and start using it:

    :::image type="content" source="./media/how-to-restore-server/restore-point-deployment-completed.png" alt-text="Screenshot that shows the deployment successfully completed of your Azure Database for PostgreSQL Flexible server." lightbox="./media/how-to-restore-server/restore-point-deployment-completed.png":::

### [CLI](#tab/cli-restore-geo-restore)

If your server was deployed with geo-redundant backup, you can initiate the restore of its backups to its paired region, with recovery point objective set to present time, via the [az postgres flexible-server geo-restore](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-geo-restore) command.


```azurecli-interactive
az postgres flexible-server geo-restore --resource-group <resource_group> --name <server> --source-server <source_server> --location <paired_region>
```

---

## Related content

- [Overview of business continuity with Azure Database for PostgreSQL - Flexible Server](concepts-business-continuity.md).
- [High availability in Azure Database for PostgreSQL - Flexible Server](/azure/reliability/reliability-postgresql-flexible-server).
- [Backup and restore in Azure Database for PostgreSQL - Flexible Server](concepts-backup-restore.md).
- [On-demand backups (Preview)](how-to-operate-on-demand-backups.md).
