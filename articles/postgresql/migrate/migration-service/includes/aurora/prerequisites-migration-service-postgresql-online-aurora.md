---
title: "Prerequisites to Use the Migration Service From Amazon Aurora PostgreSQL (Online)"
description: Get the online prerequisites for the migration service in Azure Database for PostgreSQL.
author: apduvuri
ms.author: adityaduvuri
ms.reviewer: maghan
ms.date: 01/24/2025
ms.service: azure-database-postgresql
ms.topic: include
---

Before you start a migration by using the migration service in Azure Database for PostgreSQL, it's important to complete the following prerequisites. These prerequisites are specifically designed for online migration scenarios.

- [Verify the source version](#verify-the-source-version)
- [Install test_decoding for source setup](#install-test_decoding-for-source-setup)
- [Configure the target setup](#configure-the-target-setup)
- [Enable CDC as a source](#enable-cdc-as-a-source)
- [Configure the network setup](#configure-the-network-setup)
- [Enable extensions](#enable-extensions)
- [Check server parameters](#check-server-parameters)
- [Check users and roles](#check-users-and-roles)

### Verify the source version

The source PostgreSQL server version must be 9.5 or later. If the source PostgreSQL version is earlier than 9.5, upgrade the version to 9.5 or later before you start the migration.

### Install test_decoding for source setup

- The test_decoding plugin receives Write-Ahead Logging (WAL) through the logical decoding mechanism. The plugin decodes WAL into text representations of the operations that are performed.
- In Amazon RDS for PostgreSQL, the test_decoding plugin is preinstalled and ready for logical replication. You can easily set up logical replication slots and stream WAL changes, for example, for change data capture (CDC) or for replication to external systems.

For more information about the test_decoding plugin, see the [PostgreSQL documentation](https://www.postgresql.org/docs/16/test-decoding.html).

### Configure the target setup

Before you begin the migration, you must create an instance of [Azure Database for PostgreSQL](/azure/postgresql/flexible-server/) in Azure. The SKU that's provisioned for Azure Database for PostgreSQL flexible server should match the source.

For more information, see [Create an Azure Database for PostgreSQL flexible server](../../../../flexible-server/quickstart-create-server.md).

### Enable CDC as a source

- The test_decoding logical decoding plugin captures the changed records from the source.
- To allow the migration user to access replication permissions, execute the following command:

  ```bash
  GRANT rds_replication TO <username>;
  ```

- In the source PostgreSQL instance, modify the following parameters in the database clusters parameter group by creating a new parameter group:

  - Set `rds.logical_replication` to `1`.
  - Set `max_replication_slots` to a value greater than `1`. The value should be greater than the number of databases you select for migration.
  - Set `max_wal_senders` to a value greater than `1`. It should be at least the same value as the value for `max_replication_slots`, plus the number of senders already used in your instance.
  - The `wal_sender_timeout` parameter ends inactive replication connections that are longer than the specified number of milliseconds. The default value for an Amazon Aurora PostgreSQL instance is `30000 milliseconds (30 seconds)`. Setting the value to `0 (zero)` disables the timeout mechanism and is a valid setting for migration.

- In the target flexible server, to prevent the online migration from running out of storage to store the logs, ensure that you have sufficient storage in your tablespace by using a provisioned managed disk. Disable the server parameter `azure.enable_temp_tablespaces_on_local_ssd` for the duration of the migration. Restore the parameter to the original state after the migration.

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

### Disable high availability (reliability) and read replicas in the target

It's critical that you disable high availability (reliability) and read replicas in the target environment before you initiate migration. These features should be enabled only after the migration is completed.
