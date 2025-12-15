---
title: Secure Your Account
description: Review the fundamentals of securing Azure Cosmos DB for Apache Gremlin from the perspective of data and networking security.
ms.topic: best-practice
ms.date: 09/11/2025
ms.custom: [security-horizontal-2025, horz-security]
ai-usage: ai-generated
---

# Secure your Azure Cosmos DB for Apache Gremlin account

[!INCLUDE[Note - Recommended services](includes/note-recommended-services.md)]

Azure Cosmos DB for Apache Gremlin is a fully managed graph database service that enables you to store, query, and traverse large-scale graph data using the Gremlin query language.

This article provides guidance on how to best secure your Azure Cosmos DB for Apache Gremlin deployment.

## Network security

- **Disable public network access and use Private Endpoints only**: Deploy Azure Cosmos DB for NoSQL with a configuration that restricts network access to an Azure-deloyed virtual network. The account is exposed through the specific subnet you configured. Then, disable public network access for the entire account and use private endpoints exclusively for services that connect to the account. For more information, see [configure virtual network access](../how-to-configure-vnet-service-endpoint.md) and [configure access from private endpoints](../how-to-configure-private-endpoints.md).

- **Enable Network Security Perimeter for network isolation**: Use Network Security Perimeter (NSP) to restrict access to your Azure Cosmos DB account by defining network boundaries and isolating it from public internet access. For more information, see [Configure Network Security Perimeter](../how-to-configure-nsp.md).

## Identity management

- **Use Azure control plane role-based access control to manage account databases and containers**: Apply Azure role-based access control to define fine-grained permissions for managing Azure Cosmos DB accounts, databases, and containers. This control ensures that only authorized users or services can perform administrative operations. For more information, see [Grant control plane access](../how-to-grant-control-plane-access.md).

## Transport security

- **Use and enforce TLS 1.3 for transport security**: Enforce transport layer security (TLS) 1.3 to secure data in transit with the latest cryptographic protocols, ensuring stronger encryption and improved performance. For more information, see [Minimum TLS enforcement](../self-serve-minimum-tls-enforcement.md).

## Data encryption

- **Encrypt data at rest or in-motion using service-managed keys or customer-managed keys (CMKs)**: Protect sensitive data by encrypting it at rest and in transit. Use service-managed keys for simplicity or customer-managed keys for greater control over encryption. For more information, see [Configure customer-managed keys](../how-to-setup-customer-managed-keys.md).

- **Use Always Encrypted to secure data with client-side encryption**: Always Encrypted ensures that sensitive data is encrypted on the client side before being sent to Azure Cosmos DB, providing an extra layer of security. For more information, see [Always Encrypted](../how-to-always-encrypted.md).

## Backup and restore

- **Enable native continuous backup and restore**: Protect your data by enabling continuous backup, which allows you to restore your Azure Cosmos DB account to any point in time within the retention period. For more information, see [Continuous backup and restore](../online-backup-and-restore.md).

- **Test backup and recovery procedures**: To verify the effectiveness of backup processes, regularly test the restoration of databases, containers, and items. For more information, see [restore a container or database](../how-to-restore-in-account-continuous-backup.md).
