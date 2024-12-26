---
title: "Migrate from Amazon Aurora offline by using the migration service"
description: Learn how to migrate offline seamlessly from Amazon Aurora to Azure Database for PostgreSQL by using the new migration service in Azure. Simplify the migration while ensuring data integrity and efficient deployment."
author: apduvuri
ms.author: adityaduvuri
ms.reviewer: maghan
ms.date: 08/30/2024
ms.service: azure-database-postgresql
ms.subservice: migration-guide
ms.topic: tutorial
ms.custom:
  - devx-track-azurecli
# customer intent: As a developer, I want to learn how to migrate from Amazon Aurora to Azure Database for PostgreSQL using the migration service, so that I can simplify the transition and ensure data integrity.
---

# Tutorial: Migrate offline from Amazon Aurora PostgreSQL to Azure Database for PostgreSQL with the migration service

This article describes how to migrate your PostgreSQL database from Amazon Aurora to Azure Database for PostgreSQL offline.

The migration service in Azure Database for PostgreSQL is a fully managed service that's integrated into the Azure portal and the Azure CLI. It's designed to simplify your migration journey to Azure Database for PostgreSQL.

In this tutorial, you:

> [!div class="checklist"]
>
> - Complete prerequisites
> - Initiate the migration
> - Monitor the migration
> - Verify the migration

## Prerequisites

[!INCLUDE [prerequisites-migration-service-postgresql-offline-aurora](includes/aurora/prerequisites-migration-service-postgresql-offline-aurora.md)]

## Initiate the migration

You can migrate by using the Azure portal or the Azure CLI.

# [Azure portal](#tab/azure-portal)

The Azure portal offers a simple and intuitive wizard-based experience to guide you through migration. By completing the steps that are outlined in this tutorial, you can seamlessly transfer your database to Azure Database for PostgreSQL - Flexible Server and take advantage of its powerful features and scalability.

To migrate by using the Azure portal, first configure the migration task. Then, connect to the source and target, and initiate the migration.

### Configure the migration task

To configure the migration task in the Azure portal:

1. Open your web browser and go to the [Azure portal](https://portal.azure.com/). Enter your credentials to sign in.

1. Go to your instance of Azure Database for PostgreSQL - Flexible Server.

1. On the service menu, select **Migration**.

    :::image type="content" source="media/tutorial-migration-service-aurora-offline/offline-portal-select-migration-pane.png" alt-text="Screenshot of the migration selection in the Azure portal." lightbox="media/tutorial-migration-service-aurora-offline/offline-portal-select-migration-pane.png":::

1. Select **Create** to migrate from Amazon Aurora to a flexible server.

   The first time you use the migration service, an empty grid appears with a prompt to begin your first migration. If migrations to your flexible server target are already created, the grid contains information about attempted migrations.

1. Select **Create** to step through a series of tabs to set up a migration.

    :::image type="content" source="media/tutorial-migration-service-aurora-offline/portal-offline-create-migration.png" alt-text="Screenshot of the Create migration pane." lightbox="media/tutorial-migration-service-aurora-offline/portal-offline-create-migration.png":::

#### Setup

Enter or select the following information:

- **Migration name**: Enter a unique identifier for each migration to this flexible server target. You can use only alphanumeric characters and hyphens (`-`) in the migration name. The name can't start with a hyphen, and it must be unique for a target server. No two migrations to the same flexible server target can have the same name.

- **Source server type**: Select the source type that corresponds to your PostgreSQL source, such as a cloud-based PostgreSQL service, an on-premises setup, or a virtual machine.

- **Migration option**: Choose one of the following options for a pre-migration validation:

  - **Validate**. Checks your server and database readiness for migration to the target source.
  - **Migrate**. Skips validations and starts the migration.
  - **Validate and Migrate**. Performs validation before triggering a migration. If there are no validation failures, the migration is triggered.

  A good practice is to select the **Validate** or **Validate and Migrate** option for pre-migration validations.

  For more information, see [Premigration validations](concepts-premigration-migration-service.md).

- **Migration mode**: Select the mode for the migration. The default option is **Offline**.

Select **Next: Connect to source**.

:::image type="content" source="media/tutorial-migration-service-aurora-offline/01-portal-offline-setup-aurora.png" alt-text="Screenshot of the migration Setup tab in the Azure portal.":::

#### Select the runtime server

The migration runtime server is a specialized feature of the migration service. The runtime server acts as an intermediary server during migration. It's a separate instance of Azure Database for PostgreSQL - Flexible Server that isn't the target server. The runtime server facilitates the migration of databases from a source environment that is accessible only via a private network.

For more information, see [Migration runtime server](concepts-migration-service-runtime-server.md).

:::image type="content" source="media/tutorial-migration-service-aurora-offline/02-portal-offline-runtime-server-aurora.png" alt-text="Screenshot of the Migration Runtime Server tab.":::

#### Connect to the source

On the **Connect to source** tab, enter or select the following information for the database source:

- **Server name**: Enter the host name or the IP address of the source PostgreSQL instance.
- **Port**: Enter the port number of the source server.
- **Server admin login name**: Enter the username of the source PostgreSQL server.
- **Password**: Enter the password of the source PostgreSQL server.
- **SSL mode**: Supported values are **Prefer** and **Require**. When Secure Sockets Layer (SSL) at the source PostgreSQL server is off, select **Prefer**. If SSL at the source server is on, select **Require**. SSL values are set in the *postgresql.conf* file.
- **Test Connection**: Initiates a connectivity test between the target and the source. When the connection is successful, go to the next step to identify networking issues between the target and source and to verify the username and password for the source. Establishing a test connection takes a few minutes.

After a successful test connection, select **Next: Select migration target**.

:::image type="content" source="media/tutorial-migration-service-aurora-offline/03-portal-offline-connect-source-aurora.png" alt-text="Screenshot of the Connect to source tab." lightbox="media/tutorial-migration-service-aurora-offline/03-portal-offline-connect-source-aurora.png":::

#### Select the migration target

On the **Select migration target** tab, enter or select the following information for the flexible server target, in addition to subscription, resource group, and server name:

- **Admin username**: The admin username of the target PostgreSQL server.
- **Password**: The password of the target PostgreSQL server.
- **Custom FQDN/IP (Optional)**: The custom FQDN/IP field is optional and can be used when the target is behind a custom DNS server or has custom DNS namespaces, making it accessible only via specific FQDNs or IP addresses. For example, this could include entries like `flexibleserver.example.com`, `198.1.0.2`, or a PostgreSQL FQDN such as `flexibleserver.postgres.database.azure.com`, if the custom DNS server contains the DNS zone `postgres.database.azure.com` or forwards queries for this zone to `168.63.129.16`, where the FQDN is resolved in the Azure public or private DNS zone.
- **Test Connection**: Initiates a connectivity test between the target and the source. When the connection is successful, go to the next step to identify networking issues between the target and source and to verify the username and password for the target server. Establishing a test connection takes a few minutes.

After a successful test connection, select **Next: Select database(s) for migration**.

:::image type="content" source="media/tutorial-migration-service-aurora-offline/04-portal-offline-select-migration-target-aurora.png" alt-text="Screenshot of the Connect target migration tab.":::

#### Select databases for migration

On the **Select database for migration** tab, select from a list of user databases to migrate from your source PostgreSQL server.

After you select the databases, select **Next: Summary**.

:::image type="content" source="media/tutorial-migration-service-aurora-offline/05-portal-offline-select-database-aurora.png" alt-text="Screenshot of the Select databases for migration tab.":::

#### Summary

The **Summary** tab summarizes all the source and target details for creating the validation or migration. Review the details, and then select **Start Validation and Migration**.

:::image type="content" source="media/tutorial-migration-service-aurora-offline/06-portal-offline-summary-aurora.png" alt-text="Screenshot of the Summary migration pane.":::

### Monitor the migration

Within a few seconds after you select **Start Validation and Migration**, a notification appears to say that the validation or migration creation is successful. You're redirected to the Flexible Server instance **Migration** pane. The state entry is **InProgress** and the substate is **PerformingPreRequisiteSteps**. The workflow takes 2 to 3 minutes to set up the migration infrastructure and check network connections.

:::image type="content" source="media/tutorial-migration-service-aurora-offline/portal-offline-monitor-migration-aurora.png" alt-text="Screenshot of the Monitor migration pane." lightbox="media/tutorial-migration-service-aurora-offline/portal-offline-monitor-migration-aurora.png":::

The grid that displays the migrations has these columns:

- **Name**
- **Status**
- **Migration mode**
- **Migration type**
- **Source server**
- **Source server type**
- **Databases**
- **Duration**
- **Start time**

The entries are displayed in descending order of start time, with the most recent entry on the top. You can select **Refresh** in the menu bar to refresh the status of the validation or migration run.

#### Migration details

In the list of migrations, select the name of a migration to see associated details.

On the **Setup** tab, select the migration option **Validate and Migrate**. In this scenario, validations are completed before migration starts. After the **PerformingPreRequisiteSteps** substate is completed, the workflow moves into the **Validation in Progress** substate.

- If validation has errors, the migration moves into a **Failed** state.

- If validation is complete without any error, the migration starts, and the workflow moves into the substate **Migrating Data**.

You can check validation details at the instance level and at the database level:

- Validation at the instance level:

  - Check validation related to the connectivity check for the source version (the `PostgreSQL version >= 9.5` server parameter check) if the extensions are enabled in the server parameters of the instance of Azure Database for PostgreSQL - Flexible Server.

- Validation at the database level:

  - Check validation of the individual databases related to extensions and collations support in Azure Database for PostgreSQL - Flexible Server.

You can see the current status for the migration and validation on the migration details pane.

:::image type="content" source="media/tutorial-migration-service-aurora-offline/portal-offline-details-migration-aurora.png" alt-text="Screenshot of the details that show validation and migration." lightbox="media/tutorial-migration-service-aurora-offline/portal-offline-details-migration-aurora.png":::

The following tables describe some possible migration states and substates.

#### Migration states

| State | Description |
| --- | --- |
| **InProgress** | The migration infrastructure setup is underway, or the actual data migration is in progress. |
| **Canceled** | The migration is canceled or deleted. |
| **Failed** | The migration failed. |
| **Validation failed** | The validation failed. |
| **Succeeded** | The migration succeeded and is completed. |
| **WaitingForUserAction** | Applicable only in online migrations. Waiting for a user to perform a cutover. |

#### Migration substates

| Substate | Description |
| --- | --- |
| **PerformingPreRequisiteSteps** | Infrastructure setup is underway for data migration. |
| **Validation in Progress** | Validation is in progress. |
| **MigratingData** | Data migration is in progress. |
| **CompletingMigration** | Migration is in the final stages of completion. |
| **Completed** | Migration is completed. |
| **Failed** | Migration failed. |

#### Validation substates

| Substate | Description |
| --- | --- |
| **Failed** | Validation failed. |
| **Succeeded** | Validation is successful. |
| **Warning** | Validation shows a warning. |

### Cancel the migration

You can cancel any ongoing validations or migrations. The workflow must be in the **In progress** state to be canceled. You can't cancel a validation or migration that's in the **Succeeded** or **Failed** state.

Canceling a migration stops further migration activity on your target server and moves the migration attempt to a **Canceled** state. The cancel action rolls back all changes made on your target server by the migration service.

# [Azure CLI](#tab/azure-cli)

This article describes how to use the Azure CLI to migrate your PostgreSQL database from Amazon Aurora to Azure Database for PostgreSQL. The Azure CLI is a powerful and flexible command-line interface that you can use to complete various tasks, including database migration.

For more information, see [Set up the Azure CLI for the migration service](how-to-setup-azure-cli-commands-postgresql.md).

After the Azure CLI is installed, at the command line, sign in to your Azure account by using the following command:

```azurecli-interactive
az login
```

### Configure the migration task

1. To begin the migration, create a JSON file to hold the migration details. Save the JSON file on your local computer as *[filename].json*. For example, you can save the file as *C:\migration-CLI\migration_body.json*.

   Copy the following JSON and paste it in the JSON file. Replace `<placeholders>` with relevant information from your scenario.

    ```json
    {
    "properties": {
    "SourceDBServerResourceId": "<source host name or IP address>:<port>@<username>",
            "SecretParameters": {
                "AdminCredentials": {
                    "SourceServerPassword": "<source password>",
                    "TargetServerPassword": "<target password>"
                },
                "targetServerUserName": "<target username>"
            },
            "DBsToMigrate": "<a comma-separated list of databases in an array, similar to the example "ticketdb","timedb","inventorydb">",
            "OverwriteDBsInTarget": "true",
            "sourceType": "AWS_AURORA",
            "sslMode": "Require"
        }
    }
    ```

1. Run the following command to check if any migrations are running. The migration name is unique for migrations in the Azure Database for PostgreSQL - Flexible Server target.

    ```azurecli-interactive
    az postgres flexible-server migration list --subscription 11111111-1111-1111-1111-111111111111 --resource-group my-learning-rg --name myflexibleserver --filter All
    ```

1. In the preceding steps, there are no migrations performed so we start with the new migration by running the following command

    ```azurecli-interactive
    az postgres flexible-server migration create --subscription 11111111-1111-1111-1111-111111111111 --resource-group my-learning-rg --name myflexibleserver --migration-name migration1 --migration-mode offline --migration-option ValidateAndMigrate --properties "C:\migration-cli\migration_body.json"
    ```

1. Run the following command to initiate the migration status in the previous step. You can check the status of the migration by providing the migration name

    ```azurecli-interactive
    az postgres flexible-server migration show --subscription 11111111-1111-1111-1111-111111111111 --resource-group my-learning-rg --name myflexibleserver --migration-name migration1
    ```

   The status of the migration progress is shown in the Azure CLI. You also can see the status of the instance of Azure Database for PostgreSQL - Flexible Server in the Azure portal.

### Cancel or delete a migration

You can cancel any ongoing migration attempts by using the `cancel` command. This command stops the specific migration attempt and rolls back all changes on your target server.

Here's the Azure CLI command to delete a migration:

```azurecli-interactive
az postgres flexible-server migration update cancel --subscription 11111111-1111-1111-1111-111111111111 --resource-group my-learning-rg --name myflexibleserver --migration-name migration1
```

---

## Verify the migration

When the database migration is finished, manually validate the data between the source and the target. Verify that all the objects in the target database are successfully created.

After migration, you can complete these tasks:

- Verify the data on your flexible server and ensure that it's an exact copy of the source instance.
- After verification, enable the high-availability option on your flexible server as needed.
- Change the SKU (version) of the flexible server to match the needs of your application. This change requires a restart of the database server.
- If you change any server parameters from their default values in the source instance, copy those server parameter values to the flexible server.
- Copy other server settings, such as tags, alerts, and firewall rules (if applicable), from the source instance to the flexible server.
- Make changes to your application to point the connection strings to a flexible server.
- Monitor the database performance closely to see if it requires performance tuning.

## Related content

- [Migrate online from Amazon Aurora PostgreSQL](tutorial-migration-service-aurora-online.md)
- [Migration service](concepts-migration-service-postgresql.md)
- [Migrate from on-premises and Azure VMs](tutorial-migration-service-iaas.md)
- [Known issues and limitations](concepts-known-issues-migration-service.md)
