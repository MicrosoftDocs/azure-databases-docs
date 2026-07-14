---
title: Connect and Query Overview in Azure Database for PostgreSQL Flexible Server
description: Links to quickstarts showing how to connect to your Azure Database for PostgreSQL flexible server and run queries.
#customer intent: As a user, I want to connect to my Azure Database for PostgreSQL flexible server, so that I can run queries against my data.
author: gbowerman
ms.author: guybo
ms.reviewer: maghan
ms.date: 07/08/2026
ms.service: azure-database-postgresql
ms.subservice: connectivity
ms.topic: how-to
ai-usage: ai-assisted
---

# Connect and query overview in Azure Database for PostgreSQL flexible server

This article includes links to examples that show how to connect and query with Azure Database for PostgreSQL. It also includes TLS recommendations and extensions that you can use to connect to the server in supported languages.

## Quickstarts

| Quickstart | Description |
| --- | --- |
| [Pgadmin](https://www.pgadmin.org/) | Use pgadmin to connect to the server. It simplifies the creation, maintenance, and use of database objects. |
| [psql in Azure Cloud Shell](../configure-maintain/quickstart-create-server.md#connect-by-using-psql) | This article shows how to run [**psql**](https://www.postgresql.org/docs/current/static/app-psql.html) in [Azure Cloud Shell](/azure/cloud-shell/overview) to connect to your server and then run statements to query, insert, update, and delete data in the database. You can run **psql** if installed on your development environment. |
| [Python](connect-python.md) | This quickstart demonstrates how to use Python to connect to a database and work with database objects to query data. |
| [Django with App Service](/azure/app-service/tutorial-python-postgresql-app) | This tutorial demonstrates how to use Ruby to create a program to connect to a database and work with database objects to query data. |

## TLS considerations for database connectivity

All drivers that Microsoft supplies or supports for connecting to databases in your Azure Database for PostgreSQL flexible servers use Transport Layer Security (TLS). No special configuration is necessary, but enforce TLS 1.2 for newly created servers. If you're using TLS 1.0 or 1.1, update the TLS version for your servers. See [How to configure TLS](../security/security-tls-how-to-connect.md).

## PostgreSQL extensions

Azure Database for PostgreSQL provides the ability to extend the functionality of your database by using extensions. Extensions bundle multiple related SQL objects together in a single package that you can load or remove from your database by using a single command. After being loaded in the database, extensions function like built-in features.

## Related content

- [Extensions and modules](../extensions/concepts-extensions.md).
- [List of extensions and modules by name](../extensions/concepts-extensions-versions.md).
- [List of extensions by version of PostgreSQL](../extensions/concepts-extensions-by-engine.md).
