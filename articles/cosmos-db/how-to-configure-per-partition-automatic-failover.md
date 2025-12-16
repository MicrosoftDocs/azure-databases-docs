---
title: Configure and use Per Partition Automatic Failover for Azure Cosmos DB
description: Learn how to enable and use Per Partition Automatic Failover for Azure Cosmos DB
author: sushantrane
ms.author: srane
ms.service: azure-cosmos-db
ms.topic: how-to
ms.date: 05/14/2025
ms.custom:
  - build-2025
appliesto:
  - ✅ NoSQL
---

# How to onboard and adopt Per-Partition Automatic Failover (PPAF) for Azure Cosmos DB

This article explains how to configure Per Partition Automatic Failover on your Azure Cosmos DB account.

> [!IMPORTANT]
> Per Partition Automatic Failover is in public preview.
> This feature is provided without a service level agreement.
> For more information, see [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).


**Per-Partition Automatic Failover (PPAF)**  is a new Azure Cosmos DB feature (currently in **Public Preview**) that improves availability for single-write region accounts. Instead of failing over an entire database account during a regional outage, Cosmos DB can **automatically fail over at the *partition level***, thus minimizing downtime and faster recovery. 


## Prerequisites

Before enabling PPAF, ensure your environment meets the following **prerequisites**:

- **Multi-region account:** Single-write region account with **at least one** other **read region** configured.
- **Consistency Model:** In the current preview, **Strong**, **Session**, **Consistent Prefix**, or **Eventual** consistencies are currently supported.
- **API Type:** The account must use the **Core (SQL) API** (NoSQL API).
- **Azure Region:** The account should be in **Azure public cloud regions** (Global Azure). Accounts in sovereign clouds aren't eligible during preview.
- **SDK Version:** Your application must use a **latest supported Azure Cosmos DB SDK** that implements PPAF logic. Currently, the preview supports:
  - **.NET SDK v3** : v 3.54.0 or later
  - **Java SDK**: v 4.75.0 or later
- **In Account Restore**: In Account Restore is not supported for accounts with PPAF enabled.

## Register for Preview

To enable this feature, register for the preview feature **Per Partition Automatic Failover Preview** in your subscription. For more information, see [register for an Azure Cosmos DB preview feature](access-previews.md).

Azure Cosmos DB team reviews your request and enables the feature upon validation of prerequisites. You receive an email once the feature is enabled. You can also reach out to [cosmosdbppafpreview@microsoft.com](mailto:cosmosdbppafpreview@microsoft.com) if you have any questions about the onboarding.

## PPAF Pricing
PPAF is part of Business Critical Service Tier and is charged accordingly. For more information, see [Azure Cosmos DB pricing](https://azure.microsoft.com/pricing/details/cosmos-db/).

## Configure the application for PPAF

Configuring your application’s Cosmos DB SDK is **critical** so that it knows to handle partition-level failovers. 

- **Upgrade SDK:** Ensure your app is running the **latest SDK version** that supports PPAF (as identified in prerequisites).
- **Configure secondary region:** Ensure your Azure Cosmos DB account has at least 1 secondary region.

## Test the PPAF Setup (Simulate Fault)

With the account and client configured, it’s prudent to **test** that everything works as expected before a real outage occurs. Azure Cosmos DB provides a way to simulate partition failures in the preview for PPAF enabled accounts:

- **Chaos Simulation (Preview):** We're releasing a preview version of the fault management feature for PPAF via REST API. For ease of use, we're providing a PowerShell script for managing the fault.
  - Download the script [`EnableDisableChaosFault.ps1` at azurecosmosdb/ppaf-samples](https://github.com/AzureCosmosDB/ppaf-samples/blob/main/ppaf-fault-script/EnableDisableChaosFault.ps1).
  - Start PowerShell and login to your subscription using "az login."
  - Navigate to the folder with the PowerShell script and invoke the script with the required parameters to invoke the fault: 
    - It might take up to 15 minutes for the fault to become effective.
    - The fault gets effective on 10% of total partition for the specified collection with a maximum of 10 partition and minimum 1 Partition.
    ``` powershell
    .\EnableDisableChaosFault.ps1 -FaultType "PerPartitionAutomaticFailover" -ResourceGroup "{ResourceGroupName}" -AccountName "{DatabaseAccountName}" -DatabaseName "{DatabaseName}" -ContainerName "{CollectionName}"  -SubscriptionId "{SubscriptionId}" -Region "{PreferredWriteRegion}" -Enable
    ```

- **Application Testing:** Test critical transactions of your application during the failover.
- **Metrics:** 
  - You can verify the traffic in the Azure portal Metrics for your account. Look at metrics like **Total Requests** broken down by region. You should see write operations occurring in a secondary region during the simulation, confirming the failover worked.
  - We have introduced a new metric known as **PartitionWriteGlobalStatus** that shows the count of write partitions for a region at any given time. You can also use this metric to track how many partitions are failed over due to fault. 

- **Disable the fault:**
  - Navigate to the folder with the PowerShell script and invoke the script with the required parameters to invoke the fault: 
    - It might take up to 15 minutes for the fault to be disabled.
    ```powershell 
    .\EnableDisableChaosFault.ps1 -FaultType "PerPartitionAutomaticFailover" -ResourceGroup "{ResourceGroupName}" -AccountName "{DatabaseAccountName}" -DatabaseName "{DatabaseName}" -ContainerName "{CollectionName}"  -SubscriptionId "{SubscriptionId}" -Region "{PreferredWriteRegion}" -Disable
    ```
