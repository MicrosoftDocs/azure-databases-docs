---
title: Migrate SSD Server to SSDv2 Using Point-in-Time-Restore
description: This article describes how to migrate a Premium SSD server to Premium SSDv2 in Azure Database for PostgreSQL flexible server.
author: kabharati
ms.author: kabharati
ms.reviewer: maghan
ms.date: 08/10/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic:  concept-article
#customer intent: As a user, I want to learn how to migrate from Premium SSD server to Premium SSDv2 in Azure Database for PostgreSQL flexible server.
---

# Migrate or restore from Premium SSD to Premium SSDv2

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

This article provides step-by-step instructions to perform a restore of an Azure Database for PostgreSQL flexible server to a custom restore point.

## Steps to migrate or restore from Premmium SSD to Premium SSDv2

### [Portal](#tab/portal-restore-custom-point)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

2. In the resource menu, select **Overview**.


    :::image type="content" source="./media/concepts-storage-migrate-ssd-to-ssd-v2/overview.png" alt-text="Screenshot showing the Overview page." lightbox="./media/concepts-storage-migrate-ssd-to-ssd-v2/overview.png":::

3. Select the **Restore** button.

    :::image type="content" source="./media/concepts-storage-migrate-ssd-to-ssd-v2/restore-button.png" alt-text="Screenshot showing the location of the Restore button in the Overview page." lightbox="./media/concepts-storage-migrate-ssd-to-ssd-v2/restore-button.png":::

4. You're redirected to the **Create Azure Database for PostgreSQL flexible server - Restore server** wizard, from where you can configure some settings for the new server that is created. After the new server is deployed, the most recent snapshot of the source server data disk is restored. In the **Point-in-time-restore (PITR)** section, select **Latest restore point**.

    :::image type="content" source="./media/concepts-storage-migrate-ssd-to-ssd-v2/latest-restore-point.png" alt-text="Screenshot showing the Select a custom restore point radio button selected." lightbox="./media/concepts-storage-migrate-ssd-to-ssd-v2/latest-restore-point.png":::

5. If you want to change the type of storage assigned to the new server, select **Configure server** and choose **Premium SSD v2** for the **Storage type** Field

    :::image type="content" source="./media/concepts-storage-migrate-ssd-to-ssd-v2/configure-server-button.png" alt-text="Screenshot showing the location of the Configure server link." lightbox="./media/concepts-storage-migrate-ssd-to-ssd-v2/configure-server-button.png":::

6. The **Compute + storage** opens to show compute and storage options for the new server:

    :::image type="content" source="./media/concepts-storage-migrate-ssd-to-ssd-v2/configure-server-page.png" alt-text="Screenshot showing the Compute + storage page." lightbox="./media/concepts-storage-migrate-ssd-to-ssd-v2/configure-server-page.png":::


7. Use the following table to understand the meaning of the different fields available in the **Compute + storage** page, and as guidance to fill the page:

    | Section | Setting | Suggested value | Description | Can be changed after instance creation |
    | --- | --- | --- | --- | --- |
    | **Compute** | | | | |
    | | **Compute tier** | Can't be changed and is automatically set to the same value as the source server. | Possible values are **Burstable** (typically used for development environments in which workloads don't need the full capacity of the CPU continuously) and **General Purpose** (typically used for production environments with most common workloads), and **Memory Optimized** (typically used for production environments running workloads that require a high memory to CPU ratio). For more information, see [Compute options in Azure Database for PostgreSQL flexible server](concepts-compute.md). | Can be changed after the server is created. However, if you're using some functionality which is only supported on certain tiers and change the current tier to one in which the feature isn't supported, the feature stops being available or gets disabled. |
    | | **Compute size** | Can't be changed and is automatically set to the same value as the source server. | Notice that the list of supported values might vary across regions, depending on the hardware available on each region. For more information, see [Compute options in Azure Database for PostgreSQL flexible server](concepts-compute.md). | Can be changed after instance is created. |
    | **Storage** | | | | |
    | | **Storage type** | Select **Premium SSD**. | Notice that the list of allowed values might vary depending on which other features you selected. For more information, see [Storage options in Azure Database for PostgreSQL flexible server](concepts-storage.md). | Can't be changed after the instance is created. |
    | | **Storage size** | Can't be changed and is automatically set to the same value as the source server. | Notice that the list of supported values might vary across regions, depending on the hardware available on each region. For more information, see [Compute options in Azure Database for PostgreSQL flexible server](concepts-compute.md). | Can be changed after the instance is created. It can only be increased. Manual or automatic shrinking of storage isn't supported. Acceptable values depend on the type of storage assigned to the instance. |
    | | **Performance tier** | Can't be changed and is automatically set to the same value as the source server. | Performance of Premium solid-state drives (SSD) is set when you create the disk, in the form of their performance tier. When setting the provisioned size of the disk, a performance tier is automatically selected. This performance tier determines the IOPS and throughput of your managed disk. For Premium SSD disks, this tier can be changed at deployment or afterwards, without changing the size of the disk, and without downtime. Changing the tier allows you to prepare for and meet higher demand without using your disk's bursting capability. It can be more cost-effective to change your performance tier rather than rely on bursting, depending on how long the extra performance is necessary. This is ideal for events that temporarily require a consistently higher level of performance. Events like holiday shopping, performance testing, or running a training environment. To handle these events, you can switch a disk to a higher performance tier without downtime, for as long as you need the extra performance. You can then return to the original tier without downtime when the extra performance is no longer necessary. | Can be changed after the instance is created. |
    | | **Storage autogrow** | Can't be changed and is automatically set to the same value as the source server. | Notice that this option might not be supported for some storage types, and it might not be honored for certain storage sizes. For more information, see [Configure storage autogrow in an Azure Database for PostgreSQL flexible server](how-to-auto-grow-storage.md). | Can be changed after the instance is created, as long as the storage type supports this feature. |
    | **Backups** | | | | |
    | | **Backup retention period (in days)** | Can't be changed and is automatically set to the same value as the source server. | The default backup retention period is 7 days, but you can extend the period to a maximum of 35 days. | Can be changed after instance is created. |
    | | **Backup redundancy** | Automatically selected for you, based on the configuration of high availability and geo-redundancy of backups. | Possible values are **Locally redundant** (provides at least 99.999999999% durability of backup objects over a year), **Zone redundant** (provides at least 99.9999999999% durability of backup objects over a year), and **Geo-Redundant** (provides at least 99.99999999999999% durability of backup objects over a year). When **Geo-redundancy** is enabled for the backup, then the backup redundancy option is set to **Geo-Redundant**. Otherwise, if high availability is set to **Disabled** or **Same zone**, then backup redundancy is set to **Locally redundant**. And if high availability is set to **Zone redundant**, then backup redundancy is set to **Zone redundant**. For more information, see [Backup redundancy options in Azure Database for PostgreSQL flexible server](concepts-backup-restore.md#backup-redundancy-options). | Can't be changed after instance is created. |
    | | **Geo-redundancy** | Leave this option disabled. | Geo-redundancy in backups is only supported on instances deployed in any of the [Azure paired regions](/azure/reliability/cross-region-replication-azure). For more information, see [Geo-redundant backup and restore in Azure Database for PostgreSQL flexible server](concepts-backup-restore.md#geo-redundant-backup-and-restore)| Can't be changed after instance is created. |

10. Once all the new server is configured to your needs, select **Review + create**.

    :::image type="content" source="./media/concepts-storage-migrate-ssd-to-ssd-v2/restore-point-review-create.png" alt-text="Screenshot showing the location of the Review + create button." lightbox="./media/concepts-storage-migrate-ssd-to-ssd-v2/restore-point-review-create.png":::

11. Review that all configurations for the new deployment are correctly set, and select **Create**.

    :::image type="content" source="./media/concepts-storage-migrate-ssd-to-ssd-v2/restore-point-create.png" alt-text="Screenshot showing the location of the Create button." lightbox="./media/concepts-storage-migrate-ssd-to-ssd-v2/restore-point-create.png":::

12. A new deployment is launched to create your new Azure Database for PostgreSQL flexible server and restore the most recent data available on the source server at the time of restore:

    :::image type="content" source="./media/concepts-storage-migrate-ssd-to-ssd-v2/restore-point-deployment-progress.png" alt-text="Screenshot that shows the deployment in progress to create your new Azure Database for PostgreSQL Flexible server, on which the most recent data available on the source server is restored." lightbox="./media/concepts-storage-migrate-ssd-to-ssd-v2/restore-point-deployment-progress.png":::

13. When the deployment completes, you can select **Go to resource**, to get you to the **Compute +Storage** page of your new Azure Database for PostgreSQL flexible server, and start validate your **Storage type**

    :::image type="content" source="./media/concepts-storage-migrate-ssd-to-ssd-v2/restore-point-deployment-completed.png" alt-text="Screenshot that shows the deployment successfully completed of your Azure Database for PostgreSQL Flexible server." lightbox="./media/concepts-storage-migrate-ssd-to-ssd-v2/restore-point-deployment-completed.png":::

### [CLI](#tab/cli-restore-custom-point)

You can restore a backup of a server to the latest restore point via the [az postgres flexible-server restore](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-restore) command.

```azurecli-interactive
az postgres flexible-server restore \
  --resource-group <resource_group> \
  --name <server> \
  --source-server <source_server> \
  --restore-time 2025-04-26T02:10:00+00:00
  --storage-type PremiumV2_LRS
```

> [!NOTE]
> - The value passed to the `--restore-time` parameter represents the point in time, in UTC, to restore from (ISO8601 format).
> - If the `--restore-time` parameter isn't present, its value defaults to the current time in the system from where the command is executed.
> - If the value passed is in the future, the backend service that receives the request normalizes it to the current date and time.
> - If the value passed is earlier than the earliest restore point available on the source server, you receive an InternalServerError.

---

## Related content

- [Restore to latest restore point](how-to-restore-latest-restore-point.md).
- [Restore full backup (fast restore)](how-to-restore-full-backup.md).
- [Restore to paired region (geo-restore)](how-to-restore-paired-region.md).
- [Restore a dropped server](how-to-restore-dropped-server.md).
