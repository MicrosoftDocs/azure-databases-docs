---
title: Release Notes for Azure Database for MySQL Flexible Server - January 2026
description: Learn about the release notes for Azure Database for MySQL Flexible Server January 2026.
ai-usage: ai-assisted
author: xboxeer
ms.author: yuzheng1
ms.reviewer: maghan
ms.date: 01/14/2026
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: release-notes
---

# Azure Database For MySQL - Flexible Server January 2026 version release notes

We're excited to announce the January 2026 version of Azure Database for MySQL Flexible Server. Starting January 22, 2026, all new servers will automatically be onboarded to this latest version. Existing servers are upgraded during their next scheduled maintenance. If you prefer to upgrade your servers earlier, you can enroll in our Virtual Canary Program by following this [link](https://aka.ms/mysql/virtual-canary).

This new version introduces a range of new features and enhancements, resolves known issues, and includes essential security patches to ensure optimal performance and security.

> [!IMPORTANT]
> - For Azure Database for MySQL instances in the Azure Public Cloud, an internal certificate is scheduled to expire by the end of February 2026. As a result, the maintenance reschedule window for this cycle is limited to dates before the end of February. Postponing maintenance beyond February may cause the server to become unreachable after the certificate expires. Therefore, rescheduling past the end of February isn't supported for this maintenance event.
> - For some Azure Database for MySQL instances in Azure National Clouds, the certificate issued by the current Certificate Authority (CA) is expected to expire before February 7, 2026. Once the certificate expires, client connections to the server fail, resulting in service unavailability.
To assess whether your server is impacted, you can verify the certificate expiration date from a client environment using the following command:`openssl s_client -starttls mysql -connect <server_dns>:3306`. For affected servers, the maintenance reschedule window is limited and can't be freely postponed, as further delay increases the risk of certificate expiration and client connection failures. In some cases, if the server was restarted recently, the certificate may have been automatically refreshed. If you believe this applies to your server, open an Azure Support case. After validation, we can extend the maintenance reschedule window up to the end of February.
> - During this maintenance cycle, two major global events—**Super Bowl (February 5–10)** and **Lunar New Year (February 16–23)**—may limit our ability to fully honor all customers’ Custom Maintenance Window (CMW) preferences during initial scheduling. As a result, some servers with CMW enabled might be assigned a maintenance date outside of their preferred window. You can still reschedule the maintenance in the Azure portal to better align with these event periods or your original CMW preference.

## Engine version changes

There will be no engine version changes in this version.

## Features

No new features are being introduced in this version.

## Improvement

- Improved the error message shown when customers attempt to enable HA on a VNET-based instance that still has Accelerated Logs enabled
- TLS 1.3 support for Azure MySQL 5.7 version

## Known issues fixes

- Fixed an issue where enabling geo backup caused subsequent GTID reset operations to fail
- Fixed an issue where certain HA servers behind a dedicated SLB couldn't enable a private endpoint
