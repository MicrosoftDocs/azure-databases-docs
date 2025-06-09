---
title: Quickstart - Use CLI to create Azure Managed Instance for Apache Cassandra cluster
description: Use this quickstart to create an Azure Managed Instance for Apache Cassandra cluster using Azure CLI.
author: TheovanKraay
ms.author: thvankra
ms.service: azure-managed-instance-apache-cassandra
ms.topic: quickstart
ms.date: 06/09/2025
ms.custom: mode-api, devx-track-azurecli
ms.devlang: azurecli
#customer intent: As a developer, I want to create clusters in Azure Managed Instance for Apache Cassandra by using the Azure CLI.
---

# Quickstart: Create an Azure Managed Instance for Apache Cassandra cluster using Azure CLI

Azure Managed Instance for Apache Cassandra is a fully managed service for pure open-source Apache Cassandra clusters. The service also allows configurations to be overridden, depending on the specific needs of each workload, which allows maximum flexibility and control where needed.

This quickstart demonstrates how to use the Azure command line interface (CLI) commands to create a cluster with Azure Managed Instance for Apache Cassandra. It also shows how to create a datacenter, and scale nodes up or down within the datacenter.

[!INCLUDE [azure-cli-prepare-your-environment.md](~/reusable-content/azure-cli/azure-cli-prepare-your-environment.md)]

- [Azure Virtual Network](/azure/virtual-network/virtual-networks-overview) with connectivity to your self-hosted or on-premises environment. For more information on connecting on premises environments to Azure, see [Connect an on-premises network to Azure](/azure/architecture/reference-architectures/hybrid-networking/).

- If you don't have an Azure subscription, create a [free account](https://azure.microsoft.com/free/?WT.mc_id=A261C142F) before you begin.

> [!IMPORTANT]
> This article requires the Azure CLI version 2.30.0 or higher. If you're using Azure Cloud Shell, the latest version is already installed.

## <a id="create-cluster"></a>Create a managed instance cluster

1. Sign in to the [Azure portal](https://portal.azure.com/).

1. Set your subscription ID in Azure CLI:

   ```azurecli-interactive
   az account set --subscription <Subscription_ID>
   ```

1. Next, create a Virtual Network with a dedicated subnet in your resource group:

   ```azurecli-interactive
   az network vnet create --name <VNet_Name> --location eastus2 \
     --resource-group <Resource_Group_Name> --subnet-name <Subnet Name>
   ```

   > [!NOTE]
   > The Deployment of an Azure Managed Instance for Apache Cassandra requires internet access. Deployment fails in environments where internet access is restricted. Make sure you aren't blocking access in your virtual network to the following Azure services that are required for Managed Cassandra to work properly:
   >
   > - Azure Storage
   > - Azure KeyVault
   > - Azure Virtual Machine Scale Sets (VMSS)
   > - Azure Monitoring
   > - Microsoft Entra ID
   > - Azure Security

1. Apply these specific permissions to the Virtual Network. The managed instance requires them. Use the `az role assignment create` command, replacing `<subscriptionID>`, `<resourceGroupName>`, and `<vnetName>` with the appropriate values:

   ```azurecli-interactive
   az role assignment create \
     --assignee a232010e-820c-4083-83bb-3ace5fc29d0b \
     --role 4d97b98b-1d4f-4787-a291-c67834d212e7 \
     --scope /subscriptions/<subscriptionID>/resourceGroups/<resourceGroupName>/providers/Microsoft.Network/virtualNetworks/<vnetName>
   ```

   > [!NOTE]
   > The `assignee` and `role` values are fixed values. Enter these values exactly as mentioned in the command. Not doing so leads to errors when creating the cluster. If you encounter any errors when executing this command, you might not have permissions to run it. Reach out to your Azure admin for permissions.

1. Next, create the cluster in your newly created Virtual Network by using the [az managed-cassandra cluster create](/cli/azure/managed-cassandra/cluster#az-managed-cassandra-cluster-create) command. Run the following command the value of `delegatedManagementSubnetId` variable:

   > [!NOTE]
   > The value of the `delegatedManagementSubnetId` is the same virtual network name that the permissions were applied.


   ```azurecli-interactive
   resourceGroupName='<Resource_Group_Name>'
   clusterName='<Cluster_Name>'
   location='eastus2'
   delegatedManagementSubnetId='/subscriptions/<subscription ID>/resourceGroups/<resource group name>/providers/Microsoft.Network/virtualNetworks/<VNet name>/subnets/<subnet name>'
   initialCassandraAdminPassword='myPassword'
   cassandraVersion='3.11' # set to 4.0 for a Cassandra 4.0 cluster

   az managed-cassandra cluster create \
     --cluster-name $clusterName \
     --resource-group $resourceGroupName \
     --location $location \
     --delegated-management-subnet-id $delegatedManagementSubnetId \
     --initial-cassandra-admin-password $initialCassandraAdminPassword \
     --cassandra-version $cassandraVersion \
     --debug
   ```

1. Create a datacenter for the cluster, with three virtual machines using the following configuration:

   - VM Size: Standard E8s v5
   - Datadisks: 4 P30 disks attached to each of the virtual machines deployed.

   - With all in place, use the [az managed-cassandra datacenter create](/cli/azure/managed-cassandra/datacenter#az-managed-cassandra-datacenter-create) command:

   ```azurecli-interactive
   dataCenterName='dc1'
   dataCenterLocation='eastus2'
   virtualMachineSKU='Standard_D8s_v4'
   noOfDisksPerNode=4

   az managed-cassandra datacenter create \
     --resource-group $resourceGroupName \
     --cluster-name $clusterName \
     --data-center-name $dataCenterName \
     --data-center-location $dataCenterLocation \
     --delegated-subnet-id $delegatedManagementSubnetId \
     --node-count 3 \
     --sku $virtualMachineSKU \
     --disk-capacity $noOfDisksPerNode \
     --availability-zone false
   ```

   > [!NOTE]
   > The value for `--sku` can be chosen from the following available VM sizes:
   >
   > - Standard_E8s_v5
   > - Standard_E16s_v5
   > - Standard_E20s_v5
   > - Standard_E32s_v5
   >
   > By default, `--availability-zone` is set to `false`. To enable availability zones, set it to `true`. Availability zones help increasing the availability of the service. For more information, see [SLA for Online Services](https://azure.microsoft.com/support/legal/sla/managed-instance-apache-cassandra/v1_0/).

   > [!WARNING]
   > Availability zones aren't supported in all Azure regions. Deployments fail if you select a region where Availability zones aren't supported. For supported regions, see [Azure regions list](/azure/reliability/availability-zones-region-support).
   >
   > The successful deployment of availability zones is subject to the availability of compute resources in all of the zones in the region selected. Deployments fail if the virtual machine size you choose isn't available in the region selected.

1. Once the datacenter is created, you can run the [az managed-cassandra datacenter update](/cli/azure/managed-cassandra/datacenter#az-managed-cassandra-datacenter-update) command to scale down or up your cluster. Change the value of `node-count` parameter to the desired value:

   ```azurecli-interactive
   resourceGroupName='<Resource_Group_Name>'
   clusterName='<Cluster Name>'
   dataCenterName='dc1'
   dataCenterLocation='eastus2'

   az managed-cassandra datacenter update \
     --resource-group $resourceGroupName \
     --cluster-name $clusterName \
     --data-center-name $dataCenterName \
     --node-count 9
   ```

## Connect to your cluster

Azure Managed Instance for Apache Cassandra doesn't create nodes with public IP addresses. To connect to your new Cassandra cluster, you must create another resource inside the same virtual network. This resource can be an application, or a virtual machine with Apache's open-source query tool [CQLSH](https://cassandra.apache.org/doc/stable/cassandra/managing/tools/cqlsh.html) installed.

You can use a [Resource Manager template](https://azure.microsoft.com/resources/templates/vm-simple-linux/) to deploy an Ubuntu virtual machine.

> [!NOTE]
> Due to some [known issues](https://issues.apache.org/jira/browse/CASSANDRA-19206) with versions of Python, we recommend that you use an Ubuntu 22.04 image which comes with Python3.10.12 or use a [Python virtual environment](https://docs.python.org/3/library/venv.html) to run CQLSH.

### Connecting from CQLSH

After the virtual machine is deployed, use SSH to connect to the machine and install CQLSH as shown in the following commands:

```bash
# Install default-jre and default-jdk
sudo apt update
sudo apt install openjdk-8-jdk openjdk-8-jre
```
Check which [versions of Cassandra are still supported](https://cassandra.apache.org/_/download.html) and pick the version you need. We recommend that you use a stable version.

Install the Cassandra libraries in order to get CQLSH by following the official steps from the [Cassandra documentation](https://cassandra.apache.org/doc/stable/cassandra/managing/tools/cqlsh.html).

Connect by using cqlsh, as described in the documentation.

### Connecting from an application

As with CQLSH, connecting from an application using one of the supported [Apache Cassandra client drivers](https://cassandra.apache.org/doc/stable/cassandra/getting-started/drivers.html) requires SSL encryption to be enabled, and certification verification to be disabled. For samples, see [Java](https://github.com/Azure-Samples/azure-cassandra-mi-java-v4-getting-started), [.NET](https://github.com/Azure-Samples/azure-cassandra-mi-dotnet-core-getting-started), [Node.js](https://github.com/Azure-Samples/azure-cassandra-mi-nodejs-getting-started), and [Python](https://github.com/Azure-Samples/azure-cassandra-mi-python-v4-getting-started).

Disabling certificate verification is recommended because certificate verification doesn't work unless you map IP addresses of your cluster nodes to the appropriate domain. If you have an internal policy which mandates that you do SSL certificate verification for any application, you can facilitate by adding entries like `10.0.1.5 host1.managedcassandra.cosmos.azure.com` in your hosts file for each node. If taking this approach, you would also need to add new entries anytime you scale up nodes.

For Java, we highly recommend enabling [speculative execution policy](https://docs.datastax.com/en/developer/java-driver/4.10/manual/core/speculative_execution/) where applications are sensitive to tail latency. For a demo that illustrate how this works and how to enable the policy, see [Implementing speculative execution policy](https://github.com/Azure-Samples/azure-cassandra-mi-java-v4-speculative-execution).

> [!NOTE]
> You usually don't need to configure certificates, rootCA, nodes, clients, or truststores for connecting to Azure Managed Instance for Apache Cassandra. SSL encryption uses the default truststore and the client's chosen runtime password. For sample code, see [Java](https://github.com/Azure-Samples/azure-cassandra-mi-java-v4-getting-started), [.NET](https://github.com/Azure-Samples/azure-cassandra-mi-dotnet-core-getting-started), [Node.js](https://github.com/Azure-Samples/azure-cassandra-mi-nodejs-getting-started), and [Python](https://github.com/Azure-Samples/azure-cassandra-mi-python-v4-getting-started)). Certificates are trusted by default. If not, add them to the truststore.

### Configuring client certificates (optional)

Configuring client certificates is optional. A client application can connect to Azure Managed Instance for Apache Cassandra as long as the preceding steps are followed. If preferred, you can also create and configure client certificates for authentication. In general, there are two ways of creating certificates:

**Self-signed certificates**: Private and public certificates (no CA) for each node. In this case, all public certificates are required.

**Certificates signed by a CA**: Issued by a self-signed CA or a public CA. For this setup, you need the root CA certificate and all intermediary certificates, if applicable. For more information, see [Preparing SSL certificates for production](https://docs.datastax.com/en/cassandra-oss/3.x/cassandra/configuration/secureSSLCertWithCA.html). 

To implement client-to-node certificate authentication or mutual Transport Layer Security (mTLS), provide the certificates by using Azure CLI. The following command uploads and applies your client certificates to the truststore for your Cassandra managed instance cluster. There's no need to modify `cassandra.yaml` settings. Once applied, the cluster requires Cassandra to verify certificates during client connections. See `require_client_auth: true` in Cassandra [client_encryption_options](https://cassandra.apache.org/doc/stable/cassandra/managing/configuration/cass_yaml_file.html)


   ```azurecli-interactive
   resourceGroupName='<Resource_Group_Name>'
   clusterName='<Cluster Name>'

   az managed-cassandra cluster update \
     --resource-group $resourceGroupName \
     --cluster-name $clusterName \
     --client-certificates /usr/csuser/clouddrive/rootCert.pem /usr/csuser/clouddrive/intermediateCert.pem
   ```


## Troubleshooting

If you encounter an error when applying permissions to your Virtual Network using Azure CLI, you can apply the same permission manually from the Azure portal. An example of such an error is *Cannot find user or service principal in graph database for 'e5007d2c-4b13-4a74-9b6a-605d99f03501'*. For more information, see [Use the Azure portal to add Azure Cosmos DB service principal](add-service-principal.md).

> [!NOTE]
> The Azure Cosmos DB role assignment is used for deployment purposes only. Azure Managed Instanced for Apache Cassandra has no backend dependencies on Azure Cosmos DB.

## Clean up resources

When no longer needed, you can use the `az group delete` command to remove the resource group, the managed instance, and all related resources:

```azurecli-interactive
az group delete --name <Resource_Group_Name>
```

## Next steps

In this quickstart, you learned how to create an Azure Managed Instance for Apache Cassandra cluster using Azure CLI. You can now start working with the cluster:

> [!div class="nextstepaction"]
> [Deploy a Managed Apache Spark Cluster with Azure Databricks](deploy-cluster-databricks.md)
