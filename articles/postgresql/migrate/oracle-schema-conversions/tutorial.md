---
title: "Oracle to PostgreSQL Schema Conversion: Tutorial"
description: "Step-by-step tutorial for converting Oracle database schemas to PostgreSQL using the VS Code PostgreSQL extension with Azure OpenAI integration."
author: apduvuri
ms.author: adityaduvuri
ms.reviewer: maghan
ms.date: 10/23/2025
ms.service: azure-database-postgresql
ms.subservice: schema-conversion
ms.topic: tutorial
ms.custom:
  - devx-track-vscode
  - schema-conversion
  - oracle-to-postgresql
  - tutorial
---

# Schema Conversion: Tutorial

This tutorial provides step-by-step instructions for converting Oracle database schemas to PostgreSQL using the VS Code PostgreSQL extension with Azure OpenAI integration.

## Prerequisites

Before starting this tutorial, ensure you have completed the [Prerequisites](prerequisites.md) and reviewed the [Best Practices](best-practices.md).

## Step-by-Step Migration Process

### Step 1: Access PostgreSQL Extension

1. Open Visual Studio Code
2. Navigate to the **PostgreSQL extension** in the VS Code sidebar (elephant icon)

### Step 2: Create PostgreSQL Connection

1. In the PostgreSQL extension panel, create a connection to your **Azure Database for PostgreSQL flexible server**
2. Provide the necessary connection details (host, database, username, password)
3. Test and save the connection

### Step 3: Open New Workspace

1. Open a **new workspace** in VS Code
2. Ensure you have a clean workspace for your migration project

### Step 4: Initialize Migration Project

1. **Right-click** on the blank workspace area
2. Select **"Open Migration Project"** from the context menu

### Step 5: Configure Project Settings

1. In the **Migration Wizard**, provide your **project name**
2. Click **Next** to proceed to the next step

### Step 6: Configure Oracle Connection

1. Provide your **Oracle connection details** including:
   - Host/Server name
   - Port number
   - Database/Service name
   - Username and password
2. Click **Load Schemas**

### Step 7: Select Oracle Schemas

1. The system will **test the Oracle connection** first
2. Once successful, it will **list all user-defined schemas** available in Oracle
3. **Choose one or multiple schemas** that need to be converted to PostgreSQL
4. Click **Next** to continue

### Step 8: Configure PostgreSQL Target

1. **Select the Azure Database for PostgreSQL flexible server connection** that you defined in the PostgreSQL extension
2. **Select the target database** accordingly from the dropdown
3. Click **Next** to proceed

### Step 9: Configure Azure OpenAI

1. Provide your **Azure OpenAI details** including:
   - Endpoint URL
   - API key
   - Deployment name (must be gpt-4.1)
2. Click **Test Connection** to verify the configuration
3. Once the connection is **successful**, click **"Create Migration Project"**

### Step 10: Execute Schema Conversion

1. The system will navigate to the **main Migration Wizard**
2. Click **Migrate** to initiate the **Schema Conversion** process
3. Monitor the conversion progress in the VS Code interface

## What Happens During Conversion

- **Schema Discovery**: The tool analyzes your Oracle schema objects
- **AI Processing**: Azure OpenAI processes and converts compatible objects
- **Validation**: Converted objects are validated in the Scratch DB
- **Review Tasks**: Objects requiring manual attention are flagged
- **Output Generation**: Successfully converted objects are saved as PostgreSQL files

## Next Steps

After the conversion completes:

1. **Review Generated Files**: Examine the converted PostgreSQL schema files
2. **Handle Review Tasks**: Address any flagged objects using GitHub Copilot Agent Mode or manual editing
3. **Test Converted Schema**: Validate the converted schema in your target environment
4. **Deploy to Production**: Deploy the validated schema to your production PostgreSQL environment

## Troubleshooting

If you encounter issues during the tutorial:

- Verify all [Prerequisites](prerequisites.md) are met
- Check your network connectivity to Oracle, PostgreSQL, and Azure OpenAI
- Review the [Best Practices](best-practices.md) for optimal configuration
- Use the built-in feedback tool: **PGSQL: Report Issue**

---

*For additional guidance on resolving Review Tasks and complex conversions, refer to the [Best Practices](best-practices.md) documentation.*