---
title: Oracle to Azure Database for PostgreSQL flexible server schema conversion limitations
description: Known limitations, unsupported objects, and constraints when using the Oracle to Azure Database for PostgreSQL schema conversion feature in Visual Studio Code with Microsoft Foundry integration.
author: apduvuri
ms.author: adityaduvuri
ms.reviewer: maghan
ms.date: 06/02/2026
ai-usage: ai-assisted
ms.service: azure-database-postgresql
ms.topic: concept-article
ms.collection: ce-skilling-ai-copilot
ms.update-cycle: 180-days
---

# Oracle to Azure Database for PostgreSQL flexible server schema conversion limitations

This article summarizes the known limitations, unsupported objects, and migration considerations when you use the Oracle to Azure Database for PostgreSQL schema conversion feature in Visual Studio Code.

## Platform support limitations

- **ARM64**: Not supported on Windows or Linux.

## Unsupported schema objects

The schema conversion tool doesn't extract the following categories of Oracle objects from the source database. Because these objects aren't extracted, they don't appear in the schema conversion report. Recreate equivalent functionality on the Azure Database for PostgreSQL target manually, or replatform application-layer constructs to an appropriate Azure service.

Oracle system and built-in schemas aren't extracted or converted. This includes schemas such as `SYS`, `SYSTEM`, `XDB`, `MDSYS`, `CTXSYS`, and `WMSYS`.

> [!NOTE]
> Objects that the tool extracts but can't fully convert *are* added to the schema conversion report as **review tasks**. You can resolve those tasks manually or with GitHub Copilot agent mode assistance.

### Tables and indexes

- Index clusters, hash clusters, external tables, hybrid partitioned tables, and blockchain tables
- Bitmap indexes, bitmap join indexes, and global partitioned indexes
- User-defined index types, user-defined operators (`CREATE OPERATOR`), and XML schema–bound indexes

### Views and materialized views

- Flashback queries (`AS OF TIMESTAMP`, `AS OF SCN`)
- Editioning views
- Materialized view logs, refresh groups, and query rewrite behavior

### Triggers

- System event triggers (`LOGON`, `LOGOFF`, `STARTUP`, `SHUTDOWN`, `SERVERERROR`)
- Cross-edition triggers

### Java in the database

- Java stored procedures, sources, and classes
- External libraries (`CREATE LIBRARY`)

### Wrapped PL/SQL

PL/SQL units that are stored in wrapped (obfuscated) form by using the Oracle `wrap` utility or `DBMS_DDL.WRAP` can't be read by the tool, so they aren't extracted. Provide the original unwrapped source to convert these objects:

- Wrapped packages and package bodies
- Wrapped procedures and functions
- Wrapped type bodies

### Scheduler and jobs

The tool extracts only simple time-based jobs, which are mapped to `pg_cron`. Advanced `DBMS_SCHEDULER` features (file watchers, event-based jobs, programs, chains, job classes, credentials, windows, and groups) aren't extracted.

### Advanced Queuing

Oracle Advanced Queuing (AQ) carries application logic and requires application-layer redesign. Replatform AQ workloads to an appropriate Azure messaging service.

### Analytic and OLAP objects

- Analytic views, attribute dimensions, and hierarchies
- OLAP dimensions (`CREATE DIMENSION`)
- Oracle Data Mining models
- Materialized zone maps (`CREATE MATERIALIZED ZONEMAP`)

### Database links

- Private and public database links (`CREATE DATABASE LINK`, `CREATE PUBLIC DATABASE LINK`)

Database links store credentials and remote endpoint information that don't translate directly to PostgreSQL. Recreate them on the target by using a PostgreSQL foreign data wrapper such as `postgres_fdw` or `oracle_fdw`, or refactor to application-level connections.

### Storage and administration

- Application contexts (`CREATE CONTEXT`, `DBMS_SESSION.SET_CONTEXT`)
- Directory objects (`CREATE DIRECTORY`)
- Fine-grained auditing (FGA) and unified audit policies (`DBMS_FGA`, `AUDIT POLICY`)
- Information Lifecycle Management (ILM) policies
- Lockdown profiles
- Registered XML schemas (`DBMS_XMLSCHEMA.REGISTERSCHEMA`)
- Resource Manager objects (resource plans, consumer groups)
- SQL Translation profiles
- Workspace Manager (`DBMS_WM` workspaces and version-enabled tables)

## Get help

When you encounter limitations:

1. **Use GitHub Copilot agent mode** for guided assistance with review tasks.
1. **Consult PostgreSQL documentation** for alternative implementations.
1. **Review best practices** for Oracle to Azure Database for PostgreSQL migration patterns.
1. **Test in a scratch environment** before deploying to production.

## Related content

- [Oracle to Azure Database for PostgreSQL schema conversion overview](schema-conversions-overview.md)
- [Best practices for Oracle to Azure Database for PostgreSQL schema conversion](schema-conversions-best-practices.md)
