---
title: "Migration Runtime Server in Azure Database for PostgreSQL"
description: "This article discusses concepts about Migration Runtime Server with the migration service in Azure Database for PostgreSQL."
author: apduvuri
ms.author: adityaduvuri
ms.reviewer: maghan
ms.date: 02/07/2025
ms.service: azure-database-postgresql
ms.topic: concept-article
---

# Migration Runtime Server with the migration service in Azure Database for PostgreSQL

The Migration Runtime Server is a crucial component in the migration service for Azure Database for PostgreSQL. It serves as an intermediary server, ensuring secure and efficient data transfer during the migration process. This server is particularly useful when migrating databases from environments that are only accessible via private networks.

By acting as a bridge between the source PostgreSQL instance and the target Azure Database for PostgreSQL - Flexible Server instance, the Migration Runtime Server facilitates seamless data migration. It ensures that the migration occurs within a secure and isolated network space, maintaining the integrity and confidentiality of the data being transferred.

This article provides an in-depth look at the Migration Runtime Server, its supported scenarios, and how to use it effectively within the migration service in Azure Database for PostgreSQL.

:::image type="content" source="media/concepts-migration-service-runtime-server/private-endpoint-scenario.png" alt-text="Screenshot that shows Migration Runtime Server." lightbox="media/concepts-migration-service-runtime-server/private-endpoint-scenario.png":::

## Supported migration scenarios with the Migration Runtime Server

Migration Runtime Server is essential for transferring data between different source PostgreSQL instances and the Azure Database for PostgreSQL - Flexible Server instance. It's necessary in the following scenarios:

- When the source is an Azure Database for PostgreSQL - Single Server configured with a private endpoint and the target is an Azure Database for PostgreSQL - Flexible Server with a private endpoint.
- For sources such as on-premises databases, Azure virtual machines, or AWS instances that are only accessible via private networks and the target Azure Database for PostgreSQL - Flexible Server instance with a private endpoint.

## How do you use the Migration Runtime Server feature?

To use the Migration Runtime Server feature within the migration service in Azure Database for PostgreSQL, you have two migration options:

- Use the Azure portal during setup.
- Specify the `migrationRuntimeResourceId` parameter in the JSON properties file during the migration create command in the Azure CLI.

Here's how to do it in both methods.

# [Azure portal](#tab/azure-portal)

### Use the Azure portal

1. Sign in to the Azure portal and access the migration service (from the target server) in the Azure Database for PostgreSQL instance.
1. Begin a new migration workflow within the service.
1. When you reach the **Select runtime server** tab, select **Yes** to use Migration Runtime Server.
1. Select your Azure subscription and resource group. Select the location of the virtual network-integrated Azure Database for PostgreSQL - Flexible Server instance.
1. Select the appropriate Azure Database for PostgreSQL - Flexible Server instance to serve as your Migration Runtime Server instance.

   :::image type="content" source="media/concepts-migration-service-runtime-server/select-runtime-server.png" alt-text="Screenshot that shows selecting Migration Runtime Server." lightbox="media/concepts-migration-service-runtime-server/select-runtime-server.png":::

# [Azure CLI](#tab/azure-cli)

### Use the Azure CLI

1. Open your command-line interface.
1. Ensure that you have the Azure CLI installed and that you're signed in to your Azure account by using `az sign-in`.
1. The version should be at least 2.62.0 or above to use the Migration Runtime Server option.
1. The `az postgres flexible-server migration create` command requires a JSON file path as part of the `--properties` parameter, which contains configuration details for the migration. Provide the `migrationRuntimeResourceId` parameter in the JSON properties file.

---

## Migration Runtime Server essentials

- **Minimal configuration**: Despite being created from Azure Database for PostgreSQL - Flexible Server, Migration Runtime Server solely facilitates migration without the need for high availability, backups, version specificity, or advanced storage features.
- **Performance and sizing**: Migration Runtime Server must be appropriately scaled to manage the workload. We recommend that you select an SKU equivalent to or greater than that of the target server.
- **Networking**: Ensure that Migration Runtime Server is appropriately integrated into the virtual network and that network security allows for secure communication with both the source and target servers. For more information, see [Network guide for migration service](how-to-network-setup-migration-service.md).
- **Post-migration cleanup**: After the migration is finished, Migration Runtime Server should be decommissioned to avoid unnecessary costs. Before deletion, ensure that all data was successfully migrated and that the server is no longer needed.

## Related content

- [Migration service](concepts-migration-service-postgresql.md)
- [Network setup](how-to-network-setup-migration-service.md)
- [Premigration validations](concepts-premigration-migration-service.md)
