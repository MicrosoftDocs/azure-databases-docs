---
title: "Migration Service - Premigration Validations"
description: Learn about premigration validations to identify issues before you run a migration to Azure Database for PostgreSQL.
author: apduvuri
ms.author: adityaduvuri
ms.reviewer: maghan
ms.date: 07/21/2025
ms.service: azure-database-postgresql
ms.topic: concept-article
---

# Premigration validation for the migrations service in Azure Database for PostgreSQL

Premigration validation is a set of rules that involves assessing and verifying the readiness of a source database system for migration to Azure Database for PostgreSQL. This process identifies and addresses potential issues affecting the database's migration or post-migration operation.

## How do you use the premigration validation feature?

You can migrate by using Azure portal or Azure CLI.

### [Portal](#tab/portal)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

1. In the resource menu, select **Migration**.

    :::image type="content" source="media/tutorial-migration-service/select-migration-page.png" alt-text="Screenshot of the Migration page." lightbox="media/tutorial-migration-service/select-migration-page.png":::

1. Select **Create** to go through a wizard-based series of tabs to perform a migration to a flexible server from on-premises or Azure VM.

    :::image type="content" source="media/tutorial-migration-service-iaas-offline/create-migration.png" alt-text="Screenshot of the Setup tab which appears after selecting Create in the Migration page." lightbox="media/tutorial-migration-service-iaas-offline/create-migration.png":::

1. In **Migration option**, select **Validate** or **Validate and migrate**.

    :::image type="content" source="media/concepts-premigration-migration-service/premigration-option.png" alt-text="Screenshot that shows the premigration option to start migration." lightbox="media/concepts-premigration-migration-service/premigration-option.png":::

### [CLI](#tab/cli)

1. Open your command-line interface.

1. Ensure that you have the Azure CLI installed, and that you're signed in to your Azure account by using `az login`. Make sure that you're using the latest available version of CLI.

1. Construct your migration task creation command with the Azure CLI.

    ```azurecli-interactive
    az postgres flexible-server migration create --subscription <subscription_id> --resource-group <resource_group> --name <target_server> --migration-name <migration> --migration-option ValidateAndMigrate --properties "path_to_json_file_with_all_migration_properties" --migration-mode offline
    ```
---

## Premigration validation options

You can choose any of the following options:

- **Validate**: Use this option to check your server and database readiness for migration to the target. *This option won't start data migration and won't require any server downtime.*
     - Plan your migrations better by performing premigration validations in advance to know the potential issues you might encounter while you perform migrations.
- **Validate and migrate**: This option performs validations, and migration gets triggered if all checks are in the **Succeeded** or **Warning** state. Validation failures don't start the migration between source and target servers.

We recommend that you use premigration validations to identify issues before you run migrations. This technique helps you to plan your migrations better and avoid any surprises during the migration process.

1. Choose the **Validate** option and run premigration validation on an advanced date of your planned migration.

1. Analyze the output and take any remedial actions for any errors.

1. Rerun step 1 until the validation is successful.

1. Start the migration by using the **Validate and migrate** option on the planned date and time.

## Validation states

After you run the **Validate** option, you see one of the following options:

- **Succeeded**: No issues were found and you can plan for the migration.
- **Failed**: Errors were found during validation, which can cause the migration to fail. Review the list of errors and their suggested workarounds. Take corrective measures before you plan the migration.
- **Warning**: Warnings are informative messages you must remember while you plan the migration.

## Related content

- [Migration service](concepts-migration-service-postgresql.md)
- [Known issues and limitations](concepts-known-issues-migration-service.md)
- [Network setup](how-to-network-setup-migration-service.md)
