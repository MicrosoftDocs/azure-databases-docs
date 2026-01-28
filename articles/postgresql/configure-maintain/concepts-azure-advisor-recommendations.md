---
title: Azure Advisor
description: Learn about Azure Advisor recommendations for your Azure Database for PostgreSQL flexible server instance.
author: danyal-bukhari
ms.author: dabukhari
ms.reviewer: maghan
ms.date: 04/02/2025
ms.service: azure-database-postgresql
ms.subservice: configuration
ms.topic: concept-article
ms.custom: sfi-image-nochange
---

# Azure Advisor for Azure Database for PostgreSQL

Learn about how Azure Advisor is applied to an Azure Database for PostgreSQL flexible server instance and get answers to common questions.

## What is Azure Advisor for PostgreSQL?

The Azure Advisor system uses telemetry to issue performance and reliability recommendations for your Azure Database for PostgreSQL database. 

Some recommendations are common to multiple product offerings, while other recommendations are based on product-specific optimizations.

## Where can I view my recommendations?

Recommendations are available from the **Overview** navigation sidebar in the Azure portal. A preview appears as a banner notification, and details can be viewed in the **Notifications** section located just below the resource usage graphs.

:::image type="content" source="media/concepts-azure-advisor-recommendations/advisor-example.png" alt-text="Screenshot of the Azure portal showing an Azure Advisor recommendation.":::

## Recommendation types

Azure Database for PostgreSQL prioritizes the following type of recommendation:

- **Performance**: To enhance the performance of your Azure Database for PostgreSQL flexible server instance, the recommendations proactively identify servers experiencing scenarios which can determine performance. These scenarios include high CPU utilization, frequent checkpoint initiations, performance-impacting log parameter settings, inactive logical replication slots, long-running transactions, orphaned prepared transactions, a high bloat ratio, and transaction wraparound risks. For more information, see [Advisor Performance recommendations](/azure/advisor/advisor-performance-recommendations).

## Understanding your recommendations

- **Daily schedule**: For Azure Database for PostgreSQL databases, we review server telemetry and issue recommendations daily. If you make changes to your server configuration, the existing recommendations remain visible until we reevaluate the recommendation the following day, approximately 24 hours later.

- **Performance history**: Some of our recommendations are based on performance history. These recommendations will only appear after a server has been operating with the same configuration for seven days. This allows us to detect patterns of heavy usage (for example, high CPU activity or high connection volume) over a sustained period. If you provisioned a new server or change to a new vCore configuration, these recommendations are paused temporarily. This prevents legacy telemetry from triggering recommendations on a newly reconfigured server. However, this also means that performance history-based recommendations might not be identified immediately.

## Related content

- [Azure Advisor Overview](/azure/advisor/advisor-overview).
