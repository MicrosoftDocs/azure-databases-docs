---
title: "Oracle to PostgreSQL Schema Conversion: Best Practices"
description: "Best practices and recommendations for optimal Oracle to PostgreSQL schema conversion using Visual Studio Code PostgreSQL extension with Azure OpenAI integration."
author: apduvuri
ms.author: adityaduvuri
ms.reviewer: maghan
ms.date: 10/25/2025
ms.service: azure-database-postgresql
ms.subservice: schema-conversion
ms.topic: conceptual
ms.custom:
  - devx-track-vscode
  - schema-conversion
  - oracle-to-postgresql
  - best-practices
---

# Schema conversion: Best practices

This article provides best practices and recommendations to ensure optimal results when using the Oracle to PostgreSQL Schema Conversion feature in Visual Studio Code.

## Azure OpenAI token management

### Token limit requirements

- **Minimum token limit**: Ensure your Azure OpenAI deployment has a token limit greater than **500K** tokens for optimal performance.
- **Token usage**: Complex schema objects require significant token capacity for accurate conversion.

:::image type="content" source="media/bestpractices/token-per-minute.png" alt-text="Screenshot of token per minute settings.":::

### Project execution strategy

- **Single project execution**: Run only **one schema conversion project at a time** to ensure fair and efficient use of the Azure OpenAI token limit.
- **Sequential processing**: Avoid running multiple conversion projects simultaneously to prevent token exhaustion and conversion failures.

## Database configuration requirements

### Oracle database sessions

- **Sessions parameter**: Ensure the Oracle database sessions parameter value is **greater than 10**.
- **Verification query**: Use the following query to check the current sessions parameter value:

```sql
SELECT name, value
FROM v$parameter
WHERE name = 'sessions'
```

## Manual validation requirements

### Complex code objects

Manually validate the following complex Oracle code objects:

- **Stored Procedures**: Review the converted procedure logic, parameter handling, and exception management
- **Packages**: Validate the package structure and dependency resolution
- **Functions**: Verify the function return types, parameter mappings, and business logic accuracy

### Validation process

1. **Review AI-generated code**: Carefully examine all converted complex objects
1. **Test functionality**: Execute converted procedures and functions in your scratch DB environment
1. **Logic verification**: Ensure business logic remains intact after conversion

---
