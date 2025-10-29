---
title: "Tutorial: Migrate from MySQL to Azure Database for MySQL Online Using DMS Physical Migration via the Azure Portal"
description: Learn to perform an online physical migration from MySQL to Azure Database for MySQL by using Azure DMS.
author: saikondapalli11
ms.author: skondapalli
ms.reviewer: randolphwest, maghan
ms.date: 10/28/2025
ms.service: azure-database-migration-service
ms.topic: tutorial
ms.collection:
  - sql-migration-content
---

# Tutorial: Migrate from MySQL to Azure Database for MySQL using DMS physical migration with the Azure portal (Preview)

Using a physical backup file, you can seamlessly migrate your MySQL on-premises or Virtual Machine (VM) workload on Azure or other cloud services to Azure Database for MySQL. With physical backup files, you can quickly restore your source server to the target flexible server instance with minimal downtime. In this tutorial, we show you how to use Azure DMS to migrate MySQL workloads from on-premises or VMs to Azure Database for MySQL with minimal downtime using [Percona XtraBackup](https://www.percona.com/mysql/software/percona-xtrabackup).

> [!NOTE]  
> DMS *physical online data migration* is now in public preview. DMS supports migration to MySQL versions 5.7 and 8.0 and migration from lower version MySQL servers (v5.6 and higher) to a higher version MySQL server. In addition, DMS supports cross-region, cross-resource group, and cross-subscription migrations.

In this tutorial, you learn how to:

> [!div class="checklist"]
> - Create and configure the source MySQL server, target flexible server, and other required services.
> - Create a DMS instance.
> - Create a MySQL migration project for physical migration in DMS.
> - Run the migration.
> - Monitor the migration.
> - Perform post-migration activities.
> - Implement best practices for performing a migration.

## Prerequisites

To complete this tutorial, you need to:

- Create or use an existing MySQL instance (the source server, whether on-premises or on VMs in Azure or other clouds).

- To complete the online migration successfully, ensure that the following prerequisites are in place on the source MySQL server:

  - Ensure the parameter [lower_case_table_names](https://dev.mysql.com/doc/refman/8.4/en/identifier-case-sensitivity.html) is set to `1`.

  - Ensure the parameter [innodb_file_per_table](https://dev.mysql.com/doc/refman/8.4/en/innodb-parameters.html#sysvar_innodb_file_per_table) is set to `ON`.

  - The system tablespace should be [ibdata1](https://dev.mysql.com/doc/refman/8.4/en/innodb-system-tablespace.html).

  - System tablespace `ibdata1` size should be greater than or equal to `12MB` (MySQL Default).

  - Ensure the parameter [innodb_page_size](https://dev.mysql.com/doc/refman/8.4/en/innodb-parameters.html#sysvar_innodb_page_size) is set to `16384` (MySQL Default).

  - Only the `INNODB` storage engine is supported.

  - Ensure the binlog retention period is set appropriately using parameter [binlog_expire_logs_seconds](https://dev.mysql.com/doc/refman/8.4/en/replication-options-binary-log.html#sysvar_binlog_expire_logs_seconds) to complete the online migration.

  - Ensure that the user used for migration has `REPLICATION CLIENT` and `REPLICATION REPLICA` permissions on the source server to read and apply the bin log.

- Take a physical backup of your MySQL workload using Percona XtraBackup.

  The following are the steps for using Percona XtraBackup to take a complete backup:

  - Install Percona XtraBackup on the on-premises or VM workload. For MySQL engine version v5.7, install Percona XtraBackup version 2.4, see [Installing Percona XtraBackup 2.4]( https://docs.percona.com/percona-xtrabackup/2.4/installation.html). For MySQL engine version v8.0, install Percona XtraBackup version 8.0, see [Installing Percona XtraBackup 8.0]( https://docs.percona.com/percona-xtrabackup/8.0/installation.html).

  - For instructions for taking a Full backup with Percona XtraBackup 2.4, see [Full backup](https://docs.percona.com/percona-xtrabackup/2.4/backup_scenarios/full_backup.html). For instructions for taking a Full backup with Percona XtraBackup 8.0, see [Full backup](https://docs.percona.com/percona-xtrabackup/8.0/create-full-backup.html)

  - While taking full backup, run the below commands in order:

    Replace `{host}`, `{user}`, `{password}`, and `{backup_dir_path}` with appropriate values, and use the same backup path in both commands.

    ```console
    xtrabackup --backup --host={host} --user={user} --password={password} --target-dir={backup_dir_path}

    xtrabackup --prepare --{backup_dir_path}
    ```

  - Considerations while taking the Percona XtraBackup:

    - Make sure you run both the backup and prepare steps.
    - Make sure there are no errors in the backup and prepare step.
    - Keep the backup and prepare step logs for Azure Support, which is required if there are failures.

    > [!IMPORTANT]  
    > Attempting to access corrupted tables imported from a source server can cause the target flexible server to crash. As a result, before taking a backup using the Percona XtraBackup utility, performing a "mysqlcheck / Optimize Table" operation on the source server is recommended.

- Create the target flexible server. For guided steps, see the quickstart [Quickstart: Create an instance of Azure Database for MySQL with the Azure portal](../mysql/flexible-server/quickstart-create-server-portal.md).

  - On the target flexible server, set `max_allowed_packet` to `1073741824` (that is, 1 GB) to prevent connection issues due to a large row data transfer.

  - Set the `sql_mode` server parameter on the target flexible server to match the source server configuration.

  - Set the `TLS version` and `require_secure_transport` server parameters to match the values of the source server.

  - Configure server parameters on the target flexible server to match any non-default values used on the source server.

- [Create an Azure Blob container](/azure/storage/blobs/storage-quickstart-blobs-portal#create-a-container) and get the Shared Access Signature (SAS) Token ([Azure portal](/azure/ai-services/translator/document-translation/how-to-guides/create-sas-tokens?tabs=Containers#create-sas-tokens-in-the-azure-portal) or [Azure CLI](/azure/storage/blobs/storage-blob-user-delegation-sas-create-cli)) for the container. Ensure you grant **Add**, **Create**, and **Write** in the **Permissions** dropdown list.

  > [!IMPORTANT]  
  > Save the Blob SAS token and URL values in a secure location. They're only displayed once and can't be retrieved once the window is closed.

- Upload the full backup file from Percona XtraBackup at {backup_dir_path} to your Azure Blob storage. Follow these [steps to upload a file](/azure/storage/common/storage-use-azcopy-blobs-upload#upload-a-file).

- DMS uses the binlog positions captured when taking the full backup from the *xtrabackup_binlog_info* file to automatically initiate the replication process for a minimal downtime migration.

- The Azure storage account should be publicly accessible using the SAS token. Azure storage account with virtual network configuration isn't supported.

- Create an [App registration](/entra/identity-platform/quickstart-register-app?tabs=certificate), and generate an app key using [client secret](/entra/identity-platform/quickstart-register-app?tabs=client-secret#add-credentials), to be used in the physical migration workflow. This app can be used with the storage account and the target flexible server for SAS key creation and server update.

- [Assign the Role-based access control (RBAC) role assignment](/azure/role-based-access-control/role-assignments-portal) with the app registration for storage account with the following roles.

  - **Storage blob data reader** for reading blob container files.

- Assign the **Contributor** role to the **app registration** on the target MySQL flexible server.

## Limitations

As you prepare for the migration, consider the following limitations.

The source server configuration hasn't been migrated. You must configure the target Flexible server appropriately before initiating the migration.

- Migration for encrypted backups isn't supported.

- Migration cancellation during the import operation isn't supported.

- Online migration support is limited to the `ROW` binlog format.

- Azure Database for MySQL doesn't support mixed case databases.

- Azure DMS statement or binlog replication doesn't support the following syntax: `CREATE TABLE 'b' as SELECT * FROM 'a';`. The replication of this DDL results in the following error: "Only BINLOG INSERT, COMMIT, and ROLLBACK statements are allowed after CREATE TABLE with START TRANSACTION statement."

- Migration duration is affected by compute maintenance on the backend, which can reset the progress.

## Best practices for a faster data load using DMS

DMS supports cross-region, cross-resource group, and cross-subscription migrations, so you can select the appropriate region, resource group, and subscription for your target flexible server. Before you create your target flexible server, consider the following configuration guidance to help ensure faster data loads using DMS.

- For an optimal migration experience, Select the [compute size and compute tier](/azure/mysql/flexible-server/concepts-service-tiers-storage) for the target flexible server based on the source MySQL server configuration.

  - We recommend setting the target flexible server to a General-Purpose or business-critical SKU during the migration. Once the migration succeeds, you can scale the instance to an appropriate size to meet your application needs.

- The MySQL version of the target flexible server must be greater than or equal to that of the source MySQL server.

- Unless you need to deploy the target flexible server in a specific zone, set the value of the Availability Zone parameter to **No preference**.

- Consider deploying both the Azure blob storage and the target flexible server in the same region for better performance during import operations.

## Set up DMS

With your target flexible server deployed and configured, you next need to set up DMS to migrate your MySQL server to a flexible server.

### Register the resource provider

To register the Microsoft. The dataMigration resource provider performs the following steps:

1. Before you create your first DMS instance, sign in to the Azure portal, and then search for and select **Subscriptions**.

1. Select the subscription for which you want to create the DMS instance, then select **Resource providers**.

   :::image type="content" source="media/tutorial-mysql-azure-external-online-portal-physical/2-resource-provider.png" alt-text="Screenshot of a Select Resource Provider." lightbox="media/tutorial-mysql-azure-external-online-portal-physical/2-resource-provider.png":::

1. Search for "Migration" and then for **Microsoft.DataMigration**, select **Register**.

   :::image type="content" source="media/tutorial-mysql-azure-external-online-portal-physical/3-register.png" alt-text="Screenshot of a Register your resource provider.":::

### Create a Database Migration Service (DMS) instance

1. In the Azure portal, select **+ Create a resource**, search for the term "Azure Database Migration Service", and then select **Azure Database Migration Service** from the dropdown list.

   :::image type="content" source="media/tutorial-mysql-azure-external-online-portal-physical/4-dms-portal-marketplace.png" alt-text="Screenshot of DMS in Azure Marketplace." lightbox="media/tutorial-mysql-azure-external-online-portal-physical/4-dms-portal-marketplace.png":::

1. On the **Azure Database Migration Service** screen, select **Create**.

   :::image type="content" source="media/tutorial-mysql-azure-external-online-portal-physical/5-dms-portal-marketplace-create.png" alt-text="Screenshot of create from Azure Marketplace." lightbox="media/tutorial-mysql-azure-external-online-portal-physical/5-dms-portal-marketplace-create.png":::

1. On the **Select migration scenario and Database Migration Service** page, under **Migration scenario**, select **MySQL** as the source server type, and then select **Azure Database for MySQL** as target server type, and then select **Select**.

1. On the Create Migration Service page, on the Basics tab, under Project details, select the appropriate subscription, and then select an existing resource group or create a new one.

1. Under **Instance details**, specify a name for the service, select a region, and verify that **Azure** is selected as the service mode.

1. To the right of **Pricing tier**, select **Configure tier**.

   :::image type="content" source="media/tutorial-mysql-azure-external-online-portal-physical/7-project-details.png" alt-text="Screenshot of a Select Configure Tier.":::

1. Select the Premium pricing tier with 4 vCores for your DMS instance on the Configure page and then select Apply.

   DMS Premium 4-vCore is free for six months (183 days) from the date the DMS service was created before charges are incurred. For more information on DMS costs and pricing tiers, see the [pricing page](https://aka.ms/dms-pricing).

   :::image type="content" source="media/tutorial-mysql-azure-external-online-portal-physical/8-configure-pricing-tier.png" alt-text="Screenshot of a Select Pricing tier.":::

   Next, we need to specify the virtual network (virtual network) that provides the DMS instance access to the source MySQL server and the target flexible server.

1. On the **Create Migration Service** page, select **Next: Networking >>**.

1. On the **Networking** tab, select an existing virtual network from the list or provide the name of the new virtual network you want to create, then select **Review + Create**.

   For more information, see the article [Create a virtual network using the Azure portal.](/azure/virtual-network/quick-create-portal).

   :::image type="content" source="media/tutorial-mysql-azure-external-online-portal-physical/8-1-networking.png" alt-text="Screenshot of a Select Networking." lightbox="media/tutorial-mysql-azure-external-online-portal-physical/8-1-networking.png":::

   Your virtual network must be configured with access to both the source MySQL server and the target flexible server, so be sure to:

   - Create a server-level firewall rule for both the source MySQL server and the target MySQL flexible server to allow the virtual network for Azure Database Migration Service access to the source and target databases.
   - Ensure that your virtual network Network Security Group (NSG) rules don't block ServiceTag's outbound port 443 for ServiceBus, Storage, and Azure Monitor. For more information about virtual network NSG traffic filtering, see [Filter network traffic with network security groups](/azure/virtual-network/virtual-network-vnet-plan-design-arm).

   > [!NOTE]  
   > To add tags to the service, advance to the **Tags** tab by selecting **Next: Tags**. Adding tags to the service is optional.

1. Navigate to the **Review + create** tab, review the configurations, view the terms, and select **Create**.

   :::image type="content" source="media/tutorial-mysql-azure-external-online-portal-physical/9-review-create.png" alt-text="Screenshot of a Select Review+Create.":::

   Your DMS instance's deployment begins now. The message "Deployment is in progress" appears for a few minutes, and then it changes to "Your deployment is complete."

1. Select **Go to resource**.

   :::image type="content" source="media/tutorial-mysql-azure-external-online-portal-physical/9-1-go-to-resource.png" alt-text="Screenshot of a Select Go to resource." lightbox="media/tutorial-mysql-azure-external-online-portal-physical/9-1-go-to-resource.png":::

1. Identify the DMS instance's IP address from the resource overview page, create a firewall rule for your source MySQL server, and target a flexible server, allow-listing the IP address of the DMS instance.

### Create a migration project

To create a migration project, perform the following steps.

1. In the Azure portal, select **All services**, search for Azure Database Migration Service, and then select **Azure Database Migration Services**.

   :::image type="content" source="media/tutorial-mysql-azure-external-online-portal-physical/10-dms-search.png" alt-text="Screenshot of a DMS search." lightbox="media/tutorial-mysql-azure-external-online-portal-physical/10-dms-search.png":::

1. In the search results, select the DMS instance you created, and then select **+ New Migration Project**.

   :::image type="content" source="media/tutorial-mysql-azure-external-online-portal-physical/2-create-migration-project.png" alt-text="Screenshot of create migration project.":::

1. On the **New migration project** page, specify a name for the project. In the **Source server type** selection box, select **MySQL**. In the **Target server type** selection box, select **Azure Database For MySQL**. In the **Migration activity type** selection box, select **[Preview] Physical online data migration**. Then, select **Create and run activity**.

   Selecting **Create project only** as the migration activity type that only creates the migration project; you can then run it later.

   :::image type="content" source="media/tutorial-mysql-azure-external-online-portal-physical/3-migration-activity-select.png" alt-text="Screenshot of selecting a migration activity.":::

### Configure the migration project

To configure your DMS migration project, perform the following steps.

1. On the **Select source** screen, we must ensure that DMS is in the virtual network, which has connectivity to the source server. Here you input **source server name**, **server port**, **user name**, and **password** to your source MySQL server and then select **Next: Select target >>**

   :::image type="content" source="media/tutorial-mysql-azure-external-online-portal-physical/4-select-source-latest.png" alt-text="Screenshot of an Add source details screen." lightbox="media/tutorial-mysql-azure-external-online-portal-physical/4-select-source-latest.png":::

1. On the **Select target** screen, under automated Server selection, choose the **Subscription**, **Location**, **Resource group**, Azure Database for MySQL **server name**, **user name**, **password** for your target Azure Database for MySQL server and select **Next: Select backup >>**

   :::image type="content" source="media/tutorial-mysql-azure-external-online-portal-physical/5-select-target-latest.png" alt-text="Screenshot of a Select target." lightbox="media/tutorial-mysql-azure-external-online-portal-physical/5-select-target-latest.png":::

1. On the **Select backup** screen, input the **application ID** of the app registration, **client secret** from the app registration, **tenant ID** from the app registration, **subscription**, **storage account** name, **blob container** name, and the **backup directory** name where the Percona XtraBackup files are stored and select **Next: Configure migration settings >>**

   There's now a **Migrate user accounts and privileges** option. When selected, this option migrates all sign-in migrations. Additionally, you can replicate any **DDL statements** from the source MySQL server to the target flexible server.

   :::image type="content" source="media/tutorial-mysql-azure-external-online-portal-physical/6-select-backup-latest.png" alt-text="Screenshot of a Select backup screen." lightbox="media/tutorial-mysql-azure-external-online-portal-physical/6-select-backup-latest.png":::

1. On the **Configure migration settings** screen, if you want to customize the migration settings, select the check box or else advance to the summary page by selecting the **Next: Summary >>**

   :::image type="content" source="media/tutorial-mysql-azure-external-online-portal-physical/7-configure-migration-settings.png" alt-text="Screenshot of configuring migration settings page.":::

1. On the Summary screen, in the Activity Name text box, specify a name for the migration activity. Ensure all the migration-related details are correct, then select "Start Migration."

   :::image type="content" source="media/tutorial-mysql-azure-external-online-portal-physical/8-migration-summary-latest.png" alt-text="Screenshot of migration summary and details page." lightbox="media/tutorial-mysql-azure-external-online-portal-physical/8-migration-summary-latest.png":::

1. Once the migration starts, the migration activity window appears. Under the Initial Load tab, the status changes to Running.

### Monitor the migration

1. As the migration is in flight, you can review the status of the migration and notice states such as **Importing** and **Estimated time remaining** for the physical backup files' data ingestion into the target MySQL flexible server.

   :::image type="content" source="media/tutorial-mysql-azure-external-online-portal-physical/9-migration-status-latest.png" alt-text="Screenshot of migration status page." lightbox="media/tutorial-mysql-azure-external-online-portal-physical/9-migration-status-latest.png":::

   After the initial load activity is completed, you automatically navigate to the **Replicate Data Changes** tab. You can monitor the migration progress as the screen autorefreshes every 30 seconds, or select the **Refresh** button.

1. Once the initial data ingestion completes, monitor the **Seconds behind source** field under the **Replicate Data Changes** tab. As soon as it's 0, proceed to start the cutover by navigating to the **Start Cutover** button at the top of the migration activity screen. Select **Refresh** to update the display and view the seconds behind the source when needed.

   :::image type="content" source="media/tutorial-mysql-azure-external-online-portal-physical/10-migration-replication-status-latest.png" alt-text="Screenshot of monitoring replication status." lightbox="media/tutorial-mysql-azure-external-online-portal-physical/10-migration-replication-status-latest.png":::

1. Before you're ready to perform a cutover, follow steps 1 through 3 in the cutover window.

1. After completing all steps, select **Confirm**, and then select **Apply**.

   :::image type="content" source="media/tutorial-mysql-azure-external-online-portal-physical/11-start-cutover.png" alt-text="Screenshot of a Perform cutover.":::

## Perform post-migration activities

When the migration finishes, be sure to complete the following post-migration activities.

- Perform validation and data integration against the target database to certify the migration completion using one of the mentioned approaches.

  - You can validate data by comparing **row count** or **checksum** between source and target flexible servers.

  - You can additionally go to the target flexible server, under **settings**, select **Databases** page, and verify that the databases intended for migration have successfully migrated to the target.

    :::image type="content" source="media/tutorial-mysql-azure-external-online-portal-physical/12-validate-migration-target.png" alt-text="Screenshot of validating migration target.":::

- Update the connection string to point to the new flexible server.

  - To clean up the DMS resources, perform the following steps:

  1. In the Azure portal, select **All services**, search for Azure Database Migration Service, and then select **Azure Database Migration Services**.

  1. Select your migration service instance from the search results, and then select **Delete service**.

  1. In the confirmation dialog box, in the **TYPE THE DATABASE MIGRATION SERVICE NAME** textbox, specify the instance's name and then select **Delete.**

- Create any [read replicas](/azure/mysql/flexible-server/concepts-read-replicas) for the flexible server for scalability and recovery.

## Migration best practices

When performing a migration, be sure to consider the following best practices.

- As part of discovery and assessment, consider the server SKU, CPU usage, storage, database sizes, and extension usage as some of the critical data to help with migrations.

- Perform test migrations before migrating for production:

  - Test migrations are important to ensure you cover all aspects of database migration, including application testing. The best practice is to begin by running a migration entirely for testing purposes. After a newly started migration enters the Replicate Data Changes phase with minimal lag, only use your Flexible Server target for running test workloads. Use that target to test the application and ensure expected performance and results. Test for application compatibility if you're migrating to a higher MySQL version.

  - After testing is completed, you can migrate the production databases. At this point, you need to finalize the day and time of the production migration. Ideally, there's low application use at this time. All stakeholders who need to be involved should be available and ready. The production migration requires close monitoring. For an online migration, the replication must be completed before you perform the cutover to prevent data loss.

- Redirect all dependent applications to access the new primary database and make the source server read-only. Then, open the applications for production usage.

- After the application starts running on the target flexible server, monitor the database performance closely to determine whether performance tuning is required.

## Related content

- [What is Azure Database for MySQL - Flexible Server?](../mysql/flexible-server/overview.md)
- [What is Azure Database Migration Service?](dms-overview.md)
- [Known Issues With Migrations To Azure Database for MySQL](known-issues-azure-mysql-fs-online.md)
- [Troubleshoot common Azure Database Migration Service (classic) issues and errors](known-issues-troubleshooting-dms.md)
- [Troubleshoot DMS errors when connecting to source databases](known-issues-troubleshooting-dms-source-connectivity.md)
