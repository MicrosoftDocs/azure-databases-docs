---
title: Request Quota Increases for Azure Database for MySQL
description: Request quota increases for Azure Database for MySQL - Flexible Server resources by using the self-service Quotas experience or a support request.
author: karla-escobar
ms.author: karlaescobar
ms.reviewer: maghan
ms.date: 05/27/2026
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: troubleshooting
ai-usage: ai-assisted
---

# Request quota increases for Azure Database for MySQL - Flexible Server

The resources in Azure Database for MySQL - Flexible Server have default quotas and limits. If your workload needs more quota than the default value, you have two options to request an increase:

- **Quotas blade in the Azure portal (recommended)**. Use the self-service quota management experience to view current usage, request increases inline, and—for many requests—receive automatic approval within minutes.
- **Support request**. Open a support ticket when the self-service experience can't fulfill your request automatically or when you need quota for many subscriptions at once.

This article describes both paths.

## Request a quota increase by using the Quotas blade (recommended)

The Azure Database for MySQL Flexible Server **Quotas** blade in the Azure portal provides a dedicated experience to:

- View current usage and limits across SKU families and regions.
- Request quota increases tailored to your Azure Database for MySQL Flexible Server deployment.

You can use this experience without filing a support ticket for most scenarios.

### Benefits of the self-service experience

| Benefit | Description |
| --- | --- |
| Self-service | Request quota increases directly from the Azure portal without filing a support ticket for most scenarios. |
| Real-time visibility | View current vCore usage and limits across all SKU families and regions at a glance. |
| Automatic approval | Many quota increase requests are automatically approved within minutes—no waiting for manual review. |
| Inline adjustments | Request increases directly from the quota table, without navigating to a separate page or form. |
| Proactive management | Identify SKU families nearing their limits before they cause deployment failures. |
| Fraud and unusual pattern safeguards | Requests that exceed limits or indicate risk are automatically escalated for review instead of being approved without review. |

### How quotas are organized

Each Azure Database for MySQL Flexible Server compute tier is represented as a separate SKU family. To scale up or down within a specific tier, make sure you have sufficient quota for each applicable SKU family in that tier. Example SKU families include:

- Burstable BS Series vCores
- General Purpose DS Series vCores
- Business Critical DS Series vCores

In the Quotas blade, you can:

- Filter by **region**, **subscription**, **provider**, or **usage**. The provider appears as **Azure Database for MySQL Flexible Server**.
- Group results by **usage**, **quota** (SKU family), or **location** (region).
- Review current usage in vCores to quickly identify SKU families nearing their quota limits.
- Make adjustments inline, without leaving the page.

### Step 1: Open the Quotas blade

1. Sign in to the [Azure portal](https://portal.azure.com).
1. In the search bar at the top, enter **Quotas**.
1. Under **Services**, select **Quotas**.

   :::image type="content" source="media/how-to-request-quota-increase/quotas-blade-search.png" alt-text="Screenshot that shows searching for Quotas in the Azure portal." lightbox="media/how-to-request-quota-increase/quotas-blade-search.png":::

Alternatively, go to **Subscriptions**, select your subscription, and then select **Usage + quotas** in the left menu.

### Step 2: Select the Azure Database for MySQL provider

1. On the **Quotas** page, select **Azure Database for MySQL** from the list of resource providers.

   :::image type="content" source="media/how-to-request-quota-increase/select-mysql-provider.png" alt-text="Screenshot that shows selecting the Azure Database for MySQL provider on the Quotas page." lightbox="media/how-to-request-quota-increase/select-mysql-provider.png":::

1. Use the **Subscription** filter at the top to select the subscription you want to review, and apply additional filters for **regions** as needed.

### Step 3: Review your quota usage and limits

The quota details page displays a table with the following columns:

- **Quota name**—The SKU family name (for example, Burstable BS Series vCores, General Purpose DS Series vCores, or Business Critical DS Series vCores).
- **Region**—The Azure region where the quota applies.
- **Current usage**—The number of vCores currently in use.
- **Limit**—The maximum quota limit for that SKU family.
- **Usage bar**—A visual indicator that shows how much of the quota is consumed.

:::image type="content" source="media/how-to-request-quota-increase/quota-usage-table.png" alt-text="Screenshot that shows the quota usage table with SKU family, region, current usage, limit, and usage bar columns." lightbox="media/how-to-request-quota-increase/quota-usage-table.png":::

Review the usage bars to identify quotas that are nearing their limits. Use the search box to find specific SKU families quickly.

### Step 4: Request a quota increase

Next to the quota you want to increase, select the pen icon. A fly-out window opens where you can submit the quota request.

:::image type="content" source="media/how-to-request-quota-increase/quota-request-flyout.png" alt-text="Screenshot that shows the pen icon and the quota request fly-out window." lightbox="media/how-to-request-quota-increase/quota-request-flyout.png":::

### Step 5: Enter the new limit

The quota type (Azure Database for MySQL Flexible Server SKU family) and current usage are already populated. Your request isn't incremental: enter the **new total limit** that you want to see reflected in the portal.

For example, to request an additional 10 vCores for the Burstable BS Series family when your current limit is 35, enter **45** as the new limit.

1. In **New limit**, enter the desired new limit.
1. The portal indicates whether the request can be automatically approved or requires manual review.

:::image type="content" source="media/how-to-request-quota-increase/quota-new-limit.png" alt-text="Screenshot that shows entering a new limit in the quota request fly-out window." lightbox="media/how-to-request-quota-increase/quota-new-limit.png":::

### Step 6: Submit and monitor the request

1. Select **Submit** to send the request for automatic processing. A processing dialog appears immediately after you submit the request.

   :::image type="content" source="media/how-to-request-quota-increase/quota-processing-dialog.png" alt-text="Screenshot that shows the processing dialog after you submit a quota request." lightbox="media/how-to-request-quota-increase/quota-processing-dialog.png":::

1. If the request can be automatically fulfilled, no support ticket is needed. You receive a confirmation within a few minutes.

   :::image type="content" source="media/how-to-request-quota-increase/quota-auto-approved.png" alt-text="Screenshot that shows a confirmation that the quota request was automatically approved." lightbox="media/how-to-request-quota-increase/quota-auto-approved.png":::

1. If the request can't be automatically fulfilled, you have the option to file a support request with the same information already populated.

   :::image type="content" source="media/how-to-request-quota-increase/quota-support-request-option.png" alt-text="Screenshot that shows the option to file a support request when a quota request can't be automatically fulfilled." lightbox="media/how-to-request-quota-increase/quota-support-request-option.png":::

### Step 7: Verify the quota increase

1. Go back to the **Quotas** blade and select the **Azure Database for MySQL** provider.
1. Confirm that the **Limit** column reflects the new, increased value.
1. If you forget the region or SKU family that was requested, review your notifications pane for the details.

:::image type="content" source="media/how-to-request-quota-increase/quota-verify-limit.png" alt-text="Screenshot that shows the updated Limit value in the Quotas blade after a successful quota increase." lightbox="media/how-to-request-quota-increase/quota-verify-limit.png":::

## Open a support request (fallback)

If the self-service experience can't automatically fulfill your request, or if you need quota for many subscriptions, open a support request instead. When you open a support request from the quota request fly-out, the new limit is already populated for you, and you only need to confirm the region and Azure Database for MySQL Flexible Server SKU family.

When you file a support ticket directly, you interact with the capacity management team for that region, which operates 24x7. You can track the status of your request from the **Help + support** dashboard.

For deployments that need quota for many subscriptions, use issue type **Service and subscription limits (quotas)** with quota type **Quota increase**.

Use the following steps to create a new support request from the Azure portal:

1. Sign in to the Azure portal.
1. From the left menu, select **Help + support**, and then select **Create a support request**.
1. On the **Problem description** tab, fill in the following details:

   - For **Summary**, provide a short description of your request, such as your workload, why the default values aren't sufficient, and any error messages you're observing.
   - For **Issue type**, select **Service and subscription limits (quotas)**.
   - For **Subscription**, select the subscription for which you want to increase the quota.
   - For **Quota type**, select **Azure Database for MySQL Flexible Server**.

   :::image type="content" source="media/how-to-request-quota-increase/request-quota-increase-mysql-flex.png" alt-text="Screenshot of new support request." lightbox="media/how-to-request-quota-increase/request-quota-increase-mysql-flex.png":::

1. On the **Additional details** tab, enter the details for your quota request. The information you provide on this tab is used to further assess your issue and help the support engineer troubleshoot the problem.
1. Fill in the following details in this form:

   - In **Request details**, select **Enter details** and select the relevant **Quota type**. Provide the requested information for your specific quota request, such as Location, Series, and New quota.
   - **File upload**: Upload diagnostic files or any other files that you think are relevant to the support request. To learn more about file upload guidance, see the [Azure support](/azure/azure-portal/supportability/how-to-manage-azure-support-request#upload-files) article.
   - **Allow collection of advanced diagnostic information?**: Choose **Yes** or **No**.
   - **Severity**: Choose one of the available severity levels based on the business impact.
   - **Preferred contact method**: Choose to be contacted by **Email** or **Phone**.

1. Fill out the remaining details, such as your availability, support language, contact information, email, and phone number.
1. Select **Next: Review + create**. Validate the information you provided, and then select **Create** to create the support request.

The Azure Database for MySQL - Flexible Server support team processes all quota requests in 24-48 hours.

## Known limitations

If you close the quota request fly-out window, in-portal notifications for that request stop. The underlying request still completes, and you can view the outcome by returning to the Quotas blade and checking the updated limit. To rely on notifications for alerts, leave the quota request window open for the few minutes that it takes to process.

## Related content

- [Create an Azure Database for MySQL - Flexible Server instance in the portal](/azure/mysql/flexible-server/quickstart-create-server-portal)
- [Service limitations](/azure/mysql/flexible-server/concepts-limitations)
