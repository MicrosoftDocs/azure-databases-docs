---
title: "Oracle to PostgreSQL Application Conversion: Reports"
description: Understanding the summary reports generated during Oracle to PostgreSQL application conversion using Visual Studio Code PostgreSQL extension.
author: shriram-muthukrishnan
ms.author: shriramm
ms.reviewer: maghan
ms.date: 04/15/2026
ms.service: azure-database-postgresql
ms.topic: concept-article
ms.collection:
  - ce-skilling-ai-copilot
---

# Oracle to Azure Database for PostgreSQL application conversion generated reports (Preview)

The Oracle to Azure Database for PostgreSQL Application Conversion feature generates a comprehensive report during the conversion process to help you validate and understand your application code conversion.

## Quick start: review your report

**Accessing your report:**
- **Automatic display**: The report automatically opens in your VS Code editor as soon as the application conversion process finishes
- **Manual access**: You can also find the report at:
  - **Location**: `.github/postgres-migration/project_name/application_code/<code_base>-postgres/`
  - **Filename**: `application-migration-report.md`

**Quick assessment:**
1. **Check Executive Summary**: Look for "Total Files Processed" and "Successfully Converted" counts.
1. **Review file status and their counts**: "Files with Warnings" and "Files Requiring Manual Review" indicate complexity.
1. **Check Migration Status**: Look for the completion indicator.

**What success looks like**: Migration Status shows completion, most files converted cleanly, minimal warnings or manual review items

> **Next Steps**: Use your report results to guide your validation strategy from [Best practices for converting Oracle application code to Azure Database for PostgreSQL (Preview)](app-conversions-best-practices.md). Focus testing on flagged areas and files with warnings.

## Report overview

The Application Conversion Report documents what was converted, any issues encountered, and recommended next steps. Review the report to validate conversion scope, identify code that needs manual attention, and plan testing and deployment of converted application code.

### What's included in your report

Generated after application conversion completion, your report provides detailed results of the code transformation process with comprehensive before/after analysis, testing results, and recommendations for next steps.

### Report sections

The Code Conversion Report is comprehensive and typically includes the following sections:

#### Executive summary

- **Total Files Processed**: Count of all files analyzed
- **Successfully Converted**: Files converted without issues
- **Files with Warnings**: Files converted but flagged for review
- **Files Requiring Manual Review**: Files needing manual attention
- **Migration Status**: Overall completion indicator

#### Detailed analysis sections

- **Migration Overview**: Project details and target environment information
- **Directory Structure Comparison**: Before/after folder layouts
- **Files Converted**: Detailed table of all file conversion results
- **Database Schema Impact Analysis**: How schema changes affect application code
- **Conversion Details**: Specific code transformations with before/after examples
- **Testing Results**: Application startup and endpoint verification
- **Environment Configuration Changes**: Updated connection parameters and dependencies

#### Additional sections (when applicable)

- **Known Issues and Limitations**: Resolved issues and production considerations
- **Future Considerations**: Performance optimizations and enhancements
- **Migration Success Metrics**: Comparative analysis table
- **Appendix**: Summary of code changes and mappings

## Use the report

Use the Code Conversion Report to validate conversion results, plan testing, and identify areas requiring manual intervention.

### Best practices for report review

- **Start with Executive Summary**: Check Migration Status and calculate success rate (Success/Total files)
- **Review Files Converted table**: Focus on any files with warnings or requiring manual review
- **Check Database Schema Impact**: Understand how Oracle-specific features were converted
- **Review Conversion Details**: Examine before/after code examples for critical business logic
- **Verify Testing Results**: Ensure application startup and endpoint functionality
- **Plan next steps**: Use "Known Issues" and "Future Considerations" for deployment planning

> **For systematic validation**: Use the [Best practices for converting Oracle application code to Azure Database for PostgreSQL (Preview)](app-conversions-best-practices.md) validation frameworks to prioritize testing based on your file statuses and Oracle integration complexity.

### Understand conversion status

**Executive summary indicators:**

| Status | Description |
| --- | --- |
| **✅ COMPLETED SUCCESSFULLY** | Overall migration completed without blocking issues |
| **Files with Warnings: N** | N files converted but should be reviewed |
| **Files Requiring Manual Review: N** | N files need manual attention before deployment |

**Individual file status (in Files Converted section):**

| Status | Description |
| --- | --- |
| **✅ Completed** | File was successfully converted with no issues |
| **⚠️ Completed with Warnings** | File was converted but has areas that should be reviewed |
| **❌ Requires Manual Review** | File has sections that need manual attention |

> **Understanding what triggers manual review**: Files requiring manual review typically contain Oracle-specific features that can't be automatically converted. See [Oracle to Azure Database for PostgreSQL application conversion limitations (Preview)](app-conversions-limitations.md) to understand which Oracle constructs commonly require manual attention and how to assess their complexity.

## File comparison feature

In addition to the report, the Application Conversion feature provides built-in file comparison tools:

1. **Access file diff**: Right-click a converted file and select **Compare App Migration File Pairs**.
1. **Side-by-side view**: View original and converted files side by side.
1. **Highlight changes**: See specific lines and sections that were modified.
1. **Navigate differences**: Use navigation controls to move between changes.

### Use file comparison effectively

- Compare critical business logic files first
- Verify that Oracle-specific constructs were properly replaced
- Check that connection handling code is correct for PostgreSQL
- Validate SQL query transformations maintain intended behavior
- Review any inline comments added by the conversion process

> **Validation priorities**: Focus your file comparison efforts using the testing priorities from [Best practices for converting Oracle application code to Azure Database for PostgreSQL (Preview)](app-conversions-best-practices.md) - start with files flagged for manual review, then files with warnings, especially those containing database connections or complex queries.

## Integrate reports with your workflow

### For development teams

1. Share the conversion report with all team members working on migration.
1. Assign manual review tasks based on flagged issues.
1. Use the report as a checklist for code review sessions.
1. Track conversion progress across multiple application modules.

> **For teams new to PostgreSQL conversion**: Use the [What is Oracle to Azure Database for PostgreSQL application conversion (Preview)?](app-conversions-overview.md) to ensure all team members understand the conversion process and expected outcomes before diving into report details.

### For testing teams

1. Use the report to identify high-priority test areas.
1. Focus testing on files with warnings or flagged issues.
1. Create test cases based on transformation details.
1. Validate that SQL changes produce expected results.

### For project management

1. Use summary statistics to track overall progress.
1. Identify blockers from the issues section.
1. Plan resources for manual conversion tasks.
1. Report on migration status using conversion percentages.

## Related content

- [What is Oracle to Azure Database for PostgreSQL application conversion (Preview)?](app-conversions-overview.md)
- [Tutorial: Oracle to Azure Database for PostgreSQL application conversion (Preview)](app-conversions-tutorial.md)
- [Best practices for converting Oracle application code to Azure Database for PostgreSQL (Preview)](app-conversions-best-practices.md)
- [Oracle to Azure Database for PostgreSQL application conversion limitations (Preview)](app-conversions-limitations.md)
