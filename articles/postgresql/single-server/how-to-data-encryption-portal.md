---
title: Data encryption - Azure portal - for Azure Database for PostgreSQL - Single server
description: Learn how to set up and manage data encryption for your Azure Database for PostgreSQL Single server by using the Azure portal.
author: sunilagarwal
ms.author: sunila
ms.reviewer: maghan
ms.date: 09/10/2024
ms.service: azure-database-postgresql
ms.subservice: single-server
ms.topic: how-to
ms.custom:
  - devx-track-azurecli
---

# Data encryption for Azure Database for PostgreSQL Single server by using the Azure portal

[!INCLUDE [applies-to-postgresql-single-server](../includes/applies-to-postgresql-single-server.md)]

[!INCLUDE [azure-database-for-postgresql-single-server-deprecation](../includes/azure-database-for-postgresql-single-server-deprecation.md)]

Learn how to use the Azure portal to set up and manage data encryption for your Azure Database for PostgreSQL Single server.

## Prerequisites for Azure CLI

- You must have an Azure subscription and be an administrator on that subscription.
- In Azure Key Vault, create a key vault and key to use for a customer-managed key.
- The key vault must have the following properties to use as a customer-managed key:
  * [Soft delete](/azure/key-vault/general/soft-delete-overview)

    ```azurecli-interactive
    az resource update --id $(az keyvault show --name \ <key_vault_name> -test -o tsv | awk '{print $1}') --set \ properties.enableSoftDelete=true
    ```

  * [Purge protected](/azure/key-vault/general/soft-delete-overview#purge-protection)

    ```azurecli-interactive
    az keyvault update --name <key_vault_name> --resource-group <resource_group_name>  --enable-purge-protection true
    ```

- The key must have the following attributes to use as a customer-managed key:
  * No expiration date
  * Not disabled
  * Able to perform get, wrap key, and unwrap key operations

## Set the right permissions for key operations

1. In Key Vault, select **Access policies** > **Add Access Policy**.

   :::image type="content" source="media/how-to-data-encryption-portal/show-access-policy-overview.png" alt-text="Screenshot of Key Vault, with Access policies and Add Access Policy highlighted." lightbox="media/how-to-data-encryption-portal/show-access-policy-overview.png":::

1. Select **Key permissions**, and select **Get**, **Wrap**, **Unwrap**, and the **Principal**, which is the name of the PostgreSQL server. If your server principal can't be found in the list of existing principals, you need to register it. You're prompted to register your server principal when you attempt to set up data encryption for the first time, and it fails.

   :::image type="content" source="media/how-to-data-encryption-portal/access-policy-wrap-unwrap.png" alt-text="Screenshot of Access policy overview." lightbox="media/how-to-data-encryption-portal/access-policy-wrap-unwrap.png":::

1. Select **Save**.

## Set data encryption for Azure Database for PostgreSQL Single server

1. In Azure Database for PostgreSQL, select **Data encryption** to set up the customer-managed key.

   :::image type="content" source="media/how-to-data-encryption-portal/data-encryption-overview.png" alt-text="Screenshot of Azure Database for PostgreSQL, with Data encryption highlighted." lightbox="media/how-to-data-encryption-portal/data-encryption-overview.png":::

1. You can either select a key vault and key pair, or enter a key identifier.

   :::image type="content" source="media/how-to-data-encryption-portal/setting-data-encryption.png" alt-text="Screenshot of Azure Database for PostgreSQL, with data encryption options highlighted." lightbox="media/how-to-data-encryption-portal/setting-data-encryption.png":::

1. Select **Save**.

1. To ensure all files (including temp files) are fully encrypted, restart the server.

## Use Data encryption for restore or replica servers

After Azure Database for PostgreSQL Single server is encrypted with a customer's managed key stored in Key Vault, any newly created copy of the server is also encrypted. You can make this new copy either through a local or geo-restore operation, or through a replica (local/cross-region) operation. So for an encrypted PostgreSQL server, you can use the following steps to create an encrypted restored server.

1. On your server, select **Overview** > **Restore**.

   :::image type="content" source="media/how-to-data-encryption-portal/show-restore.png" alt-text="Screenshot of Azure Database for PostgreSQL, with Overview and Restore highlighted." lightbox="media/how-to-data-encryption-portal/show-restore.png":::

   Or for a replication-enabled server, under the **Settings** heading, select **Replication**.

   :::image type="content" source="media/how-to-data-encryption-portal/postgresql-replica.png" alt-text="Screenshot of Azure Database for PostgreSQL, with Replication highlighted." lightbox="media/how-to-data-encryption-portal/postgresql-replica.png":::

1. After the restore operation is complete, the new server created is encrypted with the primary server's key. However, the features and options on the server are disabled, and the server is inaccessible. This prevents any data manipulation, because the new server's identity hasn't yet been given permission to access the key vault.

   :::image type="content" source="media/how-to-data-encryption-portal/show-restore-data-encryption.png" alt-text="Screenshot of Azure Database for PostgreSQL, with Inaccessible status highlighted." lightbox="media/how-to-data-encryption-portal/show-restore-data-encryption.png":::

1. To make the server accessible, revalidate the key on the restored server. Select **Data Encryption** > **Revalidate key**.

   > [!NOTE]  
   > The first attempt to revalidate will fail, because the new server's service principal needs to be given access to the key vault. To generate the service principal, select **Revalidate key**, which will show an error but generates the service principal. Thereafter, refer to [these steps](#set-the-right-permissions-for-key-operations) earlier in this article.

   :::image type="content" source="media/how-to-data-encryption-portal/show-revalidate-data-encryption.png" alt-text="Screenshot of Azure Database for PostgreSQL, with revalidation step highlighted." lightbox="media/how-to-data-encryption-portal/show-revalidate-data-encryption.png":::

   You will have to give the key vault access to the new server. For more information, see [Enable Azure RBAC permissions on Key Vault](/azure/key-vault/general/rbac-guide?tabs=azure-cli#enable-azure-rbac-permissions-on-key-vault).

1. After registering the service principal, revalidate the key again, and the server resumes its normal functionality.

   :::image type="content" source="media/how-to-data-encryption-portal/restore-successful.png" alt-text="Screenshot of Azure Database for PostgreSQL, showing restored functionality." lightbox="media/how-to-data-encryption-portal/restore-successful.png":::

## Next step

> [!div class="nextstepaction"]
> [Azure Database for PostgreSQL Single server data encryption with customer-managed key](concepts-data-encryption-postgresql.md)
