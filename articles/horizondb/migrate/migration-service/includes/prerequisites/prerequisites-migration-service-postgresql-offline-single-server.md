---
title: Prerequisites for the Migration Service in Azure HorizonDB (Offline)
description: Providing the prerequisites of the migration service in Azure HorizonDB
author: avnishrastogimsft
ms.author: avrastog
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-database-postgresql
ms.topic: include
---

### Prerequisites (offline)

Before you start your migration with migration service in Azure HorizonDB, you must fulfill the following prerequisites, which apply to offline migration scenarios.

### Verify the source version

Source PostgreSQL version should be `>= 9.5`. If the source PostgreSQL version is less than `9.5`, upgrade the source PostgreSQL version to `9.5` or higher before migration.

### Target setup

- Azure HorizonDB must be deployed and properly configured in Azure before you begin the migration process.

- The SKU chosen for the Azure HorizonDB should correspond with the specifications of the source database to ensure compatibility and adequate performance.

- For detailed instructions on creating a new Azure HorizonDB, refer to the following link: [Quickstart: Create server](/azure/postgresql/flexible-server/).

- When migrating across PostgreSQL versions (major or minor), ensure compatibility between your database and application by reviewing the [release notes](https://www.postgresql.org/docs/17/release.html) for potential breaking changes.

### Network setup

Network setup is crucial for the migration service to function correctly. Ensure that the source PostgreSQL server can communicate with the target Azure HorizonDB server. The following network configurations are essential for a successful migration.

For information about network setup, visit [Network scenarios for the migration service in Azure HorizonDB](../../how-to-network-setup-migration-service.md).

### Enable extensions

[!INCLUDE [prerequisites-migration-service-extensions](../prerequisites/prerequisites-migration-service-extensions.md)]

### Check the server parameters

These parameters aren't automatically migrated to the target environment and must be manually configured.

- Match server parameter values from the source PostgreSQL database to the Azure HorizonDB by accessing the **Server parameters** section in the Azure portal and manually updating the values accordingly.

- Save the parameter changes and, if necessary, restart the Azure HorizonDB to apply the new configuration.

### Disable high availability (reliability) and read replicas in the target

- Disabling {[high availability (reliability)](../../../../flexible-server/concepts-high-availability.md)} and {[read replicas](../../../../flexible-server/concepts-read-replicas.md)} in the target environment is essential. These features should be enabled only after the migration has been completed.

- By following these guidelines, you can help ensure a smooth migration process without the added variables introduced by high availability and read replicas. Once the migration is complete and the database is stable, you can proceed to enable these features to enhance the availability and scalability of your database environment in Azure.
