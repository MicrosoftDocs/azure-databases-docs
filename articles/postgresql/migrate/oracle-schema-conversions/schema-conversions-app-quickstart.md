---
title: "Oracle to Azure Database for PostgreSQL Application Conversion: Quickstart"
description: "Step-by-step quickstart for converting Oracle client application code to PostgreSQL using the Visual Studio PostgreSQL extension with Azure OpenAI integration."
author: jjfrost
ms.author: jfrost
ms.reviewer: maghan
ms.date: 11/18/2025
ms.service: azure-database-postgresql
ms.topic: quickstart
---

# Quickstart: Oracle to Azure Database for PostgreSQL application conversion Preview

This quickstart walks you through converting **Oracle client application code** to Azure Database for PostgreSQL by using the **Application Conversion** feature in the Oracle to Azure Database for PostgreSQL migration tooling, available in the Visual Studio Code PostgreSQL extension.

You learn how to:
- Import your source application code into the migration workspace.
- Start the automated code conversion process.
- View the generated migration report.
- Review and compare converted files by using the built-in diff tools.

While it's **not required** to perform a database schema conversion beforehand, we **strongly recommend** completing a schema migration first.  
If you already converted your Oracle schema to PostgreSQL, the application conversion process provides more accurate context and higher-quality code transformation results.

### Step 1: Set up your environment

1. Before you get started on Application Conversion, set your GitHub Copilot Agent Mode Model to **Claude Sonnet 4** or higher.
1. Open the GitHub Copilot chat interface and then select **Claude Sonnet 4** or higher for the model.

### Step 2: Copy your codebase into the migration project

1. Locate the `application_code` folder in your project under `.github/postgres-migration/project_name/application_code`.
1. Copy the codebase folder you want to migrate into the `application_code` folder inside your project folder.

### Step 3: Start client code migration

1. Select **Migrate Application** to start the application conversion wizard.
1. On the form that loads, select the folder you copied into the root of your workspace.
1. Choose the database that has the context for your application, such as the database where you deploy your converted DDL or where you already have your application.
1. Select **Convert Application**.
   - This action invokes a custom composite prompt and Agent Mode Tool.
   - This action generates a TODO list of tasks that Agent Mode proceeds to work on for you.
   - Additional Agent Mode tools connect to and read your database for enhanced context for the application conversion.

### Step 4: Code conversion report

1. When the application conversion finishes in Agent Mode, it automatically generates and opens a comprehensive report.

### Step 5: Compare code changes using file diff feature

1. You can also review file differences for your application code.
1. For example, you can right-select a `.java` file and select **Compare App Migration File Pairs**.
1. This action opens a file diff view with the original file and the updated file.

## What are "Coding Notes"?

**Coding Notes** are metadata artifacts automatically generated during the schema conversion phase.  
They capture key transformation details and insights from your Oracle-to-PostgreSQL schema conversion that the process later uses to enhance **application code conversion**.

Coding Notes might include information such as:
- Data type mappings and structural changes
- Conversion details for sequences, identities, and composite types
- Adjustments to date/time or interval implementations
- References to tables with referential integrity constraints
- Summaries of complex Oracle packages, including procedure and function signatures
- Additional AI-generated hints to improve code translation accuracy

During **application conversion**, the AI model uses these notes as contextual signals to produce more precise and semantically aligned PostgreSQL-compatible code.

## Related content

- [Oracle to PostgreSQL Migration Overview](schema-conversions-overview.md)
- [Oracle to PostgreSQL Migration Schema Tutorial](schema-conversions-tutorial.md)
- [Oracle to PostgreSQL Migration Limitations](schema-conversions-limitations.md)
