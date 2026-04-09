---
title: Connection types and connectors overview
description: Learn about the different connection types, drivers, and connectors available for connecting to and querying an Azure HorizonDB cluster.
author: avnishrastogimsft
ms.author: avrastog
ms.reviewer: maghan
ms.date: 04/08/2026
ms.service: azure-database-postgresql
ms.subservice: connectivity
ms.topic: overview
ai-usage: ai-assisted
---

# Connection types and connectors for Azure HorizonDB

Azure HorizonDB is a fully managed PostgreSQL-compatible database service that supports standard PostgreSQL connection protocols and drivers. You can connect to an Azure HorizonDB cluster using existing PostgreSQL clients, ORMs, and SQL syntax without changing your application code.

This article provides an overview of the connection types, client drivers, and tools available for connecting to and querying your Azure HorizonDB cluster.

## Connection endpoints

Azure HorizonDB provides two types of connection endpoints for your cluster:

- **Primary read-write endpoint**: Use this endpoint for transactional workloads, administrative operations, and all write queries. Applications connect to the primary endpoint on port **5432** by default.
- **Read-only endpoints**: Use these endpoints to scale read traffic across multiple readable replicas. Read-only endpoints offload read queries from the primary node, improving overall cluster performance.

## Connection methods

You can connect to Azure HorizonDB using several methods:

| Method | Description |
| --- | --- |
| **psql** | The standard PostgreSQL command-line terminal. Use psql locally or through [Azure Cloud Shell](/azure/cloud-shell/overview) to connect and run queries interactively. |
| **pgAdmin** | A popular open-source GUI tool for managing PostgreSQL databases. Use [pgAdmin](https://www.pgadmin.org/) to connect to your cluster and manage database objects visually. |
| **Azure CLI** | Use the [Azure CLI](connect-azure-cli.md) to connect and query your Azure HorizonDB cluster directly from the command line. |
| **VS Code extension** | The [PostgreSQL extension for Visual Studio Code](../development/vs-code-extension/vs-code-overview.md) allows you to connect, query, and manage your Azure HorizonDB cluster from within VS Code. |
| **Application drivers** | Connect from your application code using language-specific PostgreSQL drivers. See [Client libraries and drivers](#client-libraries-and-drivers). |

## Client libraries and drivers

Azure HorizonDB supports all standard PostgreSQL client libraries and drivers. The following table lists commonly used drivers for each language:

| Language | Client interface | More information | Download |
| --- | --- | --- | --- |
| Python | [psycopg](https://www.psycopg.org/) | DB API 2.0-compliant | [Download](https://pypi.org/project/psycopg2/) |
| PHP | [php-pgsql](https://secure.php.net/manual/en/book.pgsql.php) | Database extension | [Install](https://secure.php.net/manual/en/pgsql.installation.php) |
| Node.js | [pg npm package](https://www.npmjs.com/package/pg) | Pure JavaScript nonblocking client | [Install](https://www.npmjs.com/package/pg) |
| Java | [JDBC](https://jdbc.postgresql.org/) | Type 4 JDBC driver | [Download](https://jdbc.postgresql.org/download/) |
| Ruby | [pg gem](https://rubygems.org/gems/pg) | Ruby interface | [Download](https://rubygems.org/downloads/pg-0.20.0.gem) |
| Go | [pq package](https://godoc.org/github.com/lib/pq) | Pure Go PostgreSQL driver | [Install](https://github.com/lib/pq/blob/master/README.md) |
| C\#/.NET | [Npgsql](https://www.npgsql.org/) | ADO.NET data provider | [Download](https://dotnet.microsoft.com/download) |
| ODBC | [psqlODBC](https://odbc.postgresql.org/) | ODBC driver | [Download](https://www.postgresql.org/ftp/odbc/releases/) |
| C | [libpq](https://www.postgresql.org/docs/current/static/libpq.html) | Primary C language interface | Included |
| C++ | [libpqxx](http://pqxx.org/) | C++ interface | [Download](https://pqxx.org/libpqxx/) |

## Connection pooling

For production workloads, use connection pooling to reduce connection overhead and improve performance. Azure HorizonDB offers [PgBouncer](concepts-pgbouncer.md) as a built-in connection pooling solution. PgBouncer runs on the same virtual machine as your database server and supports both public and private connections.

Key benefits of using PgBouncer:

- Reduces the overhead of creating new connections for each operation.
- Scales to up to 10,000 connections with low overhead.
- Supports [Microsoft Entra authentication](../security/security-entra-concepts.md).
- Seamlessly restarts on failover to a standby server.

For guidance on selecting the right pooling strategy, see [Connection pooling best practices](concepts-connection-pooling-best-practices.md).

## Transport Layer Security (TLS)

All connections to Azure HorizonDB use Transport Layer Security (TLS) to encrypt data in transit. TLS 1.2 is enforced for newly created clusters. If your applications use TLS 1.0 or 1.1, update the TLS version for your cluster.

For detailed configuration steps, see [Connect clients with TLS](../security/security-tls-how-to-connect.md).

## Authentication

Azure HorizonDB supports multiple authentication methods:

- **Microsoft Entra authentication**: Use Microsoft Entra ID (formerly Azure Active Directory) for centralized identity management and passwordless authentication. For details, see [Microsoft Entra authentication](../security/security-entra-concepts.md).
- **SCRAM authentication**: Use Salted Challenge Response Authentication Mechanism (SCRAM) for local database users with password-based authentication. For details, see [Connect with SCRAM authentication](../security/security-connect-scram.md).
- **Managed identity**: Connect applications using Azure managed identities to eliminate the need for credentials in application code. For details, see [Connect applications with a managed identity](../security/security-connect-with-managed-identity.md).

## Language quickstarts

Use these quickstarts to connect to and query your Azure HorizonDB cluster:

| Language | Quickstart |
| --- | --- |
| Python | [Connect and query with Python](connect-python.md) |
| Java | [Connect and query with Java](connect-java.md) |
| C\#/.NET | [Connect and query with .NET](connect-csharp.md) |
| Go | [Connect and query with Go](connect-go.md) |
| PHP | [Connect and query with PHP](connect-php.md) |
| Azure CLI | [Connect and query with Azure CLI](connect-azure-cli.md) |

## Related content

- [Connection libraries for Azure HorizonDB](concepts-connection-libraries.md)
- [PgBouncer in Azure HorizonDB](concepts-pgbouncer.md)
- [Connection pooling best practices](concepts-connection-pooling-best-practices.md)
- [Secure Connectivity with SSL and TLS](../security/security-tls.md)
- [PostgreSQL extension for Visual Studio Code](../development/vs-code-extension/vs-code-overview.md)
