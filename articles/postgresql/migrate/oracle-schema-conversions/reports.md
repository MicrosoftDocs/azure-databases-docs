---
title: "Oracle to PostgreSQL Schema Conversion: Reports"
description: "Understanding the extraction and migration summary reports generated during Oracle to PostgreSQL schema conversion using VS Code PostgreSQL extension."
author: apduvuri
ms.author: adityaduvuri
ms.reviewer: maghan
ms.date: 10/24/2025
ms.service: azure-database-postgresql
ms.subservice: schema-conversion
ms.topic: conceptual
ms.custom:
  - devx-track-vscode
  - schema-conversion
  - oracle-to-postgresql
  - reports
---

# Schema Conversion: Reports

The Oracle to PostgreSQL Schema Conversion feature generates two comprehensive reports during the migration process to help you validate and understand your schema conversion.

## Report Types

### Oracle DDL Extraction Report

Generated during the initial Oracle database connection and schema extraction phase.

**Key Information:**
- Oracle instance connection details and version
- Schema summary with object counts and success rates
- Object type breakdown (tables, procedures, functions, etc.)
- Processing time and any extraction errors

### Migration Summary Report

Generated after schema conversion completion, providing detailed conversion results.

**Key Information:**
- Migration statistics and success rates
- Object-by-object mapping from Oracle to PostgreSQL
- Data type transformation details
- Deployment instructions and file references
- Performance recommendations and known limitations

## Report Locations

- **Extraction Report**: Generated during Oracle schema discovery
- **Migration Summary Report**: Saved in `/results/reports/migration_summary_report.md`

## Using the Reports

Use the Extraction Report to validate migration scope and verify Oracle connectivity and Migration Summary Report to validate conversion results, plan deployment, and identify manual tasks.

**Best Practices:**
- Review extraction results to ensure all expected objects are captured
- Validate object mappings align with application requirements  
- Check data type conversions for compatibility
- Implement performance recommendations for optimal PostgreSQL results

---