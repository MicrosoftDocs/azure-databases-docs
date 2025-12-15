---
title: Integrated Vector Database
titleSuffix: Azure Cosmos DB
description: Review how to use Azure Cosmos DB as a vector database in numerous domains and situations across analytical and generative AI.
author: markjbrown
ms.author: mjbrown
ms.service: azure-cosmos-db
ms.custom:
  - build-2024
ms.topic: concept-article
ms.date: 09/04/2025
ms.update-cycle: 180-days
ms.collection:
  - ce-skilling-ai-copilot
appliesto:
  - ✅ NoSQL
  - ✅ PostgreSQL
---

# Vector database

> [!TIP]
> For the latest vector database and RAG pattern app samples, visit [Azure Cosmos DB Samples Gallery](https://aka.ms/AzureCosmosDB/Gallery/AI).

Vector databases are used in numerous domains and situations across analytical and generative AI, including natural language processing, video and image recognition, recommendation system, and search, among others.

In 2023, a notable trend in software was the integration of AI enhancements, often achieved by incorporating specialized standalone vector databases into existing tech stacks. This article explains what vector databases are and presents an alternative architecture that you might want to consider: using an integrated vector database in the NoSQL or relational database you already use, especially when working with multi-modal data. This approach not only allows you to reduce cost but also achieve greater data consistency, scalability, and performance.

> [!TIP]
> Data consistency, scalability, and performance are critical for data-intensive applications, which is why OpenAI chose to build the ChatGPT service on top of Azure Cosmos DB. You, too, can take advantage of its integrated vector database, as well as its single-digit millisecond response times, automatic and instant scalability, and guaranteed speed at any scale. See [implementation samples](#how-to-implement-integrated-vector-database-functionalities) and [try it for free](free-tier.md).

## What is a vector database?

A vector database is a database designed to store and manage [vector embeddings](#embeddings), which are mathematical representations of data in a high-dimensional space. In this space, each dimension corresponds to a feature of the data, and tens of thousands of dimensions might be used to represent sophisticated data. A vector's position in this space represents its characteristics. Words, phrases, or entire documents, and images, audio, and other types of data can all be vectorized. These vector embeddings are used in similarity search, multi-modal search, recommendations engines, large languages models (LLMs), etc.

In a vector database, embeddings are indexed and queried through [vector search](#vector-search) algorithms based on their vector distance or similarity. A robust mechanism is necessary to identify the most relevant data. Some well-known vector search algorithms include Hierarchical Navigable Small World (HNSW), Inverted File (IVF), and DiskANN.

### Integrated vector database vs pure vector database

There are two common types of vector database implementations: pure vector database and integrated vector database in a NoSQL or relational database.

- A *pure* vector database is designed to efficiently store and manage vector embeddings, along with a small amount of metadata; it's separate from the data source from which the embeddings are derived.

- A vector database that is *integrated* in a highly performant NoSQL or relational database provides additional capabilities. The integrated vector database in a NoSQL or relational database can store, index, and query embeddings alongside the corresponding original data. This approach eliminates the extra cost of replicating data in a separate pure vector database. Moreover, keeping the vector embeddings and original data together better facilitates multi-modal data operations, and enables greater data consistency, scale, and performance. A highly performant database with schema flexibility and integrated vector database is especially optimal for [AI agents](ai-agents.md).

### Vector database use cases

Vector databases are used in numerous domains and situations across analytical and generative AI, including natural language processing, video and image recognition, recommendation system, and search. For example, you can use a vector database to:

- Identify similar images, documents, and songs based on their contents, themes, sentiments, and styles
- Identify similar products based on their characteristics, features, and user groups
- Recommend contents, products, or services based on individuals' preferences
- Recommend contents, products, or services based on user groups' similarities
- Identify the best-fit potential options from a large pool of choices to meet complex requirements
- Identify data anomalies or fraudulent activities that are dissimilar from predominant or normal patterns
- Implement persistent memory for AI agents

> [!TIP]
> Besides these typical use cases for vector databases, our integrated vector database is also an ideal solution for production-level LLM caching thanks to its low latency, high scalability, and high availability.

Vector databases are especially popular for enabling [retrieval-augmented generation (RAG)](#retrieval-augmented-generation) that harnesses LLMs and custom data or domain-specific information. This approach allows you to:

- Generate contextually relevant and accurate responses to user prompts from AI models
- Overcome LLMs' [tokens](#tokens) limits
- Reduce the costs from frequent fine-tuning on updated data

This process involves extracting pertinent information from a custom data source and integrating it into the model request through prompt engineering. Before sending a request to the LLM, the user input/query/request is also transformed into an embedding, and vector search techniques are employed to locate the most similar embeddings within the database. This technique enables the identification of the most relevant data records in the database. These retrieved records are then supplied as input to the LLM request using [prompt engineering](#prompts-and-prompt-engineering).

> [!Note]
> **Interested in ultra-high throughput vector search capabilities?** 
> Azure Cosmos DB is developing enhanced vector search features designed for large vector datasets paired with ultra-high throughput inserts and searches. It can accommodate millions of queries per second (QPS) with predictable, low latency and unmatched cost efficiency. Sign up to learn more about early access opportunities and get notified when these capabilities become available.
> 
> [*Sign up for the expanded Private Preview.*](https://aka.ms/cosmos-high-scale-vector-preview)

## Vector database related concepts

### Embeddings

An embedding is a special format of data representation that machine learning models and algorithms can easily use. The embedding is an information-dense representation of the semantic meaning of a piece of text. Each embedding is a vector of floating-point numbers, such that the distance between two embeddings in the vector space is correlated with semantic similarity between two inputs in the original format. For example, if two texts are similar, then their vector representations should also be similar. A vector database extension that allows you to store your embeddings with your original data ensures data consistency, scale, and performance.

### Vector search

Vector search is a method that helps you find similar items based on their data characteristics rather than by exact matches on a property field. This technique is useful in applications such as searching for similar text, finding related images, making recommendations, or even detecting anomalies.

It works by taking the vector representations (lists of numbers) of your data that you created with a machine learning model by using an embeddings API, such as [Azure OpenAI Embeddings](/azure/ai-services/openai/how-to/embeddings) or [Hugging Face on Azure](https://azure.microsoft.com/solutions/hugging-face-on-azure). It then measures the distance between the data vectors and your query vector. The data vectors that are closest to your query vector are the ones that are found to be most similar semantically.

Using a native vector search feature offers an efficient way to store, index, and search high-dimensional vector data directly alongside other application data. This approach removes the necessity of migrating your data to costlier alternative vector databases and provides a seamless integration of your AI-driven applications.

### Prompts and prompt engineering

A prompt refers to a specific text or information that can serve as an instruction to an LLM, or as contextual data that the LLM can build upon. A prompt can take various forms, such as a question, a statement, or even a code snippet. Prompts can serve as:

- Instructions that provide directives to the LLM
- Primary content that gives information to the LLM for processing
- Examples to help condition the model to a particular task or process
- Cues to direct the LLM's output in the right direction
- Supporting content that represents supplemental information the LLM can use to generate output

The process of creating good prompts for a scenario is called prompt engineering. For more information about prompts and best practices for prompt engineering, see [System message design](/azure/ai-services/openai/concepts/advanced-prompt-engineering).

### Tokens

Tokens are small chunks of text generated by splitting the input text into smaller segments. These segments can either be words or groups of characters, varying in length from a single character to an entire word. For instance, the word hamburger would be divided into tokens such as ham, bur, and ger while a short and common word like pear would be considered a single token. LLMs like ChatGPT, GPT-3.5, or GPT-4 break words into tokens for processing. [[Go back](#vector-database-use-cases)]

### Retrieval-augmented generation

Retrieval-augmentated generation (RAG) is an architecture that augments the capabilities of LLMs like ChatGPT, GPT-3.5, or GPT-4 by adding an information retrieval system like vector search that provides grounding data, such as those stored in a vector database. This approach allows your LLM to generate contextually relevant and accurate responses based on your custom data sourced from vectorized documents, images, audio, video, etc.

A simple RAG pattern using Azure Cosmos DB for NoSQL could:

1. Enable [Azure Cosmos DB NoSQL Vector Index](nosql/vector-search.md)
1. Set up a database and container with a container vector policy and vector index
1. Insert data into an Azure Cosmos DB for NoSQL database and container
1. Create embeddings from a data property using Azure OpenAI Embeddings
1. Link the Azure Cosmos DB for NoSQL.
1. Create a vector index over the embeddings properties
1. Create a function to perform vector similarity search based on a user prompt
1. Perform question answering over the data using an Azure OpenAI Completions model

The RAG pattern, with prompt engineering, serves the purpose of enhancing response quality by offering more contextual information to the model. RAG enables the model to apply a broader knowledge base by incorporating relevant external sources into the generation process, resulting in more comprehensive and informed responses. For more information, see [Grounding LLMs](https://techcommunity.microsoft.com/t5/fasttrack-for-azure/grounding-llms/ba-p/3843857).

## How to implement integrated vector database functionalities

You can implement integrated vector database functionalities for Azure Cosmos DB and its various compatibility APIs.

### NoSQL API

Azure Cosmos DB for NoSQL is the world's first serverless NoSQL vector database. Store your vectors and data together in [Azure Cosmos DB for NoSQL with integrated vector database capabilities](nosql/vector-search.md) where you can create a vector index based on [DiskANN](https://www.microsoft.com/research/publication/diskann-fast-accurate-billion-point-nearest-neighbor-search-on-a-single-node/), a suite of high-performance vector indexing algorithms developed by Microsoft Research.

DiskANN enables you to perform highly accurate, low-latency queriers at any scale while leveraging all the benefits of Azure Cosmos DB for NoSQL such as 99.999% SLA (with HA-enabled), geo-replication, seamless transition from serverless to provisioned throughput (RU) all in one data store.

#### Links and samples

- [What is the database behind ChatGPT? - Microsoft Mechanics](https://www.youtube.com/watch?v=6IIUtEFKJec)
- [Vector indexing in Azure Cosmos DB for NoSQL](index-policy.md#vector-indexes)
- [VectorDistance system function NoSQL queries](/cosmos-db/query/vectordistance)
- [Vector Search in Azure Cosmos DB for NoSQL](nosql/vector-search.md)
- [Python - Notebook tutorial](https://github.com/microsoft/AzureDataRetrievalAugmentedGenerationSamples)
- [C# - Build Your Own Copilot Complete Solution Accelerator with AKS and Semantic Kernel](https://aka.ms/cdbcopilot)
- [C# - Build Your Own Copilot Sample App and Hands-on-Lab](https://github.com/AzureCosmosDB/cosmosdb-nosql-copilot)
- [Python - Movie Chatbot](https://github.com/AzureCosmosDB/Fabric-Conf-2024-Build-AI-Apps/tree/main/AzureCosmosDBforNoSQL)

#### Code samples

- [Python Notebook - Vector database integration through LangChain tutorial](https://python.langchain.com/docs/integrations/vectorstores/azure_cosmos_db)
- [Python Notebook - LLM Caching integration through LangChain tutorial](https://python.langchain.com/docs/integrations/vectorstores/azure_cosmos_db_no_sql/)
- [Python - LlamaIndex integration](https://developers.llamaindex.ai/python/examples/vector_stores/azurecosmosdbmongodbvcoredemo/)
- [Python - Semantic Kernel memory integration](https://github.com/microsoft/semantic-kernel/tree/main/python/semantic_kernel/connectors/memory_stores/azure_cosmosdb)
- [Python Notebook - Movie Chatbot](https://github.com/AzureCosmosDB/Fabric-Conf-2024-Build-AI-Apps/tree/main/AzureCosmosDBforMongoDB)

> [!div class="nextstepaction"]
> [Use Azure Cosmos DB for MongoDB lifetime free tier](mongodb/vcore/free-tier.md)
  
### API for PostgreSQL

Use the natively integrated vector database in [Azure Cosmos DB for PostgreSQL](postgresql/howto-use-pgvector.md), which offers an efficient way to store, index, and search high-dimensional vector data directly alongside other application data. This approach removes the necessity of migrating your data to costlier alternative vector databases and provides a seamless integration of your AI-driven applications.

#### Code sample

- Python: [Python notebook tutorial - food review chatbot](https://github.com/microsoft/AzureDataRetrievalAugmentedGenerationSamples/tree/main/Python/CosmosDB-PostgreSQL_CognitiveSearch)

## Next step

> [!div class="nextstepaction"]
> [Use the Azure Cosmos DB lifetime free tier](free-tier.md)
