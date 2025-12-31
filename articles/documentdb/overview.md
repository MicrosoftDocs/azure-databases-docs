---
title: Introduction/overview
description: Learn about Azure DocumentDB (with MongoDB compatibility), what it is, and how it can be used to build solutions for unstructured data.
author: seesharprun
ms.author: sidandrews
ms.topic: overview
ms.date: 12/31/2025
ai-usage: ai-generated
---

# What is Azure DocumentDB (with MongoDB compatibility)?

Azure DocumentDB is a fully managed, open-source, [99.03% MongoDB-compatible](https://learn.microsoft.com/azure/documentdb/compatibility-query-language#compatibility-philosophy) database. Built-in AI, Azure integrations, and multi-cloud flexibility included for mission-critical applications.

## Open-source and community-driven

[DocumentDB](https://github.com/documentdb/documentdb) is an open-source, MongoDB-compatible, Linux Foundation–governed document database released under the permissive MIT license .
Azure DocumentDB is built on DocumentDB, it does not run the MongoDB database server or its codebase. [MongoDB’s SSPL licensing](https://en.wikipedia.org/wiki/Server_Side_Public_License) does not apply to DocumentDB or Azure DocumentDB.

DocumentDB delivers 99.03% MongoDB compatibility via the wire protocol and BSON support, plus capabilities such as indexing and vector search, while keeping the implementation transparent and community-driven.

Azure DocumentDB pairs that open-source foundation with a fully managed Azure service, adding fully-managed enterprise security, scalability, and reliability.

## Flexible and scalable data management

Azure DocumentDB allows you to store and manage unstructured data with ease. Its schema-agnostic design means you can adapt your data model as your application evolves, without worrying about rigid structures. This flexibility is ideal for applications that require rapid iteration or deal with diverse data types.

The service supports high-capacity vertical and horizontal scaling with no shard key required until the database surpasses terabytes. You can automatically shard existing databases with no downtime, and scale clusters up or down—both vertically and horizontally—all while keeping your applications running.

## 99.03% MongoDB compatibility

Azure DocumentDB is designed to work seamlessly with MongoDB tools and drivers, making it easy for developers to migrate existing applications or build new ones. By supporting MongoDB APIs, the service allows you to apply your existing knowledge and resources without the need for extensive rework.

This compatibility also means you can integrate Azure DocumentDB into your existing development workflows, using popular tools like MongoDB Compass or the MongoDB shell. The result is a smooth development experience that accelerates your time to market.

## Multi-cloud and hybrid-cloud

DocumentDB enables true multi-cloud and hybrid architectures with zero data loss. The open-source database can run on-premises or in any cloud, and Azure DocumentDB extends the same capability as a fully managed Azure service. Together, they allow applications to use the same MongoDB-compatible interface and drivers across environments, while supporting cross-cloud replication and failover without data loss or application changes.

To get started, deploy DocumentDB using the [Kubernetes operator](https://github.com/documentdb/documentdb-kubernetes-operator).

See the [multi-cloud replication demo](https://www.youtube.com/watch?v=uRBGvXWfBis) on YouTube.

## AI-driven applications with integrated vector database

Azure DocumentDB empowers generative AI applications with an integrated vector database at no additional cost, enabling indexing and querying of high-dimensional data for advanced AI use cases. Unlike other platforms, Azure DocumentDB keeps all original data and vector data within the database, ensuring simplicity and security without external integrations. Even the free tier includes vector database capabilities, making sophisticated AI features accessible.

## Native Azure integration

Azure DocumentDB provides seamless integration with the Azure ecosystem, enabling developers to manage resources using familiar Azure tools like Azure Monitor and Azure CLI. This deep integration ensures efficient resource management and unified support across all your Azure services, eliminating the need to juggle multiple support teams.

