---
title: Encryption at rest in Azure DocumentDB
description: Learn about encryption of data in Azure DocumentDB databases using service-managed and customer-managed encryption keys.
author: niklarin
ms.author: nlarin
ms.topic: concept-article
ms.date: 09/01/2025
---

# Data encryption in Azure DocumentDB

All the data managed by an Azure DocumentDB is always encrypted at rest. That data includes all system and user databases, temporary files, logs, and backups.

## Encryption at rest with service-managed key (SMK) or customer-managed key (CMK)

Azure DocumentDB supports two modes of data encryption at rest: **service-managed keys (SMK)** and **customer-managed keys (CMK)**. Data encryption with service-managed keys is the default mode for Azure DocumentDB. In this mode, the service automatically manages the encryption keys used to encrypt your data. You don't need to take any action to enable or manage encryption in this mode.

In the **customer-managed keys** mode, you can bring your own encryption key to encrypt your data. When you specify a customer-managed key, that key is used to protect and control access to the key that encrypts your data. Customer-managed keys offer greater flexibility to manage access controls. You must deploy your own Azure Key Vault and configure it to store the encryption keys used by your Azure DocumentDB cluster.

The configuration mode can only be selected at cluster creation time. It can't be changed from one mode to another for the lifetime of the cluster.

To achieve the encryption of your data, Azure DocumentDB uses [server-side encryption of Azure Storage for data at rest](/azure/virtual-machines/disk-encryption). When using CMK, you're responsible for providing keys for encrypting and decrypting data in Azure Storage services. These keys must be stored in Azure Key Vault. 

## Benefits provided by each mode (SMK or CMK)

Data encryption with **service-managed keys** for Azure DocumentDB provides the following benefits:
- The service automatically and fully controls data access.
- The service automatically and fully controls your key's life cycle, including rotation of the key.
- You don't need to worry about managing data encryption keys.
- Data encryption based on service-managed keys doesn't negatively affect the performance of your workloads.
- It simplifies the management of encryption keys (including their regular rotation), and the management of the identities used to access those keys.

Data encryption with **customer-managed keys** for Azure DocumentDB provides the following benefits:
- You fully control data access. You can revoke a key to make a database inaccessible.
- You fully control a key's life cycle to align with corporate policies.
- You can centrally manage and organize all your encryption keys in your own instances of Azure Key Vault.
- Data encryption based on customer-managed keys doesn't negatively affect the performance of your workloads.
- You can implement separation of duties between security officers, database administrators, and system administrators.

## CMK requirements

With **customer-managed encryption key** you assume all the responsibility for maintaining properly configured components required for CMK to work. Hence, you must deploy your own [Azure Key Vault](/azure/key-vault/general/basic-concepts) and provide a [user-assigned managed identity](/entra/identity/managed-identities-azure-resources/overview#managed-identity-types). You must generate or import your own key. You must grant required permissions on the Key Vault, so that your Azure DocumentDB can perform the necessary actions on the key. You have to take care of configuring all networking aspects of the Azure Key Vault in which the key is kept, so that your Azure DocumentDB instance can access the key. Auditing access to the key is also your responsibility. 

When you configure customer-managed keys for an Azure DocumentDB for MonogDB cluster, Azure Storage wraps the root data encryption key (DEK) for the account with the customer-managed key in the associated key vault. The protection of the root encryption key changes, but the data in your Azure Storage account always remains encrypted. There's no extra action required on your part to ensure that your data remains encrypted. Protection by customer-managed keys takes effect immediately.

Azure Key Vault is a cloud-based, external key management system. It's highly available and provides scalable, secure storage for RSA cryptographic keys. It doesn't allow direct access to a stored key, but provides encryption and decryption services to authorized entities. Key Vault can generate the key, import it, or receive it transferred from an on-premises HSM device.

Following is the list of requirements and recommendations for data encryption configuration for Azure DocumentDB:

### Key vault

The key vault used for CMK setup must meet the following requirements:

  - Key vault and Azure DocumentDB must belong to the same [Microsoft Entra tenant](/entra/identity-platform/developer-glossary#tenant).
  - Recommendation: Set the **Days to retain deleted vaults** setting for Key Vault to *90 days*. This configuration setting can be defined only at key vault creation time. Once an instance is created, it isn't possible to modify this setting.
  - Enable the [`soft-delete` feature](/azure/key-vault/general/soft-delete-overview) in key vault to help you with protecting from data loss, if a key or a key vault instance is accidentally deleted. Key vault retains soft-deleted resources for 90 days unless the user recovers or purges them in the meantime. The recover and purge actions have their own permissions associated with a key vault, a role-based access control (RBAC) role, or an access policy permission. The soft-deleted feature is on by default. If you have a key vault that was deployed long time ago, it might still have soft-delete disabled. In that case, you can [turn it on](/azure/key-vault/general/soft-delete-overview#supporting-interfaces).
  - Enable [purge protection](/azure/key-vault/general/best-practices#turn-on-data-protection-for-your-vault) to enforce a mandatory retention period for deleted vaults and vault objects.
  - Configure networking access to allow your cluster to access the encryption key in the key vault. Use one of the following configuration options:
      - **Allow public access from all networks** lets all hosts on the Internet to access the key vault.
      - Select **Disable public access** and **Allow trusted Microsoft services to bypass this firewall** to disable all public access but to allow your cluster to access the key vault.

### Encryption key

The encryption key selected for CMK configuration must meet the following requirements:

  - The key used for encrypting the data encryption key can be only asymmetric, RSA, or RSA-HSM. Key sizes of 2,048, 3,072, and 4,096 are supported. 
      - Recommendation: Use a 4,096-bit key for better security.
  - The date and time for key activation (if set) must be in the past. The date and time for expiration (if set) must be in the future.
  - The key must be in **Enabled** state.
  - If you're importing an existing key into Azure Key Vault, provide it in the supported file formats (`.pfx`, `.byok`, or `.backup`).

### Permissions

Grant the Azure DocumentDB's user-assigned managed identity access to the encryption key:
  - **Preferred**: Azure Key Vault should be configured with [RBAC permission model](/azure/key-vault/general/rbac-guide) and the managed identity should be assigned the [Key Vault Crypto Service Encryption User](/azure/key-vault/general/rbac-guide#azure-built-in-roles-for-key-vault-data-plane-operations) role.
  - **Legacy**: If Azure Key Vault is configured with [Access policy permission model](/azure/key-vault/general/assign-access-policy), grant the following permissions to the managed identity:
    - **get**: To retrieve the properties and the public part of the key in key vault.
    - **list**: To list and iterate through the keys stored in key vault.
    - **wrapKey**: To encrypt the data encryption key.
    - **unwrapKey**: To decrypt the data encryption key.

## CMK key version updates

CMK in Azure DocumentDB supports automatic key version updates, also known as version-less keys. Azure DocumentDB service automatically picks up the new key version and reencrypts the data encryption key. This capability can be combined with the Azure Key Vault's [autorotation feature](/azure/key-vault/keys/how-to-configure-key-rotation).

## Considerations

When you're using a customer-managed key for data encryption, follow these recommendations to configure Key Vault:
- To prevent accidental or unauthorized deletion of this critical resource, set an [Azure resource lock](/azure/azure-resource-manager/management/lock-resources) on key vault.
- Review and enable Azure Key Vault [availability and redundancy](/azure/key-vault/general/disaster-recovery-guidance) options.
- Enable [logging](/azure/key-vault/general/howto-logging) and [alerting](/azure/key-vault/general/alert) on Azure Key Vault instance used to store keys. Key vault provides logs that are easy to inject into other security information and event management (SIEM) tools. Azure Monitor Logs is one example of a service that is already integrated.
- Enable [key autorotation](/azure/key-vault/keys/how-to-configure-key-rotation). Azure DocumentDB service always picks up the latest version of the selected key. 
- [Lock down public networking access to Key Vault](/azure/key-vault/general/secure-key-vault#network-security) by selecting **Disable public access** and **Allow trusted Microsoft services to bypass this firewall**.

> [!NOTE]  
> After you select **Disable public access** and **Allow trusted Microsoft services to bypass this firewall**, you might get an error similar to the following when you try to use public access to administer Key Vault via the portal: "You enabled the network access control. Only allowed networks have access to this key vault." This error doesn't preclude the ability to provide keys during customer-managed key setup or fetch keys from Key Vault during cluster operations.

- Keep a copy of the customer manged key in a secure place, or escrow it to an escrow service.
- If Key Vault generates the key, create a [key backup](/azure/key-vault/general/backup) before you use the key for the first time. You can only restore the backup to Key Vault.

## Related content

- Follow [these steps to enable data encryption at rest with customer-managed key in Azure DocumentDB](./how-to-data-encryption.md)
- [Troubleshoot CMK setup](./how-to-database-encryption-troubleshoot.md)
- [Migrate data to Azure DocumentDB](./migration-options.md)
