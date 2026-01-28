---
title: "Required Permissions for Migration Creation and Monitoring"
description: Permissions required for a user to create and monitor migrations.
author: shriramm
ms.author: shriramm
ms.reviewer: maghan
ms.date: 07/21/2025
ms.service: azure-database-postgresql
ms.topic: concept-article
---

# Required permissions for migration creation and monitoring

To create and monitor migrations using the PostgreSQL Migration Service, users need specific permissions. Here's a guide on the permissions required and steps to configure them effectively.

##  Role-Based Access Control (RBAC): Minimum set of permissions

The following permissions are the minimum required for a user to successfully create and monitor migrations:

- **Resource group** and **Subscription**
    - Microsoft.Resources/subscriptions/resourceGroups/read
    - Microsoft.Resources/subscriptions/read
    - Microsoft.Resources/subscriptions/locations/read
    - Microsoft.Resources/subscriptions/resourceGroups/deployments/read
    - Microsoft.Resources/deployments/read
    - Microsoft.Resources/subscriptions/resourceGroups/resources/read

- **Migration-specific**
    - Microsoft.DBforPostgreSQL/flexibleServers/checkMigrationNameAvailability/action
    - Microsoft.DBforPostgreSQL/flexibleServers/migrations/write
    - Microsoft.DBforPostgreSQL/flexibleServers/migrations/read
    - Microsoft.DBforPostgreSQL/flexibleServers/migrations/delete

- **Target server**
    - Microsoft.DBforPostgreSQL/flexibleServers/read
    - Microsoft.DBforPostgreSQL/flexibleServers/databases/read

- **Source server (required for Single Server sources only)**
    - Microsoft.DBforPostgreSQL/servers/read
    - Microsoft.DBforPostgreSQL/servers/administrators/read
    - Microsoft.DBforPostgreSQL/servers/databases/read

- **Connectivity** and **Database List**
    - Microsoft.DBforPostgreSQL/flexibleServers/testConnectivity/action
    - Microsoft.DBforPostgreSQL/flexibleServers/getSourceDatabaseList/action

- **Configurations**
    - Microsoft.DBforPostgreSQL/flexibleServers/configurations/read
    - Microsoft.DBforPostgreSQL/servers/configurations/read

### Default roles

By default, privileged administrator roles such as **Owner** or **Contributor** at the subscription level have the necessary permissions enabled.

### Assigning a custom role for migration

If you want to grant permissions specifically for creating and monitoring migrations, without other database admin privileges, consider creating a custom role.

- [Create a custom role](/azure/role-based-access-control/custom-roles-portal) with the permissions listed above.

- Assign the custom role's scope at the subscription level for both the single server and flexible server involved in the migration.

- [Assign this custom role to the user](/azure/role-based-access-control/role-assignments-portal) responsible for conducting the migration.

### Other requirements for migrations that include a runtime server

If a runtime server is part of your migration setup, ensure the permissions Microsoft.DBforPostgreSQL/flexibleServers/migrations/* are included in the scope of the runtime server.

By setting up these permissions, you ensure that your migration process is both secure and aligned with PostgreSQL Migration Service requirements.

## (Preview) Online Migration publication permissions

Publication creation is mandatory in Online migration to define the data set for [logical replication with pgoutput](https://www.postgresql.org/docs/current/logical-replication-architecture.html) during PostgreSQL migration. It controls the granularity and ensures that only desired table changes are streamed for replication, supporting efficient and controlled cloud migration workflows.

You have to enable publication creation at the source through any **one** of the below options:

1. **Grant Create on Database + Use Inheritance Role**: In this option, you can provide the migration user required permissions without altering table ownership.

For all the databases that you are planning to migrate – `CREATE` gives the user permission to create a publication to streams changes.

```bash
GRANT CREATE ON DATABASE your_db TO migration_user;
```

Next, grant role membership to migration user so that **all** the tables can be included as part of the publication. Select user-defined roles that own tables or objects in the database. This has to be done for **all** the tables of the Database to be migrated.

```bash
GRANT role1,  role2...etc  TO migration_user;
```

2. **Use Superuser credentials at the source for migration**: Superuser credential helps source user create the desired publication without any permission issues.

```bash
CREATE ROLE migration_user WITH LOGIN SUPERUSER PASSWORD 'your_secure_password'; 
```

Elevated access can also be achieved by granting superuser privileges to an existing role to be used for migration:  

```bash
ALTER ROLE existing_migration_user WITH SUPERUSER;
```

3. **Grant Create on Database + Transfer Ownership (Altering Owner)**: Allow a non-superuser migration user to create publications by giving them the needed privileges and control over tables.

```bash
GRANT CREATE ON DATABASE your_db TO migration_user; 
```

```bash
ALTER TABLE table1, table2...etc OWNER TO migration_user; 
```

Ownership of **all** tables of the Database to be migrated has to be changed to migration_user. Changing table ownership and reverting back may affect application permissions.

### Table configuration for Change Data Capture

The following table lists the scenarios where Change data capture (CDC) operations are supported:

| Table type | Insert | Update | Delete | Truncate |
| --- | --- | --- | --- | --- |
| With Primary Key | Supported | Supported | Supported | Supported |
| Replica Identity = INDEX | Supported | Supported | Supported | Supported |
| Replica Identity = FULL | Supported | Supported | Supported | Supported |
| No Primary Key, Replica Identity = DEFAULT  | Supported | Not Supported | Not Supported | Supported |

The migration will fail if any unsupported actions are performed.

## Related content

- [Migration service](concepts-migration-service-postgresql.md)
- [Network setup](how-to-network-setup-migration-service.md)
- [Premigration validations](concepts-premigration-migration-service.md)
