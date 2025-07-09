---
title: Server self-heal for Azure Database for MySQL - Flexible Server
description: Learn how to use server self-heal in Azure Database for MySQL - Flexible Server to automatically recover from certain failures.
author: xboxeer
ms.author: yuzheng1
ms.date: 07/09/2025
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: how-to
---
# Self-Heal in Azure Database for MySQL

## Overview

The **Self-Heal** feature in Azure Database for MySQL empowers customers to resolve common server issues independently, without needing to open a support case. It provides a one-click repair experience that helps restore service health quickly and safely.

Self-Heal is always available in the Azure portal and can be triggered proactively by customers whenever they suspect something is wrong with their server—even if no alerts or errors are currently shown.

## Key Benefits

- **Self-service recovery**: Resolve common issues without waiting for support.
- **Always available**: Accessible at any time from the Azure portal.
- **Safe and scoped**: Actions are predefined and tailored to specific scenarios.

## How It Works

The Self-Heal feature functions as a lightweight diagnostic and repair utility, similar to tools like the Windows Network Troubleshooter. When a customer clicks the **Self-Heal** button, the system immediately executes a predefined remediation workflow designed to address known issues.

Self-Heal actions are categorized into two types:

- **Non-impactful Self-Heal**:  
  - Doesn't cause downtime  
  - Suitable for resolving issues such as log corruption or missing logs  

- **Impactful Self-Heal**:  
  - May involve brief server downtime  
  - Used for addressing availability-related issues such as server unresponsiveness or stuck states  

Customers are informed of the potential impact before initiating any action.

## Supported Scenarios

The initial release of Self-Heal supports a focused set of scenarios, including:

- Missing or corrupted logs  
- Server unresponsive or unreachable  
- Server availability issues (for example, stuck in restarting state)  

Support for additional scenarios will be added over time based on telemetry and customer feedback.

## Accessing Self-Heal

To use Self-Heal:

1. Navigate to your MySQL server in the Azure portal.
2. Select **Help** from the left-hand menu.
3. Click **Self Heal** and choose the appropriate action.

## Frequently Asked Questions (FAQ)

**Q: Will clicking the Self-Heal button automatically open a support case?**

A: **No.** Triggering a Self-Heal action does **not** create a support case. The feature is designed to help customers resolve issues independently, without involving Azure support unless further assistance is needed.


**Q: When should I use Self-Heal?**

A: You can use Self-Heal **any time** you suspect your server isn't behaving as expected—even if there are no active alerts. It’s a proactive tool that helps you quickly address common issues without waiting for diagnostics or support.


**Q: Will Self-Heal cause downtime?**

A: It depends on the type of action:

- **Non-impactful Self-Heal**: No downtime. Safe to run at any time.
- **Impactful Self-Heal**: May cause brief downtime. You’ll be informed before proceeding.


**Q: Is Self-Heal available for all MySQL servers?**

A: Currently, Self-Heal is available for **Azure Database for MySQL – Flexible Server**, and only for **non-HA (High Availability) servers**.

For HA-enabled servers, the recommended way to quickly recover from availability issues is to perform a **forced failover**, which is designed to restore service with minimal disruption.

