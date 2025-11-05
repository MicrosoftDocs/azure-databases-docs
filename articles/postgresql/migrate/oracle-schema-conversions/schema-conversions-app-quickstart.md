---
title: "Oracle to PostgreSQL Application Conversion: Quickstart"
description: "Step-by-step tutorial for converting Oracle database schemas to PostgreSQL using the Visual Studio PostgreSQL extension with Azure OpenAI integration."
author: jjfrost
ms.author: jfrost
ms.reviewer: maghan
ms.date: 11/18/2025 
ms.service: azure-database-postgresql
ms.topic: quickstart
---

# Quickstart: Oracle to PostgreSQL application conversion Preview

# Quickstart: Oracle to PostgreSQL Application Conversion (Preview)

This quickstart walks you through converting **Oracle client application code** to PostgreSQL using the **Application Conversion** feature in the Oracle to PostgreSQL Migration Tooling, available in the Visual Studio Code PostgreSQL extension.

You’ll learn how to:
- Import your source application code into the migration workspace  
- Start the automated code conversion process
= View the generated migration report
- Review and compare converted files using the built-in diff tools  

While it’s **not required** to perform a database schema conversion beforehand, we **strongly recommend** completing a schema migration first.  
Having your Oracle schema already converted to PostgreSQL ensures the application conversion can provide more accurate context and higher-quality code transformation results.


### Step 1: Setup your environment

1. Before you get started on Application Conversion, we highly recommend you set your GitHub Copilot Agent Mode Model to be “Claude Sonnet 4” or higher
1. Open the GitHub Copilot chat interface and then for the model select “Claude Sonnet 4” or higher

### Step 2: Copy your codebase into the migration project

1. Locate the "application_code" folder in your project under .github/postgres-migration/project_name/application_code
1. Next, copy the codebase folder you wish to migrate into the “application_code” folder inside your project folder

### Step 3: Start Client Code Migration

1. Next, click “Migrate Application” to start the application conversion wizard
1. On the form that loads, select the folder you copied into the root of your workspace
1. Choose the database which has the context for your application, for example, the database that represented where you will deploy your converted DDL or where you already have
1. Click “Convert Application”
    - This kicks off a custom composite prompt and Agent Mode Tool, you will see it get invoked
    - This will also generate a TODO list of tasks which Agent Mode will proceed to work on for you
    - Additional Agent Mode tools will also connect to, and read your database for enhanced context for the application conversion

### Step 4: Code Conversion Report

1. When the application conversion finishes in Agent Mode, a comprehensive report will get generated and open automatically at the end

### Step 5: Compare Code Changes using File Diff Feature

1. Lastly, you can also do file diff reviews of you application code
1. For example, you can right click on a .java file and select “Compare App Migration File Pairs”
1. This will open a file diff view like this, with the original file on left and updated file on right.

## What Are "Coding Notes"?

**Coding Notes** are metadata artifacts automatically generated during the schema conversion phase.  
They capture key transformation details and insights from your Oracle-to-PostgreSQL schema conversion that are later used to enhance the **application code conversion** process.

Coding Notes may include information such as:
- Data type mappings and structural changes  
- Conversion details for sequences, identities, and composite types  
- Adjustments to date/time or interval implementations  
- References to tables with referential integrity constraints  
- Summaries of complex Oracle packages, including procedure and function signatures  
- Additional AI-generated hints to improve code translation accuracy  

During **application conversion**, these notes are used as contextual signals by the AI model to produce more precise and semantically aligned PostgreSQL-compatible code.

## Related content

- [Oracle to PostgreSQL Migration Overview](schema-conversions-overview.md)
- [Oracle to PostgreSQL Migration Schema Tutorial](schema-conversions-tutorial.md)
- [Oracle to PostgreSQL Migration Limitations](schema-conversions-limitations.md)