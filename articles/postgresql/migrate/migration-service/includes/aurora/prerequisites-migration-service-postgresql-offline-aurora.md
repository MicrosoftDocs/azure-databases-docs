---
title: "Prerequisites to Use the Migration Service From Amazon Aurora PostgreSQL (Offline)"
description: Get the offline prerequisites for the migration service in Azure Database for PostgreSQL.
author: apduvuri
ms.author: adityaduvuri
ms.reviewer: maghan
ms.date: 01/24/2025
ms.service: azure-database-postgresql
ms.topic: include
---

Before you start a migration by using the migration service in Azure Database for PostgreSQL, it's important to complete the following prerequisites. These prerequisites are specifically designed for offline migration scenarios.

- [Verify the source version](#verify-the-source-version)
- [Configure the target setup](#configure-the-target-setup)
- [Configure the network setup](#configure-the-network-setup)
- [Enable extensions](#enable-extensions)
- [Check server parameters](#check-server-parameters)
- [Check users and roles](#check-users-and-roles)
- [Disable high availability (reliability) and read replicas on the target](#disable-high-availability-reliability-and-read-replicas-on-the-target)

### Verify the source version

The source PostgreSQL server version must be 9.5 or later. If the source PostgreSQL version is earlier than 9.5, upgrade the version to 9.5 or later before you start the migration.

### Configure the target setup

Before you begin the migration, you must create an instance of [Azure Database for PostgreSQL](/azure/postgresql/flexible-server/) in Azure. The SKU that's provisioned for Azure Database for PostgreSQL - Flexible Server should match the source.

For more information, see [Create an instance of Azure Database for PostgreSQL - Flexible Server](../../../../flexible-server/quickstart-create-server.md).

### Configure the network setup

Network setup is crucial for the migration service to function correctly. Ensure that the source PostgreSQL server can communicate with the target server in Azure Database for PostgreSQL.

For information about network setup, see [Network scenarios for the migration service](../../how-to-network-setup-migration-service.md).

### Enable extensions

[!INCLUDE [prerequisites-migration-service-extensions](../prerequisites/prerequisites-migration-service-extensions.md)]

### Check server parameters

Server parameters aren't automatically migrated to the target environment and must be manually configured.

- Match server parameter values from the source PostgreSQL database to the instance of Azure Database for PostgreSQL. In the Azure portal, go to **Server parameters** and manually update the values.

- Save the parameter changes and restart the instance of Azure Database for PostgreSQL to apply the new configuration if necessary.

### Check users and roles

When you migrate to Azure Database for PostgreSQL, it's essential to address the migration of users and roles separately because they require manual intervention.

- **Manual migration of users and roles**: Users and their associated roles must be manually migrated to the instance of Azure Database for PostgreSQL. To facilitate this process, you can use the pg_dumpall utility with the `--globals-only` flag to export global objects such as roles and user accounts.

  Execute the following command. Replace `<username>` with the actual username, and replace `<filename>` with the name you want to use for the output file.

  ```sql
  pg_dumpall --globals-only -U <username> -f <filename>.sql
  ```

- **Restriction on superuser roles**: Azure Database for PostgreSQL doesn't support superuser roles. Superuser permissions must be removed before migration. Ensure that you adjust the permissions and roles accordingly.

By completing these steps, you can ensure that user accounts and roles are correctly migrated to Azure Database for PostgreSQL without issues related to superuser restrictions.

### Disable high availability (reliability) and read replicas on the target

It's critical that you disable high availability (reliability) and read replicas in the target environment before you initiate migration. These features should be enabled only after the migration is completed.
