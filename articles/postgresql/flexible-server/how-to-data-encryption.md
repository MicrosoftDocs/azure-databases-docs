---
title: Configure data encryption
description: Learn how to configure data encryption in Azure Database for PostgreSQL - Flexible Server.
author: techlake
ms.author: hganten
ms.reviewer: maghan
ms.date: 01/14/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
---
# Configure data encryption

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

This article provides step-by-step instructions to configure data encryption for an Azure Database for PostgreSQL flexible server.

> [!IMPORTANT]
> Selection of system or customer managed encryption key for data encryption of an Azure Database for PostgreSQL flexible server, can only be made when the server is deployed.

In this article, you learn how to create a new server and configure its data encryption options. For existing servers, whose data encryption is configured to use customer managed encryption key, you learn:
- How to select a different user assigned managed identity with which the service accesses the encryption key.
- How to specify a different encryption key or how to rotate the encryption key currently used for data encryption.

To learn about data encryption in the context of Azure Database for PostgreSQL - Flexible Server, see the [data encryption](concepts-data-encryption.md).

## Configure data encryption with system managed key during server provisioning

### [Portal](#tab/portal-system-managed-server-provisioning)

Using the [Azure portal](https://portal.azure.com/):

1. During provisioning of a new instance of Azure Database for PostgreSQL Flexible Server, in the **Security** tab.

    :::image type="content" source="./media/how-to-data-encryption/create-server-security-tab.png" alt-text="Screenshot showing how to get to the Security tab, from where you can configure data encryption settings." lightbox="./media/how-to-data-encryption/create-server-security-tab.png":::

2. In the **Data encryption key**, select the **Service-managed key** radio button.

    :::image type="content" source="./media/how-to-data-encryption/create-server-system-assigned.png" alt-text="Screenshot showing how to select the system managed encryption key during server provisioning." lightbox="./media/how-to-data-encryption/create-server-system-assigned.png":::

3. If you enable geo-redundant backup storage to be provisioned together with the server, the aspect of the **Security** tab changes slightly because the server uses two separate encryption keys. One for the primary region in which you're deploying your server, and one for the paired region to which the server backups are asynchronously replicated.

    :::image type="content" source="./media/how-to-data-encryption/create-server-system-assigned-geo-redundant.png" alt-text="Screenshot showing how to select the system managed encryption key during server provisioning, when the server is enabled for geo-redundant backup storage." lightbox="./media/how-to-data-encryption/create-server-system-assigned-geo-redundant.png":::

### [CLI](#tab/cli-system-managed-server-provisioning)

You can enable data encryption with system assigned encryption key, while provisioning a new server, via the [az postgres flexible-server create](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-create) command.

```azurecli-interactive
az postgres flexible-server create --resource-group <resource_group> --name <server> ...
```

> [!NOTE]
> Notice that there's no special parameter in the previous command to specify that the server must be created with system assigned key for data encryption. The reason being that data encryption with system assigned key is the default option.
> Also, notice that you must complete the command provided with other parameters whose presence and values would vary depending on how you want to configure other features of the provisioned server.

---

## Configure data encryption with customer managed key during server provisioning

### [Portal](#tab/portal-customer-managed-server-provisioning)

Using the [Azure portal](https://portal.azure.com/):


1. [Create one user assigned managed identity](/entra/identity/managed-identities-azure-resources/how-manage-user-assigned-managed-identities), if you don't have one created yet.

2. [Create one Azure Key Vault](/azure/key-vault/general/quick-create-portal) or [create one Managed HSM](/azure/key-vault/managed-hsm/quick-create-cli), if you don't have one key store created yet. Make sure that you meet the [requirements](concepts-data-encryption.md#requirements), and follow the [recommendations](concepts-data-encryption.md#recommendations) before you configure the key store, create the key and assign the required permissions to the user assigned managed identity.

3. [Create one key in your key store](/azure/key-vault/keys/quick-create-portal).

4. During provisioning of a new instance of Azure Database for PostgreSQL Flexible Server, in the **Security** tab.

    :::image type="content" source="./media/how-to-data-encryption/create-server-security-tab.png" alt-text="Screenshot showing how to get to the Security tab, from where you can configure data encryption settings." lightbox="./media/how-to-data-encryption/create-server-security-tab.png":::

5. In the **Data encryption key**, select the **Service-managed key** radio button.

    :::image type="content" source="./media/how-to-data-encryption/create-server-customer-assigned.png" alt-text="Screenshot showing how to select the customer managed encryption key during server provisioning." lightbox="./media/how-to-data-encryption/create-server-customer-assigned.png":::

6. If you enable geo-redundant backup storage to be provisioned together with the server, the aspect of the **Security** tab changes slightly because the server uses two separate encryption keys. One for the primary region in which you're deploying your server, and one for the paired region to which the server backups are asynchronously replicated.

    :::image type="content" source="./media/how-to-data-encryption/create-server-customer-assigned-geo-redundant.png" alt-text="Screenshot showing how to select the customer managed encryption key during server provisioning, when the server is enabled for geo-redundant backup storage." lightbox="./media/how-to-data-encryption/create-server-customer-assigned-geo-redundant.png":::

7. In **User assigned managed identity**, select **Change identity**.

    :::image type="content" source="./media/how-to-data-encryption/create-server-customer-assigned-change-identity.png" alt-text="Screenshot showing how to select the user assigned managed identity to access the data encryption key for the data of the server location." lightbox="./media/how-to-data-encryption/create-server-customer-assigned-change-identity.png":::

8. Among the list of user assigned managed identities, select the one you want your server to use to access the data encryption key stored in an Azure Key Vault.

    :::image type="content" source="./media/how-to-data-encryption/create-server-customer-assigned-select-identity.png" alt-text="Screenshot showing how to select the user assigned managed identity to access the data encryption key for the data of the server location and copy of the backup kept in server's region." lightbox="./media/how-to-data-encryption/create-server-customer-assigned-select-identity.png":::

9. Select **Add**.

    :::image type="content" source="./media/how-to-data-encryption/create-server-customer-assigned-add-identity.png" alt-text="Screenshot showing the location of the Add button to assign the identity with which the server accesses the data encryption key." lightbox="./media/how-to-data-encryption/create-server-customer-assigned-add-identity.png":::

10. Select **Select a key**.

    :::image type="content" source="./media/how-to-data-encryption/create-server-customer-assigned-select-key.png" alt-text="Screenshot showing how to select a data encryption key." lightbox="./media/how-to-data-encryption/create-server-customer-assigned-select-key.png":::

11. **Subscription** is automatically populated with the name of the subscription on which your server is about to be created. The key store that keeps the data encryption key must exist in the same subscription as the server.

    :::image type="content" source="./media/how-to-data-encryption/create-server-customer-assigned-key-subscription.png" alt-text="Screenshot showing how to select the subscription in which the key store should exist." lightbox="./media/how-to-data-encryption/create-server-customer-assigned-key-subscription.png":::

12. In **Key store type**, select the radio button corresponding to the type of key store in which you plan to store the data encryption key. In this example, we choose **Key vault**, but the experience is very similar if you choose **Managed HSM**.

    :::image type="content" source="./media/how-to-data-encryption/create-server-customer-assigned-key-store-type.png" alt-text="Screenshot showing how to select the type of store that keeps the data encryption key." lightbox="./media/how-to-data-encryption/create-server-customer-assigned-key-store-type.png":::

13. Expand **Key vault** (or **Managed HSM**, if you selected that storage type), and select the instance where the data encryption key exists.

> [!NOTE]
> When you expand the drop down box, it shows **No available items**. It takes a few seconds until it lists all the instances of key vault which are deployed in the same region as the server.

    :::image type="content" source="./media/how-to-data-encryption/create-server-customer-assigned-key-vault.png" alt-text="Screenshot showing how to select the key store that keeps the data encryption key." lightbox="./media/how-to-data-encryption/create-server-customer-assigned-key-vault.png":::

14. Expand **Key**, and select the name of the key that you want to use for data encryption.

    :::image type="content" source="./media/how-to-data-encryption/create-server-customer-assigned-key-key.png" alt-text="Screenshot showing how to select the data encryption key." lightbox="./media/how-to-data-encryption/create-server-customer-assigned-key-key.png":::

15. Expand **Version**, and select the identifier of the version of the key that you want to use for data encryption.

    :::image type="content" source="./media/how-to-data-encryption/create-server-customer-assigned-key-version.png" alt-text="Screenshot showing how to select the version to use of the data encryption key." lightbox="./media/how-to-data-encryption/create-server-customer-assigned-key-version.png":::

16. Select **Select**.

    :::image type="content" source="./media/how-to-data-encryption/create-server-customer-assigned-key-select.png" alt-text="Screenshot showing how to select the chose key." lightbox="./media/how-to-data-encryption/create-server-customer-assigned-key-select.png":::

17. Configure all other settings of the new server and select **Review + create**.

    :::image type="content" source="./media/how-to-data-encryption/create-server-customer-assigned-key-review-create.png" alt-text="Screenshot showing how to complete creation of server." lightbox="./media/how-to-data-encryption/create-server-customer-assigned-key-review-create.png":::

### [CLI](#tab/cli-customer-managed-server-provisioning)

You can enable data encryption with system assigned encryption key, while provisioning a new server, via the [az postgres flexible-server create](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-create) command.

```azurecli-interactive
az postgres flexible-server create --resource-group <resource_group> --name <server> ...
```

> [!NOTE]
> Notice that there's no special parameter in the previous command to specify that the server must be created with system assigned key for data encryption. The reason being that data encryption with system assigned key is the default option.
> Also, notice that you must complete the command provided with other parameters whose presence and values would vary depending on how you want to configure other features of the provisioned server.

---

## Configure user assigned encryption key during server provisioning

## Set up customer managed key during server creation
Prerequisites:

- Microsoft Entra user managed identity in the region where the Azure Database for PostgreSQL flexible server instance will be created. Follow this [tutorial](/azure/active-directory/managed-identities-azure-resources/qs-configure-portal-windows-vm) to create identity.

- Key Vault with key in region where the Azure Database for PostgreSQL flexible server instance will be created. Follow this [tutorial](/azure/key-vault/general/quick-create-portal) to create Key Vault and generate key. Follow [requirements section in concepts doc](concepts-data-encryption.md) for required Azure Key Vault settings.

Follow the steps below to enable CMK while creating the Azure Database for PostgreSQL flexible server instance using Azure portal.

1. Navigate to the Azure Database for PostgreSQL flexible server create pane via Azure portal.

2. Provide required information on Basics and Networking tabs.

3. Navigate to Security tab. On the screen, provide Microsoft Entra ID  identity that has access to the Key Vault and Key in Key Vault in the same region where you're creating this server.

4. On Review Summary tab, make sure that you provided correct information in Security section and press Create button.

5. Once it's finished, you should be able to navigate to Data Encryption  screen for the server and update identity or key if necessary.

## Update customer managed key on the CMK enabled Azure Database for PostgreSQL flexible server instance

Prerequisites:

- Microsoft Entra user-managed identity in region where the Azure Database for PostgreSQL flexible server instance will be created. Follow this [tutorial](/azure/active-directory/managed-identities-azure-resources/qs-configure-portal-windows-vm) to create identity.

- Key Vault with key in region where the Azure Database for PostgreSQL flexible server instance will be created. Follow this [tutorial](/azure/key-vault/general/quick-create-portal) to create Key Vault and generate key.

Follow the steps below to update CMK on CMK enabled Azure Database for PostgreSQL flexible server instance using Azure portal:

1. Navigate to the Azure Database for PostgreSQL flexible server create page via the Azure portal.

2. Navigate to Data Encryption screen under Security tab.

3. Select different identity to connect to Azure Key Vault, remembering that this identity needs to have proper access rights to the Key Vault.

4. Select different key by choosing subscription, Key Vault and key from dropdowns provided.

## Related content

- [Data encryption](concepts-data-encryption.md).
