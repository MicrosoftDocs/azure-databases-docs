---
title: Required Permissions for Migration Creation and Monitoring
description: Permissions required for a user to create and monitor migrations.
author: shriramm
ms.author: shriramm
ms.reviewer: maghan
ms.date: 11/11/2024
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: conceptual
---

# Required Permissions for Migration Creation and Monitoring

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

To create and monitor migrations using the PostgreSQL Migration Service, users need specific permissions. Here's a guide on the permissions required and steps to configure them effectively.

## Minimum Set of Permissions

The following permissions are the minimum required for a user to successfully create and monitor migrations:

- **Resource Group and Subscription Permissions**
    - Microsoft.Resources/subscriptions/resourceGroups/read
    - Microsoft.Resources/subscriptions/read
    - Microsoft.Resources/subscriptions/locations/read
    - Microsoft.Resources/subscriptions/resourceGroups/deployments/read
    - Microsoft.Resources/deployments/read
    - Microsoft.Resources/subscriptions/resourceGroups/resources/read

- **Migration-Specific Permissions**
    - Microsoft.DBforPostgreSQL/flexibleServers/checkMigrationNameAvailability/action
    - Microsoft.DBforPostgreSQL/flexibleServers/migrations/write
    - Microsoft.DBforPostgreSQL/flexibleServers/migrations/read
    - Microsoft.DBforPostgreSQL/flexibleServers/migrations/delete

- **Flexible Server Access Permissions**
    - Microsoft.DBforPostgreSQL/flexibleServers/read
    - Microsoft.DBforPostgreSQL/flexibleServers/databases/read

- **Source Server Access Permissions (Required for Single Server Sources only)**
    - Microsoft.DBforPostgreSQL/servers/read
    - Microsoft.DBforPostgreSQL/servers/administrators/read
    - Microsoft.DBforPostgreSQL/servers/databases/read

- **Connectivity and Database List Actions**
    - Microsoft.DBforPostgreSQL/flexibleServers/testConnectivity/action
    - Microsoft.DBforPostgreSQL/flexibleServers/getSourceDatabaseList/action

- **Configuration Access Permissions**
    - Microsoft.DBforPostgreSQL/flexibleServers/configurations/read
    - Microsoft.DBforPostgreSQL/servers/configurations/read


### Default roles

By default, privileged administrator roles such as **Owner** or **Contributor** at the subscription level have the necessary permissions enabled.

### Assigning a Custom Role for Migration

If you want to grant permissions specifically for creating and monitoring migrations, without additional database admin privileges, consider creating a custom role.

- [Create a custom role](https://learn.microsoft.com/azure/role-based-access-control/custom-roles-portal) with the permissions listed above.

- Assign the custom role’s scope at the subscription level for both the single server and flexible server involved in the migration. 

- [Assign this custom role to the user](https://learn.microsoft.com/azure/role-based-access-control/role-assignments-portal) responsible for conducting the migration.

### Additional Requirements for Runtime Server Migrations

If a runtime server is part of your migration setup, ensure the permissions Microsoft.DBforPostgreSQL/flexibleServers/migrations/* are included in the scope of the runtime server.

By setting up these permissions, you ensure that your migration process is both secure and aligned with PostgreSQL Migration Service requirements.

## Related content

- [Migration service](concepts-migration-service-postgresql.md)
- [Network setup](how-to-network-setup-migration-service.md)
- [Premigration validations](concepts-premigration-migration-service.md)