---
title: Agent Memory in Azure Cosmos DB for NoSQL
titleSuffix: Azure Cosmos DB for NoSQL
description: Learn how to implement agent memories in Azure Cosmos DB for NoSQL. Discover design patterns, data models, and query strategies for storing short-term and long-term AI agent memory with vector and full-text search capabilities.
author: jcodella
ms.author: jacodel
ms.service: azure-cosmos-db
ms.topic: how-to
ms.date: 10/20/2025
appliesto:
  - ✅ NoSQL
ai-usage: ai-assisted
---

# Agent memories in Azure Cosmos DB for NoSQL

*Agent memory* refers to an AI agent's ability to persist and recall information from previous interactions. This capability is also called *AI memory*. Agent memory includes prior facts, interactions, and experiences. AI agents use this stored information to better reason, plan, and act over time. This article guides you through the most common patterns for storing and retrieving agent memories in your applications. It explains how each pattern works, highlights its strengths and limitations, and offers practical tips so you can confidently choose the right approach for your use cases.

## What Are Agent Memories?
 Agent memory is often divided into short-term (episodic or working) memory and long-term memory. This section explains the differences between each type.

### Short-Term Memory

Short-term memory holds recent context. For example, recent conversation turns, state information, results from tool or function calls. These values are all useful to the agent for the current task or thread. It can get deleted after some time (for example, using [time-to-live (TTL)](../time-to-live.md)), aggregated or summarized by thread, and classified as long-term memory. 

For example:
- In a conversational agent, the last 5–10 user or agent dialogue turns, including prompts, large language model (LLM) responses, tool call results, etc. 
- Intermediate states or partial task steps (for example retrieval of information from an API or tool call used in a subsequent step).

### Long-Term Memory

Long-term memory is more persistent and accumulates knowledge or patterns over multiple threads or conversations. It supports recall beyond immediate context. For example,
- User preferences (for example "User prefers responses in bullet lists", or "User is vegetarian").
- Historical summaries or reflections of short-term memories, or long threads. For example, "In this thread, the customer discussed their preferences for cotton socks and dislike of synthetic materials."

## Design patterns for agent memory storage

In the next section, we divide the discussion into four parts: In part one, we guide you through partition key selection, helping you choose a key that balances write and query throughput across partitions. In part two, we provide guidance on configuring a vector index for semantic search or a full-text index for text-based search, depending on your retrieval needs. Then, we explore data modeling patterns and their trade-offs. Finally, we cover query patterns that can be applied for different retrieval scenarios.

## Choose a partition key

Because Azure Cosmos DB automatically partitions your data, choosing a partition key is one of the most important design choices for your data model. The partition key determines how data distributes across logical and physical partitions. This distribution directly affects query performance, insert performance, scalability, and cost. Each partition key value maps to a distinct logical partition. A good partition strategy balances locality (keeping related items together for efficient queries) with distribution. In this guide, we highlight three common approaches. Read about [partitioning in Azure Cosmos DB for more detail.](../partitioning-overview.md)

Here are some common patterns and trade-offs when using Cosmos DB (or Cosmos-style NoSQL + vector features) to store agent memory.

### Use a GUID as the partition key

Each item gets its own unique partition key value, typically a GUID. This strategy maximizes write distribution and avoids the hot partition problem, because every write lands in a different logical partition. It's simple to implement and works well for write-heavy workloads without strong locality requirements. The tradeoff is that queries span logical and possibly physical partitions, which can be more expensive. This strategy can be useful for storing ephemeral AI agent turns where you care more about logging and long-term analytics than revisiting specific conversations.

- Example: A partition key `/pk` that takes on values like: "b9c5b6ce-2d9a-4a2b-9d76-0f5f9b2a9a91"

### Use a unique thread ID as the partition key

All items for a conversation share the same partition key equal to the thread (or thread) ID. This technique colocates turns and summaries, which makes "latest N," phrase filters, and other queries within a thread efficient. However, you must ensure there's enough workload distribution across threads to reduce likelihood of hot partitions. This approach works well for conversational agents and RAG applications. Most queries target a single conversation. Common queries include retrieving recent turns or performing vector search within one thread.

- Example: A partition key `/threadId` that takes on values like: "thread-1234"

### Use a tenant ID and thread ID as the partition key

You can use a two-level hierarchical partition key where the leading level is the tenant ID and the second is the thread ID. This technique preserves locality within a thread while grouping threads under a tenant for governance, quotas, and analytics. It also reduces cross-partition scans for tenant-level queries and enables safer multitenant isolation patterns. This technique is best for multitenant apps where each customer (tenant) runs many concurrent conversations and more isolation is needed.

- Example: A partition key `["/tenantId", "/threadId"]` takes on values like `tenantId = "contoso"`, `threadId = "thread-1234"`

## Indexes for semantic and full-text search

Azure Cosmos DB supports both vector indexing for semantic similarity search and full-text indexing for keyword-based retrieval, allowing you to choose the right search strategy based on your agent memory requirements.

### Configure a vector index

When you enable vector search in Azure Cosmos DB, you choose not only whether to shard but also which index type to use. Cosmos supports multiple vector-index algorithms, including `quantizedFlat` and `DiskANN`. The `quantizedFlat` index type is suited for smaller workloads or when you expect the number of vectors to remain modest (for example, tens of thousands of vectors total). It compresses (quantizes) each vector and performs an exact search over the compressed space, trading a slight accuracy loss for lower RU cost and faster scans. 

When your vector data scales up (for example, hundreds of thousands to billions of embeddings), `DiskANN` is the better choice. DiskANN implements approximate nearest-neighbor indexing and is optimized for high throughput, low latency, and cost efficiency at scale. It supports dynamic updates and achieves excellent recall across large datasets. Learn more about [vector indexes in Azure Cosmos DB](../vector-search.md#vector-indexing-policies).

If you're using DiskANN, you can decide whether to shard the vector index via the [vectorIndexShardKey](sharded-diskann.md). This decision lets you partition the DiskANN index based on an item property (for example, session, user, tenant), reducing the candidate search space and making semantic queries more efficient and focused. For example, you can shard by a tenant, userid, or both. In multitenant systems, isolating the vector index per tenant ensures that search on a particular tenant or user data is fast and efficient. Using the multitenant example from the section on [partitioning](#choose-a-partition-key), you can set the vectorIndexShardKey and the partition key to be the same, or just the first level of your hierarchical partition key. 

Using a global (nonsharded) index offers simplicity and the ability to search on the entire set of vectors. Both of these options allow you to further refine the search using `WHERE` clause filters as with any other query. 

### Configure a full text index

Azure Cosmos DB's full text search capability enables advanced text-based queries over your memory items, making it ideal for keyword and phrase-based retrieval scenarios. When you enable full text indexing on specific paths in your container (such as `/content`), Azure Cosmos DB automatically applies linguistic processing including tokenization, stemming, and case normalization. This feature allows queries to match variations of words (for example, "running" matches "run," "runs," "ran") and improves recall for natural language searches.

Full text indexes are valuable for agent memory workloads where you need to retrieve conversations based on specific subjects, entities, or phrases mentioned by users or agents. For instance, you can quickly find all turns where "refund policy" or "billing issues" are discussed, regardless of the exact phrasing. Unlike vector search, which finds semantically similar content, full text search provides precise lexical matching with linguistic intelligence. Azure Cosmos DB uses BM25 (Best Match 25), a statistical ranking function that scores items based on term frequency and item length normalization, ensuring that the most relevant results are surfaced first. You can combine full text search with vector search in hybrid queries to apply both BM25 scoring for keyword relevance and vector similarity for semantic meaning. Learn more about [full text search in Azure Cosmos DB](full-text-search.md).

## Recommended data model: One document per turn

This is the recommended data model for storing chat histories and agent memories in Azure Cosmos DB. Each item represents a complete back-and-forth exchange (or turn) between two entities in a conversation thread, for example, a user prompt and the agent’s response, or an agent’s call to a tool and the resulting output. Each item serves as a natural unit of memory that can be stored, queried, vectorized, and expired as a single entity. This structure makes it efficient to retrieve context for a single exchange or recent history, perform vector or keyword search at either the exchange or per-message level, and maintain balanced item size with manageable storage costs.

> [!NOTE]
> This model is the most common for both single and multi-agent apps. It provides a good balance between small item size and the utility or value of information included in a single memory item.

#### Example scenarios

- An agent chat application where each turn consists of the user's question and the agent's reply, and you frequently need to resurface entire question and answer pairs for context injection.
- A planning agent that queries an external API (tool) and logs both the request and tool response as one memory unit. This scenario allows downstream queries to recall the whole exchange.
- Applications that use the memories as part of a [semantic cache](semantic-cache.md). This approach can reduce latency, token consumption, and LLM-based costs.
    
#### Data item properties

| Property | Type | Required | Description | Example |
| --------------- | ----------------- | ------- | ----------- | ----------- |
| `id` | string | ✅ | Partition key. For more information, see [choosing a partition key](#choose-a-partition-key) | `"b9c5b6ce-2d9a-4a2b-9d76-0f5f9b2a9a91"` or `tenant-001`  |
| `threadId` | string | ✅ | Thread / conversation identifier (commonly the partition key). | `"thread-1234"` |
| `turnIndex` | number (int) | ✅ | Monotonic counter of the *exchange* (0-based or 1-based). | `7` |
| `messages` | object | ✅ | Messages that make up this exchange (for example, user prompt, agent reply, optional tool call/response). | For more information, see [`messages` properties](#properties-of-messages-object). |
| `turnEmbedding` | number[] | optional | Vector for the *whole* exchange (for example, embedding of a concatenated or summarized message pair). | `[0.013, -0.092, ]` |
| `embedding` | number[] | optional | Vector for this specific turn (You can create embedding of user question for a [semantic cache](semantic-cache.md)). | `[0.11, 0.02, ]` |

#### Properties of `messages` object

| Property | Type | Required | Description | Example |
| --------------- | ----------------- | ------- | ----------- | ----------- |
| `role` | string | ✅ | Origin of the message. Typical: `"user"`, `"agent"`, `"tool"`. | `"agent"` |
| `entityId` | string | ✅ | Name or ID of the user, agent, tool, etc. that this message is associated with. | `"agent-assistant-01"` |
| `name` | string | ✅  | Tool/function name or agent persona label. | `"kb.search"` |
| `content` | string | ✅ | Text payload (prompt, reply, tool result snippet). | `"Refund policy is 30 days for unopened items."` |
| `timestamp` | string (ISO 8601) | optional | Message timestamp. | `"2025-09-24T10:14:27Z"` |
| `metadata` | object | optional | Per-message extras (for example, tokens, tool args/results identifiers). | `{ "tokens": 17 }` |

```json
{
  "id": "tenant-001",
  "threadId": "thread-1234",
  "turnIndex": 7,
  "entityId": "agent-assistant-01",
  "messages": [
    {
      "role": "user",
      "content": "What's our refund policy for accessories?",
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
  "embedding": [0.013, -0.092, 0.551, ],
  "metrics": { "latencyMs": 300 }
}
```

#### Advantages

- Good for longer threads/conversations. 
- Easy to get "latest N turns" by ordering on turnIndex or timestamp.
- Supports embedding-per-turn for vector similarity queries within the thread and [semantic caching](semantic-cache.md).
- Easy to TTL (expire) older memories if needed.
- Smaller items per turn don't require potentially expensive updates.

#### Limitations

- When summarizing or consolidating, you might want to generate "summary turns."
- You might need to periodically prune or compact older turns.

## Alternative data models
These alternative data models can also be used for storing chat histories and agent memories, depending on your application’s requirements. However, each comes with trade-offs in storage efficiency, retrieval complexity, and overall cost. While the turn-based model is generally preferred, the following options are provided for completeness and to help you evaluate different design choices based on your scenario.

### One response per item

In this design, every agent or user interaction (that is "turn") is stored as its own item in Azure Cosmos DB. All turn items for a single thread or thread carry the same `threadId`, which acts as a logical link between other turns in the same thread. This pattern is useful for fine-grained retrieval, analytics, or vector similarity search on every single utterance.

#### Example scenarios

- A conversational agent where embeddings are created for every user and agent message, enabling per-utterance semantic search within a thread.
- Analytics dashboards that measure agent vs. user token counts, sentiment, or latency at the per-message level.
- RAG (retrieval-augmented generation) flows that need to embed and search every response independently (for example "find the most relevant past statement across all threads").

#### Data item properties

| Property | Type | Required | Description | Example |
| --------------- | ----------------- | ------- | ----------- | ----------- |
| `id` | string | ✅ | Partition key. For more information, see [choosing a partition key](#choose-a-partition-key) | `"b9c5b6ce-2d9a-4a2b-9d76-0f5f9b2a9a91"` or `tenant-001`  |
| `threadId` | string | ✅ | Identifier for the conversation/thread. Often chosen as the **partition key** so all turns for a thread are colocated and efficiently queried. In multitenant apps, consider hierarchical primary keys like `/tenantId`, `/threadId`. | `"thread-1234"` |
| `turnIndex` | number (int) | ✅ | Monotonic turn counter (0,1,2…). Use with `threadId` to sort/fetch latest N turns. | `3` |
| `entityId` | string | ✅ | Name or ID of the user, agent, tool, etc. that this response is associated with. | `"user-12345"` |
| `role` | string | ✅ | The role that produced the turn. Common values: `"user"`, `"agent"`, `"tool"` (or similar).  | `"agent"`   |
| `content`  | string | ✅ | Main text content for the turn (prompt, reply, tool result, etc.).  | `"This is one response from an LLM"` |
| `timestamp` | string (ISO 8601) | ✅ | Creation time for the turn (ISO 8601). Alternatively, you can sort by the system `_ts` (epoch seconds) without storing your own timestamp.  | `"2025-09-24T10:15:00Z"` |
| `embedding` | number[]  | optional | Vector embedding for `content` (or a summary). Must be a **top-level** field included in the container's vector policy/index to enable vector search. | `[0.017, -0.234, 0.561, ]`  |
| `metrics` | object | optional | Free-form metrics/attrs for the turn. Keep names machine-friendly (no spaces) for easier querying and indexing. | `{ "inputTokens": 25, "outputTokens": 8 }` |

An example of this memory data item would look like: 
```json
{
  "id": "tenant-001",
  "threadId": "thread-1234", 
  "turnIndex": 3, 
  "entityId": "agent-assistant-01",
  "role": "agent",
  "content": "This is one response from an LLM",
  "embedding": [-1.12402894028,  ],        
  "timestamp": "2025-09-24T10:15:00Z",
  "metrics": { "inputTokens": 12, "outputTokens": 8, "latencyMs": 177 },

}
```

#### Advantages

- Each memory is kept at an atomic/granular level.
- Easy to update/TTL individual responses. 
- Retrieving last N results can be done with a query with filter on the thread ID.

#### Limitations

- Vector embeddings only capture one response at a time. 
- Not keeping a complete turn in one data item (back-and-forth between agent and user or tool call) can limit utility of the memory without subsequent queries. 
- Not ideal model for [semantic caching](semantic-cache.md).

### One thread per item

Here, all the turns of a conversation (user, agent, tools, etc.) for a given thread or thread are aggregated into a single item. This item contains a list or array of turn entries (each with turnIndex, role, content, embedding, etc.), and optional summary fields, metadata, and a thread-level embedding. Because the entire thread is stored in one item, retrieving the full history (or a large window) becomes a single read. However, appending new turns requires updating (replacing) the item, which can become costly if the item grows large. This model can be useful when sessions are bounded in size or short-lived, and you prefer single-item reads to reconstruct context.

> [!IMPORTANT]
> This model is typically not recommended, as there's a risk to have long or unbounded threads, which can have high RU charges for CRUD operations on the item. 

#### Example scenarios

- Chatbots in customer onboarding or troubleshooting flows, where each thread is short (limited number of turns) and agents need to fetch the entire conversation quickly in one read.
- Conversation summarization services, where you run periodic batch jobs over full sessions to generate embeddings or summaries.

#### Data item properties

| Property  | Type | Required | Description | Example |
| ------------------ | ---------------- | ------- | ------------ | -------------- |
| `id` | string | ✅ | Partition key. For more information, see [choosing a partition key](#choose-a-partition-key) | `"b9c5b6ce-2d9a-4a2b-9d76-0f5f9b2a9a91"` or `tenant-001`  |
| `threadId` | string  | ✅ | Logical thread or thread identifier (often used as partition key). | `"thread-1234"`  |
| `turns` | array of objects | ✅ | A list of individual turn records (user or agent). Each turn contains a small structure. For example, index, role, content, etc. | `[ { "turnIndex": 0, "role": "user", "entityId": "user-12345", "content": "Hello" }, { "turnIndex": 1, "role": "agent", "entityId": "agent-assistant-01", "content": "Hi there!" } ]` |
| `embedding` | number[] | optional | Embedding vector computed over a summary or aggregation of the thread. Useful for semantic search over key points of the conversation.  | `[0.101, -0.231, 0.553, …]` |
| `summary`  | string  | optional | A textual "roll-up" or summary of the key points in the thread. | `"User wanted to schedule a meeting; agent fetched available times and confirmed A.M. slots."` |
| `metrics` | object  | optional | Key/value attributes or metrics about the thread. | `{ "startTime": "2025-09-24T09:05:00Z", "lastTurnTime": "2025-09-24T10:15:00Z", "turnCount": 7 }` |

An example of a memory data item would look like: 
```json
{
  "id": "tenant-001",
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
  "embedding": [  ]
}
```

#### Advantages

- All memory for a thread is in one logical item; simple to load in one read.
- Summary text of thread and keep thread information and vector embedding in one data item

#### Limitations

- Requires client-side sorting after retrieval.
- Item size could grow large (Cosmos DB has a size limit per item, currently 2 MB for some APIs, though in NoSQL it can be more but you must consider RU cost and latency).
- Large item updates (writing appends) can incur higher RU charges.
- Vector search becomes coarser. In this pattern, we recommend summarizing the thread and storing a vector embedding for the summary. However, this implementation can be expensive if the thread is frequently updated. 
- Harder to TTL individual turns; TTL applies at the item (thread) granularity.

## Query patterns for memory retrieval

This section demonstrates common retrieval query patterns for fetching agent memories from Azure Cosmos DB. Each pattern illustrates a different strategy for grounding the agent with the appropriate historical context.

### Retrieve most recent memories

When you want to reconstruct conversation context or show recent user/agent interactions, this query pattern is the simplest. It retrieves the last K messages in timestamp order, which is useful for feeding into chat context or displaying a conversation history. Use this pattern when freshness and chronological order matter.
```sql
SELECT TOP @k c.content, c.timestamp
FROM c
WHERE c.threadId = @threadId
ORDER BY c.timestamp DESC
```

### Retrieve memories by semantic search

Semantic queries let you find turns whose embeddings are most similar to a given query vector, even if they don't share exact words. This pattern surfaces contextually relevant memories (answers, references, and hints) beyond recent messages. This pattern is useful when relevancy is important over recency. However, you can use a `WHERE` clause to filter to the most recent semantically similar results. 

```sql
SELECT TOP @k c.content, c.timestamp, VectorDistance(c.embedding, @queryVector) AS dist
FROM c
    WHERE c.threadId = @threadId
ORDER BY VectorDistance(c.embedding, @queryVector)
```

### Retrieve memories by hybrid search

Hybrid queries in Cosmos DB let you fuse vector similarity with keyword (full-text / BM25) scoring. This hybrid functionality enables you to return contextually relevant memories even when they don't share exact words, while still honoring textual precision via full-text terms.

```sql
SELECT TOP @k c.content, c.timestamp, VectorDistance(c.embedding, @queryVector) AS dist
FROM c
    WHERE c.threadId = @threadId
ORDER BY RANK RRF(VectorDistance(c.embedding, @queryVector), FullTextScore(c.content, @searchString))
```

### Retrieve memories that contain phrases or keywords

Keyword or phrase search is useful for filtering memories that explicitly mention a term (for example, "billing," "refund," "meeting") regardless of semantic closeness. This approach is helpful when you want strict matching or fallback to lexical recall. This approach can be extended for use in combination with semantic or recency queries to improve recall. 

```sql
SELECT TOP @k c.content, c.timestamp, 
FROM c
WHERE c.threadId = @threadId
  AND FULLTEXTCONTAINS(c.content, @phrase)
ORDER BY c.timestamp DESC
```

In the previous example, the `WHERE` clause is scoped to a specific thread using the sessionId (or ID). If instead you partition your data by tenantId, you can search across all threads for that tenant by querying on the tenant key. For example:

```sql
WHERE c.tenantId = "tenant-001"
```

## Related content

- [Learn about vector indexing and search](vector-search-overview.md)
- [Learn about full text search](full-text-search-faq.yml)
- [Learn about hybrid search](hybrid-search.md)
- [Learn about semantic caching](semantic-cache.md)
