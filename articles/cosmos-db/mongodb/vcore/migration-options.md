---
title: Options to migrate data from MongoDB
titleSuffix: vCore-based Azure Cosmos DB for MongoDB
description: Review various options to migrate your data from other MongoDB sources to vCore-based Azure Cosmos DB for MongoDB.
author: sandeep-nair
ms.author: sandnair
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: upgrade-and-migration-article
ms.date: 06/11/2025
# CustomerIntent: As a MongoDB user, I want to understand the various options available to migrate my data to vCore-based Azure Cosmos DB for MongoDB, so that I can make an informed decision about which option is best for my use case.
---

# What are the options to migrate data from MongoDB to vCore-based Azure Cosmos DB for MongoDB?

This document describes the various options to lift and shift your MongoDB workloads to vCore-based Azure Cosmos DB for MongoDB offering.

Migrations can be done in two ways:

- Offline Migration: A snapshot based bulk copy from source to target. New data added/updated/deleted on the source after the snapshot isn't copied to the target. The application downtime required depends on the time taken for the bulk copy activity to complete.

- Online Migration: Apart from the bulk data copy activity done in the offline migration, a change stream monitors all additions/updates/deletes. After the bulk data copy is completed, the data in the change stream is copied to the target. This process ensures that all updates made during the migration process are also transferred to the target. The application downtime required is minimal.

## Premigration Assessment

Use the [MongoDB migration extension for Azure Data Studio](/azure-data-studio/extensions/database-migration-for-mongo-extension) to perform a compatibility assessment. The purpose of this stage is to identify any incompatibilities or warnings that exist in the current MongoDB solution. You should resolve the issues found in the assessment results before moving on with the migration process.

> [!TIP]
> We recommend you review the [supported features and syntax](./compatibility.md) in detail and perform a proof-of-concept prior to the actual migration.

## Migration

The tools discussed in this article assist you in migrating your MongoDB workloads from the following sources:

- MongoDB Virtual Machine
- MongoDB Atlas
- AWS DocumentDB

### Web App Utility (Online)

Streamline your migration to Azure Cosmos DB for MongoDB (vCore-based) with [MongoMigrationwebBasedUtility](https://github.com/AzureCosmosDB/MongoMigrationwebBasedUtility) a tool designed for efficiency, reliability, and ease of use. The repository offers detailed, step-by-step instructions for migrating your workloads. This tool offers a seamless experience for both online and offline data migrations. The process is user-friendly, requiring only the source and target details to be provided. It enables you to effortlessly migrate your MongoDB collections while maintaining control, security, and scalability, unlocking the full potential of Azure Cosmos DB.

Key features include:

- Supports private deployment within your virtual network for enhanced security
- Automatic resume capabilities if there's connection loss or transient errors
- User-friendly interface
- Access to C# source code on GitHub

The tool supports flexible deployment options and operates independently without dependencies on other Azure resources. Additionally, it offers scalable performance with customizable Azure Web App pricing plans. 


### Azure Data Studio (Online)

The [MongoDB migration extension for Azure Data Studio](/azure-data-studio/extensions/database-migration-for-mongo-extension) is a straightforward and zero cost tool designed to help you migrate your MongoDB workloads to the vCore-based Azure Cosmos DB for MongoDB. 

> [!IMPORTANT]
> This tool doesn't support the following scenarios:
> - Migrations where either the source or target account is enabled with Private Endpoint.
> - Migrations where the firewalls of the source or target account cannot accept a wide IP range. This tool requires you to allow connections from global Azure datacenters to both the source and target accounts. For more information, see the [global Azure IP address ranges](/azure/virtual-network/service-tags-overview#discover-service-tags-by-using-downloadable-json-files).


This tool has two phases:

- **Premigration assessment** - An evaluation of your current MongoDB data estate to determine if there are any incompatibilities.
- **Migration** - The migration operation using services managed by Azure.

With the graphical user interface, you can oversee the entire premigration assessment and migration process from start to finish, or you can choose to perform just the premigration assessment. While the migration is initiated in Azure Data Studio, it actually runs in the cloud on Azure-managed resources.

### Native MongoDB tools (Offline)

You can also use the native MongoDB tools such as *mongodump/mongorestore*, *mongoexport/mongoimport* to migrate datasets offline (without replicating live changes) to vCore-based Azure Cosmos DB for MongoDB offering.

| Scenario | MongoDB native tool |
| --- | --- |
| Move subset of database data (JSON/CSV-based) | *mongoexport/mongoimport* |
| Move whole database (BSON-based) | *mongodump/mongorestore* |

- *mongoexport/mongoimport* is the best pair of migration tools for migrating a subset of your MongoDB database.
  - *mongoexport* exports your existing data to a human-readable JSON or CSV file. *mongoexport* takes an argument specifying the subset of your existing data to export.
  - *mongoimport* opens a JSON or CSV file and inserts the content into the target database instance (vCore-based Azure Cosmos DB for MongoDB in this case.).
  - JSON and CSV aren't a compact format; you could incur excess network charges as *mongoimport* sends data to vCore-based Azure Cosmos DB for MongoDB.
- *mongodump/mongorestore* is the best pair of migration tools for migrating your entire MongoDB database. The compact BSON format makes more efficient use of network resources as the data is inserted into vCore-based Azure Cosmos DB for MongoDB.
  - *mongodump* exports your existing data as a BSON file.
  - *mongorestore* imports your BSON file dump into vCore-based Azure Cosmos DB for MongoDB.

> [!NOTE]
> The MongoDB native tools can move data only as fast as the host hardware allows.

### Data migration using Azure Databricks (Online)

In certain special cases, you may need greater control and higher throughput during migration. Using Azure Databricks for migration provides full control over the migration rate. This method is also capable of handling large datasets that are terabytes in size. The Spark migration utility functions as a job within Databricks.

[Sign up  for Azure Cosmos DB for MongoDB Spark Migration](https://forms.office.com/r/cLSRNugFSp) to gain access to the Spark Migration Tool GitHub repository. The repository offers detailed, step-by-step instructions for migrating your workloads from various Mongo sources to vCore-based Azure Cosmos DB for MongoDB.


## Related content

- Migrate data to vCore-based Azure Cosmos DB for MongoDB using [native MongoDB tools](how-to-migrate-native-tools.md).
- Migrate data to vCore-based Azure Cosmos DB for MongoDB using the [MongoDB migration extension for Azure Data Studio](/azure-data-studio/extensions/database-migration-for-mongo-extension).
