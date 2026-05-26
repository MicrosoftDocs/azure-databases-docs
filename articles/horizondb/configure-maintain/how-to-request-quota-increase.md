---
title: How to Request a Quota Increase in Azure HorizonDB
description: Learn how to request a quota increase for Azure HorizonDB. You also learn how to enable a subscription to access a region.
author: avnishrastogimsft
ms.author: avrastog
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-database-postgresql
ms.subservice: configuration
ms.topic: how-to
---

# Request quota increases in Azure HorizonDB

The resources in Azure HorizonDB have default quotas/limits. However, there might be a case where your workload needs more quota than the default value. In such case, you must reach out to the Azure HorizonDB team to request a quota increase. This article explains how to request a quota increase for Azure HorizonDB resources.

## Create a new support request

To request a quota increase, you must create a new support request with your workload details. The Azure HorizonDB team then processes your request and approves or denies it. Use the following steps to create a new support request from the Azure portal:

1. Sign into the Azure portal.

1. From the left-hand menu, select **Help + support** and then select **Create a support request**.

1. In the **Problem Description** tab, fill the following details:

   - For **Summary**, Provide a short description of your request such as your workload, why the default values aren't sufficient along with any error messages you're observing.
   - For **Issue type**, select **Service and subscription limits (quotas)**
   - For **Subscription**, select the subscription for which you want to increase the quota.
   - For **Quota type**, select **Azure HorizonDB**

   :::image type="content" source="media/how-to-request-quota-increase/create-quota-increase-request.png" alt-text="Screenshot of create a new Azure HorizonDB request for quota increase." lightbox="media/how-to-request-quota-increase/create-quota-increase-request.png" :::

1. In the **Additional Details** tab, enter the details corresponding to your quota request. The Information provided on this tab will be used to further assess your issue and help the support engineer troubleshoot the problem.

1. Fill the following details in this form:

   - In **Request details** select **Enter details** and select the relevant **Quota Type**

   provide the requested information for your specific quota request like Location, Series, New Quota.

   - **File upload**: Upload the diagnostic files or any other files that you think are relevant to the support request. To learn more on the file upload guidance, see the [Azure support](/azure/azure-portal/supportability/how-to-manage-azure-support-request#upload-files) article.

   - **Allow collection of advanced ​diagnostic information?​**: Choose Yes or NO

   - **Severity**: Choose one of the available severity levels based on the business impact.

   - **Preferred contact method**: You can either choose to be contacted over **Email** or by **Phone**.

1. Fill out the remaining details such as your availability, support language, contact information, email, and phone number on the form.

1. Select **Next: Review+Create**. Validate the information provided and select **Create** to create a support request.

The Azure HorizonDB support team processes all quota requests in 24-48 hours.

## Related content

- [Create an Azure HorizonDB cluster](quickstart-create-cluster.md)
