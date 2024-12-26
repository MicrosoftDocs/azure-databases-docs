---
title: "Known issues, limitations, and troubleshooting"
titleSuffix: Azure Database Migration Service
description: Known issues, limitations, and troubleshooting guide for Azure SQL Migration extension for Azure Data Studio
author: abhims14
ms.author: abhishekum
ms.reviewer: maghan, randolphwest
ms.date: 09/18/2024
ms.service: azure-database-migration-service
ms.topic: troubleshooting
ms.collection:
  - sql-migration-content
---

# Known issues, limitations, and troubleshooting

This article provides a list of known issues and troubleshooting steps associated with the Azure SQL Migration extension for Azure Data Studio.

> [!IMPORTANT]  
> The latest version of Integration Runtime (5.28.8488) prevents access to a network file share on a local host. This security measure will lead to failures when performing migrations to Azure SQL using DMS. Please ensure you run Integration Runtime on a different machine than the network share hosting.

## Error code: 2007 - CutoverFailedOrCancelled

- **Message**: `Cutover failed or cancelled for database <DatabaseName>. Error details: The restore plan is broken because firstLsn <First LSN> of log backup <URL of backup in Azure Storage container>' is not <= lastLsn <last LSN> of Full backup <URL of backup in Azure Storage container>'. Restore to point in time.`

- **Cause**: The error can occur due to the backups being placed incorrectly in the Azure Storage container. If the backups are placed in the network file share, this error could also occur due to network connectivity issues.

- **Recommendation**: Ensure the database backups in your Azure Storage container are correct. If you're using network file share, there can be network-related issues and lags that are causing this error. Wait for the process to be completed.

- **Message**: `Cutover failed or cancelled for database '{databaseName}'. Error details: 'errorCode: Ext_RestoreSettingsError, message: RestoreId: {RestoreId}, OperationId: {operationId}, Detail: Failed to complete restore., RestoreJobState: Restoring, CompleteRestoreErrorMessage: The database contains incompatible physical layout. Too many full text catalog files.`

- **Cause**: SQL VM restore currently doesn't support restoring databases with full text catalog files as Azure SQL Vm doesn't support them at the moment.

- **Recommendation**: Remove full text catalog files from database when creating the restore

- **Message**: `Cutover failed or cancelled for database '{databaseName}'. Error details: 'Migration cannot be completed because provided backup file name '{providedFileName}' should be the last restore backup file '{lastRestoredFileName}'.'`

- **Cause**: This error occurs due to a known limitation in SqlMi. It means the '{providedFileName}' is different from '{lastRestoredFileName}'. SqlMi will automatically restore all valid backup files in the container based on the LSN sequence. A typical failure case could be: the '{providedFileName}' is "log1", but the files in container has other files, like "log2", which have largest LSN number than "log1". In this case, SqlMi will automatically restore all files in the container. In the end of completing the migration, SqlMi will report this error message.

- **Recommendation**: For offline migration mode, please provide the "lastBackupName" with the largest LSN. For online migration scenario this warning/error can be ignored if the migration status is succeeded.

## Error code: 2009 - MigrationRestoreFailed

- **Message**: `Migration for Database 'DatabaseName' failed with error cannot find server certificate with thumbprint.`

- **Cause**: Before migrating data, you need to migrate the certificate of the source SQL Server instance from a database that is protected by Transparent Data Encryption (TDE) to the target Azure SQL Managed Instance or SQL Server on Azure Virtual Machine.

- **Recommendation**: Migrate the TDE certificate to the target instance and retry the process. For more information about migrating TDE-enabled databases, see [Tutorial: Migrate TDE-enabled databases (preview) to Azure SQL in Azure Data Studio](tutorial-transparent-data-encryption-migration-ads.md).

- **Message**: `Migration for Database <DatabaseName> failed with error 'Non retriable error occurred while restoring backup with index 1 - 3169 The database was backed up on a server running version %ls. That version is incompatible with this server, which is running version %ls. Either restore the database on a server that supports the backup, or use a backup that is compatible with this server.`

- **Cause**: Unable to restore a SQL Server backup to an earlier version of SQL Server than the version at which the backup was created.

- **Recommendation**: See [Issues that affect database restoration between different SQL Server versions](/support/sql/admin/backup-restore-operations) for troubleshooting steps.

- **Message**: `Migration for Database <DatabaseName> failed with error 'The managed instance has reached its storage limit. The storage usage for the managed instance can't exceed 32768 MBs.`

- **Cause**: The Azure SQL Managed Instance has reached its resource limits.

- **Recommendation**: For more information about storage limits, see [Overview of Azure SQL Managed Instance resource limits](/azure/azure-sql/managed-instance/resource-limits).

- **Message**: `Migration for Database <DatabaseName> failed with error 'Non retriable error occurred while restoring backup with index 1 - 3634 The operating system returned the error '1450(Insufficient system resources exist to complete the requested service.)`

- **Cause**: One of the symptoms listed in [OS errors 1450 and 665 are reported for database files during DBCC CHECKDB or Database Snapshot Creation](/support/sql/admin/1450-and-665-errors-running-dbcc-checkdb#symptoms) can be the cause.

- **Recommendation**: See [OS errors 1450 and 665 are reported for database files during DBCC CHECKDB or Database Snapshot Creation](/support/sql/admin/1450-and-665-errors-running-dbcc-checkdb#symptoms) for troubleshooting steps.

- **Message**: `The restore plan is broken because firstLsn <First LSN> of log backup <URL of backup in Azure Storage container>' isn't <= lastLsn <last LSN> of Full backup <URL of backup in Azure Storage container>'. Restore to point in time.`

- **Cause**: The error can occur due to the backups being placed incorrectly in the Azure Storage container. If the backups are placed in the network file share, this error could also occur due to network connectivity issues.

- **Recommendation**: Ensure the database backups in your Azure Storage container are correct. If you're using network file share, there can be network related issues and lags that are causing this error. Wait for the process to complete.

- **Message**: `Migration for Database <Database Name> failed with error 'Non retriable error occurred while restoring backup with index 1 - 3234 Logical file <Name> isn't part of database <Database GUID>. Use RESTORE FILELISTONLY to list the logical file names. RESTORE DATABASE is terminating abnormally.'.`

- **Cause**: You've specified a logical file name that isn't in the database backup. Another potential cause of this error is an incorrect storage account container name.

- **Recommendation**: Run RESTORE FILELISTONLY to check the logical file names in your backup. For more information about RESTORE FILELISTONLY, see [RESTORE Statements - FILELISTONLY (Transact-SQL)](/sql/t-sql/statements/restore-statements-filelistonly-transact-sql).

- **Message**: `Migration for Database <Database Name> failed with error 'Azure SQL target resource failed to connect to storage account. Make sure the target SQL VNet is allowed under the Azure Storage firewall rules.'`

- **Cause**: Azure Storage firewall isn't configured to allow access to Azure SQL target.

- **Recommendation**: For more information about Azure Storage firewall setup, see [Configure Azure Storage firewalls and virtual networks](/azure/storage/common/storage-network-security).

- **Message**: `Migration for Database <Database Name> failed with error 'There are backups from multiple databases in the container folder. Please make sure the container folder has backups from a single database.`

- **Cause**: Backups of multiple databases are in the same container folder.

- **Recommendation**: If migrating multiple databases to **Azure SQL Managed Instance** using the same Azure Blob Storage container, you must place backup files for different databases in separate folders inside the container. For more information about LRS, see [Migrate databases from SQL Server to SQL Managed Instance by using Log Replay Service (Preview)](/azure/azure-sql/managed-instance/log-replay-service-migrate#limitations).

- **Message**: `Migration for Database <Database Name> failed with error 'Non retriable error occurred while restoring backup with index 1 - 12824 The sp_configure value 'contained database authentication' must be set to 1 in order to restore a contained database.  You may need to use RECONFIGURE to set the value_in_use. RESTORE DATABASE is terminating abnormally.`

- **Cause**: The source database is a contained database. A specific configuration is needed to enable restoring a contained database. For more information about contained databases, see [Contained Database Users](/sql/relational-databases/security/contained-database-users-making-your-database-portable).

- **Recommendation**: Run the following query connected to the source SQL Server in the context of the specific database before starting the migration. Then, attempt the migration of the contained database again.

  ```sql
  -- Enable "contained database authentication"
  EXECUTE sp_configure 'contained', 1;

  RECONFIGURE;
  ```

  > [!NOTE]  
  > For more information on general troubleshooting steps for Azure SQL Managed Instance errors, see [Known issues with Azure SQL Managed Instance](/azure/azure-sql/managed-instance/doc-changes-updates-known-issues)

## Error code: 2012 - TestConnectionFailed

- **Message**: `Failed to test connections using provided Integration Runtime. Error details: 'Remote name could not be resolved.'`

- **Cause**: Your network settings in the firewall are causing the Self-Hosted Integration Runtime to be unable to connect to the service back end.

- **Recommendation**: There's a Domain Name System (DNS) issue. Contact your network team to fix the issue. For more information, see [Troubleshoot Self-Hosted Integration Runtime](/azure/data-factory/self-hosted-integration-runtime-troubleshoot-guide).

- **Message**: `Failed to test connections using provided Integration Runtime. 'Cannot connect to <File share>. Detail Message: The system could not find the environment option that was entered`

- **Cause**: The Self-Hosted Integration Runtime can't connect to the network file share where the database backups are placed.

- **Recommendation**: Make sure your network file share name is entered correctly.

- **Message**: `Failed to test connections using provided Integration Runtime. The file name does not conform to the naming rules by the data store. Illegal characters in path.`

- **Cause**: The Self-Hosted Integration Runtime can't connect to the network file share where the database backups are placed.

- **Recommendation**: Make sure your network file share name is entered correctly.

- **Message**: `Failed to test connections using provided Integration Runtime.`

- **Cause**: Connection to the Self-Hosted Integration Runtime has failed.

- **Recommendation**: See [Troubleshoot Self-Hosted Integration Runtime](/azure/data-factory/self-hosted-integration-runtime-troubleshoot-guide) for general troubleshooting steps for Integration Runtime connectivity errors.

## Error code: 2014 - IntegrationRuntimeIsNotOnline

- **Message**: `Integration Runtime <IR Name> in resource group <Resource Group Name> Subscription <SubscriptionID> isn't online.`

- **Cause**: The Self-Hosted Integration Runtime isn't online.

- **Recommendation**: Make sure the Self-hosted Integration Runtime is registered and online. To perform the registration, you can use scripts from [Automating self-hosted integration runtime installation using local PowerShell scripts](/azure/data-factory/self-hosted-integration-runtime-automation-scripts). Also, see [Troubleshoot self-hosted integration runtime](/azure/data-factory/self-hosted-integration-runtime-troubleshoot-guide) for general troubleshooting steps for Integration Runtime connectivity errors.

## Error code: 2030 - AzureSQLManagedInstanceNotReady

- **Message**: `Azure SQL Managed Instance <Instance Name> isn't ready.`

- **Cause**: Azure SQL Managed Instance not in ready state.

- **Recommendation**: Wait until the Azure SQL Managed Instance has finished deploying and is ready, then retry the process.

## Error code: 2033 - SqlDataCopyFailed

- **Message**: `Migration for Database <Database> failed in state <state>.`

- **Cause**: ADF pipeline for data movement failed.

- **Recommendation**: Check the MigrationStatusDetails page for more detailed error information.

## Error code: 2038 - MigrationCompletedDuringCancel

- **Message**: `Migration cannot be canceled as Migration was completed during the cancel process. Target server: <Target server> Target database: <Target database>.`

- **Cause**: A cancellation request was received, but the migration was completed successfully before the cancellation was completed.

- **Recommendation**: No action required. Migration succeeded.

## Error code: 2039 - MigrationRetryNotAllowed

- **Message**: `Migration isn't in a retriable state. Migration must be in state WaitForRetry. Current state: <State>, Target server: <Target Server>, Target database: <Target database>.`

- **Cause**: A retry request was received when the migration wasn't in a state allowing retrying.

- **Recommendation**: No action required. Migration is ongoing or completed.

## Error code: 2040 - MigrationTimeoutWaitingForRetry

- **Message**: `Migration retry timeout limit of 8 hours reached. Target server: <Target Server>, Target database: <Target Database>.`

- **Cause**: Migration was idle in a failed, but retrievable state for 8 hours and was automatically canceled.

- **Recommendation**: No action is required; the migration was canceled.

## Error code: 2041 - DataCopyCompletedDuringCancel

- **Message**: `Data copy finished successfully before canceling completed. Target schema is in bad state. Target server: <Target Server>, Target database: <Target Database>.`

- **Cause**: Cancel request was received, and the data copy was completed successfully, but the target database schema hasn't been returned to its original state.

- **Recommendation**: If desired, the target database can be returned to its original state by running the first query and all of the returned queries, then running the second query and doing the same.

  ```sql
  SELECT [ROLLBACK]
  FROM [dbo].[__migration_status]
  WHERE STEP IN (3, 4, 6);

  SELECT [ROLLBACK]
  FROM [dbo].[__migration_status]
  WHERE STEP IN (5, 7, 8)
  ORDER BY STEP DESC;
  ```

## Error code: 2042 - PreCopyStepsCompletedDuringCancel

- **Message**: `Pre Copy steps finished successfully before canceling completed. Target database Foreign keys and temporal tables have been altered. Schema migration may be required again for future migrations. Target server: <Target Server>, Target database: <Target Database>.`

- **Cause**: Cancel request was received and the steps to prepare the target database for copy were completed successfully. The target database schema hasn't been returned to its original state.

- **Recommendation**: If desired, target database can be returned to its original state by running the following query and all of the returned queries.

  ```sql
  SELECT [ROLLBACK]
  FROM [dbo].[__migration_status]
  WHERE STEP IN (3, 4, 6);
  ```

## Error code: 2043 - CreateContainerFailed

- **Message**: `Create container <ContainerName> failed with error Error calling the endpoint '<URL>'. Response status code: 'NA - Unknown'. More details: Exception message: 'NA - Unknown [ClientSideException] Invalid Url:<URL>.`

- **Cause**: The request failed due to an underlying issue such as network connectivity, a DNS failure, a server certificate validation, or a timeout.

- **Recommendation**: For more troubleshooting steps, see [Troubleshoot Azure Data Factory and Synapse pipelines](/azure/data-factory/data-factory-troubleshoot-guide#error-code-2108).

## Error code: 2049 - FileShareTestConnectionFailed

- **Message**: `The value of the property '' is invalid: 'Access to <share path> is denied, resolved IP address is <IP address>, network type is OnPremise'.`

- **Cause**: The network share where the database backups are stored is in the same machine as the self-hosted Integration Runtime (SHIR).

- **Recommendation**: The latest version of Integration Runtime (**5.28.8488**) prevents access to a network file share on a local host. Ensure you run Integration Runtime on a different machine than the network share hosting. If hosting the self-hosted Integration Runtime and the network share on different machines isn't possible with your current migration setup, you can use the option to opt out using `DisableLocalFolderPathValidation`.

  > [!NOTE]  
  > For more information, see [Set up an existing self-hosted IR via local PowerShell](/azure/data-factory/create-self-hosted-integration-runtime#set-up-an-existing-self-hosted-ir-via-local-powershell). Use the disabling option with discretion as this is less secure.

## Error code: 2055 - SqlInfoCollectionFailed

- **Message**: `A database operation failed with the following error: 'VIEW SERVER PERFORMANCE STATE permission was denied on object 'server', database 'master'. The user does not have permission to perform this action.`

- **Cause**: The login used for target server(Azure SQL DB) doesn't has ##MS_ServerStateReader## server role.

- **Recommendation**: Provide ##MS_ServerStateReader## role to the login for Azure SQL Target.
Query:
ALTER SERVER ROLE ##MS_ServerStateReader## ADD MEMBER login.

Note: This query should be run in context of master DB

## Error code: 2056 - SqlInfoValidationFailed

- **Message**: `CollationMismatch: Source database collation <CollationOptionSource> is not the same as the target database <CollationOptionTarget>. Source database: <SourceDatabaseName> Target database: <TargetDatabaseName>.`

- **Cause**: The source database collation isn't the same as the target database's collation.

- **Recommendation**: Make sure to change the target Azure SQL Database collation to the same as the source SQL Server database. Azure SQL Database uses `SQL_Latin1_General_CP1_CI_AS` collation by default, in case your source SQL Server database uses a different collation you might need to re-create or select a different target database whose collation matches. For more information, see [Collation and Unicode support](/sql/relational-databases/collations/collation-and-unicode-support)

- **Message**: `TableColumnCollationMismatch: Table <Tablename> with column <columnname> has collation <collationoptionsource> on source but has collation <collationoptiontarget> on target table.`

- **Cause**: The source database table column's collation isn't the same as the target database table column's collation.

- **Recommendation**:

  1. Make sure to migrate the Schema to target Azure SQL Database using Database Migration Service. Refer [blog](https://techcommunity.microsoft.com/t5/microsoft-data-migration-blog/public-preview-schema-migration-for-target-azure-sql-db/ba-p/3990463).

  1. Follow this [article](/sql/relational-databases/collations/set-or-change-the-column-collation) to manually change collation.

  For more information, see [Collation and Unicode support](/sql/relational-databases/collations/collation-and-unicode-support)

- **Message**: `DatabaseSizeMoreThanMax: No tables were found in the target Azure SQL Database. Check if schema migration was completed beforehand.`

- **Cause**: The selected tables for the migration don't exist in the target Azure SQL Database.

- **Recommendation**: Make sure the target database schema was created before starting the migration. For more information on how to deploy the target database schema, see [SQL Database Projects extension](/azure-data-studio/extensions/sql-database-project-extension)

- **Message**: `DatabaseSizeMoreThanMax: The source database size <Source Database Size> exceeds the maximum allowed size of the target database <Target Database Size>. Check if the target database has enough space.`

- **Cause**: The target database doesn't have enough space.

- **Recommendation**: Make sure the target database schema was created before starting the migration. For more information on how to deploy the target database schema, see [SQL Database Projects extension](/azure-data-studio/extensions/sql-database-project-extension).

- **Message**: `NoTablesFound: Some of the source tables don't exist in the target database. Missing tables: <TableList>`.

- **Cause**: The selected tables for the migration don't exist in the target Azure SQL Database.

- **Recommendation**: Check if the selected tables exist in the target Azure SQL Database. If this migration is called from a PowerShell script, check if the table list parameter includes the correct table names and is passed into the migration.

- **Message**: `SqlVersionOutOfRange: Source instance version is lower than 2008, which is not supported to migrate. Source instance: <InstanceName>`.

- **Cause**: Azure Database Migration Service doesn't support migrating from SQL Server instances lower than 2008.

- **Recommendation**: Upgrade your source SQL Server instance to a newer version of SQL Server. For more information, see [Upgrade SQL Server](/sql/database-engine/install-windows/upgrade-sql-server).

- **Message**: `TableMappingMismatch: Some of the source tables don't exist in the target database. Missing tables: <TableList>`.

- **Cause**: The selected tables for the migration don't exist in the target Azure SQL Database.

- **Recommendation**: Check if the selected tables exist in the target Azure SQL Database. If this migration is called from a PowerShell script, check if the table list parameter includes the correct table names and is passed into the migration.

## Error code: 2060 - SqlSchemaCopyFailed

- **Message**: `The SELECT permission was denied on the object 'sql_logins', database 'master', schema 'sys'.`

- **Cause**: The account customers use to connect Azure SQL Database lacks the permission to access `sys.sql_logins` table.

- **Recommendation**: There are two ways to mitigate the issue:

  1. Add 'sysadmin' role to the account, which grants the admin permission.

  1. If customers can't use sysadmin account or can't grant sysadmin permission to the account, then minimum permission on source SQL Server required is "db_owner" and on target Azure SQL DB create a user in master and grant **##MS_DatabaseManager##**,**##MS_DatabaseConnector##**, **##MS_DefinitionReader##** and **##MS_LoginManager##** fixed server roles to the user. For example,

     ```sql
     -- Run the script in the master database
     CREATE LOGIN testuser WITH PASSWORD = '*********';

     ALTER SERVER ROLE ##MS_DefinitionReader## ADD MEMBER [testuser];
     GO

     ALTER SERVER ROLE ##MS_DatabaseConnector## ADD MEMBER [testuser];
     GO

     ALTER SERVER ROLE ##MS_DatabaseManager## ADD MEMBER [testuser];
     GO

     ALTER SERVER ROLE ##MS_LoginManager## ADD MEMBER [testuser];
     GO

     CREATE USER testuser FOR LOGIN testuser;
     EXECUTE sp_addRoleMember 'dbmanager', 'testuser';
     EXECUTE sp_addRoleMember 'loginmanager', 'testuser';
     ```

- **Message**: `Failed to get service token from ADF service.`

- **Cause**: The customer's SHIR fails to connect data factory.

- **Recommendation**: This is sample doc how to solve it: [Integration runtime Unable to connect to Data Factory](/answers/questions/139976/integration-runtime-unable-to-connect-to-data-fact)

- **Message**: `IR Nodes are offline.`

- **Cause**: The cause might be that the network is interrupted during migration and thus the IR node become offline. Make sure that the machine where SHIR is installed is on.

- **Recommendation**: Make sure that the machine where SHIR is installed is on.

- **Message**: `Deployed failure: {0}. Object element: {1}.`

- **Cause**: This is the most common error customers might encounter. It means that the object can't be deployed to the target because it's unsupported on the target.

- **Recommendation**: Customers need to check the assessment results ([Assessment rules](/azure/azure-sql/migration-guides/database/sql-server-to-sql-database-assessment-rules)). This is the list of assessment issues that might fail the schema migration:

  - [BULK INSERT](/azure/azure-sql/migration-guides/database/sql-server-to-sql-database-assessment-rules#BulkInsert)
  - [COMPUTE clause](/azure/azure-sql/migration-guides/database/sql-server-to-sql-database-assessment-rules#ComputeClause)
  - [Cryptographic provider](/azure/azure-sql/migration-guides/database/sql-server-to-sql-database-assessment-rules#CryptographicProvider)
  - [Cross database references](/azure/azure-sql/migration-guides/database/sql-server-to-sql-database-assessment-rules#CrossDatabaseReferences)
  - [Database principal alias](/azure/azure-sql/migration-guides/database/sql-server-to-sql-database-assessment-rules#DatabasePrincipalAlias)
  - [DISABLE_DEF_CNST_CHK option](/azure/azure-sql/migration-guides/database/sql-server-to-sql-database-assessment-rules#DisableDefCNSTCHK)
  - [FASTFIRSTROW hint](/azure/azure-sql/migration-guides/database/sql-server-to-sql-database-assessment-rules#FastFirstRowHint)
  - [FILESTREAM](/azure/azure-sql/migration-guides/database/sql-server-to-sql-database-assessment-rules#FileStream)
  - [MS DTC](/azure/azure-sql/migration-guides/database/sql-server-to-sql-database-assessment-rules#MSDTCTransactSQL)
  - [OPENROWSET (bulk)](/azure/azure-sql/migration-guides/database/sql-server-to-sql-database-assessment-rules#OpenRowsetWithNonBlobDataSourceBulk)
  - [OPENROWSET (provider)](/azure/azure-sql/migration-guides/database/sql-server-to-sql-database-assessment-rules#OpenRowsetWithSQLAndNonSQLProvider)

  > [!NOTE]  
  > To view error detail, Open the Microsoft Integration runtime configuration manager, and navigate to **Diagnostics > Logging > View logs**. In the Event viewer, navigate to **Application and Service logs > Connectors - Integration runtime**, and filter for errors.

- **Message**: `Deployed failure: Index cannot be created on computed column '{0}' of table '{1}' because the underlying object '{2}' has a different owner. Object element: {3}.`

  Sample Generated Script: `IF NOT EXISTS (SELECT * FROM sys.indexes WHERE object_id = OBJECT_ID(N'[Sales].[Customer]') AND name = N'AK_Customer_AccountNumber') CREATE UNIQUE NONCLUSTERED INDEX [AK_Customer_AccountNumber] ON [Sales].[Customer] ( [AccountNumber] ASC )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)`

- **Cause**: All function references in the computed column must have the same owner as the table.

- **Recommendation**: See [Ownership Requirements](/sql/relational-databases/indexes/indexes-on-computed-columns#ownership-requirements).

## Error code: Ext_RestoreSettingsError

- **Message**: `Unable to read blobs in storage container, exception: The remote server returned an error: (403) Forbidden.; The remote server returned an error: (403) Forbidden`

- **Cause**: The Azure SQL target is unable to connect to blob storage.

- **Recommendation**: Confirm that target network settings allow access to blob storage. For example, if you're migrating to a SQL Server on Azure VM target, ensure that outbound connections on the Virtual Machine aren't being blocked.

- **Message**: `Failed to create restore job. Unable to read blobs in storage container, exception: The remote name could not be resolved.`

- **Cause**: The Azure SQL target is unable to connect to blob storage.

- **Recommendation**: Confirm that target network settings allow access to blob storage. For example, if migrating to SQL VM, ensure that outbound connections on VM aren't being blocked.

- **Message**: `Migration for Database <Database Name> failed with error 'Migration cannot be completed because provided backup file name <Backup File Name> should be the last restore backup file <Last Restore Backup File Name>'`.

- **Cause**: The most recent backup wasn't specified in the backup settings.

- **Recommendation**: Specify the most recent backup file name in backup settings and retry the operation.

- **Message**: `Operation failed: errorCode: Ext_RestoreSettingsError, message: RestoreId: 1111111-aaaa-bbbb-cccc-dddddddd, OperationId: 2222222-aaaa-bbbb-cccc-dddddddd, Detail: Unable to read blobs in storage container, exception: Unable to connect to the remote server;Unable to connect to the remote server;A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond 11.111.11.111:443.`

- **Cause**: The error is possible to occur for both storage accounts with public network and private endpoint configuration. It's also possible that you have an on-premises DNS server that controls a hybrid network routing and DHCP. Unless you allow the Azure IP addresses configured in your DNS server, your SQL Server on Azure VM target has no chance to resolve the remote storage blob endpoint.

- **Recommendation**: To debug this issue, you can try pinging your Azure Blob Storage URL from your SQL Server on Azure VM target and confirm if you have a connectivity problem. To solve this issue, you have to allow the Azure IP addresses configured in your DNS server. For more information, see [Troubleshoot Azure Private Endpoint connectivity problems](/azure/private-link/troubleshoot-private-endpoint-connectivity)

## Error code: No such host is known OR urlopen error [Errno 11001] getaddrinfo failed

- **Message**: `No such host is known`

- **Cause**: While migrating logins using PowerShell command [New-AzDataMigrationLoginsMigration](/powershell/module/az.datamigration/new-azdatamigrationloginsmigration), it fails with the previous message.

- **Recommendation**: To resolve this issue, upgrade the Microsoft Azure PowerShell - Database Migration Service cmdlets - Az.DataMigration above minimum 0.14.5 version.

  Latest version of Az.Datamigration can be downloaded from [the PowerShell gallery](https://www.powershellgallery.com/packages/Az.DataMigration/0.14.7) or the following command can be used to upgrade.

```powershell
 Update-Module -Name Az.DataMigration
```
- **Message**: `urlopen error [Errno 11001] getaddrinfo failed`

- **Cause**: While migrating logins using Azure CLI [Az dataMigration login-migration](/cli/azure/datamigration), it fails with the previous message.

- **Recommendation**: To resolve this issue, upgrade the Microsoft Azure CLI - Database Migration Service extension - az dataMigration to 1.0.0b1 or a later version. Run the following command to upgrade.

```azurecli
 az extension update -n datamigration
```

## Azure Database Migration Service Naming Rules

If your DMS service failed with "Error: Service name 'x_y_z' is not valid", then you need to follow the Azure Database Migration Service Naming Rules. As Azure Database Migration Service uses Azure Data factory for its compute, it follows the exact same naming rules as mentioned in the [naming rules](/azure/data-factory/naming-rules).

## Azure SQL Database limitations

Migrating to Azure SQL Database by using the Azure SQL extension for Azure Data Studio has the following limitations:

[!INCLUDE [sql-db-limitations](includes/sql-database-limitations.md)]

## Azure SQL Managed Instance limitations

Migrating to Azure SQL Managed Instance by using the Azure SQL extension for Azure Data Studio has the following limitations:

[!INCLUDE [sql-mi-limitations](includes/sql-managed-instance-limitations.md)]

## SQL Server on Azure VMs limitations

Migrating to SQL Server on Azure VMs by using the Azure SQL extension for Azure Data Studio has the following limitations:

[!INCLUDE [sql-vm-limitations](includes/sql-virtual-machines-limitations.md)]

## Azure Data Studio limitations

### Failed to start Sql Migration Service: Error: Request error

- **Message**: `Error at ClientRequest.<anonymous> (c:\Users\MyUser\.azuredatastudio\extensions\microsoft.sql-migration-1.4.2\dist\main.js:2:7448) at ClientRequest.emit (node:events:538:35) at TLSSocket.socketOnEnd (node:_http_client:466:9) at TLSSocket.emit (node:events:538:35) at endReadableNT (node:internal/streams/readable:1345:12) at process.processTicksAndRejections (node:internal/process/task_queues:83:21)`

- **Cause**: This issue occurs when Azure Data Studio isn't able to download the MigrationService package from https://github.com/microsoft/sqltoolsservice/releases. The download failure can be due to disconnected network work or unresolved proxy settings.

- **Recommendation**: The sure fire way of solving this issue is by downloading the package manually. Follow the mitigation steps outlined in this link: https://github.com/microsoft/azuredatastudio/issues/22558#issuecomment-1496307891

## Related content

- [Azure SQL migration extension for Azure Data Studio](/azure-data-studio/extensions/azure-sql-migration-extension)
- [Migrate databases from SQL Server to SQL Managed Instance by using Log Replay Service (Preview)](/azure/azure-sql/managed-instance/log-replay-service-migrate#limitations)
- [Checklist: Best practices for SQL Server on Azure VMs](/azure/azure-sql/virtual-machines/windows/performance-guidelines-best-practices-checklist)
