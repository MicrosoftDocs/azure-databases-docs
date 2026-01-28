---
title: High-Dimensional Vector Embeddings
titleSuffix: Azure Cosmos DB
description: Learn about high-dimensional vector embeddings, or mathematical representations of data in Azure Cosmos DB.
author: jcodella
ms.author: jacodel
ms.service: azure-cosmos-db
ms.topic: concept-article
ms.date: 11/07/2025
ms.update-cycle: 180-days
ms.collection:
  - ce-skilling-ai-copilot
appliesto:
  - ✅ NoSQL
  - ✅ PostgreSQL
---

# Vector embeddings in Azure Cosmos DB

Vectors, also known as embeddings or vector embeddings, are mathematical representations of data in a high-dimensional space. They represent various types of information, such as text, images, and audio, in a format that machine learning models can process.

When an AI model receives text input, it first tokenizes the text into tokens. Each token is then converted into its corresponding embedding. This conversion process can be done using an embedding generation model, such as [Azure OpenAI embeddings](/azure/ai-services/openai/how-to/embeddings) or [Hugging Face on Azure](https://azure.microsoft.com/solutions/hugging-face-on-azure).

The model processes these embeddings through multiple layers, capturing complex patterns and relationships within the text. The output embeddings can then be converted back into tokens if needed, generating readable text.

> [!VIDEO 3500398e-96fb-48a7-935a-7b778c9d9c7b]

## Vectors

Each embedding is a vector of floating-point numbers (for example, `float32` or `float16`), such that the distance between two embeddings in the vector space is correlated with semantic similarity between two inputs in the original format. For example, if two texts are similar, then their vector representations should also be similar. These high-dimensional representations capture semantic meaning, making it easier to perform tasks like searching, clustering, and classifying.

Here are two examples of texts represented as vectors:

:::image type="content" source="../media/gen-ai/concepts/vector-examples.png" lightbox="../media/gen-ai/concepts/vector-examples.png" alt-text="Screenshot of vector examples in Azure Cosmos DB.":::

> Image source: [OpenAI](https://openai.com/index/introducing-text-and-code-embeddings/)

## Dimensions and closeness

Each box containing floating-point numbers corresponds to a dimension, and each dimension corresponds to a feature or attribute that might be comprehensible to humans. Large language model (LLM) text embeddings typically have a few thousand dimensions, while more complex data models might have tens of thousands of dimensions.

Between the two vectors in the preceding example, some dimensions are similar while other dimensions are different, which are due to the similarities and differences in the meaning of the two phrases.

This image shows the spatial closeness of vectors that are similar, contrasting vectors that are drastically different:

:::image type="content" source="../media/gen-ai/concepts/vector-closeness.png" lightbox="../media/gen-ai/concepts/vector-closeness.png" alt-text="Screenshot of vector closeness in Azure Cosmos DB.":::

> Image source: [OpenAI](https://openai.com/index/introducing-text-and-code-embeddings/)

## Examples

You can see more examples in this [interactive visualization](https://openai.com/index/introducing-text-and-code-embeddings/#text-similarity-models) that transforms data into a three-dimensional space.

## Related content

- [What is a vector database?](../vector-database.md)
- [Retrieval-augmented generation (RAG)](rag.md)
- [Vector search in Azure Cosmos DB NoSQL](../vector-search.md)
- [Vector store in Azure Cosmos DB for MongoDB](../mongodb/vcore/vector-search.md)
- [Vector search in Azure Cosmos DB](vector-search-overview.md)
- [What are tokens?](tokens.md)
- [What are distance functions?](distance-functions.md)
- [kNN vs ANN vector search algorithms](knn-vs-ann.md)
