---
title: "Migrate MySQL On-Premises to Azure Database for MySQL: Security"
description: "Moving to a cloud-based service doesn’t mean the entire internet has access to it always."
author: SudheeshGH
ms.author: sunaray
ms.reviewer: maghan
ms.date: 11/27/2024
ms.service: azure-database-mysql
ms.subservice: migration-guide
ms.topic: how-to
---

# Migrate MySQL on-premises to Azure Database for MySQL: Security

Ensuring robust security is paramount when migrating MySQL databases from on-premises environments to Azure Database for MySQL. This article delves into the critical security considerations and best practices to safeguard your data throughout migration. By using Azure's comprehensive security features, such as advanced threat protection, encryption, and access controls, you can protect your databases against potential vulnerabilities and threats. This guide provides the insights needed to implement a secure migration strategy, addressing critical aspects like data encryption, network security, and compliance. Whether you aim to enhance data protection, meet regulatory requirements, or ensure the integrity of your databases, this article equips you with the knowledge to achieve a secure and successful migration.

## Prerequisites

[Migrate MySQL on-premises to Azure Database for MySQL: Business Continuity and Disaster Recovery (BCDR)](12-business-continuity-and-disaster-recovery.md)

## Overview

Moving to a cloud-based service doesn't mean the entire internet has access to it always. Azure provides best in class security that ensures data workloads are continually protected from bad actors and rouge programs.

## Authentication

Azure Database for MySQL supports the basic authentication mechanisms for MySQL user connectivity, but also supports [integration with Microsoft Entra ID](../../concepts-azure-ad-authentication.md). This security integration works by issuing tokens that act like passwords during the MySQL login process. [Configuring Active Directory integration](../../howto-configure-sign-in-azure-ad-authentication.md) is incredibly simple to do and supports not only users, but Microsoft Entra groups as well.

This tight integration allows administrators and applications to take advantage of the enhanced security features of [Azure Identity Protection](/azure/active-directory/identity-protection/overview-identity-protection) to surface any identity issues.

> [!NOTE]  
> This security feature is supported by MySQL 5.7 and later. Most [application drivers](../../howto-configure-sign-in-azure-ad-authentication.md) are supported as long as the `clear-text` option is provided.

## Threat protection

If a user or application credentials are compromised, logs aren't likely to reflect any failed login attempts. Compromised credentials can allow bad actors to access and download the data. [Azure Threat Protection](../../concepts-security.md#threat-protection) can watch for anomalies in logins (such as unusual locations, rare users or brute force attacks) and other suspicious activities. Administrators can be notified in the event something doesn't `look` right.

## Audit logging

MySQL has a robust built-in audit log feature. By default, this [audit log feature is disabled](../../concepts-audit-logs.md) in Azure Database for MySQL. Server level logging can be enabled by changing the `audit\_log\_enabled` server parameter. Once enabled, logs can be accessed through [Azure Monitor](/azure/azure-monitor/overview) and [Log Analytics](/azure/azure-monitor/logs/log-analytics-workspace-overview) by turning on [diagnostic logging.](../../howto-configure-audit-logs-portal.md#set-up-diagnostic-logs)

To query for user connection-related events, run the following KQL query:

```bash
AzureDiagnostics
| where ResourceProvider =="MICROSOFT.DBFORMYSQL"
| where Category == 'MySqlAuditLogs' and event\_class\_s == "connection\_log"
| project TimeGenerated, LogicalServerName\_s, event\_class\_s, event\_subclass\_s
, event\_time\_t, user\_s , ip\_s , sql\_text\_s
| order by TimeGenerated asc
```

## Encryption

Data in the MySQL instance is encrypted at rest by default. Any automated backups are also encrypted to prevent potential leakage of data to unauthorized parties. This encryption is typically performed with a key that is created when the instance is created. In addition to this default encryption key, administrators have the option to [bring your own key (BYOK).](../../concepts-data-encryption-mysql.md)

When using a customer-managed key strategy, it's vital to understand responsibilities around key lifecycle management. Customer keys are stored in an [Azure Key Vault](/azure/key-vault/general/basic-concepts) and then accessed via policies. It's vital to follow all recommendations for key management, the loss of the encryption key equates to the loss of data access.

In addition to a customer-managed key, use service-level keys to [add double encryption](../../concepts-infrastructure-double-encryption.md). Implementing this feature can provide highly encrypted data at rest, but it does come with encryption performance penalties. Testing should be performed.

Data can be encrypted during transit using SSL/TLS. As previously discussed, it might be necessary to [modify your applications](../../howto-configure-ssl.md) to support this change and also configure the appropriate TLS validation settings.

## Firewall

Once users are set up and the data is encrypted at rest, the migration team should review the network data flows. Azure Database for MySQL provides several mechanisms to secure the networking layers by limiting access to only authorized users, applications, and devices.

The frontline of defense for protecting the MySQL instance is to implement [firewall rules](../../concepts-firewall-rules.md). IP addresses can be limited to only valid locations when accessing the instance via internal or external IPs. If the MySQL instance is destined to only serve internal applications, then [restrict public access](../../howto-deny-public-network-access.md).

When moving an application to Azure along with the MySQL workload, it's likely there are been multiple virtual networks setup in a hub and spoke pattern that requires [Virtual Network Peering](/azure/virtual-network/virtual-network-peering-overview) to be configured.

## Private link

To limit access to the Azure Database for MySQL to internal Azure resources, enable [Private Link](../../concepts-data-access-security-private-link.md). Private Link ensures that the MySQL instance is assigned a private IP rather than a public IP address.

> [!NOTE]  
> There are many other [basic Azure Networking considerations](../../concepts-data-access-and-security-vnet.md) that must be taken into account that are not the focus of this guide.

Review a set of potential [security baseline](/azure/mysql/security-baseline) tasks that can be implemented across all Azure resources. Not all of the items described on the reference link apply to the specific data workloads or Azure resources.

## Security checklist

  - Use Microsoft Entra authentication where possible.

  - Enable Advanced Thread Protection.

  - Enable all auditing features.

  - Consider a Bring-Your-Own-Key (BYOK) strategy.

  - Implement firewall rules.

  - Utilize private endpoints for workloads that don't travel over the Internet.

## Next step

> [!div class="nextstepaction"]
> [Migrate MySQL on-premises to Azure Database for MySQL: Summary](14-summary.md)
