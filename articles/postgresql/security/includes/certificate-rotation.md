---
title: Certificate Rotation
description: Certificate rotation for Azure Database for PostgreSQL
author: techlake
ms.author: hganten
ms.reviewer: maghan
ms.date: 12/19/2025
ms.service: azure-database-postgresql
ms.subservice: security
ms.topic: include
---

> [!IMPORTANT]  
> **Microsoft started a TLS certificate rotation for Azure Database for PostgreSQL** to update intermediate CA certificates and the resulting certificate chain. The root CAs stay the same.
>
> If your client configuration uses the [***Recommended configurations for TLS***](../security-tls.md#recommended-configurations-for-tls), you don't need to take any action.
> 
> **Intermediate certificate rotation schedule:**
>
> - Updates for Azure regions West Central US and East Asia are complete.
> - Updates for UK South and US Government regions start on January 21, 2026.
> - Updates for Central US start on January 26, 2026.
> - Updates for all other regions start on January 28, 2026.
> - After the Spring Festival (Chinese New Year) 2026, China regions will also undergo a certificate rotation that includes a **change to one of the root CAs**.
