---
title: Azure Cosmos DB Agent Kit
titleSuffix: Azure Cosmos DB for NoSQL
description: Learn how the Azure Cosmos DB Agent Kit extends AI coding assistants like GitHub Copilot, Claude Code, and Gemini CLI with expert-level Azure Cosmos DB best practices. Install with one command and get production-ready guidance instantly.
author: sajeetharan
ms.author: sasinnat 
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: feature-guide
ms.date: 01/29/2026
ms.collection:
  - ce-skilling-ai-copilot
ai-usage: ai-assisted
appliesto:
  - ✅ NoSQL
---

# Azure Cosmos DB Agent Kit for AI coding assistants

The Azure Cosmos DB Agent Kit ([AzureCosmosDB/cosmosdb-agent-kit](https://github.com/AzureCosmosDB/cosmosdb-agent-kit)) is an open-source collection of skills that extends AI coding assistants with expert-level Azure Cosmos DB best practices. Built on the [Agent Skills](https://agentskills.io/) format, the kit works seamlessly with **GitHub Copilot**, **Claude Code**, **Gemini CLI**, and other Agent Skills-compatible tools.

Install with one command, and your AI pair programmer instantly knows production-ready Azure Cosmos DB patterns, optimization techniques, and best practices.

## The challenge

When building applications with Azure Cosmos DB, developers often face critical decisions:

- **Partition key selection**: Which key ensures high cardinality and supports query patterns?
- **Query optimization**: Why is this query consuming so many RUs?
- **Data modeling**: Should data be embedded or referenced?
- **Hot partition prevention**: How to avoid bottlenecks in production?

Poor decisions in these areas can lead to performance issues, scalability problems, or unexpectedly high costs. The Agent Kit solves this by teaching your AI coding assistant the answers.

## What's included

The Agent Kit includes **45+ curated rules** across **eight categories**, each prioritized by real-world impact:

| Category | Priority | Description |
|----------|----------|-------------|
| **Data Modeling** | Critical | Best practices for structuring documents and relationships |
| **Partition Key Design** | Critical | Guidelines for choosing effective partition keys |
| **Query Optimization** | High | Techniques to reduce RU consumption and improve performance |
| **SDK Best Practices** | High | Proper client initialization, retry logic, and error handling |
| **Indexing Strategies** | Medium-High | Efficient index policies for your workloads |
| **Throughput & Scaling** | Medium | Autoscale, provisioned throughput, and capacity planning |
| **Global Distribution** | Medium | Multi-region writes and consistency level selection |
| **Monitoring & Diagnostics** | Low-Medium | Logging, metrics, and troubleshooting patterns |

## Prerequisites

Before installing the Azure Cosmos DB Agent Kit:

- An AI coding assistant that supports Agent Skills:
  - **GitHub Copilot** (Visual Studio Code, Visual Studio, JetBrains IDEs)
  - **Claude Code**
  - **Gemini CLI**
  - Any other Agent Skills-compatible tool
- **Node.js** with npm/npx installed for the installation command

## Installation

Install the Agent Kit with a single command:

```bash
npx add-skill AzureCosmosDB/cosmosdb-agent-kit
```

That's it. The skill is now installed in your development environment and activates automatically when you work on Azure Cosmos DB-related tasks.

## Usage

Once installed, the skill activates automatically when relevant tasks are detected. Simply ask your AI agent naturally:

```text
Review my Cosmos DB data model for performance issues
```

```text
Help me choose a partition key for my e-commerce orders collection
```

```text
Optimize this query that's consuming too many RUs
```

```text
What's wrong with my Cosmos DB connection code?
```

### Example: Code review

Consider this initial code for a product catalog API:

```javascript
// cosmosService.js
const { CosmosClient } = require('@azure/cosmos');

const endpoint = process.env.COSMOS_ENDPOINT;
const key = process.env.COSMOS_KEY;

// Creating new client on every request
async function getProducts(category) {
    const client = new CosmosClient({ endpoint, key });
    const database = client.database('ProductCatalog');
    const container = database.container('Products');

    // Using SELECT * pulls all properties
    const query = `SELECT * FROM c WHERE c.category = '${category}'`;
    const { resources } = await container.items.query(query).fetchAll();
    
    return resources;
}

module.exports = { getProducts };
```

When you prompt "Review this Azure Cosmos DB service code for best practices issues", the Agent Kit teaches your AI assistant to identify:

1. **SDK Anti-pattern**: Creating a new `CosmosClient` on every request wastes resources
2. **Query Optimization**: `SELECT *` pulls unnecessary data, consuming extra RUs
3. **Security Risk**: String concatenation in queries can lead to injection attacks
4. **Missing Error Handling**: No retry logic for rate limiting (429 errors)

The AI assistant provides improved code:

```javascript
// cosmosService.js
const { CosmosClient } = require('@azure/cosmos');

const endpoint = process.env.COSMOS_ENDPOINT;
const key = process.env.COSMOS_KEY;

// Singleton client instance - reuse across requests
const client = new CosmosClient({
    endpoint,
    key,
    connectionPolicy: {
        retryOptions: {
            maxRetryAttemptCount: 5,
            maxWaitTimeInSeconds: 30
        }
    }
});

const database = client.database('ProductCatalog');
const container = database.container('Products');

async function getProducts(category) {
    // Project only needed fields to reduce RU consumption
    const query = {
        query: `SELECT c.id, c.name, c.price, c.description, c.imageUrl 
                FROM c 
                WHERE c.category = @category`,
        parameters: [{ name: '@category', value: category }]
    };

    try {
        const { resources, requestCharge } = await container.items
            .query(query)
            .fetchAll();

        // Log RU consumption for monitoring
        console.log(`Query consumed ${requestCharge} RUs`);

        return resources;
    } catch (error) {
        if (error.code === 429) {
            // Handle rate limiting gracefully
            console.warn('Rate limited, retry after:', error.retryAfterInMs);
            throw new Error('Service temporarily unavailable');
        }
        throw error;
    }
}

module.exports = { getProducts };
```

## Skill structure

Each skill in the Agent Kit contains:

```
skills/cosmosdb-best-practices/
├── SKILL.md          # Triggers activation, describes capabilities
├── AGENTS.md         # Compiled rules (what agents read)
├── rules/            # Individual rule files
│   ├── data-modeling.md
│   ├── partition-keys.md
│   ├── query-optimization.md
│   └── ...
└── metadata.json     # Version and metadata
```

When you work on Azure Cosmos DB code, the AI agent automatically loads the relevant rules and applies them to your context.

## Compatibility

The Azure Cosmos DB Agent Kit works with:

- **GitHub Copilot** - Visual Studio Code, Visual Studio, JetBrains IDEs
- **Claude Code** - Anthropic's coding assistant
- **Gemini CLI** - Google's command-line AI assistant
- **Any Agent Skills-compatible tool**

## Contributing

Have you discovered a best practice the kit doesn't cover? Share it with the community:

- A query pattern that dramatically reduced RUs
- A data modeling approach that scaled beautifully
- An SDK configuration that improved reliability
- A monitoring technique that caught issues early

### How to contribute

1. Fork the [repository](https://github.com/AzureCosmosDB/cosmosdb-agent-kit)
2. Add your rule to the appropriate category in `/skills/cosmosdb-best-practices/rules/`
3. Submit a pull request with a description of the scenario and impact
4. Help thousands of developers write better Azure Cosmos DB code

For detailed contribution guidelines, see [CONTRIBUTING.md](https://github.com/AzureCosmosDB/cosmosdb-agent-kit/blob/main/CONTRIBUTING.md).

## Considerations

- **Read-only guidance**: The Agent Kit provides code suggestions and best practices only; it doesn't execute operations on your database
- **Skill activation**: Skills activate automatically based on context; no manual configuration needed
- **Local installation**: Skills are installed locally in your development environment
- **Regular updates**: Keep the skill updated to get the latest best practices

## Related content

- [Azure Cosmos DB best practices for .NET](../best-practice-dotnet.md)
- [Azure Cosmos DB best practices for Java](../best-practice-java.md)
- [Azure Cosmos DB best practices for Python](../best-practice-python.md)
- [Azure Cosmos DB best practices for JavaScript](../best-practices-javascript.md)
- [Model context protocol (MCP) toolkit](model-context-protocol-toolkit.md)
- [Azure Cosmos DB Samples Gallery](https://aka.ms/AzureCosmosDB/Gallery)
