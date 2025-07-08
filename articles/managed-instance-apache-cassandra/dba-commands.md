---
title: Run DBA Commands for Azure Managed Instance for Apache Cassandra
description: Learn how to run DBA commands when you need to use them manually in Azure Managed Instance for Apache Cassandra.
author: TheovanKraay
ms.service: azure-managed-instance-apache-cassandra
ms.custom: devx-track-azurecli, sfi-ropc-blocked
ms.topic: how-to
ms.date: 06/05/2025
ms.author: thvankra
#customer intent: As a database administrator, I want to run DBA commands when necessary to manage Azure Managed Instance for Apache Cassandra.
---

# DBA commands for Azure Managed Instance for Apache Cassandra

Azure Managed Instance for Apache Cassandra is a fully managed service for pure open-source Apache Cassandra clusters. The service also allows configurations to be overridden, depending on the specific needs of each workload. This feature allows maximum flexibility and control where needed. This article describes how to run database administrator (DBA) commands manually when necessary.

> [!IMPORTANT]
> The `nodetool` and `sstable` commands are in public preview.
>
> This feature is provided without a service-level agreement (SLA). We don't recommend this feature for production workloads. For more information, see [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).

## DBA command support

With Azure Managed Instance for Apache Cassandra, you can run `nodetool` and `sstable` commands by using the Azure CLI for routine DBA administration. Not all commands are supported, and there are some limitations. For supported commands, see the following sections.

>[!WARNING]
> Some of these commands can destabilize the Cassandra cluster. Only use these commands carefully and after testing in nonproduction environments. Where possible, deploy a `--dry-run` option first. Microsoft doesn't offer any SLA or support on issues that arise from running commands that alter the default database configuration or tables.

## Run a nodetool command

Azure Managed Instance for Apache Cassandra provides the following Azure CLI command to run DBA commands:

```azurecli-interactive
az managed-cassandra cluster invoke-command --resource-group <rg> \
  --cluster-name <cluster> --host <ip of data node> --command-name nodetool \
  --arguments "<nodetool-subcommand>"="" "paramerter1"="" 
```

The subcommand needs to be in the `--arguments` section with an empty value. The `nodetool` flags without a value are in the form `<flag>"="`. If the flag has a value, it's in the form `<flag>"="value`.

This example shows how to run a `nodetool` command without flags. In this case, it's the `nodetool status` command:

```azurecli-interactive
az managed-cassandra cluster invoke-command --resource-group <rg> --cluster-name <cluster> \
  --host <ip of data node> --command-name nodetool --arguments "status"="" 
```

This example shows how to run a `nodetool` command with a flag. In this case, it's the `nodetool compact` command:

```azurecli-interactive
az managed-cassandra cluster invoke-command --resource-group <rg> --cluster-name <cluster> \
  --host <ip of data node> --command-name nodetool --arguments "compact"="" "-st"="65678794" 
```

Both return JSON in the following form:

```json 
{
    "commandErrorOutput": "",
    "commandOutput": "<result>",
    "exitCode": 0
}
```

In most cases, you need only `commandOutput` or `exitCode`. This example shows how to get only `commandOutput`:

```azurecli-interactive
az managed-cassandra cluster invoke-command --query "commandOutput" --resource-group $resourceGroupName \
  --cluster-name $clusterName --host $host --command-name nodetool --arguments getstreamthroughput=""
```

## Run an sstable command

The `sstable` commands require read/write access to the Cassandra data directory and the Cassandra database to be stopped. To accommodate this requirement, specify these two parameters: `--cassandra-stop-start true` and `--readwrite true`.

```azurecli-interactive
az managed-cassandra cluster invoke-command --resource-group <test-rg> \
  --cluster-name <test-cluster> --host <ip> --cassandra-stop-start true --readwrite true \
  --command-name sstableutil --arguments "system"="peers"
```

```json
{
"commandErrorOutput": "",
"commandOutput": "Listing files...\n/var/lib/cassandra/data/system/peers-37f71aca7dc2383ba70672528af04d4f/me-1-big-CompressionInfo.db\n/var/lib/cassandra/data/system/peers-37f71aca7dc2383ba70672528af04d4f/me-1-big-Data.db\n/var/lib/cassandra/data/system/peers-37f71aca7dc2383ba70672528af04d4f/me-1-big-Digest.crc32\n/var/lib/cassandra/data/system/peers-37f71aca7dc2383ba70672528af04d4f/me-1-big-Filter.db\n/var/lib/cassandra/data/system/peers-37f71aca7dc2383ba70672528af04d4f/me-1-big-Index.db\n/var/lib/cassandra/data/system/peers-37f71aca7dc2383ba70672528af04d4f/me-1-big-Statistics.db\n/var/lib/cassandra/data/system/peers-37f71aca7dc2383ba70672528af04d4f/me-1-big-Summary.db\n/var/lib/cassandra/data/system/peers-37f71aca7dc2383ba70672528af04d4f/me-1-big-TOC.txt\n",
"exitCode": 0
}
```

## Run other commands

The `cassandra-reset-password` command lets a user change their password for Cassandra.

```azurecli-interactive
az managed-cassandra cluster invoke-command --resource-group <rg> --cluster-name <cluster> \
  --host <ip of data node> --command-name cassandra-reset-password --arguments password="<password>"
```

The password is URL encoded (UTF-8) in this command, which means that the following rules apply:

- The alphanumeric characters `a` through `z`, `A` through `Z`, and `0` through `9` remain the same.
- The special characters `.`, `-`, `*`, and `_` remain the same.
- The space character is converted into a plus sign (`+`).
- All other characters are unsafe and are first converted into one or more bytes by using some encoding scheme. The three-character string `%xy` represents each byte, where `xy` is the two-digit hexadecimal representation of the byte.

The `cassandra-reset-auth-replication` command lets a user change their schema for the Cassandra user. Separate the datacenter names by space.

```azurecli-interactive
az managed-cassandra cluster invoke-command --resource-group <rg> --cluster-name <cluster> \
  --host <ip of data node> --command-name cassandra-reset-auth-replication \
  --arguments password="<datacenters>"
```

The datacenters are URL encoded (UTF-8) when they're passed into this command, which means that the following rules apply:

- The alphanumeric characters `a` through `z`, `A` through `Z`, and `0` through `9` remain the same.
- The special characters `.`, `-`, `*`, and `_` remain the same.
- The space character is converted into a plus sign (`+`).
- All other characters are unsafe and are first converted into one or more bytes by using some encoding scheme. The three-character string `%xy` represents each byte, where `xy` is the two-digit hexadecimal representation of the byte.

The `sstable-tree` command lets a user see their SSTables.

```azurecli-interactive
az managed-cassandra cluster invoke-command --resource-group <rg> --cluster-name <cluster> \
  --host <ip of data node> --command-name sstable-tree
```

The `sstable-delete` command lets a user delete their SSTables that were made before a certain time.

```azurecli-interactive
az managed-cassandra cluster invoke-command --resource-group <rg> --cluster-name <cluster> \
  --host <ip of data node> --command-name sstable-delete --arguments datetime="<YYYY-MM-DD hh:mm:ss>"
```

The `datetime` argument must be formatted as shown in the example. You can also add `--dry-run=""` as an argument to see which files the command deletes.

## List of supported sstable commands

For more information on each command, see [SSTable tools](https://cassandra.apache.org/doc/latest/cassandra/managing/tools/sstable/index.html).

- `sstableverify`
- `sstablescrub`
- `sstablemetadata`
- `sstablelevelreset`
- `sstableutil`
- `sstablesplit`
- `sstablerepairedset`
- `sstableofflinerelevel`
- `sstableexpiredblockers`

## List of supported nodetool commands

For more information on each command, see [Use nodetool](https://cassandra.apache.org/doc/latest/cassandra/troubleshooting/use_nodetool.html).

- `status`
- `cleanup`
- `clearsnapshot`
- `compact`
- `compactionhistory`
- `compactionstats`
- `describecluster`
- `describering`
- `disableautocompaction`
- `disablehandoff`
- `disablehintsfordc`
- `drain`
- `enableautocompaction`
- `enablehandoff`
- `enablehintsfordc`
- `failuredetector`
- `flush`
- `garbagecollect`
- `gcstats`
- `getcompactionthreshold`
- `getcompactionthroughput`
- `getconcurrentcompactors`
- `getendpoints`
- `getinterdcstreamthroughput`
- `getlogginglevels`
- `getsstables`
- `getstreamthroughput`
- `gettimeout`
- `gettraceprobability`
- `gossipinfo`
- `info`
- `invalidatecountercache`
- `invalidatekeycache`
- `invalidaterowcache`
- `listsnapshots`
- `netstats`
- `pausehandoff`
- `proxyhistograms`
- `rangekeysample`
- `rebuild`
- `rebuild_index`: For arguments, use `"keyspace"="table indexname..."`.
- `refresh`
- `refreshsizeestimates`
- `reloadlocalschema`
- `replaybatchlog`
- `resetlocalschema`
- `resumehandoff`
- `ring`
- `scrub`
- `setcachecapacity`: For arguments, use `"key-cache-capacity" = "<row-cache-capacity> <counter-cache-capacity>"`.
- `setcachekeystosave`: For arguments, use `"key-cache-keys-to-save":"<row-cache-keys-to-save> <counter-cache-keys-to-save>"`.
- `setcompactionthreshold`: For arguments, use `"<keyspace>"="<table> <minthreshold> <maxthreshold>`.
- `setcompactionthroughput`
- `setconcurrentcompactors`
- `sethintedhandoffthrottlekb`
- `setinterdcstreamthroughput`
- `setstreamthroughput`
- `settimeout`
- `settraceprobability`
- `statusbackup`
- `statusbinary`
- `statusgossip`
- `statushandoff`
- `stop`
- `tablehistograms`
- `tablestats`
- `toppartitions`
- `tpstats`
- `truncatehints`
- `verify`
- `version`
- `viewbuildstatus`

## Related content

- [Create a managed instance cluster from the Azure portal](create-cluster-portal.md)
- [Manage Azure Managed Instance for Apache Cassandra resources by using the Azure CLI](manage-resources-cli.md)
- [Management operations in Azure Managed Instance for Apache Cassandra](management-operations.md)
