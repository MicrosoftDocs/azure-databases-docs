---
title: Oracle to PostgreSQL Schema Conversion - Limitations in Azure HorizonDB
description: Known limitations, unsupported objects, and constraints when using the Oracle to PostgreSQL schema conversion feature in Visual Studio Code with Azure OpenAI integration in Azure HorizonDB.
author: apduvuri
ms.author: adityaduvuri
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-database-postgresql
ms.topic: concept-article
ms.collection:
  - ce-skilling-ai-copilot
---

# Oracle to Azure Database PostgreSQL schema conversion limitations Preview in Azure HorizonDB

This preview summarizes known limitations, unsupported objects, and migration considerations when using the Oracle → PostgreSQL schema conversion feature in Visual Studio Code.

This article outlines the known limitations and constraints when using the Oracle to PostgreSQL schema conversion feature in Visual Studio Code.

## Platform support limitations

- **ARM64**: Currently **not supported** on Windows and Linux platforms

## Unsupported Oracle objects

The following Oracle database objects aren't automatically converted and are flagged as **Review Tasks** that require manual intervention:

### Schema objects

- Global temporary table
- Blockchain table
- Bitmap index
- Reverse key index
- Invisible index
- Global partitioned index
- Index on virtual column
- Oracle Text domain index
- Oracle Spatial domain index
- Sequence order
- Sequence no order
- DDL triggers with FOLLOWS, PRECEDES, or WHEN
- Autonomous transaction triggers
- System event triggers
- Hierarchical queries
- PIVOT and UNPIVOT operations
- Flashback queries
- Materialized view query rewrite
- REFRESH ON COMMIT MV
- REFRESH FAST MV

### Data types

- INVISIBLE data type

<a id="getting-help"></a>

## Get help

When you encounter limitations:

1. **Use GitHub Copilot Agent Mode** for guided assistance with review tasks.
1. **Consult PostgreSQL documentation** for alternative implementations.
1. **Review best practices** for Oracle to PostgreSQL migration patterns.
1. **Test in scratch environment** before deploying to production.

## Related content

- [What is Oracle to Azure HorizonDB schema conversion Preview?](schema-conversions-overview.md)
- [Best practices for converting Oracle schemas in Azure HorizonDB](schema-conversions-best-practices.md)
