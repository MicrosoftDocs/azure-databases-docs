---
title: Configure Intelligent Tuning - Azure Portal in Azure HorizonDB
description: This article describes how to configure intelligent tuning in an Azure HorizonDB instance through the Azure portal.
author: avnishrastogimsft
ms.author: avrastog
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-database-postgresql
ms.subservice: monitoring
ms.topic: how-to
---

# Configure intelligent tuning by using the Azure portal in Azure HorizonDB

This article provides a step-by-step procedure to configure intelligent tuning in an Azure HorizonDB instance by using the Azure portal.

To learn more about intelligent tuning, see the [overview](concepts-intelligent-tuning.md).

> [!IMPORTANT]  
> Autovacuum tuning is currently supported for the General Purpose and Memory Optimized server compute tiers that have four or more vCores. The Burstable server compute tier isn't supported.

## Steps to enable intelligent tuning on your

1. Visit the [Azure portal](https://portal.azure.com/) and select the Azure HorizonDB instance on which you want to enable intelligent tuning.

1. On the left pane, select **Server parameters** and then search for **intelligent tuning**.

   :::image type="content" source="media/how-to-intelligent-tuning-portal/enable-intelligent-tuning.png" alt-text="Screenshot of the pane for server parameters with a search for intelligent tuning." lightbox="media/how-to-intelligent-tuning-portal/enable-intelligent-tuning.png" :::

1. The pane shows two parameters: `intelligent_tuning` and `intelligent_tuning.metric_targets`. To activate intelligent tuning, change `intelligent_tuning` to **ON**. You have the option to select one, multiple, or all available tuning targets in `intelligent_tuning.metric_targets`. Select the **Save** button to apply these changes.

   :::image type="content" source="media/how-to-intelligent-tuning-portal/choose-tuning-targets.png" alt-text="Screenshot of Server Parameter blade with tuning targets options." lightbox="media/how-to-intelligent-tuning-portal/choose-tuning-targets.png" :::

> [!NOTE]  
> Both `intelligent_tuning` and `intelligent_tuning.metric_targets` server parameters are dynamic. That is, no server restart is required when their values are changed.

### Considerations for selecting values for tuning targets

When you're choosing values from the `intelligent_tuning.metric_targets` server parameter, take the following considerations into account:

- The `NONE` value takes precedence over all other values. If you choose `NONE` alongside any combination of other values, the parameter is perceived as set to `NONE`. This is equivalent to `intelligent_tuning = OFF`, so no tuning occurs.

- The `ALL` value takes precedence over all other values, with the exception of `NONE`. If you choose `ALL` with any combination, barring `NONE`, all the listed parameters undergo tuning.

- The `ALL` value encompasses all existing metric targets. This value also automatically applies to any new metric targets that you might add in the future. This allows for comprehensive and future-proof tuning of your Azure HorizonDB instance.

## Related content

- [Perform intelligent tuning in Azure HorizonDB](concepts-intelligent-tuning.md)
