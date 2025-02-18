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

# Connection Pooling for Cosmos DB for MongoDB vCore

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

Connection pooling is a technique used to manage and reuse database connections efficiently. It minimizes the overhead of establishing and closing connections repeatedly, improving performance and scalability. For Cosmos DB for MongoDB vCore, effective connection pooling is crucial for handling high-throughput applications and optimizing resource utilization.

## What is Connection Pooling?

- `Definition`: A pool of reusable connections maintained by the driver or application to interact with the database.
- `Purpose`: To reduce latency and resource consumption during database operations.
- `Implementation`: Managed by the database driver, configured through parameters in the connection string or programmatically.

## Benefits of Connection Pooling
- `Reduced Latency`: Eliminates the need to establish a new connection for each request.
- `Improved Throughput`: Enables concurrent operations by reusing existing connections.
- `Resource Optimization`: Reduces the load on the database server by controlling the number of active connections.
- `Scalability`: Supports applications with high user concurrency.

## Configuring Connection Pooling for Cosmos DB MongoDB API

**Connection String Parameters**: Cosmos DB MongoDB API supports connection pooling configurations through parameters in the connection string. Key parameters include:

| Parameter | Description | Default Value | Example |
| --- | --- | --- | --- |
| `maxPoolSize` | Maximum number of connections in the pool. | 100 | `maxPoolSize=200` |
| `minPoolSize` | Minimum number of connections to maintain in the pool. | 0 | `minPoolSize=10` |
| `waitQueueTimeoutMS` | Time (in milliseconds) a thread waits for a connection to become available before throwing an error. | Unlimited | `waitQueueTimeoutMS=5000` |
| `connectTimeoutMS` | Time (in milliseconds) to wait before timing out while connecting. | 30000 | `connectTimeoutMS=1000` |
| `socketTimeoutMS` | Time (in milliseconds) before closing a socket due to inactivity. | 30000 | `socketTimeoutMS=10000` |

### Example Connection String with Pooling Parameters:
```plaintext
mongodb+srv://<username>:<password>@<cluster-url>/<database>?maxPoolSize=200&minPoolSize=10&waitQueueTimeoutMS=5000
```

## Best Practices for Connection Pooling

1. Optimize Pool Size:
    - Set `maxPoolSize` based on the expected load and server capacity.
    - Use `minPoolSize` to maintain a base level of connections, reducing latency during spikes.

1. Timeout Management:
    - Configure `waitQueueTimeoutMS` to prevent requests from waiting indefinitely.
    - Set `connectTimeoutMS` and `socketTimeoutMS` to reasonable values for your application.

1. Monitor Pool Usage:

    - Use monitoring tools to track the number of active and idle connections.
    - Adjust pool settings based on observed usage patterns.

1. Secure Connections:

    - Always enable TLS (`tls=true`) in the connection string for secure communication.

1. Avoid Over-Provisioning:

    - Excessively high `maxPoolSize` can lead to resource contention on the client and server.

## Programmatic Configuration Examples
**Python: Using PyMongo**
```python
from pymongo import MongoClient

# Connection URI with pooling options
uri = "mongodb+srv://<username>:<password>@<cluster-url>/<database>?maxPoolSize=200&minPoolSize=10&waitQueueTimeoutMS=5000"

# Create client
client = MongoClient(uri)

# Access database
db = client["myDatabase"]

# Perform operations
print(db.list_collection_names())
```    

**Node.js: Using MongoDB Driver**
```js
const { MongoClient } = require('mongodb');

// Connection URI with pooling options
const uri = "mongodb+srv://<username>:<password>@<cluster-url>/<database>?maxPoolSize=200&minPoolSize=10&waitQueueTimeoutMS=5000";

// Create client
const client = new MongoClient(uri, {
  useNewUrlParser: true,
  useUnifiedTopology: true,
});

async function run() {
  try {
    await client.connect();
    console.log("Connected successfully to MongoDB vCore server");

    const db = client.db("myDatabase");
    const collections = await db.listCollections().toArray();
    console.log("Collections:", collections);
  } finally {
    await client.close();
  }
}

run().catch(console.error);
```

## Troubleshooting Common Issues

| Issue | Cause | Solution |
| --- | --- | --- |
|High Latency | Insufficient pool size or high contention. | Increase maxPoolSize and monitor connection usage. |
| Timeout Errors | Connections are exhausted or wait time is too short. | Adjust waitQueueTimeoutMS and connectTimeoutMS values. |
| Resource Contention on Server | Excessively high maxPoolSize. | Reduce maxPoolSize to balance client-server resource usage. |
| Idle Connections | minPoolSize is set too high. | Lower minPoolSize to align with typical workload. |
