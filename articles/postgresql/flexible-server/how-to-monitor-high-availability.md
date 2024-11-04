---
title: High Availability (HA) Health Status Monitoring
description: This article describes how to monitor the health of HA-enabled instances for Azure Database for PostgreSQL - Flexible Server using Azure Resource Health.
author: varun-dhawan
ms.author: varundhawan
ms.reviewer: maghan
ms.date: 11/04/2024
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
---

# High Availability (HA) Health Status Monitoring for Azure Database for PostgreSQL - Flexible Server

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

Azure Database for PostgreSQL Flexible Server includes a High Availability (HA) Health Status Monitoring feature, which leverages Azure’s Resource Health Check (RHC) framework. This service provides continuous insights into the health of HA-enabled instances, notifying you of events that might impact connectivity and availability. The following details each health state and associated scenarios to help you troubleshoot and maintain HA stability.

## Health States

Each HA state is monitored through various internal signals that represent specific conditions. Below are the possible HA states along with visual indicators and scenarios that may impact your Azure Database for PostgreSQL Flexible Server.

#### **Available – HA is Healthy**  
   The *Available* status indicates that your HA-enabled server is operating normally with no detected issues affecting failover readiness. All necessary configurations are intact, and no significant error conditions have been detected.

    :::image type="content" source="./media/how-to-monitor-ha/high-availability-status-available.png" alt-text="Screenshot showing HA Available status.":::

#### **Degraded – Network Security Group (NSG) or Virtual Appliance Blocking Connections**  
   The *Degraded* status may appear when NSG rules or a virtual appliance is blocking essential connections required for high availability. This configuration issue prevents full HA functionality and should be corrected by adjusting the NSG settings.

    :::image type="content" source="./media/how-to-monitor-ha/high-availability-status-degraded-nsg-blocked.png" alt-text="Screenshot showing HA Degraded status due to NSG blocking connections.":::

#### **Degraded – Read-Only State**  
   If your PostgreSQL Flexible Server enters a read-only state, the *Degraded* status will reflect this restriction. This typically requires provisioning additional resources or addressing the conditions that led to the read-only setting to restore full functionality.

    :::image type="content" source="./media/how-to-monitor-ha/high-availability-status-degraded-read-only.png" alt-text="Screenshot showing HA Degraded status due to read-only state.":::

#### **Degraded – High Availability in Degraded State**  
   When the HA service itself is experiencing degraded performance, possibly due to transient issues or system-level conditions, this status will appear. Implementing retry logic can help mitigate the effects of these temporary connectivity disruptions.

    :::image type="content" source="./media/how-to-monitor-ha/high-availability-status-degraded-performance.png" alt-text="Screenshot showing HA Degraded status due to performance issues.":::

#### **Degraded – Planned Failover Initiated**  
   During a planned failover event initiated for your server, the *Degraded* status appears, signifying that HA failover processes are active. This is generally a brief and controlled process, and service should resume shortly.

    :::image type="content" source="./media/how-to-monitor-ha/high-availability-status-degraded-planned-failover.png" alt-text="Screenshot showing HA Degraded status due to planned failover.":::

#### **Degraded – Unplanned Failover Initiated**  
   In case of an unplanned failover, this status indicates an active failover event triggered by unexpected circumstances. This scenario may involve brief connectivity interruptions until the server completes failover procedures.

    :::image type="content" source="./media/how-to-monitor-ha/high-availability-status-degraded-unplanned-failover.png" alt-text="Screenshot showing HA Degraded status due to unplanned failover.":::

#### **Degraded – Upgrade Failover Initiated**  
   During system upgrades, your HA server might undergo an upgrade failover to apply necessary updates. While in this state, the server may restrict new connections temporarily, and retry logic should be implemented to handle transient issues effectively.

    :::image type="content" source="./media/how-to-monitor-ha/high-availability-status-degraded-upgrade-failover.png" alt-text="Screenshot showing HA Degraded status due to upgrade failover.":::

## Configuring Resource Health Alerts

You can set up Resource Health alerts to receive real-time notifications when any changes occur in the health status of your HA-enabled PostgreSQL instance. Configurations are available through the Azure portal or using an ARM template, helping you stay informed of HA status updates without actively monitoring the portal.

For more details on setting up alerts, follow these guides:
- [Configure Resource Health Alerts via Portal](/azure/azure-monitor/alerts/alerts-create-activity-log-alert-rule)
- [Create Resource Health Alerts using ARM Template](/azure/service-health/resource-health-alert-arm-template-guide)

By leveraging HA Health Status Monitoring, you gain essential insights into your PostgreSQL server’s HA performance, enabling a proactive approach to managing uptime and availability.

## Related Content
- [Get an overview of Resource Health](/azure/service-health/resource-health-overview)
- [Review Resource Health FAQ](/azure/service-health/resource-health-faq)
- [Learn more about Resource Health alerts](/azure/service-health/resource-health-alert-monitor-guide)

