---
title: Quickstart - Use CLI to create Azure Managed Instance for Apache Cassandra cluster
description: Use this quickstart to create an Azure Managed Instance for Apache Cassandra cluster using Azure CLI.
author: TheovanKraay
ms.author: thvankra
ms.service: azure-managed-instance-apache-cassandra
ms.topic: quickstart
ms.date: 11/02/2021
ms.custom: mode-api, devx-track-azurecli
ms.devlang: azurecli
---

# Quickstart: Create an Azure Managed Instance for Apache Cassandra cluster using Azure CLI

Azure Managed Instance for Apache Cassandra is a fully managed service for pure open-source Apache Cassandra clusters. The service also allows configurations to be overridden, depending on the specific needs of each workload, allowing maximum flexibility and control where needed.

This quickstart demonstrates how to use the Azure command line interface (CLI) commands to create a cluster with Azure Managed Instance for Apache Cassandra. It also shows how to create a datacenter, and scale nodes up or down within the datacenter.

[!INCLUDE [azure-cli-prepare-your-environment.md](~/reusable-content/azure-cli/azure-cli-prepare-your-environment.md)]

* [Azure Virtual Network](/azure/virtual-network/virtual-networks-overview) with connectivity to your self-hosted or on-premises environment. For more information on connecting on premises environments to Azure, see the [Connect an on-premises network to Azure](/azure/architecture/reference-architectures/hybrid-networking/) article.

* If you don't have an Azure subscription, create a [free account](https://azure.microsoft.com/free/?WT.mc_id=A261C142F) before you begin.

> [!IMPORTANT]
> This article requires the Azure CLI version 2.30.0 or higher. If you are using Azure Cloud Shell, the latest version is already installed.

## <a id="create-cluster"></a>Create a managed instance cluster

1. Sign in to the [Azure portal](https://portal.azure.com/)

1. Set your subscription ID in Azure CLI:

   ```azurecli-interactive
   az account set -s <Subscription_ID>
   ```

1. Next, create a Virtual Network with a dedicated subnet in your resource group:

   ```azurecli-interactive
   az network vnet create -n <VNet_Name> -l eastus2 -g <Resource_Group_Name> --subnet-name <Subnet Name>
   ```

   > [!NOTE]
   > The Deployment of an Azure Managed Instance for Apache Cassandra requires internet access. Deployment fails in environments where internet access is restricted. Make sure you are not blocking access within your virtual network (VNet) to the following Azure services that are required for Managed Cassandra to work properly:
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
   > The `assignee` and `role` values are fixed values. Enter these values exactly as mentioned in the command. Not doing so leads to errors when creating the cluster. If you encounter any errors when executing this command, you may not have permissions to run it, reach out to your Azure admin for permissions.

1. Next create the cluster in your newly created Virtual Network by using the [az managed-cassandra cluster create](/cli/azure/managed-cassandra/cluster#az-managed-cassandra-cluster-create) command. Run the following command the value of `delegatedManagementSubnetId` variable:

   > [!NOTE]
   > The value of the `delegatedManagementSubnetId` is the same VNet name that the permissions were applied.


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

 - VM Size: Standard D8s v4 (Other sizes can be also used depending on your deployment, this is the minimal recommended size)
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
   > - Standard_E8s_v4
   > - Standard_E16s_v4
   > - Standard_E20s_v4
   > - Standard_E32s_v4
   > - Standard_DS13_v2
   > - Standard_DS14_v2
   > - Standard_D8s_v4
   > - Standard_D16s_v4
   > - Standard_D32s_v4
   >
   > Note that `--availability-zone` is set to `false`. To enable availability zones, set it to `true`. Availability zones help increasing the availability of the service. For more details, review the full service-level agreement (SLA) details [here](https://azure.microsoft.com/support/legal/sla/managed-instance-apache-cassandra/v1_0/).

   > [!WARNING]
   > Availability zones are not supported in all Azure regions. Deployments fail if you select a region where Availability zones are not supported. See [here](/azure/reliability/availability-zones-region-support) for supported regions. The successful deployment of availability zones is subject to the availability of compute resources in all of the zones in the region selected. Deployments fail if the virtual machine size you choose is not available in the region selected.

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

Azure Managed Instance for Apache Cassandra does not create nodes with public IP addresses. To connect to your new Cassandra cluster, you must create another resource inside the same virtual network. This resource can be an application, or a virtual machine (VM) with Apache's open-source query tool [CQLSH](https://cassandra.apache.org/doc/latest/cassandra/tools/cqlsh.html) installed.

You can use a [Resource Manager template](https://azure.microsoft.com/resources/templates/vm-simple-linux/) to deploy an Ubuntu virtual machine.

> [!NOTE]
> Due to some [known issues](https://issues.apache.org/jira/browse/CASSANDRA-19206) with versions of Python, the recommendation is to use an Ubuntu 22.04 image which comes with Python3.10.12 or use a [Python virtual environment](https://docs.python.org/3/library/venv.html) to run CQLSH.

### Connecting from CQLSH

After the virtual machine is deployed, use SSH to connect to the machine and install CQLSH as shown in the following commands:

```bash
# Install default-jre and default-jdk
sudo apt update
sudo apt install openjdk-8-jdk openjdk-8-jre
```
Check which [versions of Cassandra are still supported](https://cassandra.apache.org/_/download.html) and pick the version you need. Stable versions are recommended.

Install the Cassandra libraries in order to get CQLSH by following the official steps from the [Cassandra documentation](https://cassandra.apache.org/doc/stable/cassandra/getting_started/installing.html#installing-the-debian-packages)

Connect by simply using cqlsh, as described in the documentation.

### Connecting from an application

As with CQLSH, connecting from an application using one of the supported [Apache Cassandra client drivers](https://cassandra.apache.org/doc/latest/cassandra/getting_started/drivers.html) requires SSL encryption to be enabled, and certification verification to be disabled. See samples for connecting to Azure Managed Instance for Apache Cassandra using [Java](https://github.com/Azure-Samples/azure-cassandra-mi-java-v4-getting-started), [.NET](https://github.com/Azure-Samples/azure-cassandra-mi-dotnet-core-getting-started), [Node.js](https://github.com/Azure-Samples/azure-cassandra-mi-nodejs-getting-started) and [Python](https://github.com/Azure-Samples/azure-cassandra-mi-python-v4-getting-started).

Disabling certificate verification is recommended because certificate verification does not work unless you map IP addresses of your cluster nodes to the appropriate domain. If you have an internal policy which mandates that you do SSL certificate verification for any application, you can facilitate by adding entries like `10.0.1.5 host1.managedcassandra.cosmos.azure.com` in your hosts file for each node. If taking this approach, you would also need to add new entries anytime you scale up nodes.

For Java, we highly recommend enabling [speculative execution policy](https://docs.datastax.com/en/developer/java-driver/4.10/manual/core/speculative_execution/) where applications are sensitive to tail latency. You can find a demo illustrating how this works and how to enable the policy [here](https://github.com/Azure-Samples/azure-cassandra-mi-java-v4-speculative-execution).

> [!NOTE]
> In most cases it should **not be necessary** to configure or install certificates (rootCA, node or client, truststores and so on) to connect to Azure Managed Instance for Apache Cassandra. SSL encryption is enabled by using the default truststore and a password of the runtime used by the client (see [Java](https://github.com/Azure-Samples/azure-cassandra-mi-java-v4-getting-started), [.NET](https://github.com/Azure-Samples/azure-cassandra-mi-dotnet-core-getting-started), [Node.js](https://github.com/Azure-Samples/azure-cassandra-mi-nodejs-getting-started) and [Python](https://github.com/Azure-Samples/azure-cassandra-mi-python-v4-getting-started) samples), because Azure Managed Instance for Apache Cassandra certificates will be trusted by that environment. In rare cases, if the certificate is not trusted, you may need to add it to the truststore.

### Configuring client certificates (optional)

Configuring client certificates is **optional**. A client application can connect to Azure Managed Instance for Apache Cassandra as long as the above steps have been taken. However, if preferred, you can also additionally create and configure client certificates for authentication. In general, there are two ways of creating certificates:

- Self signed certs. This means a private and public (no CA) certificate for each node - in this case we need all public certificates.
- Certs signed by a CA. This can be a self-signed CA or even a public one. In this case we need the root CA certificate (refer to [instructions on preparing SSL certificates](https://docs.datastax.com/en/cassandra-oss/3.x/cassandra/configuration/secureSSLCertWithCA.html) for production), and all intermediaries (if applicable).

If you need to implement client-to-node certificate authentication or mutual Transport Layer Security (mTLS), you need to provide the certificates via Azure CLI. The below command will upload and apply your client certificates to the truststore for your Cassandra Managed Instance cluster (i.e. you do not need to edit `cassandra.yaml` settings). Once applied, your  cluster will require Cassandra to verify the certificates when a client connects (see `require_client_auth: true` in Cassandra [client_encryption_options](https://cassandra.apache.org/doc/latest/cassandra/configuration/cass_yaml_file.html#client_encryption_options)).

   ```azurecli-interactive
   resourceGroupName='<Resource_Group_Name>'
   clusterName='<Cluster Name>'

   az managed-cassandra cluster update \
     --resource-group $resourceGroupName \
     --cluster-name $clusterName \
     --client-certificates /usr/csuser/clouddrive/rootCert.pem /usr/csuser/clouddrive/intermediateCert.pem
   ```


## Troubleshooting

If you encounter an error when applying permissions to your Virtual Network using Azure CLI, such as *Cannot find user or service principal in graph database for 'e5007d2c-4b13-4a74-9b6a-605d99f03501'*, you can apply the same permission manually from the Azure portal. Learn how to do this [here](add-service-principal.md).

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
