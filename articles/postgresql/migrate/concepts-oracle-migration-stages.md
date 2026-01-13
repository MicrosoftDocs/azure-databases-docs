---
title: "Oracle to Azure Database for PostgreSQL Migration Stages"
description: "This article outlines the key stages involving successful Oracle to Azure Database for PostgreSQL migrations."
author: JaredMSFT
ms.author: jaredmeade
ms.reviewer: maghan
ms.date: 01/24/2025
ms.service: azure-database-postgresql
ms.topic: concept-article
---

# Oracle To Azure Database for PostgreSQL Migration Stages

A comprehensive end-to-end migration from Oracle to Azure Postgres requires the careful execution of several key steps and migration stages. These milestones are all closely related and essential to a complete and successful migration.



## Discovery

Most customers are already well acquainted with the quantities and locations of their Oracle database instances (especially their associated licensing costs), however for the sake of completeness we are highlighting this phase as an important starting point in your migration. The Discovery phase is an ideal stage to determine the appropriate scope of your migration efforts. Do you have an Oracle database server "farm" environment requiring tens, hundreds, or even thousands of databases to migrate? Are you considering an at-scale migration following a "migration factory" approach? Rather, is your environment more suitable for the end-to-end migration of a single database alongside a parallel modernization of all connected clients before moving onto the next database on the migration list? In either case, an up-to-date and thorough inventory is a critical prerequisite, and the Discovery phase ensures you are prepared for success.

## Assessments

Assessments encapsulate many different types of estimate-based exploratory operations which are individually defined by their unique characteristics. Some assessments are designed to estimate and categorize the complexity of effort and resources involved in migration of database objects and based upon factors such as the numbers of objects (potentially even exploring the number of lines of code) requiring attention from a subject matter expert. Alternatively, other types of assessments explore the structure and size of the underlying data and provide guidance regarding the amount of time required to fully migrate data to the destination environment. Yet another assessment type is structured to ensure your destination Azure Postgres resources are appropriately scaled to accommodate the compute, memory, IOPS, and network configuration required to service your data. One of the most important assessments which must be included to ensure your migration success is a thorough review and consideration of all connected clients and the scope comprising all dependent applications. To summarize, when preparing your migration assessments, ensure you are assessing all aspects of your database migration, including:

- Database schema / code conversion quantity and complexity
- Database size and scale
- Database resource operating requirements
- Client application code migration

Your assessment accuracy will be closely tied to the specific underlying tools and service platforms involved in the execution and completion of subsequent migration steps. It's therefore important to consider that there are several factors which can impact the accuracy of these assessment estimates and reported results are directly correlated to the underlying tools utilized in your migration assessment. Care must be taken to avoid interpolating estimate outputs from different or combined tools when reviewing and incorporating assessment outputs into your migration plans.

For more information, see our [Oracle to Azure Postgres Migration Playbook](https://download.microsoft.com/download/8/f/c/8fc4fe39-7cb1-484a-aaa0-418704b90c0e/Oracle%20to%20Azure%20Postgres%20Migration%20Playbook.pdf)

## Database Schema Migration

Structured data definitions are one of the hallmarks of transactional database engines and an essential foundation to a well-designed data platform. Ensuring that your unique Oracle data structures and data type definitions will be properly mapped to their respective tables within Azure Postgres is a critical requirement to the overall success in your migration. While all transactional databases share many similarities, data table and column data type differences do exist and care must be taken to ensure your data isn't inadvertently lost, truncated, or mangled due to mismatched data definitions. Numeric data types, date/time data types, and text-based data types are just some examples of areas that must be closely examined when developing corresponding data mappings for your migration.

For additional information and examples of the differences between Oracle and Postgres data types, see our [Oracle to Azure Postgres Migration Playbook](https://download.microsoft.com/download/8/f/c/8fc4fe39-7cb1-484a-aaa0-418704b90c0e/Oracle%20to%20Azure%20Postgres%20Migration%20Playbook.pdf)

## Database Code Migration

Database code migration refers to the process of converting database code written for Oracle to be compatible with the Postgres database engine, while maintaining both the original functionality and existing performance characteristics. This process entails converting Oracle PL/SQL queries, stored procedures, functions, triggers, and other database objects to be compliant Postgres PL/pgSQL. Fortunately, Oracle's PL/SQL and Postgres' PL/pgSQL procedural language dialects share many similarities, and this is commonly the initial factor many organizations identify when selecting Postgres as the best fit for Oracle database migrations. There are, however, some unique differences and distinctions between the two database languages which must be considered. Areas of attention include: database-specific keywords and syntax, exception handling, built-in functions, data types, and sequence incrementation.

In many instances, the Postgres extension ecosystem can be a powerful ally to assist with streamlining your code migration process. For example, the extension "Oracle Functions for PostgreSQL" (orafce) provides a set of built-in Oracle compatibility functions and packages which can reduce the need to rewrite parts of your codebase that rely on and reference these Oracle functions. Using this compatibility-based approach during the migration of Oracle code to PostgreSQL offers significant advantages in terms of reducing the complexity, time, and cost of the migration process by maintaining your original logic and functionality of your source database definitions, ensures consistency in results, and enhances developer productivity. All of these benefits add up to an achieved simplified and more efficient code migration to PostgreSQL.

For additional information and examples of the differences between Oracle and Postgres built-in functions and logic operators, see our [Oracle to Azure Postgres Migration Playbook](https://download.microsoft.com/download/8/f/c/8fc4fe39-7cb1-484a-aaa0-418704b90c0e/Oracle%20to%20Azure%20Postgres%20Migration%20Playbook.pdf)

## Data Migration

In today's data-driven environment, your data is arguably your most valuable asset. Your data resources increasingly influence every aspect of informed business operations and strategic decision making. It's therefore especially vital that your data migration pipelines operate efficiently and expediently, are fully consistent and verifiable, and ultimately complete successfully.

Your data migration strategy should be carefully considered to determine whether "offline" or "live" approaches are applicable to your environment. Each data migration strategy has its own blend of benefits and considerations, and the choice between "offline" and "live" operations depend on the specific requirements and constraints of your environment. For example, "offline" migrations can be more straightforward and less complex than "live" migrations, however, "offline" migrations involve downtime for the period of time required to fully migrate your data to your destination database. "Live" migrations offer minimal to no downtime, however they involve more complexity and infrastructure to oversee the initial backfill data load and the subsequent data synchronization of changes which might have occurred since the start of the data migration. Careful planning, thorough assessment of business requirements, and consideration of your team's specific critical factors will ensure you are able to make an informed decision fully aligned with your data migration needs.

## Application Code Migration

While external applications might be technically considered outside the domain of database team migration responsibilities, updating and modernizing the database connectivity to your client applications is an essential and closely interrelated stage to the overall success of your database migration journey. As with the other phases of your migration, the associated effort and complexity involved in remediating your client application platform compatibility depends on the unique circumstances of your environment. Are your client applications developed by a third party? If so, it's important to ensure that their software product is certified to support the Postgres database platform. Are your in-house applications using object relational mapping technologies, such as Hibernate or Entity Framework? In some cases, a small configuration or file change might be all that is required. Conversely, if you have significant amounts of database queries and statements embedded within your code, you might need to allocate more time to appropriately review, modify, and validate your code changes.

Alternatively, there are partner solution providers offering novel approaches capable of translating legacy client database operations in real-time. These proxy services provide an abstraction over your database layers which effectively decouple your applications from any database-specific language dependencies.

In many cases, your decision might incorporate a combination of multiple strategies and hybrid approach collectively employed for their respective strengths and combined capabilities. Deploying a real-time database translation layer can enable your teams to rapidly re-deploy their client applications while providing your software engineers and developers with appropriate time and resource planning to refactor their database-specific dependencies to support Postgres native operations.

> [!IMPORTANT]  
> Each of these choices is accompanied by their own particular sets of considerations and benefits and it is essential that your teams carefully review each of these approaches to determine the ideal strategic path forward.

## Migration Validation

When migrating from Oracle to PostgreSQL, ensuring data integrity and logical consistency are both paramount. Migration validation plays a critical role in this process, as it involves verifying that the data transferred from the source Oracle database is accurate and complete in the target PostgreSQL system. This step is essential not only for maintaining the trustworthiness of the data but also for confirming that the migration process hasn't introduced any errors or discrepancies. Validation checks can include comparing table counts, verifying data types and structures, comparing row-level column values, and ensuring that complex queries yield consistent results across both databases. Additionally, special attention must be paid while handling differences in how the two database systems manage data, such as variations in date and time formats, character encoding, and handling of null values.

This typically involves setting up automated validation scripts that can compare datasets in both databases and highlight any anomalies. Tools and frameworks designed for data comparison can be leveraged to streamline this process. Post-migration validation should be an iterative process, with multiple checks conducted at various stages of the migration to catch issues early and minimize the risk of data corruption. By prioritizing data validation, organizations can confidently transition from Oracle to PostgreSQL, knowing that their data remains reliable and actionable.

## Performance Tuning

Performance is generally viewed as one of the most tangible and important characteristics that determine the perception and usability of your platform. Ensuring that your migration is both accurate and performant is paramount to achieving success and cannot be overlooked. More specifically, query performance is often considered the most critical indicator of optimal database configuration and is commonly used as a litmus test by your users to determine the state of health of your environment.

Fortunately, the Azure platform natively incorporates the tooling and capabilities needed to monitor performance points across a variety of metrics, including scale, efficiency, and perhaps most importantly, speed. These Intelligent Performance features work hand-in-hand with the Postgres monitoring resources to simplify your tuning processes, and in many cases, automate these steps to automatically adapt and adjust as needed. The following Azure tools can ensure your database systems are operating at their very best levels.

### Query Store

Query Store for Azure Postgres serves as the foundation for your monitoring features. Query Store tracks the statistics and operational metrics from your Postgres database, including queries, associated explain plans, resource utilization, and workload timing. These data points can uncover long running queries, queries consuming the most resources, the most frequently run queries, excessive table bloat, and many more operational facets of your database. This information helps you spend less time troubleshooting by quickly identifying any operations or areas requiring attention. Query Store provides a comprehensive view of your overall workload performance by identifying:

- Long running queries, and how they change over time.
- Wait types affecting those queries.
- Details on top database queries by Calls (execution count), by data-usage, by IOPS and by Temporary file usage (potential tuning candidates for performance improvements).
- Drill down details of a query, to view the Query ID and history of resource utilization.
- Deeper insight into overall databases resource consumption.

### Index Tuning

Index tuning is a feature of Azure Database for PostgreSQL flexible server that can automatically improve the performance of your workload by analyzing tracked queries and providing index recommendations. It's natively built into Azure Database for PostgreSQL flexible server, and builds upon Query Store functionality. Index tuning analyzes workloads tracked by Query Store and produces index recommendations to improve the performance of the analyzed workload or to drop duplicate or unused indexes. This is accomplished in three unique ways:

- Identify which indexes are beneficial to create because they could significantly improve the queries analyzed during an index tuning session.
- Identify indexes that are exact duplicates and can be eliminated to reduce the performance impact their existence and maintenance have on the system's overall performance.
- Identify indexes not used in a configurable period that could be candidates to eliminate.

#### Intelligent Tuning

Intelligent Tuning is an ongoing monitoring and analysis process that not only learns about the characteristics of your workload but also tracks your current load and resource usage, such as CPU or IOPS. It doesn't disturb the normal operations of your application workload. The process allows the database to dynamically adjust to your workload by discerning the current bloat ratio, write performance, and checkpoint efficiency on your instance. With these insights, Intelligent Tuning deploys tuning actions that enhance your workload's performance and avoid potential pitfalls. This feature comprises two automatic tuning functions:

- **Autovacuum tuning:** This function tracks the bloat ratio and adjusts autovacuum settings accordingly. It factors in both current and predicted resource usage to prevent workload disruptions.
- **Writes tuning:** This function monitors the volume and patterns of write operations, and it modifies parameters that affect write performance. These adjustments enhance both system performance and reliability, to proactively avert potential complications.

> [!TIP]  
> Learn more about applying [Intelligent Performance](/azure/postgresql/flexible-server/concepts-query-store) to maximize your Azure Postgres platforms.

## Cloud Optimization

Optimization of your new Azure Postgres database environment signifies the culmination of all the incredible effort and hard work that has led your team to arrive at this key point. Cloud optimization might be a new responsibility, especially when coming from an on-premises or legacy database environment. The Azure cloud platform introduces a new and enhanced set of valuable and cutting-edge scalability features allowing your team to "dial-in" the precise allocation of resources, features, and cost-efficiency to match your organizational needs today, and well on into the future. Cloud Optimization is an ongoing process of continuous refinement to your environment as viewed through the lenses of the best practices associated with the Microsoft well-architected Framework: cost optimization, operational excellence, performance efficiency, reliability, and security.

**Cost Optimization** is a combination of right-sizing your resources, applying strategies for cost management, and efficient resource utilization.

**Operating Excellence** includes the adoption of automation for deployments, monitoring, and scaling, and reduces error while increasing efficiency.

**Performance Efficiency** ensures you choose the appropriate resources to meet requirements without over-provisioning, while also applying best practices for scalability to handle varying loads efficiently during peak operational periods.

**Reliability** guides you toward designed highly available and fault-tolerant systems with redundancy and failover mechanisms to minimize downtime, and disaster recovery strategies for implementing robust recovery plans, including backup and restore procedures.

**Security** emphasizes the importance of strong identity protocols and access management practices, such as least privilege access, password-less authentication, and role-based access control. Data protection and encryption ensures sensitive data is protected both at rest and in transit. Security also includes tools and best practices for threat-detection, and automated responses to address security incidents promptly. Compliance ensures your environment complies with industry standards and regulations.

For more information on the five pillars of cloud optimization implementation guidance and fundamentals, please visit our [Azure Well-Architected Framework (WAF) center](/azure/well-architected/).

To ensure these pillars are aligned to your Azure Postgres deployment, review our [Azure Well-Architected Framework Service Guide for PostgreSQL](/azure/well-architected/service-guides/postgresql).

## Related content

- [Oracle to Azure PostgreSQL Best Practices](./best-practices-oracle-to-postgresql.md)
- [Oracle to Azure PostgreSQL Migration Playbook](https://download.microsoft.com/download/8/f/c/8fc4fe39-7cb1-484a-aaa0-418704b90c0e/Oracle%20to%20Azure%20Postgres%20Migration%20Playbook.pdf)
- [Oracle to Azure PostgreSQL Migration Workarounds](https://github.com/Microsoft/DataMigrationTeam/blob/master/Whitepapers/Oracle%20to%20Azure%20Database%20for%20PostgreSQL%20Migration%20Workarounds.pdf)
- [Azure Database for PostgreSQL Migration Partners](./partners-migration-postgresql.md)
