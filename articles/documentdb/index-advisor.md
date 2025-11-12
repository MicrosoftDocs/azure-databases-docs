---
title: Tune Query Performance with Index Advisor (Preview)
titleSuffix: Azure DocumentDB
description: Learn how to use Index Advisor in Azure DocumentDB to optimize query performance through automated index recommendations and real-time analysis.
author: khelanmodi
ms.author: khelanmodi
ms.topic: feature-guide
ms.date: 11/07/2025
ai-usage: ai-assisted
---

# Tune query performance with Index Advisor in Azure DocumentDB (preview)

Index Advisor is a built-in performance tuning assistant for Azure DocumentDB that helps you diagnose slow queries, understand query execution behavior, and implement optimized index strategies. Index Advisor analyzes your query structure along with collection and index statistics. Index Advisor then generates clear, data-driven recommendations with readable explanations that describe why a specific index would help improve performance.

## Benefits of Index Advisor

Here are some benefits of using Index Advisor.

- **Identify performance bottlenecks** and inefficient queries.
- **Receive actionable index recommendations** prioritized by performance effect.
- **Understand why an index matters** through clear, plain-English explanations.
- **Apply index recommendations instantly** within the extension.
- **Compare before-and-after performance** automatically once the index is created.

## Use cases for Index Advisor

Index Advisor supports various query patterns and optimization scenarios to help improve your database performance.

| Scenario | Description |
| --- | --- |
| **Equality / Range Query** | Handles simple equality or range filters (for example, `field = value` or `field > value`). |
| **Compound Filter / Covered Query / Lookup Join** | Analyzes queries that involve multiple filter conditions or joins that can be optimized with compound or covered indexes for Find Queries. |
| **Composite Index** | Suggests multi-field (composite) indexes to support complex Find/ sort queries |
| **Sort Only** | Identifies when a sort operation can be improved or covered by an index. |
| **Filter + Sort / Index Pushdown** | Recommends index structures that allow filtering and sorting to be handled efficiently within the index layer, reducing document scans. |
| **Existing index coverage** | Supported for Find queries; if an index already exists, no new index is suggested. |

If your query scenario falls outside these patterns, contact the [Azure DocumentDB team](https://nam.dcv.ms/sY4hGfyA2n) for assistance with your specific use case.

## Prerequisites

[!INCLUDE[Prerequisite - Existing cluster](includes/prerequisite-existing-cluster.md)]

- Visual Studio Code

  - [DocumentDB](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-documentdb) extension installed
  
  - [GitHub Copilot](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot) extension installed with a valid GitHub Copilot subscription

## Connect to your Azure DocumentDB cluster

Connect to your Azure DocumentDB cluster within the Visual Studio Code extension.

1. Open the DocumentDB for Visual Studio Code extension from the Activity Bar.

1. Select **Add Connection** to create a new cluster connection.

1. Choose your authentication method and provide the required connection details.

1. Test the connection to ensure it's working properly.

1. Expand your cluster to view available databases and collections.

## Open a query for analysis

Begin performance analysis with Index Advisor by opening a query in the DocumentDB extension.

1. Open a **Find**, **Aggregate**, or **Count** query in the extension.

1. Go to the **Query Insights** tab.

1. **Run** your query. The panel displays key performance indicators such as execution time, documents returned, keys examined, and documents examined. Index Advisor collects and analyzes the query execution plan and statistics from the connected cluster (Standard Mode) or from preloaded data (Preload Mode). A language model (GitHub Copilot) examines the **sanitized** plan and statistics to recommend optimal indexes.

    > [!IMPORTANT]
    > All literal query values (for example, emails, numbers, or text) are replaced with `<value>` placeholders before being sent for analysis.
    >
    > Here's an example of the sanitization:
    >
    > - Unsanitized query that isn't sent
    >
    >   ```json
    >   {
    >     "filter": {
    >       "email": "john.doe@example.com",
    >       "age": { "$gt": 25 }
    >     }
    >    }
    >   ```
    >
    > - Sanitized query that is sent
    >
    >   ```json
    >   {
    >     "filter": {
    >       "email": "<value>",
    >       "age": { "$gt": "<value>" }
    >     }
    >    }
    >   ```
    >

1. **Apply** a recommendation directly; the extension creates the index and reruns the query to update performance metrics.

1. Review the **Query Statistics** and **Execution Plan** summaries.

    :::image type="content" source="media/index-advisor/query-statistics.png" lightbox="media/index-advisor/query-statistics.png" alt-text="Screenshot of the query statistics section with information including the execution time, number of documents returned, and keys/documents examined.":::

1. Explore the **Optimization Opportunities** list. Each recommendation includes a human-readable explanation and a suggested index definition.

    :::image type="content" source="media/index-advisor/optimization-opportunities.png" lightbox="media/index-advisor/optimization-opportunities.png" alt-text="Screenshot of the optimization opportunities with a list of recommendations for the current query.":::

1. Select  **Apply** to create the recommended index. Index creation runs asynchronously in the background. Once complete, the panel automatically refreshes with updated results. After index creation, Index Advisor **re-runs the analysis** and updates metrics so you can compare performance improvements.

## Limitations of Index Advisor

Here are limitations of the Index Advisor feature.

- **Regional availability:** Index Advisor is currently available only in the **United States** and **Canada** regions.
- **Index management:** The Index Advisor only recommends creating new indexes; it doesn't recommend dropping or hiding existing indexes at this time.
- **Scenario coverage:** Only the supported scenarios listed earlier are optimized in this release. For other query types, contact the [Azure DocumentDB team](https://nam.dcv.ms/sY4hGfyA2n) or check out [Indexing Best Practices](./how-to-create-indexes.md).
- **Data sensitivity:** Treat database and collection names as metadata, but still review internal data classification policies.

## Best practices when using Index Advisor

Here are best practices for using the Index Advisor feature.

- Follow your organization’s **data governance policies** when exporting or sharing statistics.
- Review index recommendations before applying them to ensure they align with your workload and cost requirements.
- Avoid manually dropping indexes without reviewing dependencies or consulting with the [Azure DocumentDB team](https://nam.dcv.ms/sY4hGfyA2n).
- If your query patterns aren't supported, check out [Indexing Best Practices](./how-to-create-indexes.md) for guidance and support.

## Considerations for Index Advisor

Index Advisor is built to help you optimize queries while protecting your data privacy at every step.

This list shows data collected by the extension:

- **Query execution plans** – structural information and performance metrics.
- **Collection statistics** – document count, data and index sizes, and index counts.
- **Index details** – index names, key patterns, and usage metrics.
- **Cluster metadata** – limited information such as Azure hosting status and API type.

### Compliance and data protection

To ensure compliance and data protection, the system implements the following safeguards before sending any information for analysis:

- Replacing all **literal values** in queries and execution plans with `<value>`.
- **Retaining** field names and query operators (such as `email`, `$gt`, `$in`) to preserve context.
- **Fully sanitizing** execution plans to ensure that no sensitive or personal data remains.
- Keeping **performance metrics** (such as `nReturned` or `executionTimeMillis`) because they contain no literal values from your data.
- Transmitting only the **sanitized structure**, statistics, and metadata required for analysis—never sample documents or raw values.
- Subjecting any future feature that requires unsanitized data to full Microsoft privacy and compliance review.

Index Advisor analyzes only query structure and performance characteristics, **never your actual data**.

## Related content

- [Sharding in Azure DocumentDB](partitioning.md)
- [Connect to Azure DocumentDB using MongoDB shell](how-to-connect-mongo-shell.md)
