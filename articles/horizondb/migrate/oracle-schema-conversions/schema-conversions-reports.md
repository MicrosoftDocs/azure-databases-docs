---
title: "Oracle to PostgreSQL Schema Conversion: Reports in Azure HorizonDB"
description: Understanding the extraction and migration summary reports generated during Oracle to PostgreSQL schema conversion using Visual Studio Code PostgreSQL extension in Azure HorizonDB.
author: apduvuri
ms.author: adityaduvuri
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-database-postgresql
ms.topic: concept-article
---

# Oracle to Azure HorizonDB schema conversion migration generated reports Preview

The Oracle to Azure HorizonDB Schema Conversion feature generates two comprehensive reports during the migration process to help you validate and understand your schema conversion.

## Report types

The two reports complement each other: the extraction report documents what was discovered and any issues encountered during schema extraction, while the Migration Summary report captures conversion results, object mappings, and recommended next steps. Review both reports together to validate migration scope, identify objects that need manual attention, and plan deployment to PostgreSQL.

### Oracle extraction report

Generated during the initial Oracle database connection and schema extraction phase.

**Key Information**
- Oracle instance connection details and version
- Schema summary with object counts and success rates
- Object type breakdown (tables, procedures, functions, etc.)
- Processing time and any extraction errors

### Migration summary report

Generated after schema conversion completion, providing detailed conversion results.

**Key information**
- Migration statistics and success rates
- Object-by-object mapping from Oracle to PostgreSQL
- Data type transformation details
- Deployment instructions and file references
- Performance recommendations and known limitations

  :::image type="content" source="media/schema-conversion-reports/conversion-report.png" alt-text="Screenshot of conversion report.":::

## Use the report

Use the Extraction Report to validate migration scope and verify Oracle connectivity and Migration Summary Report to validate conversion results, plan deployment, and identify manual tasks.

**Best Practices**
- Review extraction results to ensure all expected objects are captured
- Validate object mappings align with application requirements
- Check data type conversions for compatibility
- Implement performance recommendations for optimal PostgreSQL results

  :::image type="content" source="media/schema-conversion-reports/extraction-report.png" alt-text="Screenshot of extraction report.":::

## Related content

- [What is Oracle to Azure HorizonDB schema conversion Preview?](schema-conversions-overview.md)
- [Tutorial: Oracle to Azure HorizonDB schema conversion Preview](schema-conversions-tutorial.md)
- [Oracle to Azure Database PostgreSQL schema conversion limitations Preview in Azure HorizonDB](schema-conversions-limitations.md)
