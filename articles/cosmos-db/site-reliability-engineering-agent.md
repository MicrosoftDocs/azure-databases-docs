---
title: Use Azure SRE Agent (Preview)
description: Learn how to use Azure site reliability engineering (SRE) agent with Azure Cosmos DB for NoSQL. Get automated diagnostics, AI-driven recommendations, and better application reliability.
author: iriaosara
ms.author: iriaosara
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: how-to
ms.date: 11/03/2025
ms.custom:
  - references_regions
ai-usage: ai-generated
appliesto:
  - ✅ NoSQL
---

# Use Azure site reliability engineering (SRE) agent with Azure Cosmos DB for NoSQL (preview)

[!INCLUDE [Note - Preview](includes/note-preview.md)]

Azure Cosmos DB SRE Agent is an AI-powered diagnostic tool that helps you use Azure SRE Agent to simplify troubleshooting and improve reliability of applications running on Azure Cosmos DB. This intelligent assistant helps developers and operations teams quickly identify, diagnose, and resolve issues before they affect application performance.

## What is Azure SRE Agent?

The Azure SRE Agent for Azure Cosmos DB combines the power of AI with deep understanding of Azure Cosmos DB operations. This combination provides intelligent troubleshooting, proactive insights, and contextual recommendations based on your specific Azure Cosmos DB configuration and usage patterns.

### Benefits of Azure SRE Agent

The Azure Cosmos DB SRE Agent addresses common operational challenges by providing the following benefits:

- **Automated diagnostics** for both SDK and server-side issues

- **Actionable insights** surfaced from diagnostic logs

- **Reduced manual troubleshooting time** through AI-driven recommendations

- **Best practices recommendations** aligned with the Azure Well-Architected Framework to ensure reliability and resiliency

- **Proactive monitoring** and intelligent guidance that minimizes downtime and accelerates root cause analysis

### Use cases for Azure SRE Agent

The Azure SRE Agent can help you with various Azure Cosmos DB scenarios:

- **Performance troubleshooting** - High latency issues, throughput optimization, and indexing problems

- **Connectivity and configuration** - Connection issues, authentication errors, and regional failover scenarios

- **Best practices guidance** - Schema design optimization, SDK configuration, and monitoring setup

## Prerequisites

- An Azure subscription

  - If you don't have an Azure subscription, create a [free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) before you begin.

- An Azure Cosmos DB for NoSQL account

  - **Contributor** or **Owner** access to the Azure Cosmos DB account
  
  - Permissions for `roleAssignments/write` and `Microsoft.ManagedIdentity/userAssignedIdentities/write`

## Set up Azure SRE Agent

Follow these steps to configure Azure SRE Agent with your Azure Cosmos DB resources.

1. Create an Azure SRE Agent in your Azure subscription that contains your Azure Cosmos DB resources. For detailed instructions, see [Azure SRE Agent usage guide](https://aka.ms/sreagent/docs).

1. Add your Azure Cosmos DB resources to the Azure SRE Agent.
    
    :::image type="content" source="media/site-reliability-engineering-agent/add-agent.png" lightbox="media/site-reliability-engineering-agent/add-agent.png" alt-text="Screenshot showing how to add resources to the Azure Cosmos DB SRE agent.":::

1. Enable the Preview Upgrade Channel to access the Azure Cosmos DB SRE Agent.
    
    :::image type="content" source="media/site-reliability-engineering-agent/enable-preview.png" lightbox="media/site-reliability-engineering-agent/enable-preview.png" alt-text="Screenshot showing how to enable preview for the Azure Cosmos DB SRE agent.":::

1. Start using the agent by initiating a conversation about your Azure Cosmos DB diagnostics needs.

## Limitations of Azure SRE Agent

Here are limitations and considerations when using Azure SRE Agent:

- The preview is limited to Sweden Central, East US 2, and Australia East regions

- Conversations are supported in English language only

- Billing for Azure SRE Agent is based on Azure Agent Units (AAU). AAUs standardize measuring agentic processing across all prebuilt Azure agents. For more information, see [Azure SRE Agent pricing](https://azure.microsoft.com/pricing/details/sre-agent/)

## Related content

- [Azure SRE Agent overview](/azure/sre-agent)
- [Azure Cosmos DB monitoring best practices](monitor-resource-logs.md)
- [Azure Cosmos DB performance troubleshooting guide](troubleshoot-dotnet-sdk.md)
- [Azure Cosmos DB SDK configuration](quickstart-dotnet.md)