---
title: Connection Pooling Strategy Using PgBouncer in Azure Database for PostgreSQL Flexible Server
description: This article describes the best practices for connection pooling in an Azure Database for PostgreSQL flexible server.
#customer intent: As a user managing an Azure Database for PostgreSQL flexible server, I want to understand connection pooling with PgBouncer, so that I can reduce resource usage and improve application performance.
author: varun-dhawan
ms.author: varundhawan
ms.reviewer: maghan
ms.date: 07/08/2026
ms.service: azure-database-postgresql
ms.subservice: connectivity
ms.topic: best-practice
---

# Connection pooling strategy using PgBouncer in Azure Database for PostgreSQL flexible server

This article provides strategic guidance for selecting a connection pooling mechanism for your Azure Database for PostgreSQL flexible servers.

## Introduction

When you use an Azure Database for PostgreSQL flexible server, you create a connection to the database by establishing a communication channel between the client application and the server. This channel manages data, executes queries, and initiates transactions. After you establish the connection, the client application can send commands to the server and receive responses. However, creating a new connection for each operation can cause performance problems for mission-critical applications. Every time you create a new connection, Azure Database for PostgreSQL starts a new process by using the postmaster process, which consumes more resources.

To address this problem, use connection pooling to create a cache of connections that Azure Database for PostgreSQL can reuse. When an application or client requests a connection, it comes from the connection pool. After the session or transaction finishes, the connection goes back to the pool for reuse. By reusing connections, you reduce resource usage and improve performance.

:::image type="content" source="./media/concepts-connection-pooling-best-practices/connection-patterns.png" alt-text="Diagram for Connection Pooling Patterns.":::

Although different tools exist for connection pooling, this section discusses different strategies to use connection pooling by using **PgBouncer**.

## What is PgBouncer?

**PgBouncer** is an efficient connection pooler designed for PostgreSQL. It reduces processing time and optimizes resource usage when managing multiple client connections to one or more databases. **PgBouncer** offers three distinct pooling modes for connection rotation:

- **Session pooling:** This method assigns a server connection to the client application for the entire duration of the client's connection. When the client application disconnects, **PgBouncer** promptly returns the server connection back to the pool. Session pooling is the default mode in open source PgBouncer. For more information, see [PgBouncer configuration](https://www.pgbouncer.org/config.html).
- **Transaction pooling:** With transaction pooling, a server connection is dedicated to the client application during a transaction. Once the transaction is successfully completed, **PgBouncer** releases the server connection, making it available again within the pool. Transaction pooling is the default mode in Azure Database for PostgreSQL's in-built PgBouncer, and it doesn't support prepared transactions.
- **Statement pooling:** In statement pooling, a server connection is allocated to the client application for each individual statement. Upon the statement's completion, the server connection is returned to the connection pool. Multi-statement transactions aren't supported in this mode.

You can use PgBouncer in three distinct usage patterns:

- **PgBouncer and application colocation deployment**
- **Application independent centralized PgBouncer deployments**
- **Built-in PgBouncer and database deployment**


Each of these patterns has its own advantages and disadvantages.

## PgBouncer and application colocation deployment

When you use this approach, you deploy PgBouncer on the same server where your application is hosted. You can deploy the application and PgBouncer on traditional virtual machines or within a microservices-based architecture, as highlighted:

### PgBouncer deployed in application VM

If your application runs on an Azure VM, you can set up PgBouncer on the same VM. To install and configure PgBouncer as a connection pooling proxy with your Azure Database for PostgreSQL flexible server, see [Steps to install and setup PgBouncer connection pooling proxy](https://techcommunity.microsoft.com/t5/azure-database-for-postgresql/steps-to-install-and-setup-pgbouncer-connection-pooling-proxy/ba-p/730555).

:::image type="content" source="./media/concepts-connection-pooling-best-practices/co-location.png" alt-text="Diagram for App co-location on VM.":::


Deploying PgBouncer in an application server can provide several advantages, especially when working with Azure Database for PostgreSQL flexible server databases. Some of the key benefits and limitations of this deployment method are:

**Benefits:**

- **Reduced latency:** By deploying **PgBouncer** on the same application VM, communication between the primary application and the connection pooler is efficient due to their proximity. Deploying PgBouncer in application VM minimizes latency and ensures smooth and swift interactions.
- **Improved security:** **PgBouncer** can act as a secure intermediary between the application and the database, providing an extra layer of security. It can enforce authentication and encryption, ensuring that only authorized clients can access the database.

Overall, deploying PgBouncer in an application server provides a more efficient, secure, and scalable approach to managing connections to Azure Database for PostgreSQL flexible server databases, enhancing the performance and reliability of the application.

**Limitations:**

- **Single point of failure:** If you deploy PgBouncer as a single instance on the application server, it becomes a potential single point of failure. If the PgBouncer instance goes down, it can disrupt the entire database connection pool, causing downtime for the application. To mitigate this single point of failure, set up multiple PgBouncer instances behind a load balancer for high availability.
- **Limited scalability:** PgBouncer scalability depends on the capacity of the server where it's deployed. If the application server reaches its connection limit, PgBouncer might become a bottleneck, limiting the ability to scale the application. You might need to distribute the connection load across multiple PgBouncer instances or consider alternative solutions like connection pooling at the application level.
- **Configuration complexity:** Configuring and fine-tuning PgBouncer can be complex, especially when considering factors such as connection limits, pool sizing, and load balancing. Administrators need to carefully tune the PgBouncer configuration to match the application's requirements and ensure optimal performance and stability.

Weigh these limitations against the benefits and evaluate whether PgBouncer is the right choice for your specific application and database setup.

### PgBouncer deployed as an AKS sidecar

You can use **PgBouncer** as a sidecar container if your application is containerized and running on [Azure Kubernetes Service (AKS)](https://azure.microsoft.com/services/kubernetes-service/), [Azure Container Instance (ACI)](https://azure.microsoft.com/products/container-instances), [Azure Container Apps (ACA)](https://azure.microsoft.com/products/container-apps/), or [Azure Red Hat OpenShift (ARO)](https://azure.microsoft.com/products/openshift/). The sidecar pattern draws its inspiration from the concept of a sidecar that attaches to a motorcycle. An auxiliary container, known as the sidecar container, is attached to a parent application. This pattern enriches the parent application by extending its functionalities and delivering supplementary support.

Deploying PgBouncer in an AKS sidecar tightly couples the application and sidecar lifecycles and shares resources such as hostname and networking to make efficient use of resources. The PgBouncer sidecar operates alongside the application container within the same pod in Azure Kubernetes Service (AKS) with 1:1 mapping, serving as a connection pooling proxy for Azure Database for PostgreSQL flexible servers.

Microsoft publishes a **PgBouncer** sidecar proxy image in Microsoft container registry.

Refer [this](https://techcommunity.microsoft.com/t5/azure-database-for-postgresql/steps-to-install-and-setup-pgbouncer-connection-pooling-on-azure/ba-p/3633043) for more details.

:::image type="content" source="./media/concepts-connection-pooling-best-practices/sidecar-proxy.png" alt-text="Diagram for App co-location on Sidecar.":::

Some of the key benefits and limitations of this deployment method are:

**Benefits:**

- **Reduced Latency:** By deploying **PgBouncer** as an AKS sidecar, communication between the primary application and the connection pooler is seamless and efficient due to their proximity. Deploying  PgBouncer an AKS sidecar minimizes latency and ensures smooth and swift interactions.
- **Simplified Management and Deployment:** The tight coupling of **PgBouncer** with the application container simplifies the management and deployment process. Both components are tightly integrated, so you can administer them more easily and coordinate them seamlessly.
- **High Availability and Connection Resiliency:** If an application container failure or restart occurs, the **PgBouncer** sidecar container closely follows, ensuring high availability. This setup guarantees connection resiliency and maintains predictable performance even during failovers, contributing to a reliable and robust system.

By considering PgBouncer as an AKS sidecar, you can use these advantages to enhance your application's performance, streamline management, and ensure continuous availability of the connection pooler.

**Limitations:**

- **Connection Performance Issues:** Large-scale applications that use thousands of pods, each running sidecar PgBouncer, might encounter potential challenges related to database connection exhaustion. This situation can result in performance degradation and service disruptions. Deploying a sidecar PgBouncer for each pod increases the number of concurrent connections to the database server, which can exceed its capacity. As a result, the database might struggle to handle the high volume of incoming connections, leading to performance problems such as increased response times or even service outages.
- **Complex Deployment:** The utilization of the sidecar pattern introduces a level of complexity to the deployment process, as it involves running two containers within the same pod. This complexity can potentially complicate troubleshooting and debugging activities, requiring extra effort to identify and resolve problems.
- **Scaling Challenges:** The sidecar pattern might not be the ideal choice for applications that demand high scalability. The inclusion of a sidecar container can impose more resource requirements, potentially limiting the number of pods that you can effectively create and manage.

While considering this sidecar pattern, carefully assess the trade-offs between deployment complexity and scalability requirements to determine the most appropriate approach for your specific application scenario.

## Application independent - centralized PgBouncer deployment

When you use this approach, you deploy PgBouncer as a centralized service that's independent of the application. You can deploy the PgBouncer service on traditional virtual machines or within a microservices-based architecture, as highlighted in the following sections:

### PgBouncer deployed in Ubuntu VM behind Azure Load Balancer

Set up the **PgBouncer** connection proxy between the application and database layer behind an Azure Load Balancer, as shown in the following image. In this pattern, you deploy multiple PgBouncer instances behind a load balancer as a service to mitigate single point of failure. This pattern is also suitable in scenarios where the application is running on a managed service like Azure App Services or Azure Functions and connecting to **PgBouncer** service for easy integration with your existing infrastructure.

To install and set up PgBouncer connection pooling proxy with Azure Database for PostgreSQL flexible servers, see [Steps to install and setup PgBouncer connection pooling proxy](https://techcommunity.microsoft.com/t5/azure-database-for-postgresql/steps-to-install-and-setup-pgbouncer-connection-pooling-proxy/ba-p/730555).

:::image type="content" source="./media/concepts-connection-pooling-best-practices/deploying-vm.png" alt-text="Diagram for App co-location on Vm with Load Balancer.":::

Some of the key benefits and limitations of this deployment method are:

**Benefits:**

- **Removing Single Point of Failure:** Application connectivity isn't affected by the failure of a single PgBouncer VM, as several PgBouncer instances are behind Azure Load Balancer.
- **Seamless Integration with Managed Services:** If your application is hosted on a managed service platform such as Azure App Services or Azure Functions, deploying PgBouncer on a VM allows for easy integration with your existing infrastructure.
- **Simplified Setup on Azure VM:** If you're already running your application on an Azure VM, setting up PgBouncer on the same VM is straightforward. Deploying PgBouncer in VM ensures that PgBouncer is deployed in close proximity to your application, minimizing network latency and maximizing performance.
- **Non-Intrusive Configuration:** By deploying PgBouncer on a VM, you can avoid modifying parameters on your Azure Database for PostgreSQL flexible server. This configuration is useful when you want to configure PgBouncer on an Azure Database for PostgreSQL flexible server. For example, changing the SSLMODE parameter to "required" on an Azure Database for PostgreSQL flexible server might cause certain applications that rely on SSLMODE=FALSE to fail. Deploying PgBouncer on a separate VM allows you to maintain the default server configuration while still using PgBouncer's benefits.


By considering these benefits, deploying PgBouncer on a VM offers a convenient and efficient solution for enhancing the performance and compatibility of your application running on Azure infrastructure.

**Limitations:**

- **Management overhead:** As you install **PgBouncer** in a VM, you might have management overhead to manage multiple configuration files. This setup makes it difficult to cope with version upgrades, new releases, and product updates.
- **Feature parity:** If you're migrating from traditional PostgreSQL to an Azure Database for PostgreSQL flexible server and using **PgBouncer**, some feature gaps might exist. For example, lack of md5 support in Azure Database for PostgreSQL.

### Centralized PgBouncer deployed as a service within AKS

If you're working with highly scalable and large containerized deployments on Azure Kubernetes Service (AKS), consisting of hundreds of pods, or in situations where multiple applications need to connect to a shared database, use **PgBouncer** as a standalone service rather than a sidecar container.

By using **PgBouncer** as a separate service, you can efficiently manage and handle connection pooling for your applications on a broader scale. This approach centralizes the connection pooling functionality, enabling multiple applications to connect to the same database resource while maintaining optimal performance and resource utilization.

Use the **PgBouncer** sidecar proxy image published in Microsoft container registry to create and deploy a service.

:::image type="content" source="./media/concepts-connection-pooling-best-practices/centralized-aks.png" alt-text="Diagram for PgBouncer as a service within AKS.":::

Some of the key benefits and limitations of this deployment method are:

**Benefits:**

- **Enhanced Reliability:** Deploying **PgBouncer** as a standalone service allows you to configure it in a highly available manner. This configuration improves the overall reliability of the connection pooling infrastructure, ensuring continuous availability even in the face of failures or disruptions. 
- **Optimal Resource Utilization:** If your application or the database server has limited resources, a separate machine dedicated to running the **PgBouncer** service can be advantageous. By deploying **PgBouncer** on a machine with ample resources, you ensure optimal performance and prevent resource contention problems.
- **Centralized Connection Management:** When centralized management of database connections is a requirement, a standalone **PgBouncer** service provides a more streamlined approach. By consolidating connection management tasks into a centralized service, you can effectively monitor and control database connections across multiple applications, simplifying administration and ensuring consistency.

By considering **PgBouncer** as a standalone service within AKS, you can use these benefits to achieve improved reliability, resource efficiency, and centralized management of database connections.

**Limitations:**

- **Increased N/W Latency:** When deploying **PgBouncer** as a standalone service, consider the potential introduction of more latency. This latency occurs because the application and the PgBouncer service need to pass connections over the network. Evaluate the latency requirements of your application and consider the trade-offs between centralized connection management and potential latency problems.

While **PgBouncer** running as a standalone service offers benefits such as centralized management and resource optimization, assess the impact of potential latency on your application's performance to ensure it aligns with your specific requirements.

## Built-in PgBouncer in Azure Database for PostgreSQL

Azure Database for PostgreSQL offers [PgBouncer](https://github.com/pgbouncer/pgbouncer) as a built-in connection pooling solution. You can enable this optional service on a per-database server basis. PgBouncer runs in the same virtual machine as the Azure Database for PostgreSQL flexible server. As the number of connections increases beyond a few hundred or thousand, Azure Database for PostgreSQL might encounter resource limitations. In such cases, built-in PgBouncer can provide a significant advantage by improving the management of idle and short-lived connections at the database server.

To learn how to enable and set up PgBouncer connection pooling in Azure Database for PostgreSQL, see [PgBouncer in Azure Database for PostgreSQL flexible server](concepts-pgbouncer.md).

Some of the key benefits and limitations of this deployment method are:

**Benefits:**

- **Seamless Configuration:** By using the built-in **PgBouncer** in your Azure Database for PostgreSQL flexible server, you don't need a separate installation or complex setup. You can easily configure it directly from the parameters, ensuring a hassle-free experience.
- **Managed Service Convenience:** As a managed service, you can enjoy the advantages of other Azure managed services. This benefit includes automatic updates, eliminating the need for manual maintenance and ensuring that **PgBouncer** stays up to date with the latest features and security patches.
- **Public and Private Connection Support:** The built-in **PgBouncer** in your Azure Database for PostgreSQL flexible server provides support for both public and private connections. This support allows you to establish secure connections over private networks or connect externally, depending on your specific requirements.
- **High Availability (HA):** In the event of a failover, where a standby server is promoted to the primary role, **PgBouncer** seamlessly restarts on the newly promoted standby without any changes required to the application connection string. This feature ensures continuous availability and minimizes disruption to the application.
- **Cost Efficient:** It's cost efficient as you don't need to pay for extra compute like VM or the containers, though it does have some CPU impact as it's another process running on the same machine.

By using the built-in PgBouncer in an Azure Database for PostgreSQL flexible server, you can enjoy the convenience of simplified configuration, the reliability of a managed service, support for various pooling modes, and seamless high availability during failover scenarios.

**Limitations:**

- **Not supported with Burstable:** **PgBouncer** isn't currently supported with Burstable server compute tier. If you change the compute tier from General Purpose or Memory Optimized to Burstable tier, you lose the **PgBouncer** capability.
- **Re-establish connections after restarts:** Whenever the server restarts during scale operations, HA failover, or a restart, the **PgBouncer** restarts along with the server virtual machine. Hence, existing connections must be re-established.

This article discusses different ways of implementing PgBouncer. The following table summarizes which deployment method to opt for:



|**Selection Criteria**|**PgBouncer on App VM**|**PgBouncer on VM using ALB***|**PgBouncer on AKS Sidecar**|**PgBouncer as a Service**|**Azure Database for PostgreSQL built-in PgBouncer**|
|---|:-:|:-:|:-:|:-:|:-:|
|Simplified Management|:::image type="icon" source="./media/concepts-connection-pooling-best-practices/yellow.png" alt-text="Medium":::|:::image type="icon" source="./media/concepts-connection-pooling-best-practices/yellow.png" alt-text="Medium":::|:::image type="icon" source="./media/concepts-connection-pooling-best-practices/red.png" alt-text="Difficult":::|:::image type="icon" source="./media/concepts-connection-pooling-best-practices/red.png" alt-text="Difficult":::|:::image type="icon" source="./media/concepts-connection-pooling-best-practices/green.png" alt-text="Easy":::|
|HA|:::image type="icon" source="./media/concepts-connection-pooling-best-practices/yellow.png" alt-text="Medium":::|:::image type="icon" source="./media/concepts-connection-pooling-best-practices/yellow.png" alt-text="Medium":::|:::image type="icon" source="./media/concepts-connection-pooling-best-practices/green.png" alt-text="Easy":::|:::image type="icon" source="./media/concepts-connection-pooling-best-practices/green.png" alt-text="Easy":::|:::image type="icon" source="./media/concepts-connection-pooling-best-practices/green.png" alt-text="Easy":::|
|Containerized Apps|:::image type="icon" source="./media/concepts-connection-pooling-best-practices/yellow.png" alt-text="Medium":::|:::image type="icon" source="./media/concepts-connection-pooling-best-practices/yellow.png" alt-text="Medium":::|:::image type="icon" source="./media/concepts-connection-pooling-best-practices/green.png" alt-text="Easy":::|:::image type="icon" source="./media/concepts-connection-pooling-best-practices/green.png" alt-text="Easy":::|:::image type="icon" source="./media/concepts-connection-pooling-best-practices/green.png" alt-text="Easy":::|
|Reduced Network Overhead & Latency|:::image type="icon" source="./media/concepts-connection-pooling-best-practices/green.png" alt-text="Easy":::|:::image type="icon" source="./media/concepts-connection-pooling-best-practices/yellow.png" alt-text="Medium":::|:::image type="icon" source="./media/concepts-connection-pooling-best-practices/green.png" alt-text="Easy":::|:::image type="icon" source="./media/concepts-connection-pooling-best-practices/yellow.png" alt-text="Medium":::|:::image type="icon" source="./media/concepts-connection-pooling-best-practices/yellow.png" alt-text="Medium":::|
|Fine grain control on monitoring and debugging|:::image type="icon" source="./media/concepts-connection-pooling-best-practices/green.png" alt-text="Easy":::|:::image type="icon" source="./media/concepts-connection-pooling-best-practices/green.png" alt-text="Easy":::|:::image type="icon" source="./media/concepts-connection-pooling-best-practices/red.png" alt-text="Difficult":::|:::image type="icon" source="./media/concepts-connection-pooling-best-practices/red.png" alt-text="Difficult":::|:::image type="icon" source="./media/concepts-connection-pooling-best-practices/green.png" alt-text="Easy":::|



:::image type="icon" source="./media/concepts-connection-pooling-best-practices/black.png" alt-text="Legend"::: **Legend**


|**Difficulty Level**|**Symbol**|
|---|:-:|
|Easy |:::image type="icon" source="./media/concepts-connection-pooling-best-practices/green.png" alt-text="Easy":::|
|Medium| :::image type="icon" source="./media/concepts-connection-pooling-best-practices/yellow.png" alt-text="Medium":::|
|Difficult |:::image type="icon" source="./media/concepts-connection-pooling-best-practices/red.png" alt-text="Difficult":::|


*ALB: Azure Load Balancer.

## Related content

- [PgBouncer in Azure Database for PostgreSQL flexible server](concepts-pgbouncer.md)
- [Connection libraries](concepts-connection-libraries.md)

