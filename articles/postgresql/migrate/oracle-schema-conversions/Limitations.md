---
title: "Oracle to PostgreSQL Schema Conversion - Limitations"
description: "Known limitations, unsupported objects, and constraints when using the Oracle to PostgreSQL schema conversion feature in VS Code with Azure OpenAI integration."
author: apduvuri
ms.author: adityaduvuri
ms.reviewer: maghan
ms.date: 10/17/2025
ms.service: azure-database-postgresql
ms.subservice: schema-conversion
ms.topic: reference
ms.custom:
  - devx-track-vscode
  - schema-conversion
  - oracle-to-postgresql
  - limitations
---

# Schema Conversion Limitations

This document outlines the known limitations and constraints when using the Oracle to PostgreSQL Schema Conversion feature in VS Code.

## Platform Support Limitations

- **ARM64**: Currently **not supported** on Windows and Linux platforms

## Unsupported Oracle Objects

The following Oracle database objects are **not automatically converted** and will be flagged as **Review Tasks** that require manual intervention:

### Schema Objects

- Global Temporary Table
- Blockchain Table
- Bitmap Index
- Reverse Key Index
- Invisible Index
- Global Partitioned Index
- Index on Virtual Column
- Oracle Text Domain Index
- Oracle Spatial Domain Index
- Sequence Order
- Sequence NoOrder
- DDL Triggers with FOLLOWS/PRECEDES/WHEN
- Autonomous Transaction Triggers
- System Event Triggers
- Hierarchical Queries
- PIVOT/UNPIVOT Operations
- Flashback Queries
- Materialized View Query Rewrite
- REFRESH ON COMMIT MV
- REFRESH FAST MV

### Data Types

- INVISIBLE DataType

## GitHub Copilot Limitations

- **Maximum Objects**: GitHub Copilot has a limitation of up to **100 objects** per conversion session
- **Batch Processing**: Large schemas may need to be processed in multiple batches
- **Complex Objects**: Highly complex objects may require multiple review iterations

## Getting Help

When encountering limitations:

1. **Use GitHub Copilot Agent Mode** for guided assistance with Review Tasks
2. **Consult PostgreSQL Documentation** for alternative implementations
3. **Review Best Practices** for Oracle to PostgreSQL migration patterns
4. **Test in Scratch Environment** before deploying to production

---
