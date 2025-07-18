---
title: "Migrate Online From On-Premises or an Azure VM to Azure Database for PostgreSQL"
description: "Learn to migrate seamlessly from on-premises or an Azure VM to Azure Database for PostgreSQL flexible server using the new migration service in Azure."
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

# Tutorial: Migrate online from an Azure VM or an on-premises PostgreSQL server to Azure Database for PostgreSQL with the migration service

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

This article guides you in migrating a PostgreSQL instance from your on-premises or Azure virtual machines (VMs) to Azure Database for PostgreSQL flexible server in online mode.

The migration service in Azure Database for PostgreSQL is a fully managed service integrated into the Azure portal and Azure CLI. It's designed to simplify your migration journey to the Azure Database for PostgreSQL flexible server.

[!INCLUDE [checklist-online](includes/checklist-online.md)]

## Prerequisites

To begin the migration, you need the following prerequisites:

[!INCLUDE [prerequisites-migration-service-postgresql-online-iaas](includes/iaas/prerequisites-migration-service-postgresql-online-iaas.md)]

## Perform the migration

You can migrate by using Azure portal or Azure CLI.

#### [Portal](#tab/portal)

This article guides you using the Azure portal to migrate your PostgreSQL database from an Azure VM or an on-premises PostgreSQL server to an Azure Database for PostgreSQL. The Azure portal allows you to perform various tasks, including database migration. Following the steps outlined in this tutorial, you can seamlessly transfer your database to Azure and take advantage of its powerful features and scalability.

### Configure the migration task

The migration service comes with a simple, wizard-based experience on the Azure portal.

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

1. In the resource menu, select **Migration**.

    :::image type="content" source="media/tutorial-migration-service-iaas-online/portal-online-select-migration-pane.png" alt-text="Screenshot of the Migration page." lightbox="media/tutorial-migration-service-iaas-online/portal-online-select-migration-pane.png":::

1. Select **Create** to go through a wizard-based series of tabs to perform a migration to a flexible server from on-premises or Azure VM.

    > [!NOTE]
    > The first time you use the migration service, an empty grid appears with a prompt to begin your first migration.

    If migrations to your flexible server target have already been created, the grid now contains information about attempted migrations.

    :::image type="content" source="media/tutorial-migration-service-iaas-online/portal-online-create-migration.png" alt-text="Screenshot of the Setup tab which appears after selecting Create in the Migration page." lightbox="media/tutorial-migration-service-iaas-online/portal-online-create-migration.png":::

#### Setup

You need to provide multiple details related to the migration, like the migration name, source server type, option, and mode.

- **Migration name** is the unique identifier for each migration to this Flexible Server target. This field accepts only alphanumeric characters and doesn't accept any special characters except a hyphen (-). The name can't start with a hyphen and should be unique for a target server. No two migrations to the same flexible server target can have the same name.

- **Source server type** - Depending on your PostgreSQL source, you can select **Azure Virtual Machine** or **On-premise Server**.

- **Migration option** - Allows you to perform validations before triggering a migration. You can pick any of the following options:
    - **Validate** - Checks your server and database readiness for migration to the target.
    - **Validate and migrate** — Performs validation before triggering a migration. If there are no validation failures, the migration is initiated.

Choosing the **Validate** or **Validate and migrate** option is always a good practice for performing premigration validations before running the migration.

To learn more about the premigration validation, visit [premigration](concepts-premigration-migration-service.md).

- **Migration mode** allows you to pick the mode for the migration. **Offline** is the default option. In this case, we'll change it to **Online**.

Select **Next: Runtime server**.

:::image type="content" source="media/tutorial-migration-service-iaas-online/portal-online-setup-migration-iaas.png" alt-text="Screenshot of the Setup tab after providing necessary details.":::

#### Runtime server

The migration runtime server is a specialized feature within the [migration service in Azure Database for PostgreSQL](concepts-migration-service-postgresql.md), designed to act as an intermediary server during migration. It's a separate Azure Database for PostgreSQL flexible server instance that isn't the target server, but is used to facilitate the migration of databases from a source environment that is only accessible via a private network.

:::image type="content" source="media/tutorial-migration-service-iaas-online/portal-online-runtime-server-migration-iaas.png" alt-text="Screenshot of the Runtime server tab.":::

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

:::image type="content" source="media/tutorial-migration-service-iaas-online/portal-online-source-server-migration-iaas.png" alt-text="Screenshot of Source server migration tab.":::

#### Target server

The **Target server** tab displays metadata for the flexible server target, such as the subscription name, resource group, server name, location, and PostgreSQL version.

- **Admininistrator login** - Name of the administrator user of the target PostgreSQL server.
- **Password** - Password of the administrator login provided to connect to target PostgreSQL server.
- **Custom FQDN or IP address**: The custom FQDN or IP address field is optional, and can be used when the target is behind a custom DNS server or has custom DNS namespaces, making it accessible only via specific FQDNs or IP addresses. For example, this could include entries like `production-flexible-server.example.com`, `198.1.0.2`, or a PostgreSQL FQDN such as `production-flexible-server.postgres.database.azure.com`, if the custom DNS server contains the DNS zone `postgres.database.azure.com` or forward queries for this zone to `168.63.129.16`, where the FQDN is resolved in the Azure public or private DNS zone.
- **Test connection** — Performs the connectivity test between the source and target. Once the connection is successful, you can proceed to the next tab. These test aims to identify any connectivity issues that might exist between the source and target servers, including verification of authentication using the credentials supplied. Establishing a test connection takes a few seconds.

After the successful test connection, select the **Next: Databases to validate or migrate**

:::image type="content" source="media/tutorial-migration-service-iaas-online/portal-online-target-server-migration-iaas.png" alt-text="Screenshot of the Target server migration tab.":::

#### Databases to validate or migrate

Under the **Databases to validate or migrate** tab, you can choose a list of user databases to migrate from your source PostgreSQL server.

After selecting the databases, select **Next: Summary**.

:::image type="content" source="media/tutorial-migration-service-iaas-online/portal-online-databases-to-validate-or-migrate-migration-iaas.png" alt-text="Screenshot of the Databases to validate or migrate  migration tab.":::

#### Summary

The **Summary** tab summarizes all the source and target details for creating the validation or migration. Review the details and select **Start validation and migration**.

:::image type="content" source="media/tutorial-migration-service-iaas-online/portal-online-summary-migration-iaas.png" alt-text="Screenshot of the Summary migration tab.":::

## Cancel the migration

You can cancel any ongoing validations or migrations. The workflow must be in the **In progress** status to be canceled. You can't cancel a validation or migration in the **Succeeded** or **Failed** status.

Canceling a validation stops any further validation activity and the validation moves to a **Canceled** status.

Canceling a migration stops further migration activity on your target server and moves to a **Canceled** status. It doesn't drop or roll back any changes on your target server. Be sure to drop the databases on your target server that is involved in a canceled migration.

#### [CLI](#tab/cli)

This article explores using the Azure CLI to migrate your PostgreSQL database from an Azure virtual machine or an on-premises PostgreSQL instance to an Azure Database for PostgreSQL. The Azure CLI provides a powerful and flexible command-line interface that allows you to perform various tasks, including database migration. Following the steps outlined in this article, you can seamlessly transfer your database to Azure and take advantage of its powerful features and scalability.

To learn more about Azure CLI with the migration service, visit [How to set up Azure CLI for the migration service](how-to-setup-azure-cli-commands-postgresql.md).

Once the CLI is installed, open the command prompt and log into your Azure account using the below command.

```azurecli-interactive
az login
```

### Configure the migration task

To begin the migration, create a JSON file with the migration details. The JSON file contains the following information:

- Edit the below placeholders `<< >>` in the JSON lines and store them in the local machine as `<<filename>>.json` where the CLI is being invoked. In this tutorial, we have saved the file in `c:/migration-CLI/migration_body.json`

```bash
{
"properties": {
"SourceDBServerResourceId": "<<source-server-hostname-or-IP-address>>:<<port>>@<<username>>",
        "SecretParameters": {
            "AdminCredentials": {
                "SourceServerPassword": "<<source-server-administrator-password>>",
                "TargetServerPassword": "<<target-server-administrator-password>>"
            },
            "targetServerUserName": "<<target-server-administrator-login>>"
        },
        "DBsToMigrate": "<<comma-separated-list-of-databases-in-array-like-["ticketdb","timedb","inventorydb"]>>",
        "OverwriteDBsInTarget": "true",
        "sourceType": "OnPremises",
        "sslMode": "Prefer"
    }
}
```

> [!NOTE]  
> When configuring the JSON properties for the migration to Azure Database for PostgreSQL flexible server, if your source environment is an Azure Virtual Machine, you can specify the source type using the `"sourceType":"AzureVM"` property. This helps the migration service understand the environment from which the data is being migrated.

- Run the following command to check if any migrations are running. The migration name is unique across the migrations within the Azure Database for PostgreSQL flexible server target.

    ```azurecli-interactive
    az postgres flexible-server migration list --subscription <subscription_id> --resource-group <resource_group> --name <target_server> --filter all
    ```

- In the above steps, there are no migrations performed so we start with the new migration by running the following command.

    ```azurecli-interactive
    az postgres flexible-server migration create --subscription <subscription_id> --resource-group <resource_group> --name <target_server> --migration-name <migration> --migration-mode offline --migration-option ValidateAndMigrate --properties "c:/migration-cli/migration_body.json"
    ```

- Run the following command to see the status of the migration initiated in the previous step. You can check the status of the migration by providing the migration name.

    ```azurecli-interactive
    az postgres flexible-server migration show --subscription <subscription_id> --resource-group <resource_group> --name <target_server> --migration-name <migration>
    ```

- The progress and status of the migration is shown in Azure CLI.

- You can also see the progress and status in Azure portal.

- You can cancel any ongoing migration attempts using the `cancel` command. This command stops the particular migration attempt, and rolls back all changes that it could have made on your target server. Following is the CLI command to cancel migration that has an "In progress" status.

    ```azurecli-interactive
    az postgres flexible-server migration update cancel --subscription <subscription_id> --resource-group <resource_group> --name <target_server> --migration-name <migration>
    ```

---

[!INCLUDE [monitor-the-migration-online](includes/monitor-the-migration-online.md)]

[!INCLUDE [initiate-the-cutover](includes/initiate-the-cutover.md)]

## Initiate the cutover

#### [Portal](#tab/portal)

For **Validate and migrate** option, completing of the online migration requires the user to complete an additional step, which is to trigger the cutover action. After the copying or cloning of the base data is complete, the migration moves to the `Waiting for user action` status and the `Waiting for cutover trigger` substatus. In this status, the user can trigger the cutover from the portal by selecting the migration.

Before initiating cutover, it's important to ensure that:

- Writes to the source are stopped - `latency` value is 0 or close to 0. The `latency` information can be obtained from the migration details screen as shown below:
- `latency` value decreases to 0 or close to 0
- The `latency` value indicates when the target last synced with the source. Writing to the source can be stopped at this point, and a cutover can be initiated. In case there's heavy traffic at the source, it's recommended to stop writes first so that `latency` can come close to 0, and then a cutover is initiated.

The cutover operation applies all pending changes from the source server to the target server, and completes the migration. If you trigger a cutover, even with nonzero `latency`, the replication stops until that point in time. All the data on the source until the cutover point is then applied to the target. If you experience a latency of 15 minutes at the cutover point, all the changes made to data in the last 15 minutes are applied to the target.

The time depends on the backlog of changes occurring in the last 15 minutes. Hence, it's recommended that the latency goes to zero or near zero before triggering the cutover.

- The migration moves to the `Succeeded` status when the `Migrating data` substatus or the cutover (in online migration) finishes successfully. If there's a problem at the `Migrating data` substatus, the migration moves into a `Failed` status.

#### [CLI](#tab/cli)

For **Validate and migrate** option, completing of the online migration requires the user to complete an additional step, which is to trigger the cutover action. After the copying or cloning of the base data is complete, the migration moves to the `Waiting for user action` status and the `Waiting for cutover trigger` substatus. In this state, the user can trigger the cutover through the CLI using the command below. The cutover can also be triggered from the portal by selecting the migration name in the migration grid.

Before initiating cutover, it's important to ensure that:

- Writes to the source are stopped - `latency` value is 0 or close to 0. The `latency` information can be obtained from the migration details screen as shown below:
- `latency` value decreases to 0 or close to 0
- The `latency` value indicates when the target last synced with the source. Writing to the source can be stopped at this point, and a cutover can be initiated. In case there's heavy traffic at the source, it's recommended to stop writes first so that `latency` can come close to 0, and then a cutover is initiated.

The cutover operation applies all pending changes from the source server to the target server, and completes the migration. If you trigger a cutover, even with nonzero `latency`, the replication stops until that point in time. All the data on the source until the cutover point is then applied to the target. If you experience a latency of 15 minutes at the cutover point, all the changes made to data in the last 15 minutes are applied to the target.

The time depends on the backlog of changes occurring in the last 15 minutes. Hence, it's recommended that the latency goes to zero or near zero before triggering the cutover.

- The migration moves to the `Succeeded` status when the `Migrating data` substatus or the cutover (in online migration) finishes successfully. If there's a problem at the `Migrating data` substatus, the migration moves into a `Failed` status.

To trigger the cutover, use the following command:

    ```azurecli-interactive
    az postgres flexible-server migration update --subscription <subscription_id> --resource-group <resource_group> --name <server> --migration-name <migration> --cutover
    ```

---

[!INCLUDE [monitor-migration-online](includes/monitor-migration-online.md)]

[!INCLUDE [check-migration-completed-online](includes/check-migration-completed-online.md)]


## Check the migration when complete

After completing the databases, you need to manually validate the data between source and target and verify that all the objects in the target database are successfully created.

After migration, you can perform the following tasks:

- Verify the data on your flexible server and ensure it's an exact copy of the source instance.

- Post verification, enable the high availability option on your flexible server as needed.

- Change the SKU of the flexible server to match the application needs. This change needs a database server restart.

- If you change any server parameters from their default values in the source instance, copy those server parameter values in the flexible server.

- Copy other server settings, such as tags, alerts, and firewall rules (if applicable), from the source instance to the flexible server.

- Make changes to your application to point the connection strings to a flexible server.

- Monitor the database performance closely to see if it requires performance tuning.

## Related content

- [Migration service](concepts-migration-service-postgresql.md)
- [Best practices](best-practices-migration-service-postgresql.md)
- [Known issues and limitations](concepts-known-issues-migration-service.md)
- [Network setup](how-to-network-setup-migration-service.md)
- [Premigration validations](concepts-premigration-migration-service.md)
