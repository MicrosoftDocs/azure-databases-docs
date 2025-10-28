---
title: Security Best Practices
titleSuffix: Azure Database Migration Service
description: Learn how to use the security measures provided by SQL Server and the Azure infrastructure to secure your migration from SQL Server to an Azure SQL product.
author: abhims14
ms.author: abhishekum
ms.reviewer: mathoma, randolphwest
ms.date: 10/28/2025
ms.service: azure-database-migration-service
ms.topic: how-to
---

# Security best practices - Azure Database Migration Service

This article contains general security best practices to follow when you migrate SQL Server databases to an Azure SQL product with Azure Database Migration Service (Azure DMS). In this article, you learn how to take advantage of security measures in SQL Server and the Azure infrastructure to secure your migration, including best practices for the source SQL Server, network, Azure Blob storage, and target Azure SQL offerings.

This article covers the following migration scenarios from SQL Server (on-premises or other clouds) to:

- Azure SQL Managed Instance
- SQL Server on Azure Virtual Machines (VMs)
- Azure SQL Database

This guide is intended for customers with questions about securely migrating to an Azure SQL product, such as database and security architects, database managers and administrators, and IT teams part of migration projects.

The work in this article is ongoing. You can provide feedback or corrections using the **Feedback** option at the end of this article.

## Source SQL Server

Consider the following security best practices for your source SQL Server:

- Encrypt data-at-rest with [Transparent data encryption (TDE)](/sql/relational-databases/security/encryption/transparent-data-encryption) for your database backups, to mitigate the risks associated with unauthorized data access, especially when migrating over the Internet. You can also [encrypt data at rest for other Azure resources](/azure/security/fundamentals/encryption-atrest).

- Use [Windows Authentication](/sql/relational-databases/security/choose-an-authentication-mode#connecting-through-windows-authentication) with Active Directory to access source or local backup file shares. Active Directory provides central management of logins that simplifies permission management.

- Follow the *principle of least privilege* to grant users the minimal granular permissions and server roles necessary to complete the tasks. For example:

  - When you migrate to Azure SQL Managed Instance or SQL Server on Azure VMs, the login that connects to the source SQL Server instance should have `CONTROL SERVER` permission.

  - When you migrate to Azure SQL Database, the login that connects to the source SQL Server instance should be a member of the **db_datareader** role.

## Network

Consider the following security best practices for your network:

- All data-in-transit transmitted by Azure DMS is protected with TLS 1.2 encryption by default.

- For data moving between your source infrastructure and Azure, consider appropriate safeguards such as HTTPS or VPN. When sending traffic between an Azure virtual network and an on-premises location over the public internet, use the encrypted [Site-to-site VPN](/azure/vpn-gateway/tutorial-site-to-site-portal). The site-to-site VPN connection is a trusted, reliable, and established technology, but the connection takes place over the internet, and bandwidth is constrained to a maximum of about 1.25 Gbps.

- Use [ExpressRoute](/azure/expressroute/expressroute-introduction) to migrate larger data sets. ExpressRoute offers greater reliability, faster speeds, consistent latencies, and a higher security footprint for connections since they don't go over the public internet.

- For migrations to Azure SQL Database, use [IP firewall rules](/azure/azure-sql/database/firewall-configure) to restrict access to only authorized IP addresses.

## Azure Blob storage

Consider the following security best practices for Azure Blob storage:

- All interactions with Azure Storage through the Azure portal should occur via HTTPS. Use [Require secure transfer](/azure/storage/common/storage-require-secure-transfer) to enforce HTTPS connections for your storage account.

- Configure Azure DMS access to Azure blob storage using a [Shared Access Signature (SAS) token](/azure/storage/common/storage-sas-overview) with limited privileges, to have granular control over the permissions granted to the Azure DMS service.

- Azure DMS supports private endpoint for Azure blob storage while copying the backup from local file share on-premises to Azure blob storage. If private endpoints aren't an option, public endpoints are used for communication between service layers.

For more information, see [Security recommendations for Azure Blob storage](/azure/storage/blobs/security-recommendations).

## Target Azure SQL product

Consider the following security best practices for your target Azure SQL product:

- Follow the principle of least privilege to grant the minimal granular permissions. When using Azure Database Migration Service, you can configure custom roles to limit the permissions granted to the Azure Database Migration Service service.

  For example:

  - [Custom roles for Azure SQL Managed Instance](/data-migration/sql-server/managed-instance/custom-roles)
  - [Custom roles for SQL Server on Azure VMs](/data-migration/sql-server/virtual-machines/custom-roles)
  - [Custom roles for Azure SQL Database](/data-migration/sql-server/database/custom-roles)

- Review the following security guides to learn how to secure your Azure SQL products:

  - [SQL Server on Azure VMs](/azure/azure-sql/virtual-machines/windows/security-considerations-best-practices)
  - [Azure SQL Database & Azure SQL Managed Instance](/azure/azure-sql/database/security-best-practice)

## Related content

- [What is Azure Database Migration Service?](dms-overview.md)
- [SQL Server security best practices](/sql/relational-databases/security/sql-server-security-best-practices)
- [Security considerations for SQL Server on Azure Virtual Machines](/azure/azure-sql/virtual-machines/windows/security-considerations-best-practices)
- [Playbook for addressing common security requirements with Azure SQL Database and Azure SQL Managed Instance](/azure/azure-sql/database/security-best-practice)
