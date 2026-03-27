---
title: Activity logs for elastic (split/merge) operations
description: Learn how to use Azure Activity Log to track partition split and merge operations in Azure Cosmos DB, including throughput scaling and multi-round splits.
author: vidatonkova
ms.author: vidatonkova
ms.service: azure-cosmos-db
ms.topic: how-to
ms.date: 03/16/2026
ai-usage: ai-assisted
appliesto:
  - ✅ NoSQL
  - ✅ MongoDB
  - ✅ Apache Cassandra
  - ✅ Apache Gremlin
  - ✅ Table
---

# Activity logs for elastic (split/merge) operations

## Background

In Azure Cosmos DB, each physical partition supports up to 10,000 RU/s of throughput and 50 GB of storage. When you increase the provisioned throughput of a database or container beyond the capacity of the current physical partitions, Azure Cosmos DB must split those partitions to accommodate the extra throughput.

A partition split divides an existing physical partition into new partitions. Each new partition takes on a portion of the data and throughput capacity of the original. This process allows the container to serve a higher total throughput because each new partition adds an additional 10,000 RU/s of capacity. Azure Cosmos DB may also merge partitions to optimize the layout for best performance and data distribution.

Both splitting and merging partitions can take hours to complete, so tracking their progress is essential. The Activity Log in the Azure portal shows the status of these elastic operations — both throughput increases (partition splits) and decreases (partition merges).

For more details on how partition splits work and best practices for scaling, see [Best practices for scaling provisioned throughput](scaling-provisioned-throughput-best-practices.md).

## Monitoring elastic operations in the Activity Log

Both partition splits and merges follow the same Activity Log pattern. To monitor the progress of an elastic operation:

1. Navigate to your Azure Cosmos DB account in the Azure portal.
1. In the left menu, select **Activity Log**.
1. Filter by the resource name of the database or container you scaled.
1. Look for log entries related to the elastic operation. Each entry includes an operation name, a status, and a timestamp.
1. Expand the log entry to see the linked scale operations nested under the main entry. The main entry reflects the latest overall status of the scaling operation. Each nested operation has its own status as well.
1. Select an individual log to open a details pane on the right. Under the **JSON** tab, the "properties" section contains detailed information about the operation.

Each operation progresses through three statuses. The specific details within each status differ between splits and merges, as described in the next sections.

| Status | Description |
| --- | --- |
| Started | Emitted at the beginning of the operation, after Azure Cosmos DB determines which partitions will split or merge. |
| In Progress | Emitted on a 30-minute interval for the duration of the operation, providing updated details as work progresses. You may not see this status if the operation finishes in under 30 minutes. |
| Succeeded | Emitted once, at the very end when the operation is complete. |

The following example shows a scale-up operation as it appears in the Activity Log, demonstrating the layout described above.

:::image type="content" source="media/monitor-activity-logs-elastic-operations/activity-log-scale-up-overview.png" lightbox="media/monitor-activity-logs-elastic-operations/activity-log-scale-up-overview.png" alt-text="Screenshot of the Activity Log in the Azure portal showing a scale-up operation with nested entries.":::

## Increasing throughput / partition split

Example: Suppose you have a container with 1 physical partition, handling 5,000 RU/s. You then increase the throughput to 15,000 RU/s. The existing partition can only support up to 10,000 RU/s — not enough for the requested 15,000 RU/s. Azure Cosmos DB splits it to create more partitions that can distribute the higher throughput.

### Main Activity Log

Once the throughput split operation has started, you'll see a main entry titled:

"Throughput Split Operation – Scaling up to throughput of 15,000"

The number reflects your new target throughput. This main entry contains all nested operations related to the split. Expand it to see the individual status updates as the operation progresses.

:::image type="content" source="media/monitor-activity-logs-elastic-operations/split-main-entry.png" lightbox="media/monitor-activity-logs-elastic-operations/split-main-entry.png" alt-text="Screenshot of the main Activity Log entry for a throughput split operation.":::

### Nested Activity Logs

**Started Status** — The Activity Log entry shows your new target throughput and the partitions that will be split to reach it. This confirms the scaling operation is underway. For this example, the new throughput is 15,000 RU/s and partition "0" will be split.

:::image type="content" source="media/monitor-activity-logs-elastic-operations/split-started-status.png" lightbox="media/monitor-activity-logs-elastic-operations/split-started-status.png" alt-text="Screenshot of the Started status entry for a partition split operation showing the target throughput and partitions to split.":::

**In Progress Status** — Emitted approximately every 30 minutes. This status provides a detailed breakdown of each partition involved in the split. Each partition is represented as one operation in the trace, allowing you to track progress at a granular level.

The breakdown below includes the values for our example and descriptions of each property.

| Property | Example Checkpoint 1 | Example Checkpoint 2 | Description |
| --- | --- | --- | --- |
| Total Operations Required | `1` | `1` | The total number of partitions that need to split to serve the requested throughput. |
| In Progress Operations | `1` | `0` | Partitions that are actively splitting. |
| WaitingToBeScheduled | `0` | `0` | Partitions ready to split but temporarily blocked by another operation on the same partition. These will proceed automatically. |
| Completed Operations | `0` | `1` | Partitions that have finished splitting and are now serving traffic at the new throughput. |
| Failed Operations | `0` | `0` | Partitions that encountered an error. These are automatically requeued under a new operation ID and will appear as a separate operation. |

The image below shows how these properties appear in the JSON tab of the Activity Log entry in the Azure portal.

:::image type="content" source="media/monitor-activity-logs-elastic-operations/split-in-progress-json.png" lightbox="media/monitor-activity-logs-elastic-operations/split-in-progress-json.png" alt-text="Screenshot of the In Progress JSON properties for a partition split in the Activity Log JSON tab.":::

**Succeeded Status** — The split is complete, all new partitions are online, and your full provisioned throughput is available.

:::image type="content" source="media/monitor-activity-logs-elastic-operations/split-succeeded-status.png" lightbox="media/monitor-activity-logs-elastic-operations/split-succeeded-status.png" alt-text="Screenshot of the Succeeded status entry for a completed partition split operation.":::

### Activity Log Status JSON Table

The table below shows the JSON properties emitted at each stage of a partition split operation. Checkpoint 1 and Checkpoint 2 illustrate how the In Progress status updates over time as partitions complete their work.

| Status | JSON Properties | |
| --- | --- | --- |
| Started | `{ "isSharedThroughput": "False", "resourceRid": "<id>", "databaseName": "database1", "collectionName": "container1", "targetThroughput": "15000", "status": "Will split partitions 0 into different partitions" }` | |
| In Progress | **Checkpoint 1:** <br> `{ "isSharedThroughput": "False", "resourceRid": "<id>", "databaseName": "database1", "collectionName": "container1", "targetThroughput": "15000", "Total Operations Required": "1", "In Progress Operations": "1", "WaitingToBeScheduled Operations": "0", "Completed Operations": "0", "Failed Operations": "0" }` | **Checkpoint 2:** <br> `{ "isSharedThroughput": "False", "resourceRid": "<id>", "databaseName": "database1", "collectionName": "container1", "targetThroughput": "15000", "Total Operations Required": "1", "In Progress Operations": "0", "WaitingToBeScheduled Operations": "0", "Completed Operations": "1", "Failed Operations": "0" }` |
| Succeeded | `{ "isSharedThroughput": "False", "resourceRid": "<id>", "databaseName": "database1", "collectionName": "container1", "targetThroughput": "15000", "status": "Completed splits operation" }` | |

## Multiple rounds of splitting

For larger throughput increases, the split process happens in multiple rounds. Each round splits partitions created by the previous round until enough exist to serve the requested throughput. Each round has its own Started and In Progress log entries. When all rounds are complete, a single Succeeded status appears on the main log entry.

Within each round, the Activity Log captures periodic checkpoints approximately every 30 minutes. Each checkpoint appears as an In Progress entry with an updated snapshot of the operation's status. Depending on how long the round takes, you may see multiple In Progress entries. If the round finishes quickly (for example, 30 minutes or less), you may only see a Started status without any In Progress reports.

Example: Suppose you have a container with 1,000 RU/s and 1 physical partition, and you increase the throughput to 30,000 RU/s.

Round 1 — Partition 0 splits into Partition 1 and Partition 2.

Round 2 — Partition 1 splits into Partition 3 and Partition 4.

At the end, you have 3 partitions (Partitions 2, 3, and 4) serving the 30,000 RU/s. Once Round 2 is completed, the main log entry shows Succeeded.

```
Main log status: Started

┌───────  Round 1: Split  ───────┐

  Partition 0
  1,000 RU/s

  ▼                              ▼

  Partition 1        Partition 2
                     ✓ final partition

┌───────  Round 2: Split  ───────┐

  Partition 1

  ▼                              ▼

  Partition 3        Partition 4
  ✓ final partition  ✓ final partition

───────  Final Partitions  ───────

  Partition 2    Partition 3    Partition 4
  from Round 1   from Round 2   from Round 2

✔ RESULT: 3 partitions serving 30,000 RU/s

Main log status: Succeeded
```

The Activity Log displays entries in the portal stacked top-down, with the most recent on top. Each round begins with its own Started entry. All In Progress entries between one Started and the next belong to the same round.

:::image type="content" source="media/monitor-activity-logs-elastic-operations/multi-round-split-activity-log.png" lightbox="media/monitor-activity-logs-elastic-operations/multi-round-split-activity-log.png" alt-text="Screenshot of the Activity Log showing multiple rounds of partition splits with Started and In Progress entries for each round.":::

For this example, the Activity Log outputs results every 5 minutes. Round 1 of the split is surrounded by the blue box and shows a Started status, followed by 2 In Progress entries. Round 2 follows a similar pattern and is enclosed by the purple box.

:::image type="content" source="media/monitor-activity-logs-elastic-operations/multi-round-split-rounds.png" lightbox="media/monitor-activity-logs-elastic-operations/multi-round-split-rounds.png" alt-text="Screenshot of the Activity Log portal view showing Round 1 and Round 2 split entries highlighted in separate boxes.":::

### Activity Log Status JSON Table

The table below shows the JSON content extracted directly from the Activity Log entries. For clarity, the common JSON fields are omitted and only the status is left.

**Round 1: Split**

| Status | JSON Properties | |
| --- | --- | --- |
| Started | `{ "status": "Will split partitions 0 into different partitions" }` | |
| In Progress | **Checkpoint 1:** <br> `{ "Total Operations Required": "1", "In Progress Operations": "1", "WaitingToBeScheduled Operations": "0", "Completed Operations": "0", "Failed Operations": "0" }` | **Checkpoint 2:** <br> `{ "Total Operations Required": "1", "In Progress Operations": "0", "WaitingToBeScheduled Operations": "0", "Completed Operations": "1", "Failed Operations": "0" }` |

Partition 0 has finished splitting, as shown by the transition from an In Progress operation to a Completed Operation. Now we move on to split Partition 2.

**Round 2: Split**

| Status | JSON Properties | |
| --- | --- | --- |
| Started | `{ "status": "Will split partitions 2 into different partitions" }` | |
| In Progress | **Checkpoint 1:** <br> `{ "Total Operations Required": "1", "In Progress Operations": "1", "WaitingToBeScheduled Operations": "0", "Completed Operations": "0", "Failed Operations": "0" }` | **Checkpoint 2:** <br> `{ "Total Operations Required": "1", "In Progress Operations": "0", "WaitingToBeScheduled Operations": "0", "Completed Operations": "1", "Failed Operations": "0" }` |
| Succeeded | `{ "status": "Completed splits operation" }` | |

## Partition merge

When you decrease the provisioned throughput of a database or container significantly, the existing number of physical partitions may no longer be necessary. You can start a partition merge to reduce the physical partition count and optimize RU/s and data distribution. Merging reduces the overhead of maintaining unused partitions and allows the system to operate more efficiently at the reduced throughput.

A merge operation combines multiple existing partitions into a single new partition. For example, if Partitions 2, 3, and 4 are merged, the result is one new Partition 5. Each new partition created by a merge is represented as one operation in the Activity Log. The merge follows the same pattern of status updates as a throughput split.

Example: Suppose you scaled a container up to 100,000 RU/s for a large data migration, which required 10 physical partitions. Though 10 physical partitions can hold 500 GB of data, only 50 GB of data was ingested, and steady state RU/s needed is only 10,000 RU/s.

After reducing the provisioned throughput to 10,000 RU/s, you can merge the 10 partitions down to 1 partition and optimize your RU/s usage.

### Main Activity Log

Once the partition merge operation has started, you'll see a main entry titled:

"PartitionCoalescer Merge operation for Container"

This entry serves as the parent for all nested operations related to the merge. Use this entry for the duration of the operation to track its progress. There might be other merge-related logs linked underneath, such as "Merge the physical partitions of a SQL container", but they don't contain status information.

The following example shows multiple merge-related logs under the main entry. Only the **PartitionCoalescer Merge operation for Container** entry is relevant.

:::image type="content" source="media/monitor-activity-logs-elastic-operations/merge-main-entry.png" lightbox="media/monitor-activity-logs-elastic-operations/merge-main-entry.png" alt-text="Screenshot of the main Activity Log entry for a partition merge operation showing nested merge-related logs.":::

### Nested Activity Logs

**Started Status**— The Activity Log entry shows the container involved in the merge and the partitions that will be merged. The container reflects whether it uses provisioned or shared throughput. There's no target throughput for this operation type because you aren't scaling up. In this example, all 10 partitions merge into 1 partition.

:::image type="content" source="media/monitor-activity-logs-elastic-operations/merge-started-status.png" lightbox="media/monitor-activity-logs-elastic-operations/merge-started-status.png" alt-text="Screenshot of the Started status entry for a partition merge operation showing partitions to merge.":::

**In Progress** — Emitted approximately every 30 minutes. This status provides a detailed breakdown of each merge operation. Each merge is represented as one operation in the trace, so you can track progress at a granular level.

The breakdown below includes the values for our example and descriptions of each property.

| Property | Example Checkpoint 1 | Example Checkpoint 2 | Description |
| --- | --- | --- | --- |
| Total Operations Required | `1` | `1` | The total number of partition merges needed to reach the target partition count. |
| In Progress Operations | `1` | `0` | Merges that are actively running. |
| WaitingToBeScheduled | `0` | `0` | Merges ready to proceed but temporarily blocked by another operation on the same partition. |
| Completed Operations | `0` | `1` | Merges that have finished. |
| Failed Operations | `0` | `0` | Merges that encountered an error. These are automatically requeued under a new operation ID. |

The image below shows how these properties appear in the JSON tab of the Activity Log entry in the Azure portal.

:::image type="content" source="media/monitor-activity-logs-elastic-operations/merge-in-progress-json.png" lightbox="media/monitor-activity-logs-elastic-operations/merge-in-progress-json.png" alt-text="Screenshot of the In Progress JSON properties for a partition merge in the Activity Log JSON tab.":::

**Succeeded** — The merge is complete and the remaining partitions are serving traffic.

:::image type="content" source="media/monitor-activity-logs-elastic-operations/merge-succeeded-status.png" lightbox="media/monitor-activity-logs-elastic-operations/merge-succeeded-status.png" alt-text="Screenshot of the Succeeded status entry for a completed partition merge operation.":::

### Activity Log Status JSON Table

The table below shows the JSON properties emitted at each stage of a merge operation. Checkpoint 1 and Checkpoint 2 illustrate how the In Progress status updates over time as partitions complete their work.

| Status | JSON Properties | |
| --- | --- | --- |
| Started | `{ "isSharedThroughput": "False", "resourceRid": "<id>", "databaseName": "database3", "collectionName": "container3", "status": "Collection <id> will merge partitions 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 into a new partition" }` | |
| In Progress | **Checkpoint 1:** <br> `{ "isSharedThroughput": "False", "resourceRid": "<id>", "databaseName": "database3", "collectionName": "container3", "Total Operations Required": "1", "In Progress Operations": "1", "WaitingToBeScheduled Operations": "0", "Completed Operations": "0", "Failed Operations": "0" }` | **Checkpoint 2:** <br> `{ "isSharedThroughput": "False", "resourceRid": "<id>", "databaseName": "database3", "collectionName": "container3", "Total Operations Required": "1", "In Progress Operations": "0", "WaitingToBeScheduled Operations": "0", "Completed Operations": "1", "Failed Operations": "0" }` |
| Succeeded | `{ "isSharedThroughput": "False", "resourceRid": "<id>", "databaseName": "database3", "collectionName": "container3", "status": "Completed merge operation." }` | |
