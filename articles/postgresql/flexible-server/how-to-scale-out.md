---
title: Scale Out
description: This article describes how to scale out an Azure Database for PostgreSQL flexible server elastic cluster.
author: JaredMSFT
ms.author: jaredmeade
ms.reviewer: adamwolk, maghan
ms.date: 11/18/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
#customer intent: As a user, I want to learn how to scale out an Azure Database for PostgreSQL elastic cluster.
---

# Scale Out

This article provides step-by-step instructions to perform horizontal scaling operations for your Azure Database for PostgreSQL flexible server elastic cluster.

Azure Database for PostgreSQL Elastic Clusters provides horizontal scaling by adding more worker nodes to your cluster. Scaling your PostgreSQL Elastic Cluster allows you to handle growth by giving your database more resources or more nodes for parallel query processing, all with minimal downtime and built-in shard management.

### [Portal](#tab/portal-scale-compute)

Using the [Azure portal](https://portal.azure.com/):

1. Open the resource: In the Azure portal, navigate to your Azure Database for PostgreSQL – Flexible Server elastic cluster.

2. Go to Compute + Storage: Under the Settings section, click Compute + storage. This blade displays the current configuration of your cluster’s nodes.

    :::image type="content" source="./media/how-to-scale-out/overview.png" alt-text="Screenshot showing the Overview page of an elastic cluster." lightbox="./media/how-to-scale-out/overview.png":::

3. Adjust Node Count: Find the Node count field. Increase the number to the desired total nodes (between 2 and 20 for most clusters at GA). For example, to double a 4-node cluster to 8 nodes, increase the slider to 8. Azure will provision additional worker nodes to reach this count.

    :::image type="content" source="./media/how-to-scale-out/scale-out.png" alt-text="Screenshot showing how to select the Compute + storage page." lightbox="./media/how-to-scale-out/scale-out.png":::

4. Apply changes: Click Save. Confirm the scale-out operation when prompted. Azure will begin adding nodes to your cluster. This operation is performed online and typically does not interrupt existing connections or queries. The deployment may take a few minutes; you can monitor progress in the portal notifications. Once complete, your cluster’s node count will reflect the new value.

> [!NOTE]
> You must explicitly trigger the shard rebalancing background process to allow existing data to be redistributed across all of your nodes. This operation involves no downtime for reads/writes.

### [CLI](#tab/cli-scale-compute)

You can initiate the horizontal scaling of your elastic cluster via the [az postgres flexible-server update](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-update) command.

```azurecli-interactive
az postgres flexible-server update `
  --resource-group <resource_group> `
  --name <cluster_name> `
  --node-count 4
```

## Rebalancing

After adding nodes to your cluster, any new data modifications and/or newly added distributed tables will use all of available nodes. Existing data shards will stay where they are until redistributed. Online rebalancing ensures reads and writes from the application continue with minimal interruption while data is being moved.

Once your elastic cluster has been successfully scaled out, rebalancing your cluster ensures that your existing data is fully distributed and your database is using all available nodes. Use the **citus_rebalance_start** function to initiate the rebalance process. This operation will distribute existing data evenly across all nodes.

```sql
SELECT citus_rebalance_start();
```

## Parallel Rebalancing

The default rebalancing operation carries out multiple shard moves in a sequential order. There are some use cases where you may prefer to rebalance faster at the expense of using more resources such as compute, memory, network bandwidth, etc. In those situations, you are able to configure a rebalance operation to perform a number of shard moves in parallel.

The **citus.max_background_task_executors_per_node** parameter allows tasks such as shard rebalancing to operate in parallel. You can increase the default value (1) as desired to boost parallelism.

```sql
ALTER SYSTEM SET citus.max_background_task_executors_per_node = 2;
SELECT pg_reload_conf();
```

Additionally, the **citus_rebalance_start** function is configurable to rebalance shards according to a number of different strategies, to best match your database workload. Now that we've added additional background task executors, here’s an example of rebalancing shards using parallel workers:

```psql
SELECT citus_rebalance_start(parallel_transfer_colocated_shards := true, parallel_transfer_reference_tables := true);
```
## Additional Considerations

Monitor your cluster after scaling: Check CPU utilization, memory usage, and IO consumption on the Azure portal’s Monitoring charts for your elastic cluster. After a scale-out operation, verify that adding nodes reflects metric improvements for throughput and/or response times, depending on your workload. Adjust further if necessary.

Scaling an elastic cluster affects cost linearly with resources. Adding nodes multiplies compute and storage costs by the number of nodes – e.g., a four-node cluster with two vCores each will roughly cost four times what a single two-vCore server would cost (since you’re running four servers). Always review the pricing impact in the portal (the Estimated Cost is updated on the Azure portal when you change the configuration before saving) to ensure it meets your budget.

High Availability: If your cluster has zone-redundant high availability enabled (each node has a standby in another AZ), scaling operations will also provision standby resources for any new nodes. The Azure service handles this automatically. Expect the scale-out to take slightly longer as it sets up HA replicas for each added node. The process and downtime characteristics remain nearly the same, just multiplied for primary and standby pairs.

Read Replicas: If your cluster is configured to use read replicas, you must follow a specific order of operations when addind additional nodes to your cluster: First, add the number of additional nodes to your primary cluster and save your changes.  Once successfully completed, then make the corresponding change to your read replica environment and save the changes.  Your newly nodes on your primary cluster will not be eligible for cluster operations until both the primary and read replica environments have been updated collectively and synchronized.

> [!NOTE]
> The ability to remove nodes from an elastic cluster (scale-in) is not yet available.

By leveraging the above scaling techniques, Azure PostgreSQL elastic elusters give you the flexibility to start small and grow your database seamlessly as demand increases, combining the simplicity of a single endpoint with the power of distributed Postgres infrastructure. Continue to monitor Azure’s documentation for the latest updates on Elastic Clusters features and best practices for scaling. 

Happy scaling!

## Related content

- [Compute options](concepts-compute.md).
- [Limits in Azure Database for PostgreSQL flexible server](concepts-limits.md).
- [Near-zero downtime scaling](concepts-scaling-resources.md#near-zero-downtime-scaling)



