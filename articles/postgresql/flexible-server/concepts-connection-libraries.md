---
title: Connection libraries
description: This article describes several libraries and drivers that you can use when coding applications to connect and query an Azure Database for PostgreSQL flexible server.
author: olmoloce
ms.author: olmoloce
ms.reviewer: maghan
ms.date: 05/17/2024
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: concept-article
---

# Connection libraries for Azure Database for PostgreSQL flexible server

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

This article lists libraries and drivers that developers can use to develop applications to connect to and query an Azure Database for PostgreSQL flexible server.

## Client interfaces

Most language client libraries used to connect to an Azure Database for PostgreSQL flexible server are external projects and are distributed independently. The libraries listed are supported on the Windows, Linux, and Mac platforms, for connecting to Azure Database for PostgreSQL flexible server. Several quickstart examples are listed in the Next steps section.

| **Language** | **Client interface** | **Additional information** | **Download** |
|--------------|----------------------------------------------------------------|-------------------------------------|--------------------------------------------------------------------|
| Python | [psycopg](https://www.psycopg.org/) | DB API 2.0-compliant | [Download](https://sourceforge.net/projects/adodbapi/) |
| PHP | [php-pgsql](https://secure.php.net/manual/en/book.pgsql.php) | Database extension | [Install](https://secure.php.net/manual/en/pgsql.installation.php) |
| Node.js | [Pg npm package](https://www.npmjs.com/package/pg) | Pure JavaScript non-blocking client | [Install](https://www.npmjs.com/package/pg) |
| Java | [JDBC](https://jdbc.postgresql.org/) | Type 4 JDBC driver | [Download](https://jdbc.postgresql.org/download/)  |
| Ruby | [Pg gem](https://deveiate.org/code/pg/) | Ruby Interface | [Download](https://rubygems.org/downloads/pg-0.20.0.gem) |
| Go | [Package pq](https://godoc.org/github.com/lib/pq) | Pure Go postgres driver | [Install](https://github.com/lib/pq/blob/master/README.md) |
| C\#/ .NET | [Npgsql](https://www.npgsql.org/) | ADO.NET Data Provider | [Download](https://dotnet.microsoft.com/download) |
| ODBC | [psqlODBC](https://odbc.postgresql.org/) | ODBC Driver | [Download](https://www.postgresql.org/ftp/odbc/releases/) |
| C | [libpq](https://www.postgresql.org/docs/current/static/libpq.html) | Primary C language interface | Included |
| C++ | [libpqxx](http://pqxx.org/) | New-style C++ interface | [Download](https://pqxx.org/libpqxx/) |

## Related content

- [Quickstart: Use Python to connect and query data in Azure Database for PostgreSQL](connect-python.md).
- [Quickstart: Use Java to connect and query data from an Azure Database for PostgreSQL flexible server](connect-java.md).
- [Quickstart: Use .NET (C#) to connect and query data from an Azure Database for PostgreSQL flexible server](connect-csharp.md).
- [Quickstart: Use Go language to connect and query data from an Azure Database for PostgreSQL flexible server](connect-go.md).
- [Quickstart: Use PHP to connect and query data from an Azure Database for PostgreSQL flexible server](connect-php.md).
- [Quickstart: Use Azure CLI to connect and query data from an Azure Database for PostgreSQL flexible server](connect-azure-cli.md).
- [Quickstart: Import data from Azure Database for PostgreSQL flexible server in Power BI](connect-with-power-bi-desktop.md).
