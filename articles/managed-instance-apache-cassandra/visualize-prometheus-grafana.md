---
title: Configure Grafana to Visualize Metrics Emitted from Azure Managed Instance for Apache Cassandra
description: Learn how to install and configure Grafana in a virtual machine to visualize metrics emitted from an Azure Managed Instance for Apache Cassandra cluster.
author: TheovanKraay
ms.service: azure-managed-instance-apache-cassandra
ms.topic: how-to
ms.date: 11/16/2021
ms.author: thvankra
ms.custom: sfi-image-nochange
---

# Configure Grafana to visualize metrics emitted from the managed instance cluster

When you deploy an Azure Managed Instance for Apache Cassandra cluster, the service provisions [Metrics Collector for Apache Cassandra](https://github.com/datastax/metric-collector-for-apache-cassandra) agent software on each data node. [Prometheus](https://prometheus.io/) consumes the metrics and they're visualized through Grafana. This article describes how to configure Prometheus and Grafana to visualize metrics emitted from your managed instance cluster.

The following tasks are required to visualize metrics:

* Deploy an Ubuntu virtual machine (VM) inside the Azure virtual network where the managed instance is present.
* Install the [Prometheus dashboards](https://github.com/datastax/metric-collector-for-apache-cassandra#installing-the-prometheus-dashboards) onto the VM.

> [!WARNING]
> Prometheus and Grafana are open-source software and aren't supported as part of Azure Managed Instance for Apache Cassandra. Visualizing metrics in the way described in this article requires you to host and maintain a VM as the server for both Prometheus and Grafana. The instructions in this article were tested only for Ubuntu Server 18.04. There's no guarantee that they work with other Linux distributions.
>
> Following this approach means that you must support any issues that might arise, such as running out of space or availability of the server. For a fully supported and hosted metrics experience, consider using [Azure Monitor metrics](monitor-clusters.md#azure-managed-instance-for-apache-cassandra-metrics) or [Azure Monitor partner integrations](/azure/azure-monitor/partners).

## Deploy an Ubuntu server

1. Sign in to the [Azure portal](https://portal.azure.com/).

1. Go to the resource group where your managed instance cluster is located. Select **Add** and search for the **Ubuntu Server 18.04 LTS** image.

   :::image type="content" source="./media/visualize-prometheus-grafana/select-ubuntu-image.png" alt-text="Screenshot that shows finding the Ubuntu server image from the Azure portal." border="true":::

1. Select the image, and then select **Create**.

1. On the **Create a virtual machine** pane, enter values for the following fields. You can leave default values for other fields:

   * **Virtual machine name**: Enter a name for your VM.
   * **Region**: Select the same region where your virtual network is deployed.

   :::image type="content" source="./media/visualize-prometheus-grafana/create-vm-ubuntu.png" alt-text="Screenshot that shows filling out the form to create a VM with the Ubuntu server image." border="true":::

1. On the **Networking** tab, select the virtual network in which your managed instance is deployed.

   :::image type="content" source="./media/visualize-prometheus-grafana/configure-networking-details.png" alt-text="Screenshot that shows configuring the Ubuntu server's network settings." border="true":::

1. Finally, select **Review + create** to create your metrics server.

## Install Prometheus dashboards

1. First, ensure that the networking settings for your newly deployed Ubuntu server have inbound port rules that allow ports `9090` and `3000`. These ports are required later for Prometheus and Grafana, respectively.

   :::image type="content" source="./media/visualize-prometheus-grafana/networking.png" alt-text="Screenshot that shows allowed ports." border="true":::

1. Connect to your Ubuntu server by using the [Azure CLI](/azure/virtual-machines/linux/ssh-from-windows#ssh-clients) or your preferred client tool to connect via Secure Shell.

1. After you connect to the VM, install the metrics collector software. First, download and unzip the files:

   ```bash
    #install unzip utility (if not already installed)
    sudo apt install unzip
    
    #get dashboards
    wget https://github.com/datastax/metric-collector-for-apache-cassandra/releases/download/v0.3.0/datastax-mcac-dashboards-0.3.0.zip -O temp.zip
    unzip temp.zip
   ```

1. Next, go to the Prometheus directory and use `vi` to edit the `tg_mcac.json` file:

   ```bash
    cd */prometheus
    vi tg_mcac.json    
   ```

1. Add the IP addresses of each node in your cluster in `targets`, each with port 9443. Your `tg_mcac.json` file should look like the following example:

   ```bash
    [
      {
        "targets": [
          "10.9.0.6:9443","10.9.0.7:9443","10.9.0.8:9443"
        ],
        "labels": {
    
        }
      }
    ]  
   ```

1. Save the file. Next, edit the `prometheus.yaml` file in the same directory. Locate the following section:

   ```bash
    file_sd_configs:
      - files:
        - 'tg_mcac.json'
   ```

1. Directly underneath this section, add the following snippet. This step is required because metrics are exposed via HTTPS.

   ```bash
    scheme: https
    tls_config:
            insecure_skip_verify: true
   ```

1. The file should now look like the following example. Ensure that the tabs on each line match the example:

   ```bash
    file_sd_configs:
      - files:
        - 'tg_mcac.json'
    scheme: https
    tls_config:
            insecure_skip_verify: true
   ```

1. Save the file. Now you can start Prometheus and Grafana. First, install Docker:

    ```bash
    sudo apt install apt-transport-https ca-certificates curl software-properties-common
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu `lsb_release -cs` test"
    sudo apt update
    sudo apt install docker-ce
    ```

1. Then install `docker-compose`:

    ```bash
    sudo apt install docker-compose
    ```

1. Now go to the top-level directory where `docker-compose.yaml` is located, and start the application:

    ```bash
    cd ..
    sudo docker-compose up
    ```

1. Prometheus should be available at port `9090` and Grafana dashboards on port `3000` on your metrics server.

   :::image type="content" source="./media/visualize-prometheus-grafana/monitor-cassandra-metrics.png" alt-text="View the Cassandra managed instance metrics in the dashboard." border="true":::

## Related content

In this article, you learned how to configure dashboards to visualize metrics in Prometheus by using Grafana. Learn more about Azure Managed Instance for Apache Cassandra with the following articles:

* [What is Azure Managed Instance for Apache Cassandra?](introduction.md)
* [Deploy a Managed Apache Spark Cluster with Azure Databricks](deploy-cluster-databricks.md)
