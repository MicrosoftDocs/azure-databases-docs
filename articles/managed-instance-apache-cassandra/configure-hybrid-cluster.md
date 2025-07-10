---
title: 'Quickstart: Configure a Hybrid Cluster with Azure Managed Instance for Apache Cassandra Client Configurator'
description: This quickstart shows how to configure a hybrid cluster with Azure Managed Instance for Apache Cassandra Client Configurator.
author: IriaOsara
ms.author: iriaosara
ms.reviewer: sidandrews
ms.date: 05/30/2025
ms.service: azure-managed-instance-apache-cassandra
ms.topic: quickstart
ms.custom:
  - ignite-2023
  - devx-track-azurecli
ms.devlang: azurecli
---

# Quickstart: Configure a hybrid cluster with Azure Managed Instance for Apache Cassandra by using Client Configurator

The Azure Client Configurator is a tool designed to assist you in configuring a hybrid cluster and simplifying the migration process to Azure Managed Instance for Apache Cassandra. If you currently have on-premises datacenters or are operating in a self-hosted environment, you can use Azure Managed Instance for Apache Cassandra to seamlessly incorporate other datacenters into your cluster while effectively maintaining them.

> [!IMPORTANT]  
> The Client Configurator tool is in public preview. This feature is provided without a service-level agreement. We don't recommend it for production workloads.
>
> For more information, see [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).

[!INCLUDE [azure-cli-prepare-your-environment.md](~/reusable-content/azure-cli/azure-cli-prepare-your-environment.md)]

- This article requires the Azure CLI version 2.30.0 or higher. If you're using Azure Cloud Shell, the latest version is already installed.
- [Azure Virtual Network](/azure/virtual-network/virtual-networks-overview) with connectivity to your self-hosted or on-premises environment. For more information on how to connect on-premises environments to Azure, see [Connect an on-premises network to Azure](/azure/architecture/reference-architectures/hybrid-networking/).
- Python installation is required. To check if Python is installed, run `python --version` in your terminal.
- Ensure that both the Azure Managed Instance for Apache Cassandra cluster and the on-premises Cassandra cluster are located on the same virtual network. If not, you need to establish network peering or another means of connectivity. For example, use Azure ExpressRoute.
- The cluster name for both the managed cluster and local cluster must be the same.
    * In the `cassandra.yaml` file, ensure that the storage port is set to 7001 and the cluster name is the same as the managed cluster:

    ```bash
    cluster_name: managed_cluster-name
    storage_port: 7001
     ```
    
    ```sql
    UPDATE system.local SET cluster_name = 'managed_cluster-name' where key='local';
    ```

## Installation

1. Download and go into the [client configurator folder](https://aka.ms/configurator-tool).
1. Set up a virtual environment to run the Python script:

    ```bash
    python3 -m venv env
    source env/bin/activate
    python3 -m pip install -r requirements.txt
    ```

1. Sign in to the Azure CLI `az login`.
1. Run the Python script within the client folder with information from the existing (on-premises) cluster:

    ```python
    python3 client_configurator.py --subscription-id <subcriptionId> --cluster-resource-group <clusterResourceGroup> --cluster-name <clusterName> --initial-password <initialPassword> --vnet-resource-group <vnetResourceGroup> --vnet-name <vnetName> --subnet-name <subnetName> --location <location> --seed-nodes <seed1 seed2 seed3> --mi-dc-name <managedInstanceDataCenterName> --dc-name <onPremDataCenterName> --sku <sku>
    ```

    |Parameter|Description|
    |---------|-----------|
    `subscription-ID`| Azure subscription ID
    `cluster-resource-group`| Resource group where your cluster resides
    `cluster-name`| Azure Managed Instance for Apache Cassandra cluster name
    `initial-password`| Password for your Azure Managed Instance for Apache Cassandra cluster
    `vnet-resource-group`| Resource group attached to the virtual network
    `vnet-name`| Name of the virtual network attached to your cluster
    `subnet-name`| Name of the IP addressed allocated to the Cassandra cluster
    `location`| Where your cluster is deployed
    `seed-nodes`| Seed nodes of the existing datacenters in your on-premises or self-hosted Cassandra cluster
    `mi-dc-name`| Datacenter name of your Azure Managed Instance for Apache Cassandra cluster
    `dc-name`| Datacenter name of the on-premises cluster
    `sku`| Virtual machine product tier size

1. The Python script produces a tar archive named `install_certs.tar.gz`.
    * Unpack this folder into `/etc/cassandra/` on each node:

      ```bash
      sudo tar -xzvf install_certs.tar.gz -C /etc/cassandra
      ```

1. Inside the `/etc/cassandra/` folder, run `sudo ./install_certs.sh`.
   * Ensure that the script is executable by running `sudo chmod +x install_certs.sh`.
   * The script installs and points Cassandra toward the new certificates that are needed to connect to the Azure Managed Instance for Apache Cassandra cluster.
   * It then prompts the user to restart Cassandra.

     :::image type="content" source="media/configure-hybrid-cluster/script-result.png" alt-text="Screenshot that shows the result of running the script." lightbox="media/configure-hybrid-cluster/script-result.png":::

1. After Cassandra is finished restarting on all nodes, check `nodetool status`. Both datacenters should appear in the list, with their nodes in the `UN (Up/Normal)` state.
1. From your instance of Azure Managed Instance for Apache Cassandra, you can then select `AllKeyspaces` to change the replication settings in your keyspace schema and start the migration process to the Azure Managed Instance for Cassandra cluster.
1. Enable the `autoReplicate` setting by using an Azure Resource Manager template (ARM template). The ARM template should include:

    ```json
    "properties":{
    ...
    "externalDataCenters": ["dc-name-1","dc-name-2"],
    "autoReplicate": "AllKeyspaces",
    ...
    }
    ```

    All of your keyspaces definitions change to include  
    `WITH REPLICATION = { 'class' : 'NetworkTopologyStrategy', 'on-prem-datacenter-1' : 3, 'mi-datacenter-1': 3 }`.
    If this topology isn't what you want, adjust it and run `nodetool rebuild` manually on the Azure Managed Instance for Apache Cassandra cluster.
  
    Learn more about [autoreplication](https://aka.ms/auto-replication).

1. Update and monitor data replication progress by selecting the **Data Center** pane.

   :::image type="content" source="media/configure-hybrid-cluster/replication-progress.png" border="true" alt-text="Screenshot that shows replication progress." lightbox="media/configure-hybrid-cluster/replication-progress.png":::

## Next step

> [!div class="nextstepaction"]
> [Learn how to migrate to Azure Managed Instance for Apache Cassandra by using Apache Spark and a dual-write proxy](dual-write-proxy-migration.md)
