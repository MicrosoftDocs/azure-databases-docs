---
title: "Tutorial: Migrate from MySQL to Azure Database for MySQL - Flexible Server online using DMS physical migration via the Azure portal (preview)"
titleSuffix: "Azure Database Migration Service"
description: "Learn to perform an online physical migration from MySQL to Azure Database for MySQL - Flexible Server by using Azure DMS."
author: skondapalli
ms.author: skondapalli
ms.reviewer: maghan, randolphwest
ms.date: 02/18/2025
ms.service: azure-database-migration-service
ms.topic: tutorial
ms.collection:
  - sql-migration-content
---

# Tutorial: Migrate from MySQL to Azure Database for MySQL - Flexible Server online using DMS physical migration via the Azure portal (preview)

> [!NOTE]  
> This article contains references to the term *slave*, a term that Microsoft no longer uses. When the term is removed from the software, we'll remove it from this article.

You can seamlessly migrate your MySQL on-premises or Virtual Machine (VM) workload on Azure or other cloud services to Azure Database for MySQL - Flexible Server using a physical backup file. With physical backup files you can quickly restore your source server on to the target flexible server instance with minimal downtime. In this tutorial we show you how to use Azure DMS to migrate MySQL workloads from on-premises or VMs to Azure Database for MySQL - Flexible Server with minimal downtime using [Percona XtraBackup](https://www.percona.com/mysql/software/percona-xtrabackup). 

> [!NOTE]  
> DMS **physical online data migration** is now in public preview. DMS supports migration to MySQL versions 5.7 and 8.0 and also supports migration from lower version MySQL servers (v5.6 and above) to a higher version MySQL server. In addition, DMS supports cross-region, cross-resource group, and cross-subscription migrations.

In this tutorial, you'll learn how to:

> [!div class="checklist"]
> - Create and configure the source MySQL server, target flexible server, and other required services.
> - Create a DMS instance.
> - Create a MySQL migration project for physical migration in DMS.
> - Run the migration.
> - Monitor the migration.
> - Perform post-migration activites.
> - Implement best practices for performing a migration.

## Prerequisites

To complete this tutorial, you need to:

- Create or use an existing MySQL instance (the source server whether on-premises or on VMs in Azure or other clouds).
- To complete the online migration successfully, ensure that the following prerequisites are in place on the source MySQL server:
  - Ensure the parameter [lower_case_table_names](https://dev.mysql.com/doc/refman/8.4/en/identifier-case-sensitivity.html) is set to **1**.
  - Ensure the parameter [innodb_file_per_table](https://dev.mysql.com/doc/refman/8.4/en/innodb-parameters.html#sysvar_innodb_file_per_table) is set to **ON**
  - The system tablespace should be [ibdata1](https://dev.mysql.com/doc/refman/8.4/en/innodb-system-tablespace.html).
  - System tablespace **ibdata1** size should be greater than or equal to **12MB** (MySQL Default).
  - Ensure the parameter [innodb_page_size](https://dev.mysql.com/doc/refman/8.4/en/innodb-parameters.html#sysvar_innodb_page_size) is set to **16384** (MySQL Default)
  - Only **INNODB** storage engine is supported.
  - Ensure the binlog retention period is set appropriately using parameter [binlog_expire_logs_seconds](https://dev.mysql.com/doc/refman/8.4/en/replication-options-binary-log.html#sysvar_binlog_expire_logs_seconds) to complete the online migration.
  - Ensure that the user used for migration has "REPLICATION CLIENT" and "REPLICATION SLAVE" permissions on the source server for reading and applying the bin log.
- Take a physical backup of your MySQL workload using Percona XtraBackup.
   The following are the steps for using Percona XtraBackup to take a full backup:
   - Install Percona XtraBackup on the on-premises or VM workload. For MySQL engine version v5.7, install Percona XtraBackup version 2.4, see [Installing Percona XtraBackup 2.4]( https://docs.percona.com/percona-xtrabackup/2.4/installation.html). For MySQL engine version v8.0, install Percona XtraBackup version 8.0, see [Installing Percona XtraBackup 8.0]( https://docs.percona.com/percona-xtrabackup/8.0/installation.html).
   - For instructions for taking a Full backup with Percona XtraBackup 2.4, see [Full backup](https://docs.percona.com/percona-xtrabackup/2.4/backup_scenarios/full_backup.html). For instructions for taking a Full backup with Percona XtraBackup 8.0, see [Full backup](https://docs.percona.com/percona-xtrabackup/8.0/create-full-backup.html)
      - While taking full backup, run the below commands in order:
        - **xtrabackup --backup --host={host} --user={user} --password={password} --target-dir={backup__dir_path}**
        - **xtrabackup --prepare --{backup_dir_path}** (Provide the same backup path here as in the previous command)
      - Considerations while taking the Percona XtraBackup:
        - Make sure you run both the backup and prepare step.
        - Make sure there are no errors in the backup and prepare step.
        - Keep the backup and prepare step logs for Azure Support, which is required in case of failures.
    > [!IMPORTANT]
      > Attempting to access corrupted tables imported from a source server can cause the target flexible server to crash. As a result, before taking a backup using the Percona XtraBackup utility, it is strongly recommended to perform a "mysqlcheck / Optimize Table" operation on the source server.
- Create the target flexible server. For guided steps, see the quickstart [Quickstart: Create an instance of Azure Database for MySQL with the Azure portal](../mysql/flexible-server/quickstart-create-server-portal.md).
   - On the target flexible server, set **max_allowed_packet** to **1073741824 (i.e., 1GB)** to prevent any connection issues due toa  large row data transfer.
   - Set **sql_mode** server parameter on the target flexible server to match the source server configuration. 
   - Set the **TLS version** and **require_secure_transport** server parameter to match the values of the source server.
   - Configure server parameters on the target flexible server to match any non-default values used on the source server.
- [Create an Azure Blob container](https://learn.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-portal#create-a-container) and get the Shared Access Signature (SAS) Token ([Azure portal](https://learn.microsoft.com/en-us/azure/ai-services/translator/document-translation/how-to-guides/create-sas-tokens?tabs=Containers#create-sas-tokens-in-the-azure-portal) or [Azure CLI](https://learn.microsoft.com/en-us/azure/storage/blobs/storage-blob-user-delegation-sas-create-cli)) for the container. Ensure that you grant **Add**, **Create**, and **Write** in the **Permissions** dropdown list. 
    > [!IMPORTANT]
      > Save the Blob SAS token and URL values in a secure location. They are only displayed once and can't be retrieved once the window is closed.
- Upload the full backup file from Percona Xtrabackup at {backup_dir_path} to your Azure Blob storage. Follow these [steps to upload a file](https://learn.microsoft.com/en-us/azure/storage/common/storage-use-azcopy-blobs-upload#upload-a-file).
- DMS uses the binlog positions captured at the time of taking the full backup from *xtrabackup_binlog_info* file to automatically initiate the replication process for a minimal downtime migration.
- The Azure storage account should be publicly accessible using SAS token. Azure storage account with virtual network configuration is not supported.
- An [App registration](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app?tabs=certificate) needs to be created, and an app key using [client secret](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app?tabs=client-secret#add-credentials) has to be generated to be used with physical migration workflow. This app will in turn be used with the storage account and the target flexible server for SAS key creation and server update. 
- [Assign the RBAC role assignment](https://learn.microsoft.com/en-us/azure/role-based-access-control/role-assignments-portal) with the app registration for storage account with the following roles.
    - **Storage blob data reader** for reading blob container files.
- Assign the **Contributor** role to the **app registration** on the target MySQL flexible server.

## Limitations

As you prepare for the migration, be sure to consider the following limitations.

- Source server configuration isn't migrated. You must configure the target Flexible server appropriately prior to initiating the migration.
- Migration for encrypted backups isn't supported.
- Migration cancellation during the import operation is not supported. 
- Online migration support is limited to the **ROW** binlog format.
- Azure Database for MySQL - Flexible Server doesn't support mixed case databases.
- Azure DMS statement or binlog replication doesn't support the following syntax: 'CREATE TABLE `b` as SELECT * FROM `a`;'. The replication of this DDL will result in the following error: "Only BINLOG INSERT, COMMIT and ROLLBACK statements are allowed after CREATE TABLE with START TRANSACTION statement."
- Migration duration can be affected by compute maintenance on the backend, which can reset the progress.

## Best practices for a faster data loads using DMS

DMS supports cross-region, cross-resource group, and cross-subscription migrations, so you're free to select appropriate region, resource group and subscription for your target flexible server. Before you create your target flexible server, consider the following configuration guidance to help ensure faster data loads using DMS.

- Select the [compute size and compute tier](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/concepts-service-tiers-storage) for the target flexible server based on the source MySQL server configuration for an optimal migration experience.
    - We recommend setting the target flexible server to a General Purpose or a Business Critical SKU for the duration of the migration, once the migration succeeds, you can scale the instance to an appropriate size to meet your application needs.

- The MySQL version for the target flexible server must be greater than or equal to that of the source MySQL server.

- Unless you need to deploy the target flexible server in a specific zone, set the value of the Availability Zone parameter to 'No preference'.

- Consider the deployment of both the Azure blob storage and the target flexible server in the same region for a better performance during import operation.


## Set up DMS

With your target flexible server deployed and configured, you next need to set up DMS to migrate your MySQL server to a flexible server.

### Register the resource provider

To register the Microsoft.DataMigration resource provider, perform the following steps.

1. Before creating your first DMS instance, sign in to the Azure portal, and then search for and select **Subscriptions**.

   :::image type="content" source="media/tutorial-mysql-external-to-flex-online-physical-portal/1-subscriptions.png" alt-text="Screenshot of a Select subscriptions from Azure Marketplace." lightbox="media/tutorial-mysql-external-to-flex-online-physical-portal/1-subscriptions.png":::

1. Select the subscription that you want to use to create the DMS instance, and then select **Resource providers**.

   :::image type="content" source="media/tutorial-mysql-external-to-flex-online-physical-portal/2-resource-provider.png" alt-text="Screenshot of a Select Resource Provider." lightbox="media/tutorial-mysql-external-to-flex-online-physical-portal/2-resource-provider.png":::

1. Search for the term "Migration", and then, for **Microsoft.DataMigration**, select **Register**.

   :::image type="content" source="media/tutorial-mysql-external-to-flex-online-physical-portal/3-register.png" alt-text="Screenshot of a Register your resource provider." lightbox="media/tutorial-mysql-external-to-flex-online-physical-portal/3-register.png":::

### Create a Database Migration Service (DMS) instance

1. In the Azure portal, select **+ Create a resource**, search for the term "Azure Database Migration Service", and then select **Azure Database Migration Service** from the dropdown list.

   :::image type="content" source="media/tutorial-mysql-external-to-flex-online-physical-portal/4-dms-portal-marketplace.png" alt-text="Screenshot of a Search Azure Database Migration Service." lightbox="media/tutorial-mysql-external-to-flex-online-physical-portal/4-dms-portal-marketplace.png":::

1. On the **Azure Database Migration Service** screen, select **Create**.

   :::image type="content" source="media/tutorial-mysql-external-to-flex-online-physical-portal/5-dms-portal-marketplace-create.png" alt-text="Screenshot of a Create Azure Database Migration Service instance." lightbox="media/tutorial-mysql-external-to-flex-online-physical-portal/5-dms-portal-marketplace-create.png":::

1. On the **Select migration scenario and Database Migration Service** page, under **Migration scenario**, select **MySQL** as the source server type, and then select **Azure Database for MySQL** as target server type, and then select **Select**.

   :::image type="content" source="media/tutorial-azure-mysql-external-to-flex-online/create-database-migration-service.png" alt-text="Screenshot of a Select Migration Scenario." lightbox="media/tutorial-azure-mysql-external-to-flex-online/create-database-migration-service.png":::

1. On the **Create Migration Service** page, on the **Basics** tab, under **Project details**, select the appropriate subscription, and then select an existing resource group or create a new one.

1. Under **Instance details**, specify a name for the service, select a region, and then verify that **Azure** is selected as the service mode.

1. To the right of **Pricing tier**, select **Configure tier**.

   :::image type="content" source="media/tutorial-mysql-external-to-flex-online-physical-portal/7-project-details.png" alt-text="Screenshot of a Select Configure Tier." lightbox="media/tutorial-mysql-external-to-flex-online-physical-portal/7-project-details.png":::

1. On the **Configure** page, select the **Premium** pricing tier with 4 vCores for your DMS instance, and then select **Apply**.

   DMS Premium 4-vCore is free for 6 months (183 days) from the DMS service creation date before incurring any charges. For more information on DMS costs and pricing tiers, see the [pricing page](https://aka.ms/dms-pricing).

   :::image type="content" source="media/tutorial-mysql-external-to-flex-online-physical-portal/8-configure-pricing-tier.png" alt-text="Screenshot of a Select Pricing tier." lightbox="media/tutorial-mysql-external-to-flex-online-physical-portal/8-configure-pricing-tier.png":::

    Next, we need to specify the VNet that will provide the DMS instance with access to the source MySQL server and the target flexible server.

1. On the **Create Migration Service** page, select **Next : Networking >>**.

1. On the **Networking** tab, select an existing VNet from the list or provide the name of new VNet to create, and then select **Review + Create**.

   For more information, see the article [Create a virtual network using the Azure portal.](/azure/virtual-network/quick-create-portal).

   :::image type="content" source="media/tutorial-mysql-external-to-flex-online-physical-portal/8-1-networking.png" alt-text="Screenshot of a Select Networking." lightbox="media/tutorial-mysql-external-to-flex-online-physical-portal/8-1-networking.png":::

   Your VNet must be configured with access to both the source MySQL server and the target flexible server, so be sure to:

   - Create a server-level firewall rule for both the source MySQL server and the target MySQL flexible server to allow the VNet for Azure Database Migration Service access to the source and target databases.
   - Ensure that your VNet Network Security Group (NSG) rules don't block the outbound port 443 of ServiceTag for ServiceBus, Storage, and Azure Monitor. For more information about VNet NSG traffic filtering, see [Filter network traffic with network security groups](/azure/virtual-network/virtual-network-vnet-plan-design-arm).

   > [!NOTE]  
   > To add tags to the service, advance to the **Tags** tab by selecting **Next : Tags**. Adding tags to the service is optional.

1. Navigate to the **Review + create** tab, review the configurations, view the terms, and then select **Create**.

   :::image type="content" source="media/tutorial-mysql-external-to-flex-online-physical-portal/9-review-create.png" alt-text="Screenshot of a Select Review+Create." lightbox="media/tutorial-mysql-external-to-flex-online-physical-portal/9-review-create.png":::

   Deployment of your instance of DMS now begins. The message **Deployment is in progress** appears for a few minutes, and then the message changes to **Your deployment is complete**.

1. Select **Go to resource**.

   :::image type="content" source="media/tutorial-mysql-external-to-flex-online-physical-portal/9-1-go-to-resource.png" alt-text="Screenshot of a Select Go to resource." lightbox="media/tutorial-mysql-external-to-flex-online-physical-portal/9-1-go-to-resource.png":::

1. Identify the IP address of the DMS instance from the resource overview page and create a firewall rule for your source MySQL server and target flexible server allow-listing the IP address of the DMS instance.

### Create a migration project

To create a migration project, perform the following steps.

1. In the Azure portal, select **All services**, search for Azure Database Migration Service, and then select **Azure Database Migration Services**.

   :::image type="content" source="media/tutorial-mysql-external-to-flex-online-physical-portal/10-dms-search.png" alt-text="Screenshot of a Locate all instances of Azure Database Migration Service." lightbox="media/tutorial-mysql-external-to-flex-online-physical-portal/10-dms-search.png":::

1. In the search results, select the DMS instance that you created, and then select **+ New Migration Project**.

   :::image type="content" source="media/tutorial-mysql-external-to-flex-online-physical-portal/2-create-migration-project.png" alt-text="Screenshot of a Select a new migration project." lightbox="media/tutorial-mysql-external-to-flex-online-physical-portal/2-create-migration-project.png":::

1. On the **New migration project** page, specify a name for the project, in the **Source server type** selection box, select **MySQL**, in the **Target server type** selection box, select **Azure Database For MySQL - Flexible Server**, in the **Migration activity type** selection box, select **[Preview] Physical online data migration**, and then select **Create and run activity**.

   Selecting **Create project only** as the migration activity type will only create the migration project; you can then run the migration project at a later time.

   :::image type="content" source="media/tutorial-mysql-external-to-flex-online-physical-portal/3-migration-activity-select.png" alt-text="Screenshot of a Create a new migration project." lightbox="media/tutorial-mysql-external-to-flex-online-physical-portal/3-migration-activity-select.png":::

### Configure the migration project

To configure your DMS migration project, perform the following steps.

1. On the **Select source** screen, we must ensure that DMS is in the VNet which has connectivity to the source server. Here you'll input **source server name**, **server port**, **user name**, and **password** to your source MySQL server and then click **Next: Select target >>**

   :::image type="content" source="media/tutorial-mysql-external-to-flex-online-physical-portal/4-select-source.png" alt-text="Screenshot of an Add source details screen." lightbox="media/tutorial-mysql-external-to-flex-online-physical-portal/4-select-source.png":::

1. On the **Select target** screen, under automated Server selection, choose the **Subscription**, **Location**, **Resource group**, Azure Database for MySQL **server name**, **user name**, **password** for your target Azure Database for MySQL server and click **Next: Select backup >>**

   :::image type="content" source="media/tutorial-mysql-external-to-flex-online-physical-portal/5-select-target.png" alt-text="Screenshot of a Select target."lightbox="media/tutorial-mysql-external-to-flex-online-physical-portal/5-select-target.png":::

1. On the **Select backup** screen, input the **application ID** of the app registration, **client secret** from the app registration, **tenant ID** from the app registration, **subscription**, **storage account** name, **blob container** name and the **backup directory** name where the percona xtrabackup files are stored and click **Next: Configure migration settings >>**

   There's now a **Migrate user accounts and privileges** option. When selected, this option will migrate all login migrations. Additionally you can replicate any **DDL statements** from the source MySQL server to the target flexible server.

   :::image type="content" source="media/tutorial-mysql-external-to-flex-online-physical-portal/6-select-backup.png" alt-text="Screenshot of a Select database." lightbox="media/tutorial-mysql-external-to-flex-online-physical-portal/6-select-backup.png":::

1. On the **Configure migration settings** screen, if you want to customize the migration settings, click on the check box or else advance to the summary page by clicking on the **Next: Summary >>**

     :::image type="content" source="media/tutorial-mysql-external-to-flex-online-physical-portal/7-configure-migration-settings.png" alt-text="Screenshot of a Select database." lightbox="media/tutorial-mysql-external-to-flex-online-physical-portal/7-configure-migration-settings.png":::

1. On the **Summary** screen, in the **Activity Name** text box, specify a name for the migration activity, then ensure all the migration related details are correct and click **Start Migration**. 
    :::image type="content" source="media/tutorial-mysql-external-to-flex-online-physical-portal/8-migration-summary.png" alt-text="Screenshot of a Select database." lightbox="media/tutorial-mysql-external-to-flex-online-physical-portal/8-migration-summary.png":::

1. Once the migration starts, the migration activity window appears. The status changes to **Running** under the **Initial Load** tab.


### Monitor the migration

1. As the migration is in flight, you can review the status of the migration and notice states such as **Importing**, and **Estimated time remaining** for the physical backup files data ingestion into the target MySQL flexible server.

   :::image type="content" source="media/tutorial-mysql-external-to-flex-online-physical-portal/9-migration-status.png" alt-text="Screenshot of a completed initial load migration." lightbox="media/tutorial-mysql-external-to-flex-online-physical-portal/9-migration-status.png":::

   After the **Initial Load** activity is completed, you're navigated to the **Replicate Data Changes** tab automatically. You can monitor the migration progress as the screen is auto-refreshed every 30 seconds or click on the **Refresh** button. 

1. Once the initial data ingestion is complete. Monitor the **Seconds behind source** field under **Replicate Data Changes** tab and as soon as it is 0, proceed to start cutover by navigating to the **Start Cutover** button at the top of the migration activity screen. Select **Refresh** to update the display and view the seconds behind source when needed.

   :::image type="content" source="media/tutorial-mysql-external-to-flex-online-physical-portal/10-migration-replication-status.png" alt-text="Screenshot of a Monitoring migration." lightbox="media/tutorial-mysql-external-to-flex-online-physical-portal/10-migration-replication-status.png":::

1. Follow the steps 1 through 3 in the cutover window before you're ready to perform a cutover.

1. After completing all steps, select **Confirm**, and then select **Apply**.

   :::image type="content" source="media/tutorial-mysql-external-to-flex-online-physical-portal/11-start-cutover.png" alt-text="Screenshot of a Perform cutover." lightbox="media/tutorial-mysql-external-to-flex-online-physical-portal/11-start-cutover.png":::

## Perform post-migration activities

When the migration has finished, be sure to complete the following post-migration activities.

- Perform validation and data integration against the target database to certify the migration completion using one of the mentioned approaches.
    - You can validate data by comparing **row count** or **checksum** between source and target flexible servers.
    - You can additionally go to the target flexible server, under **settings** select **Databases** blade and verify that the databases intended for migration have successfully migrated to the target. 

    :::image type="content" source="media/tutorial-mysql-external-to-flex-online-physical-portal/12-validate-migration-target.png" alt-text="Screenshot of a Perform cutover." lightbox="media/tutorial-mysql-external-to-flex-online-physical-portal/12-validate-migration-target.png":::

- Update the connection string to point to the new flexible server.

  - To clean up the DMS resources, perform the following steps:

    1. In the Azure portal, select **All services**, search for Azure Database Migration Service, and then select **Azure Database Migration Services**. 

    1. Select your migration service instance from the search results, and then select **Delete service**.

    1. In the confirmation dialog box, in the **TYPE THE DATABASE MIGRATION SERVICE NAME** textbox, specify the name of the instance, and then select **Delete**.

- Create any [read replicas](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/concepts-read-replicas) for the flexible server for scalability as well as recovery purposes.

## Migration best practices

When performing a migration, be sure to consider the following best practices.

- As part of discovery and assessment, take the server SKU, CPU usage, storage, database sizes, and extensions usage as some of the critical data to help with migrations.

- Perform test migrations before migrating for production:

  - Test migrations are important for ensuring that you cover all aspects of the database migration, including application testing. The best practice is to begin by running a migration entirely for testing purposes. After a newly started migration enters the Replicate Data Changes phase with minimal lag, only use your Flexible Server target for running test workloads. Use that target for testing the application to ensure expected performance and results. If you're migrating to a higher MySQL version, test for application compatibility.

  - After testing is completed, you can migrate the production databases. At this point, you need to finalize the day and time of production migration. Ideally, there's low application use at this time. All stakeholders who need to be involved should be available and ready. The production migration requires close monitoring. For an online migration, the replication must be completed before you perform the cutover, to prevent data loss.

- Redirect all dependent applications to access the new primary database and make the source server read-only. Then, open the applications for production usage.

- After the application starts running on the target flexible server, monitor the database performance closely to see if performance tuning is required.

## Related content

- [What is Azure Database for MySQL - Flexible Server?](../mysql/flexible-server/overview.md)
- [What is Azure Database Migration Service?](dms-overview.md)
- [Known Issues With Migrations To Azure Database for MySQL](known-issues-azure-mysql-fs-online.md)
- [Troubleshoot common Azure Database Migration Service (classic) issues and errors](known-issues-troubleshooting-dms.md)
- [Troubleshoot DMS errors when connecting to source databases](known-issues-troubleshooting-dms-source-connectivity.md)
