---
title: Multi-region writes
description: Multi-region writes in Azure Cosmos DB let you achieve near-zero downtime and high availability. Learn how to set up and manage multi-region write accounts.
author: TheovanKraay
ms.author: thvankra
ms.service: azure-cosmos-db
ms.topic: concept-article
ms.date: 09/03/2025
ms.custom:
  - ai-gen-docs-bap
  - ai-gen-title
  - ai-seo-date:08/15/2025
  - ai-gen-description
appliesto:
  - ✅ NoSQL
  - ✅ MongoDB
  - ✅ Apache Cassandra
  - ✅ Apache Gremlin
  - ✅ Table
---

# Multi-region writes in Azure Cosmos DB

To achieve near-zero downtime during a partial or total outage when read consistency isn't required, set up your account for multi-region writes. This article explains the key concepts to know when you set up a multi-region write account. 

## Hub region

In a multi-region-write database account with two or more regions, the first region where your account is created is called the "hub" region. All other regions you add to the account are called "satellite" regions. If you remove the hub region from the account, the next region, in the order you added them, is automatically chosen as the hub region.

Any writes that arrive in satellite regions are quorum committed in the local region, then sent to the hub region for [conflict resolution](conflict-resolution-policies.md) asynchronously. When a write goes to the hub region and is conflict resolved, it becomes a "confirmed" write. Until then, it's a "tentative" or "unconfirmed" write. Any write served from the hub region immediately becomes a confirmed write. 

## Understanding timestamps

A multi-region-write account uses two server timestamp values for each entity. The first is the server epoch time when the entity is written in that region. You see this timestamp in both single-region write and multi-region write accounts. The second server timestamp is the epoch time when the absence of a conflict is confirmed, or a conflict is fixed in the hub region. A confirmed or conflict-fixed write gets a conflict-resolution timestamp (`crts`), but an unconfirmed or tentative write doesn't get `crts`. Cosmos DB sets two timestamps on the server. The main difference is whether the account uses single-write or multi-write region configuration.

| Timestamp | Meaning | When exposed |
| --- | --- | --- |
| `_ts` | The server epoch time at which the entity was written | Always exposed by all read and query APIs. |
| `crts` | The epoch time when a multi-write conflict is fixed, or the absence of a conflict is confirmed. For multi-write region configuration, this timestamp sets the order of changes for Change Feed: Finds the start time for Change Feed requests, Sets the sort order in Change Feed responses. | Shown in Change Feed responses only when the request enables "New Wire Model." This behavior is the default for ["all versions and deletes"](change-feed.md#all-versions-and-deletes-mode-preview) Change Feed mode. |

## Related content

- [Conflict types and resolution policies when using multiple write regions](conflict-resolution-policies.md)
- [Multi-region writes in your applications that use Azure Cosmos DB](how-to-multi-master.md)
- [Consistency levels in Azure Cosmos DB](consistency-levels.md)
- [Request Units in Azure Cosmos DB](request-units.md)
- [Global data distribution with Azure Cosmos DB - under the hood](global-distribution.md)
- [Availability of Azure Cosmos DB software development kits (SDKs) in multiregional environments](troubleshoot-sdk-availability.md)
