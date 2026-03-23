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
> **Microsoft is rotating TLS certificates for Azure Database for PostgreSQL** to update the Certificate Authority and the resulting certificate chain.
>
> If your client configuration uses the [***Recommended configurations for TLS***](../security-tls.md#recommended-configurations-for-tls), you don't need to take action.
> 
> **Intermediate certificate rotation schedule:**
>
> - Updates for Azure regions West Central US and East Asia are complete.
> - Updates for UK South and US Government regions start on January 21, 2026.
> - Updates for Central US start on January 26, 2026.
> - Updates for all other regions start on January 28, 2026.
>
> **Root certificate rotation schedule:**
>
> - Updates for root CA certificates from DigiCert Global Root CA (G1) to DigiCert Global Root G2 in China regions start March 9, 2026.