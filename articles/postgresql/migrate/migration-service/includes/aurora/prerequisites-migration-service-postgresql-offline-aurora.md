---
title: "Prerequisites to use the migration service from Amazon Aurora PostgreSQL (offline)"
description: Get the offline prerequisites for the migration service in Azure Database for PostgreSQL.
author: apduvuri
ms.author: adityaduvuri
ms.reviewer: maghan
ms.date: 06/19/2024
ms.service: azure-database-postgresql
ms.topic: include
---

Before you start a migration by using the Azure Database for PostgreSQL migration service, it's important to fulfill the following prerequisites. The prerequisites are specifically designed for offline migration scenarios.

- [Verify the source version](#verify-the-source-version)
- [Configure the target setup](#configure-the-target-setup)
- [Configure the network setup](#configure-the-network-setup)
- [Enable extensions](#enable-extensions)
- [Check server parameters](#check-server-parameters)
- [Check users and roles](#check-users-and-roles)
- [Disable high availability (reliability) and read replicas on the target](#disable-high-availability-reliability-and-read-replicas-on-the-target)

### Verify the source version

The source PostgreSQL server version must be 9.5 or later.

If the source PostgreSQL version is earlier than 9.5, upgrade the version to 9.5 or later before you start the migration.

### Configure the target setup

- Before you begin the migration, you must create an instance of [Azure Database for PostgreSQL](/azure/postgresql/flexible-server/) in Azure.
- The SKU that's provisioned for Azure Database for PostgreSQL - Flexible Server should match the source.

### Configure the network setup

Network setup is crucial for the migration service to function correctly. Ensure that the source PostgreSQL server can communicate with the target server of Azure Database for PostgreSQL. The following network configurations are essential for a successful migration.

For information about network setup, see the [network guide for the migration service](../../how-to-network-setup-migration-service.md).

### Enable extensions

[!INCLUDE [prerequisites-migration-service-extensions](../prerequisites/prerequisites-migration-service-extensions.md)]

### Check server parameters

These parameters aren't automatically migrated to the target environment and must be manually configured.

- Match server parameter values from the source PostgreSQL database to the instance of Azure Database for PostgreSQL. In the Azure portal, go **Server parameters** and manually update the values accordingly.

- Save the parameter changes and restart the instance Azure Database for PostgreSQL to apply the new configuration if necessary.

### Check users and roles

When you migrate to Azure Database for PostgreSQL, it's essential to address the migration of users and roles separately because they require manual intervention:

- **Manual migration of users and roles**: Users and their associated roles must be manually migrated to the instance of Azure Database for PostgreSQL. To facilitate this process, you can use the pg_dumpall utility with the `--globals-only` flag to export global objects such as roles and user accounts. Execute the following command, replacing `<username>` with the actual username and `<filename>` with the name of the output file you want:

  ```sql
  pg_dumpall --globals-only -U <username> -f <filename>.sql
  ```

- **Restriction on superuser roles**: Azure Database for PostgreSQL doesn't support superuser roles. Therefore, users with superuser privileges must have those permissions removed before migration. Ensure that you adjust the permissions and roles accordingly.

By following these steps, you can ensure that user accounts and roles are correctly migrated to Azure Database for PostgreSQL without encountering issues related to superuser restrictions.

### Disable high availability (reliability) and read replicas on the target

It's critical that you disable high availability (reliability) and read replicas in the target environment before you initiate migration. These features should be enabled only after the migration is completed.

By following these guidelines, you can help ensure a smooth migration process without the added variables that are introduced by high availability and read replicas. When the migration is completed and the database is stable, you can enable these features to enhance the availability and scalability of your database environment in Azure.
