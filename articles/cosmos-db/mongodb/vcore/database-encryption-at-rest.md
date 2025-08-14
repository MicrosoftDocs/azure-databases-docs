---
title: Encryption at rest in Azure Cosmos DB for MongoDB vCore
description: Learn about encryption of data in Azure Cosmos DB for MongoDB vCore databases using service-managed and customer-managed encryption keys.
author: niklarin
ms.author: nlarin
ms.service: azure-cosmos-db
ms.topic: concept-article
ms.date: 08/04/2025
appliesto:
  - ✅ MongoDB (vCore)
---

# Data encryption in Azure Cosmos DB for MongoDB vCore

All the data managed by an Azure Cosmos DB for MongoDB vCore is always encrypted at rest. That data includes all system and user databases, temporary files, logs, and backups.

[!INCLUDE[MongoDB vCore](./includes/notice-customer-managed-key-preview.md)]

## Encryption at rest with service-managed key (SMK) or customer-managed key (CMK)

Azure Cosmos DB for MongoDB vCore supports two modes of data encryption at rest: **service-managed keys (SMK)** and **customer-managed keys (CMK)**. Data encryption with service-managed keys is the default mode for Azure Cosmos DB for MongoDB vCore. In this mode, the service automatically manages the encryption keys used to encrypt your data. You don't need to take any action to enable or manage encryption in this mode.

In the **customer-managed keys** mode, you can bring your own encryption key to encrypt your data. When you specify a customer-managed key, that key is used to protect and control access to the key that encrypts your data. Customer-managed keys offer greater flexibility to manage access controls. You must deploy your own Azure Key Vault and configure it to store the encryption keys used by your Azure Cosmos DB for MongoDB vCore cluster.

The configuration mode can only be selected at cluster creation time. It can't be changed from one mode to another for the lifetime of the cluster.

To achieve the encryption of your data, Azure Cosmos DB for MongoDB vCore uses [server-side encryption of Azure Storage for data at rest](/azure/virtual-machines/disk-encryption). When using CMK, you're responsible for providing keys for encrypting and decrypting data in Azure Storage services. These keys must be stored in Azure Key Vault. 

## Benefits provided by each mode (SMK or CMK)

Data encryption with **service-managed keys** for Azure Cosmos DB for MongoDB vCore provides the following benefits:
- The service automatically and fully controls data access.
- The service automatically and fully controls your key's life cycle, including rotation of the key.
- You don't need to worry about managing data encryption keys.
- Data encryption based on service-managed keys doesn't negatively affect the performance of your workloads.
- It simplifies the management of encryption keys (including their regular rotation), and the management of the identities used to access those keys.

Data encryption with **customer-managed keys** for Azure Cosmos DB for MongoDB vCore provides the following benefits:
- You fully control data access. You can revoke a key to make a database inaccessible.
- You fully control a key's life cycle to align with corporate policies.
- You can centrally manage and organize all your encryption keys in your own instances of Azure Key Vault.
- Data encryption based on customer-managed keys doesn't negatively affect the performance of your workloads.
- You can implement separation of duties between security officers, database administrators, and system administrators.

## CMK requirements

With **customer-managed encryption key** you assume all the responsibility for maintaining properly configured components required for CMK to work. Hence, you must deploy your own [Azure Key Vault](/azure/key-vault/general/basic-concepts) and provide a [user-assigned managed identity](/entra/identity/managed-identities-azure-resources/overview#managed-identity-types). You must generate or import your own key. You must grant required permissions on the Key Vault, so that your Azure Cosmos DB for MongoDB vCore can perform the necessary actions on the key. You have to take care of configuring all networking aspects of the Azure Key Vault in which the key is kept, so that your Azure Cosmos DB for MongoDB vCore instance can access the key. Auditing access to the key is also your responsibility. 

When you configure customer-managed keys for an Azure Cosmos DB for MonogDB vCore cluster, Azure Storage wraps the root data encryption key (DEK) for the account with the customer-managed key in the associated key vault. The protection of the root encryption key changes, but the data in your Azure Storage account always remains encrypted. There's no extra action required on your part to ensure that your data remains encrypted. Protection by customer-managed keys takes effect immediately.

Azure Key Vault is a cloud-based, external key management system. It's highly available and provides scalable, secure storage for RSA cryptographic keys. It doesn't allow direct access to a stored key, but provides encryption and decryption services to authorized entities. Key Vault can generate the key, import it, or receive it transferred from an on-premises HSM device.

Following is the list of requirements and recommendations for data encryption configuration for Azure Cosmos DB for MongoDB vCore:

- **Key vault**
    - Key vault and Azure Cosmos DB for MongoDB vCore must belong to the same [Microsoft Entra tenant](/entra/identity-platform/developer-glossary#tenant).
    - Recommendation: Set the **Days to retain deleted vaults** setting for Key Vault to *90 days*. This configuration setting can be defined only at key vault creation time. Once an instance is created, it isn't possible to modify this setting.
    - Enable the [`soft-delete` feature](/azure/key-vault/general/soft-delete-overview) in key vault to help you with protecting from data loss, if a key or a key vault instance is accidentally deleted. Key vault retains soft-deleted resources for 90 days unless the user recovers or purges them in the meantime. The recover and purge actions have their own permissions associated with a key vault, an RBAC role, or an access policy permission. The soft-deleted feature is on by default. If you have a key vault that was deployed long time ago, it might still have soft-delete disabled. In that case, you can [turn it on](/azure/key-vault/general/soft-delete-overview#supporting-interfaces).
    - Enable [purge protection](/azure/key-vault/general/best-practices#turn-on-data-protection-for-your-vault) to enforce a mandatory retention period for deleted vaults and vault objects.
- **Key**
    - The key used for encrypting the data encryption key can be only asymmetric, RSA, or RSA-HSM. Key sizes of 2,048, 3,072, and 4,096 are supported. 
        - Recommendation: Use a 4,096-bit key for better security.
    - The date and time for key activation (if set) must be in the past. The date and time for expiration (if set) must be in the future.
    - The key must be in **Enabled** state.
    - If you're importing an existing key into Azure Key Vault, provide it in the supported file formats (`.pfx`, `.byok`, or `.backup`).
- **Permissions**: Grant the Azure Cosmos DB for MongoDB vCore's user-assigned managed identity access to the key by:
  - **Preferred**: Azure Key Vault should be configured with [RBAC permission model](/azure/key-vault/general/rbac-guide) and the managed identity should be assigned the [Key Vault Crypto Service Encryption User](/azure/key-vault/general/rbac-guide#azure-built-in-roles-for-key-vault-data-plane-operations) role.
  - Legacy: If Azure Key Vault is configured with [Access policy permission model](/azure/key-vault/general/assign-access-policy), grant the following permissions to the managed identity:
    - **get**: To retrieve the properties and the public part of the key in key vault.
    - **list**: To list and iterate through the keys stored in key vault.
    - **wrapKey**: To encrypt the data encryption key.
    - **unwrapKey**: To decrypt the data encryption key.

## CMK key version updates

CMK in Azure Cosmos DB for MongoDB vCore supports automatic key version updates, also known as version-less keys. Azure Cosmos DB for MonogoDB vCore service automatically picks up the new key version and reencrypts the data encryption key. This capability can be combined with the Azure Key Vault's [autorotation feature](/azure/key-vault/keys/how-to-configure-key-rotation).

## Considerations

When you're using a customer-managed key for data encryption, follow these recommendations to configure Key Vault:
- To prevent accidental or unauthorized deletion of this critical resource, set a [resource lock](/azure/azure-resource-manager/management/lock-resources) on key vault.
- Review and enable Azure Key Vault [availability and redundancy](/azure/key-vault/general/disaster-recovery-guidance) options.
- Enable [logging](/azure/key-vault/general/howto-logging) and [alerting](/azure/key-vault/general/alert) on Azure Key Vault instance used to store keys. Key vault provides logs that are easy to inject into other security information and event management (SIEM) tools. Azure Monitor Logs is one example of a service that is already integrated.
- [Lock down Key Vault](/azure/key-vault/general/secure-key-vault#network-security) by selecting **Disable public access** and **Allow trusted Microsoft services to bypass this firewall**.

> [!NOTE]  
> After you select **Disable public access** and **Allow trusted Microsoft services to bypass this firewall**, you might get an error similar to the following when you try to use public access to administer Key Vault via the portal: "You have enabled the network access control. Only allowed networks have access to this key vault." This error doesn't preclude the ability to provide keys during customer-managed key setup or fetch keys from Key Vault during cluster operations.

- Keep a copy of the customer manged key in a secure place, or escrow it to the escrow service.
- If Key Vault generates the key, create a [key backup](/azure/key-vault/general/backup) before you use the key for the first time. You can only restore the backup to Key Vault.

### Accidental key access revocation from Azure Key Vault

Someone with sufficient access rights to Key Vault might accidentally disable cluster access to the key by:

- Unassigning the RBAC role **[Key Vault Crypto Service Encryption User](/azure/key-vault/general/rbac-guide#azure-built-in-roles-for-key-vault-data-plane-operations)** or revoking the permissions from the identity that's used to retrieve the key in Key Vault.
- Deleting the key.
- Deleting the Key Vault instance.
- Changing the Key Vault firewall rules.
- Deleting the managed identity of the cluster in Microsoft Entra ID.

### Inaccessible customer-managed key condition

When you configure data encryption with a customer-managed key stored in key vault, continuous access to this key is required for the cluster to stay online. If that's not the case, the cluster changes its state to **Inaccessible** and begins denying all connections.

> [!NOTE]  
> In preview, cluster status may continue to be **Ready** and not change to **Inaccessible**.

Some of the possible reasons why the cluster state might become **Inaccessible** are:

| Cause | Resolution |
| --- | --- |
| Any of the encryption keys pointed by the cluster had an expiry date and time configured, and that date and time is reached. | You must extend the expiry date of the key. Then you must wait for the service to revalidate the key and automatically transition the cluster state to **Ready**. Only when the cluster is back to **Ready** state you can rotate the key to a newer version or create a new key, and update the cluster so that it refers to that new version of the same key or to the new key. |
| You delete the Key Vault instance, the Azure Cosmos DB for MongoDB vCore instance can't access the key and moves to an **Inaccessible** state. | [Recover the Key Vault instance](/azure/key-vault/general/key-vault-recovery) and wait for the service to run the periodical revalidation of the key, and automatically transition the cluster state to **Ready**. |
| You delete, from Microsoft Entra ID, a [managed identity](/azure/active-directory/managed-identities-azure-resources/how-manage-user-assigned-managed-identities) that's used to retrieve any of the encryption keys stored in key vault. | [Recover the identity](/azure/active-directory/fundamentals/recover-from-deletions) and wait for the service to run the periodical revalidation of the key, and automatically transition the cluster state to **Ready**. |
| Your key vault permission model is configured to use role-based access control. You remove the [Key Vault Crypto Service Encryption User](/azure/key-vault/general/rbac-guide#azure-built-in-roles-for-key-vault-data-plane-operations) RBAC role assignment from the [managed identities](/azure/active-directory/managed-identities-azure-resources/how-manage-user-assigned-managed-identities) that are configured to retrieve any of the keys. | Grant the RBAC role again to the [managed identity](/azure/active-directory/managed-identities-azure-resources/how-manage-user-assigned-managed-identities) and wait for the service to run the periodical revalidation of the key, and automatically transition the cluster state to **Ready**. An alternative approach consists of granting the role on the key vault to a different [managed identity](/azure/active-directory/managed-identities-azure-resources/how-manage-user-assigned-managed-identities), and updating the cluster so that it uses this other [managed identity](/azure/active-directory/managed-identities-azure-resources/how-manage-user-assigned-managed-identities) to access the key. |
| Your key vault permission model is configured to use access policies. You revoke the **list**, **get**, **wrapKey**, or **unwrapKey** access policies from the [managed identities](/azure/active-directory/managed-identities-azure-resources/how-manage-user-assigned-managed-identities) that are configured to retrieve any of the keys. | Grant the RBAC role to the managed identity and wait for the service to run the periodical revalidation of the key, and automatically transition the cluster state to **Ready**. An alternative approach consists of granting the required access policies on the key vault to a different managed identity, and updating the cluster so that it uses this other managed identity to access the key. |
| You set up overly restrictive key vault firewall rules, so that your Azure Cosmos DB for MongoDB vCore cluster can't communicate with the key vault to retrieve your keys. | When you configure a key vault firewall, make sure that you select the option to allow [trusted Microsoft services](/azure/key-vault/general/overview-vnet-service-endpoints#trusted-services) so that your Azure Cosmos DB for MongoDB vCore can bypass the firewall. |

> [!NOTE]  
> When a key is disabled, deleted, expired, or not reachable, a cluster that has data encrypted with that key becomes **Inaccessible**, as stated earlier. The cluster state doesn't change to **Ready** again until it can revalidate the encryption keys.
>  
> Generally, a cluster becomes **Inaccessible** within 60 minutes after a key is disabled, deleted, expired, or not reachable. After the key becomes available, the cluster might take up to 60 minutes to become **Ready** again.

### Recovering from managed identity deletion

If the user-assigned managed identity used to access the encryption key stored in key vault is deleted in Microsoft Entra ID, you should follow these steps to recover:
1. [Recover the identity](/azure/active-directory/fundamentals/recover-from-deletions) or create a new managed Entra ID identity.
1. If you created a new identity, even if it has the same name as the deleted one, update the Azure Database for flexible cluster properties so that it knows it has to use this new identity to access the encryption key.
1. Make sure this identity has proper permissions for operations on key in Azure Key Vault (AKV).
1. Wait for about one hour until the cluster revalidates the key.

> [!IMPORTANT]  
> Simply creating new Entra ID identity with the same name as deleted identity doesn't recover from managed identity deletion.

## Related content

- [Follow these steps to enable data encryption at rest with customer-managed key in Azure Cosmos DB for MongoDB vCore](./how-to-data-encryption.md)
- [Migrate data to Azure Cosmos DB for MongoDB vCore](./migration-options.md)