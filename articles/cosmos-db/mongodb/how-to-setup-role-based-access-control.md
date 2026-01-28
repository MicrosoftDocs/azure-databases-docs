---
title: Configure Role-Based Access Control
titleSuffix: Azure Cosmos DB for MongoDB
description: Learn how to configure role-based access control in Azure Cosmos DB for MongoDB to secure data access.
author: gahl-levy
ms.author: gahllevy
ms.service: azure-cosmos-db
ms.subservice: mongodb
ms.topic: how-to
ms.date: 08/20/2025
ms.custom:
  - devx-track-azurecli
  - devx-track-extended-java
  - devx-track-js
  - sfi-ropc-nochange
appliesto:
  - ✅ MongoDB
ai-usage: ai-assisted
---

# Configure role-based access control in Azure Cosmos DB for MongoDB

Azure Cosmos DB for MongoDB provides a built-in role-based access control system for data plane operations. Use role-based access control to authorize data requests with fine-grained, role-based permissions. This guide shows you how to enable role-based access control, create roles and users, and authenticate with supported drivers.

## Prerequisites

- An Azure subscription
- An Azure Cosmos DB for MongoDB account (version 3.6 or higher)
- Latest version of Azure CLI

## Enable role-based access control

Enable role-based access control on your Azure Cosmos DB for MongoDB account.

1. Sign in to Azure CLI.

    ```azurecli-interactive		
    az login
    ```

1. Enable the role-based access control capability on your database account.

    ```azurecli-interactive		
    az cosmosdb create \
        --resource-group "<resource-group-name>" \
        --name "<account-name>" \
        --kind "MongoDB" \
        --capabilities "EnableMongoRoleBasedAccessControl"
    ```

    > [!TIP]
    > You can also enable role-based access control from the Features tab in the Azure portal.

3. Create a database for users to connect to in the Azure portal.

## Create roles and users

Define custom roles and users to control access to your database account.

1. Create a role definition.

    ```azurecli-interactive
    az cosmosdb mongodb role definition create \
        --resource-group "<resource-group-name>" \
        --account-name "<account-name>" \
        --body {\"Id\":\"test.My_Read_Only_Role101\",\"RoleName\":\"My_Read_Only_Role101\",\"Type\":\"CustomRole\",\"DatabaseName\":\"test\",\"Privileges\":[{\"Resource\":{\"Db\":\"test\",\"Collection\":\"test\"},\"Actions\":[\"insert\",\"find\"]}],\"Roles\":[]}
    ```

    > [!TIP]
    > Alternatively, use a JSON file:
    >
    > ```azurecli-interactive
    > az cosmosdb mongodb role definition create \
    >    --resource-group "<resource-group-name>" \
    >    --account-name "<account-name>" \
    >    --body @role.json
    > ```
    >
    > ```json
    > {
    >   "Id": "test.My_Read_Only_Role101",
    >   "RoleName": "My_Read_Only_Role101",
    >   "Type": "CustomRole",
    >   "DatabaseName": "test",
    >   "Privileges": [{
    >     "Resource": {
    >       "Db": "test",
    >       "Collection": "test"
    >     },
    >     "Actions": ["insert", "find"]
    >   }],
    >   "Roles": []
    > }
    > ```
    >

1. Create a user definition with a role assignment.

    ```azurecli-interactive
    az cosmosdb mongodb user definition create \
        --resource-group "<resource-group-name>" \
        --account-name "<account-name>" \
				--body {\"Id\":\"test.myName\",\"UserName\":\"myName\",\"Password\":\"pass\",\"DatabaseName\":\"test\",\"CustomData\":\"Some_Random_Info\",\"Mechanisms\":\"SCRAM-SHA-256\",\"Roles\":[{\"Role\":\"My_Read_Only_Role101\",\"Db\":\"test\"}]}
    ```

    > [!TIP]
    > Alternatively, use a JSON file:
    >
    > ```azurecli-interactive
    > az cosmosdb mongodb role definition create \
    >    --resource-group "<resource-group-name>" \
    >    --account-name "<account-name>" \
    >    --body @role.json
    > ```
    >
    > ```json
    > {
    >   "Id": "test.myName",
    >   "UserName": "myName",
    >   "Password": "pass",
    >   "DatabaseName": "test",
    >   "CustomData": "Some_Random_Info",
    >   "Mechanisms": "SCRAM-SHA-256",
    >   "Roles": [{
    >     "Role": "My_Read_Only_Role101",
    >     "Db": "test"
    >   }]
    > }
    > ```
    >

## Authenticate with drivers

Connect to your database using supported drivers and role-based access control credentials.

### [Python (`pymongo`)](#tab/python)

```python
from pymongo import MongoClient
client = MongoClient(
    "mongodb://<YOUR_HOSTNAME>:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000",
    username="<YOUR_USER>",
    password="<YOUR_PASSWORD>",
    authSource='<YOUR_DATABASE>',
    authMechanism='SCRAM-SHA-256',
    appName="<YOUR appName FROM CONNECTION STRING IN AZURE PORTAL>"
)
```

### [Node.js](#tab/nodejs)

```javascript
connectionString = "mongodb://" + "<YOUR_USER>" + ":" + "<YOUR_PASSWORD>" + "@" + "<YOUR_HOSTNAME>" + ":10255/" + "<YOUR_DATABASE>" +"?ssl=true&retrywrites=false&replicaSet=globaldb&authmechanism=SCRAM-SHA-256&appname=@" + "<YOUR appName FROM CONNECTION STRING IN AZURE PORTAL>" + "@";
var client = await mongodb.MongoClient.connect(connectionString, { useNewUrlParser: true, useUnifiedTopology: true });
```

### [Java](#tab/java)

```java
connectionString = "mongodb://" + "<YOUR_USER>" + ":" + "<YOUR_PASSWORD>" + "@" + "<YOUR_HOSTNAME>" + ":10255/" + "<YOUR_DATABASE>" +"?ssl=true&retrywrites=false&replicaSet=globaldb&authmechanism=SCRAM-SHA-256&appname=@" + "<YOUR appName FROM CONNECTION STRING IN AZURE PORTAL>" + "@";
MongoClientURI uri = new MongoClientURI(connectionString);
MongoClient client = new MongoClient(uri);
```

### [Mongo shell (`mongosh`)](#tab/mongo-shell)

```shell
mongosh --authenticationDatabase <YOUR_DB> --authenticationMechanism SCRAM-SHA-256 "mongodb://<YOUR_USERNAME>:<YOUR_PASSWORD>@<YOUR_HOST>:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000"
```

### [MongoDB Compass](#tab/mongodb-compass)

```shell
connectionString = "mongodb://" + "<YOUR_USER>" + ":" + "<YOUR_PASSWORD>" + "@" + "<YOUR_HOSTNAME>" + ":10255/" + "?ssl=true&retrywrites=false&replicaSet=globaldb&authmechanism=SCRAM-SHA-256&appname=@" + "<YOUR appName FROM CONNECTION STRING IN AZURE PORTAL>" + "@"
+"&authSource=" +"<YOUR_DATABASE>";
```

---

## Perform common operations

Now, perform some common operations for role-based access control features in Azure Cosmos DB for MongoDB.

1. Use the following command to display all role definitions.

    ```powershell
    az cosmosdb mongodb role definition list --account-name <account-name> --resource-group <resource-group-name>
    ```

1. Verify the existence of a role by its ID.

    ```powershell
    az cosmosdb mongodb role definition exists --account-name <account-name> --resource-group <resource-group-name> --id test.My_Read_Only_Role
    ```

1. Remove a role definition using its ID.

    ```powershell
    az cosmosdb mongodb role definition delete --account-name <account-name> --resource-group <resource-group-name> --id test.My_Read_Only_Role
    ```

1. Display all user definitions.

    ```powershell
    az cosmosdb mongodb user definition list --account-name <account-name> --resource-group <resource-group-name>
    ```

1. Verify the existence of a user by its ID.

    ```powershell
    az cosmosdb mongodb user definition exists --account-name <account-name> --resource-group <resource-group-name> --id test.myName
    ```

1. Remove a user definition using its ID.

    ```powershell
    az cosmosdb mongodb user definition delete --account-name <account-name> --resource-group <resource-group-name> --id test.myName
    ```

## Related content

- [Role-based access control](role-based-access-control.md)
- [Frequently asked questions about role-based access control](faq.yml#role-based-access-control)
