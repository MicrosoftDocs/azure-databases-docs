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

*Agentic memory* (also referred to as *agent memory* or *AI memory*) refers to an AI agent’s ability to persist and recall prior interactions, facts, and experiences to better reason, plan, or act over time. Agent memory is often divided into short-term (episodic / working) memory and long-term memory.  This article is designed to guide you through the most common patterns for storing and retrieving agentic memories in your applications. It explains how each pattern works, highlights its strengths and limitations, and offers practical tips so you can confidently choose the right approach for your use cases.

### Short-Term Memory

Short-term memory holds recent context (for example, recent conversation turns, transient states) that's useful to the agent for threads or tasks. It may get deleted after some time (for example, using [TTL](../nosql/time-to-live.md)), summarized, or moved to long-term memory. For example:
- In a conversational agent, the last 5–10 user/agent dialogue turns, including prompts, LLM responses, tool call results, etc. 
- Intermediate states or partial task steps (for example retrieval of information from an API/tool call used in a subsequent step).

### Long-Term Memory
Long-term memory is more persistent and accumulates knowledge or patterns over multiple threads. It supports recall beyond immediate context. For example,
- User preferences (e.g. “User prefers responses in bullet lists”, or “User is vegetarian”).
- Historical summaries or reflections of short-term memories, or long threads.

## Design patterns: Partition key selection
Partitioning is one of the most important design choices when modeling data for Azure Cosmos DB. The partition key determines how data is distributed in logical partitions and across physical partitions, which directly affects query and insert performance, scalability, and cost. A good partition strategy balances locality (keeping related items together for efficient queries) with distribution. In this guide, we highlight three common approaches. You should read about [partitioning in Azure Cosmos DB for more detail.](../partitioning-overview.md)

Below are some common patterns and trade-offs when using Cosmos DB (or Cosmos-style NoSQL + vector features) to store agent memory.

### Use a GUID as the partition key
Each item gets its own unique partition key value, typically a GUID. This strategy maximizes write distribution and avoids the hot partition problem, because every write lands in a different logical partition. It's simple to implement and works well for write heavy workloads without strong locality requirements. The tradeoff is that queries span logical and possibly physical partitions, which can be more expensive. This can be useful for storing ephemeral AI agent turns where you care more about logging and long-term analytics than revisiting specific conversations. F

- Example: Partition Key: `/pk` that takes on values like: "b9c5b6ce-2d9a-4a2b-9d76-0f5f9b2a9a91"

### Use a unique thread ID as the partition key
All items for a conversation share the same partition key equal to the thread (or thread) ID. This colocates turns and summaries, which makes “latest N”, phrase filters, and other queries within a thread efficient. However, you must ensure there are enough workload distribution across threads to reduce likelihood of hot partitions. This is generally a good choice for conversational agents or RAG apps where most queries are scoped to a single conversation, such as retrieving the latest turns or doing vector search within one thread.

- Example: Partition Key: /threadId that takes on values like: "thread-1234"

### Multitenancy: Use a tenant ID and thread ID as a hierarchical partition key

Use a two-level hierarchical partition key where the leading level is the tenant ID and the second is the thread ID. This preserves locality within a thread while grouping threads under a tenant for governance, quotas, and analytics. It also reduces cross-partition scans for tenant-level queries and enables safer multitenant isolation patterns. This is best for multitenant apps where each customer (tenant) runs many concurrent conversations and more isolation is needed.

- Example: ["/tenantId", "/threadId"] takes on values like tenantId = "contoso", threadId = "thread-1234"

## Design patterns: Data models & query patterns

### One turn per document
In this model, each document captures a complete back-and-forth exchange, or turn, within a thread, such as a user prompt, the agent’s reply, and any intermediate tool calls. When grouping related messages together, the document becomes a natural unit of memory that can be stored, queried, and expired as a whole. This makes it efficient to retrieve context for a single exchange, while still supporting vector search and keyword search at the exchange or per-message level. 

##### Data model
**Properties in a data item**
| Property | Type | Required | Description | Example |
| --------------- | ----------------- | -------: | ----------- | ----------- |
| `id` | string | ✅ | Partition key. See above for [guidance on choosing a partition key](#partition-key-selection)| `"thread-1234#0007"` |
| `threadId` | string | ✅ | Thread / conversation identifier (commonly the partition key). | `"thread-1234"` |
| `turnIndex` | number (int) | ✅ | Monotonic counter of the *exchange* (0-based or 1-based). | `7` |
| `messages` | object | ✅ | Messages that make up this exchange (for example, user prompt, agent reply, optional tool call/response). | See table below |
| `turnEmbedding` | number[] | optional | Vector for the *whole* exchange (for example, embedding of a concatenated or summarized message pair). | `[0.013, -0.092, …]` |
| `startedAt` | string (ISO 8601) | optional | Timestamp when the exchange began. | `"2025-09-24T10:14:25Z"` |
| `endedAt` | string (ISO 8601) | optional | Timestamp when the exchange completed. | `"2025-09-24T10:14:28Z"` |
| `embedding` | number[] | optional | Vector for this specific turn (You can create embedding of user question for a [semantic cache](semantic-cache.md)). | `[0.11, 0.02, …]` |

**Properties in the `messages` object**
 | Property | Type | Required | Description | Example |
| ----------- | ----------------- | -------: | --------- | --------- |
| `role` | string | ✅ | Origin of the message. Typical: `"user"`, `"agent"`, `"tool"`. | `"agent"` |
| `name` | string | ✅  | Tool/function name or agent persona label. | `"kb.search"` |
| `content` | string | ✅ | Text payload (prompt, reply, tool result snippet). | `"Refund policy is 30 days for unopened items."` |
| `timestamp` | string (ISO 8601) | optional | Message timestamp. | `"2025-09-24T10:14:27Z"` |
| `metadata` | object | optional | Per-message extras (for example, tokens, tool args/results IDs). | `{ "tokens": 17 }` |

```json
{
  "id": "thread-1234#0007",
  "threadId": "thread-1234",
  "turnIndex": 7,
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

#### Query patterns

**Most recent messages**
```sql
SELECT TOP @k d.role, d.content FROM c JOIN d in c.messages
FROM c
WHERE c.threadId = @threadId
ORDER BY c.timestamp DESC
```

**Most relevant memory by semantic search**
```SQL
SELECT TOP @k d.role, d.content FROM c JOIN d in c.messages, VECTOR_DISTANCE(c.embedding, @queryVector) AS dist
FROM c
WHERE c.threadId = @threadId
ORDER BY VECTOR_DISTANCE(c.embedding, @queryVector)
```

**Memories that contain phrases or keywords**
```sql
SELECT TOP @k d.role, d.content FROM c JOIN d in c.messages
FROM c
WHERE c.threadId = @threadId
  AND FULLTEXTCONTAINS(d.content, @phrase)
ORDER BY c.timestamp DESC
```

### One response per document

In this design, every agent or user interaction (that is “turn”) is stored as its own document in Azure Cosmos DB. All turn documents for a single thread or thread carry the same `threadId`, which acts as a logical link between other turns in the same thread.

##### Data model

**Properties in the data item**
| Property  | Type  | Required | Description   | Example  |
| ----------- | ----------------- | -------: | -----------  | -------- |
| `id` | string | ✅ | Partition key. See above for [guidance on choosing a partition key](#partition-key-selection) | `"b9c5b6ce-2d9a-4a2b-9d76-0f5f9b2a9a91"`  |
| `threadId` | string | ✅ | Identifier for the conversation/thread. Often chosen as the **partition key** so all turns for a thread are colocated and efficiently queried. In multitenant apps, consider hierarchical PKs like `/tenantId`, `/threadId`. | `"thread-1234"` |
| `turnIndex` | number (int) | ✅ | Monotonic turn counter (0,1,2…). Use with `threadId` to sort/fetch latest N turns. | `3` |
| `role` | string | ✅ | Who produced the turn. Common values: `"user"`, `"agent"`, `"tool"` (or similar).  | `"agent"`   |
| `content`  | string | ✅ | Main text content for this turn (prompt, reply, tool result, etc.).  | `"This is one response from an LLM"` |
| `timestamp` | string (ISO 8601) | ✅ | Creation time for the turn (ISO 8601). Alternatively, you can sort by the system `_ts` (epoch seconds) without storing your own timestamp.  | `"2025-09-24T10:15:00Z"` |
| `embedding` | number[]  | optional | Vector embedding for `content` (or a summary). Must be a **top-level** field that’s included in the container’s vector policy/index to enable vector search. | `[0.017, -0.234, 0.561, ...]`  |
| `metrics` | object | optional | Free-form metrics/attrs for the turn. Keep names machine-friendly (no spaces) for easier querying and indexing. | `{ "inputTokens": 25, "outputTokens": 8 }` |

An example of this memory data item would look like: 
```json
{
  "id": "b9c5b6ce-2d9a-4a2b-9d76-0f5f9b2a9a91",  // unique guid for the document
  "threadId": "thread-1234", // unique id for the thread
  "turnIndex": 3, 
  "role": "agent",
  "content": "This is one response from an LLM",
  "embedding": [-1.12402894028, ... ],         // optional vector
  "timestamp": "2025-09-24T10:15:00Z",
  "metrics": { "inputTokens": 12, "outputTokens": 8, "latencyMs": 177 },

}
```
**Pros**
- Good for longer threads/conversations. 
- Easy to get “latest N turns” by ordering on turnIndex or timestamp.
- Supports embedding-per-turn for vector similarity queries within the thread.
- Easy to TTL (expire) older memories if needed.
- Smaller documents per turn don't require potentially expensive updates

**Cons**
- When summarizing or consolidating, you might want to generate “summary turns”.
- You may need to periodically prune or compact older turns.


#### Query patterns

**Most recent messages**
```sql
SELECT TOP @k c.content, c.timestamp
FROM c
WHERE c.threadId = @threadId
ORDER BY c.timestamp DESC
```

**Most relevant memory by semantic search**
```sql
SELECT TOP @k c.content, c.timestamp, VECTOR_DISTANCE(c.embedding, @queryVector) AS dist
FROM c
    WHERE c.threadId = @threadId
ORDER BY VECTOR_DISTANCE(c.embedding, @queryVector)
```

**Memories that contain phrases or keywords**
```sql
-- Case-insensitive phrase match
SELECT TOP @k c.content, c.timestamp, 
FROM c
WHERE c.threadId = @threadId
  AND FULLTEXTCONTAINS(c.content, @phrase)
ORDER BY c.timestamp DESC
```


### One thread per document
Here, all the turns of a conversation (user, agent, tools, etc.) for a given thread or thread are aggregated into a single document. This document contains a list or array of turn entries (each with turnIndex, role, content, embedding, etc.), and optional summary fields, metadata, and a thread-level embedding. Because the entire thread is stored in one document, retrieving the full history (or a large window) becomes a single read. However, appending new turns requires updating (replacing) the document, which can become costly if the document grows large or if there's write contention.


#### Data model
| Property  | Type | Required | Description | Example |
| ------------------ | ---------------- | -------: | ------------ | -------------- |
| `id` | string  | ✅ | Partition key. See above for [guidance on choosing a partition key](#partition-key-selection) | `"thread-1234"`  |
| `threadId` | string  | ✅ | Logical thread or thread identifier (often used as partition key). | `"thread-1234"`  |
| `turns` | array of objects | ✅ | A list of individual turn records (user or agent). Each turn contains a small structure (for example, index, speaker, content, embedding). | `[ { "turnIndex": 0, "speaker": "user", "content": "Hello" }, { "turnIndex": 1, "speaker": "agent", "content": "Hi there!" } ]` |
| `embedding` | number[] | optional | Embedding vector computed over a summary or aggregation of the thread. Useful for semantic search over key points of the conversation.  | `[0.101, -0.231, 0.553, …]` |
| `summary`  | string  | optional | A textual “roll-up” or summary of the key points in the thread. | `"User wanted to schedule a meeting; agent fetched available times and confirmed A.M. slots."` |
| `metrics` | object  | optional | Key/value attributes or metrics about the thread. | `{ "startTime": "2025-09-24T09:05:00Z", "lastTurnTime": "2025-09-24T10:15:00Z", "turnCount": 7 }` |

An example of a memory data item would look like: 
```json
{
  "id": "thread-1234",
  "threadId": "thread-1234",
  "turns": [
    {
      "turnIndex": 0,
      "speaker": "user",
      "content": "...",
      "timestamp": "2025-09-24T10:15:00Z",
    },
    {
      "turnIndex": 1,
      "speaker": "agent",
      "content": "...",
      "timestamp": "2025-09-24T10:15:00Z",
    },
  ],
  "LastUpdatedtimestamp": "2025-09-24T10:15:00Z",
  "summary": "...", // optional summary of the turns in this thread
  "embedding": [ … ],      // optional embedding of the summary / compressed memory
}
```

**Pros**
- All memory for a thread is in one logical document; simple to load in one read.
- Summary text of thread and keep thread information and vector embedding in one data item

**Cons**
- Requires client-side sorting after retrieval.
- Document size could grow large (Cosmos DB has a size limit per item, currently 2 MB for some APIs, though in NoSQL it can be more but you must consider RU cost and latency).
- Large document updates (writing appends) can incur higher RU charges.
- Vector search becomes coarser. In this pattern, we recommend summarizing the thread and storing a vector embedding for the summary. However, this can be expensive if the thread is frequently updated. 
- Harder to TTL individual turns; TTL applies at the document (thread) granularity.

> [!IMPORTANT]
> This model is typically not recommended unless the thread size has few turns, has infrequent updates, and retrieval patterns are simple (for example, retrieve the entire document all at once). Cosmos DB doesn't support sorting on nested objects/arrays, so sorting of last N messages would need to be implemented in application code. 


##### **Query Patterns**

**Retrieve the entire thread**
```sql
SELECT TOP @k *
FROM c
WHERE threadID = @threadID
```
Note: Cosmos DB query language doesn't support sorting by array/nested properties

**Retrieve thread by semantic search of the summary**
```sql
SELECT TOP @k c.content, c.timestamp, VECTOR_DISTANCE(c.embedding, @queryVector) AS dist
FROM c
    WHERE c.threadId = @threadId
ORDER BY VECTOR_DISTANCE(c.embedding, @queryVector)
```

# Next steps
- [Learn about vector indexing and search](vector-search-overview.md)
- [Learn about full text search](full-text-search-faq.md)
- [Learn about hybrid search](hybrid-search.md)
- [Learn about semantic caching](semantic-cache.md)
- [Build a multi-agent app with Azure Cosmos DB](https://aka.ms/CosmosDB/BankingAgentWorkshop)