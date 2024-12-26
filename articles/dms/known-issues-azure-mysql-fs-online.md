---
title: Known issues with migrations to Azure MySQL Database
description: Learn about known migration issues associated with migrations to Azure MySQL Database
author: karlaescobar
ms.author: karlaescobar
ms.reviewer: sanjaymi, randolphwest
ms.date: 09/18/2024
ms.service: azure-database-migration-service
ms.topic: troubleshooting
ms.collection:
  - sql-migration-content
ms.custom:
  - mvc
---

# Known Issues With Migrations To Azure Database for MySQL

Known issues associated with migrations to Azure Database for MySQL are described in the following sections.

## Schema Migration Issue for v8.0 MySQL Flexible Server target

- **Error**: A migration to a MySQL Flexible Server with engine version 8.0.30 or higher can fail when the feature to generate invisible primary keys for InnoDB tables is enabled (see [MySQL :: MySQL 8.0 Reference Manual :: 13.1.20.11 Generated Invisible Primary Keys](https://dev.mysql.com/doc/refman/8.0/en/create-table-gipks.html)). The failure might occur when migrating table schema from the source to the target, when applying changes during the replication phase of online migrations, when retrying a migration, or when migrating to a target where the schema has been migrated manually.

  **Potential error message**:

  - "Unknown error."
  - "Failed to generate invisible primary key. Auto-increment column already exists."
  - "The column 'my_row_id' in the target table 'table name' in database 'database' does not exist on the source table."

  **Limitation**: Migration to MySQL Flexible Server instance where sql_generate_invisible_primary_key is enabled isn't supported by DMS.

  **Workaround**: Set the server parameter sql_generate_invisible_primary_key for target MySQL Flexible Server to OFF. The server parameter can be found in the Server parameters pane under the All tab for the target MySQL Flexible Server. Additionally, drop the target database and start over the DMS migration to not have any mismatched schemas.

## Incompatible SQL Mode

One or more incompatible SQL modes can cause many different errors. Following is an example error along with server modes that should be looked at if this error occurs.

- **Error**: An error occurred while preparing the table '{table}' in database '{database}' on server '{server}' for migration during activity '{activity}'. As a result, this table will not be migrated.

  **Limitation**: This error occurs when one of the following SQL modes is set on one server but not the other server.

  **Workaround**:

  - NO_ZERO_DATE

    When the default value for a date on a table or the data is 0000-00-00 on the source, and the target server has the NO_ZERO_DATE SQL mode set, the schema and/or data migration fail. There are two possible workarounds. The first is to change the default values of the columns to be NULL or a valid date. The second option is to remove the NO_ZERO_DATE SQL mode from the global SQL mode variable.

  - NO_AUTO_CREATE_USER

    When running migrations from MySQL source server 5.7 to MySQL target server 8.0 that are doing **schema migration of routines**, it runs into errors if no_auto_create_user SQL mode is set on MySQL source server 5.7.

## Binlog Retention Issues

- **Error**: Fatal error reading binlog. This error can indicate that the binlog file name and/or the initial position were specified incorrectly.

  **Limitation**: This error occurs if binlog retention period is too short.

  **Workaround**: There are multiple variables that can be configured in this case: binlog_expire_logs_seconds determines the retention period and binlog deletion can be prevented altogether by setting binlog_expire_logs_auto_purge off. MySQL 5.7 has deprecated system variable expire_logs_days.

## Timeout Obtaining Table Locks

- **Error**: An exception occurred while attempting to acquire a read lock on the server '{server}' for consistent view creation.

  **Limitation**: This error occurs when there's a timeout while obtaining locks on all the tables when transactional consistency is enabled.

  **Workaround**: Ensure that the selected tables aren't locked or that no long running transactions are running on them.

## Write More Than 4 MB of Data to Azure Storage

- **Error**: The request body is too large and exceeds the maximum permissible limit.

  **Limitation**: This error likely occurs when there are too many tables to migrate (>10k). There's a 4-MB limit for each call to the Azure Storage service.

  **Workaround**: Reach out to support by [creating a support request](https://ms.portal.azure.com/#blade/Microsoft_Azure_Support/HelpAndSupportBlade/overview?DMC=troubleshoot) and we can provide custom scripts to access our REST APIs directly.

## Duplicate key entry issue

- **Error**: The error is often a symptom of timeouts, network issues or target scaling.

  **Potential error message**: A batch couldn't be written to the table '{table}' due to a SQL error raised by the target server. For context, the batch contained a subset of rows returned by the following source query.

  **Limitation**: This error can be caused by timeout or broken connection to the target, resulting in duplicate primary keys. It might also be related to multiple migrations to the target running at the same time, or the user having test workloads running on the target while the migration is running. Additionally, the target might require primary keys to be unique, even though they aren't required to be so on the source.

  **Workaround**: To resolve this issue, ensure that there are no duplicate migrations running and that the source primary keys are unique. If error persists, reach out to support by [creating a support request](https://ms.portal.azure.com/#blade/Microsoft_Azure_Support/HelpAndSupportBlade/overview?DMC=troubleshoot) and we can provide custom scripts to access our REST APIs directly.

## Replicated operation had mismatched rows error

- **Error**: Online Migration Fails to Replicate Expected Number of Changes.

  **Potential error message**: An error occurred applying records to the target server which were read from the source server's binary log. The changes started at binary log '{mysql-bin.log}' and position '{position}' and ended at binary log '{mysql-bin.log}' and position '{position}'. All records on the source server prior to position '{position}' in binary log '{mysql-bin.log}' have been committed to the target.

  **Limitation**: On the source, there were insert and delete statements into a table, and the deletions were by an apparent unique index.

  **Workaround**: We recommend migrating the table manually.

## Table data truncated error

- **Error**: Enum column has a null value in one or more rows and the target SQL mode is set to strict.

  **Potential error message**: A batch couldn't be written to the table '{table}' due to a data truncation error. Please ensure that the data isn't too large for the data type of the MySQL table column. If the column type is an enum, make sure SQL Mode isn't set as TRADITIONAL, STRICT_TRANS_TABLES, or STRICT_ALL_TABLES and is the same on source and target.

  **Limitation**: The error occurs when historical data was written to the source server when they had certain setting, but when it's changed, data can't move.

  **Workaround**: To resolve the issue, we recommend changing the target SQL mode to non-strict or changing all null values to be valid values.

<a id="creating-object-failure"></a>

## Create object failure

- **Error**: An error occurred after view validation failed.

  **Limitation**: The error occurs when trying to migrate a view and the table that the view is supposed to be referencing can't be found.

  **Workaround**: We recommend migrating views manually.

## Unable to find table

- **Error**: An error occurred as referencing table cannot be found.

  **Potential error message**: The pipeline was unable to create the schema of object '{object}' for activity '{activity}' using strategy MySqlSchemaMigrationViewUsingTableStrategy because of a query execution.

  **Limitation**: The error can occur when the view is referring to a table that was deleted or renamed, or when the view was created with incorrect or incomplete information. This error can happen if a subset of tables are migrated, but the tables they depend on aren't.

  **Workaround**: We recommend migrating views manually. Check if all tables referenced in foreign keys and CREATE VIEW statements are selected for migration.

## All pooled connections broken

- **Error**: All connections on the source server were broken.

  **Limitation**: The error occurs when all the connections acquired at the start of initial load are lost due to server restart, network issues, heavy traffic on the source server or other transient problems. This error isn't recoverable. Additionally, this error occurs if an attempt to migrate a server is made during the maintenance window.

  **Workaround**: The migration must be restarted, and we recommend increasing the performance of the source server. Another issue is scripts that kill long running connections, prevents these scripts from working.

## Consistent snapshot broken

**Limitation**: The error occurs when the customer performs DDL during the initial load of the migration instance.

**Workaround**: To resolve this issue, we recommend refraining from making DDL changes during the Initial Load.

## Foreign key constraint

- **Error**: The error occurs when there is a change in the referenced foreign key type from the table.

  **Potential error message**: Referencing column '{pk column 1}' and referenced column '{fk column 1}' in foreign key constraint '{key}' are incompatible.

  **Limitation**: The error can cause schema migration of a table to fail, as the PK column in table 1 might not be compatible with the FK column in table 2.

  **Workaround**: To resolve this issue, we recommend dropping the foreign key and re-creating it after the migration process is completed.

## Related content

- [Tutorial: Migrate Azure Database for MySQL - Single Server to Flexible Server online using DMS via the Azure portal](tutorial-mysql-azure-single-to-flex-online-portal.md)
- [Tutorial: Migrate MySQL to Azure Database for MySQL offline using DMS](tutorial-mysql-azure-mysql-offline-portal.md)
