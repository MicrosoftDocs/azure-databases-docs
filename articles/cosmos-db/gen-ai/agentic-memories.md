---
title: Agentic Memory in Azure Cosmos DB for NoSQL
titleSuffix: Azure Cosmos DB for NoSQL
description: Learn about implementing agentic memories in Azure Cosmos DB
author: jcodella
ms.author: jacodel
ms.service: azure-cosmos-db
ms.topic: how-to
ms.date: 9/24/2025
appliesto:
  - ✅ NoSQL
---

# Agentic Memories in Azure Cosmos DB for NoSQL

## What Are Agentic Memories?

*Agentic memory* (also referred to as *agent memory* or *AI memory*) refers to an AI agent’s ability to persist and recall prior interactions, facts, and experiences to better reason, plan, or act over time. Agent memory is often divided into short-term (episodic / working) memory and long-term memory. This article is designed to guide you through the most common patterns for storing and retrieving agentic memories in your applications. It explains how each pattern works, highlights its strengths and limitations, and offers practical tips so you can confidently choose the right approach for your use cases.

### Short-Term Memory

Short-term memory holds recent context. For example, recent conversation turns, state information, results from tool or function calls. These are all useful to the agent the current task or thread. It can get deleted after some time (for example, using [TTL](../nosql/time-to-live.md)), aggregated or summarized by thread, and classified as *long-term* memory. 

For example:
- In a conversational agent, the last 5–10 user/agent dialogue turns, including prompts, LLM responses, tool call results, etc. 
- Intermediate states or partial task steps (for example retrieval of information from an API/tool call used in a subsequent step).

### Long-Term Memory
Long-term memory is more persistent and accumulates knowledge or patterns over multiple threads or conversations. It supports recall beyond immediate context. For example,
- User preferences (for example “User prefers responses in bullet lists”, or “User is vegetarian”).
- Historical summaries or reflections of short-term memories, or long threads. For example, "In this thread, the customer discussed their preferences for cotton socks and dislike of synthetic materials".


## Design patterns
In the next section, we divide the discussion into three parts. First, we guide you through partition key selection, helping you pick a key that balances write and query throughput across partitions. Then, we explore data modeling patterns and various trade-offs. Finally, we cover basic query patterns that can be applied for different retrieval scenarios. 

## Choose a partition key
As Azure Cosmos DB automatically partitions your data, choosing a partition key is one of the most important design choices for your data model. The partition key determines how data is distributed in logical partitions and across physical partitions, which directly affects query and insert performance, scalability, and cost. Each partition key value maps to a distinct logical partition. A good partition strategy balances locality (keeping related items together for efficient queries) with distribution. In this guide, we highlight three common approaches. You should read about [partitioning in Azure Cosmos DB for more detail.](../partitioning-overview.md)

Below are some common patterns and trade-offs when using Cosmos DB (or Cosmos-style NoSQL + vector features) to store agent memory.

### Use a GUID 
Each item gets its own unique partition key value, typically a GUID. This strategy maximizes write distribution and avoids the hot partition problem, because every write lands in a different logical partition. It's simple to implement and works well for write heavy workloads without strong locality requirements. The tradeoff is that queries span logical and possibly physical partitions, which can be more expensive. This can be useful for storing ephemeral AI agent turns where you care more about logging and long-term analytics than revisiting specific conversations.

- Example: Partition Key: `/pk` that takes on values like: "b9c5b6ce-2d9a-4a2b-9d76-0f5f9b2a9a91"

### Use a unique thread ID
All items for a conversation share the same partition key equal to the thread (or thread) ID. This colocates turns and summaries, which makes “latest N”, phrase filters, and other queries within a thread efficient. However, you must ensure there are enough workload distribution across threads to reduce likelihood of hot partitions. This is generally a good choice for conversational agents or RAG apps where most queries are scoped to a single conversation, such as retrieving the latest turns or doing vector search within one thread.

- Example: Partition Key: /threadId that takes on values like: "thread-1234"

### Use a tenant ID and thread ID

Use a two-level hierarchical partition key where the leading level is the tenant ID and the second is the thread ID. This preserves locality within a thread while grouping threads under a tenant for governance, quotas, and analytics. It also reduces cross-partition scans for tenant-level queries and enables safer multitenant isolation patterns. This is best for multitenant apps where each customer (tenant) runs many concurrent conversations and more isolation is needed.

- Example: ["/tenantId", "/threadId"] takes on values like tenantId = "contoso", threadId = "thread-1234"


### Choose a vector indexing type
When you enable vector search in Azure Cosmos DB, you must choose not only whether to shard but also which index type to use. Cosmos supports multiple vector-index algorithms, including `quantizedFlat` and `DiskANN`. The `quantizedFlat` index type is suited for smaller workloads or when you expect the number of vectors to remain modest (for example, tens of thousands of vectors total). It compresses (quantizes) each vector and performs an exact search over the compressed space, trading a slight accuracy loss for lower RU cost and faster scans. 

However, once your vector data scales up (for example, hundreds of thousands to billions of embeddings), `DiskANN` is the better choice. DiskANN implements approximate nearest-neighbor indexing and is optimized for high throughput, low latency, and cost efficiency at scale. It supports dynamic updates and achieves excellent recall across large datasets.

Learn more about [vector indexes in Azure Cosmos DB](../nosql/vector-search.md#vector-indexing-policies).


If using DiskANN, you then decide whether to shard the vector index via the  [vectorIndexShardKey](sharded-diskann.md). This lets you partition the DiskANN index based on a document property (for example, session, user, tenant), reducing the candidate search space and making semantic queries more efficient and focused. For example, you can shard by a tenant and/or userid. In multitenant systems, isolating the vector index per tenant ensures that search on a particular tenant or user data is fast and efficient. Using the multitenant example from the section on [partitioning](#choose-a-partition-key), you can set the vectorIndexShardKey and the partition key to be the same, or just the first level of your hierarchical partition key. 

On the other hand, using a global (nonsharded) index offers simplicity and the ability to search on the entire set of vectors. Both of these allow you to further refine the search using `WHERE` clause filters as with any other query. 

## Data models

### One turn per document
In this model, each document captures a complete back-and-forth exchange, or turns, between two entities in a thread. For example, this could be a user's prompt and the agent’s response, or the agent's call to a tool and the response. The document becomes a natural unit of memory that can be stored, queried, and expired as a whole. This makes it efficient to retrieve context for a single exchange, while still supporting vector search and keyword search at the exchange or per-message level. This model is ysefyk when the natural unit of memory is a complete exchange (prompt + response, or agent + tool back-and-forth). 

**Example scenarios**:
    - An agentic chat application where each turn consists of the user’s question and the agent’s reply, and you frequently need to resurface entire Q&A pairs for context injection.
    - A planning agent that queries an external API (tool) and logs both the request and tool response as one memory unit, so downstream queries can recall the whole exchange. 
    - Using the memories as part of a [semantic cache](semantic-cache.md), which can reduce user epxierence latency, token consumption, and LLM-based costs.
    
**Properties in a data item**

| Property | Type | Required | Description | Example |
| --------------- | ----------------- | ------- | ----------- | ----------- |
| `id` | string | ✅ | Partition key. See above for guidance on [choosing a partition key](#choose-a-partition-key)| `"thread-1234#0007"` |
| `threadId` | string | ✅ | Thread / conversation identifier (commonly the partition key). | `"thread-1234"` |
| `turnIndex` | number (int) | ✅ | Monotonic counter of the *exchange* (0-based or 1-based). | `7` |
| `messages` | object | ✅ | Messages that make up this exchange (for example, user prompt, agent reply, optional tool call/response). | See table below |
| `turnEmbedding` | number[] | optional | Vector for the *whole* exchange (for example, embedding of a concatenated or summarized message pair). | `[0.013, -0.092, …]` |
| `startedAt` | string (ISO 8601) | optional | Timestamp when the exchange began. | `"2025-09-24T10:14:25Z"` |
| `endedAt` | string (ISO 8601) | optional | Timestamp when the exchange completed. | `"2025-09-24T10:14:28Z"` |
| `embedding` | number[] | optional | Vector for this specific turn (You can create embedding of user question for a [semantic cache](semantic-cache.md)). | `[0.11, 0.02, …]` |

**Properties in the `messages` object**

 | Property | Type | Required | Description | Example |
| --------------- | ----------------- | ------- | ----------- | ----------- |
| `role` | string | ✅ | Origin of the message. Typical: `"user"`, `"agent"`, `"tool"`. | `"agent"` |
| `entityId` | string | ✅ | Name or ID of the user, agent, tool, etc. that this message is associated with. | `"agent-assistant-01"` |
| `name` | string | ✅  | Tool/function name or agent persona label. | `"kb.search"` |
| `content` | string | ✅ | Text payload (prompt, reply, tool result snippet). | `"Refund policy is 30 days for unopened items."` |
| `timestamp` | string (ISO 8601) | optional | Message timestamp. | `"2025-09-24T10:14:27Z"` |
| `metadata` | object | optional | Per-message extras (for example, tokens, tool args/results IDs). | `{ "tokens": 17 }` |

```json
{
  "id": "thread-1234#0007",
  "threadId": "thread-1234",
  "turnIndex": 7,
  "entityId": "agent-assistant-01",
  "messages": [
    {
      "role": "user",
      "content": "What’s our refund policy for accessories?",
      "timestamp": "2025-09-24T10:14:25Z",
      "metadata": { "tokens": 12 }
    },
    {
      "role": "agent",
      "content": "Let me check the knowledge base…",
      "timestamp": "2025-09-24T10:14:25Z",
      "metadata": { "tokens": 8 }
    },
  
  ],
  "embedding": [0.013, -0.092, 0.551, ...],
  "startedAt": "2025-09-24T10:14:25Z",
  "endedAt": "2025-09-24T10:14:55Z",
  "metrics": { "inputTokens": 12, "outputTokens": 17, "latencyMs": 300 }
}
```

**Advantages**
- Good for longer threads/conversations. 
- Easy to get “latest N turns” by ordering on turnIndex or timestamp.
- Supports embedding-per-turn for vector similarity queries within the thread and [semantic caching](semantic-cache.md).
- Easy to TTL (expire) older memories if needed.
- Smaller documents per turn don't require potentially expensive updates

**Limitations**
- When summarizing or consolidating, you might want to generate “summary turns”.
- You may need to periodically prune or compact older turns.

### One response per document
In this design, every agent or user interaction (that is “turn”) is stored as its own document in Azure Cosmos DB. All turn documents for a single thread or thread carry the same `threadId`, which acts as a logical link between other turns in the same thread. This pattern is useful for fine-grained retrieval, analytics, or vector similarity search on every single utterance.

**Example scenarios:**
- A conversational agent where embeddings are created for every user and agent message, enabling per-utterance semantic search within a thread.
- Analytics dashboards that measure agent vs. user token counts, sentiment, or latency at the per-message level.
- RAG (retrieval-augmented generation) flows that need to embed and search every response independently (for example “find the most relevant past statement across all threads”).

**Properties in the data item**
| Property  | Type  | Required | Description   | Example  |
| ----------- | ----------------- | ------- | -----------  | -------- |
| `id` | string | ✅ | Partition key. See above for guidance on [choosing a partition key](#choose-a-partition-key) | `"b9c5b6ce-2d9a-4a2b-9d76-0f5f9b2a9a91"`  |
| `threadId` | string | ✅ | Identifier for the conversation/thread. Often chosen as the **partition key** so all turns for a thread are colocated and efficiently queried. In multitenant apps, consider hierarchical PKs like `/tenantId`, `/threadId`. | `"thread-1234"` |
| `turnIndex` | number (int) | ✅ | Monotonic turn counter (0,1,2…). Use with `threadId` to sort/fetch latest N turns. | `3` |
| `entityId` | string | ✅ | Name or ID of the user, agent, tool, etc. that this response is associated with. | `"user-12345"` |
| `role` | string | ✅ | Who produced the turn. Common values: `"user"`, `"agent"`, `"tool"` (or similar).  | `"agent"`   |
| `content`  | string | ✅ | Main text content for this turn (prompt, reply, tool result, etc.).  | `"This is one response from an LLM"` |
| `timestamp` | string (ISO 8601) | ✅ | Creation time for the turn (ISO 8601). Alternatively, you can sort by the system `_ts` (epoch seconds) without storing your own timestamp.  | `"2025-09-24T10:15:00Z"` |
| `embedding` | number[]  | optional | Vector embedding for `content` (or a summary). Must be a **top-level** field that’s included in the container’s vector policy/index to enable vector search. | `[0.017, -0.234, 0.561, ...]`  |
| `metrics` | object | optional | Free-form metrics/attrs for the turn. Keep names machine-friendly (no spaces) for easier querying and indexing. | `{ "inputTokens": 25, "outputTokens": 8 }` |

An example of this memory data item would look like: 
```json
{
  "id": "b9c5b6ce-2d9a-4a2b-9d76-0f5f9b2a9a91",
  "threadId": "thread-1234", 
  "turnIndex": 3, 
  "entityId": "agent-assistant-01",
  "role": "agent",
  "content": "This is one response from an LLM",
  "embedding": [-1.12402894028, ... ],        
  "timestamp": "2025-09-24T10:15:00Z",
  "metrics": { "inputTokens": 12, "outputTokens": 8, "latencyMs": 177 },

}
```

**Advantages**
- Each memory is kept at an atomic/granular level.
- Easy to update/TTL inidivudal responses. 
- Retrieving last N results can be done with a query with filter on the thread ID.

**Limitations**
- Vector embeddings only capture one response at a time. 
- Not keeping a complete turn in one data item (back-and-forth between agent and user or tool call) can limit utility of the memory without subsequent queries. 
- Not ideal model for [semantic caching](semantic-cache.md).

#### One thread per document
Here, all the turns of a conversation (user, agent, tools, etc.) for a given thread or thread are aggregated into a single document. This document contains a list or array of turn entries (each with turnIndex, role, content, embedding, etc.), and optional summary fields, metadata, and a thread-level embedding. Because the entire thread is stored in one document, retrieving the full history (or a large window) becomes a single read. However, appending new turns requires updating (replacing) the document, which can become costly if the document grows large. This model can be useful when sessions are bounded in size or short-lived, and you prefer single-document reads to reconstruct context.

**Example scenarios:**
- Chatbots in customer onboarding or troubleshooting flows, where each thread is short (< 50 turns) and agents need to fetch the entire conversation quickly in one read.
- Conversation summarization services, where you run periodic batch jobs over full sessions to generate embeddings or summaries.


| Property  | Type | Required | Description | Example |
| ------------------ | ---------------- | ------- | ------------ | -------------- |
| `id` | string  | ✅ | Partition key. See above for guidance on [choosing a partition key](#choose-a-partition-key)| `"thread-1234"`  |
| `threadId` | string  | ✅ | Logical thread or thread identifier (often used as partition key). | `"thread-1234"`  |
| `turns` | array of objects | ✅ | A list of individual turn records (user or agent). Each turn contains a small structure (for example, index, role, content, embedding, entityId). | `[ { "turnIndex": 0, "role": "user", "entityId": "user-12345", "content": "Hello" }, { "turnIndex": 1, "role": "agent", "entityId": "agent-assistant-01", "content": "Hi there!" } ]` |
| `embedding` | number[] | optional | Embedding vector computed over a summary or aggregation of the thread. Useful for semantic search over key points of the conversation.  | `[0.101, -0.231, 0.553, …]` |
| `summary`  | string  | optional | A textual “roll-up” or summary of the key points in the thread. | `"User wanted to schedule a meeting; agent fetched available times and confirmed A.M. slots."` |
| `metrics` | object  | optional | Key/value attributes or metrics about the thread. | `{ "startTime": "2025-09-24T09:05:00Z", "lastTurnTime": "2025-09-24T10:15:00Z", "turnCount": 7 }` |

An example of a memory data item would look like: 
```json
{
  "id": "thread-1234",
  "threadId": "thread-1234",
  "messages": [
    {
      "messageIndex": 0,
      "role": "user",
      "entityId": "user-12345",
      "content": "...",
      "timestamp": "2025-09-24T10:15:00Z",
    },
    {
      "messageIndex": 1,
      "role": "agent",
      "entityId": "agent-assistant-01",
      "content": "...",
      "timestamp": "2025-09-24T10:15:00Z",
    },
  ],
  "LastUpdatedtimestamp": "2025-09-24T10:15:00Z",
  "summary": "...", 
  "embedding": [ … ]
}
```

**Advantages**
- All memory for a thread is in one logical document; simple to load in one read.
- Summary text of thread and keep thread information and vector embedding in one data item

**Limitations**
- Requires client-side sorting after retrieval.
- Document size could grow large (Cosmos DB has a size limit per item, currently 2 MB for some APIs, though in NoSQL it can be more but you must consider RU cost and latency).
- Large document updates (writing appends) can incur higher RU charges.
- Vector search becomes coarser. In this pattern, we recommend summarizing the thread and storing a vector embedding for the summary. However, this can be expensive if the thread is frequently updated. 
- Harder to TTL individual turns; TTL applies at the document (thread) granularity.

> [!IMPORTANT]
> This model is typically not recommended unless the thread size has few turns, infrequent updates, and retrieval patterns are simple (for example, retrieve the entire document all at once). Azure Cosmos DB doesn't support sorting on nested objects/arrays, so sorting of last N messages would need to be implemented in application code. 

### Query for retrieval

#### Most recent memories
When you want to reconstruct a conversation context or show recent user/agent interactions, this query pattern is the simplest. It retrieves the last K messages in timestamp order, which is useful for feeding into chat context or displaying a conversation history. Use this when freshness and chronological order matter.
```sql
SELECT TOP @k c.content, c.timestamp
FROM c
WHERE c.threadId = @threadId
ORDER BY c.timestamp DESC
```

#### Retrieve thread by semantic search
Semantic queries let you find turns whose embeddings are most similar to a given query vector, even if they don’t share exact words. This pattern surfaces contextually relevant memories (answers, references, hints) beyond recent messages. This is useful when relevancy is important over recency, however you can use a `WHERE` clause to filter to most recent semantically similar results. 

```sql
SELECT TOP @k c.content, c.timestamp, VECTOR_DISTANCE(c.embedding, @queryVector) AS dist
FROM c
    WHERE c.threadId = @threadId
ORDER BY VECTOR_DISTANCE(c.embedding, @queryVector)
```

#### Memories that contain phrases or keywords
Keyword or phrase search is useful for filtering memories that explicitly mention a term (for example “billing,” “refund,” “meeting”) regardless of semantic closeness. This is helpful when you want strict matching or fallback to lexical recall. This can be extended for use in combination with semantic or recency queries to improve recall. 

```sql
SELECT TOP @k c.content, c.timestamp, 
FROM c
WHERE c.threadId = @threadId
  AND FULLTEXTCONTAINS(c.content, @phrase)
ORDER BY c.timestamp DESC
```


## Next steps
- [Learn about vector indexing and search](vector-search-overview.md)
- [Learn about full text search](full-text-search-faq.md)
- [Learn about hybrid search](hybrid-search.md)
- [Learn about semantic caching](semantic-cache.md)
- [Build a multi-agent app with Azure Cosmos DB](https://aka.ms/CosmosDB/BankingAgentWorkshop)