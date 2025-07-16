---
title: "Migrate Offline From an Azure VM or an On-Premises PostgreSQL Server to Azure Database for PostgreSQL, the Migration Service"
description: "Learn to migrate seamlessly from Azure VM or an on-premises PostgreSQL server to Azure Database for PostgreSQL using the new migration service in Azure."
author: apduvuri
ms.author: adityaduvuri
ms.reviewer: maghan
ms.date: 07/16/2025
ms.service: azure-database-postgresql
ms.subservice: migration-guide
ms.topic: tutorial
ms.custom:
- devx-track-azurecli
- sfi-image-nochange
# CustomerIntent: As a user, I want to learn how to perform offline migration from on-premises and Azure virtual machines to Azure Database for PostgreSQL flexible server using the migration service in Azure, so that I can simplify the transition and ensure data integrity and efficient deployment.
---

# Tutorial: Migrate offline from an Azure VM or an on-premises PostgreSQL server to Azure Database for PostgreSQL with the migration service

This article guides you in migrating a PostgreSQL instance from your on-premises or Azure virtual machines (VMs) to Azure Database for PostgreSQL flexible server in offline mode.

The migration service in Azure Database for PostgreSQL is a fully managed service integrated into the Azure portal and Azure CLI. It's designed to simplify your migration journey to the Azure Database for PostgreSQL flexible server.

> [!div class="checklist"]
>  
> - Prerequisites
> - Perform the migration
> - Monitor the migration
> - Check the migration when completed

## Prerequisites

To begin the migration, you need the following prerequisites:

[!INCLUDE [prerequisites-migration-service-postgresql-offline-iaas](includes/iaas/prerequisites-migration-service-postgresql-offline-iaas.md)]

## Perform the migration

You can migrate by using Azure portal or Azure CLI.

### [Portal](#tab/portal)

This article guides you using the Azure portal to migrate your PostgreSQL database from an Azure VM or an on-premises PostgreSQL server to an Azure Database for PostgreSQL. The Azure portal allows you to perform various tasks, including database migration. Following the steps outlined in this tutorial, you can seamlessly transfer your database to Azure and take advantage of its powerful features and scalability.

### Configure the migration task

The migration service comes with a simple, wizard-based experience on the Azure portal.

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

1. In the resource menu, select **Migration**.

    :::image type="content" source="media/tutorial-migration-service-iaas-offline/portal-offline-select-migration-pane.png" alt-text="Screenshot of the Migration page." lightbox="media/tutorial-migration-service-iaas-offline/portal-offline-select-migration-pane.png":::

1. Select **Create** to go through a wizard-based series of tabs to perform a migration to a flexible server from on-premises or Azure VM.

    > [!NOTE]
    > The first time you use the migration service, an empty grid appears with a prompt to begin your first migration.

    If migrations to your flexible server target have already been created, the grid now contains information about attempted migrations.

    :::image type="content" source="media/tutorial-migration-service-iaas-offline/portal-offline-create-migration.png" alt-text="Screenshot of the Setup tab which appears after selecting Create in the Migration page." lightbox="media/tutorial-migration-service-iaas-offline/portal-offline-create-migration.png":::

#### Setup

You need to provide multiple details related to the migration, like the migration name, source server type, option, and mode.

- **Migration name** is the unique identifier for each migration to this Flexible Server target. This field accepts only alphanumeric characters and doesn't accept any special characters except a hyphen (-). The name can't start with a hyphen and should be unique for a target server. No two migrations to the same flexible server target can have the same name.

- **Source server type** - Depending on your PostgreSQL source, you can select **Azure Virtual Machine** or **On-premise Server**.

- **Migration option** - Allows you to perform validations before triggering a migration. You can pick any of the following options:
    - **Validate** - Checks your server and database readiness for migration to the target.
    - **Validate and migrate** — Performs validation before triggering a migration. If there are no validation failures, the migration is initiated.

Choosing the **Validate** or **Validate and migrate** option is always a good practice for performing premigration validations before running the migration.

To learn more about the premigration validation, visit [premigration](concepts-premigration-migration-service.md).

- **Migration mode** allows you to pick the mode for the migration. **Offline** is the default option. In this case, we'll use the default.

Select **Next: Runtime server**.

:::image type="content" source="media/tutorial-migration-service-iaas-offline/portal-offline-setup-migration-iaas.png" alt-text="Screenshot of the Setup tab after providing necessary details.":::

#### Runtime server

The migration runtime server is a specialized feature within the [migration service in Azure Database for PostgreSQL](concepts-migration-service-postgresql.md), designed to act as an intermediary server during migration. It's a separate Azure Database for PostgreSQL flexible server instance that isn't the target server, but is used to facilitate the migration of databases from a source environment that is only accessible via a private network.

:::image type="content" source="media/tutorial-migration-service-iaas-offline/portal-offline-runtime-server-migration-iaas.png" alt-text="Screenshot of the Runtime server tab.":::

For more information about the runtime server, visit [Migration runtime server](concepts-migration-service-runtime-server.md).

#### Source server

The **Source server** tab prompts you to give details related to the source selected in the **Setup** tab, which is the source of the databases.

- **Server name** - Provide the name of the host or the IP address of the source PostgreSQL server.
- **Port** - Port number of the source server.
- **Admininistrator login** - Name of the administrator user of the source PostgreSQL server.
- **Password** - Password of the administrator login provided to connect to source PostgreSQL server.
- **SSL mode** - Supported values are `preferred` and `required`. When the SSL at the source PostgreSQL server is `OFF`, use `prefer`. If the SSL at the source server is `ON`, use the `require`. SSL values can be determined in postgresql.conf file of the source server.
- **Test connection** — Performs the connectivity test between the target and source. Once the connection is successful, you can proceed to the next tab. These test aims to identify any connectivity issues that might exist between the target and source servers, including verification of authentication using the credentials supplied. Establishing a test connection takes a few seconds.

After the successful test connection, select **Next: Target server**.

:::image type="content" source="media/tutorial-migration-service-iaas-offline/portal-offline-source-server-migration-iaas.png" alt-text="Screenshot of Source server migration tab.":::

#### Target server

The **Target server** tab displays metadata for the flexible server target, such as the subscription name, resource group, server name, location, and PostgreSQL version.

- **Admininistrator login** - Name of the administrator user of the target PostgreSQL server.
- **Password** - Password of the administrator login provided to connect to target PostgreSQL server.
- **Custom FQDN or IP address**: The custom FQDN or IP address field is optional, and can be used when the target is behind a custom DNS server or has custom DNS namespaces, making it accessible only via specific FQDNs or IP addresses. For example, this could include entries like `production-flexible-server.example.com`, `198.1.0.2`, or a PostgreSQL FQDN such as `production-flexible-server.postgres.database.azure.com`, if the custom DNS server contains the DNS zone `postgres.database.azure.com` or forward queries for this zone to `168.63.129.16`, where the FQDN is resolved in the Azure public or private DNS zone.
- **Test connection** — Performs the connectivity test between the source and target. Once the connection is successful, you can proceed to the next tab. These test aims to identify any connectivity issues that might exist between the source and target servers, including verification of authentication using the credentials supplied. Establishing a test connection takes a few seconds.

After the successful test connection, select the **Next: Databases to validate or migrate**

:::image type="content" source="media/tutorial-migration-service-iaas-offline/portal-offline-target-server-migration-iaas.png" alt-text="Screenshot of the Target server migration tab.":::

#### Databases to validate or migrate

Under the **Databases to validate or migrate** tab, you can choose a list of user databases to migrate from your source PostgreSQL server.

After selecting the databases, select **Next: Summary**.

:::image type="content" source="media/tutorial-migration-service-iaas-offline/portal-offline-databases-to-validate-or-migrate-migration-iaas.png" alt-text="Screenshot of the Databases to validate or migrate  migration tab.":::

#### Summary

The **Summary** tab summarizes all the source and target details for creating the validation or migration. Review the details and select **Start validation and migration**.

:::image type="content" source="media/tutorial-migration-service-iaas-offline/portal-offline-summary-migration-iaas.png" alt-text="Screenshot of the Summary migration tab.":::

### Cancel the migration using the portal

You can cancel any ongoing validations or migrations. The workflow must be in the **In progress** status so that it can be canceled. You can't cancel a validation or migration in the **Succeeded** or **Failed** state.

- Canceling a validation stops further validation activity, and the validation moves to a **Canceled** state.
- Canceling a migration stops further migration activity on your target server and moves to a **Canceled** state. The cancel action returns all changes the migration service makes on your target server.

#### [CLI](#tab/cli)

This article explores using the Azure CLI to migrate your PostgreSQL database from an Azure virtual machine or an on-premises PostgreSQL instance to an Azure Database for PostgreSQL. The Azure CLI provides a powerful and flexible command-line interface that allows you to perform various tasks, including database migration. Following the steps outlined in this article, you can seamlessly transfer your database to Azure and take advantage of its powerful features and scalability.

To learn more about Azure CLI with the migration service, visit [How to set up Azure CLI for the migration service](how-to-setup-azure-cli-commands-postgresql.md).

Once the CLI is installed, open the command prompt and log into your Azure account using the below command.

```azurecli-interactive
az login
```

### Configure the migration task

To begin the migration, create a JSON file with the migration details. The JSON file contains the following information:

- Edit the below placeholders `<< >>` in the JSON lines and store them in the local machine as `<<filename>>.json` where the CLI is being invoked. In this tutorial, we have saved the file in C:\migration-CLI\migration_body.json

```bash
{
"properties": {
"SourceDBServerResourceId": "<<source hostname or IP address>>:<<port>>@<<username>>",
        "SecretParameters": {
            "AdminCredentials": {
                "SourceServerPassword": "<<Source Password>>",
                "TargetServerPassword": "<<Target Password>>"
            },
            "targetServerUserName": "<<Target username>>"
        },
        "DBsToMigrate": "<<comma separated list of databases in a array like - ["ticketdb","timedb","inventorydb"]>>",
        "OverwriteDBsInTarget": "true",
        "sourceType": "OnPremises",
        "sslMode": "Prefer"
    }
}
```

> [!NOTE]  
> When configuring the JSON properties for the migration to Azure Database for PostgreSQL Flexible Server, if your source environment is an Azure Virtual Machine, you can specify the source type using the `"sourceType":"AzureVM"` property. This helps the migration service understand the environment from which the data is being migrated.

- Run the following command to check if any migrations are running. The migration name is unique across the migrations within the Azure Database for PostgreSQL flexible server target.

    ```azurecli-interactive
    az postgres flexible-server migration list --subscription 11111111-1111-1111-1111-111111111111 --resource-group my-learning-rg --name myflexibleserver --filter All
    ```

- In the above steps, there are no migrations performed so we start with the new migration by running the following command

    ```azurecli-interactive
    az postgres flexible-server migration create --subscription 11111111-1111-1111-1111-111111111111 --resource-group my-learning-rg --name myflexibleserver --migration-name migration1 --migration-mode offline --migration-option ValidateAndMigrate --properties "C:\migration-cli\migration_body.json"
    ```

- Run the following command to initiate the migration status in the previous step. You can check the status of the migration by providing the migration name

    ```azurecli-interactive
    az postgres flexible-server migration show --subscription 11111111-1111-1111-1111-111111111111 --resource-group my-learning-rg --name myflexibleserver --migration-name migration1
    ```

- The status of the migration progress is shown in the Azure CLI.
- You can also see the status of the Azure Database for PostgreSQL flexible server in the Azure portal.

- You can cancel any ongoing migration attempts using the `cancel` command. This command stops the particular migration attempt and rolls back all changes on your target server. Here's the CLI command to delete a migration:

    ```azurecli-interactive
    az postgres flexible-server migration update cancel --subscription 11111111-1111-1111-1111-111111111111 --resource-group my-learning-rg --name myflexibleserver --migration-name migration1
    ```

---

## Monitor the migration

After you select the **Start validation and migration** button, a notification appears, in a few seconds, to say that the validation or migration creation is successful. You're automatically redirected to the flexible server's **Migration** page. The entry shows **Status** as **In progress**. The workflow takes 2 to 3 minutes to set up the migration infrastructure and check network connections.

:::image type="content" source="media/tutorial-migration-service-iaas-offline/portal-offline-monitor-migration.png" alt-text="Screenshot of the monitor migration page." lightbox="media/tutorial-migration-service-iaas-offline/portal-offline-monitor-migration.png":::

The grid that displays the migrations has the following columns: **Name**, **Status**, **Migration mode**, **Migration type**, **Source server**, **Source server type**, **Databases**, **Duration**, and **Start time**. The entries are displayed sorted by **Start time** in descending order, with the most recent entry on the top. You can use the **Refresh** button in the toolbar, to refresh the status of the validation or migration run.

### Migration details

Select the migration name in the grid to see the associated details.

Remember that in the previous steps, when you created this migration, you configured the migration option as **Validate and migrate**. In this scenario, validations are performed first, before migration starts. After the **PerformingPreRequisiteSteps** substrate is completed, the workflow moves into the substrate of **Validation in Progress**.

- If validation has errors, the migration moves into a **Failed** state.

- If validation is complete without error, the migration starts, and the workflow moves into the substate of **Migrating Data**.

Validation details are available at the instance and database level.

- **Validation details for instance**
    - Contains validation related to the connectivity check, source version, that is, PostgreSQL version >= 9.5, and server parameter check, whether the extensions are enabled in the server parameters of the Azure Database for PostgreSQL flexible server.
- **Validation and migration details for databases**
    - It contains validation of the individual databases related to extensions and collations support in Azure Database for PostgreSQL flexible server.

You can see the **Validation status** and **Migration status** under the migration details page.

:::image type="content" source="media/tutorial-migration-service-iaas-offline/portal-offline-details-migration.png" alt-text="Screenshot of the details showing validation and migration." lightbox="media/tutorial-migration-service-iaas-offline/portal-offline-details-migration.png":::

Some possible migration statuses:

### Migration statuses

| Status | Description |
| --- | --- |
| **In progress** | The migration infrastructure setup is underway, or the actual data migration is in progress. |
| **Canceled** | The migration is canceled or deleted. |
| **Failed** | The migration has failed. |
| **Validation failed** | The validation has failed. |
| **Validation passed** | The validation has failed. |
| **Validation passed with warning** | The validation has passed with warnings. |
| **Succeeded** | The migration has succeeded and is complete. |
| **Waiting for user action** | Applicable only for online migration. Waiting for user action to perform cutover. |

### Migration substatuses

| Substatus | Description |
| --- | --- |
| **PerformingPreRequisiteSteps** | Infrastructure setup is underway for data migration. |
| **Validation in progress** | Validation is in progress. |
| **MigratingData** | Data migration is in progress. |
| **CompletingMigration** | Migration is in the final stages of completion. |
| **Completed** | Migration has been completed. |
| **Failed** | Migration has failed. |

### Validation substatuses

| Substatus | Description |
| --- | --- |
| **Failed** | Validation has failed. |
| **Succeeded** | Validation is successful. |
| **Warning** | Validation is in warning. |

## Check the migration when complete

After completing the databases, you need to manually validate the data between source and target and verify that all the objects in the target database are successfully created.

After migration, you can perform the following tasks:

- Verify the data on your flexible server and ensure it's an exact copy of the source instance.

- Post verification, enable the high availability option on your flexible server as needed.

- Change the SKU of the flexible server to match the application needs. This change needs a database server restart.

- If you change any server parameters from their default values in the source instance, copy those server parameter values in the flexible server.

Copy other server settings, such as tags, alerts, and firewall rules (if applicable), from the source instance to the flexible server.

- Make changes to your application to point the connection strings to a flexible server.

- Monitor the database performance closely to see if it requires performance tuning.

## Related content

- [Migration service](concepts-migration-service-postgresql.md)
- [Best practices](best-practices-migration-service-postgresql.md)
- [Known Issues and limitations](concepts-known-issues-migration-service.md)
- [Network setup](how-to-network-setup-migration-service.md)
- [Premigration validations](concepts-premigration-migration-service.md)
