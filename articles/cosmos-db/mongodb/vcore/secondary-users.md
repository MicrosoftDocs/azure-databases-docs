---
  title: Read and Read/Write privileges with secondary users on Azure Cosmos DB for MongoDB vCore
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: Learn how to create and configure secondary users  
  author: sajeetharan
  ms.author: sasinnat
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: conceptual
  ms.date: 11/02/2024
---

# Read and Read/Write Privileges with Secondary Users on Azure Cosmos DB for MongoDB vCore (Preview)

Azure Cosmos DB for MongoDB vCore now supports secondary users with specialized read-write roles. This feature enables secondary users to access and modify data without requiring full administrative privileges, making it easier to delegate responsibilities while enhancing data security. By allowing granular access control, teams can confidently extend data access to various stakeholders, such as developers and analysts, without compromising system integrity.


## Configuring Secondary Users 

 > [!NOTE]
>  Enable this feature before creating a cluster. It can only be enabled using an ARM template during the preview phase.


```powershell
"previewFeatures": {
            "value": [
                "EnableReadOnlyUser"
            ]
        }

```
 
# Supported commands and examples

 The MongoDB vCore  now supports Role-Based Access Control (RBAC) for secondary users with read and write privileges. This allows administrators to assign roles that grant access to secondary databases for essential read operations while protecting primary data integrity.

 > [!NOTE]
>  You can use any of the MongoDB drivers or mongotools such as mongosh to perform these operations.

## Authenticate and perform operations via Mongosh

```powershell
mongosh mongodb+srv://<YOUR_USERNAME>:<YOUR_PASSWORD>@>YOUR_HOST>?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000

```
 > [!NOTE]
>  Make sure you whitelist your client IP under the networking settings on azure portal. 

### CreateUser

Creates a new user on the database where you run the command. The `createUser` 
command returns a duplicate user error if the user exists. 

#### Admin Role 

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

#### ReadOnly Role

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

### Update User

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

### Drop User

Removes the user from the database on which you run the command. 


```powershell
use admin
db.runCommand(
    {
        dropUser:"<username>"
    }
)
```

### List Users

Returns information about one or more users.

```powershell
use admin
db.runCommand(
    {
        usersInfo:1
    }
)
```

## Limitations

-  You can create up to 10 users/roles per database.
-  The `Updateuser` command now only supports password updates and cannot modify other object fields.
