---
title: Troubleshoot encryption at rest with customer-managed key (CMK) in Azure DocumentDB
description: Learn about troubleshooting steps and techniques for CMK on Azure DocumentDB clusters.
author: niklarin
ms.author: nlarin
ms.topic: concept-article
ms.date: 09/04/2025
---

# Troubleshooting data encryption with customer-managed key (CMK) in Azure DocumentDB

This guide is designed to help you troubleshoot common issues when using [customer-managed key (CMK) for data encryption at rest](./database-encryption-at-rest.md#encryption-at-rest-with-service-managed-key-smk-or-customer-managed-key-cmk) with Azure DocumentDB. It offers practical solutions for troubleshooting various components involved in the CMK setup.

A managed identity, a key vault, an encryption key in the key vault, and proper permissions granted to the managed identity [are required](./database-encryption-at-rest.md#cmk-requirements) to configure CMK on an Azure DocumentDB cluster.

If managed identity, key vault, key, or permissions and not configurated as per [the requirements](./database-encryption-at-rest.md#cmk-requirements), you may not be able to enable CMK during cluster provisioning. If proper setup becomes invalid on a CMK-enabled cluster, data on this cluster becomes unavailable due to the core security requirement of encryption with the customer-managed key. 

Follow the steps in this section to troubleshoot all components required for proper CMK setup.

## Reasons for key access revocation from Azure Key Vault

Someone with sufficient access rights to Key Vault might accidentally disable cluster access to the key by:

- Unassigning the RBAC role **[Key Vault Crypto Service Encryption User](/azure/key-vault/general/rbac-guide#azure-built-in-roles-for-key-vault-data-plane-operations)** or revoking the permissions from the identity that's used to retrieve the key in Key Vault.
- Deleting the key.
- Deleting the Key Vault instance.
- Changing the Key Vault firewall rules or otherwise misconfiguring the Key Vault's networking settings.
- Deleting the managed identity of the cluster in Microsoft Entra ID.

These actions cause the customer-managed key used for data encryption to become inaccessible.

## Troubleshooting inaccessible customer-managed key condition

When you configure data encryption with a customer-managed key stored in key vault, continuous access to this key is required for the cluster to stay online. If that's not the case, the cluster changes its state to **Inaccessible** and begins denying all connections.

Some of the possible reasons why the cluster state might become **Inaccessible** are:

| Cause | Resolution |
| --- | --- |
| The encryption key pointed by the cluster had an expiry date and time configured, and that date and time is reached. | You must extend the expiry date of the key. Then you must wait for the service to revalidate the key and automatically transition the cluster state to **Ready**. Only when the cluster is back to **Ready** state you can rotate the key to a newer version or create a new key, and update the cluster so that it refers to that new version of the same key or to the new key. |
| You delete the Key Vault instance, the Azure DocumentDB instance can't access the key and moves to an **Inaccessible** state. | [Recover the Key Vault instance](/azure/key-vault/general/key-vault-recovery) and wait for the service to run the periodical revalidation of the key, and automatically transition the cluster state to **Ready**. |
| You delete, from Microsoft Entra ID, a [managed identity](/azure/active-directory/managed-identities-azure-resources/how-manage-user-assigned-managed-identities) that's used to retrieve any of the encryption keys stored in key vault. | [Recover the identity](/azure/active-directory/fundamentals/recover-from-deletions) and wait for the service to run the periodical revalidation of the key, and automatically transition the cluster state to **Ready**. |
| Your key vault permission model is configured to use role-based access control. You remove the [Key Vault Crypto Service Encryption User](/azure/key-vault/general/rbac-guide#azure-built-in-roles-for-key-vault-data-plane-operations) RBAC role assignment from the [managed identities](/azure/active-directory/managed-identities-azure-resources/how-manage-user-assigned-managed-identities) that are configured to retrieve any of the keys. | Grant the RBAC role again to the [managed identity](/azure/active-directory/managed-identities-azure-resources/how-manage-user-assigned-managed-identities) and wait for the service to run the periodical revalidation of the key, and automatically transition the cluster state to **Ready**. Alternatively, you can grant the role on the key vault to a different [managed identity](/azure/active-directory/managed-identities-azure-resources/how-manage-user-assigned-managed-identities) and update the cluster so that it uses this other [managed identity](/azure/active-directory/managed-identities-azure-resources/how-manage-user-assigned-managed-identities) to access the key. |
| Your key vault permission model is configured to use [access policies](/azure/key-vault/general/troubleshoot-azure-policy-for-key-vault). You revoke the **list**, **get**, **wrapKey**, or **unwrapKey** access policies from the [managed identities](/azure/active-directory/managed-identities-azure-resources/how-manage-user-assigned-managed-identities) that are configured to retrieve any of the keys. | Grant the RBAC role to the managed identity and wait for the service to run the periodical revalidation of the key, and automatically transition the cluster state to **Ready**. Alternatively, you can grant the required access policies on the key vault to a different managed identity and update the cluster so that it uses this other managed identity to access the key. |
| You set up overly restrictive key vault firewall rules, so that your Azure DocumentDB cluster can't communicate with the key vault to retrieve your keys. | When you configure a key vault firewall, make sure that you either disable public access and selected the option to allow [trusted Microsoft services](/azure/key-vault/general/overview-vnet-service-endpoints#trusted-services) or allowed public access from all networks. With public access from all networks your Azure DocumentDB cluster can access the key vault. With disabled public access and the option to allow trusted Microsoft services to access the key value, your cluster can bypass the firewall. |

> [!NOTE]  
> When a key is disabled, deleted, expired, or not reachable, a cluster that has data encrypted with that key becomes **Inaccessible**, as stated earlier. The cluster state doesn't change to **Ready** again until it can revalidate the encryption key.
>  
> Generally, a cluster becomes **Inaccessible** within 60 minutes after a key is disabled, deleted, expired, or not reachable. After the key becomes available, the cluster might take up to 60 minutes to become **Ready** again.

## Recovering from managed identity deletion

If the user-assigned managed identity used to access the encryption key stored in key vault is deleted in Microsoft Entra ID, you should follow these steps to recover:
1. [Recover the identity](/azure/active-directory/fundamentals/recover-from-deletions) or create a new managed Entra ID identity.
1. If you created a new identity, even if it has the same name as the deleted one, update the Azure Database for flexible cluster properties so that it knows it has to use this new identity to access the encryption key.
1. Make sure this identity has proper permissions for operations on key in Azure Key Vault (AKV).
1. Wait for about one hour until the cluster revalidates the key.

> [!IMPORTANT]  
> Creating new Entra ID identity *with the same name* as deleted identity doesn't recover from managed identity deletion.

## Troubleshooting failed CMK-enabled cluster provisioning

If any of [the CMK requirements](./database-encryption-at-rest.md#cmk-requirements) *aren't* met, an attempt to provision a cluster with CMK enabled fails. The following error during cluster provisioning indicates that [the key vault](./database-encryption-at-rest.md#key-vault), the [encryption key](./database-encryption-at-rest.md#encryption-key), or the [permissions for managed identity](./database-encryption-at-rest.md#permissions) weren't set up correctly: 'Couldn't get access to the key. It might be missing, the provided user identity doesn't have GET permissions on it, or the key vault hasn't enabled access to the public internet.'

To troubleshoot this situation:
1. Check all [CMK requirements](./database-encryption-at-rest.md#cmk-requirements).
1. Provision cluster with the managed identity and the key vault that you checked.
1. Delete the failed cluster entity. The failed cluster has `clusterStatus` property set to **Failed**. In the Azure portal, you can find cluster status on the **Overview** blade in the cluster properties.

## Related content

- Learn about [data encryption at rest fundamentals](./database-encryption-at-rest.md)
- Check [the best practices for configuring key vault for CMK](./database-encryption-at-rest.md#considerations)
- [Follow these steps to enable data encryption at rest with customer-managed key in Azure DocumentDB](./how-to-data-encryption.md)
