---
title: Issues Connecting Source Databases
titleSuffix: Azure Database Migration Service
description: Learn about how to troubleshoot known issues/errors associated with connecting Azure Database Migration Service to source databases.
author: abhims14
ms.author: abhishekum
ms.reviewer: randolphwest
ms.date: 10/28/2025
ms.service: azure-database-migration-service
ms.topic: troubleshooting
ms.collection:
  - sql-migration-content
---

# Troubleshoot DMS errors when connecting to source databases

The following article provides detail about how to address potential issues you might encounter when connecting the Azure Database Migration Service (DMS) to your source database. Each section in this article relates to a specific type of source database, listing the error you might encounter together with detail and links to information about how to troubleshoot the connectivity.

## SQL Server

Potential issues associated with connecting to a source SQL Server database and how to address them are provided in the following table.

| Error | Cause and troubleshooting detail |
| --- | --- |
| SQL connection failed. A network-related or instance-specific error occurred while establishing a connection to SQL Server. The server was not found or was not accessible. Verify that the instance name is correct, and that SQL Server is configured to allow remote connections. | This error occurs if the service can't locate the source server. To address the issue, see [Error connecting to source SQL Server when using dynamic port or named instance](known-issues-troubleshooting-dms.md#error-connecting-to-source-sql-server-when-using-dynamic-port-or-named-instance). |
| **Error 53** - SQL connection failed. (Also, for error codes 1, 2, 5, 53, 233, 258, 1225, 11001) | This error occurs if the service can't connect to the source server. To address the issue, refer to the following resources, and then try again.<br /><br />[Interactive user guide to troubleshoot the connectivity issue](/troubleshoot/sql/database-engine/connect/resolve-connectivity-errors-overview)<br /><br />[Prerequisites for migrating SQL Server to Azure SQL Database](pre-reqs.md#prerequisites-for-migrating-sql-server-to-azure-sql-managed-instance)<br /><br />[Prerequisites for migrating SQL Server to an Azure SQL Managed Instance](pre-reqs.md#prerequisites-for-migrating-sql-server-to-azure-sql-managed-instance) |
| **Error 18456** - Login failed. | This error occurs if the service can't connect to the source database using the provided T-SQL credentials. To address the issue, verify the entered credentials. You can also refer to [MSSQLSERVER_18456](/sql/relational-databases/errors-events/mssqlserver-18456-database-engine-error) or to the troubleshooting documents listed in the note below this table, and then try again. |
| Malformed AccountName value '{0}' provided. Expected format for AccountName is DomainName\UserName | This error occurs if the user selects Windows authentication but provides the username in an invalid format. To address the issue, either provide username in the correct format for Windows authentication or select **SQL Authentication**. |

## AWS RDS MySQL

Potential issues associated with connecting to a source AWS RDS MySQL database and how to address them are provided in the following table.

| Error | Cause and troubleshooting detail |
| --- | --- |
| **Error [2003]**[HY000] - connection failed. ERROR [HY000] [MySQL][ODBC x.x(w) driver] Cannot connect to MySQL server on '{server}' (10060) | This error occurs if the MySQL ODBC driver can't connect to the source server. To address the issue, refer to the troubleshooting documents listed in the note below this table, and then try again. |
| **Error [2005]**[HY000] - connection failed. ERROR [HY000] [MySQL][ODBC x.x(w) driver] Unknown MySQL server host '{server}' | This error occurs if the service can't find the source host on RDS. The issue could either be because the listed source doesn't exist or there's a problem with RDS infrastructure. To address the issue, refer to the troubleshooting documents listed in the note below this table, and then try again. |
| **Error [1045]**[HY000] - connection failed. ERROR [HY000] [MySQL][ODBC x.x(w) driver] Access denied for user '{user}'@'{server}' (using password: YES) | This error occurs if MySQL ODBC driver can't connect to the source server due to invalid credentials. Verify the credentials you have entered. If the issue continues, verify that source computer has the correct credentials. You might need to reset the password in the console. If you still encounter the issue, refer to the troubleshooting documents listed in the note below this table, and then try again. |
| **Error [9002]**[HY000] - connection failed. ERROR [HY000] [MySQL][ODBC x.x(w) driver] The connection string might not be right. Visit portal for references. | This error occurs if the connection is failing due to an issue with the connection string. Verify the connection string provided is valid. To address the issue, refer to the troubleshooting documents listed in the note below this table, and then try again. |
| **Error in binary logging. Variable binlog_format has value '{value}'. Please change it to 'row'.** | This error occurs if there's an error in binary logging; the variable binlog_format has the wrong value. To address the issue, change the binlog_format in parameter group to 'ROW', and then reboot the instance. For more information, see to [Binary Logging Options and Variables](https://dev.mysql.com/doc/refman/5.7/en/replication-options-binary-log.html) or [AWS RDS MySQL Database Log Files documentation](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_LogAccess.Concepts.MySQL.html). |

For more information about troubleshooting issues related to connecting to a source AWS RDS MySQL database, see the following resources:

- [Troubleshooting for Amazon RDS Connectivity issues](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_Troubleshooting.html#CHAP_Troubleshooting.Connecting)

- [How do I resolve problems connecting to my Amazon RDS database instance?](https://repost.aws/knowledge-center/rds-cannot-connect)

## AWS RDS PostgreSQL

Potential issues associated with connecting to a source AWS RDS PostgreSQL database and how to address them are provided in the following table.

| Error | Cause and troubleshooting detail |
| --- | --- |
| **Error [101]**[08001] - connection failed. ERROR [08001] timeout expired. | This error occurs if the Postgres driver can't connect to the source server. To address the issue, refer to the troubleshooting documents listed in the note below this table, and then try again. |
| **Error: Parameter wal_level has value '{value}'. Please change it to 'logical' to allow replication.** | This error occurs if the parameter wal_level has the wrong value. To address the issue, change the rds.logical_replication in parameter group to 1, and then reboot the instance. For more information, see to [Pre-requisites for migrating to Azure PostgreSQL using DMS](tutorial-postgresql-azure-postgresql-online.md#prerequisites) or [PostgreSQL on Amazon RDS](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_PostgreSQL.html). |

For more information about troubleshooting issues related to connecting to a source AWS RDS PostgreSQL database, see the following resources:

- [Troubleshooting for Amazon RDS Connectivity issues](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_Troubleshooting.html#CHAP_Troubleshooting.Connecting)

- [How do I resolve problems connecting to my Amazon RDS database instance?](https://repost.aws/knowledge-center/rds-cannot-connect)

## AWS RDS SQL Server

Potential issues associated with connecting to a source AWS RDS SQL Server database and how to address them are provided in the following table.

| Error | Cause and troubleshooting detail |
| --- | --- |
| **Error 53** - SQL connection failed. A network-related or instance-specific error occurred while establishing a connection to SQL Server. The server was not found or was not accessible. Verify that the instance name is correct, and that SQL Server is configured to allow remote connections. (provider: Named Pipes Provider, error: 40 - Could not open a connection to SQL Server) | This error occurs if the service can't connect to the source server. To address the issue, refer to the troubleshooting documents listed in the note below this table, and then try again. |
| **Error 18456** - Login failed. Login failed for user '{user}' | This error occurs if the service can't connect to the source database with the T-SQL credentials provided. To address the issue, verify the entered credentials. You can also refer to [MSSQLSERVER_18456](/sql/relational-databases/errors-events/mssqlserver-18456-database-engine-error) or to the troubleshooting documents listed in the note below this table, and try again. |
| **Error 87** - Connection string is not valid. A network-related or instance-specific error occurred while establishing a connection to SQL Server. The server was not found or was not accessible. Verify that the instance name is correct, and that SQL Server is configured to allow remote connections. (provider: SQL Network Interfaces, error: 25 - Connection string is not valid) | This error occurs if the service can't connect to the source server because of an invalid connection string. To address the issue, verify the connection string provided. If the issue persists, refer to the troubleshooting documents listed in the note below this table, and then try again. |
| **Error - Server certificate not trusted.** A connection was successfully established with the server, but then an error occurred during the login process. (provider: SSL Provider, error: 0 - The certificate chain was issued by an authority that is not trusted.) | This error occurs if the certificate used isn't trusted. To address the issue, you need to find a certificate that can be trusted, and then enable it on the server. Alternatively, you can select the Trust Certificate option while connecting. Take this action only if you're familiar with the certificate used and you trust it.<br /><br />TLS connections that are encrypted using a self-signed certificate don't provide strong security -- they're susceptible to man-in-the-middle attacks. Don't rely on TLS using self-signed certificates in a production environment or on servers that are connected to the internet.<br /><br />For more information, see to [Using SSL with a Microsoft SQL Server DB Instance](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/SQLServer.Concepts.General.SSL.Using.html) or [Tutorial: Migrate RDS SQL Server to Azure using DMS](index.yml). |
| **Error 300** - User does not have required permissions. VIEW SERVER STATE permission was denied on object '{server}', database '{database}' | This error occurs if user doesn't have permission to perform the migration. To address the issue, refer to [GRANT Server Permissions - Transact-SQL](/sql/t-sql/statements/grant-server-permissions-transact-sql) or [Tutorial: Migrate RDS SQL Server to Azure using DMS](index.yml) for more details. |

For more information about troubleshooting issues related to connecting to a source AWS RDS SQL Server, see the following resources:

- [Solving Connectivity errors to SQL Server](/troubleshoot/sql/database-engine/connect/resolve-connectivity-errors-overview)
- [How do I resolve problems connecting to my Amazon RDS database instance?](https://repost.aws/knowledge-center/rds-cannot-connect)

## Known issues

- [Known issues/migration limitations with online migrations to Azure SQL Database](index.yml)
- [Known issues and limitations with online migrations from PostgreSQL to Azure Database for PostgreSQL](known-issues-azure-postgresql-online.md)

## Related content

- [Azure Database Migration Service PowerShell](/powershell/module/az.datamigration#data_migration)
- [How to configure server parameters in Azure Database for MySQL by using the Azure portal](../mysql/howto-server-parameters.md)
- [Overview of prerequisites for using Azure Database Migration Service](pre-reqs.md)
- [FAQ about using Azure Database Migration Service](faq.yml)
