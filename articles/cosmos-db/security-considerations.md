---
title: Security considerations
description: Review considerations and best practices for securing your Azure Cosmos DB account including features that Microsoft implements for your account's security.
author: iriaosara
ms.author: iriaosara
ms.service: azure-cosmos-db
ms.topic: concept-article
ms.date: 10/02/2024
#Customer Intent: As a security architect, I want to review best practices and considerations, so that I can ensure my Azure Cosmos DB account is following the latest guidance for security.
---

# Security considerations in Azure Cosmos DB

Data security is a shared responsibility between you, the customer, and your database provider. Depending on the database provider you choose, the amount of responsibility you carry can vary. If you choose an on-premises solution, you need to provide everything from endpoint protection to physical security of your hardware, which is no easy task. If you choose a platform as a service (PaaS) cloud database provider, such as Azure Cosmos DB, your area of concern shrinks considerably.

For more information, see [shared responsibility in the cloud](/azure/security/fundamentals/shared-responsibility).

## Checklist

We recommend the following checklist of requirements on which to compare database systems:

- Network security and firewall settings
- User authentication and fine-grained user controls
- Ability to replicate data globally for regional failures
- Ability to fail over from one datacenter to another
- Local data replication within a datacenter
- Automatic data backups
- Restoration of deleted data from backups
- Ability to protect and isolate sensitive data
- Monitoring for attacks
- Built-in responses to attacks
- Ability to geo-fence data to adhere to data governance restrictions
- Physical protection of servers in protected datacenters
- Certifications

Although it might seem obvious, recent [large-scale database breaches](https://support.microsoft.com/topic/national-public-data-breach-what-you-need-to-know-843686f7-06e2-4e91-8a3f-ae30b7213535) remind us of the simple but critical importance of the following requirements:

- Patched servers that are kept up to date
- HTTPS by default/TLS encryption
- Administrative accounts with strong passwords

## How does Azure Cosmos DB secure my database?

Azure Cosmos DB secures your database by default with many features built-in to the service and Azure at large.

| Security requirement | Azure Cosmos DB's security approach |
| --- | --- |
| Network security | Using an IP firewall is the first layer of protection to secure your database. Azure Cosmos DB supports policy-driven IP-based access controls for inbound firewall support. The IP-based access controls are similar to the firewall rules used by traditional database systems. However, they're expanded so that an Azure Cosmos DB database account is only accessible from an approved set of machines or cloud services. To learn more, see [Azure Cosmos DB firewall support](how-to-configure-firewall.md). With Azure Cosmos DB, you can enable a specific IP address (168.61.48.0), an IP range (168.61.48.0/8), and combinations of IPs and ranges. Azure Cosmos DB blocks all requests that originate from machines outside this allowed list. Requests from approved machines and cloud services then must complete the authentication process to be given access control to the resources. You can use [virtual network service tags](/azure/virtual-network/service-tags-overview) to achieve network isolation and protect your Azure Cosmos DB resources from the general internet. Use service tags in place of specific IP addresses when you create security rules. By specifying the service tag name (for example, `AzureCosmosDB`) in the appropriate source or destination field of a rule, you can allow or deny the traffic for the corresponding service. |
| Authorization | Azure Cosmos DB uses hash-based message authentication code (HMAC) for authorization. Each request is hashed by using the secret account key, and the subsequent base-64 encoded hash is sent with each call to Azure Cosmos DB. To validate the request, Azure Cosmos DB uses the correct secret key and properties to generate a hash, and then it compares the value with the one in the request. If the two values match, the operation is authorized successfully and the request is processed. If they don't match, there's an authorization failure and the request is rejected. You can use a primary key, allowing fine-grained access to a resource such as a document. To learn more, see [Secure access to Azure Cosmos DB resources](secure-access-to-data.md). |
| Users and permissions | By using the primary key for the account, you can create user resources and permission resources per database. A resource token is associated with a permission in a database and determines whether the user has access (read-write, read-only, or no access) to an application resource in the database. Application resources include containers, documents, attachments, stored procedures, triggers, and user defined functions (UDFs). The resource token is then used during authentication to provide or deny access to the resource. To learn more, see [Secure access to Azure Cosmos DB resources](secure-access-to-data.md). |
| Active Directory integration (Azure role-based access control) | You can also provide or restrict access to the Azure Cosmos DB account, database, container, and offers (throughput) by using access control (IAM) in the Azure portal. IAM provides role-based access control and integrates with Active Directory. You can use built-in roles or custom roles for individuals and groups. |
| Global replication | Azure Cosmos DB offers turnkey global distribution, which enables you to replicate your data to any one of Azure's worldwide datacenters in a turnkey way. Global replication lets you scale globally and provide low-latency access to your data around the world. In the context of security, global replication ensures data protection against regional failures. To learn more, see [Distribute data globally](distribute-data-globally.md). |
| Regional failovers | If you replicate your data in more than one datacenter, Azure Cosmos DB automatically rolls over your operations if a regional datacenter goes offline. You can create a prioritized list of failover regions by using the regions in which your data is replicated. To learn more, see [Regional failovers in Azure Cosmos DB](high-availability.md). |
| Local replication | Even within a single datacenter, Azure Cosmos DB automatically replicates data for high availability, giving you the choice of [consistency levels](consistency-levels.md). This replication guarantees a 99.99% [availability service level agreement (SLA)](https://azure.microsoft.com/support/legal/sla/cosmos-db) for all single region accounts and all multi-region accounts with relaxed consistency, and 99.999% read availability on all multi-region database accounts. |
| Automated online backups | Azure Cosmos DB databases are backed up regularly and stored in a geo-redundant store. To learn more, see [Automatic online backup and restore with Azure Cosmos DB](online-backup-and-restore.md). |
| Restore deleted data | You can use the automated online backups to recover data accidentally deleted up to ~30 days after the event. To learn more, see [Automatic online backup and restore with Azure Cosmos DB](online-backup-and-restore.md). |
| Protect and isolate sensitive data | All data in the regions listed in What's new? is now encrypted at rest. Personal data and other confidential data can be isolated to specific containers and read-write, or read-only access can be limited to specific users. |
| Monitor for attacks | By using [audit logging and activity logs](./monitor.md), you can monitor your account for normal and abnormal activity. You can view what operations were performed on your resources. This data includes who initiated the operation, when the operation occurred, the status of the operation, and much more. |
| Respond to attacks | After you contact Azure support to report a potential attack, a five-step incident response process begins. The goal is to restore normal service security and operations. The process restores services as quickly as possible after an issue is detected and an investigation is started. To learn more, see [Microsoft Azure security response in the cloud](https://azure.microsoft.com/resources/shared-responsibilities-for-cloud-computing/). |
| Geo-fencing | Azure Cosmos DB ensures data governance for sovereign regions (for example, Germany, China, and US Government). |
| Protected facilities | Data in Azure Cosmos DB is stored on solid state drives in Azure's protected datacenters. To learn more, see [Microsoft global datacenters](https://www.microsoft.com/cloud-platform/global-datacenters). |
| HTTPS & TLS encryption | All connections to Azure Cosmos DB support HTTPS. Azure Cosmos DB supports Transport Layer Security (TLS) levels up to 1.2 (included). It's possible to enforce a minimum TLS level on the server side. To do so, see the self-service guide [Self-serve minimum TLS version enforcement in Azure Cosmos DB](./self-serve-minimum-tls-enforcement.md). |
| Encryption at rest | All data stored in Azure Cosmos DB is encrypted at rest. Learn more in [Azure Cosmos DB encryption at rest](./database-encryption-at-rest.md). |
| Patched servers | As a managed database, Azure Cosmos DB automatically patches and manages server on your behalf eliminating the need for manual maintenance tasks. |
| Administrative accounts with strong passwords | It's impossible to have an administrative account with no password in Azure Cosmos DB. Security via TLS and HMAC secret-based authentication is baked in by default. |
| Security and data protection certifications | For the most up-to-date list of certifications, see [Azure compliance](https://www.microsoft.com/trustcenter/compliance/complianceofferings) and the latest [Azure compliance document](https://download.microsoft.com/download/1/E/9/1E94186C-EACA-4632-8DDF-D546C8482073/AzureTrustedCloud-Compliance.pdf) with all Azure certifications, including Azure Cosmos DB. |

## Related content

- [Well Architected Framework security guidance](/azure/well-architected/service-guides/cosmos-db#security)
- [Security baseline](/security/benchmark/azure/baselines/azure-cosmos-db-security-baseline)
