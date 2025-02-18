---
title: |
  Tutorial: Azure Cosmos DB for MongoDB vCore: Setting Up AKS and Standalone VMs 
titleSuffix: Azure Cosmos DB for MongoDB (vCore)
description: In this tutorial, we cover integrating Azure Cosmos DB for MongoDB vCore with advanced Azure services, including Azure Kubernetes Service (AKS) and Standalone Virtual Machines (VMs). It covers prerequisites, setup instructions, and deployment strategies for both services. The guide is designed to assist developers and IT professionals in efficiently managing containerized and virtualized environments to enhance database functionality and system scalability.
author: v-smedapati
ms.author: v-smedapati
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: tutorial
ms.date: 11/29/2024
# CustomerIntent: As a developer, I need to set up Azure resources like AKS or Standalone VMs to integrate with Azure Cosmos DB for MongoDB vCore, focusing on scalable deployments, secure connections, and efficient resource management.
---

# Additional Prerequisites on Azure (Stretch)
When working with Azure Cosmos DB for MongoDB vCore, certain Azure infrastructure components may be required to support deployments in different environments. This document details the prerequisites and setup steps for two critical Azure-based deployments:

1. **Azure Kubernetes Service (AKS)**

1. **Standalone Virtual Machines (VMs)**

These prerequisites ensure a stable and efficient deployment of MongoDB vCore, providing scalability, security, and operational efficiency.

## Azure Kubernetes Service (AKS)
Azure Kubernetes Service (AKS) is a managed Kubernetes service that simplifies deploying, managing, and scaling containerized applications using Kubernetes on Azure.

### Prerequisites

Before setting up Cosmos DB for MongoDB vCore on AKS, ensure the following requirements are met:

- **Azure Subscription** with appropriate permissions to create and manage resources.
- **Azure CLI** installed and authenticated.
- **Kubernetes CLI (kubectl)** installed.
- **Helm** installed (for deploying MongoDB client applications if needed).
- **A Virtual Network (VNet)** for AKS cluster networking.
- **Azure Container Registry (optional)** for storing container images.

### Deployment Steps

1. **Create an AKS Cluster**

      ```bash
      az aks create --resource-group <ResourceGroupName> \
        --name <AKSClusterName> \
        --node-count 3 \
        --enable-addons monitoring \
        --generate-ssh-keys
      ```  
    - Replace `<ResourceGroupName>` with your Azure resource group.
    - Replace `<AKSClusterName>` with your desired AKS cluster name.

1. **Get AKS Credentials**
      ```bash
      az aks get-credentials --resource-group <ResourceGroupName> --name <AKSClusterName>
      ```  
    - This command allows you to interact with the AKS cluster using `kubectl`.

1. **Deploy MongoDB Client Applications (Optional)**
    - If you need a MongoDB client inside the cluster, use Helm.
      ```bash
      helm repo add bitnami https://charts.bitnami.com/bitnami
      helm install my-mongo-client bitnami/mongodb --set architecture=standalone
      ```
    
    - This installs a standalone MongoDB client inside the AKS cluster.

1. **Configure Network Policies**
    - Ensure AKS nodes can communicate with Azure Cosmos DB:
      ```bash
        az network nsg rule create --resource-group <ResourceGroupName> \
        --nsg-name <NSGName> --name AllowCosmosDB \
        --priority 100 --direction Outbound \
        --destination-address-prefixes "<CosmosDB IP>" \
        --destination-port-ranges 10255 \
        --access Allow --protocol Tcp
      ```
    
    - Replace `<CosmosDB IP>` with the actual IP address of your Cosmos DB instance.  

## Standalone Virtual Machines (VMs)
For scenarios where AKS is not required, standalone Virtual Machines (VMs) provide a flexible and straightforward way to deploy and manage MongoDB applications connecting to Azure Cosmos DB.

### Prerequisites

Before setting up standalone VMs, ensure:

- **Azure Subscription** is available.
- **Virtual Network (VNet) and Subnet** for VM network configuration.
- **SSH access (for Linux VMs) or RDP access (for Windows VMs).**
- **Firewall rules allow outbound connections to Cosmos DB.**
- **MongoDB client installed on VM.**

### Deployment Steps
1. **Create a Virtual Machine**

    - **For Linux VM:**

      ```bash
      az vm create --resource-group <ResourceGroupName> \
        --name <VMName> --image UbuntuLTS \
        --admin-username azureuser \
        --generate-ssh-keys
      ```
    - **For Windows VM:**

      ```bash
      az vm create --resource-group <ResourceGroupName> \
        --name <VMName> --image Win2022Datacenter \
        --admin-username azureuser \
        --admin-password <YourPassword>
      ```
1. Install MongoDB Client

    - **For Linux VM:**

      ```bash
      sudo apt update && sudo apt install -y mongodb-clients
      ```
    - **For Windows VM:**

      - Download the MongoDB shell from MongoDB Official Site.
      - Install and configure the MongoDB shell.


1. **Configure Firewall Rules**

    - Ensure outbound access to Cosmos DB for MongoDB vCore:

      ```bash
      az network nsg rule create --resource-group <ResourceGroupName> \
        --nsg-name <NSGName> --name AllowCosmosDB \
        --priority 100 --direction Outbound \
        --destination-address-prefixes "<CosmosDB IP>" \
        --destination-port-ranges 10255 \
        --access Allow --protocol Tcp
      ```

1. **Connect to Cosmos DB**

    - Use the MongoDB shell or a programming language of choice to connect:

      ```shell
      mongosh "mongodb+srv://<username>:<password>@<cosmosdb-host>/?retryWrites=true&w=majority"
      ```

## Conclusion 

Deploying Azure Cosmos DB for MongoDB vCore on AKS or Standalone VMs provides flexibility based on different infrastructure requirements.

- **AKS** is recommended for scalable and managed containerized workloads.

- **Standalone VMs** are ideal for simpler, direct-hosted applications requiring minimal orchestration.

Both approaches require proper network configurations and client installations to ensure smooth connectivity to Azure Cosmos DB.
