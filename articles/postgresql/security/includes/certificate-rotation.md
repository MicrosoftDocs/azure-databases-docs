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
> **Certificate rotation schedule**
>
> - Azure regions West Central US, East Asia, and UK South started their TLS certificate rotation on November 11, 2025.
> - Beginning January 19, 2026, this certificate rotation is planned to extend to the remaining (except China) regions including Azure Government.
> - After the Spring Festival (Chinese New Year) 2026, China regions will also undergo a certificate rotation that includes a **change to one of the root CAs**.
