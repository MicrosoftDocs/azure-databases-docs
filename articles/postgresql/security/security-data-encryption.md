---
title: Data Encryption
description: Learn how data encryption works in Azure Database for PostgreSQL flexible server instances.
author: techlake
ms.author: hganten
ms.reviewer: maghan
ms.date: 08/08/2025
ms.service: azure-database-postgresql
ms.subservice: security
ms.topic: concept-article
ms.custom:
  - horz-security
---

# Data encryption at rest in Azure Database for PostgreSQL

All the data managed by an Azure Database for PostgreSQL flexible server instance is always encrypted at rest. That data includes all system and user databases, server logs, write-ahead log segments, and backups. Encryption is handled by the underlying storage through [Server-side encryption of Azure Disk Storage](/azure/virtual-machines/disk-encryption).

## Encryption at Rest with Service (SMK) or Customer Managed Keys (CMK)

Azure Database for PostgreSQL supports two modes of data encryption at rest: **service managed keys (SMK)** and **customer managed keys (CMK)**. Data encryption with service managed keys is the default mode for Azure Database for PostgreSQL flexible server. In this mode, the service automatically manages the encryption keys used to encrypt your data. You don't need to take any action to enable or manage encryption in this mode.

In the **customer managed keys** mode, you can bring your own encryption key to encrypt your data. This mode gives you more control over the encryption process, but it also requires you to manage the encryption keys yourself. You must deploy your own Azure Key Vault or Azure Key Vault Managed Hardware Security Module (HSM) and configure it to store the encryption keys used by your Azure Database for PostgreSQL flexible server instance.

The mode can only be selected at server creation time. It can't be changed from one mode to another for the lifetime of the server.

To achieve the encryption of your data, Azure Database for PostgreSQL uses [Azure Storage encryption for data at rest](/azure/storage/common/storage-service-encryption). When using CMK, the customer is responsible for providing keys for encrypting and decrypting data in Blob Storage and Azure Files services. These keys must be stored in Azure Key Vault or Azure Key Vault Managed Hardware Security Module (HSM). For more information, see [customer-managed keys for Azure Storage encryption](/azure/storage/common/customer-managed-keys-overview).

## Benefits provided by each mode (SMK or CMK)

Data encryption with **service managed keys** for Azure Database for PostgreSQL provides the following benefits:

- The service automatically and fully controls data access.
- The service automatically and fully controls your key's life cycle, including rotation of the key.
- You don't need to worry about managing data encryption keys.
- Data encryption based on service managed keys doesn't negatively affect the performance of your workloads.
- It simplifies the management of encryption keys (including their regular rotation), and the management of the identities used to access those keys.

Data encryption with **customer managed keys** for Azure Database for PostgreSQL provides the following benefits:

- You fully control data access. You can remove a key to make a database inaccessible.
- You fully control a key's life cycle, including rotation of the key, to align with corporate policies.
- You can centrally manage and organize all your encryption keys in your own instances of Azure Key Vault.
- Data encryption based on customer managed keys doesn't negatively affect the performance of your workloads.
- You can implement separation of duties between security officers, database administrators, and system administrators.

## CMK requirements

With **customer managed encryption key** you assume all the responsibility. Hence, you must deploy your own Azure Key Vault or Azure Key Vault HSM. You must generate or import your own key. You must grant required permissions on the Key Vault, so that your Azure Database for PostgreSQL flexible server instance can perform the necessary actions on the key. You have to take care of configuring all networking aspects of the Azure Key Vault in which the key is kept, so that your Azure Database for PostgreSQL flexible server instance can access the key. Auditing access to the key is also your responsibility. Finally, you're responsible for rotating the key and, when required, updating the configuration of your Azure Database for PostgreSQL flexible server instance so that it references the rotated version of the key.

When you configure customer-managed keys for a storage account, Azure Storage wraps the root data encryption key (DEK) for the account with the customer-managed key in the associated key vault or managed HSM. The protection of the root encryption key changes, but the data in your Azure Storage account remains encrypted always. There's no extra action required on your part to ensure that your data remains encrypted. Protection by customer-managed keys takes effect immediately.

Azure Key Vault is a cloud-based, external key management system. It's highly available and provides scalable, secure storage for RSA cryptographic keys, optionally backed by [FIPS 140 validated](/azure/key-vault/keys/about-keys#compliance) hardware security modules (HSMs). It doesn't allow direct access to a stored key, but provides encryption and decryption services to authorized entities. Key Vault can generate the key, import it, or receive it transferred from an on-premises HSM device.

Following is the list of requirements to configure data encryption for Azure Database for PostgreSQL:

- Key Vault and your Azure Database for PostgreSQL flexible server instance must belong to the same Microsoft Entra tenant. Cross-tenant Key Vault and server interactions aren't supported. Moving the Key Vault resource afterward requires you to reconfigure the data encryption.
- We recommended you to set the **Days to retain deleted vaults** configuration for Key Vault to 90 days. If you configured an existing Key Vault instance with a lower number, it should still be valid. However, if you wish to modify this setting and increase the value, it's necessary to create a new Key Vault instance. Once an instance is created, it isn't possible to modify this setting.
- Enable the soft-deleted feature in Key Vault to help you with protecting from data loss, if a key or a Key Vault instance is accidentally deleted. Key Vault retains soft-deleted resources for 90 days unless the user recovers or purges them in the meantime. The recover and purge actions have their own permissions associated with a Key Vault an RBAC role or an access policy permission. The soft-deleted feature is on by default. If you have some Key Vault which was deployed long time ago, it might still have soft-delete disabled. In that case, you can turn it on using Azure CLI.
- Enable purge protection to enforce a mandatory retention period for deleted vaults and vault objects.
- Grant the Azure Database for PostgreSQL flexible server instance's user assigned managed identity access to the key by:
- **Preferred**: Azure Key Vault should be configured with [RBAC permission model](/azure/key-vault/general/rbac-guide) and the managed identity should be assigned the [Key Vault Crypto Service Encryption User](/azure/key-vault/general/rbac-guide#azure-built-in-roles-for-key-vault-data-plane-operations) role.
- Legacy: If Azure Key Vault is configured with [Access policy permission model](/azure/key-vault/general/assign-access-policy), grant the following permissions to the managed identity:
- **get**: To retrieve the properties and the public part of the key in Key Vault.
- **list**: To list and iterate through the keys stored in Key Vault.
- **wrapKey**: To encrypt the data encryption key.
- **unwrapKey**: To decrypt the data encryption key.
- The key used for encrypting the data encryption key can be only asymmetric, RSA, or RSA-HSM. Key sizes of 2,048, 3,072, and 4,096 are supported. We recommend using a 4,096-bit key for better security.
- The date and time for key activation (if set) must be in the past. The date and time for expiration (if set) must be in the future.
- The key must be in **Enabled** state.
- If you're importing an existing key into Key Vault, provide it in the supported file formats (`.pfx`, `.byok`, or `.backup`).

## CMK key version updates

CMK can be configured with manual key rotation and updates or with automatic key version updates after a manual or automatic key rotation in the Key Vault.

For details see [Configure data encryption with customer managed key during server provisioning](../security/security-configure-data-encryption.md).

> [!IMPORTANT]  
> When you rotate the key to a new version, you must keep the old key available for the reencryption to succeed. While most reencryptions should happen within 30 minutes, we recommend that you wait at least 2 hours before disabling access to the old key version.

### Manual key rotation and updates

When you configure CMK with manual key updates, you must manually update the key version in the Azure Database for PostgreSQL flexible server instance after a manual or automatic key rotation in the Key Vault. The server will continue to use the old key version until you update it. You provision this mode by specifying a key URI including the version `GUID` in the URI. For example, `https://<keyvault-name>.vault.azure.net/keys/<key-name>/<key-version>`. Until recently this was the only option available.

Whenever you manually rotate the key or AKV auto-rotates the key based on its rotation policy, you had to update the CMK property on your PostgreSQL instance. This approach proved to be error-prone work for the operators or required a custom script to handle the rotation, especially when using Key Vault's automatic rotation feature.

### Automatic key version updates

To enable automatic key version updates, use a version-less key URI. This eliminates the need to update the CMK's version property in your PostgreSQL instance after a key rotation. PostgreSQL will automatically pick up the new key version and reencrypt the data encryption key. This is a huge simplification in your key lifecycle management, especially when combined with Key Vault auto-rotation.

To implement using ARM, Bicep, Terraform, Azure PowerShell or Azure CLI, simply omit the version `GUID` from your key URI.

In the Portal select the checkbox to guide the UI to suppress version GUIDs during interactive selection and when validating the URI.

## Recommendations

When you're using a customer managed key for data encryption, follow these recommendations to configure Key Vault:
- To prevent accidental or unauthorized deletion of this critical resource, set a resource lock on Key Vault.
- Enable auditing and reporting on all encryption keys. Key Vault provides logs that are easy to inject into other security information and event management (SIEM) tools. Azure Monitor Logs is one example of a service that's already integrated.
- Lock down Key Vault by selecting **Disable public access** and **Allow trusted Microsoft services to bypass this firewall**.
- Enable automatic key version updates.

> [!NOTE]  
> After you select **Disable public access** and **Allow trusted Microsoft services to bypass this firewall**, you might get an error similar to the following when you try to use public access to administer Key Vault via the portal: "You have enabled the network access control. Only allowed networks have access to this key vault." This error doesn't preclude the ability to provide keys during customer managed key setup or fetch keys from Key Vault during server operations.

- Keep a copy of the customer managed key in a secure place, or escrow it to the escrow service.
- If Key Vault generates the key, create a key backup before you use the key for the first time. You can only restore the backup to Key Vault.

## Special considerations

### Accidental key access revocation from Azure Key Vault

Someone with sufficient access rights to Key Vault, might accidentally disable server access to the key by:

- Unassigning the RBAC role **[Key Vault Crypto Service Encryption User](/azure/key-vault/general/rbac-guide#azure-built-in-roles-for-key-vault-data-plane-operations)** or revoking the permissions from the identity that's used to retrieve the key in Key Vault.
- Deleting the key.
- Deleting the Key Vault instance.
- Changing the Key Vault firewall rules.
- Deleting the managed identity of the server in Microsoft Entra ID.

### Monitoring the keys kept in Azure Key Vault

To monitor the database state, and to turn on alerts for the loss of access to the data encryption protector, configure the following Azure features:

- [Resource health](/azure/service-health/resource-health-overview): A database that lost access to the CMK appears as **Inaccessible** after the first connection to the database is denied.
- [Activity log](/azure/service-health/alerts-activity-log-service-notifications-portal): When access to the CMK in the customer-managed Key Vault instance fails, entries are added to the activity log. You can reinstate access if you create alerts for these events as soon as possible.
- [Action groups](/azure/azure-monitor/alerts/action-groups): Define these groups to receive notifications and alerts based on your preferences.

### Restoring backups of a server configured with a customer managed key

After your Azure Database for PostgreSQL flexible server instance is encrypted with a customer managed key stored in Key Vault, any newly created server copy is also encrypted. You can make this new copy through a [point-in-time restore (PITR)](../backup-restore/concepts-backup-restore.md) operation or read replicas.

When you're setting up data encryption with customer managed key, during operation like restore of a backup or creation of a read replica, you can avoid problems by following these steps on the primary and restored or replica servers:

- Initiate the restore process or the process of creating a read replica from the primary Azure Database for PostgreSQL flexible server instance.
- On the restored or replica server, you can change the customer managed key and the user assigned managed identity that's used to access Key Vault. Ensure that the identity assigned in the newly created server has the required permissions on the Key Vault.
- Don't revoke the original key after restoring. At this time, we don't support key revocation after you restore a server with customer managed key to another server.

### Managed HSMs

Hardware security modules (HSMs) are tamper-resistant hardware devices that help secure cryptographic processes by generating, protecting, and managing keys used for encrypting data, decrypting data, creating digital signatures, and creating digital certificates. HSMs are tested, validated, and certified to the highest security standards, including FIPS 140 and Common Criteria.

Azure Key Vault Managed HSM is a fully managed, highly available, single-tenant, standards-compliant cloud service. You can use it to safeguard cryptographic keys for your cloud applications through [FIPS 140-3 validated HSMs](/azure/key-vault/keys/about-keys#compliance).

When you're creating new Azure Database for PostgreSQL flexible server instances in the Azure portal with the customer managed key, you can choose **Azure Key Vault Managed HSM** as a key store, as an alternative to **Azure Key Vault**. The prerequisites, in terms of user-defined identity and permissions, are the same as with Azure Key Vault (as listed [earlier in this article](#cmk-requirements)). For more information on how to create a Managed HSM instance, its advantages and differences from a shared Key Vault-based certificate store, and how to import keys into Managed HSM, see [What is Azure Key Vault Managed HSM?](/azure/key-vault/managed-hsm/overview).

### Inaccessible customer managed key condition

When you configure data encryption with a customer managed key stored in Key Vault, continuous access to this key is required for the server to stay online. If that's not the case, the server changes its state to **Inaccessible** and begins denying all connections.

Some of the possible reasons why the server state might become **Inaccessible** are:

| Cause | Resolution |
| --- | --- |
| Any of the encryption keys pointed by the server had an expiry date and time configured, and that date and time is reached. | You must extend the expiry date of the key. Then you must wait for the service to revalidate the key and automatically transition the server state to **Ready**. Only when the server is back on **Ready** state you can rotate the key to a newer version or create a new key, and update the server so that it refers to that new version of the same key or to the new key. |
| You rotate the key and forget to update the instance of Azure Database for PostgreSQL flexible server so that it points to the new version of the key. The old key, to which the server is pointing, expires and turns the server state into **Inaccessible**. | To avoid this situation, every time you rotate the key, make sure you also update the instance of your server to point to the new version. To do that, you can use the `az postgres flexible-server update`, following the example that describes ["Change key/identity for data encryption. Data encryption can't be enabled post server creation, this will only update the key/identity."](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-update-examples). If you prefer to update it using the API, you can invoke the [Servers - Update](/rest/api/postgresql/servers/update) endpoint of the service. |
| You delete the Key Vault instance, the Azure Database for PostgreSQL flexible server instance can't access the key and moves to an **Inaccessible** state. | [Recover the Key Vault instance](/azure/key-vault/general/key-vault-recovery) and wait for the service to run the periodical revalidation of the key, and automatically transition the server state to **Ready**. |
| You delete, from Microsoft Entra ID, a [managed identity](/azure/active-directory/managed-identities-azure-resources/how-manage-user-assigned-managed-identities) that's used to retrieve any of the encryption keys stored in Key Vault. | [Recover the identity](/azure/active-directory/fundamentals/recover-from-deletions) and wait for the service to run the periodical revalidation of the key, and automatically transition the server state to **Ready**. |
| Your Key Vault permission model is configured to use role-based access control. You remove the [Key Vault Crypto Service Encryption User](/azure/key-vault/general/rbac-guide#azure-built-in-roles-for-key-vault-data-plane-operations) RBAC role assignment from the [managed identities](/azure/active-directory/managed-identities-azure-resources/how-manage-user-assigned-managed-identities) that are configured to retrieve any of the keys. | Grant the RBAC role again to the [managed identity](/azure/active-directory/managed-identities-azure-resources/how-manage-user-assigned-managed-identities) and wait for the service to run the periodical revalidation of the key, and automatically transition the server state to **Ready**. An alternative approach consists on granting the role on the Key Vault to a different [managed identity](/azure/active-directory/managed-identities-azure-resources/how-manage-user-assigned-managed-identities), and update the server so that it uses this other [managed identity](/azure/active-directory/managed-identities-azure-resources/how-manage-user-assigned-managed-identities) to access the key. |
| Your Key Vault permission model is configured to use access policies. You revoke the **list**, **get**, **wrapKey**, or **unwrapKey** access policies from the [managed identities](/azure/active-directory/managed-identities-azure-resources/how-manage-user-assigned-managed-identities) that are configured to retrieve any of the keys. | Grant the RBAC role again to the managed identity and wait for the service to run the periodical revalidation of the key, and automatically transition the server state to **Ready**. An alternative approach consists on granting the required access policies on the Key Vault to a different managed identity, and update the server so that it uses this other managed identity to access the key. |
| You set up overly restrictive Key Vault firewall rules, so that your Azure Database for PostgreSQL flexible server instance can't communicate with the Key Vault to retrieve your keys. | When you configure a Key Vault firewall, make sure that you select the option to allow [trusted Microsoft services](/azure/key-vault/general/overview-vnet-service-endpoints#trusted-services) so that your Azure Database for PostgreSQL flexible server instance can bypass the firewall. |

> [!NOTE]  
> When a key is disabled, deleted, expired, or not reachable, a server that has data encrypted with that key becomes **Inaccessible**, as stated earlier. The server state doesn't change to **Ready** again until it can revalidate the encryption keys.
>
> Generally, a server becomes **Inaccessible** within 60 minutes after a key is disabled, deleted, expired, or not reachable. After the key becomes available, the server might take up to 60 minutes to become **Ready** again.

### Recovering from managed identity deletion

If the user assigned managed identity used to access the encryption key stored in Key Vault is deleted in Microsoft Entra ID, you should follow these steps to recover:
1. Either [recover the identity](/azure/active-directory/fundamentals/recover-from-deletions) or create a new managed Entra ID identity.
1. If you created a new identity, even if it has the exact same name it had before it was deleted, update the Azure Database for flexible server instance properties so that it knows it has to use this new identity to access the encryption key.
1. Make sure this identity has proper permissions for operations on key in Azure Key Vault (AKV).
1. Wait for around one hour until the server revalidates the key.

> [!IMPORTANT]  
> Simply creating new Entra ID identity with the same name as deleted identity doesn't recover from managed identity deletion.

### Using data encryption with customer managed keys and geo-redundant business continuity features

Azure Database for PostgreSQL supports advanced [data recovery](../flexible-server/concepts-business-continuity.md) features, such as [replicas](../../postgresql/flexible-server/concepts-read-replicas.md) and [geo-redundant backup](../backup-restore/concepts-backup-restore.md). Following are requirements for setting up data encryption with CMKs and these features, in addition to [basic requirements for data encryption with CMKs](#cmk-requirements):
- The geo-redundant backup encryption key needs to be created in a Key Vault instance that must exist in the region where the geo-redundant backup is stored.
- The [Azure Resource Manager REST API](/azure/azure-resource-manager/management/overview) version for supporting geo-redundant backup-enabled CMK servers is 2022-11-01-preview. If you want to use [Azure Resource Manager templates](/azure/azure-resource-manager/templates/overview) to automate the creation of servers that use both encryption with CMKs and geo-redundant backup features, use this API version.
- You can't use the same [user-managed identity](/azure/active-directory/managed-identities-azure-resources/how-manage-user-assigned-managed-identities) to authenticate for the primary database's Key Vault instance and the Key Vault instance that holds the encryption key for geo-redundant backup. To maintain regional resiliency, we recommend that you create the user-managed identity in the same region as the geo-redundant backups.
- If you set up a [read replica database](../flexible-server/concepts-read-replicas.md) to be encrypted with CMKs during creation, its encryption key needs to be in a Key Vault instance in the region where the read replica database resides. The [user-assigned identity](/azure/active-directory/managed-identities-azure-resources/how-manage-user-assigned-managed-identities) to authenticate against this Key Vault instance needs to be created in the same region.

## Limitations

These are the current limitations for configuring the customer managed key in an Azure Database for PostgreSQL flexible server instance:

- You can configure customer managed key encryption only during creation of a new server, not as an update to an existing Azure Database for PostgreSQL flexible server instance. You can [restore a PITR backup to a new server with CMK encryption](../backup-restore/concepts-backup-restore.md#point-in-time-recovery) instead.
- After you configure customer managed key encryption, you can't revert back to system managed key. If you want to revert, you must [restore the server to a new one with data encryption configured with system managed key](../backup-restore/concepts-backup-restore.md#point-in-time-recovery).
- The instance of Azure Key Vault Managed HSM or the instance of Azure Key Vault on which you plan to store the encryption key, must exist in the same region on which the instance of Azure Database for flexible server is being created.

## Related content

- [Configure data encryption](../security/security-configure-data-encryption.md)
