---
title: "Oracle to PostgreSQL migration"
description: "Migrate from Oracle to PostgreSQL using the built-in migration tools with AI-assisted schema and application code conversion. Visual Studio Code only."
author: mmcfarland
ms.author: mattmcfarland
ms.date: 05/21/2026
ms.service: postgresql
ms.subservice: vs-code-pgsql-extensions
ms.topic: how-to
---


# Oracle to PostgreSQL migration

The PostgreSQL extension for Visual Studio Code provides an end-to-end workflow for migrating Oracle databases to PostgreSQL. A guided wizard walks you through connecting to your Oracle source, selecting schemas, configuring a Microsoft Foundry model for AI-assisted DDL conversion, and choosing a PostgreSQL scratch database for validation. After the project is created, a dashboard tracks extraction, conversion, export, and review in a single view.

> [!IMPORTANT]
> **The Oracle to PostgreSQL migration workflow is available in Visual Studio Code only.**

## Prerequisites

Before you begin, ensure you have:

- [Visual Studio Code](https://code.visualstudio.com/) installed.
- The [PostgreSQL extension](https://marketplace.visualstudio.com/items?itemName=ms-ossdata.vscode-pgsql) installed.
- Access to an Oracle source database with read permissions for schema extraction.
- A PostgreSQL instance to use as a scratch validation database (for example, an Azure Database for PostgreSQL Flexible Server).
- A Microsoft Foundry resource with a deployed `gpt-5.2` model. You need the endpoint URL and either an API key or a Microsoft Entra ID account with access.

## Verify the migrations feature is enabled

The `pgsql.enableMigrations` setting controls the **Migrations (Preview)** view and all migration commands. This setting is enabled by default.

If the **Migrations (Preview)** view doesn't appear in the sidebar, verify the setting:

1. Open VS Code settings (<kbd>Ctrl</kbd>+<kbd>,</kbd> on Windows/Linux, <kbd>Cmd</kbd>+<kbd>,</kbd> on macOS).
1. Search for `pgsql.enableMigrations`.
1. Confirm the value is `true`.

## Create a migration project

A migration project is a four-step wizard that collects your source, target, and AI configuration before creating the project workspace.

### Step 1: Project setup

1. Open the **Migrations (Preview)** view in the sidebar.
1. Select the **+** button in the view toolbar, or right-click a workspace folder in Explorer and select **Create Migration Project**.

   The **New Oracle to Azure Database for PostgreSQL migration project** page opens, listing what you need:

   - Connection details for the source database
   - Name of the schema(s) to convert
   - Endpoint URL and key for a Microsoft Foundry resource
   - Connection name for an existing PostgreSQL instance

1. Enter a name in the **Project Name** field.
1. Select **Next: Oracle Connection**.

:::image type="content" source="./media/screenshots/vscode/oracle-migration/migration-project-setup.png" alt-text="New migration project page with Project Name field" lightbox="./media/screenshots/vscode/oracle-migration/migration-project-setup.png":::

### Step 2: Connect to Oracle

The **Connect to Oracle** page collects your Oracle source database credentials and lets you load schemas.

1. Complete the Oracle connection fields:

   | Field | Description |
   |---|---|
   | **Oracle Hostname** | Hostname or IP address of the Oracle database server. |
   | **Oracle Port** | Listener port (default: `1521`). |
   | **Oracle SID or Service Name** | Oracle SID or service name for the database instance. |
   | **Oracle Username** | Database user with read access to schema objects. |
   | **Oracle Password** | Password for the Oracle user. |

1. Select **Load Schemas** to connect and retrieve the list of available schemas.
1. In the **Schemas** dropdown, select one or more schemas to migrate.
1. Select **Next: PostgreSQL Connection**.

### Step 3: Choose an Azure Database for PostgreSQL scratch database

The **Choose an Azure Database for PostgreSQL scratch database** page selects the PostgreSQL instance that the AI model uses to validate converted DDL files.

> [!NOTE]
> Use a dedicated scratch database for validation. The extension might execute converted DDL against this database during the conversion process.

1. In the **PostgreSQL Connection** dropdown, select an existing connection profile. If the connection you need isn't listed, select **Refresh Profiles** to reload available profiles, or create a new connection in the [Connections](connections.md) view first.
1. In the **PostgreSQL Database** dropdown, select the target database. Select **Load Databases** if the list is empty.
1. After you select a database, the extension automatically verifies that recommended PostgreSQL extensions are installed. You can also select **Verify Extensions** to run the check manually. If any extensions are missing, the page lists them and provides guidance on allowlisting and installing them through the Azure Database for PostgreSQL Flexible Server documentation.
1. Select **Next: Microsoft Foundry Model Configuration**.

### Step 4: Configure the Microsoft Foundry model

The **Choose a Microsoft Foundry Model** page configures the Microsoft Foundry deployment that powers schema and code conversion.

1. Complete the language model fields:

   | Field | Description |
   |---|---|
   | **Model Name** | `gpt-5.2`. |
   | **Microsoft Foundry Endpoint** | Microsoft Foundry resource endpoint URL (for example, `https://<resource>.openai.azure.com/`). |
   | **Authentication Method** | Choose **API Key** or **Microsoft Entra Id**. |
   | **Microsoft Foundry API Key** | API key for the Microsoft Foundry resource (shown when **Authentication Method** is **API Key**). |
   | **Azure Account** | Microsoft account with access to the resource (shown when **Authentication Method** is **Microsoft Entra Id**). |
   | **Tenant** | Azure AD tenant for the account (shown when **Authentication Method** is **Microsoft Entra Id**). |
   | **Deployment Name** | Name of the deployed model in your Microsoft Foundry resource. |

1. Select **Test Microsoft Foundry Connection** to verify connectivity.
1. Select **Create Migration Project**.

> [!TIP]
> Microsoft Foundry recommends 500,000 TPM (Tokens Per Minute) for optimal migration performance.

## Run schema migration

After the project is created, the **Oracle Migration** dashboard opens. The dashboard displays **Schema Migration** and **Schema Review** cards, along with a **Settings** accordion that summarizes your project configuration.

### Extract and convert schemas

The **Schema Migration** card (Step 1) runs extraction, conversion, and export as a continuous pipeline.

1. On the **Schema Migration** card, select **Migrate**.

   The button label updates as the pipeline progresses:

   | Status | Button label |
   |---|---|
   | Extraction running | **Extracting ...** |
   | Extraction complete, conversion pending | **Resume Migration** |
   | Conversion running | **Converting ...** |
   | All phases complete | **Migration Complete** |

1. Monitor progress in the expanded card:
   - **Extraction** shows the count of extracted objects (for example, "15 of 42 objects extracted") and the current schema and object being processed.
   - **Conversion** shows the count of converted chunks (for example, "3 of 8 Chunks converted") and the current chunk being processed.
1. After export completes, select **View Migration Report** to open the generated migration report.

### Review migration tasks

The **Schema Review** card (Step 2) displays items that require manual attention after conversion. A **Grouped** / **Tasks** switcher at the top of the review area lets you choose how to work through the list.

#### Grouped view

The **Grouped** view organizes review tasks into collapsible accordion groups by category. Use this view when you want to process related issues together.

<!-- visual:oracle-migration.review-task-groups pending screenshot capture (manual environment — png pending: ./media/screenshots/vscode/oracle-migration/review-task-groups.png) -->

1. On the **Schema Review** card, select **Review** to expand the review surface, then select **Grouped**.
1. Use the **Pending** and **Resolved** tabs to switch between tasks that still need attention and tasks you have already approved.
1. Expand a group to see its metadata (schemas, object types, criticality) and the individual task cards inside it.
1. Use the group-level actions to process tasks in bulk:

   | Action | Description |
   |---|---|
   | **Run all** | Open every pending task in the group in Copilot Agent Mode for AI-assisted review. |
   | **Resolve all** | Mark all tasks in the group as resolved. A confirmation dialog shows the group name and task count before proceeding. |
   | **Reset all** | Return all resolved tasks in the group to the pending state. Available on the **Resolved** tab. |
   | **View in Tasks** | Switch to the flat **Tasks** view filtered to this group. |

1. To act on a single task inside the group, select **Run Task** to open it in Copilot Agent Mode, or select **Resolve** to mark it complete. Select **Reset** on a resolved task to return it to the pending state.

> [!NOTE]
> **Resolve all** and **Reset all** are disabled when a group contains more than 800 tasks.

#### Tasks view

The **Tasks** view shows all review tasks in a flat table. Use this view when you want to sort, filter, or search across all tasks regardless of group.

1. Select **Tasks** in the switcher.
1. Use the filter dropdowns (**Status**, **Criticality**, **Object Type**, **Schema**) to narrow the task list.
1. Select **Run Task** on a pending item to open it in Copilot Agent Mode for AI-assisted review and correction.
1. After fixing an item, select **Resolve** to mark it complete.

> [!TIP]
> Select **View Logs** in the dashboard to inspect extraction and conversion log files for troubleshooting.

## Migrate application code

After schema migration, convert Oracle-specific application code (SQL scripts, stored procedures, loader control files, shell scripts, or Java files) to PostgreSQL-compatible equivalents. Application migration is a Preview feature.

### Choose a migration method

The extension offers two paths for application code migration:

- **Full app modernization** &mdash; If the GitHub Copilot app modernization extension is installed, select **Migrate using app modernization** to continue the migration with coding notes from the schema conversion. Select **View coding notes** to review the generated guidance before proceeding.
- **Database-only option** &mdash; To convert only database-related application code within this extension, select **Migrate using PostgreSQL extension**.

### Convert application code within the extension

1. On the **Application Migration** card, select **Migrate Data** (or **Select Method** if the app modernization extension is detected).
1. In the **Convert Application** page, select **Select Oracle Application to Convert** and choose the folder that contains Oracle application code.
1. Select a **PostgreSQL Connection** and **PostgreSQL Database** for conversion context.
1. Select **Load Databases** if the database list is empty.
1. Select **Convert Application** to start the conversion.

### Use Copilot tools for application migration

The extension registers two Copilot language model tools for migration assistance:

- **Oracle Client Code Application Converter** (`pgsql_migration_oracle_app`) &mdash; Converts Oracle client application code to PostgreSQL equivalents using prompt templates and coding guidance from the schema migration analysis. Accepts the following parameters:
  - **Application Codebase Folder** (required) &mdash; Location of the code to convert.
  - **Coding Notes Location Path** (optional) &mdash; Path to coding notes from the schema migration.
  - **Postgres DB Name** (optional) &mdash; Name of the PostgreSQL database for conversion context.
  - **Postgres DB Connection** (optional) &mdash; Connection name for the PostgreSQL database.

- **Show Oracle to Postgres Migration Report** (`pgsql_migration_show_report`) &mdash; Displays the migration report generated by the schema conversion. Requires a **Path to Report File** parameter.

For more information on using Copilot tools, see [Copilot integration](copilot-integration.md).

## Compare converted files

After conversion, review changes side by side using the built-in diff commands.

1. In Explorer, right-click a converted SQL file under the `oracle` or `postgres` folder in the migration project and select **Compare DDL Migration File Pairs**.
1. For converted application code files (`.sql`, `.ctl`, `.sh`, `.load`, or `.java`), right-click the file and select **Compare Application Migration File Pairs**.

The side-by-side diff view shows the original Oracle source alongside the converted PostgreSQL output, so you can identify any artifacts that require manual adjustment.

> [!NOTE]
> DDL files must follow the structure `folder/oracle|postgres/SCHEMA_NAME/DDL-TYPE/filename.sql` for the compare command to locate the matching file pair.

## Manage migration projects

Use the **Migrations (Preview)** view in the sidebar to manage your projects:

| Action | Description |
|---|---|
| **Open Migration Project** | Open an existing migration project in the dashboard. |
| **Reveal in Explorer** | Show the project folder in the Explorer view. |
| **Delete** | Remove a migration project. You're prompted to confirm before deletion. |
| **Refresh** | Reload the list of migration projects in the current workspace. |

## Related content

- [Copilot integration](copilot-integration.md)
- [Connections and identity](connections.md)
- [Extension settings reference](reference/settings.md)
- [Copilot tools reference](reference/copilot-tools.md)
