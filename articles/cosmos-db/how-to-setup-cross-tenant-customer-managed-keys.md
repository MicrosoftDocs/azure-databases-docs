---
title: Configure cross-tenant customer-managed keys for your Azure Cosmos DB account with Azure Key Vault (preview)
description: Learn how to configure encryption with customer-managed keys for Azure Cosmos DB using an Azure Key Vault that resides in a different tenant.
author: iriaosara
ms.author: iriaosara
ms.service: azure-cosmos-db
ms.custom: devx-track-azurecli, devx-track-azurepowershell, devx-track-arm-template
ms.topic: how-to
ms.date: 09/27/2022
appliesto:
  - ✅ NoSQL
  - ✅ MongoDB
  - ✅ Apache Cassandra
  - ✅ Apache Gremlin
  - ✅ Table
---

# Configure cross-tenant customer-managed keys for your Azure Cosmos DB account with Azure Key Vault

Data stored in your Azure Cosmos DB account is automatically and seamlessly encrypted with service-managed keys managed by Microsoft. However, you can choose to add a second layer of encryption with keys you manage. These keys are known as customer-managed keys (or CMK). Customer-managed keys are stored in an Azure Key Vault instance.

This article walks through how to configure encryption with customer-managed keys at the time that you create an Azure Cosmos DB account. In this example cross-tenant scenario, the Azure Cosmos DB account resides in a tenant managed by an Independent Software Vendor (ISV) referred to as the service provider. The key used for encryption of the Azure Cosmos DB account resides in a key vault in a different tenant that the customer manages.


[!INCLUDE [entra-msi-cross-tenant-cmk-overview](~/reusable-content/ce-skilling/azure/includes/entra-msi-cross-tenant-cmk-overview.md)]

[!INCLUDE [entra-msi-cross-tenant-cmk-create-identities-authorize-key-vault](~/reusable-content/ce-skilling/azure/includes/entra-msi-cross-tenant-cmk-create-identities-authorize-key-vault.md)]

## Create a new Azure Cosmos DB account encrypted with a key from a different tenant


Up to this point, you configured the multitenant application on the service provider's tenant. You also installed the application on the customer's tenant and configured the key vault and key on the customer's tenant. Next you can create an Azure Cosmos DB account on the service provider's tenant and configure customer-managed keys with the key from the customer's tenant.

When creating an Azure Cosmos DB account with customer-managed keys, we must ensure that it has access to the keys the customer used. In single-tenant scenarios, either give direct key vault access to the Azure Cosmos DB principal or use a specific managed identity. In a cross-tenant scenario, we can no longer depend on direct access to the key vault as it is in another tenant managed by the customer. This constraint is the reason in the previous sections we created a cross-tenant application and registered a managed identity inside the application to give it access to the customer's key vault. This managed identity, coupled with the cross-tenant application ID, is what we use when creating the cross-tenant CMK Azure Cosmos DB Account. For more information, see the [Phase 3 - The service provider encrypts data in an Azure resource using the customer-managed key](#phase-3---the-service-provider-encrypts-data-in-an-azure-resource-using-the-customer-managed-key) section of this article.

Whenever a new version of the key is available in the key vault, it is automatically updated on the Azure Cosmos DB account.

## Using Azure Resource Manager JSON templates

Deploy an ARM template with the following specific parameters:

> [!NOTE]
> If you're recreating this sample in one of your Azure Resource Manager templates, use an `apiVersion` of `2022-05-15`.

| Parameter | Description | Example value |
| --- | --- | --- |
| `keyVaultKeyUri` | Identifier of the customer-managed key residing in the service provider's key vault. | `https://my-vault.vault.azure.com/keys/my-key` |
| `identity` | Object specifying that the managed identity should be assigned to the Azure Cosmos DB account. | `"identity":{"type":"UserAssigned","userAssignedIdentities":{"/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourcegroups/my-resource-group/providers/Microsoft.ManagedIdentity/userAssignedIdentities/my-identity":{}}}` |
| `defaultIdentity` | Combination of the resource ID of the managed identity and the application ID of the multitenant Microsoft Entra application. | `UserAssignedIdentity=/subscriptions/ffffffff-eeee-dddd-cccc-bbbbbbbbbbb0/resourcegroups/my-resource-group/providers/Microsoft.ManagedIdentity/userAssignedIdentities/my-identity&FederatedClientId=aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e` |

Here's an example of a template segment with the three parameters configured:

```json
{
  "kind": "GlobalDocumentDB",
  "location": "East US 2",
  "identity": {
    "type": "UserAssigned",
    "userAssignedIdentities": {
      "/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourcegroups/my-resource-group/providers/Microsoft.ManagedIdentity/userAssignedIdentities/my-identity": {}
    }
  },
  "properties": {
    "locations": [
      {
        "locationName": "East US 2",
        "failoverPriority": 0,
        "isZoneRedundant": false
      }
    ],
    "databaseAccountOfferType": "Standard",
    "keyVaultKeyUri": "https://my-vault.vault.azure.com/keys/my-key",
    "defaultIdentity": "UserAssignedIdentity=/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourcegroups/my-resource-group/providers/Microsoft.ManagedIdentity/userAssignedIdentities/my-identity&FederatedClientId=aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e"
  }
}
```

> [!IMPORTANT]
> This feature isn't yet supported in Azure PowerShell, Azure CLI, or the Azure portal.

You can't configure customer-managed keys with a specific version of the key version when you create a new Azure Cosmos DB account. The key itself must be passed with no versions and no trailing backslashes.

To Revoke or Disable customer-managed keys, see [configure customer-managed keys for your Azure Cosmos DB account with Azure Key Vault](how-to-setup-customer-managed-keys.md)

## FAQs

**How do I migrate an Azure Cosmos DB account with Customer Managed Keys enabled to a different resource group or to a different subscription?**

As a prerequisite, make sure the account is in an Active state. Accounts in a Revoked state can't be migrated.

The general guideline to migrate a Cosmos DB account to a different resource group or subscription is described in the [moving Azure resources to a new resource group or subscription](/azure/azure-resource-manager/management/move-resource-group-and-subscription) article.

After you've successfully moving the Azure Cosmos DB account per the general guideline, any identities (System-Assigned or User-Assigned) associated with the account must be [reassigned](how-to-setup-managed-identity.md). This reassignment is required in order to ensure that these identities continue to have the necessary permissions to access the Key Vault key.

**How do I migrate an Azure Cosmos DB account to a different tenant?**

If your Cosmos DB account has Customer Managed Keys enabled, you can only migrate the account if it's a cross-tenant customer-managed key account. For more information, see the guide on [configuring cross-tenant customer-managed keys for your Azure Cosmos DB account with Azure Key Vault](how-to-setup-cross-tenant-customer-managed-keys.md).

> [!WARNING]
> After migrating, it's crucial to keep the Azure Cosmos DB account and the Azure Key Vault in separate tenants to preserve the original cross-tenant relationship. Ensure the Key Vault key remains in place until the Cosmos DB account migration is complete.

## See also

- [Configure customer-managed keys for your Azure Cosmos account with Azure Key Vault](how-to-setup-cmk.md)
