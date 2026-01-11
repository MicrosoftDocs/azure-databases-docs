---
title: High Availability (HA) Health Status Monitoring
description: This article describes how to monitor the health of HA-enabled instances for Azure Database for PostgreSQL flexible server using Azure Resource Health.
author: gkasar
ms.author: gkasar
ms.reviewer: maghan
ms.date: 11/04/2024
ms.service: azure-database-postgresql
ms.topic: how-to
---

# High Availability (HA) health status monitoring for Azure Database for PostgreSQL 

Azure Database for PostgreSQL flexible server includes a High Availability (HA) Health Status Monitoring feature, which uses Azure's Resource Health Check (RHC) framework. This service provides continuous insights into the health of HA-enabled instances, notifying you of events that might affect connectivity and availability. The following details each health state and associated scenarios to help you troubleshoot and maintain HA stability.

## Health States

Each HA state is monitored through various internal signals that represent specific conditions. Below are the possible HA states along with visual indicators and scenarios that might affect your Azure Database for PostgreSQL flexible server.

### Ready – HA is Healthy

The *Ready* status indicates that your HA-enabled server is operating normally with no detected issues affecting failover readiness. All necessary configurations are intact, and no significant error conditions have been detected.

:::image type="content" source="media/how-to-monitor-high-availability/high-availability-status-available.png" alt-text="Screenshot of showing HA Ready status." lightbox="media/how-to-monitor-high-availability/high-availability-status-available.png":::

### Degraded – Network Security Group (NSG) or Virtual Appliance Blocking Connections

The *Degraded* status might appear when NSG rules or a virtual appliance is blocking essential connections required for high availability. This configuration issue prevents full HA functionality and should be corrected by adjusting the NSG settings.

:::image type="content" source="media/how-to-monitor-high-availability/high-availability-status-degraded-nsg-blocked.png" alt-text="Screenshot of showing HA Degraded status due to NSG blocking connections." lightbox="media/how-to-monitor-high-availability/high-availability-status-degraded-nsg-blocked.png":::

### Degraded – Read-Only State

If your PostgreSQL flexible server enters a read-only state, the *Degraded* status reflects this restriction. This typically requires provisioning additional resources or addressing the conditions that led to the read-only setting to restore full functionality.

:::image type="content" source="media/how-to-monitor-high-availability/high-availability-status-degraded-read-only.png" alt-text="Screenshot of showing HA Degraded status due to read-only state." lightbox="media/how-to-monitor-high-availability/high-availability-status-degraded-read-only.png":::

### Degraded – High Availability in Degraded State

When the HA service itself is experiencing degraded performance, possibly due to transient issues or system-level conditions, this status appears. Implementing retry logic can help mitigate the effects of these temporary connectivity disruptions.  It's important to note that the "degraded" status does not mean the server is unavailable. Instead, it indicates that the overall HA setup and health checks have not yet fully completed. Despite this status, the server may still be operational and accessible.

To accurately monitor your database's availability during such periods, we recommend using the "is_db_alive" metric as part of [Database Availability Metrics](../monitor/concepts-monitoring.md). This metric provides a reliable indicator of the database's availability, helping you distinguish between a temporary incomplete HA setup and actual downtime.


:::image type="content" source="media/how-to-monitor-high-availability/high-availability-status-degraded-performance.png" alt-text="Screenshot of showing HA Degraded status due to performance issues." lightbox="media/how-to-monitor-high-availability/high-availability-status-degraded-performance.png":::

### Degraded – Planned Failover Initiated

During a planned failover event initiated for your server, the *Degraded* status appears, signifying that HA failover processes are active. This is generally a brief and controlled process, and service should resume shortly.

:::image type="content" source="media/how-to-monitor-high-availability/high-availability-status-degraded-planned-failover.png" alt-text="Screenshot of showing HA Degraded status due to planned failover." lightbox="media/how-to-monitor-high-availability/high-availability-status-degraded-planned-failover.png":::

### Degraded – Unplanned Failover Initiated

For an unplanned failover, this status indicates an active failover event triggered by unexpected circumstances. This scenario might involve brief connectivity interruptions until the server completes failover procedures.

:::image type="content" source="media/how-to-monitor-high-availability/high-availability-status-degraded-unplanned-failover.png" alt-text="Screenshot of showing HA Degraded status due to unplanned failover." lightbox="media/how-to-monitor-high-availability/high-availability-status-degraded-unplanned-failover.png":::

### Degraded – Upgrade Failover Initiated

During system upgrades, your HA server might undergo an upgrade failover to apply necessary updates. While in this state, the server might restrict new connections temporarily, and retry logic should be implemented to handle transient issues effectively.

:::image type="content" source="media/how-to-monitor-high-availability/high-availability-status-degraded-upgrade-failover.png" alt-text="Screenshot of showing HA Degraded status due to upgrade failover." lightbox="media/how-to-monitor-high-availability/high-availability-status-degraded-upgrade-failover.png":::

## Configuring Resource Health Alerts

You can set up Resource Health alerts to receive real-time notifications when any changes occur in the health status of your HA-enabled PostgreSQL instance. Configurations are available through the Azure portal or using an ARM template, helping you stay informed of HA status updates without actively monitoring the portal.

### Steps to Configure Resource Health Alerts via Portal

1. Navigate to the Azure portal and select your PostgreSQL flexible server.
1. In the left-hand menu, select "Alerts" under the "Monitoring" section.
1. Select "New alert rule" and configure the alert logic based on Resource Health signals.
1. Set up the action group to specify how you want to be notified (email, SMS, etc.).
1. Review and create the alert rule.

### Steps to Create Resource Health Alerts using ARM Template

1. Download the ARM template from the [Resource Health Alerts ARM Template Guide](/azure/service-health/resource-health-alert-arm-template-guide).
1. Customize the template with your specific server details and alert preferences.
1. Deploy the ARM template using Azure CLI or Azure PowerShell.
1. Verify the deployment and ensure the alerts are active.

For more details on setting up alerts, follow these guides:

- [Configure Resource Health Alerts via Portal](/azure/azure-monitor/alerts/alerts-create-activity-log-alert-rule)
- [Create Resource Health Alerts using ARM Template](/azure/service-health/resource-health-alert-arm-template-guide)

By using HA Health Status Monitoring, you gain essential insights into your PostgreSQL server's HA performance, enabling a proactive approach to managing uptime and availability.

## Related content

- [Get an overview of Resource Health](/azure/service-health/resource-health-overview)
- [Review Resource Health FAQ](/azure/service-health/resource-health-faq)
- [Learn more about Resource Health alerts](/azure/service-health/resource-health-alert-monitor-guide)
