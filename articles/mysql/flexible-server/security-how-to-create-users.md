---
title: How to Create Users for Azure Database for MySQL
description: This article describes how to create new user accounts to interact with an Azure Database for MySQL server.
author: SudheeshGH
ms.author: sunaray
ms.reviewer: maghan, randolphwest
ms.date: 01/07/2026
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: how-to
ms.custom:
  - horz-security
---

# Create users in Azure Database for MySQL

This article describes creating new user accounts to interact with an Azure Database for MySQL server.

> [!NOTE]  
> This article references the term *slave*, which Microsoft no longer uses. When the term is removed from the software, we remove it from this article.

You provided a server admin username and password when creating your Azure Database for MySQL server. For more information, see [Quickstart: Create an instance of Azure Database for MySQL with the Azure portal](quickstart-create-server-portal.md). You can determine your server admin user name in the Azure portal.

The server admin user has these privileges:

`SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, RELOAD, PROCESS, REFERENCES, INDEX, ALTER, SHOW DATABASES, CREATE TEMPORARY TABLES, LOCK TABLES, EXECUTE, REPLICATION SLAVE, REPLICATION CLIENT, CREATE VIEW, SHOW VIEW, CREATE ROUTINE, ALTER ROUTINE, CREATE USER, EVENT, TRIGGER`

After you create an Azure Database for the MySQL server, you can use the first server admin account to create more users and grant admin access to them. You can also use the server admin account to create less privileged users with access to individual database schemas.

> [!NOTE]  
> The SUPER privilege and DBA role aren't supported. For more details, see [the supported privileges documentation](concepts-limitations.md#privileges-and-data-manipulation-support).
>
> Password related plugin `caching_sha2_password` are enabled by default.
>
> Refer to this document if you want to enable `validate_password` plugin: [Built-in stored procedures in Azure Database for MySQL](concepts-built-in-store-procedure.md#2-plugin-management)

## Create a database

1. Get the connection information and admin user name.

   To connect to your database server, you need the full server name and admin sign-in credentials. You can easily find the server name and sign-in information on the server Overview or the Properties page in the Azure portal.

1. Use the admin account and password to connect to your database server. Use your preferred client tool, MySQL Workbench, mysql.exe, or HeidiSQL.

1. Edit and run the following SQL code. Replace the placeholder value `db_user` with your intended new user name. Replace the placeholder value `testdb` with your database name.

This SQL code creates a new database named testdb. It then makes a new user in the MySQL service and grants that user all privileges for the new database schema (testdb.\*).

```sql
CREATE DATABASE testdb;
```

## Create a nonadmin user

You can create a nonadmin user using the `CREATE USER` MySQL statement.

```sql
CREATE USER 'db_user'@'%' IDENTIFIED BY 'StrongPassword!';

GRANT ALL PRIVILEGES ON testdb . * TO 'db_user'@'%';

FLUSH PRIVILEGES;
```

## Verify the user permissions

To view the privileges allowed for user `db_user` on `testdb` database, run the ```SHOW GRANTS``` MySQL statement.

```sql
USE testdb;

SHOW GRANTS FOR 'db_user'@'%';
```

## Connect to the database with the new user

Sign in to the server, specify the designated database, and use the new username and password. This example shows the MySQL command line. When you use this command, you're prompted for the user's password. Use your own server name, database name, and user name. See how to connect in the following table.

```console
--host mydemoserver.mysql.database.azure.com --database testdb --user db_user -p
```

## Limit privileges for a user

To restrict the type of operations a user can run on the database, you must explicitly add the operations in the **GRANT** statement. See the following example:

```sql
CREATE USER 'new_master_user'@'%' IDENTIFIED BY 'StrongPassword!';

GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, RELOAD, PROCESS, REFERENCES, INDEX, ALTER, SHOW DATABASES, CREATE TEMPORARY TABLES, LOCK TABLES, EXECUTE, REPLICATION SLAVE, REPLICATION CLIENT, CREATE VIEW, SHOW VIEW, CREATE ROUTINE, ALTER ROUTINE, CREATE USER, EVENT, TRIGGER ON *.* TO 'new_master_user'@'%' WITH GRANT OPTION;

FLUSH PRIVILEGES;
```

## About azure_superuser

Servers are created with a user called `azure_superuser`. Microsoft created a system account to manage the server and conduct monitoring, backups, and regular maintenance. On-call engineers might also use this account to access the server during an incident with certificate authentication and must request access using just-in-time (JIT) processes.

## Related content

- [User account management](https://dev.mysql.com/doc/refman/5.7/en/access-control.html)
- [GRANT syntax](https://dev.mysql.com/doc/refman/5.7/en/grant.html)
- [Privileges](https://dev.mysql.com/doc/refman/5.7/en/privileges-provided.html)
