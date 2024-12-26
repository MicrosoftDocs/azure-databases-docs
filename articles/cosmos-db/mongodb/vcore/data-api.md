---
  title: Data API for Azure Cosmos DB for MongoDB vCore
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: Explains how to interact with your MongoDB vCore data over HTTPS with simple RESTful endpoints.
  author: sajeetharan
  ms.author: sasinnat
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: conceptual
  ms.date: 11/03/2024
---

# Data API for Azure Cosmos DB for MongoDB vCore (Preview)

The Data API for Azure Cosmos DB for MongoDB vCore is an https interface that allows developers to access and interact with their MongoDB vCore data without needing a database driver. It simplifies data operations by enabling CRUD and aggregation operations through HTTP requests. This API is ideal for web applications, providing secure and scalable access to MongoDB vCore databases.  
 

## Enabling Data API on MongoDB vCore

You can enable or disable this feature using the Azure CLI or an ARM template. Portal support will be added soon.

### Steps to enable Data API on vCore cluster via ARM template

1. **Get connection string**:
   - Obtain the connection string of your vCore cluster from the Azure portal.

2. **Retrieve authentication token**:
   - Run the following commands in Windows PowerShell:
     ```powershell
     az login
     az account get-access-token --resource-type arm
     ```

3. **Send PATCH request**:
   - Use the connection string from the Azure portal and send a PATCH request with:
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

4. **Verify result**:
   - Ensure the response payload includes `"dataApi": {"mode": "Enabled"}`.
   - If you encounter the error "Data API isn't supported on this cluster," note that only newly provisioned clusters support Data API.

## Update MongoDB vCore cluster configuration

### Request

**Method:** `PATCH`  
**Endpoint:** `https://eastus2euap.management.azure.com/subscriptions/<subscriptionId>/resourceGroups/<resourceGroup>/providers/Microsoft.DocumentDB/mongoClusters/<ClusterName>?api-version=2024-10-01-preview`


### Request body

```json
{
  "properties": {
    "dataApi": {
      "mode": "Enabled"
    }
  }
}
```

## Obtain connection string

To obtain the connection string for your MongoDB vCore cluster, follow these steps:

1. Navigate to the **MongoDB vCore cluster** that you created.
2. Go to **Settings** and select **Connection Strings**.
3. Copy the **Data API endpoint** provided.

## How to use Data API

Let's explore the supported operations, how to use the Data API.

#### Aggregate

Use this command to perform an aggregation operation on a collection.

```bash
curl {cluster-name}.data.global.mongocluster.cosmos.azure.com:443/data/v1/action/aggregate -H "Content-Type: application/ejson" -H "Accept:application/ejson" -d '{"database": "newDB", "collection": "newCollection", "pipeline": [{"$limit": 500}]}'
```

#### List databases

List all databases in the specified MongoDB vCore cluster.

```bash
curl {cluster-name}.data.global.mongocluster.cosmos.azure.com:443/data/v1/action/listDatabases -H "Content-Type: application/ejson" -H "Accept:application/ejson" -d '{}'

```

#### List collections

List all collections within a specific database.

```bash
curl {cluster-name}.data.global.mongocluster.cosmos.azure.com:443/data/v1/action/listCollections -H "Content-Type: application/ejson" -H "Accept:application/ejson" -d '{"database": "newDB"}'
```

### Get schema

Retrieve the schema details of a specific database.


Here's the formatted version for your .md file:

```bash
curl {cluster-name}.data.global.mongocluster.cosmos.azure.com:443/data/v1/action/getSchema -H "Content-Type: application/ejson" -H "Accept:application/ejson" -d '{"database": "newDB"}'
```

### Limitations

- Data API works on newly created MongoDB vCore cluster.
- Data API doesn't support access using reusable access token.
- Only support aggregate and few other list control plane actions.

