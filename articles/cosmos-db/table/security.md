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
ms.date: 09/10/2025
ms.custom: security-horizontal-2025
ai-usage: ai-generated
appliesto:
  - ✅ Table
---

# Secure your Azure Cosmos DB for Table account

Azure Cosmos DB for Table is a globally distributed, multi-model database service designed for mission-critical applications. While Azure Cosmos DB provides built-in security features to protect your data, it's essential to follow best practices to further enhance the security of your account, data, and networking configurations.

This article provides guidance on how to best secure your Azure Cosmos DB for Table deployment.

## Network security

- **Disable public network access and use Private Endpoints only**: Deploy Azure Cosmos DB for Table with a configuration that restricts network access to an Azure-deloyed virtual network. The account is exposed through the specific subnet you configured. Then, disable public network access for the entire account and use private endpoints exclusively for services that connect to the account. For more information, see [configure virtual network access](../how-to-configure-vnet-service-endpoint.md) and [configure access from private endpoints](../how-to-configure-private-endpoints.md).

## Identity management

- **Use managed identities to access your account from other Azure services**: Managed identities eliminate the need to manage credentials by providing an automatically managed identity in Microsoft Entra ID. Use managed identities to securely access Azure Cosmos DB from other Azure services without embedding credentials in your code. For more information, see [Managed identities for Azure resources](/entra/identity/managed-identities-azure-resources/overview).

- **Use Azure control plane role-based access control to manage account databases and containers**: Apply Azure role-based access control to define fine-grained permissions for managing Azure Cosmos DB accounts, databases, and containers. This control ensures that only authorized users or services can perform administrative operations. For more information, see [Grant control plane access](how-to-connect-role-based-access-control.md#grant-control-plane-role-based-access).

- **Use native data plane role-based access control to query, create, and access items within a container**: Implement data plane role-based access control to enforce least privilege access for querying, creating, and accessing items within Azure Cosmos DB containers. This control helps secure your data operations. For more information, see [Grant data plane access](how-to-connect-role-based-access-control.md#grant-data-plane-role-based-access).

- **Separate the Azure identities used for data and control plane access**: Use distinct Azure identities for control plane and data plane operations to reduce the risk of privilege escalation and ensure better access control. This separation enhances security by limiting the scope of each identity.
