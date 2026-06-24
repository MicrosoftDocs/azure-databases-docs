---
title: Shared Responsibility Model for Azure Managed Instance for Apache Cassandra
description: Detailed information about the support model and responsibilities.
author: ManishSharma
ms.author: mansha
ms.service: azure-managed-instance-apache-cassandra
ms.topic: how-to
ms.date: 01/28/2026
ms.custom: sfi-image-nochange, sfi-ropc-blocked
---

# Azure Managed Instance for Apache Cassandra Shared Responsibility Model

## Introduction
This document defines the division of responsibilities between Microsoft and customers when using **Azure Managed Instance for Apache Cassandra (Cassandra MI)**.

The goal is to provide clarity on:
- Operational ownership boundaries  
- Performance and availability expectations  
- Security and compliance responsibilities  

> [!Important]
> - There's **no latency SLA**. Performance depends on the SKU you select and workload characteristics.
> - Microsoft guarantees **uptime of the Cassandra process**, not API-level performance or query latency.
> - Issues caused by **resource saturation (CPU, disk, memory, network)** must be investigated and mitigated by the customer. Microsoft provides metrics and logs to support this analysis.

## Microsoft Responsibilities

Microsoft operates and manages the underlying infrastructure for Cassandra MI. This responsibility includes:

### Infrastructure and platform
- Provisioning of Cassandra clusters, datacenters, and nodes  
- Operating system management, patching, and security updates  
- Hardware and host infrastructure lifecycle management  
- Network isolation by using Azure Virtual Networks (VNets)

### Availability and SLA
- SLA-backed availability for **production datacenters only**
- SLA applies to:
  - OS  
  - Cassandra process  
  - Hardware failures  
- SLA **doesn't cover**:
  - Resource exhaustion (CPU, disk, memory, network)  
  - Application or query-level failures  
- No SLA for:
  - Non-production or deallocated clusters or datacenters  

### Scaling and versioning
- Node scaling (add or remove nodes) triggered through the Azure portal or APIs  
- Availability of new Cassandra versions after stable OSS releases  
- Removal of deprecated versions from provisioning options  

### Security and encryption
- Encryption at rest and in transit  
- Certificate management and rotation for TLS or SSL  
- Continuous vulnerability scanning and remediation  

### Monitoring and support
- Integration with Azure Monitor for logs and metrics  
- Proactive alerts for platform-level outages  
- Root cause analysis (RCA) for platform incidents impacting production

### Backup and restore
- Automated online backups based on your schedule and retention preferences
- Backup restoration through a support request

> [!NOTE]  
> - Customer Managed Keys (CMK) are supported for data at rest.  
> - CMK isn't currently supported for backups.

---

## Customer responsibilities

You're responsible for all **data, schema, and application-level operations**.

### Data modeling and query design
- Designing optimal partition keys and data models  
- Avoiding hot partitions and inefficient queries  
- Query tuning and performance optimization

### Schema and configuration
- Managing keyspaces, replication factors, and consistency levels  
- Performing schema changes  
- Tuning compaction and garbage collection (GC) strategies  
- Overriding default Cassandra configurations when required

### Performance and monitoring
- Monitoring:
  - CPU usage  
  - Memory usage  
  - Disk utilization
  - IOPS and throughput  
- Investigating latency by using:
  - Azure Monitor  
  - Prometheus  
  - Cassandra metrics  

- Taking corrective and preventive actions  

### Capacity planning
- Planning for throughput and storage growth  
- Scaling datacenters up or down as needed

> [!Note] 
> **Storage scaling limitation**
> You can't directly modify disk size. To change disk size, you must:<br>
> - Create a new datacenter with the desired disk size<br>
> - Migrate workloads<br>

### Version upgrades
- Initiating major and minor upgrades (for example, Cassandra 3.x → 5.x)
- Validating application compatibility before upgrades  

> [!Note]
> You're **responsible** for downtime due to outdated or deprecated versions.

### Backup strategy
- Define backup schedules and retention policies.
- Implementing disaster recovery (DR) strategy  

### Networking
- Configuring:
  - VNets, subnets, and NSGs  
  - DNS resolution  
  - Firewall rules  

- Setting up:
  - VPN / ExpressRoute (if hybrid)  

### Security and access
- Managing database users and roles  
- Implementing application-level encryption (if required)  
- Ensuring compliance with regulatory requirements  

### Operations
- Handling application-level issues:
  - Query timeouts  
  - Tombstone accumulation  
  - Data inconsistencies  

- Using approved tools (no SSH/JMX access)  
- Reviewing logs and acting on anomalies  

---

## Shared Responsibilities

Some areas require collaboration between Microsoft and the customer:

### Security monitoring
- Microsoft provides logs and telemetry  
- Customers must:
  - Review alerts  
  - Investigate anomalies  
  - Take corrective actions  
> [!NOTE]
> If **mTLS (mutual TLS)** is used:<br>
> - Client-side certificate lifecycle and renewal is the **customer’s responsibility**

### Hybrid deployments
- Microsoft manages Azure-hosted nodes  
- Customers manage on-premises Cassandra nodes  
- Connectivity between environments is a **shared responsibility**  

### Compliance
- Microsoft ensures platform-level compliance  
- Customers own:
  - Application-level compliance  
  - Data governance policies  

### Configuration guidance
Customers are expected to follow Microsoft-recommended configurations, including:
- Required outbound network rules  
- Security and networking best practices  

---

## Responsibility matrix

| Task                                      | Microsoft | Customer |
|-------------------------------------------|----------|----------|
| Infrastructure provisioning & management  | ✅       |          |
| OS & Cassandra patching                   | ✅       |          |
| Backup (platform-managed)                 | ✅       |          |
| Long-term backup scheduling               |          | ✅       |
| Data model design & optimization          |          | ✅       |
| Version upgrades                          |          | ✅       |
| Network configuration                     |          | ✅       |
| Monitoring & alert review                 |          | ✅       |
| Compliance & governance                   | ✅       | ✅       |
| Availability (platform SLA)               | ✅       |          |
| Security                                  | ✅       | ✅       |

---

## Alternative: Azure Cosmos DB for NoSQL API

Azure Cosmos DB (NoSQL API) is a fully managed, cloud-native alternative with additional benefits:

| Benefit                         | Description |
|--------------------------------|------------|
| Native SDK Availability        | SDKs for Java, .NET, Python, Node.js |
| Enterprise-Grade Support       | 24×7 Microsoft support with escalation paths |
| Fully Managed Experience       | Automated patching, backups, compliance |
| Guarantees                | <10 ms latency, 99.999% availability, consistency guarantees, refer [Azure service-level agreements](https://www.microsoft.com/licensing/docs/view/Service-Level-Agreements-SLA-for-Online-Services?lang=1)  |
| Integrated Security & Compliance | Encryption, identity, global compliance certifications |
| Global Distribution & Autoscale | Multi-region replication and automatic scaling |