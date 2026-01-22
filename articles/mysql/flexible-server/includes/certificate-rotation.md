---
title: Certificate Rotation
description: Certificate rotation for Azure Database for MySQL
author: techlake
ms.author: hganten
ms.reviewer: maghan, randolphwest
ms.date: 01/05/2026
ms.service: azure-database-mysql
ms.subservice: security
ms.topic: include
ms.custom: references_regions
---

> [!IMPORTANT]  
> **Azure Database for MySQL has started a TLS certificate rotation** to update intermediate CA certificates and the resulting certificate chain. The root Certificate Authorities stay the same.
>
> If your client configuration uses the [***Recommended configurations for TLS***](../security-tls.md#recommended-configurations-for-tls), you don't need to take any action.
>
> **Certificate rotation schedule**
>
> - Azure regions West Central US, East Asia, and UK South began their TLS certificate rotation on November 11, 2025.
> - From January 19, 2026, this certificate rotation extends to the remaining (except China) regions, including Azure Government.
> - After the Spring Festival (Chinese New Year) 2026, China regions also undergo a certificate rotation that includes a **change to one of the root CAs**.
