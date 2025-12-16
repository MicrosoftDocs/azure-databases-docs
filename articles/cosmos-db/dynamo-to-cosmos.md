---
title: Migrate Your Application from Amazon DynamoDB to Azure Cosmos DB
description: Learn how to migrate your .NET application from Amazon DynamoDB to Azure Cosmos DB.
author: manishmsfte
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.collection:
 - migration
 - aws-to-azure
ms.custom: devx-track-dotnet
ms.topic: how-to
ms.date: 05/02/2020
ms.author: mansha
appliesto:
  - ✅ NoSQL
---

# Migrate your application from Amazon DynamoDB to Azure Cosmos DB

Azure Cosmos DB is a scalable, globally distributed, fully managed database. It provides guaranteed low-latency access to your data.

This article describes how to migrate your .NET application from Amazon DynamoDB to Azure Cosmos DB with minimal code changes. To learn more about Azure Cosmos DB, see the [overview](introduction.md) article.

## Conceptual differences

The following table lists key conceptual differences between Azure Cosmos DB and DynamoDB:

| DynamoDB | Azure Cosmos DB |
|---|---|
| Not applicable | Database |
| Table | Collection |
| Item | Document |
| Attribute | Field |
| Secondary index | Secondary index |
| Primary key > partition key | Partition key |
| Primary key > sort key | Not required |
| Stream | Change feed |
| Write compute unit | Request unit (flexible, can be used for reads or writes) |
| Read compute unit | Request unit (flexible, can be used for reads or writes) |
| Global table| Not required. You can directly select the region while provisioning the Azure Cosmos DB account. (You can change the region later.) |

## Structural differences

The JSON structure of Azure Cosmos DB is simpler than the JSON structure of DynamoDB. The following example shows the differences.

### DynamoDB

The following JSON object represents the data format in DynamoDB:

```json
{
  "TableName": "Music",
  "KeySchema": [
    { 
      "AttributeName": "Artist",
      "KeyType": "HASH",
    },
    { 
      "AttributeName": "SongTitle",
      "KeyType": "RANGE"
    }
    ],
    "AttributeDefinitions": [
    { 
      "AttributeName": "Artist",
      "AttributeType": "S"
    },
    { 
      "AttributeName": "SongTitle",
      "AttributeType": "S"
    }
  ],
  "ProvisionedThroughput": {
    "ReadCapacityUnits": 1,
    "WriteCapacityUnits": 1
  }
}
```

With `Artist` as partition key and `SongTitle` as sort key.

### Azure Cosmos DB

The following JSON object represents the data format in Azure Cosmos DB:

```json
{
  "Artist": "",
  "SongTitle": "",
  "AlbumTitle": "",
  "Year": 9999,
  "Price": 0.0,
  "Genre": "",
  "Tags": ""
}
```

## Migrate your code

This article is scoped to migrate an application's code to Azure Cosmos DB, which is a critical aspect of database migration. To help you understand how the migration process works, the following sections compare the code between Amazon DynamoDB and Azure Cosmos DB.

To download the source code, clone the following repo:

```bash
git clone https://github.com/Azure-Samples/DynamoDB-to-CosmosDB
```

### Prerequisites

- .NET Framework 4.7.2.
- Latest version of [!INCLUDE [cosmos-db-visual-studio](includes/cosmos-db-visual-studio.md)]
- Access to an Azure Cosmos DB for NoSQL account.
- Local installation of Amazon DynamoDB.
- Java 8.
- Downloadable version of Amazon DynamoDB. Run it at port 8000. (You can change and configure the code.)

### Set up your code

Add the following NuGet package to your project:

```pwsh
Install-Package Microsoft.Azure.Cosmos
```

### Establish a connection

#### DynamoDB

In Amazon DynamoDB, you use the following code to connect:

```csharp
AmazonDynamoDBConfig addbConfig = new AmazonDynamoDBConfig();
addbConfig.ServiceURL = "endpoint";
try
{
    aws_dynamodbclient = new AmazonDynamoDBClient(addbConfig);
}
catch { }
```

#### Azure Cosmos DB

To connect Azure Cosmos DB, update your code to:

```csharp
client_documentDB = new CosmosClient(
    "<nosql-account-endpoint>",
    tokenCredential
);
```

#### Optimize the connection in Azure Cosmos DB

With Azure Cosmos DB, you can use the following options to optimize your connection:

- `ConnectionMode`: Use direct connection mode to connect to the data nodes in the Azure Cosmos DB service. Use gateway mode only to initialize and cache the logical addresses and refresh on updates. For more information, see [Azure Cosmos DB SQL SDK connectivity modes](sdk-connection-modes.md).

- `ApplicationRegion`: Use this option to set the preferred geo-replicated region for interacting with Azure Cosmos DB. For more information, see [Distribute your data globally with Azure Cosmos DB](distribute-data-globally.md).

- `ConsistencyLevel`: Use this option to override the default consistency level. For more information, see [Consistency levels in Azure Cosmos DB](consistency-levels.md).

- `BulkExecutionMode`: Use this option to execute bulk operations by setting the `AllowBulkExecution` property to `true`. For more information, see [Bulk import data to an Azure Cosmos DB for NoSQL account by using the .NET SDK](tutorial-dotnet-bulk-import.md).

   ```csharp
   client_cosmosDB = new CosmosClient("Your connection string", new CosmosClientOptions()
       {
           ConnectionMode = ConnectionMode.Direct,
           ApplicationRegion = Regions.EastUS2,
           ConsistencyLevel = ConsistencyLevel.Session,
           AllowBulkExecution = true,
       });
   ```

### Create the container

#### DynamoDB

To store the data in Amazon DynamoDB, you need to create the table first. Define the schema, key type, and attributes, as shown in the following code:

```csharp
// movies_key_schema
public static List<KeySchemaElement> moviesKeySchema =
    new List<KeySchemaElement>
    {
        new KeySchemaElement
        {
            AttributeName = partitionKeyName,
            KeyType = "HASH"
        },
        new KeySchemaElement
        {
            AttributeName = sortKeyName,
            KeyType = "RANGE"
        },
    };

// key names for the Movies table
public const string partitionKeyName = "year";
public const string sortKeyName = "title";
public const int readUnits = 1, writeUnits = 1;

// movie_items_attributes
public static List<AttributeDefinition> movieItemsAttributes =
    new List<AttributeDefinition>
    {
        new AttributeDefinition
        {
            AttributeName = partitionKeyName,
            AttributeType = "N"
        },
        new AttributeDefinition
        {
            AttributeName = sortKeyName,
            AttributeType = "S"
        }
    };

CreateTableRequest request;
CreateTableResponse response;

// Build the 'CreateTableRequest' structure for the new table
request = new CreateTableRequest
{
    TableName             = tableName,
    AttributeDefinitions  = tableAttributes,
    KeySchema             = tableKeySchema,
    // Provisioned-throughput settings are always required,
    // although the local test version of DynamoDB ignores them.
    ProvisionedThroughput = new ProvisionedThroughput(readUnits, writeUnits)
};
```

#### Azure Cosmos DB

In Amazon DynamoDB, you need to provision the read compute units and the write compute units. In Azure Cosmos DB, you specify the throughput as [request units per second (RU/s)](request-units.md). You can use RU/s for any operations dynamically. The data is organized as database, container, and then item. You can specify the throughput at the database level, at the collection level, or both.

To create a database:

```csharp
await client_cosmosDB.CreateDatabaseIfNotExistsAsync(movies_table_name);
```

To create a container:

```csharp
await cosmosDatabase.CreateContainerIfNotExistsAsync(new ContainerProperties()
    {
        PartitionKeyPath = "/" + partitionKey,
        Id = newCollectionName
    },
    provisionedThroughput);
```

### Load the data

#### DynamoDB

The following code shows how to load the data in Amazon DynamoDB. The `moviesArray` code lists JSON documents, and then you need to iterate through and load the JSON documents into Amazon DynamoDB.

```csharp
int n = moviesArray.Count;
for (int i = 0, j = 99; i < n; i++)
{
    try
    {
        string itemJson = moviesArray[i].ToString();
        Document doc = Document.FromJson(itemJson);
        Task putItem = moviesTable.PutItemAsync(doc);
        if (i >= j)
        {
          j++;
          Console.Write("{0,5:#,##0}, ", j);
          if (j % 1000 == 0)
              Console.Write("\n ");
          j += 99;
        }
        await putItem;
    }
    catch { }
}
```

#### Azure Cosmos DB

In Azure Cosmos DB, you can opt to stream and write by using `moviesContainer.CreateItemStreamAsync()`. However, in this example, the JSON is deserialized into the `MovieModel` type to demonstrate the type-casting feature. The code is multithreaded and uses the distributed architecture in Azure Cosmos DB to speed up the loading.

```csharp
List<Task> concurrentTasks = new List<Task>();
for (int i = 0, j = 99; i < n; i++)
{
  try
  {
      MovieModel doc = JsonConvert.DeserializeObject<MovieModel>(moviesArray[i].ToString());
      doc.Id = Guid.NewGuid().ToString();
      concurrentTasks.Add(moviesContainer.CreateItemAsync(doc,new PartitionKey(doc.Year)));
      if (i >= j)
      {
          j++;
          Console.Write("{0,5:#,##0}, ", j);
          if (j % 1000 == 0)
              Console.Write("\n               ");
          j += 99;
      }
  }
  catch (Exception ex)
  {
      Console.WriteLine("\n     ERROR: Could not write the movie record #{0:#,##0}, because:\n       {1}",
                          i, ex.Message);
      operationFailed = true;
      break;
  }
}
await Task.WhenAll(concurrentTasks);
```

### Create a document

#### DynamoDB

Writing a new document in Amazon DynamoDB isn't type safe. The following example uses `newItem` as the document type:

```csharp
Document writeNew = await moviesTable.PutItemAsync(newItem, token);
```

#### Azure Cosmos DB

Azure Cosmos DB provides type safety via a data model. This example uses a data model named `MovieModel`:

```csharp
public class MovieModel
{
    [JsonProperty("id")]
    public string Id { get; set; }
    [JsonProperty("title")]
    public string Title{ get; set; }
    [JsonProperty("year")]
    public int Year { get; set; }
    [JsonProperty("info")]
    public MovieInfo MovieInfo { get; set; }

    public MovieModel(string title, int year)
    {
        this.Title = title;
        this.Year = year;
    }
    public MovieModel() { }

    internal string PrintInfo()
    {
        if (this.MovieInfo != null)
            return string.Format(
                "\nMovie with title:{1}\n Year: {2}, Actors: {3}\n Directors:{4}\n Rating:{5}\n",
                this.Id,
                this.Title,
                this.Year,
                String.Join(",",this.MovieInfo.Actors),
                this.MovieInfo,
                this.MovieInfo.Rating);
        else
            return string.Format(
                "\nMovie with  title:{0}\n Year: {1}\n",
                this.Title,
                this.Year);
    }
}
```

In Azure Cosmos DB, `newItem` is `MovieModel`:

```csharp
MovieModel movieModel = new MovieModel
{
    Id = Guid.NewGuid().ToString(),
    Title = "The Big New Movie",
    Year = 2018,
    MovieInfo = new MovieInfo() { Plot = "Nothing happens at all.", Rating = 0 }
};
await moviesContainer.CreateItemAsync(movieModel, new Microsoft.Azure.Cosmos.PartitionKey(movieModel.Year));
```

### Read a document

#### DynamoDB

To read in Amazon DynamoDB, you need to define primitives:

```csharp
// Create primitives for the HASH and RANGE portions of the primary key
Primitive hash = new Primitive(year.ToString(), true);
Primitive range = new Primitive(title, false);

Document movieRecord = await moviesTable.GetItemAsync(hash, range, token);
```

#### Azure Cosmos DB

With Azure Cosmos DB, the query is natural (LINQ):

```csharp
IQueryable<MovieModel> movieQuery = moviesContainer.GetItemLinqQueryable<MovieModel>(true)
                        .Where(f => f.Year == year && f.Title == title);
// The query is executed synchronously here, but can also be executed asynchronously via the IDocumentQuery<T> interface
foreach (MovieModel movie in movieQuery)
{
    movie_record_cosmosdb = movie;
}
```

The document collection in the preceding example is type safe and provides a natural query option.

### Update an item

#### DynamoDB

To update an item in Amazon DynamoDB:

```csharp
updateResponse = await client.UpdateItemAsync(updateRequest);
```

#### Azure Cosmos DB

In Azure Cosmos DB, an update is treated as `Upsert` operation (that is, insert the document if it doesn't exist):

```csharp
await moviesContainer.UpsertItemAsync<MovieModel>(updatedMovieModel);
```

### Delete a document

#### DynamoDB

To delete an item in Amazon DynamoDB, you again need to fall on primitives:

```csharp
Primitive hash = new Primitive(year.ToString(), true);
Primitive range = new Primitive(title, false);
DeleteItemOperationConfig deleteConfig = new DeleteItemOperationConfig();
deleteConfig.ConditionalExpression = condition;
deleteConfig.ReturnValues = ReturnValues.AllOldAttributes;
  
Document deletedItem = await table.DeleteItemAsync(hash, range, deleteConfig);
```

#### Azure Cosmos DB

In Azure Cosmos DB, you can get the document and delete it asynchronously:

```csharp
var result = ReadingMovieItem_async_List_CosmosDB("SELECT * FROM c WHERE c.info.rating > 7 AND c.year = 2018 AND c.title = 'The Big New Movie'");
while (result.HasMoreResults)
{
    var resultModel = await result.ReadNextAsync();
    foreach (var movie in resultModel.ToList<MovieModel>())
    {
        await moviesContainer.DeleteItemAsync<MovieModel>(movie.Id, new PartitionKey(movie.Year));
    }
}
```

### Query documents

#### DynamoDB

In Amazon DynamoDB, API functions are required to query the data:

```csharp
QueryOperationConfig config = new QueryOperationConfig();
config.Filter = new QueryFilter();
config.Filter.AddCondition("year", QueryOperator.Equal, new DynamoDBEntry[ ] { 1992 });
config.Filter.AddCondition("title", QueryOperator.Between, new DynamoDBEntry[ ] { "B", "Hzz" });
config.AttributesToGet = new List<string> { "year", "title", "info" };
config.Select = SelectValues.SpecificAttributes;
search = moviesTable.Query(config);
```

#### Azure Cosmos DB

In Azure Cosmos DB, you can do projection and filter inside a simple SQL query:

```csharp
var result = moviesContainer.GetItemQueryIterator<MovieModel>( 
  "SELECT c.Year, c.Title, c.info FROM c WHERE Year = 1998 AND (CONTAINS(Title, 'B') OR CONTAINS(Title, 'Hzz'))");
```

For range operations (for example, `between`), you need to do a scan in Amazon DynamoDB:

```csharp
ScanRequest sRequest = new ScanRequest
{
    TableName = "Movies",
    ExpressionAttributeNames = new Dictionary<string, string>
    {
        { "#yr", "year" }
    },
    ExpressionAttributeValues = new Dictionary<string, AttributeValue>
    {
        { ":y_a", new AttributeValue { N = "1960" } },
        { ":y_z", new AttributeValue { N = "1969" } },
    },
    FilterExpression = "#yr between :y_a and :y_z",
    ProjectionExpression = "#yr, title, info.actors[0], info.directors, info.running_time_secs"
};

ClientScanning_async(sRequest).Wait();
```

In Azure Cosmos DB, you can use a SQL query and a single-line statement:

```csharp
var result = moviesContainer.GetItemQueryIterator<MovieModel>(
    "SELECT c.title, c.info.actors[0], c.info.directors, c.info.running_time_secs FROM c WHERE c.year BETWEEN 1960 AND 1969");
```

### Delete a container

#### DynamoDB

To delete the table in Amazon DynamoDB, you can specify:

```csharp
await client.DeleteTableAsync(tableName);
```

#### Azure Cosmos DB

To delete the collection in Azure Cosmos DB, you can specify:

```csharp
await moviesContainer.DeleteContainerAsync();
```

Then delete the database too, if necessary:

```csharp
await cosmosDatabase.DeleteAsync();
```

## Summary

As the preceding examples show, Azure Cosmos DB supports natural queries (SQL), and  operations are asynchronous. You can easily migrate your complex code to Azure Cosmos DB. The code becomes simpler after the migration.

### Related content

- Learn about [performance optimization](performance-tips.md).
- Learn how to [optimize reads and writes](key-value-store-cost.md).
- Learn about [monitoring in Azure Cosmos DB](monitor.md).
