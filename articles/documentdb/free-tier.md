---
title: Free tier
description: Free tier on Azure DocumentDB.
author: suvishodcitus
ms.author: suvishod
ms.topic: how-to
ms.date: 11/08/2023
ms.custom:
  - references_regions
# CustomerIntent: As a database owner, I want customers/developers to be able to evaluate the service for free.
---

# Build applications for free with Azure DocumentDB Free Tier

Azure DocumentDB now introduces a new SKU, the "Free Tier," enabling users to explore the platform without any financial commitments. The free tier lasts for the lifetime of your account, boasting command and feature parity with a regular Azure DocumentDB account.

It makes it easy for you to get started, develop, test your applications, or even run small production workloads for free. With Free Tier, you get a dedicated MongoDB cluster with 32-GB storage, perfect for all of your learning & evaluation needs. Users can provision a single free database server per subscription. This feature is currently available in limited set of regions only.


## Get started

Follow this document to [create a new Azure DocumentDB](quickstart-portal.md) cluster and just select 'Free Tier' checkbox. 
Alternatively, you can also use [Bicep template](quickstart-bicep.md) to provision the resource.

:::image type="content" source="media/how-to-scale-cluster/provision-free-tier.jpg" alt-text="Screenshot of the free tier provisioning.":::

## Upgrade to higher tiers

As your application grows, and the need for more powerful machines arises, you can effortlessly transition to any of our available paid tiers with just a click. Just select the cluster tier of your choice from the Scale blade, 
specify your storage requirements, and you're all set. Rest assured, your data, connection string, and network rules remain intact throughout the upgrade process.

:::image type="content" source="media/how-to-scale-cluster/upgrade-free-tier.jpg" alt-text="Screenshot of the free tier scaling.":::

## Supported Regions
Free Tier is now available in an expanded list of regions, making it easier for developers worldwide to get started with their projects.

### Why this matters:

* **Proximity**: Deploy closer to your users or applications for better performance.
* **Compliance**: Choose regions that match your data regulatory needs.

You can now create Free Tier clusters in the following Azure regions:

* **Americas**: Brazil South, Canada Central, Central US, East US, West US, West US 2
* **Europe**: France Central, Germany North, North Europe, Norway East, Switzerland North
* **Asia Pacific**: Australia Central 2, Australia East, Central India, South India, East Asia, Japan East, Japan West

## Benefits

* Zero cost
* Effortless onboarding
* Generous storage (32-GB)
* Dedicated resources for consistent performance
* Seamless upgrade path


## Restrictions

* For a given subscription, only one free tier account is permissible.
* High availability, Microsoft Entra ID (formerly known as Azure Active Directory), Backup / Restore, HNSW & DiskANN vector indexes, and Diagnostic Logging aren't supported.
* Free tier clusters are paused after 60 days of inactivity.
* Transition from a paid tier account to a free tier accounts isn't supported.

## Next steps

Now that you’ve explored the free tier of Azure DocumentDB, it’s time to dive into how to assess your migration and successfully move your MongoDB workload to Azure.

> [!div class="nextstepaction"]
> [Migration options for Azure DocumentDB](migration-options.md)
