---
title: Materialized Views in Azure Managed Instance for Apache Cassandra
description: Learn how to enable materialized views in Azure Managed Instance for Apache Cassandra, which allows maximum flexibility and control where needed.
author: TheovanKraay
ms.author: thvankra
ms.service: azure-managed-instance-apache-cassandra
ms.topic: how-to
ms.date: 06/05/2025
#customer intent: As a database administrator, I want to understand materialized views and how to enable them.
---

# Materialized views in Azure Managed Instance for Apache Cassandra

Azure Managed Instance for Apache Cassandra is a fully managed service for pure open-source Apache Cassandra clusters. The service also allows configurations to be overridden, depending on the specific needs of each workload. This feature allows maximum flexibility and control where needed. This article discusses how to enable materialized views.

## Materialized view support

Materialized views are disabled by default, but you can enable them on your cluster. We discourage users of Azure Managed Instance for Apache Cassandra from using materialized views. They're experimental. In particular:

- The implementation of materialized views is a distributed system design that isn't extensively modeled and simulated. There are no formal proofs about its properties.
- There's no way to determine if a materialized view is out of sync with its base table.
- There's no upper bound on how long it takes for a materialized view to sync when there's a change to its base table.
- If there's an error and a materialized view goes out of sync, the only way to resolve the situation is to drop the materialized view and re-create it.

For more information, see [Materialized views marked experimental-Apache Mail Archives](https://lists.apache.org/thread/o5bk8xyxyl6k3sjf7kkblqw52gm5s9mp) and the [proposal to do so](https://www.mail-archive.com/dev@cassandra.apache.org/msg11516.html).

Microsoft doesn't offer any service-level agreement or support on issues with materialized views.

## Alternatives to materialized views

Like most NoSQL stores, Apache Cassandra isn't designed to have a normalized data model. If you need to update data in more than one place, send all the necessary statements as part of a [BATCH](https://cassandra.apache.org/doc/latest/cassandra/reference/cql-commands/commands-toc.html). This approach has two advantages over materialized views:

- `BATCH` guarantees that all statements in the batch are committed or none.
- All the statements have the same quorum and commit semantics.

If your workload truly needs a normalized data model, consider a scalable relational store like [Azure Cosmos DB for PostgreSQL](../cosmos-db/postgresql/introduction.md).

## Enable materialized views

Set `enable_materialized_views: true` in the `rawUserConfig` field of your Cassandra datacenter. Use the following Azure CLI command to update each datacenter in your cluster:

```azurecli-interactive
FRAGMENT="enable_materialized_views: true"
ENCODED_FRAGMENT=$(echo "$FRAGMENT" | base64 -w 0)
# or
# ENCODED_FRAGMENT="ZW5hYmxlX21hdGVyaWFsaXplZF92aWV3czogdHJ1ZQo="
resourceGroupName='MyResourceGroup'
clusterName='cassandra-hybrid-cluster'
dataCenterName='dc1'
az managed-cassandra datacenter update \
  --resource-group $resourceGroupName \
  --cluster-name $clusterName \
  --data-center-name $dataCenterName \
  --base64-encoded-cassandra-yaml-fragment $ENCODED_FRAGMENT
```

## Related content

- [Create a managed instance cluster from the Azure portal](create-cluster-portal.md)
- [Deploy a Managed Apache Spark Cluster with Azure Databricks](deploy-cluster-databricks.md)
- [Manage Azure Managed Instance for Apache Cassandra resources by using the Azure CLI](manage-resources-cli.md)
