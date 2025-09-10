---
title: AI Knowledge Graphs
description: Create AI knowledge graphs using Azure Cosmos DB for NoSQL to allow AI apps to manage and query complex data relationships.
author: jcodella
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: how-to
ms.date: 09/08/2025
ms.update-cycle: 180-days
ms.author: jacodel
ms.collection:
  - ce-skilling-ai-copilot
appliesto:
  - ✅ NoSQL
---

# Create AI knowledge graphs using Azure Cosmos DB with retrieval-augmented generation (RAG)

[CosmosAIGraph](https://aka.ms/cosmosaigraph) is an innovative solution that applies the power of Azure Cosmos DB to create AI-powered knowledge graphs. This technology integrates advanced graph database capabilities with AI to provide a robust platform for managing and querying complex data relationships. By utilizing Cosmos DB's scalability and performance in both document and vector form, CosmosAIGraph enables the creation of sophisticated data models that can answer various data questions and uncover hidden relationships and concepts in semi-structured data.

## Questions knowledge graphs help to answer

**Complex relationship queries**
- *Question*: "What are the direct and indirect connections between Person A and Person B within a social network?"
- *Explanation*: Graph RAG can traverse the graph to find all paths and relationships between two nodes, providing a detailed map of connections, which is difficult for vector search because it doesn't have authoritative/curated view of relationships between entities.

**Hierarchical data queries**
- *Question*: "What is the organizational hierarchy from the CEO down to the entry-level employees in this company?"
- *Explanation*: Graph RAG can efficiently navigate hierarchical structures, identifying parent-child relationships and levels within the hierarchy, whereas vector search is more suited for finding similar items rather than understanding hierarchical relationships.

**Contextual path queries**
- *Question*: "What are the steps involved in the supply chain from raw material procurement to the final product delivery?"
- *Explanation*: Graph RAG can follow the specific paths and dependencies within a supply chain graph, providing a step-by-step breakdown. Vector search, while excellent at finding similar items, lacks the capability to follow and understand the sequence of steps in a process.

When it comes to [RAG](rag.md), combining *knowledge graphs* and *vector search* can offer powerful capabilities that expand the range of questions that can be answered about the data. Graph RAG enhances the retrieval process by using the structured relationships within a graph, making it ideal for applications that require contextual understanding and complex querying, such as knowledge management systems and personalized content delivery.

On the other hand, vector search excels in handling unstructured data and finding similarities based on vector embeddings, which is useful for tasks like image and document retrieval. Together, these technologies can provide a comprehensive solution that combines the strengths of both structured and unstructured data processing.

:::image type="content" source="../media/gen-ai/cosmos-ai-graph/cosmos-ai-graph-architecture.png" alt-text="Diagram of the Cosmos AI Graph infrastructure, components, and flow." lightbox="../media/gen-ai/cosmos-ai-graph/cosmos-ai-graph-architecture.png":::

## OmniRAG

CosmosAIGraph features *OmniRAG*, a versatile approach to data retrieval that dynamically selects the most suitable method—whether it's database queries, vector matching, or knowledge graph traversal—to answer user queries effectively and with utmost accuracy, as it likely gathers more context, and more authoritative context, than any one of these sources could on its own.

The key to this dynamic selection is the user intent, determined from the user question using simple utterance analysis or AI. This ensures that each query is addressed using the optimal technique, enhancing accuracy and efficiency. For instance, a user query about hierarchical relationships would utilize graph traversal, while a query about similar documents would employ vector search, all within a unified framework provided by CosmosAIGraph.

Moreover, with the help of orchestration within the RAG process, more than one source could be used to collect the context for AI. For example, the graph could be consulted with first and then for each of the entities found the actual database records could be pulled as well, and if no results were found, vector search would likely return closely matching results. This holistic approach maximizes the strengths of each retrieval method, delivering comprehensive and contextually relevant answers.

### Example user questions and strategy used

| User questions | Strategy |
| --- | --- |
| What is the Python Flask Library? | DB RAG |
| What are its dependencies? | Graph Rag |
| What is the Python Flask Library? | Database RAG |
| What are its dependencies? | Graph RAG |
| Who is the author? | DB RAG |
| What other libraries did they write? | Graph RAG |
| Display a graph of all their libraries and dependencies | Graph RAG |

## Get started

CosmosAIGraph applies Azure Cosmos DB to create AI-powered graphs and knowledge graphs, enabling sophisticated data models for applications like recommendation systems and fraud detection. It combines traditional database, vector database, and graph database capabilities with AI to manage and query complex data relationships efficiently. To get started, see the [CosmosAIGraph repo](https://aka.ms/cosmosaigraph).

## Related content

- [CosmosAIGraph on Azure Cosmos DB TV - YouTube](https://www.youtube.com/watch?v=0alvRmEgIpQ)
- [Vector search in Azure Cosmos DB](vector-search-overview.md)
- [What are tokens?](tokens.md)
- [Vector embeddings in Azure Cosmos DB](vector-embeddings.md)
- [Retrieval-augmented generation (RAG) in Azure Cosmos DB](rag.md)

## Next step

> [!div class="nextstepaction"]
> [Use the Azure Cosmos DB lifetime free tier](../free-tier.md)
