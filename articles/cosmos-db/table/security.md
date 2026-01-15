---
title: Secure your account
titleSuffix: Azure Cosmos DB for Table
description: Review the fundamentals of securing Azure Cosmos DB for Table from the perspective of data and networking security.
author: seesharprun
ms.author: sidandrews
ms.reviewer: skhera
ms.service: azure-cosmos-db
ms.subservice: table
ms.topic: best-practice
ms.date: 09/11/2025
ms.custom: security-horizontal-2025
ai-usage: ai-generated
---

# Secure your Azure Cosmos DB for Table account

Azure Cosmos DB for Table is a fully managed NoSQL database service that enables you to store, manage, and query large volumes of key-value data using the familiar Azure Table storage APIs. While Azure Cosmos DB provides built-in security features to protect your data, it's essential to follow best practices to further enhance the security of your account, data, and networking configurations.

This article provides guidance on how to best secure your Azure Cosmos DB for Table deployment.

## Network security

- **Disable public network access and use private endpoints only**

  - Public network access: Disabled  
  - Connectivity: Private endpoint  
  - Virtual network: Azure virtual network–integrated subnet  

  Verify in the Azure portal that **Public network access** is set to **Disabled** and that at least one private endpoint is configured for the account.
  <!-- Converted narrative prose into a concise parameter/value list with a single verification criterion and normalized the product name to Azure Cosmos DB for Table. -->

  For more information, see [configure virtual network access](../how-to-configure-vnet-service-endpoint.md) and [configure access from private endpoints](../how-to-configure-private-endpoints.md).

- **Enable Network Security Perimeter for network isolation**

  - Network Security Perimeter: Enabled  
  - Access scope: Restricted to approved network boundaries  

  Verify that the Azure Cosmos DB for Table account is associated with a Network Security Perimeter and that inbound access is limited to the intended network scope.
  <!-- Converted paragraph-style guidance into a parameter/value list with an explicit verification step. -->

  For more information, see [Configure Network Security Perimeter](../how-to-configure-nsp.md).

## Identity management

- **Use managed identities to access your account from other Azure services**

  - Identity type: System-assigned or user-assigned managed identity  
  - Scope: Azure Cosmos DB for Table account  
  - Authentication: Microsoft Entra ID  

  Verify that the managed identity is enabled on the calling Azure resource and granted access to the Azure Cosmos DB for Table account.
  <!-- Replaced narrative description with a structured parameter/value list and added a verification statement. -->

  For more information, see [Managed identities for Azure resources](/entra/identity/managed-identities-azure-resources/overview).

- **Use Azure control plane role-based access control to manage account databases and tables**

  - Access plane: Control plane  
  - Resource types: Account, database, table (Table API resource)  
  - Authorization model: Azure role-based access control (RBAC)  

  Verify role assignments under **Access control (IAM)** for the Azure Cosmos DB for Table account.
  <!-- Disambiguated resource terminology by replacing containers with tables (Table API resources) and converted prose into a parameter/value list. -->

  For more information, see [Grant control plane access](how-to-connect-role-based-access-control.md#grant-control-plane-role-based-access).

- **Use native data plane role-based access control to query, create, and access items within a table**

  - Access plane: Data plane  
  - Resource type: Table (Table API resource)  
  - Authorization model: Native Azure Cosmos DB RBAC  

  Verify that data plane role assignments allow only the required permissions for the target table.
  <!-- Clarified table versus container usage and converted the guidance into a structured list with verification. -->

  For more information, see [Grant data plane access](how-to-connect-role-based-access-control.md#grant-data-plane-role-based-access).

- **Separate the Azure identities used for data and control plane access**

  - Identity usage: Dedicated identities per access plane  
  - Control plane identity: Administrative operations  
  - Data plane identity: Application data access  

  Verify that no single identity is assigned roles across both control and data planes beyond operational requirements.
  <!-- Converted descriptive guidance into explicit parameters with a clear success criterion. -->

## Transport security

- **Use and enforce TLS for transport security**

  - Minimum TLS version: 1.3  

  Verify the **Minimum TLS version** setting under the account networking configuration in the Azure portal.
  <!-- Converted a single descriptive bullet into a parameter/value list with a verification line. -->

  For more information, see [Minimum TLS enforcement](../self-serve-minimum-tls-enforcement.md).

## Data encryption

- **Encrypt data at rest and in transit**

  - Encryption at rest: Enabled  
  - Key type: Service-managed keys or customer-managed keys (CMKs)  
  - Encryption in transit: TLS-encrypted connections  

  Verify key configuration under **Encryption** in the Azure portal for the Azure Cosmos DB for Table account.
  <!-- Replaced narrative encryption guidance with a structured parameter/value list and verification statement. -->

  For more information, see [Configure customer-managed keys](../how-to-setup-customer-managed-keys.md).

- **Use Always Encrypted to secure data with client-side encryption**

  - Encryption model: Client-side (Always Encrypted)  
  - Protected data: Sensitive columns within a table (Table API resource)  

  Verify that encrypted columns remain encrypted in transit and at rest by inspecting client configuration and stored data.
  <!-- Converted prose into a parameter/value list and clarified table resource usage with verification guidance. -->

  For more information, see [Always Encrypted](../how-to-always-encrypted.md).

## Backup and restore

- **Enable native continuous backup and restore**

  - Backup mode: Continuous  
  - Retention: Configured per business requirements  

  Verify that restore points are available in the **Restore** blade for the Azure Cosmos DB for Table account.
  <!-- Converted paragraph-style backup guidance into structured parameters with a verification step. -->

  For more information, see [Continuous backup and restore](../online-backup-and-restore.md).

- **Test backup and recovery procedures**

  - Restore scope: Database or table (Table API resource)  
  - Test frequency: Regularly scheduled  

  Verify successful test restores by completing a restore operation to a new account or table.
  <!-- Normalized table terminology and converted narrative guidance into a parameter/value list with success criteria. -->

  For more information, see [restore a container or database](../how-to-restore-in-account-continuous-backup.md).

---

### Agent feedback applied

[Agent: mamccrea-test-agent]  
1. Normalized incorrect product naming in the Network security section by replacing references to “Azure Cosmos DB for NoSQL” with “Azure Cosmos DB for Table.”  
2. Disambiguated resource terminology by consistently using “table (Table API resource)” instead of ambiguous container references.  
3. Converted prose under “Network security” into concise parameter/value lists with verification criteria.  
4. Converted prose under “Identity management” into structured parameter/value lists with verification criteria.  
5. Converted prose under “Transport security” into a parameter/value list with verification criteria.  
6. Converted prose under “Data encryption” into structured lists with verification criteria.  
7. Converted prose under “Backup and restore” into structured lists with verification criteria.