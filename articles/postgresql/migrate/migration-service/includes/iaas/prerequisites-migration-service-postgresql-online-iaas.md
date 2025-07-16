---
title: "Prerequisites Using the Migration Service From an Azure VM or an On-Premises PostgreSQL Server (Online)"
description: Providing the online prerequisites for the migration service in Azure Database for PostgreSQL.
author: apduvuri
ms.author: adityaduvuri
ms.reviewer: maghan
ms.date: 01/24/2025
ms.service: azure-database-postgresql
ms.topic: include
---

Before starting the migration with the Azure Database for PostgreSQL migration service, it's important to fulfill the following prerequisites, specifically designed for online migration scenarios.

- [Verify the source version](#verify-the-source-version)
- [Install test_decoding - Source Setup](#install-test_decoding---source-setup)
- [Configure target setup](#configure-target-setup)
- [Enable CDC as a source](#enable-cdc-as-a-source)
- [Configure network setup](#configure-network-setup)
- [Enable extensions](#enable-extensions)
- [Check server parameters](#check-server-parameters)
- [Check users and roles](#check-users-and-roles)
- [Disable high availability (reliability) and read replicas in the target](#disable-high-availability-reliability-and-read-replicas-in-the-target)

### Verify the source version

The source PostgreSQL server version must be 9.5 or later.

If the source PostgreSQL version is less than 9.5, upgrade it to 9.5 or higher before you start the migration.

### Install test_decoding - Source Setup

- **test_decoding** receives WAL through the logical decoding mechanism and decodes it into text representations of the operations performed.

- For more information about the test-decoding plugin, see the [PostgreSQL documentation](https://www.postgresql.org/docs/16/test-decoding.html).

### Configure target setup

Before you begin the migration, you must set up an [Azure Database for PostgreSQL](/azure/postgresql/flexible-server/) in Azure.

The SKU chosen for the Azure Database for PostgreSQL should correspond with the specifications of the source database to ensure compatibility and adequate performance.

When migrating across PostgreSQL versions (major or minor), ensure compatibility between your database and application by reviewing the [release notes](https://www.postgresql.org/docs/17/release.html) for potential breaking changes.

### Enable CDC as a source

- `test_decoding` logical decoding plugin captures the changed records from the source.
- In the source PostgreSQL instance, set the following parameters and values in the postgresql.conf configuration file:
    - Set `wal_level` to `logical`.
    - Set `max_replication_slots` to a value greater than 1. Should be greater than the number of databases selected for migration.
    - Set `max_wal_senders` to a value greater than 1. Should be set to, at least, the same valuae as `max_replication_slots`, plus the number of senders already used by your instance.
    - `wal_sender_timeout` parameter terminates replication connections that are inactive longer than the specified number of milliseconds. Default for an on-premises PostgreSQL database is 60000 milliseconds (60 seconds). Setting the value to 0 (zero) disables the timeout mechanism, and is a recommended value for migration.

To prevent the online migration from running out of space, ensure that you have sufficient tablespace space, by using a provisioned managed disk. To achieve this, disable the server parameter `azure.enable_temp_tablespaces_on_local_ssd` on the flexible server for the duration of the migration, and restore it to the original state after the migration.

### Configure network setup

Network setup is crucial for the migration service to function correctly. Ensure that the source PostgreSQL server can communicate with the target Azure Database for PostgreSQL server. The following network configurations are essential for a successful migration.

For information about network setup, visit [Network guide for migration service](../../how-to-network-setup-migration-service.md).

#### Additional networking considerations

To facilitate connectivity between the source and target PostgreSQL instances, it's essential to verify and potentially modify the pg_hba.conf file of the source server. This file includes client authentication and must be configured to allow the target PostgreSQL to connect to the source. Changes to the pg_hba.conf file, typically require a restart of the source PostgreSQL instance to take effect.

The pg_hba.conf file is located in the data directory of the PostgreSQL installation. This file should be checked and configured, if the source database is an on-premises PostgreSQL server or a PostgreSQL server hosted on an Azure VM.

### Enable extensions

[!INCLUDE [prerequisites-migration-service-extensions](../prerequisites/prerequisites-migration-service-extensions.md)]

### Check server parameters

These parameters aren't automatically migrated to the target environment, and must be manually configured.

- Match server parameter values from the source PostgreSQL database to the Azure Database for PostgreSQL by accessing the **Server parameters** page in the Azure portal, and manually updating the values accordingly.

- Save the parameter changes and restart the Azure Database for PostgreSQL to apply the new configuration, if necessary.

### Check users and roles

When migrating to Azure Database for PostgreSQL, it's essential to address the migration of users and roles separately, as they require manual intervention:

- **Manual migration of users and roles**: Users and roles must be manually migrated to the Azure Database for PostgreSQL. To facilitate this process, you can use the `pg_dumpall` utility with the `--globals-only` flag to export global objects, such as roles and users. Execute the following command, replacing `<<username>>` with the actual username, and `<<filename>>` with your desired output file name:

  ```sql
  pg_dumpall --globals-only -U <<username>> -f <<filename>>.sql
  ```

- **Restriction on superuser roles**: Azure Database for PostgreSQL doesn't support superuser roles. Therefore, users with superuser privileges must have those privileges removed before migration. Ensure that you adjust the permissions and roles accordingly.

By following these steps, you can ensure that user accounts and roles are correctly migrated to the Azure Database for PostgreSQL without encountering issues related to superuser restrictions.

### Disable high availability (reliability) and read replicas in the target

- Disabling high availability (reliability) and reading replicas in the target environment is essential. These features should be enabled only after the migration is completed.

- By following these guidelines, you can help ensure a smooth migration process, without the added variables introduced by high availability and read replicas. Once the migration is complete and the database is stable, you can proceed to enable these features to enhance the availability and scalability of your database environment in Azure.
