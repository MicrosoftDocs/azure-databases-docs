---
title: Consistency level choices
description: Azure Cosmos DB has five consistency levels to help balance eventual consistency, availability, and latency trade-offs.
author: markjbrown
ms.author: mjbrown
ms.service: azure-cosmos-db
ms.topic: concept-article
ms.date: 09/03/2025
ms.custom: cosmos-db-video
ai-usage: ai-assisted
appliesto:
  - ✅ NoSQL
  - ✅ MongoDB
  - ✅ Apache Cassandra
  - ✅ Apache Gremlin
  - ✅ Table
---

# Consistency levels in Azure Cosmos DB

Distributed databases that rely on replication for high availability, low latency, or both must balance read consistency, availability, latency, and throughput as defined by the [PACELC theorem](https://en.wikipedia.org/wiki/PACELC_theorem). The linearizability of the strong consistency model is the standard for data programmability. However, it increases write latencies because data must replicate and commit across large distances. Strong consistency also reduces availability during failures because data can't replicate and commit in every region. Eventual consistency offers higher availability and better performance, but it's more difficult to program applications because data might not be consistent across all regions.

> [!VIDEO https://learn-video.azurefd.net/vod/player?id=7b1f8d3d-ae64-4f52-a5b7-252ba78429af]

Most distributed NoSQL databases on the market today provide only strong and eventual consistency. Azure Cosmos DB offers five well-defined levels. From strongest to weakest, the levels are:

- [*Strong*](#strong-consistency)
- [*Bounded staleness*](#bounded-staleness-consistency)
- [*Session*](#session-consistency)
- [*Consistent prefix*](#consistent-prefix-consistency)
- [*Eventual*](#eventual-consistency)

For more information on the default consistency level, see [configuring the default consistency level](how-to-manage-consistency.md#configure-the-default-consistency-level) or [override the default consistency level](how-to-manage-consistency.md#override-the-default-consistency-level).

Each level balances availability and performance. The following image shows the consistency levels as a spectrum.

:::image type="content" source="./media/consistency-levels/five-consistency-levels.png" alt-text="Diagram of consistency as a spectrum starting with strong and progressing to higher availability, throughput, and lower latency with eventual." border="false" :::

## Consistency levels and Azure Cosmos DB APIs

Azure Cosmos DB supports wire protocol-compatible APIs for popular databases, including MongoDB, Apache Cassandra, Apache Gremlin, and Azure Table Storage. For the API for Gremlin or Table, Azure Cosmos DB uses the default consistency level configured on the account. To learn about consistency level mapping, see [API for Cassandra consistency mapping](cassandra/consistency-mapping.md) for Apache Cassandra and [API for MongoDB consistency mapping](mongodb/consistency-mapping.md) for MongoDB.

## Scope of read consistency

Read consistency applies to a single read operation within a logical partition. A remote client, stored procedure, or trigger can issue the read operation.

## Configure the default consistency level

Configure the default consistency level on your Azure Cosmos DB account at any time. The default consistency level configured on your account applies to all Azure Cosmos DB databases and containers under that account. All reads and queries issued against a container or a database use the specified consistency level by default. When you change your account-level consistency, redeploy your applications and make any necessary code modifications to apply these changes. Learn more in [how to configure the default consistency level](how-to-manage-consistency.md#configure-the-default-consistency-level). You can also override the default consistency level for a specific request. Learn more in the [override the default consistency level](how-to-manage-consistency.md?#override-the-default-consistency-level) article.

> [!TIP]
> Overriding the default consistency level applies only to reads within the SDK client. An account configured for strong consistency by default still writes and replicates data synchronously to every region in the account. When the SDK client instance or request overrides this consistency with session or weaker consistency, reads are performed using a single replica. For more information, see [consistency levels and throughput](consistency-levels.md#consistency-levels-and-throughput).

> [!IMPORTANT]
> Recreate any SDK instance after changing the default consistency level by restarting the application. This step ensures the SDK uses the new default consistency level.

## Guarantees associated with consistency levels

Azure Cosmos DB guarantees that 100% of read requests meet the consistency guarantee for the chosen consistency level. The precise definitions of the five consistency levels in Azure Cosmos DB using the  TLA - Temporal Logic of Actions - specification language are provided in the [azure/azure-cosmos-tla](https://github.com/azure/azure-cosmos-tla) GitHub repo.

The semantics of the five consistency levels are described in the following sections.

### Strong consistency

Strong consistency offers a linearizability guarantee. Linearizability means serving requests concurrently. The reads are guaranteed to return the most recent committed version of an item. A client never sees an uncommitted or partial write. Users are always guaranteed to read the latest committed write.

The following graphic shows strong consistency with musical notes. After the data is written to the "West US 2" region, when you read the data from other regions, you get the most recent value:

:::image type="content" source="media/consistency-levels/strong-consistency.gif" alt-text="Animation showing strong consistency level with musical notes that are always synced.":::

#### Dynamic quorum

Under normal circumstances, for an account with strong consistency, a write is considered committed when all regions acknowledge replication of the record. If your account has three or more regions, the system can lower the number of regions needed for a quorum when some regions are slow or not responding. This helps keep strong consistency even if a few regions have issues. At that point, unresponsive regions are taken out of the quorum set of regions in order to preserve strong consistency. They're only added back when they become consistent with other regions and perform as expected. The number of regions that can potentially be taken out of the quorum set depends on the total number of regions. For example, in a three or four region account, the majority is two or three regions respectively, so only one region can be removed in either case. For a five region account, the majority is three, so up to two unresponsive regions can be removed. This capability is known as "dynamic quorum" and can improve both write availability and replication latency for accounts with three or more regions.

> [!NOTE]
> When regions are removed from the quorum set as part of dynamic quorum, those regions are no longer able to serve reads until readded into the quorum.

### Bounded staleness consistency

For single-region write accounts with two or more regions, data is replicated from the primary region to all secondary (read-only) regions. For multi-region write accounts with two or more regions, data is replicated from the region it was originally written in to all other writable regions. In both scenarios, while not common, there could occasionally be a replication lag from one region to another.

In bounded staleness consistency, the lag of data between any two regions is always less than a specified amount. The amount can be "K" versions (that is, "updates") of an item or by "T" time intervals, whichever is reached first. In other words, when you choose bounded staleness, the maximum "staleness" of the data in any region can be configured in two ways:

- The number of versions (*K*) of the item
- The time interval (*T*) reads might lag behind the writes

Bounded staleness is primarily beneficial to single-region write accounts with two or more regions. If the data lag in a region (determined per physical partition) exceeds the configured staleness value, writes for that partition are throttled until staleness is back within the configured upper bound.

For a single-region account, Bounded Staleness provides the same write consistency guarantees as Session and Eventual Consistency. With Bounded Staleness, data is replicated to a local majority (three replicas in a four replica set) in the single region.

> [!IMPORTANT]
> With Bounded Staleness consistency, staleness checks are made only across regions and not within a region. Within a given region, data is always replicated to a local majority (three replicas in a four replicas set) regardless of the consistency level.

Reads when using Bounded Staleness returns the latest data available in that region by reading from two available replicas in that region. Since writes within a region always replicate to a local majority (three out of four replicas), consulting two replicas return the most updated data available in that region.

> [!IMPORTANT]
> With Bounded Staleness consistency, reads from a nonprimary region might not show the latest data from all regions. However, they always return the newest data available in that region, within the allowed staleness limit.

Bounded Staleness works best for globally distributed applications using a single-region write accounts with two or more regions, where near strong consistency across regions is desired. For multi-region write accounts with two or more regions, application servers should direct reads and writes to the same region in which the application servers are hosted. Bounded Staleness in a multi-write account is an anti-pattern. This level would require a dependency on replication lag between regions, which shouldn't matter if data is read from the same region it was written to.

The following graphic illustrates the bounded staleness consistency with musical notes. After the data is written to the "West US 2" region, the "East US 2" and "Australia East" regions read the written value based on the configured maximum lag time or the maximum operations:

:::image type="content" source="media/consistency-levels/bounded-staleness-consistency.gif" alt-text="Animation of bounded staleness consistency level using music notes that are eventually synced within a predefined delay of time or versions.":::

### Session consistency

In session consistency, within a single client session, reads are guaranteed to honor the read-your-writes, and write-follows-reads guarantees. This guarantee assumes a single "writer" session or sharing the session token for multiple writers.

Like all consistency levels weaker than Strong, writes are replicated to a minimum of three replicas (in a four replica set) in the local region, with asynchronous replication to all other regions.

After every write operation, the client receives an updated Session Token from the server. The client caches the tokens and sends them to the server for read operations in a specified region. If the replica against which the read operation is issued contains data for the specified token (or a more recent token), the requested data is returned. If the replica doesn't contain data for that session, the client retries the request against another replica in the region. If necessary, the client retries the read against extra available regions until data for the specified session token is retrieved.

> [!IMPORTANT]
> In Session Consistency, the client uses a session token to guarantee that it never reads data corresponding to an older session. If the client uses an old session token, but newer data is available in the database, the system returns the latest version. Even with an outdated token, you always get the most recent data. The Session Token is used as a minimum version barrier but not as a specific (possibly historical) version of the data to be retrieved from the database.

Session Tokens in Azure Cosmos DB are partition-bound, meaning they're exclusively associated with one partition. In order to ensure you can read your writes, use the session token that was last generated for the relevant items.

If the client didn't initiate a write to a physical partition, the client doesn't contain a session token in its cache and reads to that physical partition behave as reads with Eventual Consistency. Similarly, if the client is re-created, its cache of session tokens is also re-created. Here too, read operations follow the same behavior as Eventual Consistency until subsequent write operations rebuild the client’s cache of session tokens.

> [!IMPORTANT]
> If Session Tokens are being passed from one client instance to another, the contents of the token shouldn't be modified.

Session consistency is the most widely used consistency level for single-region and globally distributed applications. It provides write latencies, availability, and read throughput comparable to that of eventual consistency. Session consistency also provides the consistency guarantees that suit the needs of applications written to operate in the context of a user. The following graphic illustrates the session consistency with musical notes. The "West US 2 writer" and the "East US 2 reader" are using the same session (Session A) so they both read the same data at the same time. Whereas the "Australia East" region is using "Session B" so, it receives data later but in the same order as the writes.

:::image type="content" source="media/consistency-levels/session-consistency.gif" alt-text="Animation of session consistency level using music notes that are synced within a single client session.":::

### Consistent prefix consistency

Like all consistency levels weaker than Strong, writes are replicated to a minimum of three replicas (in a four-replica set) in the local region, with asynchronous replication to all other regions.

In consistent prefix, updates made as single document writes see eventual consistency.

Updates made as a batch within a transaction, are returned consistent to the transaction in which they were committed. Write operations within a transaction of multiple documents are always visible together.

Assume two write operations are performed transactionally (all or nothing operations) on document Doc1 followed by document Doc2, within transactions T1 and T2. When client does a read in any replica, the user sees either "Doc1 v1 and Doc2 v1" or "Doc1 v2 and Doc2 v2" or neither document if the replica is lagging, but never "Doc1 v1 and Doc2 v2" or "Doc1 v2 and Doc2 v1" for the same read or query operation.

The following graphic illustrates the consistency prefix consistency with musical notes. In all the regions, the reads never see out of order writes for a transactional batch of writes:

:::image type="content" source="media/consistency-levels/consistent-prefix.gif" alt-text="Animation of consistent prefix level using music notes that are synced eventually but as a transaction that isn't out of order.":::

### Eventual consistency

Like all consistency levels weaker than Strong, writes are replicated to a minimum of three replicas (in a four replica set) in the local region, with asynchronous replication to all other regions.

In Eventual consistency, the client issues read requests against any one of the four replicas in the specified region. This replica could be lagging and could return stale or no data.

Eventual consistency is the weakest form of consistency because a client might read values older than those values it read in the past. Eventual consistency is ideal where the application doesn't require any ordering guarantees. Examples include count of Retweets, Likes, or nonthreaded comments. The following graphic illustrates the eventual consistency with musical notes.

:::image type="content" source="media/consistency-levels/eventual-consistency.gif" alt-text="Animation showing eventual consistency level with music notes that are eventually synced, but not within a specific bound.":::

## Consistency guarantees in practice

In practice, you might often get stronger consistency guarantees. Consistency guarantees for a read operation correspond to the freshness and ordering of the database state that you request. Read consistency is tied to the ordering and propagation of the write and update operations.  

If there are no write operations on the database, a read operation with **eventual**, **session**, or **consistent prefix** consistency levels might yield the same results as a read operation with the strong consistency level.

If your account is configured with a consistency level other than the strong consistency, you can find out the probability that your clients might get strong and consistent reads for your workloads. Figure out this probability by looking at the *Probabilistically Bounded Staleness (PBS)* metric. This metric is exposed in the Azure portal. For more information, see [Monitor Probabilistically Bounded Staleness (PBS) metric](how-to-manage-consistency.md#monitor-probabilistically-bounded-staleness-metric).

Probabilistically bounded staleness shows how eventual your eventual consistency is. This metric provides insight into how often you get stronger consistency than the consistency level currently configured on your Azure Cosmos DB account. In other words, you can see the probability (measured in milliseconds) of getting consistent reads for a combination of write and read regions.

## Consistency levels and latency

Read latency for all consistency levels is guaranteed to be less than 10 milliseconds at the 99th percentile. Average read latency, at the 50th percentile, is typically 4 milliseconds or less.

Write latency for all consistency levels is guaranteed to be less than 10 milliseconds at the 99th percentile. Average write latency, at the 50th percentile, is usually 5 milliseconds or less. Azure Cosmos DB accounts spanning several regions with strong consistency are an exception to this guarantee.

### Write latency and Strong consistency

For Azure Cosmos DB accounts configured with strong consistency with more than one region, the write latency is equal to two times round-trip time (RTT) between any of the two farthest regions, plus 10 milliseconds at the 99th percentile. High network RTT between regions increases Azure Cosmos DB request latency because strong consistency completes an operation only after ensuring the operation is committed to all regions in the account.

Exact RTT latency depends on speed-of-light distance and Azure networking topology. Azure networking doesn't provide latency service level agreements (SLAs) for RTT between Azure regions, but it publishes [Azure network round-trip latency statistics](/azure/networking/azure-network-latency). For your Azure Cosmos DB account, replication latencies are displayed in the Azure portal. Use the Azure portal by going to the Metrics section and selecting the **Consistency** option. Using the Azure portal, you can monitor the replication latencies between various regions that are associated with your Azure Cosmos DB account.

> [!IMPORTANT]
> Strong consistency for accounts with regions spanning more than 5,000 miles (8,000 kilometers) is blocked by default because of high write latency. To enable this capability, contact support.

## Consistency levels and throughput

- For strong and bounded staleness, reads are done against two replicas in a four-replica set (minority quorum) to ensure consistency guarantees. Session, consistent prefix, and eventual consistency use single-replica reads. As a result, for the same number of request units, read throughput for strong and bounded staleness is half that of the other consistency levels.

- For a given type of write operation, such as insert, replace, upsert, or delete, the write throughput for request units is identical across all consistency levels. For strong consistency, changes must be committed in every region (global majority), while for all other consistency levels, the local majority (three replicas in a four-replica set) is used.

|**Consistency Level**|**Quorum Reads**|**Quorum Writes**|
|--|--|--|
|**Strong**|Local Minority|Global Majority|
|**Bounded Staleness**|Local Minority|Local Majority|
|**Session**|Single Replica (using session token)|Local Majority|
|**Consistent Prefix**|Single Replica|Local Majority|
|**Eventual**|Single Replica|Local Majority|

> [!NOTE]
> The RU cost of reads for local minority reads is twice that of weaker consistency levels because reads are made from two replicas to ensure consistency guarantees for the strong and bounded staleness consistency levels.

## Consistency levels and data durability

In a globally distributed database environment, the consistency level directly affects data durability during a region-wide outage. When developing a business continuity plan, understand the maximum period of recent data updates the application can tolerate losing during recovery from a disruptive event. The time period of updates that can be lost is referred to as the **recovery point objective** (**RPO**).

This table shows the relationship between consistency models and data durability during a region-wide outage.

|**Regions**|**Replication mode**|**Consistency level**|**RPO**|
|---------|---------|---------|---------|
|1|Single or Multiple write regions|Any Consistency Level|< 240 Minutes|
|>1|Single write region|Session, Consistent Prefix, Eventual|< 15 minutes|
|>1|Single write region|Bounded Staleness|*K* & *T*|
|>1|Single write region|Strong|0|
|>1|Multiple write regions|Session, Consistent Prefix, Eventual|< 15 minutes|
|>1|Multiple write regions|Bounded Staleness|*K* & *T*|

*K* = The number of *K* versions (updates) of an item.

*T* = The time interval *T* since the last update.

For a single-region account, the minimum value of *K* and *T* is 10 write operations or 5 seconds. For multi-region accounts, the minimum value of *K* and *T* is 100,000 write operations or 300 seconds. This value defines the minimum recovery point objective (RPO) for data when using Bounded Staleness.

## Strong consistency and multiple write regions

Azure Cosmos DB accounts with multiple write regions can't use strong consistency because a distributed system can't provide a recovery point objective (RPO) of zero and a recovery time objective (RTO) of zero. Additionally, strong consistency with multiple write regions doesn't improve write latency because writes must be replicated and committed to all regions in the account. This setup results in the same write latency as a single-write-region account.

## More reading

To learn more about consistency concepts, read the following articles:

- [High-level TLA⁺ specifications for the five consistency levels offered by Azure Cosmos DB](https://github.com/tlaplus/azure-cosmos-tla)
- [Replicated data consistency explained through baseball (video) by Doug Terry](https://www.youtube.com/watch?v=gluIh8zd26I)
- [Replicated data consistency explained through baseball (whitepaper) by Doug Terry](https://www.microsoft.com/research/publication/replicated-data-consistency-explained-through-baseball/)
- [Session guarantees for weakly consistent replicated data](https://dl.acm.org/citation.cfm?id=383631)
- [Consistency tradeoffs in modern distributed database systems design: CAP is only part of the story](https://www.computer.org/csdl/magazine/co/2012/02/mco2012020037/13rRUxjyX7k)
- [Probabilistic bounded staleness (PBS) for practical partial quorums](https://vldb.org/pvldb/vol5/p776_peterbailis_vldb2012.pdf)
- [Eventually consistent - revisited](https://www.allthingsdistributed.com/2008/12/eventually_consistent.html)

## Related content

- [Configure the default consistency level](how-to-manage-consistency.md#configure-the-default-consistency-level)
- [Override the default consistency level](how-to-manage-consistency.md#override-the-default-consistency-level)
- Learn more about the [Azure Cosmos DB SLA](https://azure.microsoft.com/support/legal/sla/cosmos-db/v1_3/).
