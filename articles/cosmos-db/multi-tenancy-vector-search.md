---
title: Multitenancy in Azure Cosmos DB
description: Review critical concepts required to build multitenant generative AI applications in Azure Cosmos DB.
author: TheovanKraay
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: concept-article
ms.date: 09/24/2025
ms.update-cycle: 180-days
ms.author: thvankra
ms.collection:
  - ce-skilling-ai-copilot
appliesto:
  - ✅ NoSQL
  - ✅ PostgreSQL
---

# Multitenancy for vector search in Azure Cosmos DB

> "OpenAI relies on Cosmos DB to dynamically scale their ChatGPT service—one of the fastest-growing consumer apps ever—enabling high reliability and low maintenance."
> — Satya Nadella

Azure Cosmos DB stands out as the world's first full-featured serverless operational database with vector search, offering unparalleled scalability and performance. By using Azure Cosmos DB, users can enhance their vector search capabilities, ensuring high reliability and low maintenance for multitenant applications.

Multitenancy enables a single instance of a database to serve multiple customers, or tenants, simultaneously. This approach efficiently shares infrastructure and operational overhead, resulting in cost savings and simplified management. It's a crucial design consideration for SaaS applications and some internal enterprise solutions.

Multitenancy introduces complexity. Your system must scale efficiently to maintain high performance across all tenants, who might have unique workloads, requirements, and service-level agreements (SLAs).

Imagine a fictional AI-assisted research platform called ResearchHub. Serving thousands of companies and individual researchers, ResearchHub manages varying user bases, data scales, and SLAs. Ensuring low query latency and high performance is vital for sustaining an excellent user experience.

Azure Cosmos DB, with its [DiskANN vector index](index-policy.md#vector-indexes) capability, simplifies multitenant design, providing efficient data storage and access mechanisms for high-performance applications.

## Multi-tenancy models in Azure Cosmos DB

In Azure Cosmos DB, we recommend two primary approaches to managing multi-tenancy: *partition key-per-tenant* or *account-per-tenant*, each with its own set of benefits and trade-offs.

### Partition key-per-tenant

For a higher density of tenants and lower isolation, the partition key-per-tenant model is effective. Each tenant is assigned a unique partition key within a given container, allowing logical separation of data. This strategy works best when each tenant has roughly the same workload volume. If there is significant skew, customers should consider isolating those tenants in their own account. Additionally, if a single tenant has more than 20GB of data, [hierarchical partition keys (HPK)](#hierarchical-partitioning-enhanced-data-organization) should be used. For vector search in particular, quantizedFlat index might perform well if vector search queries can be focused to a particular partition or sets of partitions.

**Benefits:**
- **Cost efficiency:** Sharing a single Cosmos DB account across multiple tenants reduces overhead.
- **Scalability:** Can manage a large number of tenants, each isolated within their partition key.
- **Simplified management:** Fewer Cosmos DB accounts to manage.
- **Hierarchical partition keys (HPK):** Optimizes data organization and query performance in multitenant apps with a high number of tenants.

**Drawbacks:**
- **Resource contention:** Shared resources can lead to contention during peak usage.
- **Limited isolation:** Logical but not physical isolation, which might not meet strict isolation requirements.
- **Less flexibility:** Reduced flexibility per tenant for enabling account-level features like geo-replication, point-in-time restore, and customer-managed keys.

#### Hierarchical partitioning: enhanced data organization

[Hierarchical partitioning](hierarchical-partition-keys.md) builds on the partition key-per-tenant model, adding deeper levels of data organization. This method involves creating multiple levels of partition keys for more granular data management. The lowest level of  hierarchical partitioning should have high cardinality. Typically, it's recommended to use an ID/guid for this level to ensure continuous scalability beyond 20GB per tenant.

**Advantages:**
- **Optimized queries:** More precise targeting of subpartitions at the parent partition level reduces query latency.
- **Improved scalability:** Facilitates deeper data segmentation for easier scaling.
- **Better resource allocation:** Evenly distributes workloads, minimizing bottlenecks for high tenant counts.

**Considerations:**
- If applications have very few tenants and use hierarchical partitioning, this can lead to bottlenecks since all documents with the same first-level key write to the same physical partitions.

**Example:**
ResearchHub can stratify data within each tenant’s partition by organizing it at various levels such as *DepartmentId* and *ResearcherId*, facilitating efficient management and queries.

:::image type="content" source="../media/gen-ai/multi-tenant/hpk.png" alt-text="Diagram showing AI data stratification.":::

### Account-per-tenant

For maximum isolation, the account-per-tenant model is preferable. Each tenant gets a dedicated Cosmos DB account, ensuring complete separation of resources.

**Benefits:**
- **High isolation:** No contention or interference due to dedicated resources.
- **Custom SLAs:** Resources and SLAs can be tailored to individual tenant needs.
- **Enhanced security:** Physical data isolation ensures robust security.
- **Flexibility:** Tenants can enable account-level features like geo-replication, point-in-time restore, and customer-managed keys as needed.

**Drawbacks:**
- **Increased management:** Higher complexity in managing multiple Cosmos DB accounts.
- **Higher costs:** More accounts mean higher infrastructure costs.

## Security isolation with customer-managed keys

Azure Cosmos DB enables [customer-managed keys](how-to-setup-customer-managed-keys.md) for data encryption, adding an extra layer of security for multitenant environments.

**Steps to implement:**
- **Set up Azure Key Vault:** Securely store your encryption keys.
- **Link to Cosmos DB:** Associate your Key Vault with your Cosmos DB account.
- **Rotate keys regularly:** Enhance security by routinely updating your keys.

Using customer-managed keys ensures each tenant's data is encrypted uniquely, providing robust security and compliance.

:::image type="content" source="../media/gen-ai/multi-tenant/account.png" alt-text="Diagram showing an example AI account-per-tenant.":::

## Other isolation models

### Container and database isolation

In addition to the partition key-per-tenant and account-per-tenant models, Azure Cosmos DB provides other isolation methods such as *container isolation* and *database isolation*. These approaches offer varying degrees of performance isolation, though they don't provide the same level of security isolation as the account-per-tenant model.

#### Container isolation

In the container isolation model, each tenant is assigned a separate container within a shared Cosmos DB account. This model allows for some level of isolation in terms of performance and resource allocation.

**Benefits:**
- **Better performance isolation:** Containers can be allocated specific performance resources, minimizing the effect of one tenant’s workload on another.
- **Easier management:** Managing multiple containers within a single account is generally easier than managing multiple accounts.
- **Cost efficiency:** Similar to the partition key-per-tenant model, this method reduces the overhead of multiple accounts.

**Drawbacks:**
- **Limited security isolation:** Unlike separate accounts, containers within the same account don't provide physical data isolation. So, this model might not meet stringent security requirements.
- **Resource contention:** Heavy workloads in one container can still affect others if resource limits are breached.

#### Database isolation

The database isolation model assigns each tenant a separate database within a shared Cosmos DB account. This provides enhanced isolation in terms of resource allocation and management.

**Benefits:**
- **Enhanced performance:** Separate databases reduce the risk of resource contention, offering better performance isolation.
- **Flexible resource allocation:** Resources can be allocated and managed at the database level, providing tailored performance capabilities.
- **Centralized management:** Easier to manage compared to multiple accounts, yet offering more isolation than container-level separation.

**Drawbacks:**
- **Limited security isolation:** Similar to container isolation, having separate databases within a single account doesn't provide physical data isolation.
- **Complexity:** Managing multiple databases can be more complex than managing containers, especially as the number of tenants grows.

While container and database isolation models don't offer the same level of security isolation as the account-per-tenant model, they can still be useful for achieving performance isolation and flexible resource management. These methods are beneficial for scenarios where cost efficiency and simplified management are priorities, and stringent security isolation isn't a critical requirement.

By carefully evaluating the specific needs and constraints of your multitenant application, you can choose the most suitable isolation model in Azure Cosmos DB, balancing performance, security, and cost considerations to achieve the best results for your tenants.

## Real-world implementation considerations

When designing a multitenant system with Cosmos DB, consider these factors:

- **Tenant workload:** Evaluate data size and activity to select the appropriate isolation model.
- **Performance requirements:** Align your architecture with defined SLAs and performance metrics.
- **Cost management:** Balance infrastructure costs against the need for isolation and performance.
- **Scalability:** Plan for growth by choosing scalable models.

### Practical implementation in Azure Cosmos DB

**Partition key-per-tenant:**
- **Assign Partition Keys:** Unique keys for each tenant ensure logical separation.
- **Store data:** Tenant data is confined to respective partition keys.
- **Optimize queries:** Use partition keys for efficient, targeted queries.

**Hierarchical partitioning:**
- **Create multi-level keys:** Further organize data within tenant partitions.
- **Targeted queries:** Enhance performance with precise subpartition targeting.
- **Manage resources:** Distribute workloads evenly to prevent bottlenecks.

**Account-per-tenant:**
- **Provide separate accounts:** Each tenant gets a dedicated Cosmos DB account.
- **Customize resources:** Tailor performance and SLAs to tenant requirements.
- **Ensure security:** Physical data isolation offers robust security and compliance.

## Best practices for using Azure Cosmos DB with vector search

Azure Cosmos DB's support for DiskANN vector index capability makes it an excellent choice for applications that require fast, high-dimensional searches, such as AI-assisted research platforms like ResearchHub. Here’s how you can apply these capabilities:

**Efficient storage and retrieval:**
- **Vector indexing:** Use the DiskANN vector index to efficiently store and retrieve high-dimensional vectors. This is useful for applications that involve similarity searches in large datasets, such as image recognition or document similarity.
- **Performance optimization:** DiskANN’s vector search capabilities enable quick, accurate searches, ensuring low latency and high performance, which is critical for maintaining a good user experience.

**Scaling across tenants:**
- **Partition key-per-tenant:** Utilize partition keys to logically isolate tenant data while benefiting from Cosmos DB’s scalable infrastructure.
- **Hierarchical partitioning:** Implement hierarchical partitioning to further segment data within each tenant’s partition, improving query performance and resource distribution.

**Security and compliance:**
- **Customer-managed keys:** Implement customer-managed keys for data encryption at rest, ensuring each tenant’s data is securely isolated.
- **Regular key rotation:** Enhance security by regularly rotating encryption keys stored in Azure Key Vault.

### Real-world example: implement ResearchHub

**Partition key-per-tenant:**
- **Assign partition keys:** Each organization (tenant) is assigned a unique partition key.
- **Data storage:** All researchers’ data for a tenant is stored within its partition, ensuring logical separation.
- **Query optimization:** Queries are executed using the tenant's partition key, enhancing performance by isolating data access.

**Hierarchical partitioning:**
- **Multi-level partition keys:** Data within a tenant’s partition is further segmented by *DepartmentId* and *ResearcherId* or other relevant attributes.
- **Granular Data Management:** This hierarchical approach allows ResearchHub to manage and query data more efficiently, reducing latency, and improving response times.

**Account-per-tenant:**
- **Separate Cosmos DB accounts:** High-profile clients or those with sensitive data are provided individual Cosmos DB accounts.
- **Custom configurations:** Resources and SLAs are tailored to meet the specific needs of each tenant, ensuring optimal performance and security.
- **Enhanced data security:** Physical separation of data with customer-managed encryption keys ensures robust security compliance.

## Conclusion

Multi-tenancy in Azure Cosmos DB, especially with its DiskANN vector index capability, offers a powerful solution for building scalable, high-performance AI applications. Whether you choose partition key-per-tenant, hierarchical partitioning, or account-per-tenant models, you can effectively balance cost, security, and performance. By using these models and best practices, you can ensure that your multitenant application meets the diverse needs of your customers, delivering an exceptional user experience.

Azure Cosmos DB provides the tools necessary to build a robust, secure, and scalable multitenant environment. With the power of DiskANN vector indexing, you can deliver fast, high-dimensional searches that drive your AI applications.

## Related content

- [Multitenancy and Azure Cosmos DB](https://aka.ms/CosmosMultitenancy)
- [Use the Azure Cosmos DB lifetime free tier](free-tier.md)
