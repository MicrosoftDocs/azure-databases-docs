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

The Data api for Azure Cosmos DB for MongoDB vCore is a https interface that allows developers to access and interact with their MongoDB vCore data without needing a database driver. It simplifies data operations by enabling CRUD and aggregation operations through HTTP requests. This API is ideal for web applications, providing secure and scalable access to MongoDB vCore databases.  
 

## Enabling Data api on MongoDB vCore

You can enable/disable this feature using Azure CLI or an ARM template. We will be adding the support to enable/disable this feature soon.

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
**Endpoint:** `https://eastus2euap.management.azure.com/subscriptions/<subscriptionId>/resourceGroups/<resourceGroup>/providers/Microsoft.DocumentDB/mongoClusters/<ClusterName>?api-version=2024-10-01-preview`


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

## Obtain Connection String

To obtain the connection string for your MongoDB vCore cluster, follow these steps:

1. Navigate to the **MongoDB vCore cluster** that you created.
2. Go to **Settings** and select **Connection Strings**.
3. Copy the **Data API endpoint** provided.

## How to use Data Api


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

### Limitations

- Data api works on newly created MongoDB vCore cluster.
- Data api does not support access using reusable access token.
- Only support aggregate and few additional list control plane actions.

