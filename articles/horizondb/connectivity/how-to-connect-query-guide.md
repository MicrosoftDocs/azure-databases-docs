---
title: Connect and query
description: Links to quickstarts showing how to connect to your Azure HorizonDB flexible server instance and run queries.
author: avnishrastogimsft
ms.author: avrastog
ms.reviewer: maghan
ms.date: 04/27/2024
ms.service: azure-database-postgresql
ms.subservice: connectivity
ms.topic: how-to
---

# Connect and query overview for Azure HorizonDB 

HorizonDB is Azure’s next‑generation PostgreSQL platform, designed to let developers securely connect to an Azure HorizonDB cluster and run standard PostgreSQL read and write queries without changing application code. Applications connect to a primary read‑write endpoint for transactional workloads and administrative operations, or to read‑only endpoints to scale read traffic across multiple readable replicas. HorizonDB is fully compatible with existing PostgreSQL clients, drivers, ORMs, and SQL syntax, allowing developers to integrate it into current applications with minimal or no code changes. This guide also includes TLS recommendations and extension that you can use to connect to the server in supported languages below.

## Quickstarts

| Quickstart | Description |
| --- | --- |
| [Pgadmin](https://www.pgadmin.org/) | You can use pgadmin to connect to the server and it simplifies the creation, maintenance and use of database objects. |
| [psql in Azure Cloud Shell](../configure-maintain/quickstart-create-server.md#connect-using-psql) | This article shows how to run [**psql**](https://www.postgresql.org/docs/current/static/app-psql.html) in [Azure Cloud Shell](/azure/cloud-shell/overview) to connect to your server and then run statements to query, insert, update, and delete data in the database. You can run **psql** if installed on your development environment. |
| [Python](connect-python.md) | This quickstart demonstrates how to use Python to connect to a database and use work with database objects to query data. |
| [Django with App Service](/azure/app-service/tutorial-python-postgresql-app) | This tutorial demonstrates how to use Ruby to create a program to connect to a database and use work with database objects to query data. |

## TLS considerations for database connectivity

Transport Layer Security (TLS) is used by all drivers that Microsoft supplies or supports for connecting to databases in your Azure HorizonDB. No special configuration is necessary but do enforce TLS 1.2 for newly created servers. We recommend if you are using TLS 1.0 and 1.1, then you update the TLS version for your servers. See [How to configure TLS](../security/security-tls-how-to-connect.md).

## PostgreSQL extensions

Azure HorizonDB provides the ability to extend the functionality of your database using extensions. Extensions bundle multiple related SQL objects together in a single package that can be loaded or removed from your database with a single command. After being loaded in the database, extensions function like built-in features.

## Related content

- [Extensions and modules](../extensions/concepts-extensions.md).
- [List of extensions and modules by name](../extensions/concepts-extensions-versions.md).
- [List of extensions by version of PostgreSQL](../extensions/concepts-extensions-by-engine.md).
