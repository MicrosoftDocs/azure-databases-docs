---
title: High Availability (HA) Health Status Monitoring
description: This article describes how to monitor the health of HA-enabled instances for Azure Database for PostgreSQL flexible server using Azure Resource Health.
#customer intent: As a user, I want to monitor the health of my HA-enabled Azure Database for PostgreSQL flexible server, so that I can maintain high availability and uptime.
author: gkasar
ms.author: gkasar
ms.reviewer: maghan
ms.date: 07/13/2026
ms.service: azure-database-postgresql
ms.subservice: high-availability
ms.topic: how-to
---

# High availability (HA) health status monitoring for Azure Database for PostgreSQL flexible server

Azure Database for PostgreSQL flexible server includes a high availability (HA) health status monitoring feature that uses Azure's Resource Health Check (RHC) framework. This service provides continuous insights into the health of HA-enabled instances and notifies you of events that might affect connectivity and availability. The following sections describe each health state and associated scenarios to help you troubleshoot and maintain HA stability.

## Health states

The service monitors each HA state through various internal signals that represent specific conditions. The following list describes the possible HA states along with visual indicators and scenarios that might affect your Azure Database for PostgreSQL flexible server.

### Ready – HA is healthy

The *Ready* status indicates that your HA-enabled server is operating normally with no detected issues that affect failover readiness. All necessary configurations are intact, and no significant error conditions exist.

:::image type="content" source="media/how-to-monitor-high-availability/high-availability-status-available.png" alt-text="Screenshot of showing HA Ready status." lightbox="media/how-to-monitor-high-availability/high-availability-status-available.png":::

### Degraded – Network Security Group (NSG) or virtual appliance blocking connections

The *Degraded* status might appear when NSG rules or a virtual appliance block essential connections required for high availability. This configuration issue prevents full HA functionality. Correct the issue by adjusting the NSG settings.

:::image type="content" source="media/how-to-monitor-high-availability/high-availability-status-degraded-nsg-blocked.png" alt-text="Screenshot of showing HA Degraded status due to NSG blocking connections." lightbox="media/how-to-monitor-high-availability/high-availability-status-degraded-nsg-blocked.png":::

### Degraded – Read-only state

If your PostgreSQL flexible server enters a read-only state, the *Degraded* status reflects this restriction. This state typically requires provisioning additional resources or addressing the conditions that led to the read-only setting to restore full functionality.

:::image type="content" source="media/how-to-monitor-high-availability/high-availability-status-degraded-read-only.png" alt-text="Screenshot of showing HA Degraded status due to read-only state." lightbox="media/how-to-monitor-high-availability/high-availability-status-degraded-read-only.png":::

### Degraded – High availability in degraded state

This status appears when the high availability (HA) service experiences degraded performance, possibly due to transient issues or system-level conditions. Implementing retry logic can help mitigate the effects of these temporary connectivity disruptions. The **degraded** status doesn't mean the server is unavailable. Instead, it indicates that the overall HA setup and health checks aren't fully complete. Despite this status, the server might still be operational and accessible.

To accurately monitor your database's availability during such periods, use the `is_db_alive` metric as part of [Database Availability Metrics](../monitor/concepts-monitoring.md). This metric provides a reliable indicator of the database's availability, helping you distinguish between a temporary incomplete HA setup and actual downtime.


:::image type="content" source="media/how-to-monitor-high-availability/high-availability-status-degraded-performance.png" alt-text="Screenshot of showing HA Degraded status due to performance issues." lightbox="media/how-to-monitor-high-availability/high-availability-status-degraded-performance.png":::

### Degraded – Planned failover initiated

During a planned failover event initiated for your server, the *Degraded* status appears, signifying that HA failover processes are active. This process is generally brief and controlled, and service should resume shortly.

:::image type="content" source="media/how-to-monitor-high-availability/high-availability-status-degraded-planned-failover.png" alt-text="Screenshot of showing HA Degraded status due to planned failover." lightbox="media/how-to-monitor-high-availability/high-availability-status-degraded-planned-failover.png":::

### Degraded – Unplanned failover initiated

For an unplanned failover, this status indicates an active failover event triggered by unexpected circumstances. This scenario might involve brief connectivity interruptions until the server completes failover procedures.

:::image type="content" source="media/how-to-monitor-high-availability/high-availability-status-degraded-unplanned-failover.png" alt-text="Screenshot of showing HA Degraded status due to unplanned failover." lightbox="media/how-to-monitor-high-availability/high-availability-status-degraded-unplanned-failover.png":::

### Degraded – Upgrade failover initiated

During system upgrades, your HA server might undergo an upgrade failover to apply necessary updates. While in this state, the server might restrict new connections temporarily. Implement retry logic to handle transient issues effectively.

:::image type="content" source="media/how-to-monitor-high-availability/high-availability-status-degraded-upgrade-failover.png" alt-text="Screenshot of showing HA Degraded status due to upgrade failover." lightbox="media/how-to-monitor-high-availability/high-availability-status-degraded-upgrade-failover.png":::

## Configuring Resource Health Alerts

Set up Resource Health alerts to get real-time notifications when any changes occur in the health status of your HA-enabled PostgreSQL instance. You can configure these alerts through the Azure portal or by using an ARM template. This way, you stay informed of HA status updates without actively monitoring the portal.

### Steps to Configure Resource Health Alerts via Portal

1. Go to the Azure portal and select your PostgreSQL flexible server.
1. In the left-hand menu, under the **Monitoring** section, select **Alerts**.
1. Select **New alert rule** and configure the alert logic based on Resource Health signals.
1. Set up the action group to specify how you want to be notified (email, SMS, and so on).
1. Review and create the alert rule.

### Steps to Create Resource Health Alerts using ARM Template

1. Download the ARM template from the [Resource Health Alerts ARM Template Guide](/azure/service-health/resource-health-alert-arm-template-guide).
1. Customize the template with your specific server details and alert preferences.
1. Deploy the ARM template by using Azure CLI or Azure PowerShell.
1. Verify the deployment and ensure the alerts are active.

For more details on setting up alerts, see the following guides:

- [Configure Resource Health Alerts via Portal](/azure/azure-monitor/alerts/alerts-create-activity-log-alert-rule)
- [Create Resource Health Alerts using ARM Template](/azure/service-health/resource-health-alert-arm-template-guide)

By using HA Health Status Monitoring, you gain essential insights into your PostgreSQL server's HA performance, enabling a proactive approach to managing uptime and availability.

## Related content

- [Get an overview of Resource Health](/azure/service-health/resource-health-overview)
- [Review Resource Health FAQ](/azure/service-health/resource-health-faq)
- [Learn more about Resource Health alerts](/azure/service-health/resource-health-alert-monitor-guide)
