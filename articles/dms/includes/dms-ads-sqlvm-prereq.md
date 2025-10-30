---
author: abhims14
ms.author: abhishekum
ms.reviewer: randolphwest
ms.date: 10/13/2025
ms.service: azure-database-migration-service
ms.topic: include
ms.collection:
  - sql-migration-content
---

- [Download and install Azure Data Studio](/azure-data-studio/download-azure-data-studio).

- [Install the Azure SQL Migration extension](/azure-data-studio/extensions/azure-sql-migration-extension) from Azure Data Studio Marketplace.

- Have an Azure account that's assigned to one of the following built-in roles:

  > [!IMPORTANT]  
  > An Azure account is required only when you configure the migration steps. An Azure account isn't required for the assessment or to view Azure recommendations in the migration wizard in Azure Data Studio.

  - Contributor for the target instance of SQL Server on Azure Virtual Machines and for the storage account where you upload your database backup files from a Server Message Block (SMB) network share.
  - Reader role for the Azure resource group that contains the target instance of SQL Server on Azure Virtual Machines or for your Azure Storage account.
  - Owner or Contributor role for the Azure subscription.
  - As an alternative to using one of these built-in roles, you can [assign a custom role](/data-migration/sql-server/virtual-machines/custom-roles).

  > [!NOTE]  
  > When migrating to Azure SQL Managed Instance or Azure SQL Virtual Machine via **Azure portal**, make sure the signed in user has **Storage Blob Data Reader** access on the blob container that contains the backup files. This permission is needed to list folders and files in the blob container during migration setup via Azure portal only.

- Create a target instance of [SQL Server on Azure Virtual Machines](/azure/azure-sql/virtual-machines/windows/create-sql-vm-portal).

  If you have an existing Azure virtual machine, it should be registered with the [SQL Server IaaS Agent Extension in Full management mode](/azure/azure-sql/virtual-machines/windows/sql-server-iaas-agent-extension-automate-management#management-modes).

- Ensure that the logins that you use to connect the source SQL Server instance are members of the **sysadmin** server role or have `CONTROL SERVER` permission.

- Provide an SMB network share, Azure storage account file share, or Azure storage account blob container that contains your full database backup files and subsequent transaction log backup files. Database Migration Service uses the backup location during database migration.

  > [!IMPORTANT]  
  > - Always use a dedicated storage account for migration. Sharing it with other workloads can lead to conflicts and security risks.
  > - Once migration is done, either rotate the Storage Account Key to keep backups secure, or delete the storage account if it's no longer needed.
  > - The Azure SQL Migration extension for Azure Data Studio doesn't take database backups, or neither initiate any database backups on your behalf. Instead, the service uses existing database backup files for the migration.
  > - If your database backup files are in an SMB network share, [create an Azure storage account](/azure/storage/common/storage-account-create) that Database Migration Service can use to upload database backup files to and to migrate databases. Make sure you create the Azure storage account in the same region where you create your instance of Database Migration Service.
  > - You can write each backup to either a separate backup file or to multiple backup files. Appending multiple backups such as full and transaction logs into a single backup media isn't supported.
  > - You can provide compressed backups to reduce the likelihood of experiencing potential issues associated with migrating large backups.

- Ensure that the service account that's running the source SQL Server instance has read and write permissions on the SMB network share that contains database backup files.

- If you're migrating a database that's protected by transparent data encryption (TDE), the certificate from the source SQL Server instance must be migrated to SQL Server on Azure Virtual Machines before you migrate data. To learn more, see [Move a TDE-protected database to another SQL Server instance](/sql/relational-databases/security/encryption/move-a-tde-protected-database-to-another-sql-server).

  > [!TIP]  
  > If your database contains sensitive data that's protected by [Always Encrypted](/sql/relational-databases/security/encryption/configure-always-encrypted-using-sql-server-management-studio), the migration process automatically migrates your Always Encrypted keys to your target instance of SQL Server on Azure Virtual Machines.

- If your database backups are on a network file share, provide a computer on which you can install a [self-hosted integration runtime](/azure/data-factory/create-self-hosted-integration-runtime) to access and migrate database backups. The migration wizard gives you the download link and authentication keys to download and install your self-hosted integration runtime.

  In preparation for the migration, ensure that the computer on which you install the self-hosted integration runtime has the following outbound firewall rules and domain names enabled:

  | Domain names | Outbound port | Description |
  | --- | --- | --- |
  | Public cloud: `{datafactory}.{region}.datafactory.azure.net`<br />or `*.frontend.clouddatahub.net`<br /><br />Azure Government: `{datafactory}.{region}.datafactory.azure.us`<br />Microsoft Azure operated by 21Vianet: `{datafactory}.{region}.datafactory.azure.cn` | 443 | Required by the self-hosted integration runtime to connect to Database Migration Service.<br />For a newly created data factory in a public cloud, locate the fully qualified domain name (FQDN) from your self-hosted integration runtime key, in the format `{datafactory}.{region}.datafactory.azure.net`.<br />For an existing data factory, if you don't see the FQDN in your self-hosted integration key, use `*.frontend.clouddatahub.net` instead. |
  | `download.microsoft.com` | 443 | Required by the self-hosted integration runtime for downloading the updates. If you have disabled auto-update, you can skip configuring this domain. |
  | `*.core.windows.net` | 443 | Used by the self-hosted integration runtime that connects to the Azure storage account to upload database backups from your network share |

  > [!TIP]  
  > If your database backup files are already provided in an Azure storage account, a self-hosted integration runtime isn't required during the migration process.

- If you use a self-hosted integration runtime, make sure that the computer on which the runtime is installed can connect to the source SQL Server instance and the network file share where backup files are located.

- Enable outbound port 445 to allow access to the network file share. For more information, see [Recommendations for using a self-hosted integration runtime](../migration-using-azure-data-studio.md#recommendations-for-using-a-self-hosted-integration-runtime-for-database-migrations).

- If you're using Azure Database Migration Service for the first time, make sure that the Microsoft.DataMigration [resource provider is registered in your subscription](../quickstart-create-data-migration-service-portal.md#register-the-resource-provider).
