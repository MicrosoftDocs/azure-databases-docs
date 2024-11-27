---
title: Security options and features
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: Learn how Azure Cosmos DB for MongoDB vCore provides database protection and data security for your data.
author: khelanmodi
ms.author: khelanmodi
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.custom:
  - ignite-2024
ms.topic: conceptual
ms.date: 11/25/2023
---

# Overview of database security in Azure Cosmos DB for MongoDB vCore

[!INCLUDE[MongoDB vCore](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

This article discusses database security best practices and key features offered by Azure Cosmos DB for MongoDB vCore to help you prevent, detect, and respond to database breaches.

## What's new in Azure Cosmos DB for MongoDB vCore security

Encryption at rest is now available for documents and backups stored in Azure Cosmos DB for MongoDB vCore in most Azure regions. Encryption at rest is applied automatically for both new and existing customers in these regions. There's no need to configure anything. You get the same great latency, throughput, availability, and functionality as before with the benefit of knowing your data is safe and secure with encryption at rest.  Data stored in your Azure Cosmos DB for MongoDB vCore cluster is automatically and seamlessly encrypted with keys managed by Microsoft using service-managed keys. 

## How do I secure my database

Data security is a shared responsibility between you, the customer, and your database provider. Depending on the database provider you choose, the amount of responsibility you carry can vary. If you choose an on-premises solution, you need to provide everything from end-point protection to physical security of your hardware - which is no easy task. If you choose a PaaS cloud database provider such as Azure Cosmos DB, your area of concern shrinks considerably. The following image, borrowed from Microsoft's [Shared Responsibilities for Cloud Computing](https://azure.microsoft.com/resources/shared-responsibilities-for-cloud-computing/) white paper, shows how your responsibility decreases with a PaaS provider like Azure Cosmos DB.

:::image type="content" source="./media/database-security/nosql-database-security-responsibilities.png" alt-text="Screenshot of customer and database provider responsibilities.":::

The preceding diagram shows high-level cloud security components, but what items do you need to worry about specifically for your database solution? And how can you compare solutions to each other?

We recommend the following checklist of requirements on which to compare database systems:

- Network security and firewall settings
- User authentication and fine grained user controls
- Ability to replicate data globally for regional failures
- Ability to fail over from one data center to another
- Local data replication within a data center
- Automatic data backups
- Restoration of deleted data from backups
- Protect and isolate sensitive data
- Monitoring for attacks
- Responding to attacks
- Ability to geo-fence data to adhere to data governance restrictions
- Physical protection of servers in protected data centers
- Certifications

And although it may seem obvious, recent [large-scale database breaches](https://thehackernews.com/2017/01/mongodb-database-security.html) remind us of the simple but critical importance of the following requirements:

- Patched servers that are kept up-to-date
- HTTPS by default/TLS encryption
- Administrative accounts with strong passwords

## How does Azure Cosmos DB secure my database

Azure Cosmos DB for MongoDB vCore seamlessly fulfills each and every one of those security requirements.

Let's dig into each one in detail.

|Security requirement|Azure Cosmos DB's security approach|
|---|---|
|Network security|Private access implmeneted via [the mature Private Link technology](https://learn.microsoft.com/azure/private-link/private-link-overview) allows to provide access to cluster for resources in Azure VNets. Public access allows to open cluster to a defined set of public IP addresses. Private and public access can be combined and enabled or disabled at any time.
**Default configuration**: Azure Cosmos DB for MongoDB vCore clusters are created locked down by default. To provide access to the cluster, networking settings should be updated to enable private and/or public access to cluster during cluster creation or after it.
[**Private access**](./how-to-private-link.md): With private access enabled a private endpoint could be created to access privately cluster from within Azure virtual network. Private endpoint is created in a specified VNet's subnet. Once done, all [Azure virtual network capabilities](https://learn.microsoft.com/azure/virtual-network/concepts-and-best-practices) are available to the cluster including local and global virtual network peering, access to private on-prem environments, filtering and routing of network traffic, and others. 
[**Public access**](#firewall-overview): Using an IP firewall is the first layer of protection to secure your database. Azure Cosmos DB for MongoDB vCore supports policy driven IP-based access controls for inbound firewall support. The IP-based access controls are similar to the firewall rules used by traditional database systems. However, they're expanded so that an Azure Cosmos DB for MongoDB vCore cluster is only accessible from an approved set of machines or cloud services. <br><br>Azure Cosmos DB for MongoDB vCore enables you to add a specific IP address (168.61.48.0), an IP range (168.61.48.0/8), and combinations of IPs and ranges. <br><br>All requests originating from machines outside this allowed list are blocked by Azure Cosmos DB for MongoDB vCore. Requests from approved machines and cloud services then must complete the authentication process to be given access control to the resources.<br><br>|
|Local replication|Even within a single region, Azure Cosmos DB for MongoDB vCore replicates the data on storage level maintaining 3 synchronous replicas of each physical shard transparently at all times. 
HA-enabled clusters have another layer of replication between each primary and standby physical shard pair. [High availability](./high-availability.md) replication is synchronous and provides zero data loss on failovers thus guaranteeing a 99.99% [monthly availability SLA for single region setup](https://azure.microsoft.com/support/legal/sla/cosmos-db).|
|Global replication|Azure Cosmos DB for MongoDB vCore offers [cross-region replication](./cross-region-replication.md) which enables you to replicate your data to another Azure region. Global replication lets you scale globally and provide low-latency access to your data around the world. In the context of security, global replication ensures data protection against infrequent regional outages. With cross-region replica cluster a copy of your data is always present in another region. The replica in another region combined with high-availability provide a 99.995% [monthly availability SLA for multi-region setup](https://azure.microsoft.com/support/legal/sla/cosmos-db).|
|Database isolation|Azure Cosmos DB for MongoDB vCore databases are hosted on their own dedicated resources. It means that each cluster gets its own dedicated node called physical shard or a few in a multishard configuration. Each physical shard has its own compute and remote storage attached to it. There's no sharing of infrastructure between clusters providing an extra layer of physical and logical isolation for your database.|
|Automated cluster backups|Backup for Azure Cosmos DB for MongoDB vCore clusters is enabled at cluster creation time, is fully automated, and can't be disabled. [Restore](./how-to-restore-cluster.md) is provided to any timestamp within 35 day backup retention period.|
|Restore *deleted* data|The automated online backups can be used to recover data you may have accidentally deleted up to ~7 days after the event.|
|HTTPS/SSL/TLS encryption|All network communications with Azure Cosmos DB for MongoDB vCore clusters are encrypted. Only connections via a MongoDB client are accepted and encryption is always enforced. Whenever data is written to Azure Cosmos DB for MongoDB vCore, your data is encrypted in-transit. Data encryption supports TLS levels up to 1.3 (included).|
|Encryption at rest|Azure Cosmos DB for MongoDB vCore data, including all backups, are encrypted on disk, including the temporary files. The service uses the AES 256-bit cipher included in Azure storage encryption, and the keys are system-managed. Storage encryption is always on, and can't be disabled.|
|Monitor for attacks|By using [audit logging](./how-to-monitor-diagnostics-logs.md) and [activity logs](https://learn.microsoft.com/azure/azure-monitor/essentials/activity-log-insights), you can monitor your database for normal and abnormal activity. You can view what operations were performed on your resources. This data includes who initiated the operation, when the operation occurred, the status of the operation, and much more.|
|Respond to attacks|Once you have contacted Azure support to report a potential attack, a five-step incident response process is kicked off. The goal of the five-step process is to restore normal service security and operations. The five-step process restores services as quickly as possible after an issue is detected and an investigation is started.<br><br>Learn more in [Microsoft Azure Security Response in the Cloud](https://azure.microsoft.com/resources/shared-responsibilities-for-cloud-computing/).|
|Protected facilities|Data in Azure Cosmos DB for MongoDB vCore is stored in Azure's protected data centers.<br><br>Learn more in [Microsoft global datacenters](https://www.microsoft.com/cloud-platform/global-datacenters)|
|Patched servers|Azure Cosmos DB for MongoDB vCore eliminates the need to manage software updates and patch clusters, that's done for you automatically.|
|Administrative accounts with strong passwords|It's hard to believe we even need to mention this requirement, but unlike some of our competitors, it's impossible to have an administrative account with no password in Azure Cosmos DB for MongoDB vCore. The password should be at least 8 characters long, include English uppercase and lowercase lettes, numbers, and non-alphanumeric characters.<br><br> Security via TLS secret based authentication is baked in by default.|
|Security and data protection certifications| For the most up-to-date list of certifications, see [Azure compliance](https://www.microsoft.com/trustcenter/compliance/complianceofferings) and the latest [Azure compliance document](https://servicetrust.microsoft.com/DocumentPage/7adf2d9e-d7b5-4e71-bad8-713e6a183cf3) with all Azure certifications including Azure Cosmos DB.|

The following screenshot shows how you can use audit logging and activity logs to monitor your account: 
:::image type="content" source="./media/database-security/nosql-database-security-application-logging.png" alt-text="Screenshot of activity logs for Azure Cosmos DB.":::

## Network security options

This section outlines various network security options you can configure for your cluster.

### No access

**No Access** is the default option for a newly created cluster if public or private access isn't enabled. In this case, no computers, whether inside or outside of Azure, can connect to the database nodes.

### Public IP access with firewall

In the public access option, a public IP address is assigned to the cluster, and access to the cluster is protected by a firewall.

## Firewall overview

Azure Cosmos DB for MongoDB vCore uses a server-level firewall to prevent all access to your cluster until you specify which computers have permission. The firewall grants access to the cluster based on the originating IP address of each request. To configure your firewall, you create firewall rules that specify ranges of acceptable IP addresses.

Firewall rules enable clients to access your cluster and all the databases within it. Server-level firewall rules can be configured using the Azure portal or programmatically using Azure tools such as the Azure CLI.

By default, the firewall blocks all access to your cluster. To begin using your cluster from another computer, you need to specify one or more server-level firewall rules to enable access to your cluster. Use the firewall rules to specify which IP address ranges from the Internet to allow. Firewall rules don't affect access to the Azure portal website itself. Connection attempts from the internet and Azure must first pass through the firewall before they can reach your databases. In addition to firewall rules, private link access that can be used for a private IP just for the Azure Cosmos DB for MongoDB vCore cluster.

## Next steps

> [!div class="nextstepaction"]
> [Migrate MongoDB data to Azure Cosmos DB for MongoDB vCore](migration-options.md)
