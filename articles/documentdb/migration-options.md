---
title: Options to migrate data from MongoDB
description: Review various options to migrate your data from other MongoDB sources to Azure DocumentDB.
author: sandeep-nair
ms.author: sandnair
ms.topic: upgrade-and-migration-article
ms.date: 09/17/2025
# CustomerIntent: As a MongoDB user, I want to understand the various options available to migrate my data to Azure DocumentDB, so that I can make an informed decision about which option is best for my use case.
---

# What are the options to migrate data from MongoDB to Azure DocumentDB?

This document describes the various options to lift and shift your MongoDB workloads to Azure DocumentDB offering.

Migrations can be done in two ways:

- Offline Migration: A snapshot based bulk copy from source to target. New data added/updated/deleted on the source after the snapshot isn't copied to the target. The application downtime required depends on the time taken for the bulk copy activity to complete.

- Online Migration: Apart from the bulk data copy activity done in the offline migration, a change stream monitors all additions/updates/deletes. After the bulk data copy is completed, the data in the change stream is copied to the target. This process ensures that all updates made during the migration process are also transferred to the target. The application downtime required is minimal.

## Premigration Assessment

Use the [Azure DocumentDB Migration extension](./how-to-assess-plan-migration-readiness.md) to perform a compatibility assessment. The purpose of this stage is to identify any incompatibilities or warnings that exist in the current MongoDB solution. You should resolve the issues found in the assessment results before moving on with the migration process.

> [!TIP]
> We recommend you review the [supported MongoDB Query Language (MQL) features and syntax](./compatibility-query-language.md) in detail and perform a proof-of-concept prior to the actual migration.

## Migration

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

## Related content

- Migrate data to Azure DocumentDB using [native MongoDB tools](how-to-migrate-native-tools.md).
- Migrate data to Azure DocumentDB using the [MongoMigrationwebBasedUtility](https://github.com/AzureCosmosDB/MongoMigrationwebBasedUtility).
