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

The Data API for Azure Cosmos DB for MongoDB vCore is an https interface that allows developers to access and interact with their MongoDB vCore data without needing a database driver. It simplifies data operations by enabling control plane and aggregation operations through HTTP requests. This API is ideal for web applications, providing secure and scalable access to MongoDB vCore databases.  
 

## Enabling Data API on MongoDB vCore

You can enable or disable this feature using the Azure portal, Azure CLI or an ARM template.

### Steps to enable Data API on Azure portal

1. **Go to Azure portal**
    - portal.azure.com

2. **Go to your vCore-based Azure Cosmos DB for MongoDB cluster**

3. **Open the 'Features' blade**

4. **Click on 'Data API'**

5. **Click on 'Enable'**

6. **Verify the result**
    - Your 'Features' blade should now display 'Data API' as 'On'.


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
curl {cluster-name}.data.mongocluster.cosmos.azure.com:443/data/v1/action/aggregate -H "Content-Type: application/ejson" -H "Accept:application/ejson" -d '{"database" : "testDB", "collection" : "testCollection", "pipeline" : [{"$limit" : 500}]}' --user "{username}:{password}"
```

```json
{ "documents" : [ { "_id" : { "$oid" : "680957492551581200c73bf8" }, "name" : "Sample Document", "createdAt" : { "$date" : { "$numberLong" : "1745442633506" } }, "tags" : [ "test", "mongo", "sample" ] } ] }
```

#### List databases

List all databases in the specified MongoDB vCore cluster.

```bash
curl {cluster-name}.data.global.mongocluster.cosmos.azure.com:443/data/v1/action/listDatabases -H "Content-Type: application/ejson" -H "Accept:application/ejson" -d '{}' --user "{username}:{password}"
```

```json
{ "databases" : [ { "name" : "testDB", "sizeOnDisk" : { "$numberInt" : "0" }, "empty" : false }, { "name" : "test", "sizeOnDisk" : { "$numberInt" : "0" }, "empty" : false } ], "totalSize" : { "$numberInt" : "0" }, "ok" : { "$numberDouble" : "1.0" } }
```

#### List collections

List all collections within a specific database.

```bash
curl {cluster-name}.data.global.mongocluster.cosmos.azure.com:443/data/v1/action/listCollections -H "Content-Type: application/ejson" -H "Accept:application/ejson" -d '{"database": "newDB"}' --user "{username}:{password}"
```

```json
{ "collections" : [ { "name" : "testCollection", "type" : "collection", "options" : {  }, "info" : { "readOnly" : false, "uuid" : { "$binary" : { "base64" : "mNh96KepTm+NtLtALGxDiw==", "subType" : "04" } } }, "idIndex" : { "v" : { "$numberInt" : "2" }, "name" : "_id_", "key" : { "_id" : { "$numberInt" : "1" } } } } ] }
```

### Get schema

Retrieve the schema details of a specific database.


Here's the formatted version for your .md file:

```bash
curl {cluster-name}.data.mongocluster.cosmos.azure.com:443/data/v1/action/getSchema -H "Content-Type: application/ejson" -H "Accept:application/ejson" -d '{"database" : "testDB", "collection" : "testCollection"}' --user "{username}:{password}"
```

```json
{ "_id" : { "bsonType" : "objectId" }, "name" : { "bsonType" : "string" }, "createdAt" : { "bsonType" : "date" }, "tags" : { "bsonType" : "array" } }
```

### Limitations

- Data API works on newly created MongoDB vCore cluster.
- Data API doesn't support access using reusable access token.
- Only supports data plane aggregation and limited control plane actions.
