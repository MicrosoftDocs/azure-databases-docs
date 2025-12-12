---
title: Configure and Manage Time to Live
description: Learn how to configure and manage time to live on a container and an item in Azure Cosmos DB.
author: markjbrown
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: how-to
ms.date: 12/05/2025
ms.author: mjbrown
ms.custom: devx-track-csharp, devx-track-azurecli, devx-track-azurepowershell
---

# Configure time to live in Azure Cosmos DB
[!INCLUDE[NoSQL](../includes/appliesto-nosql.md)]

In Azure Cosmos DB, you can choose to configure time to live (TTL) at the container level, or you can override it at an item level after setting TTL for the container. You can configure TTL for a container by using the Azure portal or the language-specific SDKs. Item-level TTL overrides can be configured by using the SDKs.

<a id="enable-time-to-live-on-a-container-using-the-azure-portal"></a>

## Enable TTL on a container by using the Azure portal

Use the following steps to enable TTL on a container with no expiration. Enabling TTL at the container level allows the same value to be overridden at an individual item's level. You can also set the TTL by entering a nonzero value for seconds.

1. Sign in to the [Azure portal](https://portal.azure.com).

1. Create a new Azure Cosmos DB account or select an existing account.

1. Open the **Data Explorer** pane.

1. Select an existing container, expand the **Settings** tab, and modify the following values:

   1. Under **Settings**, find **Time to Live**.
   1. Based on your requirement, you can:
     * Turn **off** this setting.
     * Set it to **On (no default)**.
     * Turn **On** with a TTL value specified in seconds.

   1. Select **Save** to save the changes.

   :::image type="content" source="./media/how-to-time-to-live/how-to-time-to-live-portal.png" alt-text="Screenshot of the settings to configure Time to live in the Azure portal." lightbox="./media/how-to-time-to-live/how-to-time-to-live-portal.png":::

* When **DefaultTimeToLive** is null, then your TTL is *Off*.
* When **DefaultTimeToLive** is *-1* then, your TTL setting is *On* (No default).
* When **DefaultTimeToLive** has any other integer value (except 0), then your TTL setting is *On*. The server automatically deletes items based on the configured value.

## Enable TTL on a container by using Azure CLI or Azure PowerShell

To create or enable TTL on a container, see:

* [Create a container with TTL by using Azure CLI](manage-with-cli.md#create-a-container-with-ttl)
* [Create a container with TTL by using PowerShell](manage-with-powershell.md#create-container-unique-key-ttl)

## Enable TTL on a container by using an SDK

### [.NET SDK v3](#tab/dotnet-sdk-v3)

```csharp
Database database = client.GetDatabase("database");

ContainerProperties properties = new ()
{
    Id = "container",
    PartitionKeyPath = "/customerId",
    // Never expire by default
    DefaultTimeToLive = -1
};

// Create a new container with TTL enabled and without any expiration value
Container container = await database
    .CreateContainerAsync(properties);
```

### [Java SDK v4](#tab/javav4)

```java
CosmosDatabase database = client.getDatabase("database");

CosmosContainerProperties properties = new CosmosContainerProperties(
    "container",
    "/customerId"
);
// Never expire by default
properties.setDefaultTimeToLiveInSeconds(-1);

// Create a new container with TTL enabled and without any expiration value
CosmosContainerResponse response = database
    .createContainerIfNotExists(properties);
```

### [Node SDK](#tab/node-sdk)

```javascript
const database = await client.database("database");

const properties = {
    id: "container",
    partitionKey: "/customerId",
    // Never expire by default
    defaultTtl: -1
};

const { container } = await database.containers
    .createIfNotExists(properties);

```

### [Python SDK](#tab/python-sdk)

```python
database = client.get_database_client('database')

database.create_container(
    id='container',
    partition_key=PartitionKey(path='/customerId'),
    # Never expire by default
    default_ttl=-1
)
```

### [Go SDK](#tab/go)

```go
db, _ := c.NewDatabase("demo_db")

pkDefinition := azcosmos.PartitionKeyDefinition{
	Paths: []string{"/state"},
	Kind:  azcosmos.PartitionKeyKindHash,
}

// Never expire by default
ttl := int32(-1)

db.CreateContainer(context.Background(), azcosmos.ContainerProperties{
	ID:                     "demo_container",
	PartitionKeyDefinition: pkDefinition,
	DefaultTimeToLive:      &ttl,
}, nil)
```

---

## Set TTL on a container by using an SDK

To set the TTL on a container, you need to provide a nonzero positive number that indicates the time period in seconds. Based on the configured TTL value, all items in the container after the last modified timestamp of the item `_ts` are deleted.

### [.NET SDK v3](#tab/dotnet-sdk-v3)

```csharp
Database database = client.GetDatabase("database");

ContainerProperties properties = new ()
{
    Id = "container",
    PartitionKeyPath = "/customerId",
    // Expire all documents after 90 days
    DefaultTimeToLive = 90 * 60 * 60 * 24
};

// Create a new container with TTL enabled and without any expiration value
Container container = await database
    .CreateContainerAsync(properties);
```

### [Java SDK v4](#tab/javav4)

```java
CosmosDatabase database = client.getDatabase("database");

CosmosContainerProperties properties = new CosmosContainerProperties(
    "container",
    "/customerId"
);
// Expire all documents after 90 days
properties.setDefaultTimeToLiveInSeconds(90 * 60 * 60 * 24);

CosmosContainerResponse response = database
    .createContainerIfNotExists(properties);
```

### [Node SDK](#tab/node-sdk)

```javascript
const database = await client.database("database");

const properties = {
    id: "container",
    partitionKey: "/customerId",
    // Expire all documents after 90 days
    defaultTtl: 90 * 60 * 60 * 24
};

const { container } = await database.containers
    .createIfNotExists(properties);
```

### [Python SDK](#tab/python-sdk)

```python
database = client.get_database_client('database')

database.create_container(
    id='container',
    partition_key=PartitionKey(path='/customerId'),
    # Expire all documents after 90 days
    default_ttl=90 * 60 * 60 * 24
)
```

### [Go SDK](#tab/go)

```go
db, _ := c.NewDatabase("demo_db")

// Expire all documents after 90 days
ttl := int32(90 * 24 * 60 * 60)

db.CreateContainer(context.Background(), azcosmos.ContainerProperties{
	ID:                     containerName,
	PartitionKeyDefinition: pkDefinition,
	DefaultTimeToLive:      &ttl,
}, nil)
```

---

## Set TTL on an item by using the Azure portal

In addition to setting a default TTL on a container, you can set a TTL for an item. Setting TTL at the item level overrides the default TTL of the item in that container.

* To set the TTL on an item, you need to provide a nonzero positive number, which indicates the period, in seconds, to expire the item after the last modified timestamp of the item `_ts`. You can provide a `-1` as well when the item shouldn't expire.

* If the item doesn't have a TTL field, then by default, the TTL set to the container applies to the item.

* If TTL is disabled at the container level, the TTL field on the item is ignored until TTL is re-enabled on the container.

Use the following steps to enable TTL on an item:

1. Sign in to the [Azure portal](https://portal.azure.com).

1. Create a new Azure Cosmos DB account or select an existing account.

1. Open the **Data Explorer** pane.

1. Select an existing container, expand it, and modify the following values:

    * Open the **Scale & Settings** window.
    * Under **Setting**, find **Time to Live**.
    * Select **On (no default)** or select **On** and set a TTL value.
    * Select **Save** to save the changes.

1. Navigate to the item for which you want to set time to live, add the `ttl` property, and select **Update**. 

    ```json
    {
        "id": "1",
        "_rid": "Jic9ANWdO-EFAAAAAAAAAA==",
        "_self": "dbs/Jic9AA==/colls/Jic9ANWdO-E=/docs/Jic9ANWdO-EFAAAAAAAAAA==/",
        "_etag": "\"0d00b23f-0000-0000-0000-5c7712e80000\"",
        "_attachments": "attachments/",
        "ttl": 10,
        "_ts": 1551307496
    }
    ```

## Set TTL on an item by using an SDK

### [.NET SDK v3](#tab/dotnet-sdk-v3)

```csharp
public record SalesOrder(string id, string customerId, int ttl);
```

```csharp
Container container = database.GetContainer("container");

SalesOrder item = new (
    "SO05", 
    "CO18009186470"
    // Expire sales order in 30 days using "ttl" property
    ttl:  60 * 60 * 24 * 30
);

await container.CreateItemAsync<SalesOrder>(item);
```

### [Java SDK v4](#tab/javav4)

```java
public class SalesOrder {

    public String id;

    public String customerId;

    // Include a property that serializes to "ttl" in JSON
    public Integer ttl;

}
```

```java
CosmosContainer container = database.getContainer("container");

SalesOrder item = new SalesOrder();
item.id = "SO05";
item.customerId = "CO18009186470";
// Expire sales order in 30 days using "ttl" property
item.ttl = 60 * 60 * 24 * 30;

container.createItem(item);
```

### [Node SDK](#tab/node-sdk)

```javascript
const container = await database.container("container");

const item = {
    id: 'SO05',
    customerId: 'CO18009186470',
    // Expire sales order in 30 days using "ttl" property
    ttl: 60 * 60 * 24 * 30
};

await container.items.create(item);
```

### [Python SDK](#tab/python-sdk)

```python
container = database.get_container_client('container')

item = {
    'id': 'SO05',
    'customerId': 'CO18009186470',
    # Expire sales order in 30 days using "ttl" property
    'ttl': 60 * 60 * 24 * 30
}

container.create_item(body=item)
```

### [Go SDK](#tab/go)

```go
custInfo := map[string]any{
	"id":    "SO05",
	"customerId": "CO18009186470",
	// Expire sales order in 30 days using "ttl" property
	"ttl": int32(60 * 60 * 24 * 30),
}

container, _ := db.NewContainer(containerName)

item, err := json.Marshal(custInfo)
container.CreateItem(context.Background(), azcosmos.NewPartitionKeyString("CO18009186470"), item, nil)
```

---

## Reset TTL by using an SDK

You can reset the TTL on an item by performing a write or update operation on the item. The write or update operation sets the `_ts` to the current time, and the TTL for the item to expire begins again. If you wish to change the TTL of an item, you can update the field just as you update any other field.

### [.NET SDK v3](#tab/dotnet-sdk-v3)

```csharp
SalesOrder item = await container.ReadItemAsync<SalesOrder>(
    "SO05", 
    new PartitionKey("CO18009186470")
);

// Update ttl to 2 hours
SalesOrder modifiedItem = item with { 
    ttl = 60 * 60 * 2 
};

await container.ReplaceItemAsync<SalesOrder>(
    modifiedItem,
    "SO05", 
    new PartitionKey("CO18009186470")    
);
```

### [Java SDK v4](#tab/javav4)

```java
CosmosItemResponse<SalesOrder> response = container.readItem(
    "SO05", 
    new PartitionKey("CO18009186470"),
    SalesOrder.class
);

SalesOrder item = response.getItem();

// Update ttl to 2 hours
item.ttl = 60 * 60 * 2;

CosmosItemRequestOptions options = new CosmosItemRequestOptions();
container.replaceItem(
    item,
    "SO05", 
    new PartitionKey("CO18009186470"),
    options
);
```

### [Node SDK](#tab/node-sdk)

```javascript
const { resource: item } = await container.item(
    'SO05',
    'CO18009186470'
).read();

// Update ttl to 2 hours
item.ttl = 60 * 60 * 2;

await container.item(
    'SO05',
    'CO18009186470'
).replace(item);
```

### [Python SDK](#tab/python-sdk)

```python
item = container.read_item(
    item='SO05',
    partition_key='CO18009186470'
)

# Update ttl to 2 hours
item['ttl'] = 60 * 60 * 2 

container.replace_item(
    item='SO05',
    body=item
)
```

### [Go SDK](#tab/go)

```go
// Read the item
resp, _ := container.ReadItem(context.Background(), azcosmos.NewPartitionKeyString("CO18009186470"), "SO05", nil)

var order map[string]any
json.Unmarshal(resp.Value, &order)

// Update ttl to 2 hours
order["ttl"] = int32(120 * 60)
updatedOrder, err = json.Marshal(order)

container.ReplaceItem(context.Background(), azcosmos.NewPartitionKeyString("CO18009186470"), "SO05", updatedOrder, nil)
```

---

## Disable TTL by using an SDK

To disable TTL on a container and stop the background process from checking for expired items, the `DefaultTimeToLive` property on the container should be deleted. Deleting this property is different from setting it to *-1*. When you set it to *-1*, new items added to the container live forever, however you can override this value on specific items in the container. When you remove the TTL property from the container the items never expire, even if they explicitly override the previous default TTL value.

### [.NET SDK v3](#tab/dotnet-sdk-v3)

```csharp
ContainerProperties properties = await container.ReadContainerAsync();

// Disable ttl at container-level
properties.DefaultTimeToLive = null;

await container.ReplaceContainerAsync(properties);
```

### [Java SDK v4](#tab/javav4)

```java
CosmosContainerResponse response = container.read();
CosmosContainerProperties properties = response.getProperties();

// Disable ttl at container-level
properties.setDefaultTimeToLiveInSeconds(null);

container.replace(properties);
```

### [Node SDK](#tab/node-sdk)

```javascript
const { resource: definition } = await container.read();

// Disable ttl at container-level
definition.defaultTtl = null;

await container.replace(definition);
```

### [Python SDK](#tab/python-sdk)

```python
database.replace_container(
    container,
    partition_key=PartitionKey(path='/id'),
    # Disable ttl at container-level
    default_ttl=None
)
```

### [Go SDK](#tab/go)

```go
containerInfo, _ := container.Read(context.Background(), nil)
props := containerInfo.ContainerProperties

// Disable ttl at container-level
props.DefaultTimeToLive = nil
container.Replace(context.Background(), *props, nil)
```

---

## Related content

* [Time to Live (TTL) in Azure Cosmos DB](time-to-live.md)
