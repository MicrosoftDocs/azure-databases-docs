---
title: Release Notes for Azure Database for MySQL Flexible Server - January 2026
description: Learn about the release notes for Azure Database for MySQL Flexible Server January 2026.
author: xboxeer
ms.author: yuzheng1
ms.reviewer: maghan
ms.date: 01/28/2026
ms.service: azure-database-mysql
ms.topic: release-notes
ai-usage: ai-assisted
---

# Azure Database for MySQL January 2026 version release notes

The January 2026 version of Azure Database for MySQL Flexible Server is now available. Starting January 22, 2026, all new servers automatically use this version. Existing servers upgrade during their next scheduled maintenance. To upgrade your servers earlier, enroll in the [Virtual Canary Program](https://aka.ms/mysql/virtual-canary).

This version introduces new features and enhancements, resolves known problems, and includes important security patches to ensure optimal performance and security.

## Maintenance scheduling considerations
  
For Azure Database for MySQL instances in the Azure public cloud, an internal certificate expires by the end of February 2026. As a result, the maintenance reschedules window for this cycle is limited to dates before the end of February. Postponing maintenance beyond February might cause the server to become unreachable after the certificate expires. Therefore, rescheduling past the end of February isn't supported for this maintenance event.

For some Azure Database for MySQL instances in Azure National Clouds, the certificate that the current Certificate Authority (CA) issued expires before February 6, 2026. After the certificate expires, client connections to the server fail, resulting in service unavailability.

To assess whether your server is affected, verify the certificate expiration date from a client environment by using the following command:`openssl s_client -starttls mysql -connect <server_dns>:3306`. For affected servers, the maintenance reschedule window is limited and can't be freely postponed, as further delay increases the risk of certificate expiration and client connection failures. In some cases, if the server was restarted recently, the certificate is automatically refreshed. If you believe this condition applies to your server, open an Azure Support case. After validation, the maintenance reschedule window can be extended up to the end of February.

During this maintenance cycle, there are major global events between **February 5–10, 2026** and **February 16–23, 2026** that might limit our ability to fully honor all customers' Custom Maintenance Window (CMW) preferences during initial scheduling. As a result, some servers with CMW enabled might be assigned a maintenance date outside of their preferred window. You can still reschedule the maintenance in the Azure portal to better align with these event periods or your original CMW preference.

## Engine version changes

This version doesn't include any engine version changes.

## Features

This version doesn't introduce any new features.

## Improvements

- Improved the error message that's shown when you attempt to enable HA on a VNET-based instance that still has Accelerated Logs enabled.
- Added TLS 1.3 support for Azure MySQL 5.7 version.

## Known issues fixes

- Fixed an issue where enabling geo backup caused subsequent GTID reset operations to fail.
- Fixed an issue where certain HA servers behind a dedicated SLB couldn't enable a private endpoint.
