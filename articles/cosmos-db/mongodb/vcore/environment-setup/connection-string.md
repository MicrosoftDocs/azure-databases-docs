---
title: |
  Tutorial: Azure Cosmos DB for MongoDB vCore: Connection String for Azure Cosmos DB MongoDB vCore
titleSuffix: Azure Cosmos DB for MongoDB (vCore)
description: In this tutorial, we explore the connection string format for Azure Cosmos DB for MongoDB vCore, detailing its components and usage. The guide provides a comprehensive explanation of the mongodb+srv format, covering critical parameters such as <username>, <password>, <cluster-url>, <database>, and various optional settings to optimize database connectivity. This documentation is tailored for developers and IT professionals to ensure secure, scalable, and efficient interactions with Cosmos DB for MongoDB vCore, complete with configuration guidelines.
author: v-smedapati
ms.author: v-smedapati
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: tutorial
ms.date: 11/29/2024
# CustomerIntent: As a developer, I need to understand the connection string format for Azure Cosmos DB for MongoDB vCore, focusing on securely connecting to the database, configuring optional parameters for optimized performance, and integrating it seamlessly into various applications.
---


# Connection String for Azure Cosmos DB MongoDB vCore

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

To connect to Azure Cosmos DB using the MongoDB API (often referred to as "Cosmos DB MongoDB vCore"), you'll need to create a connection string with the appropriate parameters. Below is a detailed guide to help you understand the connection string format, the various parameters, and examples of how to use them.

A typical connection string for Cosmos DB using MongoDB API looks like this:
```plaintext
mongodb+srv://<username>:<password>@<cluster-url>/<database>?<options>	
```
## Key Components in the Connection String

1. `mongodb+srv://`:
This prefix specifies the protocol to connect to the database.
    - `mongodb`: Indicates the MongoDB protocol.
    - `+srv`: Indicates a DNS SRV record, which simplifies connecting to clusters by automatically resolving the server addresses.

1. `<username>`:
This is the MongoDB username for your Cosmos DB account. You can create this through the Azure Portal when setting up your Cosmos DB database account.
    
    Example `myusername`

1. `<password>`:
This is the password associated with the MongoDB username. Be sure to escape any special characters (like @, /, etc.) if they appear in the password.
    
    Example: `mypassword123`

1. `<cosmosdb-uri>`: 
The URI is the endpoint provided by Cosmos DB, which typically includes your region and the account name.
It can be found in the Keys section of the Azure Portal under your Cosmos DB account.
    
    Example: `mycosmosdb.mongo.cosmos.azure.com`

1. `<port>`:
Cosmos DB MongoDB API generally uses port 10255 for the connection. You can use this port unless your specific configuration suggests otherwise.

    Example: `10255`

1. `<database>`:
The database name you wish to connect to. This could be any database within your Cosmos DB instance.

    Example: `myDatabase`

1. `<options>`:
Optional parameters to configure the connection. Common options include:

    - `retryWrites`: Enables retryable writes (default: `true`).
    - `tls` or `ssl`: Ensures a secure connection. (`tls=true` or `ssl=true`)
    - `authSource`: Specifies the database to use for authentication.

    Example:
    ```plaintext
    retryWrites=true&tls=true&authSource=admin
    ```


## Full Example Connection Strings

### Example 1: Simple Connection
```plaintext
mongodb+srv://myUser:myPass%40word@myCluster.mongodb.cosmos.azure.com/myDatabase
```
The `@` character is encoded as `%40` in URLs because the `@` symbol has a specific function in URL syntax. It is commonly used to separate the username from the hostname in authentication strings.

### Example 2: With Options
```plaintext
mongodb+srv://myUser:myPass%40word@myCluster.mongodb.cosmos.azure.com/myDatabase?retryWrites=true&tls=true&authSource=admin
```

### Example 3: Connecting Without SRV
For environments that don’t support SRV, use the format without +srv:
```plaintext
mongodb://<username>:<password>@<host1>:<port>,<host2>:<port>,<host3>:<port>/<database>?<options>
```
Example:

```plaintext
mongodb://myUser:myPass%40word@myCluster1.mongo.cosmos.azure.com:27017,myCluster2.mongo.cosmos.azure.com:27017/myDatabase?tls=true&replicaSet=globaldb&authSource=admin
```

## Explanation of Common Connection Options

Here are the current tiers for the service:

| Option | Description | Example |
| --- | --- | --- |
| `retryWrites` | Automatically retries certain write operations. Default: `true`. | `retryWrites=true` |
| `tls` or `ssl` | Enables Transport Layer Security (TLS) for secure connections. | `tls=true` |
| `authSource` | Specifies the database to use for user authentication. | `authSource=admin` |
| `replicaSet` | Specifies the name of the replica set | `replicaSet=globaldb` |
| `maxPoolSize` | Limits the number of concurrent connections in the connection pool. | `maxPoolSize=50` |
| `connectTimeoutMS` | Time in milliseconds to wait for a connection to be established. | `connectTimeoutMS=3000` |
| `readPreference` | Specifies the preferred replica to read from (e.g., `primary`, `secondary`, or `nearest`). | `readPreference=primary` |


## Best Practices
1. **Secure Credentials**: Avoid hardcoding credentials. Use environment variables or a secrets manager.
1. **Connection Pooling**: Optimize connection pooling for better performance.
1. **TLS Encryption**: Always enable TLS (tls=true) for secure communication.
1. **Test Locally Before Deployment**: Verify the connection string works in your local environment before deploying to production.