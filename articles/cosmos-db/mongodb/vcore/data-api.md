---
  title: Data api for Azure Cosmos DB for MongoDB vCore
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: Explains how to interact with your MongoDB vCore data over HTTPS with simple RESTful endpoints
  author: sajeetharan
  ms.author: sasinnat
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: conceptual
  ms.date: 11/03/2024
---

# Data api for Azure Cosmos DB for MongoDB vCore (Preview)

The Data API for for Azure Cosmos DB for MongoDB vCore is a RESTful interface that allows developers to access and interact with their MongoDB vCore data without needing a database driver. It simplifies data operations by enabling CRUD and aggregation operations through HTTP requests. This API is ideal for web applications, providing secure and scalable access to MongoDB vCore databases.  
 

## Enabling Data api on MongoDB vCore

You can Enable/Disable this feature using Azure CLI or an ARM template.  

### Steps to Enable Data API on vCore Cluster via ARM template

1. **Get Connection String**:
   - Obtain the connection string of your vCore cluster from the Azure Portal.

2. **Retrieve Authentication Token**:
   - Run the following commands in Windows PowerShell:
     ```powershell
     az login
     az account get-access-token --resource-type arm
     ```

3. **Send PATCH Request**:
   - Use the connection string from the Azure Portal and send a PATCH request with:
     - **Authentication Token**: Use the token retrieved from PowerShell.
     - **Body**:
       ```json
       {
         "properties": {
           "dataApi": {
             "mode": "Enabled"
           }
         }
       }
       ```

4. **Verify Result**:
   - Ensure the response payload includes `"dataApi": {"mode": "Enabled"}`.
   - If you encounter the error "Data Api is not supported on this cluster," note that only newly provisioned clusters support Data Api.

## Update MongoDB vCore Cluster Configuration

### Request

**Method:** `PATCH`  
**Endpoint:** `https://eastus2euap.management.azure.com/subscriptions/7becce9d-b7ae-4daf-8b8b-e0544927ed88/resourceGroups/wilwangresourcegroup/providers/Microsoft.DocumentDB/mongoClusters/wilwangcluster?api-version=2024-10-01-preview`


### Request Body

```json
{
  "properties": {
    "dataApi": {
      "mode": "Enabled"
    }
  }
}
```
### Response

```
{
  "id": "/subscriptions/7becce9d-b7ae-4daf-8b8b-e0544927ed88/resourceGroups/wilwangresourcegroup/providers/Microsoft.DocumentDB/mongoClusters/wilwangcluster",
  "name": "wilwangcluster",
  "type": "Microsoft.DocumentDB/mongoClusters",
  "tags": {},
  "location": "eastus2",
  "systemData": {
    "createdAt": "2024-10-03T22:52:53.4411804Z",
    "createdBy": "wilwang@microsoft.com",
    "createdByType": "User",
    "lastModifiedAt": "2024-10-18T17:46:06.0179756Z",
    "lastModifiedBy": "wilwang@microsoft.com",
    "lastModifiedByType": "User"
  },
  "properties": {
    "provisioningState": "Succeeded",
    "clusterStatus": "Ready",
    "administrator": {
      "userName": "wilwang"
    },
    "serverVersion": "7.0",
    "compute": {
      "tier": "M40"
    },
    "storage": {
      "sizeGb": 128
    },
    "sharding": {
      "shardCount": 1
    },
    "highAvailability": {
      "targetMode": "ZoneRedundantPreferred"
    },
    "connectionString": "mongodb+srv://<user>:<password>@wilwangcluster.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000",
    "backup": {
      "earliestRestoreTime": "2024-10-03T23:00:37Z"
    },
    "privateEndpointConnections": [],
    "publicNetworkAccess": "Enabled",
    "previewFeatures": [
      "GeoReplicas"
    ],
    "replica": {
      "role": "Primary",
      "replicationState": "Active"
    },
    "infrastructureVersion": "2.0",
    "dataApi": {
      "mode": "Enabled"
    }
  }
}
```

## Obtain Connection String

To obtain the connection string for your MongoDB vCore cluster, follow these steps:

1. Navigate to the **MongoDB vCore cluster** that you created.
2. Go to **Settings** and select **Connection Strings**.
3. Copy the **Data API endpoint** provided.

# How to use Data Api

# Sample Curl Commands for Azure Cosmos DB MongoDB Cluster

Run the following `curl` commands with the format:

```bash
curl <connection-string> -H "Content-Type: application/ejson" -H "Accept:application/ejson" -d '{<parameters>}'
```
### Aggregate

Use this command to perform an aggregation operation on a collection.

```bash
curl {cluster-name}.data.global.mongocluster.cosmos.azure.com:443/data/v1/action/aggregate \
-H "Content-Type: application/ejson" \
-H "Accept:application/ejson" \
-d '{
      "database": "newDB",
      "collection": "newCollection",
      "pipeline": [{"$limit": 500}]
    }'
```

### List Databases

List all databases in the cluster.

```bash
curl {cluster-name}.data.global.mongocluster.cosmos.azure.com:443/data/v1/action/listDatabases \
-H "Content-Type: application/ejson" \
-H "Accept:application/ejson" \
-d '{}'
```

### List Collections

List all collections within a specific database.

```bash
curl {cluster-name}.data.global.mongocluster.cosmos.azure.com:443/data/v1/action/listCollections \
-H "Content-Type: application/ejson" \
-H "Accept:application/ejson" \
-d '{
      "database": "newDB"
    }'
```

### Get Schema

Get the schema of a specific database.

```bash
curl {cluster-name}.data.global.mongocluster.cosmos.azure.com:443/data/v1/action/getSchema \
-H "Content-Type: application/ejson" \
-H "Accept:application/ejson" \
-d '{
      "database": "newDB"
    }'
```

## Limitations

- Data api works on newly created MongoDB vCore cluster.
- Data api does not support access using reusable access token.
- Only support aggregate and few additional list control plane actions.

