---
title: Options to migrate data from MongoDB
description: Review various options to migrate your data from other MongoDB sources to Azure DocumentDB.
author: sandeep-nair
ms.author: sandnair
ms.topic: upgrade-and-migration-article
ms.date: 09/17/2025
ai-usage: ai-assisted
# CustomerIntent: As a MongoDB user, I want to understand the various options available to migrate my data to Azure DocumentDB, so that I can make an informed decision about which option is best for my use case.
---

# What are the options to migrate data from MongoDB to Azure DocumentDB?

This article helps you plan and execute a migration from MongoDB to Azure DocumentDB. It covers the available migration tools, the key phases of a migration, and best practices to reduce risk and minimize downtime.

Whether you're migrating from an on-premises MongoDB server, a cloud-hosted VM, or a managed MongoDB service, the migration options, guidance, and best practices in this article apply.


## Key migration phases

A successful migration follows these distinct phases. Each phase has specific goals and success criteria.

### 1. Assess

Run an automated scan of your source MongoDB by using the [Azure DocumentDB Migration extension](./how-to-assess-plan-migration-readiness.md) to identify unsupported features, commands, query syntax, and index types. The assessment also provides an overview of MongoDB version, license, instance type, and database and collection metrics. Use these findings to plan schema changes and identify any required refactoring before migration.

> [!TIP]
> We recommend you review the [supported MongoDB Query Language (MQL) features and syntax](./compatibility-query-language.md) in detail and perform a proof-of-concept prior to the actual migration.

### 2. Prepare

Analyze the assessment report and measure source TPS (transactions per second). Run trial migrations on representative data to establish target Compute Tier, Storage Tier, and shard count. Conduct performance tests to ensure the target configuration meets your requirements.

### 3. Refine

Prepare target collections with appropriate shard keys and indexes that match your production query patterns. If using multiple shards, decide how to distribute collections across shards to balance load and minimize cross-shard operations.

### 4. Migrate

Run the migration job to move data in either offline or online mode:

- **Offline migration**: Takes a snapshot of the source at the start and bulk-copies it to the target. Any data added, updated, or deleted on the source after the snapshot isn't copied. Required downtime depends on how long the bulk copy takes.
- **Online migration**: Performs the same bulk copy as offline, but also monitors the change stream throughout the process. Changes made during migration are replicated to the target, so the application downtime required is minimal. Requires change stream and a sufficiently large oplog on the source.

> [!TIP]
> For online migrations, ensure that change stream is enabled and the oplog is sized appropriately on your source MongoDB to capture all changes during the migration window.

For available tools, see [Migration tools](#migration-tools).

### 5. Validate

Validate that all data has been copied, including the latest updates. Compare document counts, run sample-based validation, and verify that indexes and data structures match expectations on the target. Use automated scripts to make validation repeatable and consistent.

### 6. Cutover

Move read traffic to the target and verify there are no functional or performance issues. Once read validation is successful, move write traffic to the target. Monitor closely during the cutover window for any anomalies.


## Migration tools

The tools discussed in this article assist you in migrating your MongoDB workloads from the following sources:

- MongoDB Virtual Machine
- MongoDB Atlas
- AWS DocumentDB


### Azure DocumentDB Migration Extension

Create and manage your migration jobs in **Visual Studio Code** with [Azure DocumentDB Migration Extension (Public Preview)](./how-to-migrate-vs-code-extension.md) — a solution designed for **simplicity**, **security**, and **zero downtime**.

This tool provides clear, step-by-step guidance to help you migrate workloads without service interruptions. You can:

- **Select specific databases and collections** for migration  
- Perform all steps **within the familiar VS Code interface**  
- Ensure **secure connectivity** throughout the process  
- Enjoy **zero cost** for using the extension  

With Azure DocumentDB Migration Extension, you can streamline your migration journey while maintaining control and security — all without additional infrastructure or complexity.

### Web App Utility (Online)

Streamline your migration to Azure DocumentDB with [MongoMigrationwebBasedUtility](https://github.com/AzureCosmosDB/MongoMigrationwebBasedUtility) a tool designed for efficiency, reliability, and ease of use. The repository offers detailed, step-by-step instructions for migrating your workloads. This tool offers a seamless experience for both online and offline data migrations. The process is user-friendly, requiring only the source and target details to be provided. It enables you to effortlessly migrate your MongoDB collections while maintaining control, security, and scalability, unlocking the full potential of Azure DocumentDB.

Key features include:

- Supports private deployment within your virtual network for enhanced security
- Automatic resume capabilities if there's connection loss or transient errors
- User-friendly interface
- Access to C# source code on GitHub

The tool supports flexible deployment options and operates independently without dependencies on other Azure resources. Additionally, it offers scalable performance with customizable Azure Web App pricing plans. 

### Native MongoDB tools (Offline)

You can also use the native MongoDB tools such as *mongodump/mongorestore*, *mongoexport/mongoimport* to migrate datasets offline (without replicating live changes) to Azure DocumentDB offering.

| Scenario | MongoDB native tool |
| --- | --- |
| Move subset of database data (JSON/CSV-based) | *mongoexport/mongoimport* |
| Move whole database (BSON-based) | *mongodump/mongorestore* |

- *mongoexport/mongoimport* is the best pair of migration tools for migrating a subset of your MongoDB database.
  - *mongoexport* exports your existing data to a human-readable JSON or CSV file. *mongoexport* takes an argument specifying the subset of your existing data to export.
  - *mongoimport* opens a JSON or CSV file and inserts the content into the target database instance (Azure DocumentDB in this case.).
  - JSON and CSV aren't a compact format; you could incur excess network charges as *mongoimport* sends data to Azure DocumentDB.
- *mongodump/mongorestore* is the best pair of migration tools for migrating your entire MongoDB database. The compact BSON format makes more efficient use of network resources as the data is inserted into Azure DocumentDB.
  - *mongodump* exports your existing data as a BSON file.
  - *mongorestore* imports your BSON file dump into Azure DocumentDB.

> [!NOTE]
> The MongoDB native tools can move data only as fast as the host hardware allows.

## Migration best practices

Use these best practices to reduce risk, estimate capacity more accurately, improve migration speed, and execute cutover safely.

### Reduce failures

- Use URL-encoded passwords in connection strings.
  Special characters such as `@`, `#`, and `:` can break parsing when they aren't encoded. URL encoding helps avoid connection failures during assessment and migration runs.

- Run a premigration assessment before migration.
  Assessment helps you identify unsupported features, compatibility gaps, and potential blockers early. Resolve findings before migration to reduce rework during cutover.

- Practice migration and cutover before production.
  Run one or more rehearsal migrations in a nonproduction environment. Practice improves timing accuracy, team readiness, and confidence during production cutover.

### Size infrastructure accurately

- Run a trial migration on a small but representative dataset.
  Use the trial to capture realistic throughput, latency, and resource consumption. A representative sample gives better estimates than synthetic test data.

- Extrapolate trial results to estimate Compute Tier, Storage Tier, and number of shards.
  Use observed trial metrics to project final sizing needs based on your full dataset volume. Revisit the estimate if your production data distribution differs from the sample.

- Use representative document count, size, and structure with production-like settings.
  Match production indexing and sharding settings during the trial to avoid underestimating cost or migration duration. Nonproduction settings can produce misleading results.

- Estimate target storage from trial outcomes instead of assuming source and target sizes are equal.
  Source and destination storage footprints can differ because of differences in index definitions and data layout. Use trial results to plan storage with a safe buffer.

### Optimize migration speed

- Migrate within the same region when possible.
  Keeping source and target in the same region reduces network latency and improves data transfer performance. It can also reduce cross-region data transfer costs.

- Scale up during migration, then scale down after cutover.
  For example, you can temporarily scale the target cluster to M200 to increase migration throughput. After migration, scale down to an appropriate tier in the supported range for steady-state workloads.

- Choose disks with higher IOPS for faster writes.
  Higher IOPS can significantly improve write-heavy migration performance. Because disk size typically can't be scaled down later, select disk size carefully during planning.

### Plan cutover carefully because there's no rollback

- Plan for downtime during a low-traffic window.
  Required downtime depends on how long your validation steps take after migration catches up. A low-traffic window reduces business impact.

- Stop all writes to the source just before cutover.
  This step prevents last-minute divergence between source and target. Confirm write activity is fully paused before you complete cutover.

- Validate migrated data before moving writes.
  Compare document counts, then run random-sample document comparison (for example, hash-based checks). Use a script when possible to make validation repeatable.

- Update application connection strings and test on the target.
  Run functional and performance validation against target reads and test traffic before enabling production writes. Confirm critical paths behave as expected.

- Move write traffic only after validation succeeds.
  Shift production writes to the target only after test results are successful and consistent. Use a staged rollout if your application architecture supports it.

### Coordinate across teams for seamless migration

- Secure buy-in from all stakeholders: app, data, infrastructure, security, network, and management teams.
  Align expectations and responsibilities early. Shared ownership reduces misunderstandings and delays during execution.

- Use planning and trial runs to build team confidence and refine procedures.
  There are no shortcuts to a smooth migration. Trial runs surface issues in a lower-risk environment and give teams practice.

- Treat cutover as critical and time-sensitive.
  Cutover requires precise coordination and clear communication. Designate decision makers and establish escalation paths before it begins.

- Know who will perform each step, when it should happen, and how to minimize downtime.
  Assign responsibilities, establish timelines, and align on success criteria. Document the cutover runbook and share it with all participants.

- Coordinate with all stakeholders when cutover requires updates to multiple workloads simultaneously.
  Schedule the cutover during a maintenance window that works for all teams. Avoid Friday nights or periods near major business events.

- Do not rush or skip due diligence steps—there is no rollback.
  Thorough validation and careful execution prevent costly mistakes. Accept that cutover takes time; speed-focused shortcuts create risk.



## Related content

- Migrate data to Azure DocumentDB using [native MongoDB tools](how-to-migrate-native-tools.md).
- Migrate data to Azure DocumentDB using the [MongoMigrationwebBasedUtility](https://github.com/AzureCosmosDB/MongoMigrationwebBasedUtility).
