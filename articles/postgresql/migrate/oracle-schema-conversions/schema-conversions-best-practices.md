---
title: "Oracle to PostgreSQL Schema Conversion: Best Practices"
description: "Best practices and recommendations for optimal Oracle to PostgreSQL schema conversion using Visual Studio Code PostgreSQL extension with Azure OpenAI integration."
author: apduvuri
ms.author: adityaduvuri
ms.reviewer: maghan
ms.date: 11/18/2025
ms.service: azure-database-postgresql
ms.collection: ce-skilling-ai-copilot
ms.topic: concept-article
---

# Best practices for converting Oracle schemas to Azure Database for PostgreSQL Preview

This article provides best practices and recommendations to ensure optimal results when using the Oracle to Azure Database for PostgreSQL schema conversion feature in Visual Studio Code.

## Azure OpenAI token management

Proper management of Azure OpenAI tokens is critical to ensure reliable, performant schema conversions, especially for large, or complex Oracle schemas. Provision sufficient token capacity, monitor usage, and apply rate controls to prevent interruptions and unexpected costs.

### Token limit requirements

- **Minimum token limit**: Ensure your Azure OpenAI deployment has a token limit greater than **500K** tokens for optimal performance.
- **Token usage**: Complex schema objects require significant token capacity for accurate conversion.

:::image type="content" source="media/schema-conversions-best-practices/token-per-minute.png" alt-text="Screenshot of token per minute settings.":::

### Project execution strategy

- **Single project execution**: Run only **one schema conversion project at a time** to ensure fair and efficient use of the Azure OpenAI token limit.
- **Sequential processing**: Avoid running multiple conversion projects simultaneously to prevent token exhaustion and conversion failures.

## Database configuration requirements

Before running conversions, ensure both the source (Oracle) and target (PostgreSQL) databases are configured and tuned to support the converted schema and expected workload. Check settings such as memory allocation, connection limits, character sets, timezone, and required extensions to prevent runtime issues and semantic mismatches during migration.

### Oracle database sessions

- **Sessions parameter**: Ensure the Oracle database sessions parameter value is **greater than 10**.
- **Verification query**: Use the following query to check the current sessions parameter value:

```sql
SELECT name, value
FROM v$parameter
WHERE name = 'sessions'
```

## Manual validation requirements

Although automated conversion accelerates migration, manual validation is essential to catch semantic differences, platform-specific behaviors, and edge cases that AI or tooling might miss. Perform focused reviews and testing of converted objects to verify correctness, performance, and maintainability in the PostgreSQL environment.

### Complex code objects

Manually validate the following complex Oracle code objects:

- **Stored Procedures**: Review the converted procedure logic, parameter handling, and exception management
- **Packages**: Validate the package structure and dependency resolution
- **Functions**: Verify the function return types, parameter mappings, and business logic accuracy

### Validation process

1. **Review AI-generated code**: Carefully examine all converted complex objects
1. **Test functionality**: Execute converted procedures and functions in your scratch database environment
1. **Logic verification**: Ensure business logic remains intact after conversion

## Related content

- [Oracle to PostgreSQL Migration Overview](schema-conversions-overview.md)
- [Oracle to PostgreSQL Migration Tutorial](schema-conversions-tutorial.md)
