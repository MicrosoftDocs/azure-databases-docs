---
title: What is Oracle to Azure Database for PostgreSQL schema conversion?
description: Learn how to convert Oracle database schemas to Azure Database for PostgreSQL by using the Visual Studio Code PostgreSQL extension, AI-powered transformation in Microsoft Foundry, and review tasks for migration to Azure Database for PostgreSQL flexible server.
author: apduvuri
ms.author: adityaduvuri
ms.reviewer: maghan
ms.date: 06/02/2026
ai-usage: ai-assisted
ms.service: azure-database-postgresql
ms.topic: overview
ms.collection: ce-skilling-ai-copilot
ms.update-cycle: 180-days
---

# What is Oracle to Azure Database for PostgreSQL schema conversion?

The Oracle to Azure Database for PostgreSQL schema conversion feature in the Visual Studio Code PostgreSQL extension helps you convert your existing Oracle database schema objects into PostgreSQL-compatible schema. This functionality is designed for relational schemas and produces converted schema for Azure Database for PostgreSQL flexible server.

The tool provides a project-based user interface to automate schema conversion. If certain objects can't be converted automatically, the tool flags them as review tasks, which you can resolve manually by using GitHub Copilot agent mode.

:::image type="content" source="media/schema-conversions-overview/schema-conversion.png" alt-text="Diagram of the Oracle to Azure Database for PostgreSQL schema conversion architecture.":::

## Architecture

The schema conversion process involves multiple components working together:

- **Source Oracle database**: Your existing Oracle database that contains the schema to convert.
- **Visual Studio Code PostgreSQL extension**: The primary interface for managing the conversion process.
- **Azure Database for PostgreSQL flexible server**: Hosts the scratch schemas used for validation and testing.
- **Microsoft Foundry**: Provides the language models that power AI-driven schema transformation.
- **Schema conversion agents**: AI-powered agents that handle the automated conversion process.

## How it works

The schema conversion process uses an intelligent, multistage approach that combines automated transformation with human oversight:

- **Connection and discovery**: The tool connects to your Oracle database and catalogs all schema objects. It analyzes their structure, dependencies, and complexity to create a conversion plan.
- **AI-powered transformation**: Schema conversion agents use language models hosted in Microsoft Foundry to transform Oracle-specific constructs into PostgreSQL-compatible equivalents. The AI takes context, relationships, and platform best practices into account.
- **Validation in scratch schemas**: The tool tests all converted objects in scratch schemas on your Azure Database for PostgreSQL flexible server. This step verifies syntax correctness and compatibility before final output generation.
- **Review task generation**: The tool flags objects that can't be fully automated or that require human judgment as review tasks. These objects might include complex business logic or Oracle-specific features that need manual attention.
- **Guided resolution**: GitHub Copilot agent mode provides assistance for completing review tasks. It offers context-aware suggestions and Azure Database for PostgreSQL flexible server best practices to help you make informed decisions.
- **Output generation**: The tool converts successfully validated objects into organized PostgreSQL `.sql` files, ready for deployment to your target environment.

## Install the extension

The Oracle to PostgreSQL schema conversion feature is built into the **PostgreSQL extension** for Visual Studio Code. You don't need to install a separate extension.

### Installation steps

1. **Open Extensions Marketplace**: In Visual Studio Code, select the Extensions icon in the Activity Bar on the left side, or use the keyboard shortcut `Ctrl+Shift+X` (Windows/Linux) or `Cmd+Shift+X` (macOS).
1. **Search for the extension**: In the Extensions Marketplace search box, enter `PostgreSQL` (or the extension ID `ms-ossdata.vscode-pgsql`) to find the extension.
1. **Install the extension**: In the search results, locate **PostgreSQL** published by **Microsoft**, and then select **Install**. Several PostgreSQL extensions are available in the Marketplace, so verify that the publisher is **Microsoft** before you install.
1. **Access Schema Conversion**: After the extension is installed, an elephant icon appears in the Visual Studio Code Activity Bar. Select the icon to open the PostgreSQL extension and access the Schema Conversion feature.

## Schema conversion workflow

This section explains the core concepts used throughout the Oracle to Azure Database for PostgreSQL schema conversion workflow, including conversion units (schemas, tables, indexes, views, and procedures), review tasks for human oversight, scratch database validation, AI-powered schema conversion agents, and the resulting PostgreSQL SQL artifacts. Understanding these concepts helps you interpret conversion results, prioritize and resolve flagged items, and prepare converted files for deployment to Azure Database for PostgreSQL flexible server.

### Scratch database

The schema conversion tool uses an Azure Database for PostgreSQL flexible server as a temporary validation environment. Within that server, the tool creates one or more **scratch schemas**, which are short-lived PostgreSQL schemas that hold converted objects so the tool can test them without affecting your production data.

Using scratch schemas inside a scratch database lets the tool verify that:

- Converted objects are syntactically correct.
- Dependencies between objects are resolved in the correct order.
- Object definitions remain compatible with the target PostgreSQL version.
- Azure Database for PostgreSQL flexible server features apply correctly.

> [!NOTE]
> The connecting user must have `CREATE` privileges on the scratch database so the tool can create and drop scratch schemas (named with the `_mig_scratch_` prefix) as needed.

### Review tasks

The tool flags items for manual review when the AI can't fully convert an object or recommends that you confirm the result. Common review tasks include:

- Complex PL/SQL procedures that need manual adjustment.
- Oracle-specific data types that have multiple PostgreSQL alternatives.
- Custom functions that contain Oracle-specific logic.

For more information about review task priorities and generated output folders, see [Review tasks and output folders for Oracle to Azure Database for PostgreSQL schema conversion](schema-conversions-review-tasks-artifacts.md).

### GitHub Copilot agent mode

GitHub Copilot agent mode is an integrated Visual Studio Code feature that provides guided prompts to help you complete review tasks and align the converted schema with your application requirements. Agent mode offers:

- Context-aware suggestions for schema modifications.
- Best practice recommendations for Azure Database for PostgreSQL flexible server.
- Code completion for complex transformations.
- Integration with your existing development workflow.

## Oracle connectivity modes

The schema conversion tool supports two connectivity modes for connecting to your source Oracle database: **thin** and **thick**. Understanding the difference helps you choose the right mode for your environment.

### Thin client mode (default)

Thin mode connects directly to Oracle Database without additional Oracle client libraries. This mode is the default and requires no extra setup.

- Requires no Oracle Instant Client installation.
- Supports Oracle Database 12.1 and later.
- Suits most schema conversion scenarios.
- Connects by using standard TCP/IP networking.

### Thick client mode

Thick mode uses Oracle Instant Client libraries to connect to Oracle Database. The schema conversion tool detects when thick mode is needed based on your Oracle network configuration and switches to it automatically.

### When thick client mode is required

You can determine whether thick client mode is required by checking the Oracle network configuration files in your source environment. Look for the following parameters in the `sqlnet.ora` file (typically located in `$ORACLE_HOME/network/admin/`):

| Parameter | Indicates thick mode is required |
| --- | --- |
| `SQLNET.CRYPTO_CHECKSUM_CLIENT` | Set to `REQUIRED` or `REQUESTED` for native network encryption |
| `SQLNET.ENCRYPTION_CLIENT` | Set to `REQUIRED` or `REQUESTED` for native network encryption |

If any of these parameters are configured in your source Oracle environment, thick client mode is required. The schema conversion tool detects this configuration and switches to thick mode automatically. Make sure Oracle Instant Client is installed on the machine where Visual Studio Code is running before you start the conversion.

### Install Oracle Instant Client

To use thick client mode, install Oracle Instant Client on the machine where Visual Studio Code and the schema conversion tool are running. Schema conversion is supported on **Windows** and **Linux** only.

1. Download the **Oracle Instant Client Basic** or **Basic Light** package from Oracle's website for your operating system.
1. Extract the package to a directory on the machine.
1. Add the Instant Client directory to the system `PATH` environment variable:
   - **Windows**: Add the Instant Client directory to the `PATH` variable through **System Properties** > **Environment Variables**, or by using PowerShell.
   - **Linux**: Add the Instant Client directory to `PATH` and set the `LD_LIBRARY_PATH` environment variable to include the directory. Make sure the `libaio` library is installed.
1. Restart Visual Studio Code to pick up the updated environment variables.

## Authentication for Microsoft Foundry

The schema conversion tool supports two authentication methods for connecting to language models in Microsoft Foundry:

### API key authentication

API key authentication uses a deployment-specific key to authorize requests. This method is straightforward and suitable for development and testing scenarios.

### Microsoft Entra ID authentication

Microsoft Entra ID authentication provides token-based, identity-driven access to Microsoft Foundry without managing API keys. This method is recommended for production environments and organizations with centralized identity management.

To use Microsoft Entra ID authentication:

1. **Assign the required role**: Make sure the signed-in user or service principal has the **Foundry User** role (formerly **Azure AI User**) on the Microsoft Foundry resource that hosts your model deployment. Assign the role in the Azure portal under **Access control (IAM)**. For more information, see [Role-based access control for Microsoft Foundry](/azure/foundry/concepts/rbac-foundry).
1. **Sign in to Azure in Visual Studio Code**: Use the **Azure: Sign In** command from the Command Palette (`Ctrl+Shift+P`) to authenticate with your Microsoft Entra ID account.
1. **Select Entra ID authentication**: In the **Migration Wizard** language model configuration step, select **Microsoft Entra ID** as the authentication method instead of **API key**.
1. **Provide the endpoint**: Enter your Microsoft Foundry endpoint URL. The tool acquires the authentication token automatically from your signed-in session.

> [!NOTE]
> Microsoft Entra ID authentication requires the **Azure Account** extension in Visual Studio Code. The extension must be signed in with an identity that has the appropriate role assignment on the Microsoft Foundry resource.

## Security and networking

When you use the schema conversion feature, make sure your Visual Studio Code environment can securely connect to both your source Oracle database and the Azure Database for PostgreSQL flexible server instance that you use as the scratch database.

Microsoft recommends connecting to your Microsoft Foundry resource by using a private endpoint. For more information, see [Configure a private link for Microsoft Foundry](/azure/ai-foundry/how-to/configure-private-link).

For more information about securing your Microsoft Foundry connections, see [Data, privacy, and security for Azure Direct Models in Microsoft Foundry](/azure/ai-foundry/responsible-ai/openai/data-privacy?tabs=azure-portal).

:::image type="content" source="media/schema-conversions-overview/azure-openai-networking.png" alt-text="Diagram of how Visual Studio Code connects to a private endpoint.":::

> [!IMPORTANT]
> Customer validation responsibility: The same AI engine used for schema conversion can also assist with validation and review. AI systems can occasionally confirm their own mistakes. To prevent data loss, functional regressions, or security issues, independently validate all converted objects and review-task resolutions before deploying to production. As part of your controls, consider enabling Foundry content filtering to help reduce harmful or undesired outputs. For guidance, see [Content filtering in Foundry](/azure/ai-foundry/concepts/content-filtering).

## Why use the schema conversion feature?

Converting Oracle schemas to Azure Database for PostgreSQL streamlines migration and modernization. It reduces manual effort and risk by automating transformations, validating results in a scratch database, and providing AI-assisted review and Azure-optimized output ready for deployment.

- **Automated conversion**: Reduces manual effort by automatically converting compatible schema objects.
- **AI-powered transformation**: Uses language models hosted in Microsoft Foundry for context-aware conversion decisions.
- **Validation-first approach**: Uses scratch schemas to confirm that converted objects work correctly.
- **Integrated workflow**: Works within the Visual Studio Code development environment.
- **Flexible Oracle connectivity**: Supports both thin and thick client modes for connecting to Oracle databases.
- **Multiple authentication options**: Supports API key and Microsoft Entra ID authentication for Microsoft Foundry.
- **Review and refinement**: Provides clear guidance for manual review tasks.
- **Azure optimization**: Designed for Azure Database for PostgreSQL flexible server.

## Supported schema objects

The conversion tool supports a broad range of Oracle schema and code objects, including data definition elements, schema-level components, and procedural code. While you can convert many common objects automatically, you might need to manually review or customize the mapping for certain Oracle-specific features or proprietary extensions. For detailed lists of supported objects and known limitations, see the sections in this article.

### How conversions are produced

The schema conversion tool combines AI-powered translation with automated validation to deliver reliable results. Microsoft Foundry models translate Oracle DDL into PostgreSQL. The tool then compiles each converted object against a scratch schema in your target Azure Database for PostgreSQL flexible server, runs static analysis, and applies automated fixes for common issues. The remaining stages of the pipeline - source parsing, metadata extraction, and script generation - run as predictable, rule-based steps.

This approach uses AI where it adds the most value and keeps the rest of the workflow deterministic and verifiable. Objects that can't be fully validated are flagged as review tasks so you can address them before you apply the converted schema. For Oracle features that don't have a practical PostgreSQL equivalent, see [Schema conversion limitations](schema-conversions-limitations.md).

### Database schema objects

The conversion tool supports the following Oracle database objects:

- **Tables**: Table definitions, column specifications, and table-level constraints.
- **Constraints**: Primary keys, foreign keys, unique constraints, and check constraints.
- **Indexes**: B-tree indexes, unique indexes, and composite indexes.
- **Sequences**: Oracle sequence objects for autoincrementing values.
- **Triggers**: Row-level and statement-level triggers.
- **Views**: Standard database views.
- **Materialized views**: Oracle materialized views and refresh logic.
- **Schemas**: Schema-level objects and organization.
- **Synonyms**: Public and private synonyms (with limitations).

### Oracle code objects

The conversion tool supports the following Oracle code constructs:

- **Triggers**: Complex trigger logic and event handling.
- **Packages**: Oracle package specifications and bodies.
- **Functions**: User-defined functions with complex logic.
- **Stored procedures**: Oracle stored procedures and parameter handling.
- **Types and collections**: Oracle object types, `TYPE BODY` member methods, `VARRAY`, nested tables, and `SUBTYPE` declarations.

## Supported Oracle versions

This section summarizes the database engine versions that support automated schema conversion and highlights compatibility considerations. Use the listed supported Oracle and PostgreSQL releases for the best results. Validate conversions in a nonproduction test environment, and use the latest minor patch of each supported major release. If your environment uses an unsupported version or includes Oracle proprietary features, you might need to perform extra manual mapping or review before deployment.

The following Oracle database versions support schema conversion:

- Oracle 21c
- Oracle 19c
- Oracle 18c
- Oracle 12.2
- Oracle 12.1

## Feedback and support

For bugs, feature requests, and issues related to the schema conversion feature or the PostgreSQL extension, use the built-in feedback tool in Visual Studio Code. You can access this tool in two ways:

### Help menu

Go to **Help** > **Report Issue**.

### Command Palette

1. Open the Command Palette with `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (macOS).
1. Run the command: **PGSQL: Report Issue**.

When you create your issue or provide feedback, include `Schema Conversion:` as a prefix in your title. This prefix helps the development team quickly identify and prioritize schema conversion-related feedback. This feedback mechanism helps the development team continuously improve the schema conversion feature and address any issues you encounter during your Oracle to Azure Database for PostgreSQL migration projects.

## Related content

- [Best practices for Oracle to Azure Database for PostgreSQL schema conversion](schema-conversions-best-practices.md)
- [Review tasks and output folders for Oracle to Azure Database for PostgreSQL schema conversion](schema-conversions-review-tasks-artifacts.md)
- [Schema conversion limitations](schema-conversions-limitations.md)
