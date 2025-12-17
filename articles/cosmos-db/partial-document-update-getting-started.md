---
title: Get Started with Partial Document Update
description: Learn how to use the partial document update feature in Azure Cosmos DB for NoSQL.
author: AbhinavTrips
ms.author: abtripathi
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: how-to
ms.custom: devx-track-dotnet, devx-track-extended-java
ms.date: 07/22/2025
appliesto:
  - ✅ NoSQL
---

# Get started with Azure Cosmos DB partial document update

This article provides examples that illustrate how to use *partial document update* with .NET, Java, and Node SDKs. It also describes common errors that you might encounter.

This article links to code samples for the following scenarios:

- Run a single patch operation
- Combine multiple patch operations
- Use conditional patch syntax based on filter predicate
- Run patch operation as part of a transaction

## Prerequisites

- An existing Azure Cosmos DB account.
  - If you have an Azure subscription, [create a new account](how-to-create-account.md?tabs=azure-portal).
  - If you don't have an Azure subscription, create a [free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) before you begin.

## Use partial document update

## [.NET](#tab/dotnet)

Support for partial document update (Patch API) in the [Azure Cosmos DB .NET v3 SDK](sdk-dotnet-v3.md) is available in version *3.23.0* and later. You can download the package from the [NuGet gallery](https://www.nuget.org/packages/Microsoft.Azure.Cosmos/3.23.0).

> [!NOTE]
> Find a complete partial document update sample in the [.NET v3 samples repository](https://github.com/Azure/azure-cosmos-dotnet-v3/blob/master/Microsoft.Azure.Cosmos.Samples/Usage/ItemManagement/Program.cs) on GitHub.

- Run a single patch operation:

    ```csharp
    ItemResponse<Product> response = await container.PatchItemAsync<Product>(
        id: "e4e4e4e4-ffff-aaaa-bbbb-c5c5c5c5c5c5",
        partitionKey: new PartitionKey("road-bikes"),
        patchOperations: new[] {
            PatchOperation.Replace("/price", 355.45)
        }
    );
    
    Product updated = response.Resource;
    ```

- Combine multiple patch operations:

    ```csharp
    List<PatchOperation> operations = new ()
    {
        PatchOperation.Add("/color", "silver"),
        PatchOperation.Remove("/used"),
        PatchOperation.Increment("/price", 50.00),
        PatchOperation.Add("/tags/-", "featured-bikes")
    };
    
    ItemResponse<Product> response = await container.PatchItemAsync<Product>(
        id: "e4e4e4e4-ffff-aaaa-bbbb-c5c5c5c5c5c5",
        partitionKey: new PartitionKey("road-bikes"),
        patchOperations: operations
    );
    ```

- Use conditional patch syntax based on filter predicate:

    ```csharp
    PatchItemRequestOptions options = new()
    {
        FilterPredicate = "FROM products p WHERE p.used = false"
    };
    
    List<PatchOperation> operations = new ()
    {
        PatchOperation.Replace($"/price", 100.00),
    };
    
    ItemResponse<Product> response = await container.PatchItemAsync<Product>(
        id: "e4e4e4e4-ffff-aaaa-bbbb-c5c5c5c5c5c5",
        partitionKey: new PartitionKey("road-bikes"),
        patchOperations: operations,
        requestOptions: options
    );
    ```

- Run patch operation as a part of a transaction:

    ```csharp
    TransactionalBatchPatchItemRequestOptions options = new()
    {
        FilterPredicate = "FROM products p WHERE p.used = false"
    };
    
    List<PatchOperation> operations = new ()
    {
        PatchOperation.Add($"/new", true),
        PatchOperation.Remove($"/used")
    };
    
    TransactionalBatch batch = container.CreateTransactionalBatch(
        partitionKey: new PartitionKey("road-bikes")
    );
    batch.PatchItem(
        id: "e4e4e4e4-ffff-aaaa-bbbb-c5c5c5c5c5c5",
        patchOperations: operations,
        requestOptions: options
    );
    batch.PatchItem(
        id: "f5f5f5f5-aaaa-bbbb-cccc-d6d6d6d6d6d6",
        patchOperations: operations,
        requestOptions: options
    );
    
    TransactionalBatchResponse response = await batch.ExecuteAsync();
    bool success = response.IsSuccessStatusCode;
    ```

## [Java](#tab/java)

Support for partial document update (Patch API) in the [Azure Cosmos DB Java v4 SDK](sdk-java-v4.md) is available in version *4.21.0* and later. You can either add it to the list of dependencies in your `pom.xml` or download it directly from [Maven](https://mvnrepository.com/artifact/com.azure/azure-cosmos).

```xml
<dependency>
  <groupId>com.azure</groupId>
  <artifactId>azure-cosmos</artifactId>
  <version>LATEST</version>
</dependency>
```

> [!NOTE]
> Find the full sample in the [Java SDK v4 samples repository](https://github.com/Azure-Samples/azure-cosmos-java-sql-api-samples/tree/main/src/main/java/com/azure/cosmos/examples/patch/sync) on GitHub.

- Run a single patch operation:

    ```java
    CosmosItemResponse<Product> response = container.patchItem(
        "e4e4e4e4-ffff-aaaa-bbbb-c5c5c5c5c5c5",
        new PartitionKey("road-bikes"),
        CosmosPatchOperations
            .create()
            .replace("/price", 355.45),
        Product.class
    );

    Product updated = response.getItem();
    ```

- Combine multiple patch operations:

    ```java
    CosmosPatchOperations operations = CosmosPatchOperations
        .create()
        .add("/color", "silver")
        .remove("/used")
        .increment("/price", 50);

    CosmosItemResponse<Product> response = container.patchItem(
        "e4e4e4e4-ffff-aaaa-bbbb-c5c5c5c5c5c5",
        new PartitionKey("road-bikes"),
        operations,
        Product.class
    );
    ```

- Use conditional patch syntax based on filter predicate:

    ```java
    CosmosPatchItemRequestOptions options = new CosmosPatchItemRequestOptions();
    options.setFilterPredicate("FROM products p WHERE p.used = false");

    CosmosPatchOperations operations = CosmosPatchOperations
        .create()
        .replace("/price", 100.00);

    CosmosItemResponse<Product> response = container.patchItem(
        "e4e4e4e4-ffff-aaaa-bbbb-c5c5c5c5c5c5",
        new PartitionKey("road-bikes"),
        operations,
        options,
        Product.class
    );
    ```

- Run patch operation as a part of a transaction:

    ```java
    CosmosBatchPatchItemRequestOptions options = new CosmosBatchPatchItemRequestOptions();
    options.setFilterPredicate("FROM products p WHERE p.used = false");

    CosmosPatchOperations operations = CosmosPatchOperations
        .create()
        .add("/new", true)
        .remove("/used");

    CosmosBatch batch = CosmosBatch.createCosmosBatch(
        new PartitionKey("road-bikes")
    );
    batch.patchItemOperation(
        "e4e4e4e4-ffff-aaaa-bbbb-c5c5c5c5c5c5",
        operations,
        options
    );
    batch.patchItemOperation(
        "f5f5f5f5-aaaa-bbbb-cccc-d6d6d6d6d6d6",
        operations,
        options
    );

    CosmosBatchResponse response = container.executeCosmosBatch(batch);
    boolean success = response.isSuccessStatusCode();
    ```

## [Node.js](#tab/nodejs)

Support for partial document update (Patch API) in the [Azure Cosmos DB JavaScript SDK](sdk-nodejs.md) is available in version *3.15.0* and later. You can download it from the [npm Registry](https://www.npmjs.com/package/@azure/cosmos).

> [!NOTE]
> Find a complete partial document update sample in the [.js v3 samples repository](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/cosmosdb/cosmos/samples/v3/typescript/src/ItemManagement.ts#L167) on GitHub. In the sample, as the container is created without a partition key specified, the JavaScript SDK resolves the partition key values from the items through the container's partition key definition.

- Run a single patch operation:

    ```javascript
    const operations =
    [
        { op: 'replace', path: '/price', value: 355.45 }
    ];
    
    const { resource: updated } = await container
        .item(
            'e4e4e4e4-ffff-aaaa-bbbb-c5c5c5c5c5c5', 
            'road-bikes'
        )
        .patch(operations);
    ```

- Combine multiple patch operations:

    ```javascript
    const operations =
    [
        { op: 'add', path: '/color', value: 'silver' },
        { op: 'remove', path: '/used' }
    ];
    
    const { resource: updated } = await container
        .item(
            'e4e4e4e4-ffff-aaaa-bbbb-c5c5c5c5c5c5', 
            'road-bikes'
        )
        .patch(operations);
    ```

## [Python (Preview)](#tab/python)

Support for partial document update (Patch API) in the [Azure Cosmos DB Python SDK](sdk-python.md) is available from version *4.4.0b2*. You can download it from the [pip registry](https://pypi.org/project/azure-cosmos/4.4.0b2/).

> [!NOTE]
> Find a complete partial document update sample in the [python samples repository](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/cosmos/azure-cosmos/samples/document_management.py#L105C8-L122) on GitHub. 

- Run a single patch operation:

    ```python
    operations =
    [
        { 'op': 'replace', 'path': '/price', 'value': 355.45 }
    ]
    
    response = container.patch_item(item='e4e4e4e4-ffff-aaaa-bbbb-c5c5c5c5c5c5', partition_key='road-bikes', patch_operations=operations)
    
    ```

- Combine multiple patch operations:

    ```python
    operations =
    [
        { 'op': 'add', 'path': '/color', 'value': 'silver' },
        { 'op': 'remove', 'path': '/used' }
    ]
    
    response = container.patch_item(item='e4e4e4e4-ffff-aaaa-bbbb-c5c5c5c5c5c5', partition_key='road-bikes', patch_operations=operations)

    ```

- Use conditional patch syntax based on filter predicate:

    ```python
    filter = "from products p WHERE p.used = false"

    operations =
    [
        { 'op': 'replace', 'path': '/price', 'value': 100.00 }
    ]

    try:
        container.patch_item(item='e4e4e4e4-ffff-aaaa-bbbb-c5c5c5c5c5c5', partition_key='road-bikes', patch_operations=operations, filter_predicate=filter)
    except exceptions.CosmosHttpResponseError as e:
        print('\nError occurred. {0}'.format(e.message))
    
    ```

## [Go](#tab/go)

- Run a single patch operation:

    ```go
	pk := azcosmos.NewPartitionKeyString("road-bikes")
	id := "e4e4e4e4-ffff-aaaa-bbbb-c5c5c5c5c5c5"

	patchOp := azcosmos.PatchOperations{}
	patchOp.AppendReplace("/price", 100.00)

	_, err := container.PatchItem(context.Background(), pk, id, patchOp, nil)
    ```

- Combine multiple patch operations:

    ```go
    pk := azcosmos.NewPartitionKeyString("road-bikes")
	id := "e4e4e4e4-ffff-aaaa-bbbb-c5c5c5c5c5c5"
	
    patchOp := azcosmos.PatchOperations{}
	patchOp.AppendAdd("/color", "silver")
	patchOp.AppendRemove("/used")
	patchOp.AppendIncrement("/price", 50)

	_, err := container.PatchItem(context.Background(), pk, id, patchOp, nil)
    ```

- Run patch operation as a part of a transaction:

    ```go
    patchOp := azcosmos.PatchOperations{}
	patchOp.AppendAdd("/new", true)
	patchOp.AppendRemove("/used")

	batch := container.NewTransactionalBatch(pk)
	batch.PatchItem("e4e4e4e4-ffff-aaaa-bbbb-c5c5c5c5c5c5", patchOp, nil)
	batch.PatchItem("f5f5f5f5-aaaa-bbbb-cccc-d6d6d6d6d6d6", patchOp, nil)

	resp, err := container.ExecuteTransactionalBatch(context.Background(), batch, nil)
	if err != nil {
		log.Fatal(err)
	}

	if resp.Success {
        // Handle success
    }
    ```

---

## Support for server-side programming

Partial document update operations can also be [executed on the server-side](stored-procedures-triggers-udfs.md) by using stored procedures, triggers, and user-defined functions.

```javascript
this.patchDocument = function (documentLink, patchSpec, options, callback) {
    if (arguments.length < 2) {
        throw new Error(ErrorCodes.BadRequest, sprintf(errorMessages.invalidFunctionCall, 'patchDocument', 2, arguments.length));
    }
    if (patchSpec === null || !(typeof patchSpec === "object" || Array.isArray(patchSpec))) {
        throw new Error(ErrorCodes.BadRequest, errorMessages.patchSpecMustBeObjectOrArray);
    }

    var documentIdTuple = validateDocumentLink(documentLink, false);
    var collectionRid = documentIdTuple.collId;
    var documentResourceIdentifier = documentIdTuple.docId;
    var isNameRouted = documentIdTuple.isNameRouted;

    patchSpec = JSON.stringify(patchSpec);
    var optionsCallbackTuple = validateOptionsAndCallback(options, callback);

    options = optionsCallbackTuple.options;
    callback = optionsCallbackTuple.callback;

    var etag = options.etag || '';
    var indexAction = options.indexAction || '';

    return collectionObjRaw.patch(
        collectionRid,
        documentResourceIdentifier,
        isNameRouted,
        patchSpec,
        etag,
        indexAction,
        function (err, response) {
            if (callback) {
                if (err) {
                    callback(err);
                } else {
                    callback(undefined, JSON.parse(response.body), response.options);
                }
            } else {
                if (err) {
                    throw err;
                }
            }
        }
    );
}; 
```

> [!NOTE]
> Find the definition of `validateOptionsAndCallback` in the [.js DocDbWrapperScript](https://github.com/Azure/azure-cosmosdb-js-server/blob/1dbe69893d09a5da29328c14ec087ef168038009/utils/DocDbWrapperScript.js#L289) on GitHub.

Sample stored procedure for patch operation:

```javascript
function patchDemo() {
    var doc = {
        "id": "exampleDoc",
        "fields": {
            "field1": "exampleString",
            "field2": 20,
            "field3": 40
        }
    };
    
    var isAccepted = __.createDocument(__.getSelfLink(), doc, (err, doc) => {
        if (err) {
            throw err;
        }
        else {
            getContext().getResponse().setBody("Example document successfully created.");
            
            var patchSpec = [
                { "op": "add", "path": "/fields/field1", "value": "newExampleString" },
                { "op": "remove", "path": "/fields/field2" },
                { "op": "incr", "path": "/fields/field3", "value": 10 }
            ];
            
            var isAccepted = __.patchDocument(doc._self, patchSpec, (err, doc) => {
                if (err) {
                    throw err;
                }
                else {
                    getContext().getResponse().appendBody(" Example document successfully patched.");
                }
            });
            
            if (!isAccepted) throw new Error("Patch wasn't accepted");
        }
    });

    if (!isAccepted) throw new Error("Create wasn't accepted.");
}
```

## Troubleshooting

Here are some common errors that you might encounter while using this feature:

| **Error message** | **Description** |
| ------------ | -------- |
| Invalid patch request: check syntax of patch specification. | The patch operation syntax is invalid. To learn more, see the [specification](partial-document-update.md#rest-api-reference-for-partial-document-update). |
| Invalid patch request: Can't patch system property `SYSTEM_PROPERTY`. | System-generated properties like `_id`, `_ts`, `_etag`, `_rid` aren't modifiable using a patch operation. To learn more, see the [partial document update FAQ](partial-document-update-faq.yml#is-partial-document-update-supported-for-system-generated-properties-). |
| The number of patch operations can't exceed 10. | There's a limit of 10 patch operations that can be added in a single patch specification. To learn more, see the [partial document update FAQ](partial-document-update-faq.yml#is-there-a-limit-to-the-number-of-partial-document-update-operations-). |
| For Operation(`PATCH_OPERATION_INDEX`): Index(`ARRAY_INDEX`) to operate on is out of array bounds. | The index of array element to be patched is out of bounds. |
| For Operation(`PATCH_OPERATION_INDEX`)): Node(`PATH`) to be replaced was removed earlier in the transaction. | The path you're trying to patch doesn't exist. |
| For Operation(`PATCH_OPERATION_INDEX`): Node(`PATH`) to be removed is absent. Note: it might also have been removed earlier in the transaction. | The path you're trying to patch doesn't exist. |
| For Operation(`PATCH_OPERATION_INDEX`): Node(`PATH`) to be replaced is absent. | The path you're trying to patch doesn't exist. |
| For Operation(`PATCH_OPERATION_INDEX`): Node(`PATH`) isn't a number. | Increment operation can only work on integer and float. For more information, see [Supported operations](partial-document-update.md#supported-operations). |
| For Operation(`PATCH_OPERATION_INDEX`): Add operation can only create a child object of an existing node (array or object) and can't create path recursively, no path found beyond: `PATH`. | Child paths can be added to an object or array node type. Also, to create `n`th child, `n-1`th child should be present. |
| For Operation(`PATCH_OPERATION_INDEX`): Given operation can only create a child object of an existing node(array or object) and can't create path recursively, no path found beyond: `PATH`. | Child paths can be added to an object or array node type. Also, to create `n`th child, `n-1`th child should be present. |

## Next step

- [Frequently asked questions about partial document update](partial-document-update-faq.yml)
