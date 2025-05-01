---
  title: Read and read/write privileges with secondary native users on Azure Cosmos DB for MongoDB vCore
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: Learn how to create and configure secondary native users  
  author: sajeetharan
  ms.author: sasinnat
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: conceptual
  ms.date: 04/29/2025
---

# Read and read/write privileges with secondary users on Azure Cosmos DB for MongoDB vCore

> [!IMPORTANT]
> Secondary native users feature in Azure Cosmos DB for MongoDB vCore is currently in preview.
> This preview version is provided without a service level agreement, and it isn't recommended
> for production workloads. Certain features might not be supported or might have constrained
> capabilities.

Azure Cosmos DB for MongoDB vCore now supports secondary users with specialized read-write roles. This feature enables secondary users to access and modify data, making it easier to delegate responsibilities while enhancing data security. If you allow granular access control, teams can confidently extend data access to various stakeholders, such as developers and analysts, without compromising system integrity.

## Prerequisites

1. [An Azure Cosmos DB for MongoDB vCore cluster](./quickstart-portal.md)

## Configuring secondary users 

Enable secondary native user management on the cluster for all native user management operations, such as creating and deleting users. You can enable or disable this feature using an ARM template or via [Azure CLI](/cli/azure/get-started-with-azure-cli).

# [Azure CLI](#tab/cli)
```azurecli-interactive
az resource patch --ids "/subscriptions/{SubscriptionId}/resourceGroups/{ResourceGroup}/providers/Microsoft.DocumentDB/mongoClusters/{ClusterName}" --api-version 2024-10-01-preview --properties "{\"previewFeatures\": [\"EnableReadOnlyUser\"]}"
```

# [ARM template](#tab/arm)
```PowerShell
"previewFeatures": {
            "value": [
                "EnableReadOnlyUser"
            ]
        }
```
---

When secondary user management is disabled, all secondary user operations on the cluster are disabled, but all secondary users created on the cluster can still be used for database access. If you need to remove all secondary users, use [the delete operation](#delete-user).

## Supported commands and examples

One administrative user with all privileges is created on the Azure Cosmos DB for MonogDB vCore cluster during cluster provisioning. This administrative user can perform all operations on the cluster and can't be deleted.

In addition, Azure Cosmos DB for MongoDB vCore supports role-based access control (RBAC) for secondary users with read-only or read-write privileges. This capability allows administrators to assign roles that grant access to secondary users for essential read operations while protecting primary data integrity.

Users are created and granted privileges at the cluster level for all databases on that cluster. The **readWriteAnyDatabase** and **clusterAdmin** roles together grant full read-write permissions on the cluster, including privileges for database management and database operations. The **readAnyDatabase** role is used to grant read-only permissions on the cluster.

 > [!NOTE]
>  Only full read-write users with database management and database operations privileges are supported. You can't assign **readWriteAnyDatabase** and **clusterAdmin** roles separately.

You can use any of the MongoDB drivers or tools such as mongosh to perform these operations.

### Authenticate and perform operations via Mongosh

```powershell
mongosh "mongodb+srv://<UserName>:<Password>@<ClusterName>?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000"
```
 > [!TIP]
>  You can get native connection string for the cluster in the Azure portal on the 'Connection strings' page.

### Create a user

Creates a new user on the cluster where you run the command. The `createUser` command returns a duplicate user error if the user exists.

#### Data admin users 

```powershell
use admin
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
use admin
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

## Limitations

-  You can create up to 10 users/roles per cluster. If you have a requirement to add more users, please open a [support ticket](/azure/azure-portal/supportability/how-to-create-azure-support-request).
-  The `Updateuser` command now only supports password updates and can't modify other object fields.
-  The `Roleinfo` command isn't supported in preview. Alternatively you can use `usersInfo`.
-  Assigning roles to specific databases or collections isn't supported.

## Next steps

- Learn about [security in Azure Cosmos DB for MongoDB vCore](./security.md)

