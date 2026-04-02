---
title: What Is Oracle to PostgreSQL Schema Conversion?
description: Learn how to convert Oracle database schemas to PostgreSQL using the Visual Studio Code PostgreSQL extension with AI-powered transformation, Azure OpenAI integration, and intelligent review tasks for seamless migration to Azure Database for PostgreSQL flexible server.
author: apduvuri
ms.author: adityaduvuri
ms.reviewer: maghan
ms.date: 11/18/2025
ms.service: azure-database-postgresql
ms.topic: overview
ms.collection: ce-skilling-ai-copilot
---

# What is Oracle to Azure Database for PostgreSQL schema conversion Preview?

The Oracle to Azure Database for PostgreSQL schema conversion feature in the Visual Studio Code PostgreSQL extension helps you convert your existing Oracle database schema objects into PostgreSQL-compatible schema. This functionality is designed for relational schemas and ensures that the converted schema works seamlessly with Azure Database for PostgreSQL flexible server.

The tool provides a project-based user interface to automate schema conversion. If certain objects can't be converted automatically, the tool flags them as Review Tasks, which you can resolve manually by using GitHub Copilot Agents.

:::image type="content" source="media/schema-conversions-overview/schema-conversion.png" alt-text="Diagram of schema conversion.":::

## Architecture

The schema conversion process involves multiple components working together:

- **Source Oracle Database**: Your existing Oracle database containing the schema to convert
- **Visual Studio Code PostgreSQL Extension**: The primary interface for managing the conversion process
- **Azure Database for PostgreSQL flexible server**: Used as the scratch database for validation and testing
- **Azure OpenAI**: Provides intelligent transformation capabilities for complex schema objects
- **Schema Conversion Agents**: AI-powered agents that handle the automated conversion process

## How it works

The schema conversion process uses an intelligent, multistage approach that combines automated transformation with human oversight:

- **Connection and Discovery**: The tool connects to your Oracle database and catalogs all schema objects. It analyzes their structure, dependencies, and complexity to create a conversion plan.
- **AI-Powered Transformation**: Schema Conversion Agents use Azure OpenAI to intelligently transform Oracle-specific constructs into PostgreSQL-compatible equivalents. The AI understands context, relationships, and best practices for both database platforms.
- **Validation in Scratch Environment**: The tool tests all converted objects in the Azure Database for PostgreSQL database (scratch database) environment. This step ensures syntax correctness and compatibility before final output generation.
- **Review Task Generation**: The tool flags objects that can't be fully automated or require human judgment as Review Tasks. These objects might include complex business logic or Oracle-specific features that need manual attention.
- **Guided Resolution**: GitHub Copilot Agent Mode provides intelligent assistance for completing Review Tasks. It offers context-aware suggestions and Azure Database for PostgreSQL flexible server best practices to help you make informed decisions.
- **Output Generation**: The tool converts successfully validated objects into organized PostgreSQL `.sql` files, ready for deployment to your target environment.

## Install the extension

The Oracle to PostgreSQL Schema Conversion functionality is built into the **PostgreSQL extension** for Visual Studio Code. You don't need a separate extension - it's included as a comprehensive feature within the main PostgreSQL extension.

### Installation steps

1. **Open Extensions Marketplace**: In Visual Studio Code, select the Extensions icon in the Activity Bar on the left side, or use the keyboard shortcut `Ctrl+Shift+X` (Windows/Linux) or `Cmd+Shift+X` (macOS).
1. **Search for PostgreSQL**: In the Extensions Marketplace search box, type "PostgreSQL" to find the extension.
1. **Install the Extension**: Locate the PostgreSQL extension in the search results and select **Install**.
1. **Access Schema Conversion**: When the extension is installed, you see an elephant icon in the Visual Studio Code sidebar representing the PostgreSQL extension. You can access the Schema Conversion feature through this extension interface.

## Schema conversion workflow

This section explains the core concepts used throughout the Oracle to PostgreSQL schema conversion workflow - including conversion units (schemas, tables, indexes, views, and procedures), review tasks for human oversight, scratch database validation, AI-powered schema conversion agents, and the resulting PostgreSQL SQL artifacts. Understanding these concepts helps you interpret conversion results, prioritize and resolve flagged items, and prepare converted files for deployment to Azure Database for PostgreSQL flexible server.

### Scratch database

An Azure Database for PostgreSQL flexible server that you use during conversion for validation purposes to ensure compatibility. This approach ensures that:
- Converted objects are syntactically correct
- Dependencies are properly resolved
- Performance characteristics are maintained
- Azure-specific features are applied appropriately

### Review tasks

The tool flags items for manual review when the AI can't fully convert an object or recommends a second look. Common review tasks include:
- Complex PL/SQL procedures that need manual optimization
- Oracle-specific data types with multiple PostgreSQL alternatives
- Custom functions with Oracle-specific logic

### GitHub Copilot agent mode

An integrated feature in Visual Studio Code that provides guided prompts to help you complete review tasks and align schema with your application requirements. The agent mode offers:
- Context-aware suggestions for schema modifications
- Best practice recommendations for Azure Database for PostgreSQL
- Code completion for complex transformations
- Integration with your existing development workflow

## Oracle connectivity modes

The schema conversion tool supports two connectivity modes for connecting to your source Oracle database: **thin** and **thick**. Understanding the difference helps you choose the right mode for your environment.

### Thin client mode (default)

Thin mode connects directly to Oracle Database without requiring any additional Oracle client libraries. This mode is the default and works out of the box.

- No Oracle Instant Client installation required
- Supports Oracle Database 12.1 and later
- Suitable for most schema conversion scenarios
- Connects using standard TCP/IP networking

### Thick client mode

Thick mode uses Oracle Instant Client libraries to connect to Oracle Database. This mode is required when thin mode can't establish a connection to your source Oracle environment.

### Identify whether your Oracle source requires thick client mode

You can determine whether thick client mode is required by checking the Oracle network configuration files in your source environment. Look for the following parameters in the `sqlnet.ora` file (typically located in `$ORACLE_HOME/network/admin/`):

| Parameter | Indicates thick mode is required |
| --- | --- |
| `SQLNET.CRYPTO_CHECKSUM_CLIENT` | Set to `REQUIRED` or `REQUESTED` for native network encryption |
| `SQLNET.ENCRYPTION_CLIENT` | Set to `REQUIRED` or `REQUESTED` for native network encryption |

If any of these parameters are configured in your source Oracle environment, select **Thick** client mode in the Migration Wizard and ensure Oracle Instant Client is installed.

### Install Oracle Instant Client

To use thick client mode, install Oracle Instant Client on the machine where VS Code and the schema conversion tool are running. Schema conversion is supported on **Windows** and **Linux** only.

1. Download the **Oracle Instant Client Basic** or **Basic Light** package from Oracle's website for your operating system.
1. Extract the package to a directory on the machine.
1. Add the Instant Client directory to the system **PATH** environment variable:
   - **Windows**: Add the Instant Client directory to the `PATH` variable through **System Properties** > **Environment Variables**, or by using PowerShell.
   - **Linux**: Add the Instant Client directory to `PATH` and set the `LD_LIBRARY_PATH` environment variable to include the directory. Ensure the `libaio` library is installed.
1. Restart VS Code to pick up the updated environment variables.

## Authentication for Azure OpenAI and Azure AI Foundry

The schema conversion tool supports two authentication methods for connecting to Azure OpenAI or Azure AI Foundry models:

### API key authentication

API key authentication uses a deployment-specific key to authorize requests. This method is straightforward and suitable for development and testing scenarios.

### Microsoft Entra ID authentication

Microsoft Entra ID (formerly Azure Active Directory) authentication provides token-based, identity-driven access to Azure OpenAI and Azure AI Foundry without managing API keys. This method is recommended for production environments and organizations with centralized identity management.

To use Microsoft Entra ID authentication:

1. **Assign the required role**: Ensure the signed-in user or service principal has the **Cognitive Services OpenAI User** role (or higher) on the Azure OpenAI resource. Assign the role in the Azure portal under **Access control (IAM)**.
1. **Sign in to Azure in VS Code**: Use the **Azure: Sign In** command from the Command Palette (`Ctrl+Shift+P`) to authenticate with your Microsoft Entra ID account.
1. **Select Entra ID authentication**: In the Migration Wizard language model configuration step, select **Microsoft Entra ID** as the authentication method instead of API key.
1. **Provide the endpoint**: Enter your Azure OpenAI or Azure AI Foundry endpoint URL. The tool acquires the authentication token automatically from your signed-in session.

> [!NOTE]
> Microsoft Entra ID authentication requires the **Azure Account** extension in VS Code. The extension must be signed in with an identity that has the appropriate role assignment on the Azure OpenAI resource.

## Security and networking

When you use the schema conversion feature, make sure your Visual Studio Code environment can securely connect to both your source Oracle database and the Azure Database for PostgreSQL flexible server instance that you use as the scratch database.

Microsoft recommends connecting to an Azure OpenAI resource by using a private endpoint. For more information, see [Create a private endpoint for Azure OpenAI](/azure/ai-foundry/openai/how-to/network).

For more information on securing your Azure OpenAI connections, visit [Data, privacy, and security for Azure Direct Models in Microsoft Foundry](/azure/ai-foundry/responsible-ai/openai/data-privacy?tabs=azure-portal).

:::image type="content" source="media/schema-conversions-overview/azure-openai-networking.png" alt-text="Diagram of how Visual Studio Code connects to a private endpoint.":::

> [!IMPORTANT]
> Customer validation responsibility: The same AI engine used for schema conversion can also assist with validation and review. AI systems can occasionally confirm their own mistakes. To prevent data loss, functional regressions, or security issues, independently validate all converted objects and review-task resolutions before deploying to production. As part of your controls, consider enabling Foundry content filtering to help reduce harmful or undesired outputs. For guidance, see [Content filtering in Foundry](/azure/ai-foundry/concepts/content-filtering).

## Why use the schema conversion feature?

Converting Oracle schemas to Azure Database for PostgreSQL streamlines migration and modernization. It reduces manual effort and risk by automating transformations, validating results in a scratch database, and providing AI-assisted review and Azure-optimized output ready for deployment.

- **Automated conversion**: Reduces manual effort by automatically converting compatible schema objects
- **AI-powered intelligence**: Uses Azure OpenAI for smart transformation decisions
- **Validation-first approach**: Uses the scratch database to ensure converted objects work correctly
- **Integrated workflow**: Works seamlessly within Visual Studio Code development environment
- **Flexible Oracle connectivity**: Supports both thin and thick client modes for connecting to Oracle databases
- **Multiple authentication options**: Supports API key and Microsoft Entra ID authentication for Azure OpenAI and Azure AI Foundry
- **Review and refinement**: Provides clear guidance for manual review tasks
- **Azure optimization**: Designed for Azure Database for PostgreSQL flexible server

## Supported schema objects

The conversion tool supports a broad range of Oracle schema and code objects, including data definition elements, schema-level components, and procedural code. While you can convert many common objects automatically, you might need to manually review or customize the mapping for certain Oracle-specific features or proprietary extensions. For detailed lists of supported objects and known limitations, see the sections in this article.

#### Database schema objects

The conversion tool supports the following Oracle database objects:

- **Tables** - Table definitions, column specifications, and table-level constraints
- **Constraints** - Primary keys, foreign keys, unique constraints, check constraints
- **Indexes** - B-tree indexes, unique indexes, composite indexes
- **Sequences** - Oracle sequence objects for autoincrementing values
- **Triggers** - Row-level and statement-level triggers
- **Views** - Standard database views
- **Materialized Views** - Oracle materialized views and refresh logic
- **Schemas** - Schema-level objects and organization
- **Synonyms** - Public and private synonyms (with limitations)

#### Oracle code objects

Advanced Oracle code constructs supported for conversion:

- **Triggers** - Complex trigger logic and event handling
- **Packages** - Oracle package specifications and bodies
- **Functions** - User-defined functions with complex logic
- **Stored Procedures** - Oracle stored procedures and parameter handling

## Supported Oracle versions

This section summarizes the database engine versions that support automated schema conversion and highlights compatibility considerations. Use the listed supported Oracle and PostgreSQL releases for the best results. Validate conversions in a nonproduction test environment, and use the latest minor patch of each supported major release. If your environment uses an unsupported version or includes Oracle proprietary features, you might need to perform extra manual mapping or review before deployment.

The following Oracle database versions support schema conversion:

- Oracle 21c
- Oracle 18c
- Oracle 19c
- Oracle 12.2
- Oracle 12.1

## Feedback and support

For bugs, feature requests, and issues related to the Schema Conversion feature or the PostgreSQL extension, use the built-in feedback tool in Visual Studio Code. You can access this tool in two ways:

### Help menu

Go to **Help** > **Report Issue**

### Command Palette

1. Open the Command Palette with `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (macOS).
1. Run the command: **PGSQL: Report Issue**.

When you create your issue or provide feedback, include `Schema Conversion:` as a prefix in your title. This prefix helps the development team quickly identify and prioritize Schema Conversion-related feedback. This feedback mechanism helps the development team continuously improve the Schema Conversion functionality and address any issues you encounter during your Oracle to PostgreSQL migration projects.

## Related content

- [Best practices for converting Oracle schemas to PostgreSQL](schema-conversions-best-practices.md)
- [Schema conversion limitations](schema-conversions-limitations.md)