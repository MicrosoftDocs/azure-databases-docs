---
title: "Tutorial: Convert Oracle schemas to Azure Database for PostgreSQL"
description: "Step-by-step tutorial for converting Oracle database schemas to Azure Database for PostgreSQL flexible server by using the Visual Studio Code PostgreSQL extension with Microsoft Foundry integration."
author: apduvuri
ms.author: adityaduvuri
ms.reviewer: maghan
ms.date: 06/02/2026
ai-usage: ai-assisted
ms.service: azure-database-postgresql
ms.topic: tutorial
ms.collection: ce-skilling-ai-copilot
ms.update-cycle: 90-days
---

# Tutorial: Oracle to Azure Database for PostgreSQL schema conversion

This tutorial guides you through converting Oracle database schemas to Azure Database for PostgreSQL by using the Visual Studio Code PostgreSQL extension with Microsoft Foundry to automate and validate schema translation.

It covers connecting to your Oracle source and Azure Database for PostgreSQL target, configuring Microsoft Foundry, running the Migration Wizard, and reviewing generated PostgreSQL artifacts. Before you begin, make sure that you have network access and credentials for both servers and a Microsoft Foundry deployment.

Here's what you can expect during the conversion:

- **Schema discovery**: The tool analyzes your Oracle schema objects.
- **AI processing**: Microsoft Foundry processes and converts compatible objects.
- **Validation**: Converted objects are validated in the scratch database.
- **Review tasks**: Objects that require manual attention are flagged.
- **Output generation**: Successfully converted objects are saved as PostgreSQL files.

## Prerequisites

This section describes the prerequisites for using the Oracle to Azure Database for PostgreSQL schema conversion feature in Visual Studio Code before starting a conversion.

### System requirements

| Category | Details |
| --- | --- |
| **Visual Studio Code** version | 1.95.2 or later |
| **GitHub Copilot** subscription | Pro+, Business, Enterprise |

### Operating system support

| Operating System | Support Details |
| --- | --- |
| **Windows** | x64 architecture only |
| **Linux** | x64 architecture |
| **macOS** | macOS 13+ |

### Target Azure Database for PostgreSQL requirements

| Component | Version requirement |
| --- | --- |
| **Azure Database for PostgreSQL** | PostgreSQL version 15 or later |
| **Scratch database** | Azure Database for PostgreSQL flexible server |

### AI model requirements

You need one of the following AI components configured:

| AI component | Model version |
| --- | --- |
| **Microsoft Foundry** | GPT-5.2 deployment |

#### Microsoft Foundry deployment configuration

In Microsoft Foundry, create a deployment that uses the `gpt-5.2` model. The deployment name is the one you chose when you created the deployment; it doesn't have to match the model name.

The endpoint is your Microsoft Foundry resource URL. Microsoft Foundry resources expose several equivalent hostnames; any of the following formats is valid:

- `https://{your-resource}.services.ai.azure.com`
- `https://{your-resource}.openai.azure.com`
- `https://{your-resource}.cognitiveservices.azure.com`

Replace `{your-resource}` with your Microsoft Foundry resource name (for example, `oracletopg`). If you need to call an inference route directly, the current preview path is `/openai/responses?api-version=2025-04-01-preview`.

For more information about endpoint formats and inference routes, see [Endpoints for Microsoft Foundry Models](/azure/ai-foundry/foundry-models/concepts/endpoints).

> [!TIP]
> To route Microsoft Foundry traffic through Azure API Management for centralized governance, throttling, and observability, configure an AI gateway in front of your Foundry resource and use the gateway URL as the endpoint. For more information, see [Configure AI Gateway in your Foundry resources](/azure/ai-foundry/configuration/enable-ai-api-management-gateway-portal).

### Required database privileges

Before you run the schema conversion, make sure that the accounts you use have the minimum required privileges on both the source Oracle database and the scratch Azure Database for PostgreSQL flexible server. The Oracle account needs read access to data and dictionary views so the tool can analyze schema and code. The Azure Database for PostgreSQL scratch account must be able to create schemas, tables, and other objects for validation. Use a dedicated service account where possible. Follow the principle of least privilege. Coordinate with your DBAs to grant any temporary elevated rights and to validate connectivity and access before you start the conversion.

#### Source Oracle privileges

The following minimum privileges are required on the source Oracle database:

| Privilege | Purpose |
| --- | --- |
| **CONNECT** | Basic database connection |
| **SELECT_CATALOG_ROLE** | Access to data dictionary views |
| **SELECT ANY DICTIONARY** | Read system metadata and dictionary objects |
| **SELECT `SYS.ARGUMENT$`** | Access to procedure and function argument information |

#### Scratch database privileges

The following privileges are required on the Azure Database for PostgreSQL flexible server (scratch database):

| Privilege | Purpose |
| --- | --- |
| **CREATE SCHEMA** | Create validation schemas |
| **CREATE ON DATABASE** | Create database objects for validation |
| **GRANT CONNECT ON DATABASE** | Connection permissions for validation processes |

### Network requirements

- **Outbound connectivity**: Microsoft Foundry endpoints.
- **Database connectivity**: Both source Oracle and target Azure Database for PostgreSQL flexible server.
- **HTTPS access**: Visual Studio Code Extensions Marketplace and GitHub Copilot services.
- **GitHub repository access**: <https://github.com/microsoft/pgsql-tools/>.

### Oracle Instant Client (for thick client mode)

The schema conversion tool connects to Oracle by using thin client mode by default, which requires no extra software. If your environment requires thick client mode, install Oracle Instant Client on the machine that runs Visual Studio Code. The tool reads your `sqlnet.ora` and `tnsnames.ora` configuration and switches to thick mode automatically when a setting requires it.

You can determine whether thick client mode is required by checking the Oracle network configuration files in your source environment. Look for the following parameters in the `sqlnet.ora` file (typically located in `$ORACLE_HOME/network/admin/`):

| Parameter | Indicates thick mode is required |
| --- | --- |
| `SQLNET.CRYPTO_CHECKSUM_CLIENT` | Set to `REQUIRED` or `REQUESTED` for native network encryption |
| `SQLNET.ENCRYPTION_CLIENT` | Set to `REQUIRED` or `REQUESTED` for native network encryption |

### Microsoft Foundry authentication

Configure one of the following authentication methods for Microsoft Foundry:

| Authentication method | Requirements |
| --- | --- |
| **API key** | Microsoft Foundry endpoint URL and API key. |
| **Microsoft Entra ID** | Azure Account extension signed in, **Foundry User** role (formerly **Azure AI User**) assigned on the Microsoft Foundry resource. |

## Migration process

This section walks through the complete migration workflow. You install the PostgreSQL extension, create and test connections to your Oracle source and Azure Database for PostgreSQL target, open and initialize a migration project, configure Microsoft Foundry for schema translation, run the Migration Wizard to discover and convert schemas, validate converted objects in a scratch database, and review or fix any flagged items before you apply the generated PostgreSQL artifacts to your target.

### Step 1: Install the PostgreSQL Visual Studio Code extension

1. Open Visual Studio Code.
1. Go to the **Extensions** view (`Ctrl+Shift+X`).
1. Search for **PostgreSQL** and install the **PostgreSQL** extension published by **Microsoft**.
    1. [Marketplace download](https://marketplace.visualstudio.com/items?itemName=ms-ossdata.vscode-pgsql)
 
    :::image type="content" source="media/schema-conversions-tutorial/postgresql-extension-installation.png" alt-text="Screenshot of installing the PostgreSQL extension in Visual Studio Code.":::

### Step 2: Create an Azure Database for PostgreSQL connection

1. In the PostgreSQL extension panel, create a connection to your **Azure Database for PostgreSQL flexible server** instance.
1. Enter the connection details (host, database, username, password).
1. Test and save the connection.
    
    :::image type="content" source="media/schema-conversions-tutorial/postgresql-new-connection.png" alt-text="Screenshot of adding new Azure Database for PostgreSQL connection.":::

### Step 3: Open a new workspace

1. Create a new folder on your local machine for the migration project.
1. Open the folder as a **new workspace** in Visual Studio Code.
    
    :::image type="content" source="media/schema-conversions-tutorial/open-workspace.png" alt-text="Screenshot of adding a new workspace in Visual Studio Code.":::

### Step 4: Initialize a migration project

1. Open the **PostgreSQL extension**.
1. Go to the **Migrations (preview)** panel.
1. Select **Create Migration Project**.
    
    :::image type="content" source="media/schema-conversions-tutorial/create-migration.png" alt-text="Screenshot of creating a new migration project.":::

### Step 5: Configure project settings

1. In the **Migration Wizard**, enter your **project name**.
1. Select **Next** to continue.

    :::image type="content" source="media/schema-conversions-tutorial/new-migration-project.png" alt-text="Screenshot of project name.":::

### Step 6: Configure the Oracle connection

1. Enter your **Oracle connection details**:
   - Host or server name.
   - Port number.
   - Database or service name.
   - Username and password.

   The tool selects thin or thick client mode automatically from your `sqlnet.ora` and `tnsnames.ora` settings; the UI doesn't expose a manual selector. Thin mode is used by default. If your `sqlnet.ora` requires thick mode, make sure that Oracle Instant Client is installed and that its location is on the `PATH` environment variable before you continue. For more information, see [Oracle Instant Client](#oracle-instant-client-for-thick-client-mode).
1. Select **Load Schemas**. The tool tests the Oracle connection and, if successful, lists all user-defined schemas available in Oracle.
1. Select one or more schemas to convert to PostgreSQL.
1. Select **Next** to continue.

   :::image type="content" source="media/schema-conversions-tutorial/connect-oracle.png" alt-text="Screenshot of configuring an Oracle server.":::

### Step 7: Configure an Azure Database for PostgreSQL scratch database

1. Select the **Azure Database for PostgreSQL connection** that you defined in the PostgreSQL extension.
1. Select the **target database** from the dropdown list.
1. Select **Next** to continue.

    :::image type="content" source="media/schema-conversions-tutorial/scratch-database.png" alt-text="Screenshot of configuring a scratch database.":::

### Step 8: Configure the Microsoft Foundry language model

1. Enter your **Microsoft Foundry details**:
   - Endpoint URL.
   - Deployment name (the name you assigned to the deployment in Microsoft Foundry; the underlying model must be `gpt-5.2`).
1. Select the **authentication method**:
   - **API key**: Enter the API key for your Microsoft Foundry deployment.
   - **Microsoft Entra ID**: Sign in with the Azure Account extension. The tool acquires the authentication token automatically. Make sure that the signed-in identity has the **Foundry User** role (formerly **Azure AI User**) on the Microsoft Foundry resource. For more information, see [Role-based access control for Microsoft Foundry](/azure/ai-foundry/concepts/rbac-azure-ai-foundry).
1. Select **Test Connection** to verify the configuration.
1. After the connection succeeds, select **Create Migration Project**.

    :::image type="content" source="media/schema-conversions-tutorial/language-model.png" alt-text="Screenshot of language model configuration.":::

### Step 9: Run the schema conversion

1. The system navigates to the main **Migration Wizard**.
1. Select **Migrate** to start the schema conversion process.
1. Monitor the conversion progress in the Visual Studio Code interface.

    :::image type="content" source="media/schema-conversions-tutorial/progress-bar.png" alt-text="Screenshot of Migration step progress.":::

### Step 10: Review the schema conversion report

1. After the schema conversion finishes, the tool generates a **schema conversion report**.
1. Review the objects that were converted successfully and the objects that were skipped.
1. The report displays the success percentage of the conversion.

### Step 11: Review and refine conversion tasks

1. After the schema conversion finishes, the tool creates **review tasks** for objects that need attention.
1. Use **GitHub Copilot agent mode** to resolve the tasks, or manually convert the schemas to PostgreSQL.
1. Compare the previous and the newly converted schema conversion statements.
1. For more information about task priorities, generated SQL files, and output folders, see [Review tasks and output folders for Oracle to Azure Database for PostgreSQL schema conversion](schema-conversions-review-tasks-artifacts.md).

### Step 12: Validate converted objects before deployment

1. Independently validate all converted objects in a nonproduction environment.
1. Confirm that dependencies, constraints, and representative workloads behave as expected.
1. Review the resolutions for all review tasks and retest after changes.

> [!IMPORTANT]
> Customer validation responsibility: The same AI engine used for schema conversion can also assist with validation and review. AI systems can occasionally confirm their own mistakes. To prevent data loss, functional regressions, or security issues, independently validate all converted objects and review-task resolutions before you deploy to production. As part of your controls, consider enabling Microsoft Foundry content filtering to help reduce harmful or undesired outputs. For guidance, see [Content filtering for Microsoft Foundry Models](/azure/ai-foundry/openai/concepts/content-filter).

For more information about the Visual Studio Code extension, visit [PostgreSQL extension for Visual Studio Code](../../extensions/vs-code-extension/overview.md).

## Related content

- [What is Oracle to Azure Database for PostgreSQL schema conversion?](schema-conversions-overview.md)
- [Review tasks and output folders for Oracle to Azure Database for PostgreSQL schema conversion](schema-conversions-review-tasks-artifacts.md)
- [Schema conversion limitations](schema-conversions-limitations.md)
