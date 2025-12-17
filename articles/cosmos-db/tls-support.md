---
title: Prepare for upcoming Transport Layer Security (TLS) 1.3 support
description: Learn how to enable TLS 1.3 for your Azure Cosmos DB account to improve your security posture.
author: iriaosara
ms.author: iriaosara
ms.service: azure-cosmos-db
ms.topic: upgrade-and-migration-article
ms.date: 09/03/2025
applies-to:
  - ✅ NoSQL
  - ✅ MongoDB
  - ✅ Apache Cassandra
  - ✅ Apache Gremlin
  - ✅ Table
---

# Prepare for upcoming TLS 1.3 support for Azure Cosmos DB

> [!IMPORTANT]
> Effective **March 31, 2025 support for TLS 1.3** will be enabled for Azure Cosmos DB.
>
>  [**Starting August 31, 2025, we are officially deprecating TLS 1.0/1.1.**](https://azure.microsoft.com/updates?id=update-retirement-tls1-0-tls1-1-versions-azure-services). Only TLS 1.2 or higher is supported. 

Azure Cosmos DB enables TLS 1.3 support on public endpoints across its platform globally to align with security best practices.
This article provides extra guidance on how to prepare for the upcoming support of TLS 1.3 for Azure Cosmos DB.

TLS 1.3 introduces substantial enhancements compared to its predecessors. TLS 1.3 improvements focus on both performance and security, featuring faster handshakes and a streamlined set of more secure cipher suites, namely TLS_AES_256_GCM_SHA384 and TLS_AES_128_GCM_SHA256. Notably, TLS 1.3 prioritizes Perfect Forward Secrecy (PFS) by eliminating key exchange algorithms that don't support it.  

Clients that utilize the latest available TLS version automatically pick TLS 1.3 when it's available. Azure Cosmos DB continues to support TLS 1.2 in addition to TLS 1.3.  

These issues are some of the known issues with TLS 1.3 enablement, potential effect, and mitigation.

## Known issues, affect, and mitigation

- **JDK Related Issues**: The io.netty versions between `4.1.68.Final` and `4.1.86.Final` inclusive contain a bug that causes the client to fail the TLS handshake in Direct mode connection when the Java runtime engine doesn't support TLS 1.3. Azure Cosmos DB Java SDK versions ranging from 4.20.0 to 4.40.0 inclusive have a transitive dependency on io.netty with this bug. The client fails with  `java.lang.IllegalArgumentException` exceptions as shown here.
    
    ```output
     Caused by: io.netty.handler.codec.DecoderException: javax.net.ssl.SSLHandshakeException: General OpenSslEngine problem at 
    ...       
    Caused by: java.lang.IllegalArgumentException: TLSv1.3 at sun.security.ssl.ProtocolVersion.valueOf(ProtocolVersion.java:187)
    ```

-  **Recommendations for mitigation**:

    - Option 1: **(Required)** Upgrade Azure Cosmos DB Java SDK at least to [minimum recommended version](sdk-java-v4.md#recommended-version).
    - Option 2: We recognize that upgrading to the latest SDK version might not always be feasible. While transitioning your application to the newest SDK, you can address this issue by switching the connection to [Gateway Mode](tune-connection-configurations-net-sdk-v3.md#customizing-gateway-connection-mode). Make sure to thoroughly test the application before deploying it in the production environment.

> [!NOTE]
> Enabling client to use TLS 1.3 requires Java runtime to support TLS 1.3

## Related content
- [How to set minimum TLS version](./self-serve-minimum-tls-enforcement.md#how-to-set-the-minimum-tls-version-for-my-cosmos-db-database-account)
- [Moving to TLS 1.2 for Azure Cosmos DB](https://aka.ms/tls12)