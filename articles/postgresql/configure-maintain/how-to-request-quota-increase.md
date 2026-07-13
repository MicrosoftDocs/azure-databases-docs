---
title: How to request a quota increase in Azure Database for PostgreSQL Flexible Server
description: Learn how to request a quota increase for Azure Database for PostgreSQL flexible server. You also learn how to enable a subscription to access a region.
#customer intent: As a user, I want to request a quota increase for my PostgreSQL flexible server, so that my workload has the resources it needs to run.
author: kabharati
ms.author: kabharati
ms.reviewer: maghan
ms.date: 07/08/2026
ms.service: azure-database-postgresql
ms.subservice: configuration
ms.topic: how-to
ai-usage: ai-assisted
---

# Request quota increases for Azure Database for PostgreSQL flexible server

The resources in Azure Database for PostgreSQL flexible server have default quotas and limits. However, your workload might need more quota than the default value. In this case, contact the Azure Database for PostgreSQL flexible server team to request a quota increase. This article explains how to request a quota increase for Azure Database for PostgreSQL flexible server resources. 

## Create a new support request

To request a quota increase, create a new support request with your workload details. The Azure Database for PostgreSQL flexible server team reviews your request and approves or denies it. Use the following steps to create a new support request from the Azure portal:

1. Sign in to the Azure portal.

1. From the left-hand menu, select **Help + support** and then select **Create a support request**.

1. In the **Problem Description** tab, enter the following details:

   * For **Summary**, provide a short description of your request such as your workload, why the default values aren't sufficient, and any error messages you're observing.
   * For **Issue type**, select **Service and subscription limits (quotas)**.
   * For **Subscription**, select the subscription for which you want to increase the quota.
   * For **Quota type**, select **Azure Database for PostgreSQL flexible server**.

   :::image type="content" source="./media/how-to-create-support-request-quota-increase/create-quota-increase-request.png" alt-text="Create a new Azure Database for PostgreSQL flexible server request for quota increase.":::

1. In the **Additional Details** tab, enter the details corresponding to your quota request. The information you provide on this tab helps the support engineer assess your issue and troubleshoot the problem.

   
1. Fill in the following details in this form:

   * In  **Request details**, select **Enter details** and choose the relevant **Quota Type**.

   Provide the requested information for your specific quota request, such as Location, Series, and New Quota.

   * **File upload**: Upload the diagnostic files or any other files that you think are relevant to the support request. To learn more about the file upload guidance, see the [Azure support](/azure/azure-portal/supportability/how-to-manage-azure-support-request#upload-files) article.

   * **Allow collection of advanced ​diagnostic information?​**: Choose Yes or No.

   * **Severity**: Choose one of the available severity levels based on the business impact.

   * **Preferred contact method**: Choose to be contacted over **Email** or by **Phone**.

1. Fill out the remaining details such as your availability, support language, contact information, email, and phone number on the form.

1. Select **Next: Review+Create**. Validate the information you provided and select **Create** to create a support request.

The Azure Database for PostgreSQL flexible server support team processes all quota requests in 24 to 48 hours.

## Related content

- [Manage Azure Database for PostgreSQL flexible server using the Azure portal](how-to-manage-server-portal.md).
- [Limits in Azure Database for PostgreSQL flexible server](concepts-limits.md).
