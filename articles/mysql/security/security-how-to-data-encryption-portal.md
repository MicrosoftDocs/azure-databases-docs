---
title: Set up Data Encryption by Using the Azure Portal
description: Learn how to set up and manage data encryption for Azure Database for MySQL - Flexible Server by using the Azure portal.
author: Tameika-MSFT
ms.author: talawren
ms.reviewer: maghan
ms.date: 07/17/2026
ms.service: azure-database-mysql
ms.subservice: security
ms.topic: how-to
---

# Data encryption for Azure Database for MySQL flexible server by using the Azure portal

This article shows you how to set up and manage data encryption at rest for Azure Database for MySQL flexible server by using the Azure portal.

In this article, you learn how to:

- Set data encryption for Azure Database for MySQL.
- Configure data encryption for database restore operations.
- Configure data encryption for replica servers.

## Encryption types

Azure Database for MySQL supports two primary types of encryption to help safeguard your data.

- **Encryption at rest** ensures that all data stored in the database, including backups and logs, is protected from unauthorized access by encrypting it on disk.
- **Encryption in transit** secures data as it moves between your client applications and the database server covered in [Transport Layer Security (TLS) in Azure Database for MySQL](security-tls.md).

## Permission models for Azure Key Vault access

Azure key vault access configuration now supports two types of permission models - [Azure role-based access control](/azure/role-based-access-control/overview) and [Vault access policy](/azure/key-vault/general/assign-access-policy). This article describes how to configure data encryption for Azure Database for MySQL by using a Vault access policy.

You can choose to use Azure RBAC as a permission model to grant access to Azure Key Vault. To do so, you need a built-in or custom role that has the three permissions and assign it through "role assignments" by using the Access control (IAM) tab in the key vault:

- KeyVault/vaults/keys/wrap/action
- KeyVault/vaults/keys/unwrap/action
- KeyVault/vaults/keys/read.

For Azure Key Vault-managed HSM, you need to assign the "Managed HSM Crypto Service Encryption User" role.

## Prerequisites

- An Azure account with an active subscription.

- If you don't have an Azure subscription, create an [Azure free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) before you begin.

  > [!NOTE]  
  > With an Azure free account, you can now try Azure Database for MySQL Flexible Server for free for 12 months. For more information, see [Use an Azure free account to try Azure Database for MySQL - Flexible Server for free](../flexible-server/quickstart-create-server-portal.md).

## Set the proper permissions for key operations

1. In Key Vault, select **Access policies**, and then select **Create**.

   :::image type="content" source="media/how-to-data-encryption-portal/1-mysql-key-vault-access-policy.jpeg" alt-text="Screenshot of Key Vault Access Policy in the Azure portal.":::

1. On the **Permissions** tab, select the following key permissions: **Get**, **List**, **Wrap Key**, and **Unwrap Key**.

1. On the **Principal** tab, select the user-assigned managed identity.

1. Select **Create**.

## Configure customer managed key

To set up the customer-managed key, follow these steps.

1. In the portal, go to your Azure Database for MySQL Flexible Server instance. Under **Security**, select **Data encryption**.

   :::image type="content" source="media/how-to-data-encryption-portal/3-mysql-data-encryption.jpeg" alt-text="Screenshot of the data encryption page.":::

1. On **Data encryption**, under **No identity assigned**, select **Change identity**.

1. In **Select user assigned managed identity**, select the `demo-umi` identity, and then select **Add**.

   :::image type="content" source="media/how-to-data-encryption-portal/4-mysql-assigned-managed-identity-demo-uni.jpeg" alt-text="Screenshot of selecting the demo-umi from the assigned managed identity page.":::

1. To the right of **Key selection method**, either **Select a key** and specify a key vault and key pair, or select **Enter a key identifier**.

   :::image type="content" source="media/how-to-data-encryption-portal/5-mysql-configure-encryption-marked.png" alt-text="Screenshot of key selection method to show user." lightbox="media/how-to-data-encryption-portal/5-mysql-configure-encryption-marked.png":::

1. Select **Save**.

## Use data encryption for restore

To use data encryption as part of a restore operation, follow these steps.

1. In the Azure portal, go to the Overview page for your server and select **Restore**.

1. On the **Security** tab, enter the identity and the key.

   :::image type="content" source="media/how-to-data-encryption-portal/6-mysql-navigate-overview-page.jpeg" alt-text="Screenshot of overview page.":::

1. Select **Change identity** and select the **User assigned managed identity** and select **Add**.

   To select the key, you can either select a **key vault** and **key pair** or enter a **key identifier**.

   :::image type="content" source="media/how-to-data-encryption-portal/7-mysql-change-identity.jpeg" alt-text="Screenshot of the change identity page.":::

## Use data encryption for replica servers

After you encrypt your Azure Database for MySQL Flexible Server instance with a customer-managed key stored in Key Vault, any newly created copy of the server is also encrypted.

1. To configure replication, under **Settings**, select **Replication**, and then select **Add replica**.

   :::image type="content" source="media/how-to-data-encryption-portal/8-mysql-replication.jpeg" alt-text="Screenshot of the Replication page.":::

1. In **Add Replica server to Azure Database for MySQL**, select the appropriate **Compute + storage** option, and then select **OK**.

   > [!IMPORTANT]  
   > When you try to encrypt an Azure Database for MySQL Flexible Server with a customer-managed key that already has replicas, configure one or more replicas by adding the managed identity and key.

## Related content

- [Data encryption with customer managed keys for Azure Database for MySQL](security-customer-managed-key.md)
- [Data encryption for Azure Database for MySQL flexible server with Azure CLI](security-how-to-data-encryption-cli.md)
