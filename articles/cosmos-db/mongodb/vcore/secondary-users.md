---
  title: Read and Read/Write privileges with secondary users on Azure Cosmos DB for MongoDB vCore
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: Learn how to create and configure secondary users  
  author: sajeetharan
  ms.author: sasinnat
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: conceptual
  ms.date: 02/18/2025
---

# Read and Read/Write Privileges with Secondary Users on Azure Cosmos DB for MongoDB vCore (Preview)

Azure Cosmos DB for MongoDB vCore now supports secondary users with specialized read-write roles. This feature enables secondary users to access and modify data, making it easier to delegate responsibilities while enhancing data security. If you allow granular access control, teams can confidently extend data access to various stakeholders, such as developers and analysts, without compromising system integrity.


## Configuring secondary users 

 > [!NOTE]
>  You can enable/disable this feature by using an ARM template or via Azure CLI during the preview phase.

### Using Azure CLI

```Bash
    az resource patch --ids "/subscriptions/{SubscriptionId}/resourceGroups/{ResourceGroup}/providers/Microsoft.DocumentDB/mongoClusters/{ClusterName}" --api-version 2024-10-01-preview --properties "{\"previewFeatures\": [\"EnableReadOnlyUser\"]}"
```

### Using ARM template


```powershell
"previewFeatures": {
            "value": [
                "EnableReadOnlyUser"
            ]
        }

```
 
## Supported commands and examples

 The MongoDB vCore now supports Role-Based Access Control (RBAC) for secondary users with read and write privileges. This capability allows administrators to assign roles that grant access to secondary databases for essential read operations while protecting primary data integrity.

 > [!NOTE]
>  You can use any of the MongoDB drivers or mongotools such as mongosh to perform these operations.

## Authenticate and perform operations via Mongosh

```powershell
mongosh mongodb+srv://<YOUR_USERNAME>:<YOUR_PASSWORD>@>YOUR_HOST>?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000
```
 > [!NOTE]
>  Make sure you allowlist your client IP under the networking settings on Azure portal. 

### CreateUser

Creates a new user on the database where you run the command. The `createUser` 
command returns a duplicate user error if the user exists. 

#### Data admin role 

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

#### ReadOnly role

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

Updates a user on the database where you run the command. The `updateUser` 
command supports only updating the password.

```powershell
use admin
db.runCommand(
    {
        updateUser:"<username>",
        pwd : "<new cleartext password>"
    }
)
```

### Drop user

Removes the user from the database on which you run the command. 

```powershell
use admin
db.runCommand(
    {
        dropUser:"<username>"
    }
)
```

### List users

Returns information about one or more users. It also supports passing in a single user to `usersInfo`. In that case, it returns information about the user, its role, etc.



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
-  RBAC support for assigning roles to specific databases or collections isn't yet supported.
