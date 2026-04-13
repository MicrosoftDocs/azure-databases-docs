---
title: "Oracle to PostgreSQL Application Conversion: Best Practices"
description: "Best practices and recommendations for optimal Oracle to PostgreSQL application conversion using Visual Studio Code PostgreSQL extension."
author: shriram-muthukrishnan
ms.author: shriramm
ms.reviewer: maghan
ms.date: 04/13/2026
ms.service: azure-database-postgresql
ms.collection: ce-skilling-ai-copilot
ms.topic: concept-article
---

# Best practices for converting Oracle application code to Azure Database for PostgreSQL (Preview)

This article provides best practices and recommendations to ensure optimal results when using the Oracle to Azure Database for PostgreSQL application conversion feature in Visual Studio Code.

## Quick Start: Essential Practices

**Most Critical for Success**:
1. **Complete schema conversion first** (important for accurate conversions)
2. **Use Claude Sonnet 4.6 or Claude Opus 4.6 model** (or similar code-centric model such as GPT-5.2-Codex; as critical for high-quality conversion results)
3. **Connect to deployed PostgreSQL database** (provides accurate object context)
4. **Let agent complete TODO list without interruption** (ensures complete conversion)
5. **Test converted code thoroughly** (manual validation is essential)

## Assess Your Oracle Integration Level

All projects follow the same conversion process, but your Oracle integration level determines where to focus your preparation and validation efforts.

### **Standard Oracle Usage** 
**Your application primarily uses**:
- Standard JDBC/ODBC connections
- Basic SQL operations (SELECT, INSERT, UPDATE, DELETE)
- Common frameworks (Spring, Hibernate, Entity Framework)
- Standard data types (VARCHAR, INTEGER, DATE)

**Preparation emphasis**: Focus on schema conversion and AI model setup  
**Validation emphasis**: Automated testing and basic connectivity verification  
**Risk level**: Low - conversion typically succeeds with standard practices

### **Moderate Oracle Integration** *(Requires careful validation)*  
**Your application includes**:
- Some Oracle-specific SQL (CONNECT BY, PIVOT, outer join syntax)
- Basic PL/SQL procedure calls  
- Oracle data types (CLOB, BLOB, NUMBER with precision)
- Framework-specific Oracle configurations

**Preparation emphasis**: Thorough dependency identification and incremental conversion approach  
**Validation emphasis**: Manual review of converted SQL and extensive integration testing  
**Risk level**: Medium - expect some manual fixes and thorough testing required

### **Heavy Oracle Integration** *(Requires migration strategy)*
**Your application heavily uses**:
- Oracle-specific APIs (Advanced Queuing, Spatial, Text Search)
- Complex PL/SQL with business logic  
- Oracle system packages (DBMS_*, UTL_*)
- Oracle enterprise features (TAF, FCF, VPD)

**Preparation emphasis**: Review [Limitations document](app-conversions-limitations.md) for manual replacement strategies  
**Validation emphasis**: Architecture review and comprehensive testing strategy  
**Risk level**: High - significant manual work and potential architecture changes required

> **Important**: Regardless of integration level, all projects require thorough testing and validation before production deployment. The conversion tool accelerates migration but doesn't replace proper testing practices.

## Pre-conversion preparation

Proper preparation before starting application conversion significantly improves conversion accuracy and reduces manual intervention requirements.

### Complete schema conversion first

While not strictly required, completing schema conversion before application conversion provides significant benefits:

- **Coding Notes availability**: Schema conversion generates Coding Notes that provide context for application conversion
- **Database context**: The conversion tool can read your converted schema for accurate object references
- **Type mapping accuracy**: Application code conversions align with actual database type mappings
- **Reduced errors**: Fewer mismatches between application code and database objects

### Organize your codebase

- **Clean structure**: Organize files logically before importing into the migration project
- **Remove unnecessary files**: Exclude files that don't contain Oracle database dependencies
- **Backup originals**: Keep a complete backup of original source code before conversion
- **Version control**: Ensure your codebase is under version control before starting

## AI model configuration

Proper configuration of GitHub Copilot Agent Mode is critical for high-quality application conversion.

### Model selection requirements

- **Required model**: Claude Sonnet 4.6 or Claude Opus 4.6 or higher.
- **Verification**: Confirm model selection in GitHub Copilot chat interface before starting conversion
- **Consistency**: Use the same model throughout the conversion process

### Agent Mode optimization

- **Single conversion session**: Complete one application conversion project at a time
- **Avoid interruptions**: Let the agent complete its TODO list without interruption
- **Monitor progress**: Watch for any prompts or questions that require input

## Database context configuration

Proper database configuration ensures the conversion tool has accurate context for code transformation.

### PostgreSQL connection setup

Before running application conversion, ensure:

- Your Azure Database for PostgreSQL connection is configured in the PostgreSQL extension
- The connection is tested and working
- You have read access to the schema objects

### Database selection

When prompted to select a database during conversion:

- Choose the database where your converted DDL is deployed
- Ensure the selected database contains all referenced objects

### Connection privileges

The PostgreSQL account used for application conversion should have:

| Privilege | Purpose |
|-----------|---------|
| CONNECT | Connect to the database |
| SELECT on tables | Read schema and table information |
| SELECT on views | Access view definitions |
| USAGE on schemas | Access schema objects |

## Conversion execution best practices

Follow these practices during the conversion process for optimal results.

### Project structure

Maintain proper project structure:

```
.github/postgres-migration/project_name/
├── application_code/
│   └── your_codebase/
├── coding_notes/
└── reports/
```

### File organization

- **Logical grouping**: Organize files by module or feature
- **Clear naming**: Use descriptive folder names
- **Flat when possible**: Avoid deeply nested structures that complicate navigation

### Conversion monitoring

During conversion:

 - **Watch the TODO list**: Monitor as Agent Mode works through tasks
 - **Note any errors**: Document any errors or warnings that appear
 - **Don't interrupt**: Allow the process to complete fully
 - **Review incrementally**: Check converted files as they're completed

## Success Indicators

**You're on track if**:
- Conversion completes without errors
- Generated TODO list has clear sequence of items (typically around 10 items)
- Database connectivity works immediately
- Unit tests pass with minimal fixes
- No Oracle-specific import errors

**Red flags requiring attention**:
- Many Oracle-specific errors during conversion
- Connection failures after conversion
- Extensive manual code changes needed
- Performance degradation in converted queries

## Critical Validation Strategy

Although automated conversion accelerates migration, manual validation is essential to catch semantic differences, platform-specific behaviors, and edge cases that AI might miss.

### **High Priority** 

#### Database connectivity
- Verify connection string formats for PostgreSQL
- Test connection pooling configurations  
- Validate timeout and retry settings

#### SQL query conversions
- Review converted query syntax for correctness
- Test queries that use complex Oracle-specific features (CONNECT BY, PIVOT)
- Validate parameter binding and placeholder syntax

#### Data type handling
- Verify type conversions in application logic (NUMBER, DATE precision)
- Test date/time handling code (Oracle vs PostgreSQL differences)
- Validate numeric precision handling

### **Medium Priority**

#### Stored procedure calls
- Review procedure and function call syntax
- Validate parameter passing (REF CURSOR, OUT parameters)
- Test return value handling and exception management

#### Framework configurations
- Verify ORM dialect changes (Hibernate, Entity Framework)
- Test connection pool settings in application servers
- Validate transaction management configurations

### **Lower Priority**

#### Performance and optimization
- Query performance compared to Oracle
- Indexing strategy effectiveness
- Connection pool sizing

### Validation process

 - **Review conversion report**: Start with the generated report to identify flagged areas
 - **Use file comparison**: Leverage built-in diff tools to understand changes
 - **Unit testing**: Execute unit tests against converted code
 - **Integration testing**: Test with actual PostgreSQL database
 - **Performance testing**: Validate query performance meets requirements

## Common Mistakes to Avoid

### **Setup Issues** 
- **Using lower AI models**: Claude Sonnet 4.6 or Claude Opus 4.6 is required for better conversion quality
- **Skipping schema conversion**: Loses accuracy context and type mapping information  
- **Interrupting agent mid-process**: Causes incomplete conversion and missing files
- **Wrong database selection**: Pointing to empty database instead of deployed schema
- **Not reviewing Oracle feature compatibility**: Check [Limitations document](app-conversions-limitations.md) before starting if you use Oracle Advanced Queuing, Spatial, Text Search, or other specialized features that require architecture planning

### **Validation Issues** *(Prevent production problems)*
-  **Assuming all conversions are correct**: AI can miss semantic differences
-  **Skipping integration testing**: Unit tests alone don't catch PostgreSQL-specific issues
-  **Not validating date/time handling**: Oracle vs PostgreSQL date behavior differs significantly
-  **Ignoring performance testing**: Query performance patterns may change

### **Process Issues**
- **Converting without backups**: Always maintain original code separately
- **Large batch conversions**: Convert in smaller, manageable modules
- **Skipping team validation**: Have both Oracle and PostgreSQL experts review results

## Language-Specific Best Practices

### Java applications *(Focus: JDBC and framework configurations)*

**Critical areas to validate**:
- Review JDBC connection code for PostgreSQL driver usage
- Validate Hibernate/JPA configuration updates (dialect changes)
- Check Spring Data repository configurations  
- Test stored procedure annotations and parameter handling

**Common issues**: Connection pool configuration, transaction isolation levels, Oracle-specific annotations

### Python applications *(Focus: Driver conversion and ORM dialects)*

**Critical areas to validate**:
- Review cx_Oracle to psycopg2/asyncpg conversions
- Validate SQLAlchemy dialect configurations
- Check connection pool settings (different libraries)
- Test parameterized query syntax and type handling

**Common issues**: LOB handling differences, array binding syntax, async patterns

### .NET applications *(Focus: Provider changes and data access)*

**Critical areas to validate**:
- Review Oracle.DataAccess to Npgsql conversions
- Validate Entity Framework configuration (provider changes)
- Check stored procedure call syntax and return handling
- Test transaction handling code and isolation levels

**Common issues**: REF CURSOR handling, Oracle-specific transaction modes, data type mappings

### Node.js applications *(Focus: Async patterns and connection management)*

**Critical areas to validate**:
- Review oracledb to pg package conversions
- Validate connection pool configurations (different APIs)
- Check async/await patterns with PostgreSQL drivers
- Test query builder syntax if applicable (Sequelize, Knex)

**Common issues**: Object binding patterns, streaming differences, connection pool behavior

## Post-conversion best practices

### Testing strategy

Implement a comprehensive testing strategy:

 -  **Unit tests**: Run all existing unit tests against converted code
 - **Integration tests**: Test database interactions with PostgreSQL
 - **Regression tests**: Verify existing functionality is preserved
 - **Performance tests**: Validate query and application performance
 - **User acceptance testing**: Conduct UAT in a staging environment

### Code review process

Conduct thorough code reviews:

- Review all flagged files from the conversion report
- Have Oracle and PostgreSQL experts review critical sections
- Document any manual changes made post-conversion
- Update team documentation with conversion patterns

### Documentation updates

Update project documentation to reflect:

- New database connection requirements
- Changed configuration settings
- Modified deployment procedures
- PostgreSQL-specific operational considerations

## Related content

- [Oracle to PostgreSQL Application Conversion Overview](app-conversions-overview.md)
- [Oracle to PostgreSQL Application Conversion Tutorial](app-conversions-tutorial.md)
- [Oracle to PostgreSQL Application Conversion Reports](app-conversions-reports.md)
- [Oracle to PostgreSQL Application Conversion Limitations](app-conversions-limitations.md)
