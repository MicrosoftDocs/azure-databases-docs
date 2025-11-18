---
title: Introduction/overview
description: Learn about Azure DocumentDB (with MongoDB compatibility), what it is, and how it can be used to build solutions for unstructured data.
author: seesharprun
ms.author: sidandrews
ms.topic: overview
ms.date: 11/12/2025
ai-usage: ai-generated
---

# What is Azure DocumentDB (with MongoDB compatibility)?

Azure DocumentDB is a fully managed MongoDB-compatible database service for building modern applications. It combines native Azure integrations, low total cost of ownership, and a familiar architecture—ideal for migrating existing applications or building new ones.

## Flexible and scalable data management

Azure DocumentDB allows you to store and manage unstructured data with ease. Its schema-agnostic design means you can adapt your data model as your application evolves, without worrying about rigid structures. This flexibility is ideal for applications that require rapid iteration or deal with diverse data types.

The service supports high-capacity vertical and horizontal scaling with no shard key required until the database surpasses terabytes. You can automatically shard existing databases with no downtime, and scale clusters up or down—both vertically and horizontally—all while keeping your applications running.

## High performance and low latency

Performance is a critical factor for modern applications, and Azure DocumentDB is optimized to deliver low-latency responses. With features like automatic indexing and partitioning, the service ensures that your queries are executed efficiently, even as your dataset grows.

Additionally, Azure DocumentDB supports various consistency levels, allowing you to balance performance and data accuracy based on your application's requirements. This flexibility ensures that you can optimize for speed without compromising on reliability.

## Seamless MongoDB compatibility

Azure DocumentDB is designed to work seamlessly with MongoDB tools and drivers, making it easy for developers to migrate existing applications or build new ones. By supporting MongoDB APIs, the service allows you to apply your existing knowledge and resources without the need for extensive rework.

This compatibility also means you can integrate Azure DocumentDB into your existing development workflows, using popular tools like MongoDB Compass or the MongoDB shell. The result is a smooth and efficient development experience that accelerates your time to market.

## AI-driven applications with integrated vector database

Azure DocumentDB empowers generative AI applications with an integrated vector database, enabling efficient indexing and querying of high-dimensional data for advanced AI use cases. Unlike other platforms, Azure DocumentDB keeps all original data and vector data within the database, ensuring simplicity and security without external integrations. Even the free tier includes vector database capabilities, making sophisticated AI features accessible at no extra cost.

## Native Azure integration

Azure DocumentDB provides seamless integration with the Azure ecosystem, enabling developers to manage resources using familiar Azure tools like Azure Monitor and Azure CLI. This deep integration ensures efficient resource management and unified support across all your Azure services, eliminating the need to juggle multiple support teams.

## Open-source and community-driven

The underlying DocumentDB technology is open-sourced ([`microsoft/documentdb`](https://github.com/documentdb/documentdb)), providing developers with complete transparency and flexibility. DocumentDB is built as an extension on the robust PostgreSQL engine, it offers a permissive MIT license, ensuring there are minimal restrictions on usage, distribution, or integration into your own solutions. By using PostgreSQL's extensibility, DocumentDB introduces powerful features to PostgreSQL like binary JSON (BSON) types, automatic indexing, and vector search. DocumentDb is a versatile choice for modern applications.

This open-source approach also aligns with Microsoft's broader mission to establish a standard for NoSQL databases, enhancing interoperability and simplifying the developer experience. Whether you're building on-premises solutions or cloud-based applications, DocumentDB empowers you with the tools and freedom to innovate. 

Azure DocumentDB combines the flexible and open-source DocumentDB platform with the best-in-class security, scalability, and reliability of Azure.
