---
title: "Oracle to PostgreSQL Schema Conversion: Best Practices"
description: "Best practices and recommendations for optimal Oracle to PostgreSQL schema conversion using VS Code PostgreSQL extension with Azure OpenAI integration."
author: apduvuri
ms.author: adityaduvuri
ms.reviewer: maghan
ms.date: 10/23/2025
ms.service: azure-database-postgresql
ms.subservice: schema-conversion
ms.topic: conceptual
ms.custom:
  - devx-track-vscode
  - schema-conversion
  - oracle-to-postgresql
  - best-practices
---

# Schema Conversion: Best Practices

This document provides best practices and recommendations to ensure optimal results when using the Oracle to PostgreSQL Schema Conversion feature in VS Code.

## Azure OpenAI Token Management

### Token Limit Requirements
- **Minimum Token Limit**: Ensure your Azure OpenAI deployment has a token limit greater than **500K** tokens for optimal performance
- **Token Usage**: Complex schema objects require significant token capacity for accurate conversion

:::image type="content" source="Images/bestpractices/tokenperminute.png" alt-text="Screenshot of Schema Conversion token per minute setting":::

### Project Execution Strategy
- **Single Project Execution**: Run only **one schema conversion project at a time** to ensure fair and efficient use of the Azure OpenAI token limit
- **Sequential Processing**: Avoid running multiple conversion projects simultaneously to prevent token exhaustion and conversion failures

## Database Configuration Requirements

### Oracle Database Sessions
- **Sessions Parameter**: Ensure the Oracle database sessions parameter value is **greater than 10**
- **Verification Query**: Use the following query to check the current sessions parameter value:

```sql
SELECT name, value
FROM v$parameter
WHERE name = 'sessions'
```

## Manual Validation Requirements

### Complex Code Objects
Manual validation is **recommended** for the following complex Oracle code objects:

- **Stored Procedures**: Review converted procedure logic, parameter handling, and exception management
- **Packages**: Validate package structure, and dependency resolution
- **Functions**: Verify function return types, parameter mappings, and business logic accuracy

### Validation Process
1. **Review AI-Generated Code**: Carefully examine all converted complex objects
2. **Test Functionality**: Execute converted procedures and functions in your Scratch DB environment
3. **Logic Verification**: Ensure business logic remains intact after conversion

---
