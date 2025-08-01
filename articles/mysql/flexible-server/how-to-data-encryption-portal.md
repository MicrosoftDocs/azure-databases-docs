---
title: Set up Data Encryption By Using the Azure portal
description: Learn how to set up and manage data encryption for Azure Database for MySQL - Flexible Server by using the Azure portal.
author: SudheeshGH
ms.author: sunaray
ms.reviewer: maghan, talawren
ms.date: 11/27/2024
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: how-to
ms.custom: sfi-image-nochange
---

# Data encryption for Azure Database for MySQL with the Azure portal

This article shows you how to set up and manage data encryption for Azure Database for MySQL, which focuses on encryption at rest, which protects data stored in the database.

In this article, you learn how to:

- Set data encryption for Azure Database for MySQL.
- Configure data encryption for restoration.
- Configure data encryption for replica servers.

Azure key vault access configuration now supports two types of permission models - [Azure role-based access control](/azure/role-based-access-control/overview) and [Vault access policy](/azure/key-vault/general/assign-access-policy). The article describes how to configure data encryption for Azure Database for MySQL using a Vault access policy. 

You can choose to use Azure RBAC as a permission model to grant access to Azure Key Vault. To do so, you need a built-in or custom role that has the below three permissions and assign it through "role assignments" using the Access control (IAM) tab in the keyvault:

- KeyVault/vaults/keys/wrap/action
- KeyVault/vaults/keys/unwrap/action
- KeyVault/vaults/keys/read. For Azure Key Vault-managed HSM, you'll also need to assign the "Managed HSM Crypto Service Encryption User" role assignment in RBAC.

## Encryption types

Azure Database for MySQL supports two primary types of encryption to help safeguard your data. **Encryption at rest** ensures that all data stored in the database, including backups and logs, is protected from unauthorized access by encrypting it on disk. **Encryption in transit** (also known as communications encryption) secures data as it moves between your client applications and the database server, typically using TLS/SSL protocols. Together, these encryption types provide comprehensive protection for your data both while it's stored and as it's transmitted.

- **Encryption at Rest**: Protects data stored in the database, backups, and logs. This is the primary focus of this article.
- **Communications Encryption (Encryption in Transit)**: Protects data as it travels between the client and the server, typically using TLS/SSL protocols.

## Prerequisites

- An Azure account with an active subscription.
- If you don't have an Azure subscription, create an [Azure free account](https://azure.microsoft.com/free) before you begin.

    > [!NOTE]
    > With an Azure free account, you can now try Azure Database for MySQL Flexible Server for free for 12 months. For more information, see [Use an Azure free account to try Azure Database for MySQL - Flexible Server for free](how-to-deploy-on-azure-free-account.md).

## Set the proper permissions for key operations

1. In Key Vault, select **Access policies**, and then select **Create**.

 :::image type="content" source="media/how-to-data-encryption-portal/1-mysql-key-vault-access-policy.jpeg" alt-text="Screenshot of Key Vault Access Policy in the Azure portal.":::

1. On the **Permissions** tab, select the following **Key permissions - Get** , **List** , **Wrap Key** , **Unwrap Key**.

1. On the **Principal** tab, select the User-assigned Managed Identity.

 :::image type="content" source="media/how-to-data-encryption-portal/2-mysql-principal-tab.jpeg" alt-text="Screenshot of the principal tab in the Azure portal.":::

1. Select **Create**.

## Configure customer managed key

To set up the customer-managed key, follow these steps.

1. In the portal, navigate to your Azure Database for MySQL Flexible Server instance, and then, under **Security** , select **Data encryption**.

 :::image type="content" source="media/how-to-data-encryption-portal/3-mysql-data-encryption.jpeg" alt-text="Screenshot of the data encryption page.":::

1. On the **Data encryption** page, under **No identity assigned** , select **Change identity** ,

1. In the **Select user assigned*** managed identity **dialog box, select the** demo-umi **identity, and then select** Add**.

 :::image type="content" source="media/how-to-data-encryption-portal/4-mysql-assigned-managed-identity-demo-uni.jpeg" alt-text="Screenshot of selecting the demo-umi from the assigned managed identity page.":::

1. To the right of **Key selection method** , either **Select a key** and specify a key vault and key pair, or select **Enter a key identifier**.

 :::image type="content" source="media/how-to-data-encryption-portal/5-mysql-configure-encryption-marked.png" alt-text="Screenshot of key selection method to show user." lightbox="media/how-to-data-encryption-portal/5-mysql-configure-encryption-marked.png":::

1. Select **Save**.

## Use Data encryption for restore

To use data encryption as part of a restore operation, follow these steps.

1. In the Azure portal, navigate to the Overview page for your server and select **Restore**.
    1. On the **Security** tab, you specify the identity and the key.

 :::image type="content" source="media/how-to-data-encryption-portal/6-mysql-navigate-overview-page.jpeg" alt-text="Screenshot of overview page.":::

1. Select **Change identity** and select the **User assigned managed identity** and select **Add**
**To select the Key** , you can either select a **key vault** and **key pair** or enter a **key identifier**

 :::image type="content" source="media/how-to-data-encryption-portal/7-mysql-change-identity.jpeg" alt-text="SCreenshot of the change identity page.":::

## Use Data encryption for replica servers

After your Azure Database for MySQL Flexible Server instance is encrypted with a customer's managed key stored in Key Vault, any newly created copy of the server is also encrypted.

1. To configuration replication, under **Settings** , select **Replication** , and then select **Add replica**.

 :::image type="content" source="media/how-to-data-encryption-portal/8-mysql-replication.jpeg" alt-text="Screenshot of the Replication page.":::

1. In the Add Replica server to Azure Database for MySQL dialog box, select the appropriate **Compute + storage** option, and then select **OK**.

 :::image type="content" source="media/how-to-data-encryption-portal/9-mysql-compute-storage.jpeg" alt-text="Screenshot of the Compute + Storage page.":::

    > [!IMPORTANT]  
    When trying to encrypt an Azure Database for MySQL Flexible Server with a customer-managed key that already has replicas, we recommend configuring one or more replicas by adding the managed identity and key.

## Related content

- [Data encryption with customer-managed keys for Azure Database for MySQL - Flexible Server](concepts-customer-managed-key.md)
- [Data encryption for Azure Database for MySQL - Flexible Server with Azure CLI](how-to-data-encryption-cli.md)
