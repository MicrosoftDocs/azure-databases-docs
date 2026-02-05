---
title: Migrate Databases at Scale Using Azure PowerShell / CLI
description: Learn how to use Azure PowerShell or CLI to migrate databases at scale with Azure Database Migration Service.
author: rwestMSFT
ms.author: randolphwest
ms.reviewer: abhishekum
ms.date: 02/19/2026
ms.service: azure-database-migration-service
ms.topic: upgrade-and-migration-article
ms.collection:
  - sql-migration-content
ms.custom:
  - devx-track-azurepowershell
---

# Migrate databases at scale using automation

Azure Database Migration Service provides the following capabilities:

- A reliable, resilient, and fault-tolerant service that orchestrates data movement activities to provide a seamless migration experience.

- The ability to run online (for migrations requiring minimal downtime) or offline (for migrations where downtime persists through the migration) migration modes to suit your business requirements.

- The flexibility to create and configure a self-hosted integration runtime to provide your own compute for accessing the source SQL Server and backups in your on-premises environment.

With automation tools like the [PowerShell - Azure DataMigration Service Module](/powershell/module/az.datamigration) or [Azure CLI](/cli/azure/datamigration), you can migrate one or more databases at scale, including databases across multiple SQL Server instances.

The following sample scripts can be referenced to suit your migration scenario using Azure PowerShell or Azure CLI:

| Migration scenario | Scripting language |
| --- | --- |
| SQL Server assessment | [PowerShell](https://github.com/Azure-Samples/data-migration-sql/blob/main/PowerShell/sql-server-assessment.md) / [Azure CLI](https://github.com/Azure-Samples/data-migration-sql/blob/main/CLI/sql-server-assessment.md) |
| SQL Server to Azure SQL Managed Instance (using file share) | [PowerShell](https://github.com/Azure-Samples/data-migration-sql/blob/main//PowerShell/sql-server-to-sql-mi-fileshare.md) / [Azure CLI](https://github.com/Azure-Samples/data-migration-sql/blob/main/CLI/sql-server-to-sql-mi-fileshare.md) |
| SQL Server to Azure SQL Managed Instance (using Azure storage) | [PowerShell](https://github.com/Azure-Samples/data-migration-sql/blob/main//PowerShell/sql-server-to-sql-mi-blob.md) / [Azure CLI](https://github.com/Azure-Samples/data-migration-sql/blob/main/CLI/sql-server-to-sql-mi-blob.md) |
| SQL Server to SQL Server on Azure Virtual Machines (using file share) | [PowerShell](https://github.com/Azure-Samples/data-migration-sql/blob/main//PowerShell/sql-server-to-sql-vm-fileshare.md) / [Azure CLI](https://github.com/Azure-Samples/data-migration-sql/blob/main/CLI/sql-server-to-sql-vm-fileshare.md) |
| SQL Server to SQL Server on Azure Virtual Machines (using Azure Storage) | [PowerShell](https://github.com/Azure-Samples/data-migration-sql/blob/main//PowerShell/sql-server-to-sql-vm-blob.md) / [Azure CLI](https://github.com/Azure-Samples/data-migration-sql/blob/main/CLI/sql-server-to-sql-vm-blob.md) |
| SQL Server to Azure SQL Database | [PowerShell](https://github.com/Azure-Samples/data-migration-sql/blob/main//PowerShell/sql-server-to-sql-db.md) / [Azure CLI](https://github.com/Azure-Samples/data-migration-sql/blob/main/CLI/sql-server-to-sql-db.md) |
| SKU recommendations | [PowerShell](https://github.com/Azure-Samples/data-migration-sql/blob/main//PowerShell/sql-server-sku-recommendation.md) / [Azure CLI](https://github.com/Azure-Samples/data-migration-sql/blob/main/CLI/sql-server-sku-recommendation.md) |
| End-to-End migration automation | [PowerShell](https://github.com/Azure-Samples/data-migration-sql/blob/main//PowerShell/scripts/) / [Azure CLI](https://github.com/Azure-Samples/data-migration-sql/blob/main/CLI/scripts/) |
| End-to-End migration automation for multiple databases | [PowerShell](https://github.com/Azure-Samples/data-migration-sql/blob/main//PowerShell/scripts/multiple%20databases/) / [Azure CLI](https://github.com/Azure-Samples/data-migration-sql/blob/main/CLI/scripts/multiple%20databases/) |

## Prerequisites

Prerequisites that are common across all supported migration scenarios using Azure PowerShell or Azure CLI are:

- Have an Azure account that is assigned to one of the built-in roles listed as follows:

  - Contributor for the target Azure SQL Managed Instance, SQL Server on Azure Virtual Machines or Azure SQL Database and, Storage Account to upload your database backup files from SMB network share (*Not applicable for Azure SQL Database*).

  - Reader role for the Azure Resource Groups containing the target Azure SQL Managed Instance, SQL Server on Azure Virtual Machines or Azure SQL Database.

  - Owner or Contributor role for the Azure subscription.

  Azure account is only required when running the migration steps and isn't required for assessment or Azure recommendation steps process.

- Create a target [Azure SQL Managed Instance](/azure/azure-sql/managed-instance/create-configure-managed-instance-powershell-quickstart), [SQL Server on Azure Virtual Machine](/azure/azure-sql/virtual-machines/windows/sql-vm-create-powershell-quickstart), or [Azure SQL Database](/azure/azure-sql/database/single-database-create-quickstart).

  If your target is Azure SQL Database, you have to migrate database schema from source to target using the [Data-tier Application experience](/sql/tools/visual-studio-code-extensions/mssql/mssql-data-tier-application) or [SQL Database Projects extension](/sql/tools/visual-studio-code-extensions/sql-database-projects/sql-database-projects-extension) for Visual Studio Code.

  If you have an existing Azure Virtual Machine, it should be registered with the [SQL Server IaaS Agent Extension in Full management mode](/azure/azure-sql/virtual-machines/windows/sql-server-iaas-agent-extension-automate-management#management-modes).

- If your target is **Azure SQL Managed Instance** or **SQL Server on Azure Virtual Machine**, ensure that the logins used to connect the source SQL Server are members of the *sysadmin* server role or have `CONTROL SERVER` permission.

- If your target is **Azure SQL Database**, ensure that the login used to connect the source SQL Server is a member, and the `db_datareader` and login for the target SQL server is `db_owner`.

- Use one of the following storage options for the full database and transaction log backup files:

  - SMB network share

  - Azure storage account file share or blob container

    - If your database backup files are provided in an SMB network share, [Create an Azure storage account](/azure/storage/common/storage-account-create) that allows the DMS service to upload the database backup files. Make sure to create the Azure Storage Account in the same region as the Azure Database Migration Service instance is created.

    - Make sure the Azure storage account blob container is used exclusively to store backup files only. Any other file types (`.txt`, `.png`, `.jpg`, etc.) interfere with the restore process, leading to a failure.

    - Azure Database Migration Service doesn't initiate any backups, and instead uses existing backups, which you might already have as part of your disaster recovery plan, for the migration.

    - Each backup can be written to either a separate backup file or multiple backup files. However, appending multiple backups (that is, full and t-log) into a single backup media isn't supported.

    - Use compressed backups to reduce the likelihood of experiencing potential issues associated with migrating large backups.

- Ensure that the service account running the source SQL Server instance has read and write permissions on the SMB network share that contains database backup files.

- The source SQL Server instance certificate from a database protected by transparent data encryption (TDE) must be migrated to the target Azure SQL Managed Instance or SQL Server on Azure Virtual Machine before migrating data.

  > [!TIP]  
  > If your database contains sensitive data that is protected by [Always Encrypted](/sql/relational-databases/security/encryption/configure-always-encrypted-using-sql-server-management-studio), the migration process automatically migrates your Always Encrypted keys to your target Azure SQL Managed Instance or SQL Server on Azure Virtual Machine.

- If your database backups are in a network file share, provide a machine to install [self-hosted integration runtime](/azure/data-factory/create-self-hosted-integration-runtime) to access and migrate database backups. The Azure PowerShell or Azure CLI modules provide the authentication keys to register your self-hosted integration runtime. In preparation for the migration, ensure that the machine where you plan to install the self-hosted integration runtime has the following outbound firewall rules and domain names enabled:

  | Domain names | Outbound ports | Description |
  | --- | --- | --- |
  | Public Cloud: `{datafactory}.{region}.datafactory.azure.net`<br />or `*.frontend.clouddatahub.net`<br />Azure Government: `{datafactory}.{region}.datafactory.azure.us`<br />China: `{datafactory}.{region}.datafactory.azure.cn` | 443 | Required by the self-hosted integration runtime to connect to the Data Migration service.<br />For new created Data Factory in public cloud, locate the FQDN from your Self-hosted Integration Runtime key, which is in format `{datafactory}.{region}.datafactory.azure.net`. For old Data factory, if you don't see the FQDN in your Self-hosted Integration key, use *.frontend.clouddatahub.net instead. |
  | `download.microsoft.com` | 443 | Required by the self-hosted integration runtime for downloading the updates. If you disabled auto-update, you can skip configuring this domain. |
  | `*.core.windows.net` | 443 | Used by the self-hosted integration runtime that connects to the Azure storage account for uploading database backups from your network share |

  If your database backup files are already provided in an Azure storage account, self-hosted integration runtime isn't required during the migration process.

- When using self-hosted integration runtime, ensure that the machine where the runtime is installed can connect to the source SQL Server instance and the network file share where backup files are located.

- Outbound port 445 should be enabled to access the network file share.

- If you're using the Azure Database Migration Service for the first time, ensure that Microsoft.DataMigration resource provider is registered in your subscription. You can follow the steps to [register the resource provider](./quickstart-create-data-migration-service-portal.md#register-the-resource-provider)

  If your migration target is Azure SQL Database, you don't need backups to perform this migration. The migration to Azure SQL Database is considered a logical migration involving the database's precreation and data movement (performed by DMS).

## Automate database migrations

Using Azure PowerShell [Az.DataMigration](/powershell/module/az.datamigration) or Azure CLI [az datamigration](/cli/azure/datamigration), you can migrate databases by automating the creation of the Azure Database Migration Service, configuring database migrations for online migration, and performing a cutover. There are several more commands and functionality that are documented in [Azure Samples](https://github.com/Azure-Samples/data-migration-sql).

Examples of automating the migration of a SQL Server database using Azure CLI:

**Step 1: Create Azure Database Migration Service, which will orchestrate your database's migration activities.**

```azurepowershell-interactive
#STEP 1: Create Database Migration Service
az datamigration sql-service create --resource-group "myRG" --sql-migration-service-name "myMigrationService" --location "EastUS2"
```

**Step 2: Configure and start online database migration from SQL Server on-premises (with backups in Azure storage) to Azure SQL Managed Instance.**

```azurepowershell-interactive
#STEP 2: Start Migration
az datamigration sql-managed-instance create `
--source-location '{\"AzureBlob\":{\"storageAccountResourceId\":\"/subscriptions/mySubscriptionID/resourceGroups/myRG/providers/Microsoft.Storage/storageAccounts/dbbackupssqlbits\",\"accountKey\":\"myAccountKey\",\"blobContainerName\":\"dbbackups\"}}' `
--migration-service "/subscriptions/mySubscriptionID/resourceGroups/myRG/providers/Microsoft.DataMigration/SqlMigrationServices/myMigrationService" `
--scope "/subscriptions/mySubscriptionID/resourceGroups/myRG/providers/Microsoft.Sql/managedInstances/mySQLMI" `
--source-database-name "AdventureWorks2008" `
--source-sql-connection authentication="SqlAuthentication" data-source="mySQLServer" password="<password>" user-name="sqluser" `
--target-db-name "AdventureWorks2008" `
--resource-group myRG `
--managed-instance-name mySQLMI
```

**Step 3: Perform a migration cutover once all backups are restored to Azure SQL Managed Instance.**

```azurepowershell-interactive
#STEP 3: Get migration ID and perform Cutover
$migOpId = az datamigration sql-managed-instance show --managed-instance-name "mySQLMI" --resource-group "myRG" --target-db-name "AdventureWorks2008" --expand=MigrationStatusDetails --query "properties.migrationOperationId"
az datamigration sql-managed-instance cutover --managed-instance-name "mySQLMI" --resource-group "myRG" --target-db-name "AdventureWorks2008" --migration-operation-id $migOpId
```

If you receive the error `The subscription is not registered to use namespace 'Microsoft.DataMigration'. See https://aka.ms/rps-not-found for how to register subscriptions.`, run the following command:

```azurepowershell
Register-AzResourceProvider -ProviderNamespace "Microsoft.DataMigration"
```

## Related content

- [Az.DataMigration](/powershell/module/az.datamigration)
- [az datamigration](/cli/azure/datamigration)
- [data-migration-sql](https://github.com/Azure-Samples/data-migration-sql)
