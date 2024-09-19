---
title: Prepare for upcoming TLS 1.3 support for Azure Cosmos DB
titleSuffix: Azure Cosmos DB
description: Learn how to enable TLS 1.3 for your Azure Cosmos DB account to improve your security posture.
author: iriaosara
ms.author: iriaosara
ms.service: azure-cosmos-db
ms.topic: conceptual
ms.date: 9/19/2024
---

# Prepare for upcoming TLS 1.3 support for Azure Cosmos DB

[!INCLUDE[NoSQL, MongoDB, Cassandra, Gremlin, Table](includes/appliesto-nosql-mongodb-cassandra-gremlin-table.md)]

Azure Cosmos DB has started to enable TLS 1.3 support on public endpoints across its platform globally to align with security best practices. [**Starting Oct 31 2024, we are officially deprecating TLS 1.0/1.1.**](https://azure.microsoft.com/updates/azure-support-tls-will-end-by-31-october-2024-2/). Only TLS 1.2 or higher will be supported. This article provides extra guidance on how to prepare for upcoming support of TLS 1.3 for Azure Cosmos DB. 

TLS 1.3 introduces substantial enhancements compared to its predecessors. TLS 1.3 improvements focus on both performance and security, featuring faster handshakes and a streamlined set of more secure cipher suites, namely TLS_AES_256_GCM_SHA384 and TLS_AES_128_GCM_SHA256. Notably, TLS 1.3 prioritizes Perfect Forward Secrecy (PFS) by eliminating key exchange algorithms that don't support it.  

Clients that utilize the latest available TLS version will automatically pick TLS 1.3 when it's available. Azure Cosmos DB continues to support TLS 1.2 in addition to TLS 1.3.  

These are some of the known issues with TLS 1.3 enablement, potential impact, and mitigation.

## Known issues, impact, and mitigation

- **JDK Related Issues**: Certain Java clients running with Java runtime version older than 1.8.0_292 and using direct mode connections are incapable of handling TLS handshake. Client applications might fail with the error along the following lines. Caused by `io.netty.handler.codec.DecoderException: javax.net.ssl.SSLHandshakeException: General OpenSslEngine`.

-  **Recommendations for mitigation**:

    - Option 1: **(Recommended)** Upgrade your application to 1.8.0_291 or latest Java runtime version.
    - Option 2: **(Recommended)** Upgrade Azure Cosmos DB Java SDK at least to [minimum recommended version](../cosmos-db/nosql/sdk-java-v4.md).
    - Option 3: We recognize that upgrading to the latest SDK version might not always be feasible. While transitioning your application to the newest SDK, you can address this issue by switching the connection to [Gateway Mode](./nosql/tune-connection-configurations-net-sdk-v3.md#customizing-gateway-connection-mode). Make sure to thoroughly test the application before deploying it in the production environment.


## Next steps

For more information about security in Azure Cosmos DB, see [Overview of database security in Azure Cosmos DB
](./database-security.md).