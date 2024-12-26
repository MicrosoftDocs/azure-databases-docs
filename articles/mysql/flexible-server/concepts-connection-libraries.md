---
title: Connection Libraries
description: This article lists each library or driver that client programs can use when connecting to Azure Database for MySQL - Flexible Server.
author: SudheeshGH
ms.author: sunaray
ms.reviewer: maghan
ms.date: 11/27/2024
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: conceptual
---

# Connection libraries for Azure Database for MySQL - Flexible Server

This article lists each library or driver that client programs can use when connecting to Azure Database for MySQL Flexible Server.

## Client interfaces

MySQL offers standard database driver connectivity for using MySQL with applications and tools that are compatible with industry standards ODBC and JDBC. Any system that works with ODBC or JDBC can use MySQL.

| **Language** | **Platform** | **Additional Resource** | **Download** |
| :--- | :--- | :--- | :--- |
| PHP | Windows, Linux | [MySQL native driver for PHP - mysqlnd](https://dev.mysql.com/downloads/connector/php-mysqlnd/) | [Download](https://www.php.net/downloads.php) |
| ODBC | Windows, Linux, macOS X, and Unix platforms | [MySQL Connector/ODBC Developer Guide](https://dev.mysql.com/doc/connector-odbc/en/) | [Download](https://dev.mysql.com/downloads/connector/odbc/) |
| ADO.NET | Windows | [MySQL Connector/Net Developer Guide](https://dev.mysql.com/doc/connector-net/en/) | [Download](https://dev.mysql.com/downloads/connector/net/) |
| JDBC | Platform independent | MySQL Connector/J 8.1 Developer Guide | [Download](https://dev.mysql.com/downloads/connector/j/) |
| Node.js | Windows, Linux, macOS X | [sidorares/node-mysql2](https://github.com/sidorares/node-mysql2/blob/master/website/docs/documentation/00-index.mdx) | [Download](https://github.com/sidorares/node-mysql2) |
| Python | Windows, Linux, macOS X | [MySQL Connector/Python Developer Guide](https://dev.mysql.com/doc/connector-python/en/) | [Download](https://dev.mysql.com/downloads/connector/python/) |
| C++ | Windows, Linux, macOS X | [MySQL Connector/C++ Developer Guide](https://dev.mysql.com/doc/refman/8.1/en/connector-cpp-info.html) | [Download](https://dev.mysql.com/downloads/connector/python/) |
| C | Windows, Linux, macOS X | [MySQL Connector/C Developer Guide](https://dev.mysql.com/doc/c-api/8.0/en/) | [Download](https://dev.mysql.com/downloads/connector/c/) |
| Perl | Windows, Linux, macOS X, and Unix platforms | [DBD::MySQL](https://metacpan.org/pod/DBD::mysql) | [Download](https://metacpan.org/pod/DBD::mysql) |

## Related content

- [Use PHP with Azure Database for MySQL - Flexible Server](connect-php.md)
- [Use Java and JDBC with Azure Database for MySQL - Flexible Server](connect-java.md)
- [Quickstart: Use .NET (C#) to connect and query data in Azure Database for MySQL - Flexible Server](connect-csharp.md)
- [Quickstart: Use Python to connect and query data in Azure Database for MySQL - Flexible Server](connect-python.md)
- [Quickstart: Use Node.js to connect and query data in Azure Database for MySQL - Flexible Server](connect-nodejs.md)
- [Ruby](../single-server/connect-ruby.md)
- [C++](../single-server/connect-cpp.md)
- [Go](../single-server/connect-go.md)
