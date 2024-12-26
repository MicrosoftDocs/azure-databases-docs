---
title: "Common issues - Azure Database Migration Service"
description: Learn about how to troubleshoot common known issues/errors associated with using Azure Database Migration Service(classic).
author: abhims14
ms.author: abhishekum
ms.reviewer: randolphwest
ms.date: 09/18/2024
ms.service: azure-database-migration-service
ms.topic: troubleshooting
ms.collection:
  - sql-migration-content
ms.custom:
  - has-azure-ad-ps-ref
---

# Troubleshoot common Azure Database Migration Service (classic) issues and errors

This article describes some common issues and errors that Azure Database Migration Service(classic) users can come across. The article also includes information about how to resolve these issues and errors.

## Migration activity in queued state

**Error:** When you create new activities in an Azure Database Migration Service project, the activities remain in a queued state.

**Cause:** This issue happens when the Azure Database Migration Service instance has reached maximum capacity for ongoing tasks that concurrently run. Any new activity is queued until the capacity becomes available.

**Resolution:** Validate the Data Migration Service instance has running activities across projects. You can continue to create new activities that automatically get added to the queue for execution. As soon as any of the existing running activities complete, the next queued activity starts running and the status changes to running state automatically. You don't need to take any further action to start migration of queued activity.

## Max number of databases selected for migration

The following error occurs when creating an activity for a database migration project for moving to Azure SQL Database or an Azure SQL Managed Instance:

**Error**: Migration settings validation error", "errorDetail":"More than max number '4' objects of 'Databases' has been selected for migration."

**Cause:** This error displays when you've selected more than four databases for a single migration activity. Currently, each migration activity is limited to four databases.

**Resolution:** Select four or fewer databases per migration activity. If you need to migrate more than four databases in parallel, provision another instance of Azure Database Migration Service. Currently, each subscription supports up to two Azure Database Migration Service instances.

## Error when attempting to stop Azure Database Migration Service

You receive following error when stopping the Azure Database Migration Service instance:

**Error**: Service failed to Stop. Error: {'error':{'code':'InvalidRequest','message':'One or more activities are currently running. To stop the service, wait until the activities have completed or stop those activities manually and try again.'}}

**Cause:** This error displays when the service instance you're attempting to stop includes activities that are still running or present in migration projects.

**Resolution:** Ensure that there are no activities running in the instance of Azure Database Migration Service you're trying to stop. You might also delete the activities or projects before attempting to stop the service.

The following steps illustrate how to remove projects to clean up the migration service instance by deleting all running tasks:

1. `Install-Module -Name AzureRM.DataMigration`
1. `Login-AzureRmAccount`
1. `Select-AzureRmSubscription -SubscriptionName <subName>`
1. `Remove-AzureRmDataMigrationProject -Name <projectName> -ResourceGroupName <rgName> -ServiceName <serviceName> -DeleteRunningTask`

## Error when attempting to start Azure Database Migration Service

You receive following error when starting the Azure Database Migration Service instance:

**Error**: Service fails to Start. Error: {'errorDetail':'The service failed to start, please contact Microsoft support'}

**Cause:** This error displays when the previous instance failed internally. This error occurs rarely, and the engineering team is aware of it.

**Resolution:** Delete the instance of the service that you can't start, and then provision new one to replace it.

## Error restoring database while migrating SQL to Azure SQL DB managed instance

When you perform an online migration from SQL Server to Azure SQL Managed Instance, the cutover fails with following error:

**Error**: Restore Operation failed for operation Id 'operationId'. Code 'AuthorizationFailed', Message 'The client 'clientId' with object id 'objectId' does not have authorization to perform action 'Microsoft.Sql/locations/managedDatabaseRestoreAzureAsyncOperation/read' over scope '/subscriptions/subscriptionId'.

**Cause:** This error indicates the application principal being used for online migration from SQL Server to SQL Managed Instance doesn't have contribute permission on the subscription. Certain API calls with SQL Managed Instance currently require this permission on subscription for the restore operation.

**Resolution:** Use the `Get-AzureADServicePrincipal` PowerShell cmdlet with `-ObjectId` available from the error message to list the display name of the application ID being used.

Validate the permissions to this application and ensure it has the [contributor role](/azure/role-based-access-control/built-in-roles#contributor) at the subscription level.

The Azure Database Migration Service Engineering Team is working to restrict the required access from current contribute role on subscription. If you have a business requirement that doesn't allow use of contribute role, contact Azure support.

## Error when deleting NIC associated with Azure Database Migration Service

When you try to delete a Network Interface Card associated with Azure Database Migration Service, the deletion attempt fails with this error:

**Error**: Cannot delete the NIC associated to Azure Database Migration Service due to the DMS service utilizing the NIC

**Cause:** This issue happens when the Azure Database Migration Service instance might still be present and consuming the NIC.

**Resolution:** To delete this NIC, delete the DMS service instance that automatically deletes the NIC used by the service.

After all the projects and activities associated to the Azure Database Migration Service instance are deleted, you can delete the service instance. The NIC used by the service instance is automatically cleaned as part of service deletion.

> [!IMPORTANT]  
> Make sure the Azure Database Migration Service instance being deleted has no running activities.

## Connection error when using ExpressRoute

When you try to connect to source in the Azure Database Migration service project wizard, the connection fails after prolonged timeout if source is using ExpressRoute for connectivity.

**Cause:** When you use [ExpressRoute](https://azure.microsoft.com/services/expressroute/), Azure Database Migration Service [requires](tutorial-sql-server-to-azure-sql.md) provisioning three service endpoints on the Virtual Network subnet associated with the service:

- Service Bus endpoint
- Storage endpoint
- Target database endpoint (for example, SQL endpoint, Azure Cosmos DB endpoint)

**Resolution:** [Enable](tutorial-sql-server-to-azure-sql.md) the required service endpoints for ExpressRoute connectivity between source and Azure Database Migration Service. |

## Lock wait timeout error when migrating a MySQL database to Azure Database for MySQL

When you migrate a MySQL database to an Azure Database for MySQL instance via Azure Database Migration Service, the migration fails with following lock wait timeout error:

**Error**: Database migration error - Failed to load file - Failed to start load process for file 'n' RetCode: SQL_ERROR SqlState: HY000 NativeError: 1205 Message: [MySQL][ODBC Driver][mysqld] Lock wait timeout exceeded; try restarting transaction

**Cause:** This error occurs when migration fails because of the lock wait timeout during migration.

**Resolution:** Consider increasing the value of server parameter **'innodb_lock_wait_timeout'**. The highest allowed value is 1073741824.

## Error connecting to source SQL Server when using dynamic port or named instance

When you try to connect Azure Database Migration Service to SQL Server source that runs on either named instance or a dynamic port, the connection fails with this error:

**Error**: -1 - SQL connection failed. A network-related or instance-specific error occurred while establishing a connection to SQL Server. The server was not found or was not accessible. Verify that the instance name is correct and that SQL Server is configured to allow remote connections. (provider: SQL Network Interfaces, error: 26 - Error Locating Server/Instance Specified)

**Cause:** This issue happens when the source SQL Server instance that Azure Database Migration Service tries to connect to either has a dynamic port or is using a named instance. The SQL Server Browser service listens to UDP port 1434 for incoming connections to a named instance or when using a dynamic port. The dynamic port might change each time SQL Server service restarts. You can check the dynamic port assigned to an instance via network configuration in SQL Server Configuration Manager.

**Resolution:** Verify that Azure Database Migration Service can connect to the source SQL Server Browser service on UDP port 1434 and the SQL Server instance through the dynamically assigned TCP port as applicable.

## Additional known issues

- [Known issues/migration limitations with online migrations to Azure SQL Database](index.yml)
- [Known issues and limitations with online migrations from PostgreSQL to Azure Database for PostgreSQL](known-issues-azure-postgresql-online.md)

## Related content

- [Azure Database Migration Service PowerShell](/powershell/module/azurerm.datamigration#data_migration)
- [How to configure server parameters in Azure Database for MySQL by using the Azure portal](../mysql/howto-server-parameters.md)
- [Overview of prerequisites for using Azure Database Migration Service](pre-reqs.md)
- [FAQ about using Azure Database Migration Service](faq.yml)
