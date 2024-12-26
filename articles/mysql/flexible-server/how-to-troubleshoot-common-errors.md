---
title: Troubleshoot Common Errors
description: Learn how to troubleshoot common migration errors encountered by users new to Azure Database for MySQL - Flexible Server.
author: sudheeshgh
ms.author: sunaray
ms.reviewer: maghan
ms.date: 11/27/2024
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: troubleshooting
ms.custom:
  - mvc
---

# Troubleshoot errors commonly encountered during or post migration to Azure Database for MySQL - Flexible Server

Azure Database for MySQL Flexible Server is a fully managed service powered by the community version of MySQL. The MySQL experience in a managed service environment might differ from running MySQL in your own environment. In this article, you see some of the common errors users might encounter while migrating to or developing on Azure Database for MySQL Flexible Server for the first time.

## Common Connection Errors

### ERROR 1184 (08S01): Aborted connection 22 to db: 'db-name' user: 'user' host: 'hostIP' (init_connect command failed)

The above error occurs after successful sign-in but before executing any command when session is established. The above message indicates you have set an incorrect value of `init_connect` server parameter, which is causing the session initialization to fail.

There are some server parameters like `require_secure_transport` that aren't supported at the session level, and so trying to change the values of these parameters using `init_connect` can result in Error 1184 while connecting to the Azure Database for MySQL Flexible Server instance as shown below:

mysql> show databases;
ERROR 2006 (HY000): MySQL server has gone away
No connection. Trying to reconnect...
Connection ID:    64897
Current database: ** NONE **
ERROR 1184 (08S01): Aborted connection 22 to db: 'db-name' user: 'user' host: 'hostIP' (init_connect command failed)

**Resolution**: Reset `init_connect` value in Server parameters tab in Azure portal and set only the supported server parameters using init_connect parameter.

## Errors due to lack of SUPER privilege and DBA role

The SUPER privilege and DBA role aren't supported on the service. As a result, you might encounter some common errors listed below:

### ERROR 1419: You don't have the SUPER privilege and binary logging is enabled (you *might* want to use the less safe log_bin_trust_function_creators variable)

The above error might occur while creating a function, trigger as below or importing a schema. The DDL statements like CREATE FUNCTION or CREATE TRIGGER are written to the binary log, so the secondary replica can execute them. The replica SQL thread has full privileges, which can be exploited to elevate privileges. To guard against this danger for servers that have binary logging enabled, the MySQL engine requires that stored function creators have the SUPER privilege, in addition to the usual CREATE ROUTINE privilege.

```sql
CREATE FUNCTION f1(i INT)
RETURNS INT
DETERMINISTIC
READS SQL DATA
BEGIN
  RETURN i;
END;
```

**Resolution**: To resolve the error, set `log_bin_trust_function_creators` to 1, execute the DDL statements or import the schema to create the desired objects. You can continue to maintain `log_bin_trust_function_creators` to 1 for your server to avoid the error in future. Our recommendation is to set `log_bin_trust_function_creators` as the security risk highlighted in [MySQL community documentation](https://dev.mysql.com/doc/refman/5.7/en/replication-options-binary-log.html#sysvar_log_bin_trust_function_creators) is minimal in Azure Database for MySQL Flexible Server as bin log isn't exposed to any threats.

#### ERROR 1227 (42000) at line 101: Access denied; you need (at least one of) the SUPER privilege(s) for this operation. Operation failed with exitcode 1

The above error might occur while importing a dump file or creating procedure that contains [definers](https://dev.mysql.com/doc/refman/5.7/en/create-procedure.html).

**Resolution**: To resolve this error, the admin user can grant privileges to create or execute procedures by running GRANT command as in the following examples:

```sql
GRANT CREATE ROUTINE ON mydb.* TO 'someuser'@'somehost';
GRANT EXECUTE ON PROCEDURE mydb.myproc TO 'someuser'@'somehost';
```

Alternately, you can replace the definers with the name of the admin user that is running the import process as shown below.

```sql
DELIMITER;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`127.0.0.1`*/ /*!50003
DELIMITER;;

/* Modified to */

DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`AdminUserName`@`ServerName`*/ /*!50003
DELIMITER ;
```

#### ERROR 1227 (42000) at line 295: Access denied; you need (at least one of) the SUPER or SET_USER_ID privileges for this operation

The above error might occur while executing CREATE VIEW with DEFINER statements as part of importing a dump file or running a script. Azure Database for MySQL Flexible Server doesn't allow SUPER privileges or the SET_USER_ID privilege to any user.

**Resolution**:

- Use the definer user to execute CREATE VIEW if possible. It's likely that there are many views with different definers having different permissions, so this might not be feasible. OR
- Edit the dump file or CREATE VIEW script and remove the DEFINER= statement from the dump file. OR
- Edit the dump file or CREATE VIEW script and replace the definer values with user with admin permissions who is performing the import or execute the script file.

> [!TIP]  
> Use sed or perl to modify a dump file or SQL script to replace the DEFINER= statement

#### ERROR 1227 (42000) at line 18: Access denied; you need (at least one of) the SUPER privilege(s) for this operation

The above error might occur if you're using trying to import the dump file from an Azure Database for MySQL Flexible Server instance with GTID enabled to the target Azure Database for MySQL Flexible Server instance. Mysqldump adds SET @@SESSION.sql_log_bin=0 statement to a dump file from a server where GTIDs are in use, which disables binary logging while the dump file is being reloaded.

**Resolution**:
To resolve this error while importing, remove or comment out the below lines in your mysqldump file and run import again to ensure it's successful.

SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;  
SET @@SESSION.SQL_LOG_BIN= 0;
SET @@GLOBAL.GTID_PURGED='';
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;

## Common connection errors for server admin sign-in

When an Azure Database for MySQL Flexible Server instance is created, a server admin sign-in is provided by the end user during the server creation. The server admin sign-in allows you to create new databases, add new users and grant permissions. If the server admin sign-in is deleted, its permissions are revoked or its password is changed, you might start to see connections errors in your application while connections. Following are some of the common errors.

### ERROR 1045 (28000): Access denied for user 'username'@'IP address' (using password: YES)

The above error occurs if:

- The username doesn't exist.
- The user username was deleted.
- its password is changed or reset.

**Resolution**:

- Validate if "username" exists as a valid user in the server or is accidentally deleted. You can execute the following query by logging into the Azure Database for MySQL Flexible Server user:

  ```sql
  select user from mysql.user;
  ```

## Related content

- [Microsoft Q&A question page](/answers/topics/azure-database-mysql.html)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/azure-database-mysql)
- [file a ticket from the Azure portal](https://portal.azure.com/?#blade/Microsoft_Azure_Support/HelpAndSupportBlade)
- [support request](https://portal.azure.com/#blade/Microsoft_Azure_Support/HelpAndSupportBlade/newsupportrequest)
- [UserVoice](https://feedback.azure.com/d365community/forum/47b1e71d-ee24-ec11-b6e6-000d3a4f0da0)
