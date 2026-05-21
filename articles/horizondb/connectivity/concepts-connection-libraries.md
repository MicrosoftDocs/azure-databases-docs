---
title: Connection Libraries in Azure HorizonDB
description: This article describes several libraries and drivers that you can use when coding applications to connect and query an Azure HorizonDB cluster.
author: scoriani
ms.author: scoriani
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-database-postgresql
ms.subservice: connectivity
ms.topic: concept-article
---

# Connection libraries in Azure HorizonDB

This article lists libraries and drivers that you can use to connect applications to and query an Azure HorizonDB cluster.

## Client interfaces

Most client libraries that connect to Azure HorizonDB are open-source projects, developed and released independently from Azure HorizonDB. You can use these libraries to establish secure connections, run SQL queries, and integrate your application with standard PostgreSQL-compatible tooling. Developers commonly use the libraries listed in this article on Windows, Linux, and macOS when connecting to an Azure HorizonDB cluster. If you want implementation examples, see the quickstart articles in the Related content section.

| **Language** | **Client interface** | **Additional information** | **Download** |
| --- | --- | --- | --- |
| Python | [psycopg](https://www.psycopg.org/) | DB API 2.0-compliant | [Download](https://pypi.org/project/psycopg/) |
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
