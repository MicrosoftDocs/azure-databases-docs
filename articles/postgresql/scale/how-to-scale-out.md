---
title: Scale Out With Elastic Clusters
description: This article describes how to scale out an Azure Database for PostgreSQL flexible server elastic cluster.
author: JaredMSFT
ms.author: jaredmeade
ms.reviewer: adamwolk, maghan
ms.date: 11/18/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
# customer intent: As a user, I want to learn how to scale out an Azure Database for PostgreSQL elastic cluster.
---

# Scale out with elastic clusters

This article provides step-by-step instructions to perform horizontal scaling operations for your Azure Database for PostgreSQL flexible server elastic cluster.

Azure Database for PostgreSQL Elastic Clusters provides horizontal scaling by adding more worker nodes to your cluster. When you scale your PostgreSQL Elastic Cluster, you can handle growth by giving your database more resources or more nodes for parallel query processing. You get all these benefits with minimal downtime and built-in shard management.

## Scale-out methods

Use one of several methods to add worker nodes to your elastic cluster—including the Azure portal, the Azure CLI, or automation via ARM templates and APIs—depending on your workflow and automation needs. The following sections provide step‑by‑step instructions for the portal and CLI, and explain post‑scale rebalancing. 

#### [Portal](#tab/portal-scale-compute)

Using the [Azure portal](https://portal.azure.com/):

1. Open the resource: In the Azure portal, navigate to your Azure Database for PostgreSQL – Flexible Server elastic cluster.

1. Go to Compute + Storage: Under the Settings section, select Compute + storage. This page displays the current configuration of your cluster's nodes.

   :::image type="content" source="./media/how-to-scale-out/overview.png" alt-text="Screenshot showing the Overview page of an elastic cluster." lightbox="./media/how-to-scale-out/overview.png":::

1. Adjust Node Count: Find the Node count field. Increase the number to the desired total nodes (between 2 and 20 for most clusters at GA). For example, to double a four node cluster to eight nodes, increase the slider to 8. Azure provisions additional worker nodes to reach this count.

   :::image type="content" source="./media/how-to-scale-out/scale-out.png" alt-text="Screenshot showing how to select the Compute + storage page." lightbox="./media/how-to-scale-out/scale-out.png":::

1. Apply changes: Select Save. Confirm the scale-out operation when prompted. Azure begins adding nodes to your cluster. This operation is performed online and typically doesn't interrupt existing connections or queries. The deployment might take a few minutes. You can monitor progress in the portal notifications. Once complete, your cluster's node count reflects the new value.

> [!NOTE]
> You must explicitly trigger the shard rebalancing background process to allow existing data to be redistributed across all of your nodes. This operation involves no downtime for reads and writes.

#### [CLI](#tab/cli-scale-compute)

You can initiate the horizontal scaling of your elastic cluster with the [az postgres flexible-server update](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-update) command.

```azurecli-interactive
az postgres flexible-server update `
  --resource-group <resource_group> `
  --name <cluster_name> `
  --node-count 4
```

---

## Rebalancing

After adding nodes to your cluster, any new data modifications or newly added distributed tables use all of the available nodes. Existing data shards stay where they are until they're redistributed. Online rebalancing ensures that reads and writes from the application continue with minimal interruption while data is being moved.

When you scale out your elastic cluster, rebalancing your cluster ensures that your existing data is fully distributed and your database uses all available nodes. Use the **citus_rebalance_start** function to start the rebalance process. This operation distributes existing data evenly across all nodes.

```sql
SELECT citus_rebalance_start();
```

## Parallel rebalancing

The default rebalancing operation carries out multiple shard moves in a sequential order. In some cases, you might prefer to rebalance faster at the expense of using more resources such as compute, memory, and network bandwidth. In those situations, you can configure a rebalance operation to perform many shard moves in parallel.

The **citus.max_background_task_executors_per_node** parameter allows tasks such as shard rebalancing to operate in parallel. You can increase the default value (1) as desired to boost parallelism.

```sql
ALTER SYSTEM SET citus.max_background_task_executors_per_node = 2;
SELECT pg_reload_conf();
```

Additionally, you can configure the **citus_rebalance_start** function to rebalance shards according to different strategies to best match your database workload. Now that you added extra background task executors, here's an example of rebalancing shards by using parallel workers:

```psql
SELECT citus_rebalance_start(parallel_transfer_colocated_shards := true, parallel_transfer_reference_tables := true);
```

## Considerations

Monitor your cluster after scaling: Check CPU utilization, memory usage, and IO consumption on the Azure portal's Monitoring charts for your elastic cluster. After a scale-out operation, verify that adding nodes reflects metric improvements for throughput and response times, depending on your workload. Adjust further if necessary.

Scaling an elastic cluster affects cost linearly with resources. Adding nodes multiplies compute and storage costs by the number of nodes. For example, a four-node cluster with two vCores each costs roughly four times what a single two-vCore server costs, since you're running four servers. Always review the pricing impact in the portal. The Estimated Cost is updated on the Azure portal when you change the configuration before saving to ensure it meets your budget.

High availability: If your cluster has zone-redundant high availability enabled, scaling operations also provision standby resources for any new nodes. The Azure service handles this automatically. Expect the scale-out to take slightly longer as it sets up HA replicas for each added node. The process and downtime characteristics remain nearly the same, multiplied for primary and standby pairs.

Read replicas: If your cluster is configured to use read replicas, you must follow a specific order of operations when adding nodes to your cluster. First, add the number of nodes to your primary cluster and save your changes. Once successfully completed, make the corresponding change to your read replica environment and save the changes. Your new nodes on your primary cluster aren't eligible for cluster operations until both the primary and read replica environments are updated and synchronized.

> [!NOTE]  
> The ability to remove nodes from an elastic cluster (scale-in) isn't yet available.

By using the preceding scaling techniques, Azure Database for PostgreSQL elastic clusters give you the flexibility to start small and grow your database seamlessly as demand increases. You get the simplicity of a single endpoint with the power of distributed Postgres infrastructure. Continue to monitor Azure's documentation for the latest updates on Elastic Clusters features and best practices for scaling.

## Related content

- [Compute options](concepts-compute.md)
- [Limits in Azure Database for PostgreSQL flexible server](concepts-limits.md)
- [Near-zero downtime scaling](concepts-scaling-resources.md#near-zero-downtime-scaling)
