---
title: Connection Libraries in Azure HorizonDB
description: This article describes several libraries and drivers that you can use when coding applications to connect and query an Azure HorizonDB instance.
author: avnishrastogimsft
ms.author: avrastog
ms.reviewer: maghan
ms.date: 05/05/2026
ms.service: azure-database-postgresql
ms.subservice: connectivity
ms.topic: concept-article
---

# Connection libraries in Azure HorizonDB

This article lists libraries and drivers that developers can use to develop applications to connect to and query an Azure HorizonDB instance.

## Client interfaces

Most language client libraries used to connect to Azure HorizonDB are external projects and are distributed independently. The libraries listed are supported on the Windows, Linux, and Mac platforms, for connecting to an Azure HorizonDB instance. Several quickstart examples are listed in the Next steps section.

| **Language** | **Client interface** | **Additional information** | **Download** |
| --- | --- | --- | --- |
| Python | [psycopg](https://www.psycopg.org/) | DB API 2.0-compliant | [Download](https://sourceforge.net/projects/adodbapi/) |
| PHP | [php-pgsql](https://www.php.net/manual/en/book.pgsql.php) | Database extension | [Install](https://www.php.net/manual/en/pgsql.installation.php) |
| Node.js | [Pg npm package](https://www.npmjs.com/package/pg) | Pure JavaScript nonblocking client | [Install](https://www.npmjs.com/package/pg) |
| Java | [JDBC](https://jdbc.postgresql.org/) | Type 4 JDBC driver | [Download](https://jdbc.postgresql.org/download/) |
| Ruby | [Pg gem](https://rubygems.org/gems/pg) | Ruby Interface | [Download](https://rubygems.org/downloads/pg-0.20.0.gem) |
| Go | [Package pq](https://pkg.go.dev/github.com/lib/pq?utm_source=godoc) | Pure Go postgres driver | [Install](https://github.com/lib/pq/blob/master/README.md) |
| C\#/ .NET | [Npgsql](https://www.npgsql.org/) | ADO.NET Data Provider | [Download](https://dotnet.microsoft.com/download) |
| ODBC | [psqlODBC](https://odbc.postgresql.org/) | ODBC Driver | [Download](https://www.postgresql.org/ftp/odbc/releases/) |
| C | [libpq](https://www.postgresql.org/docs/current/libpq.html) | Primary C language interface | Included |
| C++ | [libpqxx](https://pqxx.org) | New-style C++ interface | [Download](https://pqxx.org/libpqxx/) |

## Related content

- [Quickstart: Use Python to connect and query data in Azure HorizonDB](connect-python.md)
- [Quickstart: Use Java and JDBC in Azure HorizonDB](connect-java.md)
- [Quickstart: Use .NET (C#) to connect and query data in Azure HorizonDB](connect-csharp.md)
- [Quickstart: Use Go language to connect and query data in Azure HorizonDB](connect-go.md)
- [Quickstart: Use PHP to connect and query data in Azure HorizonDB](connect-php.md)
- [Quickstart: Connect and query with Azure CLI in Azure HorizonDB](connect-azure-cli.md)
- [Quickstart: Import data in Power BI in Azure HorizonDB](../integration/connect-with-power-bi-desktop.md)
