# Oracle to Azure Database for PostgreSQL application conversion limitations (Preview)

This article outlines the known limitations and constraints when using the Oracle to PostgreSQL application conversion feature in Visual Studio Code.

## Overview & Quick Assessment

The Oracle to PostgreSQL application conversion feature successfully handles the majority of common database application patterns automatically. However, some Oracle-specific features and advanced functionality require manual intervention during or after the automated conversion process.

**What works well automatically:**
- Standard database connectivity (JDBC, ODBC, basic drivers)
- Common SQL operations (SELECT, INSERT, UPDATE, DELETE, basic JOINs)
- Popular frameworks (Spring Boot, Hibernate, Entity Framework, Django ORM)
- Standard data types and basic stored procedure calls
- Typical transaction management patterns

**What requires attention:**
- Oracle-specific APIs and packages (DBMS_*, UTL_*, etc.) 
- Advanced PL/SQL integration
- Specialized Oracle features (Advanced Queuing, Spatial, Text Search)
- Custom connection pooling configurations
- Oracle-proprietary data types

**Bottom line:** Most business applications that use Oracle as a standard relational database will convert successfully with minimal manual work. Applications heavily integrated with Oracle-specific features will require more planning and manual intervention.

## Quick Impact Check

Use this checklist to assess the likely conversion complexity for your application:

### **Low Impact - Proceed with Confidence**

Your application will likely convert smoothly if it primarily uses:

- **Standard database drivers**: JDBC, ODBC, or language-standard database libraries
- **Basic SQL patterns**: Standard SELECT, INSERT, UPDATE, DELETE operations
- **Common frameworks**: Spring Boot, Hibernate, Entity Framework, SQLAlchemy, Sequelize
- **Standard data types**: VARCHAR, INTEGER, DATE, TIMESTAMP, DECIMAL
- **Simple stored procedures**: Basic parameter passing and result handling
- **Standard connection patterns**: Connection strings, basic pooling, standard transactions

### **Medium Impact - Plan for Manual Work**

Your application will need some manual attention if it includes:

- **Oracle-specific SQL**: CONNECT BY, PIVOT/UNPIVOT, Oracle outer join syntax (+)
- **PL/SQL integration**: Custom functions, procedures with Oracle-specific logic
- **Oracle data types**: CLOB, BLOB, NUMBER with specific precision, Oracle dates
- **Advanced framework features**: Oracle-specific ORM configurations, custom dialects
- **Connection complexity**: TNS names, Oracle Wallet, advanced pooling configurations
- **Basic Oracle packages**: Limited use of DBMS_OUTPUT, simple UTL_FILE operations

### **High Impact - Significant Migration Effort Required**

Your application will require substantial manual work if it heavily uses:

- **Oracle Advanced Queuing (AQ)**: Message queuing and notifications
- **Oracle Spatial/GIS**: Geospatial data types and spatial queries  
- **Oracle Text Search**: Full-text indexing and search APIs
- **Oracle Streams**: Data replication and change capture
- **Complex PL/SQL**: Heavy business logic in database procedures/packages
- **Oracle XML DB**: XML storage, indexing, and specialized XML functions
- **Oracle-specific security**: Advanced authentication, proxy authentication, VPD

## AI model requirements

- **Model requirement**: Claude Sonnet 4.6 or Claude Opus 4.6 is required for optimal conversion results
- **Lower models**: Using models below Claude Sonnet 4 may produce less accurate or incomplete conversions
- **Token limits**: Very large codebases may require multiple conversion sessions

## Schema conversion dependency

While not strictly required, the following limitations apply when schema conversion is not performed first:

- **Reduced accuracy**: Conversion accuracy may be lower without Coding Notes context
- **Missing type mappings**: Data type conversions may not align with actual database schema
- **Object reference issues**: Application code may reference objects that don't exist in PostgreSQL format

## Common Application Limitations

### **What Gets Converted Automatically**

The application conversion tool handles these common patterns without manual intervention:

- **Database driver imports and usage patterns**: Automatic conversion from Oracle drivers (ojdbc, cx_Oracle, ODP.NET, node-oracledb) to PostgreSQL equivalents
- **Basic SQL syntax differences**: Oracle outer joins (+), date functions (SYSDATE → NOW()), string operations, DUAL table references
- **Framework dialect configurations in code**: Hibernate Oracle dialect → PostgreSQL, Entity Framework providers, SQLAlchemy dialects
- **Standard connection patterns and basic pooling**: Connection string formats, basic pooling configurations
- **Common ORM annotations and configurations**: Framework-specific Oracle configurations converted to PostgreSQL equivalents
- **Standard data type usage in application logic**: VARCHAR, INTEGER, DATE, TIMESTAMP, DECIMAL handling

### **What May Need Manual Review** *(Moderate frequency)*

These patterns often convert but may require verification or adjustment:

#### **Complex SQL patterns**
- **CONNECT BY hierarchical queries**: Require PostgreSQL recursive CTEs
- **PIVOT/UNPIVOT operations**: Require PostgreSQL crosstab or manual rewrite
- **MODEL clause**: No direct PostgreSQL equivalent
- **MERGE statement variations**: May require PostgreSQL INSERT ON CONFLICT syntax

#### **Advanced PL/SQL integration**
- **Complex procedure calls**: Advanced parameter handling, REF CURSORs
- **Oracle-specific transaction modes**: Isolation levels, autonomous transactions
- **Exception handling patterns**: Oracle-specific exception types

#### **Specialized data types**
- **LONG and LONG RAW**: Deprecated types requiring special handling
- **Oracle Object types**: Complex object types may need restructuring
- **VARRAY and nested tables**: Require PostgreSQL array handling
- **BFILE**: No direct PostgreSQL equivalent

### **What Requires Manual Replacement** *(Specialized Oracle features)*

These Oracle-specific features have no direct PostgreSQL equivalent:

#### **Oracle-specific APIs**
- **Oracle Advanced Queuing (AQ)**: Requires complete messaging architecture replacement
- **Oracle Streams**: No direct PostgreSQL equivalent for data replication
- **Oracle Spatial APIs**: Requires PostGIS integration and manual conversion
- **Oracle Text search APIs**: Requires PostgreSQL full-text search implementation
- **Oracle XMLDB functions**: May require manual PostgreSQL XML function mapping

#### **Oracle system packages**
- **DBMS_OUTPUT calls**: Require manual replacement or removal
- **DBMS_SCHEDULER references**: Need PostgreSQL pg_cron or alternative job scheduling
- **UTL_FILE operations**: Require PostgreSQL-specific file handling approaches
- **DBMS_LOCK usage**: Requires PostgreSQL advisory locks

#### **Enterprise Oracle features**
- **Oracle Transparent Application Failover (TAF)**: Requires alternative high-availability approach
- **Oracle Fast Connection Failover (FCF)**: No direct PostgreSQL equivalent
- **Oracle proxy authentication**: Requires alternative authentication approach
- **Flashback queries**: No time-travel query equivalent

### 🔧 **External Configuration** *(Outside application codebase)*

These items are outside the scope of application code conversion:

- **Infrastructure configurations**: Docker files, deployment scripts with Oracle dependencies
- **Environment configurations**: TNS names files, Oracle Wallet files, server connection pools
- **CI/CD pipeline configurations**: Build scripts referencing Oracle dependencies
- **Database connection pools**: Application server (Tomcat, IIS) connection pool configurations

## Language-specific limitations

 **Note**: Standard driver imports and basic usage patterns convert automatically. The limitations below apply to advanced features and specialized APIs that may require manual attention.

### Java limitations

- **Oracle JDBC extensions**: Custom Oracle JDBC features may not convert automatically
- **Oracle UCP (Universal Connection Pool)**: Requires HikariCP or other PostgreSQL-compatible pool
- **Oracle-specific annotations**: May require manual updates

### Python limitations

- **cx_Oracle-specific features**: Some advanced features have no psycopg2 equivalent
- **Oracle LOB handling**: Large object handling differs in PostgreSQL
- **Array binding syntax**: Differs between Oracle and PostgreSQL drivers

### .NET limitations

- **ODP.NET managed driver features**: Some features don't map to Npgsql
- **Oracle-specific transaction modes**: May require adjustment
- **REF CURSOR handling**: Differs between providers

### Node.js limitations

- **oracledb advanced features**: Some pooling and streaming features differ
- **Oracle object type bindings**: Require manual conversion to PostgreSQL

## Infrastructure and deployment considerations

> **Note**: These items are outside the scope of application code conversion and require separate infrastructure updates.

### Connection configuration files
- **TNS names files**: Oracle tnsnames.ora files need PostgreSQL host/port/database equivalents
- **Oracle Wallet configurations**: SSL/authentication files require PostgreSQL certificate setup
- **Connection pool configurations**: Application server pools (WebLogic, Tomcat) need PostgreSQL driver setup

### Deployment artifacts
- **Build scripts**: Maven/Gradle dependencies need PostgreSQL driver updates
- **Docker configurations**: Base images and driver installations need updates  
- **CI/CD pipelines**: Database connection tests and deployment scripts need updates

## Large codebase considerations

For very large codebases:

- **Conversion time**: Large projects may take significant time to process
- **Memory usage**: Very large files may require more system resources
- **Incremental approach**: Consider converting in logical modules rather than entire codebase at once
- **Token limits**: AI model token limits may affect very large individual files

## Getting help

When you encounter limitations:

1. **Use GitHub Copilot Agent Mode**: Request additional assistance for manual conversion tasks
2. **Consult PostgreSQL documentation**: Find alternative implementations for Oracle-specific features
3. **Review best practices**: See the best practices guide for Oracle to PostgreSQL migration patterns
4. **Test thoroughly**: Validate all converted code in a nonproduction environment before deployment
5. **File feedback**: Report issues using the built-in feedback tool with `Application Conversion:` prefix

### Reporting issues

1. Open the Command Palette with `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (macOS)
2. Run the command: **PGSQL: Report Issue**
3. Include `Application Conversion:` as a prefix in your issue title
4. Provide details about the specific limitation or issue encountered

## Related content

- [Oracle to PostgreSQL Application Conversion Overview](app-conversions-overview.md)
- [Oracle to PostgreSQL Application Conversion Tutorial](app-conversions-tutorial.md)
- [Oracle to PostgreSQL Application Conversion Best Practices](app-conversions-best-practices.md)
- [Oracle to PostgreSQL Schema Conversion Limitations](https://learn.microsoft.com/en-us/azure/postgresql/migrate/oracle-schema-conversions/schema-conversions-limitations)
