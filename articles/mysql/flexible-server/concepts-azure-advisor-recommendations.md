---
title: Azure Advisor
description: Learn about how Azure Advisor is applied to Azure Database for MySQL - Flexible Server and get answers to common questions.
author: SudheeshGH
ms.author: sunaray
ms.reviewer: maghan
ms.date: 11/27/2024
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: article
ms.custom: sfi-image-nochange
---

# Azure Advisor for Azure Database for MySQL - Flexible Server

Learn about how Azure Advisor is applied to Azure Database for MySQL Flexible Server and get answers to common questions.

## What is Azure Advisor for MySQL?

Azure Advisor system uses telemetry to issue performance and reliability recommendations for your MySQL database.  
Advisor recommendations are split among our MySQL database offerings:

- Azure Database for MySQL single server
- Azure Database for MySQL Flexible Server

Some recommendations are common to multiple product offerings, while other recommendations are based on product-specific optimizations.

## Where can I view my recommendations?

Recommendations are available from the **Overview** navigation sidebar in the Azure portal. A preview will appear as a banner notification, and details can be viewed in the **Notifications** section located just below the resource usage graphs.

:::image type="content" source="media/concepts-azure-advisor-recommendations/advisor-example.png" alt-text="Screenshot of the Azure portal showing an Azure Advisor recommendation." lightbox="media/concepts-azure-advisor-recommendations/advisor-example.png":::

## Recommendation types

Azure Database for MySQL Flexible Server prioritizes the following types of recommendations:

- **Performance**: To improve the speed of your MySQL server. This includes CPU usage, memory pressure, connection pooling, disk utilization, and product-specific server parameters. For more information, see [Advisor Performance recommendations](/azure/advisor/advisor-performance-recommendations).
- **Reliability**: To ensure and improve the continuity of your business-critical databases. This includes storage limit and connection limit recommendations. For more information, see [Advisor Reliability recommendations](/azure/advisor/advisor-high-availability-recommendations).
- **Cost**: To optimize and reduce your overall Azure spending. This includes server right-sizing recommendations. For more information, see [Advisor Cost recommendations](/azure/advisor/advisor-cost-recommendations).

<a id="understanding-your-recommendations"></a>

## Understand your recommendations

- **Daily schedule**: For Azure Database for MySQL Flexible Server databases, we check server telemetry and issue recommendations on a daily schedule. If you make a change to your server configuration, existing recommendations will remain visible until we re-examine telemetry on the following day.
- **Performance history**: Some of our recommendations are based on performance history. These recommendations will only appear after a server has been operating with the same configuration for 7 days. This allows us to detect patterns of heavy usage (e.g. high CPU activity or high connection volume) over a sustained time period. If you provision a new server or change to a new vCore configuration, these recommendations will be paused temporarily. This prevents legacy telemetry from triggering recommendations on a newly reconfigured server. However, this also means that performance history-based recommendations might not be identified immediately.

## Next step

> [!div class="nextstepaction"]
> [Azure Advisor Overview](/azure/advisor/advisor-overview)
