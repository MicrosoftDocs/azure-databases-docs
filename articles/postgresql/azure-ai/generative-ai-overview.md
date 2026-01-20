---
title: Generative AI
description: Learn about using generative AI with Azure Database for PostgreSQL.
author: mulander
ms.author: adamwolk
ms.reviewer: maghan
ms.date: 01/20/2026
ms.service: azure-database-postgresql
ms.topic: concept-article
ms.collection:
  - ce-skilling-ai-copilot
ms.update-cycle: 180-days
ms.custom:
  - ignite-2023
---

# Generative AI with Azure Database for PostgreSQL

Generative AI refers to a class of AI algorithms that can learn from existing multimedia content and produce new content. The produced content can be customized through techniques such as prompts and fine-tuning. Generative AI algorithms apply specific machine learning models:

- Transformers and recurrent neural networks (RNNs) for text generation
- Generative adversarial networks (GANs) and variational autoencoders (VAEs) for image generation

Generative AI is used in image and music synthesis and in healthcare, along with common tasks such as text autocompletion, text summarization, and translation. Generative AI techniques enable features on data such as clustering and segmentation, semantic search and recommendations, topic modeling, question answering, and anomaly detection.

The following video demonstrates the use of generative AI with Azure Database for PostgreSQL and the [`pgvector` extension](../extensions/../extensions/how-to-use-pgvector.md), which can help you understand the concepts in this article.

> [!Video https://www.youtube.com/embed/em0PKDGzzlQ?si=cT0VVzVv_2xV1Mi_]

## OpenAI

OpenAI is a research organization and technology company known for its pioneering work in the field of AI and machine learning. Its mission is to ensure that artificial general intelligence (AGI), which refers to highly autonomous AI systems that can outperform humans in most economically valuable work, benefits all of humanity. OpenAI brought to market state-of-the-art generative models such as GPT-3, GPT-3.5, and GPT-4.

Azure OpenAI is a Microsoft service offering to help build generative AI applications by using Azure. Azure OpenAI gives customers advanced language AI with OpenAI GPT-4, GPT-3, Codex, DALL-E, and Whisper models, with the security and enterprise capabilities of Azure. Azure OpenAI codevelops the APIs with OpenAI to ensure compatibility and a smooth transition from one to the other.

With Azure OpenAI, customers get the security capabilities of Microsoft Azure while running the same models as OpenAI. Azure OpenAI offers private networking, regional availability, and responsible AI content filtering.

[Learn more about Azure OpenAI](/azure/ai-services/openai/overview).

## Large language model

A large language model (LLM) is a type of AI model that's trained on massive amounts of text data to understand and generate humanlike language. LLMs are typically based on deep learning architectures, such as transformers. They're known for their ability to perform a wide range of natural language understanding and generation tasks. The Azure OpenAI service and OpenAI's ChatGPT are examples of LLM offerings.

Key characteristics and capabilities of LLMs include:

- **Scale**: The scale of LLMs is immense, in terms of the number of parameters that their architectures use. Models like GPT-3 contain from hundreds of millions to trillions of parameters, which allow them to capture complex patterns in language.
- **Pretraining**: LLMs undergo pretraining on a large corpus of text data from the internet. This pretraining enables them to learn grammar, syntax, semantics, and a broad range of knowledge about language and the world.
- **Fine-tuning**: After pretraining, LLMs can be fine-tuned on specific tasks or domains with smaller, task-specific datasets. This fine-tuning process allows them to adapt to more specialized tasks, such as text classification, translation, summarization, and question answering.

## GPT

GPT stands for Generative Pretrained Transformer, and it refers to a series of large language models that OpenAI developed. The GPT models are neural networks that are pretrained on vast amounts of data from the internet, so they're capable of understanding and generating humanlike text.

Here's an overview of the major GPT models and their key characteristics:

- **GPT-3**: Released in June 2020 and a well-known model in the GPT series. It has 175 billion parameters, which makes it one of the largest and most powerful language models in existence.

  GPT-3 achieved remarkable performance on a wide range of natural language understanding and generation tasks. It can perform tasks like text completion, translation, and question answering with human-level fluency.

  GPT-3 is divided into various model sizes, ranging from the smallest (125 million parameters) to the largest (175 billion parameters).

- **GPT-4**: The latest GPT model from OpenAI. It has 1.76 trillion parameters.

## Vectors

A vector is a mathematical concept that's used in linear algebra and geometry to represent quantities that have both magnitude and direction. In the context of machine learning, vectors are often used to represent data points or features.

Key attributes and operations of vectors include:

- **Magnitude**: The length or size of a vector, often denoted as its norm, represents the magnitude of the data. It's a non-negative real number.
- **Direction**: The direction indicates the orientation or angle of the quantity that it represents, in relation to a reference point or coordinate system.
- **Components**: A vector can be decomposed into its components along different axes or dimensions. In a 2D Cartesian coordinate system, a vector can be represented as (*x*, *y*), where *x* and *y* are its components along the x-axis and y-axis, respectively. A vector in *n* dimensions is an *n*-tuple (`{x1, x2... xn}`).
- **Addition and scalar multiplication**: Vectors can be added together to form new vectors, and they can be multiplied by scalars (real numbers).
- **Dot products and cross-products**: Vectors can be combined via dot products (scalar products) and cross-products (vector products).

## Vector databases

A vector database, also known as a vector database management system (DBMS), is a type of database system that's designed to store, manage, and query vector data efficiently. Traditional relational databases primarily handle structured data in tables, whereas vector databases are optimized for the storage and retrieval of multidimensional data points represented as vectors. These databases are useful for applications where operations such as similarity searches, geospatial data, recommendation systems, and clustering are involved.

Key characteristics of vector databases include:

- **Vector storage**: Vector databases store data points as vectors with multiple dimensions. Each dimension represents a feature or attribute of the data point. These vectors can represent a wide range of data types, including numerical, categorical, and textual data.
- **Efficient vector operations**: Vector databases are optimized for performing vector operations, such as vector addition, subtraction, dot products, and similarity calculations (for example, cosine similarity or Euclidean distance).
- **Efficient search**: Efficient indexing mechanisms are crucial for quick retrieval of similar vectors. Vector databases use various indexing mechanisms to enable fast retrieval.
- **Query languages**: Vector databases provide query languages and APIs that are tailored for vector operations and similarity searches. These query languages allow users to express their search criteria efficiently.
- **Similarity search**: Vector databases excel at similarity searches, which allow users to find data points that are similar to a provided query point. This characteristic is valuable in search and recommendation systems.
- **Geospatial data handling**: Some vector databases are designed for geospatial data, so they're well suited for applications like location-based services, geographic information systems (GISs), and map-related tasks.
- **Support for diverse data types**: Vector databases can store and manage various types of data, such as vectors, images, and text.

PostgreSQL can gain the capabilities of a vector database with the help of the [`pgvector` extension](../extensions/../extensions/how-to-use-pgvector.md).

## Embeddings

Embeddings are a concept in machine learning and natural language processing that involves representing objects (such as words, documents, or entities) as vectors in a multidimensional space.

These vectors are often dense. That is, they have a high number of dimensions. They're learned through various techniques, including neural networks. Embeddings aim to capture semantic relationships and similarities between objects in a continuous vector space.

Common types of embeddings include:

- **Word**: In natural language processing, word embeddings represent words as vectors. Each word is mapped to a vector in a high-dimensional space, where words with similar meanings or contexts are located closer to each other. `Word2Vec` and `GloVe` are popular word-embedding techniques.
- **Document**: Document embeddings represent documents as vectors. `Doc2Vec` is popular for creating document embeddings.
- **Image**: Images can be represented as embeddings to capture visual features for tasks like object recognition.

Embeddings are central to representing complex, high-dimensional data in a form that machine learning models can easily process. They can be trained on large datasets and then used as features for various tasks. LLMs use them.

PostgreSQL can gain the capabilities of [generating vector embeddings with Azure AI extension OpenAI integration](generative-ai-azure-openai.md).

## Scenarios

Generative AI has a wide range of applications across various domains and industries, including technology, healthcare, entertainment, finance, manufacturing, and more. Here are some common tasks that people can accomplish by using generative AI:

- [Semantic search](generative-ai-semantic-search.md):
  - Generative AI enables semantic search on data rather than lexicographical search. The latter looks for exact matches to queries, whereas semantic search finds content that satisfies the search query's intent.
- Chatbots and virtual assistants:
  - Develop chatbots that can engage in natural context-aware conversations; for example, to implement self-help for customers.
- Recommendation systems:
  - Improve recommendation algorithms by generating embeddings or representations of items or users.
- Clustering and segmentation:
  - Generative AI-generated embeddings allow clustering algorithms to cluster data so that similar data is grouped together. This clustering enables scenarios such as customer segmentation, which allows advertisers to target their customers differently based on their attributes.
- Content generation:
  - Generate humanlike text for applications like chatbots, novel/poetry creation, and natural language understanding.
  - Create realistic images, artwork, or designs for graphics, entertainment, and advertising.
  - Generate videos, animations, or video effects for films, gaming, and marketing.
  - Generate music.
- Translation:
  - Translate text from one language to another.
- Summarization:
  - Summarize long articles or documents to extract key information.
- Data augmentation:
  - Generate extra data samples to expand and improve training datasets for machine learning models.
  - Create synthetic data for scenarios that are difficult or expensive to collect in the real world, such as medical imaging.
- Drug discovery:
  - Generate molecular structures and predict potential drug candidates for pharmaceutical research.
- Game development:
  - Create game content, including levels, characters, and textures.
  - Generate realistic in-game environments and landscapes.
- Data denoising and completion:
  - Clean noisy data by generating clean data samples.
  - Fill in missing or incomplete data in datasets.

## Related content

- [Integrate Azure Database for PostgreSQL with Azure Cognitive Services](generative-ai-azure-cognitive.md)
- [Integrate Azure Database for PostgreSQL with Azure Machine Learning](generative-ai-azure-machine-learning.md)
- [Generate vector embeddings with Azure OpenAI in Azure Database for PostgreSQL](generative-ai-azure-openai.md)
- [Azure AI extension in Azure Database for PostgreSQL](generative-ai-azure-overview.md)
- [Create a recommendation system with Azure Database for PostgreSQL and Azure OpenAI](generative-ai-recommendation-system.md)
- [Create a semantic search with Azure Database for PostgreSQL and Azure OpenAI](generative-ai-semantic-search.md)
- [Enable and use pgvector in Azure Database for PostgreSQL](../extensions/../extensions/how-to-use-pgvector.md)
