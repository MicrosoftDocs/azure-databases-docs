---
title: Resolve Capacity Errors
description: The article describes how you can resolve capacity errors when deploying or scaling Azure Database for MySQL - Flexible Server.
author: karla-escobar
ms.author: karlaescobar
ms.reviewer: maghan
ms.date: 06/26/2025
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: troubleshooting
ai-usage: ai-assisted
---

# Resolve capacity errors for Azure Database for MySQL

The article describes how you can resolve capacity errors when deploying or scaling Azure Database for MySQL - Flexible Server.

## Exceeded quota

**Error message(s):**
- Not enough quota to provision or update the server for your subscription.

**Resolution:**
[Submit a request to increase your quota](how-to-request-quota-increase.md).

For more information on quota concepts, see the [Azure Quotas Documentation](/azure/quotas/).

## Subscription access

**Error message(s):**
- Provisioning in the requested region isn't supported.

**Cause:**  
Your subscription may not have access to create a server in the selected region if it isn't registered with the MySQL resource provider (RP).

**Resolution:**
[Register the MySQL resource provider to your subscription](#register-the-mysql-resource-provider-to-your-subscription) to resolve it.

## Enable region

**Error message(s):**
- Subscriptions aren't available for provisioning in this region.
- Provisioning is restricted in this region.
- The region is at capacity or has restrictions in place.

Your subscription might not have access to create a server in the selected region.

**Resolution:**
[File a support request](https://ms.portal.azure.com/#blade/Microsoft_Azure_Support/HelpAndSupportBlade) to gain access to the selected region.

## Availability zone not supported

**Error message(s):**
- Specified Availability Zone not supported in this region.

**Resolution:**  
Select a different availability zone or [file a support request](https://ms.portal.azure.com/#blade/Microsoft_Azure_Support/HelpAndSupportBlade) for additional assistance in gaining access to the specified availability zone.

## SKU not available

**Error message(s):**
- The specified VM family isn't supported in this region.
- Provisioning for specific server SKUs isn't supported.
- Specified SKU not supported in this region.

**Resolution:**  
Choose a different SKU if unavailable. Submit a support request at [https://ms.portal.azure.com/#blade/Microsoft_ABlade](https://ms.portal.azure.com/#blade/Microsoft_ABlade). Requests are reviewed on a case-by-case basis.

The availability of SKUs may differ across regions; either the specific SKU isn't supported in the region or is temporarily unavailable.

If you see the following errors,
- The specified virtual machine family isn't supported in this region.

## Regional constraints

**Error message(s):**
- The region is restricted.
- The region is out of capacity.
- Provisioning is restricted in this region. Choose a different region. For exceptions to this rule, open a support request with the Issue type of 'Service and subscription limits'.
- Subscriptions aren't available for provisioning in this region. Choose a different region. For exceptions to this rule, open a support request with the Issue type of 'Service and subscription limits'.

**Resolution:**  
Your subscription might not have access to create a server in the selected region.[Submit a support request](https://ms.portal.azure.com/#blade/Microsoft_ABlade). Requests are reviewed on a case-by-case basis.

## Register the MySQL resource provider to your subscription

To deploy the Azure Database for MySQL resources, register your subscription with the MySQL resource provider (RP) in the Azure portal.

You can register your subscription using the Azure portal, [the Azure CLI](/cli/azure/install-azure-cli), or [Azure PowerShell](/PowerShell/azure/install-azure-powershell).

#### [Azure portal](#tab/portal)

To register your subscription in the Azure portal, follow these steps:

1. In the Azure portal, select **More services.**

1. Go to **Subscriptions** and select your subscription.

1. On the **Subscriptions** page, in the left hand pane under **Settings** select **Resource providers.**

1. Enter **MySQL** in the filter to bring up the MySQL-related extensions.

1. Select **Register**, **Re-register**, or **Unregister** for the **Microsoft.DBforMySQL** provider, depending on your desired action.

   :::image type="content" source="media/resolve-capacity-errors/resource-provider-screen.png" alt-text="Screenshot of register mysql resource provider screen." lightbox="media/resolve-capacity-errors/resource-provider-screen.png":::

#### [Azure CLI](#tab/azure-cli)

To register your subscription using [the Azure CLI](/cli/azure/install-azure-cli), run this cmdlet:

```azurecli-interactive
az provider register --namespace Microsoft.DBforMySQL
```

#### [Azure PowerShell](#tab/powershell)

To register your subscription using [Azure PowerShell](/powershell/azure/install-az-ps), run this cmdlet:

```powershell
Register-AzResourceProvider -ProviderNamespace Microsoft.DBforMySQL
```

## Other provisioning issues

If you're still experiencing provisioning issues, open a **Region** access request under the support article of Azure Database for MySQL - Flexible Server and specify the vCores you want to utilize.

## Azure program regions

Azure Program offerings (Azure Pass, Imagine, Azure for Students, MPN, BizSpark, BizSpark Plus, Microsoft for Startups / Sponsorship Offers, Microsoft Developer Network(MSDN) / Visual Studio Subscriptions) have access to a limited set of regions.

If your subscription is part of the above offerings and you require access to any of the listed regions, submit an access request. Alternatively, you might opt for an alternate region:

Australia Central, Australia Central 2, Australia SouthEast, Brazil SouthEast, Canada East, China East, China North, China North 2, France South, Germany North, Japan West, India Central, India West, Korea South, Norway West, South Africa West, South India, Switzerland West, UAE Central, UK West, US DoD Central, US DoD East, US Gov Arizona, US Gov Texas, West Central US, West India.

## Related content

- [Azure subscription and service limits, quotas, and constraints](/azure/azure-resource-manager/management/azure-subscription-service-limits)
