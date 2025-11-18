---
title: Secure your cluster
description: Learn how to secure Azure DocumentDB clusters with best practices for data and network protection. Strengthen security and prevent breaches.
author: seesharprun
ms.author: sidandrews
ms.reviewer: skhera
ms.topic: best-practice
ms.date: 09/29/2025
ms.custom:
  - security-horizontal-2025
ai-usage: ai-generated
---

# Secure your Azure DocumentDB cluster

Azure DocumentDB is a fully managed NoSQL database service designed for high-performance, mission-critical applications. Securing your Azure DocumentDB cluster is essential to protect your data and network.

This article explains best practices and key features to help you prevent, detect, and respond to database breaches.

## Network security

- **Restrict access using private endpoints and firewall rules**: By default, clusters are locked down. Control which resources can connect to your cluster by enabling private access via Private Link or public access with IP-based firewall rules. For more information, see [how to enable private access](how-to-private-link.md) and [how to enable public access](how-to-public-access.md).

- **Combine public and private access as needed**: You can configure both public and private access options on your cluster and change them at any time to meet your security requirements. For more information, see [network configuration options](how-to-private-link.md).

## Identity management

- **Use managed identities to access your account from other Azure services**: Managed identities eliminate the need to manage credentials by providing an automatically managed identity in Microsoft Entra ID. Use managed identities to securely access Azure DocumentDB from other Azure services without embedding credentials in your code. For more information, see [Managed identities for Azure resources](/entra/identity/managed-identities-azure-resources/overview).

- **Use Azure control plane role-based access control to manage account databases and collections**: Apply Azure role-based access control to define fine-grained permissions for managing Azure DocumentDB clusters, databases, and collections. This control ensures that only authorized users or services can perform administrative operations.

- **Use native data plane role-based access control to query, create, and access items within a container**: Implement data plane role-based access control to enforce least privilege access for querying, creating, and accessing items within Azure DocumentDB collections. This control helps secure your data operations. For more information, see [Grant data plane access](how-to-connect-role-based-access-control.md).

- **Separate the Azure identities used for data and control plane access**: Use distinct Azure identities for control plane and data plane operations to reduce the risk of privilege escalation and ensure better access control. This separation enhances security by limiting the scope of each identity.

- **Use strong passwords for administrative clusters**: Administrative clusters require strong passwords with at least eight characters, including uppercase, lowercase, numbers, and nonalphanumeric characters. Strong passwords prevent unauthorized access. For more information, see [how to manage users](secondary-users.md).

- **Create secondary user clusters for granular access**: Assign read-write or read-only privileges to secondary user clusters for more granular access control on your cluster's databases. For more information, see [how to create secondary users](secondary-users.md).

## Transport security

- **Enforce transport layer security encryption for all connections**: All network communications with Azure DocumentDB clusters are encrypted in transit using transport layer security (TLS) up to 1.3. Only connections via a MongoDB client are accepted, and encryption is always enforced. For more information, see [how to connect securely](how-to-connect-mongo-shell.md).

- **Use HTTPS for management and monitoring**: Ensure that all management and monitoring operations are performed over HTTPS to protect sensitive information. For more information, see [how to monitor diagnostics logs](how-to-monitor-diagnostics-logs.md).

## Data encryption

- **Encrypt data at rest using service-managed or customer-managed keys**: All data, backups, logs, and temporary files are encrypted on disk using Advanced Encryption Standard (AES) 256-bit encryption. You can use service-managed keys by default or configure customer-managed keys for greater control. For more information, see [how to configure data encryption](how-to-data-encryption.md).

- **Use baseline encryption**: Data encryption at rest is enforced for all clusters and backups, ensuring your data is protected always. For more information, see [encryption at rest](database-encryption-at-rest.md).

## Backup and restore

- **Enable automated cluster backups**: Backups are enabled at cluster creation, fully automated, and can't be disabled. You can restore your cluster to any timestamp within the 35-day retention period. For more information, see [how to restore a cluster](how-to-restore-cluster.md).

## Monitoring and response

- **Monitor for attacks using audit and activity logs**: Use audit logging and activity logs to monitor your database for normal and abnormal activity, including who performed operations and when. For more information, see [how to monitor diagnostics logs](how-to-monitor-diagnostics-logs.md).

- **Respond to attacks with Azure support**: If you suspect an attack, contact Azure support to initiate a five-step incident response process to restore service security and operations. For more information, see [shared responsibility in the cloud](/azure/security/fundamentals/shared-responsibility).

## Related content

- [Overview](overview.md)
- [How to enable private access](how-to-private-link.md)
- [How to enable public access](how-to-public-access.md)
