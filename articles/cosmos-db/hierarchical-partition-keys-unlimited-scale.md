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

This document explains how hierarchical partition keys (HPK) can help you model high-cardinality data. To avoid hitting the 20 GB logical partition size limit, use a multi-level partition key path that ends with a unique identifier, such as /id.

In Azure Cosmos DB, items are grouped into logical partitions based on the value of the partition key. A single logical partition has a maximum storage size of 20 GB. For more information, see [logical partitions overview](partitioning.md). If your data model causes too many items to share the same partition key value (for example, all events for a single customer, tenant, device, or account), that logical partition can grow until it reaches the 20-GB limit, at which point writes targeting that partition fail.

You can avoid this limit by using [hierarchical partition keys](hierarchical-partition-keys.md) (HPK) with a unique identifier as the final level. A unique identifier guarantees that the previous levels can exceed 20GB. For example, if the partition key hierarchy is TenantId, UserId, and id (guid), then you can have infinite data for each combination of TenantId, UserId. This strategy works with any HPK container — no extra account-level settings are required.

## Best practice: use a unique last level

Choose one to three business-grouping levels (such as tenant, customer, or workload) and use a unique final level of `/id`. Azure Cosmos DB uses the combined hierarchy to distribute items.

For example, a multitenant application might use the following hierarchical partition key path:

- `/tenantId`
- `/userId`
- `/id`

With hierarchical partition keys, the logical partition key is defined as the full concatenation of all levels. In this example, each logical partition key is the combination of `tenantId` + `userId` + `id`. Because `id` is unique for every item, each logical partition contains at most one item and never approaches the 20-GB limit. This means the first and second levels (`tenantId` and `userId`) can individually exceed 20 GB of data, because their data is spread across many logical partitions defined by the full three-level key.

You can apply this strategy today by creating a new container with an HPK path that ends with `/id`. For more information about creating containers with hierarchical partition keys, see [Create a container by using hierarchical partition keys](hierarchical-partition-keys.md#create-a-container-by-using-hierarchical-partition-keys).

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

To use hierarchical partition keys, you must use a supported version of the Azure Cosmos DB SDK. See [supported SDK versions](hierarchical-partition-keys.md#get-started).

## Optional: enforce the pattern at the account level

The ability to exceed 20 GB on the first and second levels is built into hierarchical partition keys — it works automatically when you end your key path with a unique value like `/id`. No account-level property is required to get this benefit.

However, if you want to **enforce** that all new containers created in an account follow this pattern, you can enable the `EnforceHierarchicalPartitionKeyIdLastLevel` property on your account. This property doesn't unlock new functionality — it prevents teams or applications from accidentally creating containers that don't use `/id` as the last level.

> [!NOTE]
> The minimum Resource Provider API version required is `2026-03-15`. For the full REST API specification, see [Database Accounts - Create Or Update](/rest/api/cosmos-db-resource-provider/database-accounts/create-or-update).

### Behavior after enablement

| Behavior | Description |
| --- | --- |
| **No defaulting of `/id`** | Azure Cosmos DB doesn't add `/id` as the last level automatically. You must specify the full HPK path at container creation time with `/id` as the last level. |
| **New container restrictions** | Creating new containers with a non-hierarchical partition key path is blocked on the account. All new containers must use hierarchical partition keys with `/id` as the last level. |
| **Existing containers unchanged** | Enabling this property doesn't retroactively modify existing containers or their partition key configuration. To adopt this pattern for existing containers, create a new container with the desired HPK definition and [migrate your data](container-copy.md). |
| **Support for additional levels** | There is support for four levels, however, a fourth level is recommended only for rare scenarios where three levels are needed in addition to `/id`. |

## Enable and configure enforcement

If you choose to enable the account-level enforcement, use one of the following methods to set the `EnforceHierarchicalPartitionKeyIdLastLevel` property on your account.

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
    '/userId'
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
        "/userId",
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

After you enable the property, create a new container by specifying a hierarchical partition key path that ends with `/id` (for example: `/tenantId`, `/userId`, `/id`). For more information about creating containers with hierarchical partition keys, see [Create a container by using hierarchical partition keys](hierarchical-partition-keys.md#create-a-container-by-using-hierarchical-partition-keys).

## Frequently asked questions

### Why am I getting errors related to the 20-GB limit?

This typically means a single logical partition (a single partition key value) has accumulated more than 20 GB of data. Switching to HPK and ensuring the final level is unique (for example, `/id`) helps prevent unbounded growth under one value. To proactively monitor for logical partitions approaching this limit, see [Create alerts to monitor logical partition key storage size](how-to-alert-on-logical-partition-key-storage-size.md).

### Why does my request fail with "The last level of the hierarchical partition key must be '/id'"?

With `EnforceHierarchicalPartitionKeyIdLastLevel` enabled, your items must include every partition key property in the hierarchy. For example, if your HPK is `/tenantId`, `/userId`, `/id`, then each item must have `tenantId`, `userId`, and `id` properties. The request must supply the matching full partition key value for point reads, updates, and deletes.

### Why can't I create a container with a non-hierarchical partition key? Request failing with "Non-hierarchical partition key collection creation is blocked"

After you enable `EnforceHierarchicalPartitionKeyIdLastLevel`, you must use hierarchical partition keys for all newly created containers. This restriction doesn't affect existing containers.

### Can I change an existing container to use hierarchical partition keys?

No. Partition key configuration is immutable. To adopt HPK (or to add a unique last level like `/id`), create a new container with the desired HPK definition and [migrate your data by using container copy jobs](container-copy.md).

### Can I still use transactional batch, stored procedures, or triggers?

If your usage depends on grouping multiple items under a single shared partition key value, a unique-last-level HPK (ending in `/id`) isn't compatible. If you need these features, consider an HPK design where the last level isn't unique (or use an alternative data model), and validate that it still avoids exceeding the 20-GB logical partition limit for your workload.

## Next steps

- [Hierarchical partition keys in Azure Cosmos DB](hierarchical-partition-keys.md)
- [Frequently asked questions on hierarchical partition keys in Azure Cosmos DB](hierarchical-partition-keys-faq.yml)
- [Partitioning and horizontal scaling in Azure Cosmos DB](partitioning.md)
