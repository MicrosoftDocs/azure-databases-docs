---
title: "Monitor the migration (online)"
description: Monitor the migration online.
author: apduvuri
ms.author: adityaduvuri
ms.reviewer: maghan
ms.date: 07/21/2025
ms.service: azure-database-postgresql
ms.topic: include
---
After you select the **Start validation and migration** button, a notification appears, in a few seconds, to say that the validation or migration creation is successful. You're automatically redirected to the flexible server's **Migration** page. The entry shows **Status** as **In progress**. The workflow takes 2 to 3 minutes to set up the migration infrastructure and check network connections.

:::image type="content" source="../media/tutorial-migration-service-online/monitor-migration.png" alt-text="Screenshot of the monitor migration page." lightbox="../media/tutorial-migration-service-online/monitor-migration.png":::

The grid that displays the migrations has the following columns: **Name**, **Status**, **Migration mode**, **Migration type**, **Source server**, **Source server type**, **Databases**, **Duration**, and **Start time**. The entries are displayed sorted by **Start time** in descending order, with the most recent entry on the top. You can use the **Refresh** button in the toolbar, to refresh the status of the validation or migration run.

### Migration details

Select the migration name in the grid to see the associated details.

Remember that in the previous steps, when you created this migration, you configured the migration option as **Validate and migrate**. In this scenario, validations are performed first, before migration starts. After the **Performing prerequisite steps** substrate is completed, the workflow moves into the substrate of **Validation in progress**.

- If validation has errors, the migration moves into a **Failed** state.

- If validation is complete without error, the migration starts, and the workflow moves into the substate of **Migrating Data**.

Validation details are available at the instance and database level.

- **Validation details for instance**
    - Contains validation related to the connectivity check, source version, that is, PostgreSQL version >= 9.5, and server parameter check, whether the extensions are enabled in the server parameters of the Azure Database for PostgreSQL flexible server.
- **Validation and migration details for databases**
    - It contains validation of the individual databases related to extensions and collations support in Azure Database for PostgreSQL flexible server.

You can see the **Validation status** and **Migration status** under the migration details page.

:::image type="content" source="../media/tutorial-migration-service-iaas-online/details-migration.png" alt-text="Screenshot of the details showing validation and migration." lightbox="../media/tutorial-migration-service-iaas-online/details-migration.png":::

Some possible migration statuses:

### Migration status

| Status | Description |
| --- | --- |
| **In progress** | The migration infrastructure setup is underway, or the actual data migration is in progress. |
| **Canceled** | The migration is canceled or deleted. |
| **Failed** | The migration has failed. |
| **Validation failed** | The validation has failed. |
| **Succeeded** | The migration has succeeded and is complete. |
| **Waiting for user action** | Waiting for user action to perform cutover. |

### Migration details

| Substatus | Description |
| --- | --- |
| **Performing prerequisite steps** | Infrastructure setup is underway for data migration. |
| **Validation in progress** | Validation is in progress. |
| **Dropping database on target** | Dropping already existing database on target server. |
| **Migrating data** | Data migration is in progress. |
| **Completing migration** | Migration is in the final stages of completion. |
| **Completed** | Migration has been completed. |
| **Failed** | Migration has failed. |

### Validation substatuses

| Substatus | Description |
| --- | --- |
| **Failed** | Validation has failed. |
| **Succeeded** | Validation is successful. |
| **Warning** | Validation is in warning. |
