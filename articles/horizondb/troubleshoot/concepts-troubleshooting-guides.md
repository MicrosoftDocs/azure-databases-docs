---
title: Troubleshooting guides
description: Troubleshooting guides for Azure HorizonDB.
author: avnishrastogimsft
ms.author: avrastog
ms.reviewer: maghan
ms.date: 04/27/2024
ms.service: azure-database-postgresql
ms.subservice: performance
ms.topic: how-to
ms.custom: sfi-image-nochange
---

# Troubleshooting guides for Azure HorizonDB 

The troubleshooting guides for Azure HorizonDB are designed to help you quickly identify and resolve common challenges you may encounter while using Azure HorizonDB. Integrated directly into the Azure portal, the troubleshooting guides provide actionable insights, recommendations, and data visualizations to assist you in diagnosing and addressing issues related to common performance problems. With these guides at your disposal, you are better equipped to optimize your Azure HorizonDB experience and ensure a smoother, more efficient database operation.

## Overview

The troubleshooting guides available in Azure HorizonDB provide you with the necessary tools to analyze and troubleshoot prevalent performance issues, 
including:
* CPU
* Memory
* IOPS
* Temporary files
* Autovacuum monitoring
* Autovacuum blockers

:::image type="content" source="./media/concepts-troubleshooting-guides/overview-troubleshooting-guides.jpg" alt-text="Screenshot of multiple Troubleshooting Guides combined." lightbox="./media/concepts-troubleshooting-guides/overview-troubleshooting-guides.jpg":::

Each guide is packed with multiple charts, guidelines, recommendations tailored to the specific problem you may encounter, which can help expedite the troubleshooting process.
The troubleshooting guides are directly integrated into the Azure portal and your Azure HorizonDB flexible server instance, making them convenient and easy to use. 

The troubleshooting guides consist of the following components:

- **CPU**

  * CPU
  * Workload
  * Transactions
  * Long running transactions
  * Queries
  * User connections
  * Locking and blocking

- **Memory**

  * Memory
  * Workload
  * Sessions
  * Queries
  * User connections
  * Memory parameters

- **IOPS**

  * IOPS
  * Workload
  * Sessions
  * Queries
  * Waits
  * Checkpoints
  * Storage

- **Temporary files**

  * Storage
  * Temporary files
  * Workload
  * Queries

- **Autovacuum monitoring**

  * Bloat
  * Tuples
  * Vacuum and analyze
  * Autovacuum workers
  * Autovacuum per table
  * Enhanced metrics

- **Autovacuum blockers**

  * Emergency autovacuum and wraparound
  * Autovacuum blockers


Before using any troubleshooting guide, it's essential to ensure that all prerequisites are in place. For a detailed list of prerequisites refer to the article [Use troubleshooting guides](how-to-troubleshooting-guides.md).

### Limitations

* Troubleshooting guides aren't available for [read replicas](../read-replica/concepts-read-replicas.md).
* Be aware that enabling Query Store on the Burstable pricing tier can lead to a negative impact on performance. As a result, it's not recommended to use Query Store with this particular pricing tier.

## Related content

- [Configure intelligent tuning for Azure HorizonDB](../monitor/how-to-enable-intelligent-performance-portal.md).
- [Troubleshooting guides for Azure HorizonDB](concepts-troubleshooting-guides.md).
- [Autovacuum tuning in Azure HorizonDB](how-to-autovacuum-tuning.md).
- [Troubleshoot high IOPS utilization in Azure HorizonDB](how-to-high-io-utilization.md).
- [Best practices for uploading data in bulk in Azure HorizonDB](how-to-bulk-load-data.md).
- [Troubleshoot high CPU utilization in Azure HorizonDB](how-to-high-cpu-utilization.md).
- [Query Performance Insight in Azure HorizonDB](../monitor/concepts-query-performance-insight.md).
