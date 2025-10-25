---
title: Oracle to PostgreSQL Schema Conversion
description: Learn how to convert Oracle database schemas to PostgreSQL using the VS Code PostgreSQL extension with AI-powered transformation, Azure OpenAI integration, and intelligent review tasks for seamless migration to Azure Database for PostgreSQL flexible server.
author: apduvuri
ms.author: adityaduvuri
ms.reviewer: maghan
ms.date: 10/17/2025
ms.service: azure-database-postgresql
ms.subservice: migration-guide
ms.topic: overview
ms.custom:
  - devx-track-azurecli
  - migration
  - schema-conversion
---

# Oracle to PostgreSQL Schema Conversion

The Oracle to PostgreSQL Schema Conversion feature in the VS Code PostgreSQL extension helps you convert your existing Oracle database schema objects into PostgreSQL-compatible schema. This functionality is designed for relational schemas and ensures that the converted schema works seamlessly with Azure Database for PostgreSQL flexible server.

The tool provides a project-based user interface to automate schema conversion. If certain objects can't be converted automatically, the tool flags them as Review Tasks, which you can resolve manually by using GitHub Copilot Agents.

:::image type="content" source="Images/Overview.png" alt-text="Screenshot of Schema Conversion overview":::

## Architecture Overview

The schema conversion process involves multiple components working together:

- **Source Oracle Database**: Your existing Oracle database containing the schema to convert
- **VS Code PostgreSQL Extension**: The primary interface for managing the conversion process
- **Azure Database for PostgreSQL flexible server**: Used as the Scratch DB for validation and testing
- **Azure OpenAI**: Provides intelligent transformation capabilities for complex schema objects
- **Schema Conversion Agents**: AI-powered agents that handle the automated conversion process

## How This Works

The schema conversion process uses an intelligent, multistage approach that combines automated transformation with human oversight:

- **Connection and Discovery**: The tool connects to your Oracle database and catalogs all schema objects. It analyzes their structure, dependencies, and complexity to create a conversion plan.
- **AI-Powered Transformation**: Schema Conversion Agents use Azure OpenAI to intelligently transform Oracle-specific constructs into PostgreSQL-compatible equivalents. The AI understands context, relationships, and best practices for both database platforms.
- **Validation in Scratch Environment**: The tool tests all converted objects in the Azure Database for PostgreSQL database (Scratch DB) environment. This step ensures syntax correctness and compatibility before final output generation.
- **Review Task Generation**: The tool flags objects that can't be fully automated or require human judgment as Review Tasks. These objects might include complex business logic or Oracle-specific features that need manual attention.
- **Guided Resolution**: GitHub Copilot Agent Mode provides intelligent assistance for completing Review Tasks. It offers context-aware suggestions and Azure Database for PostgreSQL flexible server best practices to help you make informed decisions.
- **Output Generation**: The tool converts successfully validated objects into organized PostgreSQL `.sql` files, ready for deployment to your target environment.

## How to install the extension
The Oracle to PostgreSQL Schema Conversion functionality is built into the **PostgreSQL extension** for VS Code. You don't need a separate extension - it's included as a comprehensive feature within the main PostgreSQL extension.

### Installation Steps

1. **Open Extensions Marketplace**: In Visual Studio Code, select the Extensions icon in the Activity Bar on the left side, or use the keyboard shortcut `Ctrl+Shift+X` (Windows/Linux) or `Cmd+Shift+X` (macOS).
1. **Search for PostgreSQL**: In the Extensions Marketplace search box, type "PostgreSQL" to find the extension.
1. **Install the Extension**: Locate the PostgreSQL extension in the search results and select **Install**.
1. **Access Schema Conversion**: When the extension is installed, you see an elephant icon in the VS Code sidebar representing the PostgreSQL extension. You can access the Schema Conversion feature through this extension interface.

## Key Concepts

### Scratch DB
An Azure Database for PostgreSQL flexible server that you use during conversion for validation purposes to ensure compatibility. This approach ensures that:
- Converted objects are syntactically correct
- Dependencies are properly resolved
- Performance characteristics are maintained
- Azure-specific features are leveraged appropriately

### Review tasks
The tool flags items for manual review when the AI can't fully convert an object or recommends a second look. Common review tasks include:
- Complex PL/SQL procedures that need manual optimization
- Oracle-specific data types with multiple PostgreSQL alternatives
- Custom functions with Oracle-specific logic

### GitHub Copilot Agent Mode
An integrated feature in VS Code that provides guided prompts to help you complete review tasks and align schema with your application requirements. The agent mode offers:
- Context-aware suggestions for schema modifications
- Best practice recommendations for Azure Database for PostgreSQL
- Code completion for complex transformations
- Integration with your existing development workflow

## Benefits

- **Automated conversion**: Reduces manual effort by automatically converting compatible schema objects
- **AI-powered intelligence**: Leverages Azure OpenAI for smart transformation decisions
- **Validation-first approach**: Uses Scratch DB to ensure converted objects work correctly
- **Integrated workflow**: Works seamlessly within VS Code development environment
- **Review and refinement**: Provides clear guidance for manual review tasks
- **Azure optimization**: Specifically designed for Azure Database for PostgreSQL flexible server

## Feedback and support

For bugs, feature requests, and issues related to the Schema Conversion feature or the PostgreSQL extension, use the built-in feedback tool in Visual Studio Code. You can access this tool in two ways:

### Help menu
Go to **Help** > **Report Issue**

### Command Palette
1. Open the Command Palette with `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (macOS).
1. Run the command: **PGSQL: Report Issue**.

When you create your issue or provide feedback, include `Schema Conversion:` as a prefix in your title. This prefix helps the development team quickly identify and prioritize Schema Conversion-related feedback. This feedback mechanism helps the development team continuously improve the Schema Conversion functionality and address any issues you encounter during your Oracle to PostgreSQL migration projects.


