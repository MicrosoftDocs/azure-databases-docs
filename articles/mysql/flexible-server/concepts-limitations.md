---
title: Limitations in Azure Database for MySQL - Flexible Server
description: This article describes limitations in Azure Database for MySQL - Flexible Server, such as the number of connection and storage engine options.
author: SudheeshGH
ms.author: sunaray
ms.reviewer: maghan
ms.date: 11/27/2024
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: concept-article
---

# Limitations in Azure Database for MySQL - Flexible Server

This article describes limitations in Azure Database for MySQL - Flexible Server. [General limitations](https://dev.mysql.com/doc/mysql-reslimits-excerpt/5.7/en/limits.html) in the MySQL database engine also apply. If you want to learn about resource limitations (compute, memory, storage), see the [article about compute and storage](concepts-service-tiers-storage.md).

## Server parameters

Azure Database for MySQL - Flexible Server supports tuning the values of server parameters. Some parameters' minimum and maximum values (for example, `max_connections`, `join_buffer_size`, `query_cache_size`) are determined by the compute tier and before you compute the size of the server. For more information about these limits, along with minimum and maximum values for server parameters like `max_connections` and `innodb_buffer_pool_size`, see the [article about server parameters](concepts-server-parameters.md).

### Generated invisible primary keys

For MySQL version 8.0 and later, [generated invisible primary keys (GIPKs)](https://dev.mysql.com/doc/refman/8.0/en/create-table-gipks.html) are enabled by default for all Azure Database for MySQL - Flexible Server instances.

MySQL 8.0+ servers add the invisible column `my_row_id` to the tables and a primary key on that column, where the InnoDB table is created without an explicit primary key. For this reason, you can't create a table that has a column named `my_row_id` unless the table creation statement also specifies an explicit primary key. [Learn more](https://dev.mysql.com/doc/refman/8.0/en/create-table-gipks.html).

By default, GIPKs appear in the output of [SHOW CREATE TABLE](https://dev.mysql.com/doc/refman/8.0/en/show-create-table.html), [SHOW COLUMNS](https://dev.mysql.com/doc/refman/8.0/en/show-columns.html), and [SHOW INDEX](https://dev.mysql.com/doc/refman/8.0/en/show-index.html). GIPKs are also visible in the `INFORMATION_SCHEMA` [COLUMNS](https://dev.mysql.com/doc/refman/8.0/en/information-schema-columns-table.html) and [STATISTICS](https://dev.mysql.com/doc/refman/8.0/en/information-schema-statistics-table.html) tables.

For more details on GIPKs and their use cases with data-in replication, see [Replicate data into Azure Database for MySQL - Flexible Server](./concepts-data-in-replication.md#generated-invisible-primary-key).

#### Steps to disable a GIPK

If you want to disable a GIPK, you have two options:

- Change the value of the [sql_generate_invisible_primary_key](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_sql_generate_invisible_primary_key) server parameter to `OFF` by using the [Azure portal](./how-to-configure-server-parameters-portal.md#configure-server-parameters) or the [Azure CLI](./how-to-configure-server-parameters-cli.md#modify-a-server-parameter-value).

- Connect to your Azure Database for MySQL - Flexible Server instance and run the following command:

  ```sql
  mysql> SET sql_generate_invisible_primary_key=OFF;
  ```

### lower_case_table_names

For [MySQL version 8.0+](https://dev.mysql.com/doc/refman/8.0/en/identifier-case-sensitivity.html) you can configure `lower_case_table_names` only when you're initializing the server. [Learn more](https://dev.mysql.com/doc/refman/8.0/en/identifier-case-sensitivity.html). Changing the `lower_case_table_names` setting after the server is initialized is prohibited. Supported values for MySQL version 8.0 are `1` and `2` in Azure Database for MySQL - Flexible Server. The default value is `1`.

You can configure these settings in the portal during server creation by specifying the desired value under Server Parameters on the Additional Configuration page. For restore operations or replica server creation, the parameter will automatically be copied from the source server and cannot be changed. 

:::image type="content" source="media/concepts-server-parameters\flexible-server-lower-case-configure.png" alt-text="Screenshot that shows how to configure lower case table name server parameter at the time of creation." lightbox="media/concepts-server-parameters\flexible-server-lower-case-configure.png":::

For MySQL version 5.7, the default value of `lower_case_table_names` is `1` in Azure Database for MySQL - Flexible Server. Although it's possible to change the supported value to `2`, reverting from `2` back to `1` isn't allowed. For assistance in changing the default value, [create a support ticket](https://azure.microsoft.com/support/create-ticket/).

## Storage engines

MySQL supports many storage engines. The following lists show which storage engines are supported and unsupported in Azure Database for MySQL - Flexible Server.

### Supported engines

- [InnoDB](https://dev.mysql.com/doc/refman/5.7/en/innodb-introduction.html)
- [MEMORY](https://dev.mysql.com/doc/refman/5.7/en/memory-storage-engine.html)

> [!NOTE]  
> - The maximum supported size for a single MySQL file is 8 TB in Azure Database for MySQL -Flexible server.

### Unsupported engines

- [MyISAM](https://dev.mysql.com/doc/refman/5.7/en/myisam-storage-engine.html)
- [BLACKHOLE](https://dev.mysql.com/doc/refman/5.7/en/blackhole-storage-engine.html)
- [ARCHIVE](https://dev.mysql.com/doc/refman/5.7/en/archive-storage-engine.html)
- [FEDERATED](https://dev.mysql.com/doc/refman/5.7/en/federated-storage-engine.html)

## Privileges and data-manipulation support

Many server parameters and settings can inadvertently degrade server performance or negate the ACID (atomic, consistent, isolated, and durable) properties of the MySQL server. To maintain service integrity and the service-level agreement at a product level, Azure Database for MySQL - Flexible Server doesn't expose multiple roles.

Azure Database for MySQL - Flexible Server doesn't allow direct access to the underlying file system. Some data-manipulation commands aren't supported.

### Supported privileges

- `LOAD DATA INFILE` is supported, but you must specify the `[LOCAL]` parameter and direct it to a UNC path (Azure storage mounted through Server Message Block). If you're using MySQL client version 8.0 or later, you need to include the `-–local-infile=1` parameter in your connection string.

- For MySQL version 8.0 and later, only the following [dynamic privileges](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#privileges-provided-dynamic) are supported:
  - [REPLICATION_APPLIER](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#priv_replication-applier)
  - [ROLE_ADMIN](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#priv_role-admin)
  - [SESSION_VARIABLES_ADMIN](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#priv_session-variables-admin)
  - [SHOW ROUTINE](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#priv_show-routine)
  - [XA_RECOVER_ADMIN](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#priv_xa-recover-admin)

### Unsupported privileges

- The database administrator (DBA) role is restricted. Alternatively, you can use the role of the administrator user who's assigned during creation of a new server. This role allows you to perform most of the Data Definition Language (DDL) and Data Manipulation Language (DML) statements.

- The following [static privileges](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#privileges-provided-static) are restricted:
  - [SUPER](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#priv_super)
  - [FILE](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#priv_file)
  - [CREATE TABLESPACE](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#priv_create-tablespace)
  - [SHUTDOWN](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#priv_shutdown)

- Granting [BACKUP_ADMIN](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#priv_backup-admin) privileges isn't supported for taking backups by using [migration tools](../migrate/how-to-decide-on-right-migration-tools.md).

- `DEFINER` requires `SUPER` privileges to create and is restricted. If you're importing data by using a backup, manually remove the `CREATE DEFINER` commands or use the `--skip-definer` command when you're performing a [mysqlpump](https://dev.mysql.com/doc/refman/5.7/en/mysqlpump.html) backup.

- The [mysql system database](https://dev.mysql.com/doc/refman/5.7/en/system-schema.html) is read-only and supports various platform as a service (PaaS) functionalities. You can't make changes to the `mysql` system database.

- `SELECT ... INTO OUTFILE` isn't supported in the service.

## Functional limitations

### Zone-redundant high availability

You can set a zone-redundant high-availability configuration only during server creation. This configuration isn't supported in the Burstable compute tier.

### Network

You can't change the connectivity method after you create the server. If you create the server with *private access (virtual network integration)*, it can't be changed to *public access (allowed IP addresses)* after creation, and vice versa.

### Stop/start operations

Operations to stop and start the server are not supported with read replica configurations (both source and replicas).

### Scale operations

Decreasing provisioned server storage isn't supported.

### Server version upgrades

Automated migration between major database engine versions isn't supported. If you want to upgrade the major version, use a [dump and restore](../concepts-migrate-dump-restore.md) on a server that you created with the new engine version.

### Restore a server

With point-in-time restore, new servers have the same compute and storage configurations as the source server that they're based on. You can scale down the newly restored server's compute after you create the server.

## Feature comparisons

Not all features available in Azure Database for MySQL - Single Server are available in Azure Database for MySQL - Flexible Server.

For the complete list of feature comparisons between Azure Database for MySQL - Single Server and Azure Database for MySQL - Flexible Server, see the [article about choosing the right MySQL Server option in Azure](../select-right-deployment-type.md#compare-the-mysql-deployment-options-in-azure).

## Related content

- [what compute and storage options are available in flexible servers](concepts-service-tiers-storage.md)
- [supported MySQL versions](concepts-supported-versions.md)
- [use the Azure portal to create an Azure Database for MySQL - Flexible Server instance](quickstart-create-server-portal.md)
