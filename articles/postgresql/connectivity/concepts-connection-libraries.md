---
title: Connection Libraries
description: This article describes several libraries and drivers that you can use when coding applications to connect and query an Azure Database for PostgreSQL flexible server instance.
author: shreyaaithal
ms.author: shaithal
ms.reviewer: maghan
ms.date: 09/30/2025
ms.service: azure-database-postgresql
ms.topic: concept-article
---

# Connection libraries for Azure Database for PostgreSQL 

This article lists libraries and drivers that developers can use to develop applications to connect to and query an Azure Database for PostgreSQL flexible server instance.

## Client interfaces

Most language client libraries used to connect to Azure Database for PostgreSQL are external projects and are distributed independently. The  libraries listed are supported on the Windows, Linux, and Mac platforms, for connecting to an Azure Database for PostgreSQL flexible server instance. Several quickstart examples are listed in the Next steps section.

| **Language** | **Client interface** | **Additional information** | **Download** |
| --- | --- | --- | --- |
| Python | [psycopg](https://www.psycopg.org/) | DB API 2.0-compliant | [Download](https://sourceforge.net/projects/adodbapi/) |
| PHP | [php-pgsql](https://secure.php.net/manual/en/book.pgsql.php) | Database extension | [Install](https://secure.php.net/manual/en/pgsql.installation.php) |
| Node.js | [Pg npm package](https://www.npmjs.com/package/pg) | Pure JavaScript nonblocking client | [Install](https://www.npmjs.com/package/pg) |
| Java | [JDBC](https://jdbc.postgresql.org/) | Type 4 JDBC driver | [Download](https://jdbc.postgresql.org/download/) |
| Ruby | [Pg gem](https://rubygems.org/gems/pg) | Ruby Interface | [Download](https://rubygems.org/downloads/pg-0.20.0.gem) |
| Go | [Package pq](https://godoc.org/github.com/lib/pq) | Pure Go postgres driver | [Install](https://github.com/lib/pq/blob/master/README.md) |
| C\#/ .NET | [Npgsql](https://www.npgsql.org/) | ADO.NET Data Provider | [Download](https://dotnet.microsoft.com/download) |
| ODBC | [psqlODBC](https://odbc.postgresql.org/) | ODBC Driver | [Download](https://www.postgresql.org/ftp/odbc/releases/) |
| C | [libpq](https://www.postgresql.org/docs/current/static/libpq.html) | Primary C language interface | Included |
| C++ | [libpqxx](http://pqxx.org/) | New-style C++ interface | [Download](https://pqxx.org/libpqxx/) |

## Related content

- [Quickstart: Use Python to connect and query data in Azure Database for PostgreSQL](connect-python.md)
- [Quickstart: Use Java to connect and query data from an Azure Database for PostgreSQL](connect-java.md)
- [Quickstart: Use .NET (C#) to connect and query data from an Azure Database for PostgreSQL](connect-csharp.md)
- [Quickstart: Use Go language to connect and query data from an Azure Database for PostgreSQL](connect-go.md)
- [Quickstart: Use PHP to connect and query data from an Azure Database for PostgreSQL](connect-php.md)
- [Quickstart: Use Azure CLI to connect and query data from an Azure Database for PostgreSQL](connect-azure-cli.md)
- [Quickstart: Import data from an Azure Database for PostgreSQL flexible server instance in Power BI](../integration/connect-with-power-bi-desktop.md)
