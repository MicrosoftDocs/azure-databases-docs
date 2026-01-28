---
title: Required Outbound Network Rules for Azure Managed Instance for Apache Cassandra
description: Learn about the required outbound network rules and FQDNs for Azure Managed Instance for Apache Cassandra.
author: seesharprun
ms.author: sidandrews
ms.service: azure-managed-instance-apache-cassandra
ms.topic: how-to
ms.date: 11/02/2021
---

# Required outbound network rules

Azure Managed Instance for Apache Cassandra requires certain network rules to properly manage the service. By ensuring that you have the proper rules exposed, you can keep your service secure and prevent operational issues.

> [!WARNING]
> Exercise caution when you apply changes to firewall rules for an existing cluster. For example, if rules aren't applied correctly, they might not be applied to existing connections, so it might appear that firewall changes didn't cause any problems. However, automatic updates of the Azure Managed Instance for Apache Cassandra nodes might fail later. Monitor connectivity after any major firewall updates for some time to ensure that there are no issues.

## Virtual network service tags

If you use a [virtual private network (VPN)](use-vpn.md), you don't need to open any other connection.

If you use Azure Firewall to restrict outbound access, we highly recommend that you use [virtual network service tags](/azure/virtual-network/service-tags-overview). The tags in the following table are required to make Azure SQL Managed Instance for Apache Cassandra function properly.

| Destination service tag                                                             | Protocol | Port    | Use  |
|----------------------------------------------------------------------------------|----------|---------|------|
| `Storage` | HTTPS | 443 | Required for secure communication between the nodes and Azure Storage for Control Plane communication and configuration.|
| `AzureKeyVault` | HTTPS | 443 | Required for secure communication between the nodes and Azure Key Vault. Certificates and keys are used to secure communication inside the cluster.|
| `EventHub` | HTTPS | 443 | Required to forward logs to Azure. |
| `AzureMonitor` | HTTPS | 443 | Required to forward metrics to Azure. |
| `AzureActiveDirectory`| HTTPS | 443 | Required for Microsoft Entra authentication.|
| `AzureResourceManager`| HTTPS | 443 | Required to gather information about and manage Cassandra nodes (for example, reboot).|
| `AzureFrontDoor.Firstparty`| HTTPS | 443 | Required for logging operations.|
| `GuestAndHybridManagement` | HTTPS | 443 | Required to gather information about and manage Cassandra nodes (for example, reboot). |
| `ApiManagement` | HTTPS | 443 | Required to gather information about and manage Cassandra nodes (for example, reboot). |

In addition to the tags table, you need to add the following address prefixes because a service tag doesn't exist for the relevant service:

- 104.40.0.0/13
- 13.104.0.0/14
- 40.64.0.0/10

## User-defined routes

If you're using a non-Microsoft firewall to restrict outbound access, we highly recommend that you configure [user-defined routes (UDRs)](/azure/virtual-network/virtual-networks-udr-overview#user-defined) for Microsoft address prefixes instead of attempting to allow connectivity through your own firewall. To add the required address prefixes in UDRs, see the [sample Bash script](https://github.com/Azure-Samples/cassandra-managed-instance-tools/blob/main/configureUDR.sh).

## Azure Global required network rules

The following table lists the required network rules and IP address dependencies.

| Destination endpoint                                                             | Protocol | Port    | Use  |
|----------------------------------------------------------------------------------|----------|---------|------|
|`snovap<region>.blob.core.windows.net:443`</br> Or</br> [ServiceTag](/azure/virtual-network/service-tags-overview#available-service-tags) - Azure Storage | HTTPS | 443 | Required for secure communication between the nodes and Azure Storage for Control Plane communication and configuration.|
|`*.store.core.windows.net:443`</br> Or</br> [ServiceTag](/azure/virtual-network/service-tags-overview#available-service-tags) - Azure Storage | HTTPS | 443 | Required for secure communication between the nodes and Azure Storage for Control Plane communication and configuration.|
|`*.blob.core.windows.net:443`</br> Or</br> [ServiceTag](/azure/virtual-network/service-tags-overview#available-service-tags) - Azure Storage | HTTPS | 443 | Required for secure communication between the nodes and Azure Storage to store backups. *Backup feature is being revised and a pattern for storage name follows by general availability.*|
|`vmc-p-<region>.vault.azure.net:443`</br> Or</br> [ServiceTag](/azure/virtual-network/service-tags-overview#available-service-tags) - Azure Key Vault | HTTPS | 443 | Required for secure communication between the nodes and Azure Key Vault. Certificates and keys are used to secure communication inside the cluster.|
|`management.azure.com:443`</br> Or</br> [ServiceTag](/azure/virtual-network/service-tags-overview#available-service-tags) - Azure Virtual Machine Scale Sets/Azure Management API | HTTPS | 443 | Required to gather information about and manage Cassandra nodes (for example, reboot).|
|`*.servicebus.windows.net:443`</br> Or</br> [ServiceTag](/azure/virtual-network/service-tags-overview#available-service-tags) - Azure Event Hubs | HTTPS | 443 | Required to forward logs to Azure.|
|`jarvis-west.dc.ad.msft.net:443`</br> Or</br> [ServiceTag](/azure/virtual-network/service-tags-overview#available-service-tags) - Azure Monitor | HTTPS | 443 | Required to forward metrics to Azure. |
|`login.microsoftonline.com:443`</br> Or</br> [ServiceTag](/azure/virtual-network/service-tags-overview#available-service-tags) - Microsoft Entra ID | HTTPS | 443 | Required for Microsoft Entra authentication.|
| `packages.microsoft.com` | HTTPS | 443 | Required for updates to Azure security scanner definition and signatures. |
| `azure.microsoft.com` | HTTPS | 443 | Required to get information about virtual machine scale sets. |
| `<region>-dsms.dsms.core.windows.net` | HTTPS | 443 | Certificate for logging. |
| `gcs.prod.monitoring.core.windows.net` | HTTPS | 443 | Logging endpoint needed for logging. |
| `global.prod.microsoftmetrics.com` | HTTPS | 443 | Needed for metrics. |
| `shavsalinuxscanpkg.blob.core.windows.net` | HTTPS | 443 | Needed to download/update security scanner. |
| `crl.microsoft.com` | HTTPS | 443 | Needed to access public Microsoft certificates. |
| `global-dsms.dsms.core.windows.net` | HTTPS | 443 | Needed to access public Microsoft certificates. |

### DNS access

The system uses Domain Name System (DNS) names to reach the Azure services described in this article so that it can use load balancers. For this reason, the virtual network must run a DNS server that can resolve those addresses. The virtual machines in the virtual network honor the name server that's communicated through the Dynamic Host Configuration Protocol.

In most cases, Azure automatically sets up a DNS server for the virtual network. If this action doesn't occur in your scenario, the DNS names that are described in this article are a good guide to get started.

## Internal port usage

The following ports are accessible only within the virtual network (or peered virtual networks/express routes). Instances of Azure Managed Instance for Apache Cassandra don't have a public IP and shouldn't be made accessible on the internet.

| Port | Use |
| ---- | --- |
| 8443 | Internal. |
| 9443 | Internal. |
| 7001 | Gossip: Used by Cassandra nodes to talk to each other. |
| 9042 | Cassandra: Used by clients to connect to Cassandra. |
| 7199 | Internal. |

## Related content

In this article, you learned about network rules to properly manage the service. Learn more about Azure SQL Managed Instance for Apache Cassandra with the following articles:

* [What is Azure Managed Instance for Apache Cassandra?](introduction.md)
* [Manage Azure Managed Instance for Apache Cassandra resources by using the Azure CLI](manage-resources-cli.md)
* [Use a VPN with Azure Managed Instance for Apache Cassandra](use-vpn.md)
