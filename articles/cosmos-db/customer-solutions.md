---
title: What Are Customers Building?
description: Explore customer use cases and solutions built on Azure Cosmos DB, including benefits, architecture patterns, and real-world examples. Learn more.
author: seesharprun
ms.author: sidandrews
ms.service: azure-cosmos-db
ms.topic: solution-overview
ms.date: 11/07/2025
ai-usage: ai-generated
---

# What are customers building with Azure Cosmos DB?

Azure Cosmos DB empowers organizations worldwide to build innovative, scalable applications that serve millions of users. From global enterprises to fast-growing startups, customers use Azure Cosmos DB's capabilities, global distribution, and guaranteed performance to create solutions that transform their industries.

This article showcases real-world customer stories, highlighting the diverse use cases, architectural patterns, and business outcomes achieved with Azure Cosmos DB.

- [Adobe](#adobe---adobe-experience-cloud-and-adobe-experience-platform)

## Adobe - Adobe Experience Cloud and Adobe Experience Platform

Adobe built a unified customer profile and identity system using Azure Cosmos DB to power real-time personalization, identity stitching, and high-throughput graph workloads.

Adobe selected Azure Cosmos DB because of these reasons:

- Instant, elastic scalability to handle highly dynamic workloads (from near-zero to millions of requests per minute) during campaigns and bursts.
- Multi-model/document-oriented storage that supports the flexible XDM (Experience Data Model) JSON-like schema Adobe uses for extensible customer data.
- Low-latency, globally distributed reads and writes to meet strict activation service level agreements (100–250 ms) for real-time personalization across devices and channels.
- Fine-grained partitioning and throughput control to support large datasets (hundreds of terabytes and thousands of partitions) and massive point-lookup and segmentation workloads.

Adobe integrated Azure Cosmos DB into their solution by:

- Ingesting streaming and batch data into a central platform where event data (web, mobile, transactional, CRM, external) is normalized into XDM. Writing profile fragments into Azure Cosmos DB in near real time by executing extract/transform/load jobs and streaming data pipelines (Kafka, Apache Flink).
- Storing and evolving an identity graph in Azure Cosmos DB to stitch fragmented identifiers (cookies, mobile identifiers, CRM identifiers) into a unified view. The identity graph is used at query time to logically join fragments without physically duplicating data.
- Using Azure Cosmos DB for high-frequency profile lookups, segmentation (both batch and streaming), and graph computations. The system runs millions of point lookups and thousands of segmentation queries with sub-250 ms activation latency.
- Combining Azure Cosmos DB with edge and streaming services to activate profiles in real time—looking up profiles at event ingestion, applying business rules or ML model outputs, and returning personalized responses to applications and channels.

As a result, Adobe's Experience Platform scales to handle billions of daily events and tens of billions of identities while providing real-time activation and governance across customer journeys.

> [!VIDEO eb2e18ed-eb0c-4d12-9c0c-172b795d3cb1]
