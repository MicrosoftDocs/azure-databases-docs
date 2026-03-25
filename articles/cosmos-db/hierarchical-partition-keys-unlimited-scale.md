---
title: Unlimited logical partition storage with hierarchical partition keys
description: Learn how to use hierarchical partition keys with a unique last level to scale beyond the 20-GB logical partition limit in Azure Cosmos DB.
author: lnajaroen
ms.author: lnajaroen
ms.service: azure-cosmos-db
ms.topic: concept-article
ms.date: 03/24/2026
ai-usage: ai-assisted
appliesto:
  - ✅ NoSQL
---

# Unlimited logical partition storage with hierarchical partition keys in Azure Cosmos DB

This document explains how Hierarchical Partition Keys (HPK) can help you model high-cardinality data and avoid hitting the 20 GB logical partition size limit by using a multi-level partition key path that ends with a unique identifier. 

In Azure Cosmos DB, items are grouped into **logical partitions** based on the value of the partition key. A single logical partition has a **maximum storage size of 20 GB**. See [logical partitions overview](partitioning.md) for more info. If your data model causes too many items to share the same partition key value (for example, all events for a single customer, tenant, device, or account), that logical partition can grow until it reaches the 20-GB limit, at which point writes targeting that partition fail.

You can avoid this limit by using [hierarchical partition keys](hierarchical-partition-keys.md) (HPK) with a unique identifier as the final level. This approach dramatically reduces the chance that any single logical partition grows without bound.

## Recommended pattern

Choose one to three business-grouping levels (such as tenant, customer, or workload) and use a unique final level of `/id`. Azure Cosmos DB uses the combined hierarchy to distribute items.

For example, a multitenant application might use the following hierarchical partition key path:

- `/tenantId`
- `/accountId`
- `/id`

Because each item has a unique `id`, no single logical partition key value accumulates unbounded data. This pattern prevents any one logical partition from reaching the 20-GB limit.

> [!IMPORTANT]
> Adding a unique last level changes how you target point operations and transactional operations. Review the [prerequisites and limitations](#prerequisites-and-limitations) before you adopt this pattern.

## Prerequisites and limitations

Before you adopt an HPK strategy that ends with a unique value of `/id`, make sure the pattern aligns with the transactional semantics your application requires.

### Transactional operations

Operations that require a single, shared partition key value across multiple items aren't compatible with a unique-last-level pattern. The following features are **not supported** when you use this pattern:

- **Transactional batch (atomic batch):** Requires multiple items to share the same partition key value.
- **Stored procedures and triggers:** Rely on grouping multiple items under one partition key value.

If you need these features, consider an HPK design where the last level isn't unique, or use an alternative data model. Validate that your design still avoids exceeding the 20-GB logical partition limit for your workload.

### Application requirements

Your application must be able to provide the full HPK value (all levels) for point reads, updates, deletes, and writes. This requirement is dependent on your SDK version. For more information, see the [supported SDK versions](hierarchical-partition-keys.md#get-started).

## Enablement and behavior

To enforce that any new containers created in an account follow this pattern, enable the `EnforceHierarchicalPartitionKeyIdLastLevel` property for your account.

> [!NOTE]
> The minimum Resource Provider API version required is `2026-03-15`.

After you enable the property, the following behavior applies:

| Behavior | Description |
| --- | --- |
| **No defaulting of `/id`** | Azure Cosmos DB doesn't add `/id` as the last level automatically. You must specify the full HPK path at container creation time with `/id` as the last level. |
| **New container restrictions** | Creating new containers with a non-hierarchical partition key path is blocked on the account. All new containers must use hierarchical partition keys with `/id` as the last level. |
| **Existing containers unchanged** | Enabling this property doesn't retroactively modify existing containers or their partition key configuration. To adopt this pattern for existing containers, create a new container with the desired HPK definition and [migrate your data](container-copy.md). |
| **Support for additional levels** | Support for more than three levels (for example, four levels) depends on enablement and service version. Use only supported levels for your account once enabled. A fourth level is recommended only for rare scenarios where three levels are needed in addition to `/id`. |

## Enable and configure

Enable the `EnforceHierarchicalPartitionKeyIdLastLevel` property for your account, and then create a new container with a hierarchical partition key path that ends with `/id`.

### [Bicep](#tab/bicep)

```bicep
resource cosmosAccount 'Microsoft.DocumentDB/databaseAccounts@2026-03-15' = {
  name: '<account-name>'
  location: '<location>'
  properties: {
    databaseAccountOfferType: 'Standard'
    enableHierarchicalPartitionKeyIdLastLevel: true
  }
}
```

After you enable the property, create a container with a hierarchical partition key path that ends with `/id`:

```bicep
partitionKey: {
  paths: [
    '/tenantId'
    '/accountId'
    '/id'
  ]
  kind: 'MultiHash'
  version: 2
}
```

### [ARM template](#tab/arm-json)

```json
{
  "type": "Microsoft.DocumentDB/databaseAccounts",
  "apiVersion": "2026-03-15",
  "name": "<account-name>",
  "location": "<location>",
  "properties": {
    "databaseAccountOfferType": "Standard",
    "enableHierarchicalPartitionKeyIdLastLevel": true
  }
}
```

After you enable the property, create a container with a hierarchical partition key path that ends with `/id`:

```json
"partitionKey": {
    "paths": [
        "/tenantId",
        "/accountId",
        "/id"
    ],
    "kind": "MultiHash",
    "version": 2
}
```

### [Azure CLI](#tab/azure-cli)

```azurecli
az cosmosdb update \
    --resource-group <resource-group-name> \
    --name <account-name> \
    --enable-hierarchical-partition-key-id-last-level true
```

### [PowerShell](#tab/powershell)

```powershell
Update-AzCosmosDBAccount `
    -ResourceGroupName "<resource-group-name>" `
    -Name "<account-name>" `
    -EnableHierarchicalPartitionKeyIdLastLevel $true
```

### [.NET SDK](#tab/net-v3)

Use the `Azure.ResourceManager.CosmosDB` management SDK to enable the property on your account.

```csharp
using Azure.ResourceManager;
using Azure.ResourceManager.CosmosDB;
using Azure.ResourceManager.CosmosDB.Models;

ArmClient client = new ArmClient(new DefaultAzureCredential());

ResourceIdentifier accountId = CosmosDBAccountResource.CreateResourceIdentifier(
    "<subscription-id>", "<resource-group-name>", "<account-name>");

CosmosDBAccountResource account = client.GetCosmosDBAccountResource(accountId);

CosmosDBAccountPatch patch = new CosmosDBAccountPatch();
patch.EnableHierarchicalPartitionKeyIdLastLevel = true;

await account.UpdateAsync(WaitUntil.Completed, patch);
```

### [Java SDK](#tab/java-v4)

Use the `azure-resourcemanager-cosmos` management SDK to enable the property on your account.

```java
import com.azure.resourcemanager.cosmos.CosmosManager;
import com.azure.resourcemanager.cosmos.models.CosmosDBAccount;

CosmosManager cosmosManager = CosmosManager.authenticate(credential, profile);

CosmosDBAccount account = cosmosManager.databaseAccounts()
    .getByResourceGroup("<resource-group-name>", "<account-name>");

account.update()
    .withEnableHierarchicalPartitionKeyIdLastLevel(true)
    .apply();
```

### [Python SDK](#tab/python)

Use the `azure-mgmt-cosmosdb` management SDK to enable the property on your account.

```python
from azure.identity import DefaultAzureCredential
from azure.mgmt.cosmosdb import CosmosDBManagementClient

credential = DefaultAzureCredential()
client = CosmosDBManagementClient(credential, "<subscription-id>")

account = client.database_accounts.get("<resource-group-name>", "<account-name>")

update_params = {
    "location": account.location,
    "properties": {
        "enable_hierarchical_partition_key_id_last_level": True
    }
}

client.database_accounts.begin_create_or_update(
    "<resource-group-name>", "<account-name>", update_params
).result()
```

---

After you enable the property, create a new container by specifying a hierarchical partition key path that ends with `/id` (for example: `/tenantId`, `/accountId`, `/id`). For more information about creating containers with hierarchical partition keys, see [Create a container by using hierarchical partition keys](hierarchical-partition-keys.md#create-a-container-by-using-hierarchical-partition-keys).

## Frequently asked questions

### Why am I getting errors related to the 20-GB limit?

This typically means a single logical partition (a single partition key value) has accumulated more than 20 GB of data. Switching to HPK and ensuring the final level is unique (for example, `/id`) helps prevent unbounded growth under one value.

### Why does my request fail with "partition key value is missing or does not match"?

With `EnforceHierarchicalPartitionKeyIdLastLevel` enabled, your items must include every partition key property in the hierarchy. For example, if your HPK is `/tenantId`, `/accountId`, `/id`, then each item must have `tenantId`, `accountId`, and `id` properties. The request must supply the matching full partition key value for point reads, updates, and deletes.

### Why can't I create a container with a non-hierarchical partition key?

After you enable `EnforceHierarchicalPartitionKeyIdLastLevel`, you must use hierarchical partition keys for all newly created containers. This restriction doesn't affect existing containers.

### Can I change an existing container to use hierarchical partition keys?

No. Partition key configuration is immutable. To adopt HPK (or to add a unique last level like `/id`), create a new container with the desired HPK definition and [migrate your data by using container copy jobs](container-copy.md).

### Can I still use transactional batch, stored procedures, or triggers?

If your usage depends on grouping multiple items under a single shared partition key value, a unique-last-level HPK (ending in `/id`) typically isn't compatible. If you need these features, consider an HPK design where the last level isn't unique (or use an alternative data model), and validate that it still avoids exceeding the 20-GB logical partition limit for your workload.

## Next steps

- [Hierarchical partition keys in Azure Cosmos DB](hierarchical-partition-keys.md)
- [Frequently asked questions on hierarchical partition keys in Azure Cosmos DB](hierarchical-partition-keys-faq.yml)
- [Partitioning and horizontal scaling in Azure Cosmos DB](partitioning.md)
