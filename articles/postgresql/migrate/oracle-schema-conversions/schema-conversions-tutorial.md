---
title: "Oracle to PostgreSQL Schema Conversion: Tutorial"
description: "Step-by-step tutorial for converting Oracle database schemas to PostgreSQL using the Visual Studio PostgreSQL extension with Azure OpenAI integration."
author: apduvuri
ms.author: adityaduvuri
ms.reviewer: maghan
ms.date: 11/18/2025
ms.service: azure-database-postgresql
ms.topic: tutorial
---

# Tutorial: Oracle to PostgreSQL schema conversion Preview

This tutorial guides you through converting Oracle database schemas to PostgreSQL using the Visual Studio PostgreSQL extension with Azure OpenAI to automate and validate schema translation

It covers connecting to your Oracle source and Azure Database for PostgreSQL target, configuring Azure OpenAI, running the Migration Wizard, and reviewing generated PostgreSQL artifacts. Before you begin, ensure you have network access and credentials for both servers and an Azure OpenAI deployment.

[!INCLUDE [prerequisites-schema-conversions](includes/prerequisites-schema-conversions.md)]

## Migration process

This section walks through the complete migration workflow: install the PostgreSQL extension, create and test connections to your Oracle source and Azure Database for PostgreSQL target, open and initialize a migration project, configure Azure OpenAI for schema translation, run the Migration Wizard to discover and convert schemas, validate converted objects in a scratch database, and review or fix any flagged items before applying the generated PostgreSQL artifacts to your target.

### Step 1: Install the PostgreSQL Visual Studio Code extension

1. Open Visual Studio.
1. Go to the **Extensions** view (Ctrl+Shift+X).
1. Search for *PostgreSQL* and install the **PostgreSQL** extension.
   1. [Marketplace download](https://marketplace.visualstudio.com/items?itemName=ms-ossdata.vscode-pgsql)

For more information about the Visual Studio Code extension, visit [PostgreSQL extension for Visual Studio Code](../../extensions/vs-code-extension/overview.md).

### Step 2: Create PostgreSQL connection

1. In the PostgreSQL extension panel, create a connection to your **Azure Database for PostgreSQL**.
1. Enter the necessary connection details (host, database, username, password).
1. Test and save the connection.

### Step 3: Open new workspace

1. Create a new folder on your local machine for the migration project.
1. Open a **new workspace** in Visual Studio Code.

### Step 4: Initialize migration project

1. **Right-click** on the blank workspace area.
1. Select **Open Migration Project** from the context menu.

### Step 5: Configure project settings

1. In the **Migration Wizard**, enter your **project name**.
1. Select **Next** to proceed to the next step.

### Step 6: Configure Oracle connection

1. Enter your **Oracle connection details** including:
   - Host or server name
   - Port number
   - Database or service name
   - Username and password
1. Select **Load Schemas**.
1. The system **tests the Oracle connection**.
1. If successful, it **lists all user-defined schemas** available in Oracle.
1. **Choose one or multiple schemas** that you want to convert to PostgreSQL.
1. Select **Next** to continue.

### Step 8: Configure PostgreSQL target

1. **Select the Azure Database for PostgreSQL connection** that you defined in the PostgreSQL extension
1. **Select the target database** from the dropdown list
1. Select **Next** to proceed

### Step 9: Configure Azure OpenAI

1. Enter your **Azure OpenAI details** including:
   - Endpoint URL
   - API key
   - Deployment name (must be gpt-4.1)
1. Select **Test Connection** to verify the configuration
1. Once the connection is **successful**, select **Create Migration Project**

### Step 10: Execute schema conversion

1. The system navigates to the **main Migration Wizard**
1. Select **Migrate** to initiate the **Schema Conversion** process
1. Monitor the conversion progress in the Visual Studio interface

## What happens during conversion?

- **Schema Discovery**: The tool analyzes your Oracle schema objects
- **AI Processing**: Azure OpenAI processes and converts compatible objects
- **Validation**: Converted objects are validated in the Scratch DB
- **Review Tasks**: Objects requiring manual attention are flagged
- **Output Generation**: Successfully converted objects are saved as PostgreSQL files

## Related content

- [Oracle to PostgreSQL Migration Overview](schema-conversions-overview.md)
- [Oracle to PostgreSQL Migration Limitations](schema-conversions-limitations.md)
