---
title: Troubleshoot forbidden exceptions
titleSuffix: Azure Cosmos DB for NoSQL
description: Diagnose and fix various causes for forbidden exceptions that can occur when working with Azure Cosmos DB for NoSQL.
author: ealsur
ms.author: maquaran
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: troubleshooting
ms.date: 08/28/2025
---

# Diagnose and troubleshoot Azure Cosmos DB forbidden exceptions

[!INCLUDE[NoSQL](../includes/appliesto-nosql.md)]

The HTTP status code 403 represents the request is forbidden to complete.

## Firewall blocking requests

Data plane requests can come to Azure Cosmos DB via the following three paths.

- Public internet (IPv4)
- Service endpoint
- Private endpoint

When a data plane request is blocked with 403 Forbidden, the error message specifies via which of the previous three paths the request came to Azure Cosmos DB.

- `Request originated from client IP {...} through public internet.`
- `Request originated from client VNET through service endpoint.`
- `Request originated from client VNET through private endpoint.`

### Solution

Understand via which path is the request **expected** to come to Azure Cosmos DB.

- If the error message shows that the request didn't come to Azure Cosmos DB via the expected path, the issue is likely to be with client-side setup. Double check your client-side setup following documentations.
  - Public internet: [Configure IP firewall in Azure Cosmos DB](../how-to-configure-firewall.md).
  - Service endpoint: [Configure access to Azure Cosmos DB from virtual networks](../how-to-configure-vnet-service-endpoint.md). Consider if you expected to use service endpoint but the request came to Azure Cosmos DB from the public internet. This situation could indicate that the subnet that the client was running in didn't enable service endpoint to Azure Cosmos DB.
  - Private endpoint: [Configure Azure Private Link for an Azure Cosmos DB account](../how-to-configure-private-endpoints.md). Also consider if you expected to use private endpoint but the request came to Azure Cosmos DB from the public internet. This situation could indicate that the domain name server (DNS) on the virtual machine wasn't configured to resolve account endpoint to the private instead of the public IP address.
- If the request came to Azure Cosmos DB via the expected path, request was blocked because the source network identity wasn't configured for the account. Check account's settings depending on the path the request came to Azure Cosmos DB.
  - Public internet: check account's [public network access](../how-to-configure-private-endpoints.md#blocking-public-network-access-during-account-creation) and IP range filter configurations.
  - Service endpoint: check account's [public network access](../how-to-configure-private-endpoints.md#blocking-public-network-access-during-account-creation) and virtual network filter configurations.
  - Private endpoint: check account's private endpoint configuration and client's private DNS configuration. This issue could be due to accessing account from a private endpoint that is set up for a different account.

If you recently updated account's firewall configurations, keep in mind that changes can take **up to 15 minutes to apply**.

## Partition key exceeding storage

On this scenario, it's common to see errors like the ones here:

```output
Response status code does not indicate success: Forbidden (403); Substatus: 1014
```

```output
Partition key reached maximum size of {...} GB
```

### Solution

This error means that your current [partitioning design](../partitioning-overview.md#logical-partitions) and workload is trying to store more than the allowed amount of data for a given partition key value. There's no limit to the number of logical partitions in your container but the size of data each logical partition can store is limited. You can reach to support for clarification.

## Nondata operations aren't allowed

This scenario happens when [attempting to perform nondata operations](security/reference-data-plane-actions.md) using Microsoft Entra identities. On this scenario, it's common to see errors like the ones here:

```output
Operation 'POST' on resource 'calls' is not allowed through Azure Cosmos DB endpoint
```

```output
Forbidden (403); Substatus: 5300; The given request [PUT ...] cannot be authorized by AAD token in data plane.
```

### Solution

Perform the operation through Azure Resource Manager, Azure portal, Azure CLI, or Azure PowerShell.
If you're using the [Azure Functions Azure Cosmos DB Trigger](/azure/azure-functions/functions-bindings-cosmosdb-v2-trigger), make sure the `CreateLeaseContainerIfNotExists` property of the trigger isn't set to `true`. Using Microsoft Entra identities blocks any nondata operation, such as creating the lease container.

## Related content

- [IP Firewall](../how-to-configure-firewall.md).
- [Virtual networks](../how-to-configure-vnet-service-endpoint.md).
- [Private endpoints](../how-to-configure-private-endpoints.md).
