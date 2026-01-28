---
title: Business Continuity With Azure Monitor and Azure Advisor
description: Learn about the concepts of business continuity with Azure Monitor and Azure Advisor in Azure Database for MySQL - Flexible Server.
author: VandhanaMehta
ms.author: vamehta
ms.reviewer: maghan
ms.date: 08/20/2025
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: concept-article
---

# Monitor business continuity for Azure Database for MySQL with Azure Advisor and Azure Monitor

Business continuity is a critical aspect of database security and operational resilience. Azure Database for MySQL integrates with Azure Advisor and Azure Monitor to help you identify risks, optimize performance, and maintain high availability. This article outlines how to use these tools to monitor and secure MySQL workloads.

Business continuity ensures that operations can continue during unexpected disruptions. For databases, this continuity means minimizing downtime, preserving data integrity, and enabling rapid recovery. Azure provides built-in tools to help you achieve these goals:

- **Azure Advisor**: Offers personalized recommendations to improve reliability, security, and performance.
- **Azure Monitor**: Provides deep observability into metrics, logs, and alerts for proactive incident response.

## Key capabilities

Azure Monitor and Azure Advisor are essential tools for maintaining business continuity in Azure Database for MySQL. By leveraging these services, you can proactively identify potential risks, receive tailored recommendations, and monitor the health and performance of your database environment. This integrated approach helps ensure your workloads remain resilient, secure, and available, even in the face of unexpected disruptions.

### Azure Advisor recommendations

Azure Advisor analyzes your MySQL server configuration and usage patterns to provide actionable insights. Common recommendations include:

- **High availability setup**: Advisor checks if zone-redundant high availability is configured and recommends enabling it if not.
- **Backup configuration**: Ensures automated backups are enabled and retained for an appropriate duration.
- **Security posture**: Flags missing configurations such as SSL enforcement or Azure AD authentication.

To learn more, visit [Azure Advisor](concepts-azure-advisor-recommendations.md)

### Azure Monitor integration

Azure Monitor collects performance metrics, telemetry, and logs from your MySQL server. Use it to:

- Track availability and latency
- Set alerts for CPU, memory, and storage thresholds
- Visualize trends using dashboards and workbooks
- Diagnose issues with Application Insights and Log Analytics

To learn more, visit [Azure Monitor](/azure/azure-monitor/metrics/data-platform-metrics)

## Implementation Steps

To ensure business continuity for your Azure Database for MySQL, it's important to leverage Azure's monitoring and advisory capabilities. By integrating Azure Monitor and Azure Advisor, you gain visibility into your database's health, receive proactive recommendations, and can quickly respond to potential issues. The following steps guide you through implementing these tools to safeguard your MySQL workloads and maintain operational resilience.

1. **Enable Diagnostic Settings**

   Configure your MySQL server to send logs and metrics to Azure Monitor.

1. **Review Advisor Recommendations**

   Go to Azure Advisor in the portal and filter by "Reliability" and "Security" categories.

1. **Set Up Alerts**

   Use Azure Monitor to define alert rules for key metrics like CPU usage, storage consumption, and connection failures.

1. **Visualize and Act**

   Create dashboards or use prebuilt workbooks to monitor trends and respond to anomalies.

## Best practices

- Enable zone-redundant high availability for critical workloads.
- Use Microsoft Entra ID authentication to strengthen identity management.
- Automate backup scheduling and test restore procedures regularly.
- Monitor performance baselines and investigate deviations promptly.

For more information, visit [Best practices for monitoring](concept-monitoring-best-practices.md)

## Related articles

- [Business continuity](concepts-business-continuity.md)

