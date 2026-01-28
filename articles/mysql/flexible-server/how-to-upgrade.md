---
title: Major Version Upgrade
description: Learn how to upgrade major version for an Azure Database for MySQL flexible server instance.
author: xboxeer
ms.author: yuzheng1
ms.reviewer: yuzheng1, maghan
ms.date: 06/11/2025
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: how-to
ms.custom:
  - devx-track-azurecli
---

# Major version upgrade in Azure Database for MySQL

> [!NOTE]  
> This article contains references to the term slave, a term that Microsoft no longer uses. When the term is removed from the software, we'll remove it from this article.

This article describes how to upgrade your MySQL major version in Azure Database for MySQL Flexible Server.
This feature enables customers to perform major version upgrades (for example, from MySQL 5.7 to 8.0 or 8.0 to 8.4) without moving data or changing application connection strings.

> [!IMPORTANT]
> - Duration of downtime varies based on the size of the database instance and the number of tables it contains.
> - When initiating a major version upgrade for Azure Database for MySQL Flexible Server via Rest API or SDK, please avoid modifying other service properties in the same request. Simultaneous changes aren't permitted and might lead to unintended results or request failure. Conduct property modifications in separate operations after the upgrade is completed.
> - Some workloads might not exhibit enhanced performance after a major version upgrade. We suggest that you evaluate the performance of your workload by first creating a replica server (as a test server), then promoting it to a standalone server, and then running the workload on the test server before implementing the upgrade in a production environment.
> - Upgrading the major MySQL version is irreversible. Your deployment might fail if validation identifies that the server is configured with any features that are [removed](https://dev.mysql.com/doc/refman/8.0/en/mysql-nutshell.html#mysql-nutshell-removals) or [deprecated](https://dev.mysql.com/doc/refman/8.0/en/mysql-nutshell.html#mysql-nutshell-deprecations) in the target version. You can make the necessary configuration changes on the server and try the upgrade again.
> - If you're upgrading from Azure Database for MySQL 5.7 to MySQL 8.0 or 8.4, be aware that some older client libraries may not be fully compatible with newer MySQL major versions. For example, applications using legacy client libraries or MySQL drivers (such as [EOL PHP Client](https://www.php.net/eol.php)) might encounter connection failures after the upgrade due to unsupported authentication methods, character sets, or protocol changes. We strongly recommend validating client compatibility before performing a major version upgrade in production. Create a test server or replica running the target MySQL version, connect your application using the same client libraries, and ensure all connections and workloads function correctly before upgrading your production server.


## Prerequisites

- Read Replicas with an older MySQL version should be upgraded before the Primary Server for replication to be compatible between different MySQL versions. Read more on [Replication Compatibility between MySQL versions](https://dev.mysql.com/doc/mysql-replication-excerpt/8.0/en/replication-compatibility.html).
- Before upgrading your production servers, it's now easier and more efficient with our built-in **Validate** feature in the Azure portal. This tool prechecks your database schema's compatibility with the target MySQL version, highlighting potential issues. While we offer this convenient option, we also **strongly recommend** you use the official Oracle [MySQL Upgrade checker tool](https://go.microsoft.com/fwlink/?linkid=2230525) to test your database schema compatibility and perform necessary regression tests to verify application compatibility with features [removed](https://dev.mysql.com/doc/refman/8.0/en/mysql-nutshell.html#mysql-nutshell-removals)/[deprecated](https://dev.mysql.com/doc/refman/8.0/en/mysql-nutshell.html#mysql-nutshell-deprecations) in the new MySQL version.
- Trigger [on-demand backup](how-to-trigger-on-demand-backup.md) before you perform a major version upgrade on your production server. Backups taken before the upgrade can be used to [roll back to the previous version](how-to-restore-server-portal.md) from the full on-demand backup.
- Before proceeding with the major version upgrade, please ensure there are no active or pending XA transactions on the database, as ongoing XA transactions can potentially cause the upgrade process to fail. First, to avoid this issue, check for any XA transactions in the "prepared" state by running `XA RECOVER;`. For any transactions identified, use `XA ROLLBACK '{xid}'`; to roll back each transaction, replacing {xid} with the transaction ID. Ensure all XA transactions are either committed or rolled back before initiating the upgrade to maintain transaction consistency and reduce the risk of upgrade failures.

> [!NOTE]  
>  When you use Oracle's official tool to check schema compatibility, you might encounter some warnings indicating unexpected tokens in stored procedures, such as:
> 
>  `mysql.az_replication_change_master - at line 3,4255: unexpected token 'REPLICATION'`
> 
>  `mysql.az_add_action_history - PROCEDURE uses obsolete NO_AUTO_CREATE_USER sql_mode`
> 
>  You can safely ignore these warnings. They refer to built-in stored procedures prefixed with `mysql.`, which are used to support Azure MySQL features. These warnings don't affect the functionality of your database.

## Perform a planned major version upgrade using the Azure portal for Burstable SKU servers

Performing a major version upgrade for an Azure Database for MySQL Burstable SKU compute tier requires a specialized workflow. Major version upgrades are resource-intensive, demanding significant CPU and memory. Burstable SKU instances, being credit-based, might struggle under these requirements, potentially causing the upgrade process to fail. Therefore, when upgrading a Burstable SKU, the system first upgrades the compute tier to a General-Purpose SKU to ensure sufficient resources are available for the upgrade.

To perform a major version upgrade for an Azure Database for MySQL Burstable SKU compute tier using the Azure portal, follow these steps:

1. In the [Azure portal](https://portal.azure.com/), select your existing Azure Database for MySQL Flexible Server instance.
   
   > [!IMPORTANT]
   > We recommend performing an upgrade first on a restored server copy rather than upgrading production directly. See [how to perform point-in-time restore](how-to-restore-server-portal.md).

2. On the **Overview** page, in the toolbar, select **Upgrade**.
   
   > [!IMPORTANT]
   > Before upgrading, visit the link for the list of [features removed](https://dev.mysql.com/doc/refman/8.0/en/mysql-nutshell.html#mysql-nutshell-removals) in the target MySQL version.
   > Verify deprecated [sql_mode](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_sql_mode) values and remove/deselect them from your current Azure Database for MySQL Flexible Server using the Server Parameters Blade on your Azure portal to avoid deployment failure.
   > [sql_mode](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_sql_mode) with values NO_AUTO_CREATE_USER, NO_FIELD_OPTIONS, NO_KEY_OPTIONS and NO_TABLE_OPTIONS are no longer supported in MySQL 8.0 and later.
    
   :::image type="content" source="media/how-to-upgrade/1-how-to-upgrade.png" alt-text="Screenshot showing Azure Database for MySQL Flexible Server Upgrade." lightbox="media/how-to-upgrade/1-how-to-upgrade.png":::
    
3. Schema Compatibility Validation

    Before proceeding with the upgrade, run Oracle's official [MySQL Upgrade checker tool](https://go.microsoft.com/fwlink/?linkid=2230525) to validate that your current database schema is compatible with the target MySQL version. This step is crucial to ensure a smooth upgrade process.

4. Pre-Upgrade Decision
   
    Before upgrading, you must choose the compute tier to upgrade to perform the major version upgrade. By default, the system upgrades from Burstable SKU to the most basic General Purpose SKU, but you can upgrade to a higher compute tier if needed. Please note that while your server operates in the "General Purpose" tier during the upgrade, you'll only be charged for the actual "General Purpose" resources used during this period.
    
5. Post-Upgrade Decision

    After the upgrade, decide whether to retain the General Purpose SKU or revert to Burstable SKU. This choice is prompted during the initial upgrade steps.
    
    The system automatically upgrades your compute tier from Burstable SKU to the selected General Purpose SKU to support the major version upgrade.

6. Major Version Upgrade

    Once the compute tier is upgraded, the system initiates the major version upgrade process. Monitor the upgrade progress through the Azure portal. The upgrade process might take some time, depending on the size and activity of your database. Please note that If the major version upgrade fails, the compute tier won't automatically revert to the previous Burstable SKU. This allows customers to continue the major version upgrade without performing the compute tier upgrade again.
    
7. Automatic Reversion

    Based on your preupgrade decision, the system either retains the General Purpose SKU or automatically reverts to Burstable SKU after the upgrade. If you automatically revert to Burstable SKU, the system reverts to the B2S SKU by default.
    
## Perform a planned major version upgrade using the Azure portal for general-purpose and business-critical SKU servers

To perform a major version upgrade of an Azure Database for MySQL Flexible Server using the Azure portal, perform the following steps.

1. In the [Azure portal](https://portal.azure.com/), select your existing Azure Database for MySQL Flexible Server instance.

   > [!IMPORTANT]
   > We recommend performing an upgrade first on a restored server copy rather than upgrading production directly. See [how to perform point-in-time restore](how-to-restore-server-portal.md).
    
2. On the **Overview** page, in the toolbar, select **Upgrade**.

   > [!IMPORTANT]
   > Before upgrading, visit the link for the list of [features removed](https://dev.mysql.com/doc/refman/8.0/en/mysql-nutshell.html#mysql-nutshell-removals) in the target MySQL version.
   > Verify deprecated [sql_mode](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_sql_mode) values and remove/deselect them from your current Azure Database for MySQL Flexible Server using the Server Parameters Blade on your Azure portal to avoid deployment failure.
   > [sql_mode](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_sql_mode) with values NO_AUTO_CREATE_USER, NO_FIELD_OPTIONS, NO_KEY_OPTIONS and NO_TABLE_OPTIONS are no longer supported in MySQL 8.0 and later.
    
     :::image type="content" source="media/how-to-upgrade/1-how-to-upgrade.png" alt-text="Screenshot showing Azure Database for MySQL Flexible Server Upgrade." lightbox="media/how-to-upgrade/1-how-to-upgrade.png":::
2. Perform Pre-Upgrade Validation

    Before proceeding with the upgrade, select the **Validate** button to check the compatibility of your server with the target MySQL version.

     :::image type="content" source="media/how-to-upgrade/how-to-validate.png" alt-text="Screenshot showing validate.":::
    
    > [!NOTE]  
    > Online validation is currently not supported for 8.0 to 8.4 major version upgrade, customer are suggested to use [community tool](https://dev.mysql.com/doc/mysql-shell/8.4/en/mysql-shell-utilities-upgrade.html) to perform pre-upgrade validation. Online validation for 8.0 to 8.4 support will be delivered in the near future.  
    > When using the 'Validate' feature to assess your database schema for compatibility with the target MySQL version, please take note of the following considerations:
    > - Table Locking During Validation: The validation process involves locking tables to inspect the entire schema accurately. This can lead to query timeouts if the database is under heavy load.
    >  
    > **Recommendation**: Avoid running validation during peak business hours or when the database handles high traffic. Instead, schedule the validation during low-activity periods to reduce the impact on operations.
    > - Potential for Hanging Due to Large Result Sets: In some instances—particularly with complex databases containing many objects—the validation result might become too large to be processed or displayed within the online workflow. This might result in the 'Validate' operation appearing to hang or remain in progress indefinitely.
    >  
    > **Recommendation**: If you encounter this issue, we suggest performing the validation locally using Oracle's official client-side upgrade checker tool, such as the one included in MySQL Shell. This approach avoids platform-side result size limitations and provides a more detailed and reliable validation output.
    > - Recommended Use Cases for Online Validation: The online 'Validate' feature is designed for simple or moderately complex schemas. For large-scale production environments—such as those with thousands of tables, views, routines, or other schema objects—we strongly recommend using Oracle's client-side upgrade checker tool to perform the compatibility check. This ensures the full schema is analyzed comprehensively and avoids potential issues related to result size or validation timeouts.

3. In the **Upgrade** sidebar, in the **MySQL version to upgrade** text box, verify the major MySQL version you want to upgrade to (for example, 8.0 or 8.4).

    :::image type="content" source="media/how-to-upgrade/2-how-to-upgrade.png" alt-text="Screenshot showing Upgrade.":::
    
    Before you can upgrade your primary server, you must first upgrade any associated read replica servers. Until this is completed, **Upgrade** is disabled.

4. On the primary server, select the confirmation message to verify that all replica servers have been upgraded, and then select **Upgrade**.
    
    :::image type="content" source="media/how-to-upgrade/how-to-upgrade.png" alt-text="Screenshot showing upgrade.":::

    **Upgrade** is enabled by default on read replica and standalone servers.

## Perform a planned major version upgrade using the Azure CLI

To perform a major version upgrade of an Azure Database for MySQL Flexible Server using the Azure CLI, perform the following steps.

1. Install the [Azure CLI](/cli/azure/install-azure-cli) for Windows or use the [Azure CLI](/azure/cloud-shell/overview) in Azure Cloud Shell to run the upgrade commands.

    This upgrade requires the Azure CLI version 2.40.0 or later. If you're using Azure Cloud Shell, the latest version is already installed. Run az version to find the version and dependent libraries that are installed. To upgrade to the latest version, run az upgrade.

2. After you sign in, run the [az MySQL server upgrade](/cli/azure/mysql/server#az-mysql-server-upgrade) command.

     ```azurecli
     az mysql flexible-server upgrade --name {your mysql server name} --resource-group {your resource group} --subscription {your subscription id} --version {target major version}
     ```

    Replace `{target major version}` with the version you want to upgrade to (for example, 8 or 8.4).

3. Under the confirmation prompt, type **y** to confirm or **n** to stop the upgrade process, and then press Enter.

## Perform a major version upgrade on a read replica server using the Azure portal

To perform a major version upgrade of an Azure Database for MySQL Flexible Server read replica server using the Azure portal, perform the following steps.

1. select your existing Azure Database for MySQL Flexible Server and read the replica server in the Azure portal.

2. On the **Overview** page, in the toolbar, select **Upgrade**.
    
    > [!IMPORTANT]
    > Before upgrading, visit the link for the list of [features removed](https://dev.mysql.com/doc/refman/8.0/en/mysql-nutshell.html#mysql-nutshell-removals) in the target MySQL version.
    > Verify deprecated [sql_mode](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_sql_mode) values and remove/deselect them from your current Azure Database for MySQL Flexible Server using the Server Parameters Blade on your Azure portal to avoid deployment failure.

3. In the **Upgrade** section, select **Upgrade** to upgrade an Azure Database for MySQL Flexible Server read replica server to the target major version.A notification appears to confirm that the upgrade is successful.

4. On the **Overview** page, confirm that your Azure Database for MySQL Flexible Server read replica server is running the target version.

5. go to your primary server and perform a major version upgrade.

## Perform minimal downtime major version upgrade using read replicas

To perform a major version upgrade of an Azure Database for MySQL Flexible Server with minimal downtime using read replica servers, perform the following steps.

1. select your existing Azure Database for MySQL Flexible Server instance in the Azure portal.

2. Create a [read replica](how-to-read-replicas-portal.md) from your primary server.

3. [Upgrade](#perform-a-planned-major-version-upgrade-using-the-azure-cli) your read replica to the target major version.

4. After you confirm that the replica server is running the target version, stop your application from connecting to your primary server.

5. Check replication status to ensure that the replica has caught up with the primary, so all data is in sync, and no new operations are being performed on the primary.

6. Confirm with the show replica status command on the replica server to view the replication status.

     ```azurecli
    SHOW SLAVE STATUS\G
    ```
    If the state of Slave_IO_Running and Slave_SQL_Running is **yes** and the value of Seconds_Behind_Master is **0**, replication works well. Seconds_Behind_Master indicates how late the replica is. If the value isn't **0**, then the replica is still processing updates. After you confirm that the value of Seconds_Behind_Master is **0**, it's safe to stop replication.

7. Promote your read replica to primary by stopping replication.

8. Set Server Parameter read_only to **0** (OFF) to start writing on the promoted primary.

9. Point your application to the new primary (former replica) running the target version. Each server has a unique connection string. Update your application to point to the (former) replica instead of the source.

    > [!NOTE]  
    > This scenario only incurs downtime during steps 4 through 7.

## Related content
- [How to upgrade Frequently asked questions](how-to-upgrade-faq.md)
- [How to configure scheduled maintenance](how-to-maintenance-portal.md)
- [MySQL version 8.0](https://dev.mysql.com/doc/refman/8.0/en/mysql-nutshell.html)
