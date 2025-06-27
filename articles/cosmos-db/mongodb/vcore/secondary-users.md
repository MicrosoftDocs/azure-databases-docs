---
  title: Read and read/write privileges with secondary native users on Azure Cosmos DB for MongoDB vCore
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: Learn how to create and configure secondary native users  
  author: sajeetharan
  ms.author: sasinnat
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: how-to
  ms.date: 06/25/2025
  appliesto:
  - ✅ MongoDB (vCore)
---

# Read and read/write privileges with secondary native users on Azure Cosmos DB for MongoDB vCore

Azure Cosmos DB for MongoDB vCore supports secondary native [DocumentDB](./oss.md) users with specialized read-write and read-only roles. This feature enables secondary users to access and modify data, making it easier to delegate responsibilities while enhancing data security. If you allow granular access control, teams can confidently extend data access to various stakeholders, such as developers and analysts, without compromising system integrity.

When a cluster is created, a built-in administrative native user account is automatically added. This account has full privileges, including user management capabilities. To create additional native users, you must log in using this built-in administrative account.

If the cluster has [a replica](./cross-region-replication.md), all secondary native users are automatically replicated to the replica and can be used to access it. All native user management operations should be performed on the primary cluster.

## Prerequisites

- [An Azure Cosmos DB for MongoDB vCore cluster](./quickstart-portal.md)

## Supported commands and examples

One administrative user with all privileges is created on the Azure Cosmos DB for MonogDB vCore cluster during cluster provisioning. This administrative user can perform all operations on the cluster and can't be deleted.

In addition, Azure Cosmos DB for MongoDB vCore supports role-based access control (RBAC) for secondary users with read-only or read-write privileges. This capability allows administrators to assign roles that grant access to secondary users for essential read operations while protecting primary data integrity.

Users are created and granted privileges at the cluster level for all databases on that cluster. The **readWriteAnyDatabase** and **clusterAdmin** roles together grant full read-write permissions on the cluster, including privileges for database management and database operations. The **readAnyDatabase** role is used to grant read-only permissions on the cluster.

 > [!NOTE]
>  Only full read-write users with database management and database operations privileges are supported. You can't assign **readWriteAnyDatabase** and **clusterAdmin** roles separately.

You can use any of the MongoDB drivers or tools such as mongosh to perform these operations.

### Authenticate and perform operations via Mongosh

Authenticate using built-in administrative account created during cluster provisioning. Only this built-in administrative account has user management privileges (userAdmin) on the cluster.

```powershell
mongosh "mongodb+srv://<UserName>:<Password>@<ClusterName>?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000"
```

 > [!TIP]
>  You can get native connection string for the cluster in the Azure portal on the 'Connection strings' page.

### Create a user

Creates a new user on the cluster where you run the command. The `createUser` command returns a duplicate user error if the user already exists.

#### Data admin users 

```powershell
db.runCommand(
    {
        createUser:"yourUserName",
        pwd : "yourPassword",
        roles : [
            { role:"clusterAdmin",db:"admin" },
            { role:"readWriteAnyDatabase", db:"admin" }
        ]
    }
)
```

#### Read-only users

```powershell
db.runCommand(
    {
        createUser:"yourUserName",
        pwd : "yourPassword",
        roles : [
            { role:"readAnyDatabase",db:"admin" }
        ]
    }
)
```

### Update user

Updates a user on the database where you run the command. The `updateUser` command supports only updating the password.

```powershell
use admin
db.runCommand(
    {
        updateUser:"<username>",
        pwd : "<new cleartext password>"
    }
)
```

### Delete user

Removes the user from the cluster.

```powershell
use admin
db.runCommand(
    {
        dropUser:"<username>"
    }
)
```

### List users

Returns information about native users created on the cluster. It also supports passing in a single user to `usersInfo`. In that case, it returns information about the user, its role, etc.

```powershell
use admin
db.runCommand(
    {
        usersInfo:1
    }
)
```

## Next steps

- Learn about [security in Azure Cosmos DB for MongoDB vCore](./security.md)
- Check [preview limitations](./limits.md#native-documentdb-secondary-users)
- Learn about [Microsoft Entra ID in Azure Cosmos DB for MongoDB vCore](./entra-authentication.md)
