---
title: Major Version Upgrade
description: Learn how to upgrade major version for an Azure Database for MySQL flexible server instance.
author: code-sidd
ms.author: sisawant
ms.reviewer: maghan
ms.date: 05/29/2025
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: how-to
ms.custom:
  - devx-track-azurecli
---

# Major version upgrade in Azure Database for MySQL

> [!NOTE]  
> This article contains references to the term slave, a term that Microsoft no longer uses. When the term is removed from the software, we will remove it from this article.

This article describes how you can upgrade your MySQL major version in-place in Azure Database for MySQL Flexible Server.
This feature enables customers to perform in-place upgrades of their MySQL 5.7 servers to MySQL 8.0 without any data movement or the need to make any application connection string changes.

> [!IMPORTANT]  
> - Duration of downtime varies based on the size of the database instance and the number of tables it contains.
> - When initiating a major version upgrade for Azure Database for MySQL Flexible Server via Rest API or SDK, please avoid modifying other properties of the service in the same request. The simultaneous changes are not permitted and might lead to unintended results or request failure. Please conduct property modifications in separate operations post-upgrade completion.
> - Some workloads might not exhibit enhanced performance after upgrading from 5.7 to 8.0. We suggest that you evaluate the performance of your workload by first creating a replica server (as a test server), then promoting it to a standalone server and then running the workload on the test server prior to implementing the upgrade in a production environment.
> - Upgrading the major MySQL version is irreversible. Your deployment might fail if validation identifies that the server is configured with any features that are [removed](https://dev.mysql.com/doc/refman/8.0/en/mysql-nutshell.html#mysql-nutshell-removals) or [deprecated](https://dev.mysql.com/doc/refman/8.0/en/mysql-nutshell.html#mysql-nutshell-deprecations). You can make necessary configuration changes on the server and try the upgrade again.

## Prerequisites

- Read Replicas with MySQL version 5.7 should be upgraded before Primary Server for replication to be compatible between different MySQL versions, read more on [Replication Compatibility between MySQL versions](https://dev.mysql.com/doc/mysql-replication-excerpt/8.0/en/replication-compatibility.html).
- Before upgrading your production servers, it's now easier and more efficient with our built-in **Validate** feature in the Azure portal. This tool pre-checks your database schema's compatibility with MySQL 8.0, highlighting potential issues. While we offer this convenient option, we also **strongly recommend** you use the official Oracle [MySQL Upgrade checker tool](https://go.microsoft.com/fwlink/?linkid=2230525) to test your database schema compatibility and perform necessary regression test to verify application compatibility with features [removed](https://dev.mysql.com/doc/refman/8.0/en/mysql-nutshell.html#mysql-nutshell-removals)/[deprecated](https://dev.mysql.com/doc/refman/8.0/en/mysql-nutshell.html#mysql-nutshell-deprecations) in the new MySQL version.

> [!NOTE]
> When you use Oracle's official tool to check schema compatibility, you might encounter some warnings indicating unexpected tokens in stored procedures, such as:
> `mysql.az_replication_change_master - at line 3,4255: unexpected token 'REPLICATION'`
  > `mysql.az_add_action_history - PROCEDURE uses obsolete NO_AUTO_CREATE_USER sql_mode`
  > You can safely ignore these warnings. They refer to built-in stored procedures prefixed with mysql., which are used to support Azure MySQL features. These warnings do not affect the functionality of your database.
- Trigger [on-demand backup](how-to-trigger-on-demand-backup.md) before you perform a major version upgrade on your production server, which can be used to [rollback to version 5.7](how-to-restore-server-portal.md) from the full on-demand backup taken.
- Before proceeding with the major version upgrade, please ensure there are no active or pending XA transactions on the database, as ongoing XA transactions can potentially cause the upgrade process to fail. To avoid this issue, first check for any XA transactions in the "prepared" state by running `XA RECOVER;`. For any transactions identified, use `XA ROLLBACK '{xid}'`; to rollback each transaction, replacing {xid} with the transaction ID. Ensure all XA transactions are either committed or rolled back before initiating the upgrade to maintain transaction consistency and reduce the risk of upgrade failures.

## Perform a planned major version upgrade from MySQL 5.7 to MySQL 8.0 using the Azure portal for Burstable SKU servers

Performing a major version upgrade for an Azure Database for MySQL Burstable SKU compute tier requires a specialized workflow. This is because major version upgrades are resource-intensive, demanding significant CPU and memory. Burstable SKU instances being credit based might struggle under these requirements, potentially causing the upgrade process to fail. Therefore, when upgrading a Burstable SKU, the system first upgrades the compute tier to a General Purpose SKU to ensure sufficient resources are available for the upgrade.

To perform a major version upgrade for an Azure Database for MySQL Burstable SKU compute tier using the Azure portal, follow these steps:

1. In the [Azure portal](https://portal.azure.com/), select your existing Azure Database for MySQL Flexible Server 5.7 server.
    > [!IMPORTANT]  
    > We recommend performing upgrade first on a restored copy of the server rather than upgrading production directly. See [how to perform point-in-time restore](how-to-restore-server-portal.md).

1. On the **Overview** page, in the toolbar, select **Upgrade**.

    > [!IMPORTANT]  
    > Before upgrading visit link for list of [features removed](https://dev.mysql.com/doc/refman/8.0/en/mysql-nutshell.html#mysql-nutshell-removals) in MySQL 8.0.
    > Verify deprecated [sql_mode](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_sql_mode) values and remove/deselect them from your current Azure Database for MySQL Flexible Server 5.7 server using the Server Parameters Blade on your Azure portal to avoid deployment failure.
    > [sql_mode](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_sql_mode) with values NO_AUTO_CREATE_USER, NO_FIELD_OPTIONS, NO_KEY_OPTIONS and NO_TABLE_OPTIONS are no longer supported in MySQL 8.0.

    :::image type="content" source="media/how-to-upgrade/1-how-to-upgrade.png" alt-text="Screenshot showing Azure Database for MySQL Flexible Server Upgrade." lightbox="media/how-to-upgrade/1-how-to-upgrade.png":::

1. Schema Compatibility Validation

   Before proceeding with the upgrade, run Oracle's official [MySQL Upgrade checker tool](https://go.microsoft.com/fwlink/?linkid=2230525) to validate that your current database schema is compatible with MySQL 8.0. This step is crucial to ensure a smooth upgrade process.

1. Pre-Upgrade Decision

   Before proceeding with the upgrade, you need to choose the compute tier to which you want to upgrade to perform the major version upgrade. By default, the system will upgrade from Burstable SKU to the most basic General Purpose SKU, but you can opt to upgrade to a higher compute tier if needed.

   > [!NOTE]  
   > While your server operates in the "General Purpose" tier during the upgrade, you will only be charged for the actual "General Purpose" resources used during this period.

1. Post-Upgrade Decision

   Decide whether to retain the General Purpose SKU or revert to Burstable SKU after the upgrade. This choice will be prompted during the initial upgrade steps.

   The system will automatically upgrade your compute tier from Burstable SKU to the selected General Purpose SKU support the major version upgrade.

1. Major Version Upgrade

   Once the compute tier is upgraded, the system will initiate the major version upgrade process. Monitor the upgrade progress through the Azure portal. The upgrade process might take some time depending on the size and activity of your database.

   > [!NOTE]  
   > If the major version upgrade fails, the compute tier will not automatically revert to the previous Burstable SKU. This is to allow customers to continue the major version upgrade without needing to perform the compute tier upgrade again.

1. Automatic Reversion

   Based on your pre-upgrade decision, the system will either retain the General Purpose SKU or automatically revert to Burstable SKU after the upgrade is complete.

   > [!NOTE]  
   > If you chose to automatically revert to Burstable SKU, the system will revert to the B2S SKU by default.

## Perform a planned major version upgrade from MySQL 5.7 to MySQL 8.0 using the Azure portal for General Purpose and Business Critical SKU servers

To perform a major version upgrade of an Azure Database for MySQL Flexible Server 5.7 server using the Azure portal, perform the following steps.

1. In the [Azure portal](https://portal.azure.com/), select your existing Azure Database for MySQL Flexible Server 5.7 server.
    > [!IMPORTANT]  
    > We recommend performing upgrade first on a restored copy of the server rather than upgrading production directly. See [how to perform point-in-time restore](how-to-restore-server-portal.md).

1. On the **Overview** page, in the toolbar, select **Upgrade**.

    > [!IMPORTANT]  
    > Before upgrading visit link for list of [features removed](https://dev.mysql.com/doc/refman/8.0/en/mysql-nutshell.html#mysql-nutshell-removals) in MySQL 8.0.
    > Verify deprecated [sql_mode](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_sql_mode) values and remove/deselect them from your current Azure Database for MySQL Flexible Server 5.7 server using the Server Parameters Blade on your Azure portal to avoid deployment failure.
    > [sql_mode](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_sql_mode) with values NO_AUTO_CREATE_USER, NO_FIELD_OPTIONS, NO_KEY_OPTIONS and NO_TABLE_OPTIONS are no longer supported in MySQL 8.0.

    :::image type="content" source="media/how-to-upgrade/1-how-to-upgrade.png" alt-text="Screenshot showing Azure Database for MySQL Flexible Server Upgrade." lightbox="media/how-to-upgrade/1-how-to-upgrade.png":::
1. Perform Pre-Upgrade Validation

    Before proceeding with the upgrade, Select the **Validate** button to check the compatibility of your server with MySQL 8.0.

    :::image type="content" source="media/how-to-upgrade/how-to-validate.png" alt-text="Screenshot showing validate.":::

    > [!NOTE]  
    > When using the 'Validate' feature to assess your database schema for compatibility with MySQL 8.0, please take note of the following considerations:
    > - Table Locking During Validation: The validation process involves locking tables in order to accurately inspect the entire schema. This can lead to query timeouts if the database is under heavy load.
    >  
    > **Recommendation**: Avoid running validation during peak business hours or when the database is handling high traffic. Instead, schedule the validation during low-activity periods to reduce impact on operations.
    > - Potential for Hanging Due to Large Result Sets: In certain cases—particularly with complex databases containing a large number of objects—the validation result might become too large to be processed or displayed within the online workflow. This might result in the 'Validate' operation appearing to hang or remain in progress indefinitely.
    >  
    > **Recommendation**: If you encounter this issue, we suggest performing the validation locally using Oracle's official client-side upgrade checker tool, such as the one included in MySQL Shell. This approach avoids platform-side result size limitations and provides a more detailed and reliable validation output.
    > - Recommended Use Cases for Online Validation: The online 'Validate' feature is designed for simple or moderately complex schemas. For large-scale production environments—such as those with thousands of tables, views, routines, or other schema objects—we strongly recommend using Oracle's client-side upgrade checker tool to perform the compatibility check. This ensures that the full schema is analyzed comprehensively and avoids potential issues related to result size or validation timeouts.

1. In the **Upgrade** sidebar, in the **MySQL version to upgrade** text box, verify the major MySQL version you want to upgrade to, i.e., 8.0.

    :::image type="content" source="media/how-to-upgrade/2-how-to-upgrade.png" alt-text="Screenshot showing Upgrade.":::

    Before you can upgrade your primary server, you first need to have upgraded any associated read replica servers. Until this is completed, **Upgrade** will be disabled.

1. On the primary server, select the confirmation message to verify that all replica servers have been upgraded, and then select **Upgrade**.

    :::image type="content" source="media/how-to-upgrade/how-to-upgrade.png" alt-text="Screenshot showing upgrade.":::

    On read replica and standalone servers, **Upgrade** is enabled by default.

## Perform a planned major version upgrade from MySQL 5.7 to MySQL 8.0 using the Azure CLI

To perform a major version upgrade of an Azure Database for MySQL Flexible Server 5.7 server using the Azure CLI, perform the following steps.

1. Install the [Azure CLI](/cli/azure/install-azure-cli) for Windows or use the [Azure CLI](/azure/cloud-shell/overview) in Azure Cloud Shell to run the upgrade commands.

    This upgrade requires version 2.40.0 or later of the Azure CLI. If you're using Azure Cloud Shell, the latest version is already installed. Run az version to find the version and dependent libraries that are installed. To upgrade to the latest version, run az upgrade.

1. After you sign in, run the [az mysql server upgrade](/cli/azure/mysql/server#az-mysql-server-upgrade) command.

    ```azurecli
    az mysql flexible-server upgrade --name {your mysql server name} --resource-group {your resource group} --subscription {your subscription id} --version 8
    ```

1. Under the confirmation prompt, type **y** to confirm or **n** to stop the upgrade process, and then press Enter.

## Perform a major version upgrade from MySQL 5.7 to MySQL 8.0 on a read replica server using the Azure portal

To perform a major version upgrade of an Azure Database for MySQL Flexible Server 5.7 server to MySQL 8.0 on a read replica using the Azure portal, perform the following steps.

1. In the Azure portal, select your existing Azure Database for MySQL Flexible Server 5.7 read replica server.

1. On the **Overview** page, in the toolbar, select **Upgrade**.

> [!IMPORTANT]  
> Before upgrading visit link for list of [features removed](https://dev.mysql.com/doc/refman/8.0/en/mysql-nutshell.html#mysql-nutshell-removals) in MySQL 8.0.
> Verify deprecated [sql_mode](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_sql_mode) values and remove/deselect them from your current Azure Database for MySQL Flexible Server 5.7 server using the Server Parameters Blade on your Azure Portal to avoid deployment failure.

1. In the **Upgrade** section, select **Upgrade** to upgrade an Azure Database for MySQL Flexible Server 5.7 read replica server to MySQL 8.0.

    A notification appears to confirm that upgrade is successful.

1. On the **Overview** page, confirm that your Azure Database for MySQL Flexible Server read replica server is running version is 8.0.

1. Now, go to your primary server and perform major version upgrade on it.

## Perform minimal downtime major version upgrade from MySQL 5.7 to MySQL 8.0 using read replicas

To perform a major version upgrade of an Azure Database for MySQL Flexible Server 5.7 server to MySQL 8.0 with minimal downtime using read replica servers, perform the following steps.

1. In the Azure portal, select your existing Azure Database for MySQL Flexible Server 5.7 server.

1. Create a [read replica](how-to-read-replicas-portal.md) from your primary server.

1. [Upgrade](#perform-a-planned-major-version-upgrade-from-mysql-57-to-mysql-80-using-the-azure-cli) your read replica to version 8.0.

1. After you confirm that the replica server is running version 8.0, stop your application from connecting to your primary server.

1. Check replication status to ensure that the replica has caught up with the primary so that all data is in sync and that no new operations are being performed on the primary.

1. Confirm with the show replica status command on the replica server to view the replication status.

    ```azurecli
     SHOW SLAVE STATUS\G
    ```
    If the state of Slave_IO_Running and Slave_SQL_Running is **yes** and the value of Seconds_Behind_Master is **0**, replication is working well. Seconds_Behind_Master indicates how late the replica is. If the value isn't **0**, then the replica is still processing updates. After you confirm that the value of Seconds_Behind_Master is ***, it's safe to stop replication.

1. Promote your read replica to primary by stopping replication.

1. Set Server Parameter read_only to **0** (OFF) to start writing on promoted primary.

1. Point your application to the new primary (former replica) which is running server 8.0. Each server has a unique connection string. Update your application to point to the (former) replica instead of the source.

> [!NOTE]  
> This scenario only incurs downtime during steps 4 through 7.

## Frequently asked questions

- **Will this cause downtime of the server and if so, how long?**

  To have minimal downtime during upgrades, follow the steps mentioned under [Perform minimal downtime major version upgrade from MySQL 5.7 to MySQL 8.0 using read replicas](#perform-minimal-downtime-major-version-upgrade-from-mysql-57-to-mysql-80-using-read-replicas).
  The server will be unavailable during the upgrade process, so we recommend you perform this operation during your planned maintenance window. The estimated downtime depends on the database size, storage size provisioned (IOPs provisioned), and the number of tables on the database. The upgrade time is directly proportional to the number of tables on the server. To estimate the downtime for your server environment, we recommend to first perform upgrade on restored copy of the server.

- **What happens to my backups after upgrade?**

  All backups (automated/on-demand) taken before major version upgrade, when used for restoration will always restore to a server with older version (5.7).
  All the backups (automated/on-demand) taken after major version upgrade will restore to server with upgraded version (8.0). It's highly recommended to take on-demand backup before you perform the major version upgrade for an easy rollback.

- **I'm currently using Burstable SKU, does Microsoft plan to support major version upgrade for this SKU in the future?**

  Burstable SKU is not able to support major version upgrade due to the performance limitation of this SKU.

  If you need to perform a major version upgrade on your Azure Database for MySQL Flexible Server instance and are currently using Burstable SKU, one temporary solution would be to upgrade to General Purpose or Business Critical SKU, perform the upgrade, and then switch back to Burstable SKU.

  Upgrading to a higher SKU might involve a change in pricing and might result in increased costs for your deployment. However, since the upgrade process is not expected to take a long time, the added costs shouldn't be significant.

## Related content

- [how to configure scheduled maintenance](how-to-maintenance-portal.md)
- [MySQL version 8.0](https://dev.mysql.com/doc/refman/8.0/en/mysql-nutshell.html)
