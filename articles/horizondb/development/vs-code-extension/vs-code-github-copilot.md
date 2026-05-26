---
title: "Quickstart: Guide for GitHub Copilot Feature for Visual Studio Code PostgreSQL Extension"
description: Learn how to use the GitHub Copilot integration in the PostgreSQL extension for Visual Studio Code with HorizonDB.
author: jjfrost
ms.author: jfrost
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-database-postgresql
ms.subservice: extensions
ms.topic: quickstart
ms.collection:
  - ce-skilling-ai-copilot
ms.update-cycle: 180-days
ms.custom:
  - build-2026
ai-usage: ai-assisted
---

# Quickstart: Configure GitHub Copilot for PostgreSQL extension in Visual Studio Code

The PostgreSQL extension for Visual Studio Code includes GitHub Copilot integration, enhancing your database workflows with AI-assisted development. Once connected to a PostgreSQL database, Copilot accesses contextual information from your live connection. This access enables the `@pgsql` Copilot Chat participant to generate accurate, schema-aware SQL queries and insights, streamlining development and minimizing context-switching within Visual Studio Code.

The `@pgsql` participant works against any database the extension can connect to, including:

- **Azure HorizonDB** clusters.

When connected to a HorizonDB cluster, Copilot is aware of the HorizonDB-specific extensions installed on the database (such as `pgvector`, `pg_diskann`, `azure_ai`, and `age`) and can generate prompts and SQL that take advantage of them.

## Prerequisites

Before you begin, verify you have the proper tools and resources downloaded and installed.

- [Visual Studio Code](https://code.visualstudio.com/) installed on your machine.
- A PostgreSQL database installed locally, or hosted in [Create an Azure HorizonDB cluster](../../configure-maintain/quickstart-create-cluster.md).
- [PostgreSQL extension](https://marketplace.visualstudio.com/items?itemName=ms-ossdata.vscode-pgsql) installed in Visual Studio Code.
- [GitHub Copilot extension](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot).
- [GitHub Copilot Chat extension](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot-chat) installed.
- [Azure account](https://azure.microsoft.com/free/) for connecting to cloud-hosted databases (optional).

## Install GitHub Copilot and GitHub Copilot Chat extensions

If you don't already have the GitHub Copilot extension installed in Visual Studio Code:

1. Select the **Extensions** icon in Visual Studio Code, search for **GitHub Copilot**, and select **Install**.
1. The GitHub Copilot Chat extension is automatically installed along with GitHub Copilot.

## Sign in to GitHub in Visual Studio Code

1. Make sure you have a GitHub account and an active GitHub Copilot subscription:
   - [Create a GitHub account](https://github.com)
   - [Enable a GitHub Copilot subscription](https://github.com/settings/copilot)
1. In Visual Studio Code, select the **Account** icon and choose **Sign in with GitHub** to use GitHub Copilot.

## Get started with GitHub Copilot

Follow the steps to begin using GitHub Copilot with the PostgreSQL Visual Studio Code extension.

1. Right-click on a PostgreSQL database in the Object Explorer and select **Chat with this database**. This works for any connection - local PostgreSQL or Azure HorizonDB.
1. If prompted, select **Allow** to enable GitHub Copilot to access the database connection context.
1. When the Copilot chat interface opens, start asking questions by using the `@pgsql` prefix to specify that you want to interact with the PostgreSQL database.

Try a prompt like:

```text
@pgsql tell me about the tables in the HR schema
```

Copilot responds with a detailed description of your schema's tables.

<a id="connecting-to-the-right-horizondb-endpoint"></a>

### Connect to the right HorizonDB endpoint

Because an Azure HorizonDB cluster exposes two endpoints, the connection you start chatting on determines which endpoint Copilot's generated SQL runs against:

- **Read/write endpoint** - Use this connection when you want Copilot to draft, modify, or execute statements that change data or schema, or that must read the latest committed state.
- **Reader endpoint** - Use this connection when you want Copilot to draft and run **read-only** queries that benefit from load-balanced scale-out across HA replicas (for example, exploratory analytics or reporting prompts).

If Copilot generates a write statement while you're connected to the reader endpoint, switch the active connection to the read/write endpoint before approving execution.

<a id="using-read-and-write-capabilities"></a>

## Use read and write capabilities

The GitHub Copilot integration for the PostgreSQL extension in Visual Studio Code supports both read and write operations. You can query data, modify schemas, and update records directly from the editor with AI-powered suggestions that take the live connection context into account.

> [!NOTE]  
> The GitHub Copilot Chat integration for PostgreSQL can make changes to your database. Use this feature with caution, especially in staging and production environments. Always review the generated SQL code before executing it, and consider testing it in a safe environment first. On Azure HorizonDB, also ensure write operations target the **read/write endpoint** - the reader endpoint is read-only.

Try a more advanced prompt:

```text
@pgsql convert the hr.employees table to use a JSONB column for the address field
```

Copilot might respond with SQL suggestions and ask permission to make changes.

To approve execution:

```text
@pgsql Yes, please make the JSONB column for me
```

Then Copilot asks for confirmation:

```text
@pgsql Yes, I confirm
```

<a id="using-context-menu-options"></a>

## Use context menu options

You can select SQL code in the editor and right-click to access GitHub Copilot context menu options like **Explain Query**, **Rewrite Query**, or **Analyze Query Performance**. On HorizonDB, the explanations and rewrite suggestions also account for HorizonDB-specific indexes (such as `pg_diskann` vector indexes) when they're present.

## Other ideas and prompt recipes

The following sections show concept prompts you can try or modify to match your database context and development environment.

### Query optimization

Use these prompts to guide Copilot in addressing specific query optimization challenges.

```text
I'm working on optimizing my database for high-concurrency workloads. The table is called transactions with millions of records, and I'm experiencing deadlocks under a heavy load. Help me optimize my table schema and queries.

I need help writing a query. The data is stored in the orders table, which uses the columns customer_id, order_date, and total_price. I also need to include a rolling 3-month average of customer spending using a window function.

I'm getting this error: 'ERROR: column "orders.total_price" must appear in the GROUP BY clause or be used in an aggregate function.'
```

### Performance optimization

Use these prompts to guide Copilot in addressing specific performance optimization challenges.

```text
Provide the Explain Plan for my most recent query, and please explain each step.

Can you run some performance metrics on my database and tell me how it performs?

My orders table has 10 million records, and queries on customer_id and order_date are slow. How can I optimize indexing, partitioning, and schema design for performance?
```

### App development

Use these prompts to guide Copilot in addressing app development challenges.

```text
Generate a FastAPI endpoint to fetch orders from the ecom.orders table with pagination.

Generate an ETL pipeline script to clean and normalize the customer table data.

Generate a FastAPI project with my database using SQLAlchemy.
```

### AI workloads on Azure HorizonDB

When you're connected to a HorizonDB cluster, you can use Copilot to build on HorizonDB's AI capabilities - `pgvector`, `pg_diskann` (with Advanced Filtering), and the `azure_ai` AI Functions backed by [AI Model Management (Gated Preview)](../../ai/ai-model-management.md) or your own Microsoft Foundry deployments.

```text
@pgsql Create a products table with a description column and a vector(1536) embedding column. Then write a query that populates the embedding column for any rows where it's NULL using azure_openai.create_embeddings with the default-embedding managed model.

@pgsql Build a pg_diskann index on the products.embedding column using vector_cosine_ops, then write a similarity search that finds the top 10 products with average_rating > 4.5 and price between 100 and 200 - using DiskANN Advanced Filtering so the WHERE clause is evaluated during the vector search.

@pgsql Use azure_ai.extract() to pull product and sentiment out of the review_text column of the product_reviews table, and azure_ai.is_true() to flag reviews that mention shipping issues.

@pgsql I have a Microsoft Foundry deployment of gpt-5 in my own subscription. Show me how to register it with model_registry.model_add as 'gpt-5-byom' and then call azure_ai.generate() with that alias to rewrite the comment_text column of user_comments to be more polite.
```

### Read scale-out

When connected to the **reader endpoint** of a HorizonDB cluster, you can ask Copilot to draft read-only workloads that take advantage of load-balanced HA replicas:

```text
@pgsql Generate a reporting query against the orders and customers tables that aggregates monthly revenue by region and customer segment. Make sure the query is read-only so it's safe to run against the HorizonDB reader endpoint.
```

## Clean up

To ensure a smooth experience, clean up any temporary resources or configurations you created during this quickstart. For example:

- Disconnect from the PostgreSQL database in Visual Studio Code.
- Remove any test databases, tables, or indexes (including any `pg_diskann` indexes) you created during the session.
- Close any open connections to avoid unnecessary resource usage.

## Feedback and support

For bugs, feature requests, and issues, use the built-in feedback tool in Visual Studio Code. You can complete this feedback via the Visual Studio Code Help menu or the PGSQL command palette.

- **Help menu**
  - Go to **Help > Report Issue**
- **Command palette**
  - Open the Command Palette with `Ctrl + Shift + P` and run: `PGSQL: Report Issue`

## Related content

- [What is the PostgreSQL extension for Visual Studio Code?](vs-code-overview.md)
- [Quickstart: PostgreSQL Extension for Visual Studio Code in Azure HorizonDB](vs-code-connect.md)
- [PostgreSQL extension for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-ossdata.vscode-pgsql)
