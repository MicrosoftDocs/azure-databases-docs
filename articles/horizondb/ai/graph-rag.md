---
title: Graph-Augmented RAG Patterns with Azure HorizonDB
description: Learn how to combine knowledge graphs, vector search, and LLM reasoning in Azure HorizonDB to build more accurate retrieval-augmented generation (RAG) applications.
author: aditivgupta
ms.author: adig
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-database-postgresql
ms.subservice: ai-graph
ms.topic: concept-article
ms.collection:
  - ce-skilling-ai-copilot
ms.update-cycle: 180-days
ms.custom:
  - build-2026
# customer intent: As a user, I want to understand the basics of Graph-augmented RAG, when to use it, and how it works alongside vector and hybrid search to improve relevance.
---

# Graph-RAG patterns with Azure HorizonDB (preview)

Standard RAG (retrieval-augmented generation) retrieves context using vector similarity alone. Graph-RAG adds relationship-aware retrieval by combining vector search with knowledge graph traversal, improving accuracy for complex queries that depend on entity relationships, citations, causal chains, or multi-hop reasoning.

Azure HorizonDB lets you execute the full graph-RAG pipeline (vector search, semantic reranking, Cypher graph traversal, and result fusion) inside the database without moving data between systems.

## Why vector search alone isn't enough

Vector similarity retrieves documents that are semantically close to a query. This works well for simple factual lookups but breaks down when:

- The answer depends on **relationships between entities** (for example, "which services were affected by the API gateway outage?")
- The query requires **multi-hop reasoning** (for example, "which team resolved the issue that caused the payment failure?")
- The correct result is **structurally important but semantically distant** (for example, a legal precedent cited by 200 cases ranks low on embedding similarity but high on citation authority)
- Context requires **entity disambiguation** (for example, distinguishing "Mercury" the planet from "Mercury" the element from "Mercury" the Roman god)

In benchmarks with the U.S. Case Law dataset (500K cases), vector search alone achieves 40% recall. Adding graph-augmented retrieval with citation traversal raises recall to 70%, a 75% improvement.

## How graph-augmented RAG works

Graph-augmented RAG extends the standard RAG pipeline with a graph retrieval stage and a fusion step that combines results from multiple retrieval signals.

**Stage 1: Vector search.** Embed the user query and retrieve the top-N candidates by cosine similarity using pgvector with a DiskANN or HNSW index.

**Stage 2: Semantic reranking.** Pass the top-N candidates through `azure_ai.rank()` with a cross-encoder model (Cohere-rerank-v4.0-fast by default, deployed via Foundry) to rescore by deep semantic relevance. This reorders results that are close in embedding space but differ in actual relevance.

**Stage 3: Graph traversal.** Query the knowledge graph (Apache AGE) to find entities and documents connected to the query through relationships: citations, causal links, organizational hierarchy, or domain-specific edges. Graph retrieval surfaces structurally important results that vector search misses.

**Stage 4: Reciprocal Rank Fusion (RRF).** Combine rankings from semantic reranking and graph traversal using RRF scoring. This produces a final ranked list that balances semantic relevance with structural importance.

**Stage 5: LLM generation.** Pass the fused top-K results as context to the LLM for answer generation.

## When to use graph-augmented RAG

Graph-augmented RAG is most effective when your queries depend on relationships between entities. The following table helps you decide which retrieval approach fits your scenario.

| Use graph-augmented RAG when | Use vector-only RAG when |
| --- | --- |
| Answers depend on entity relationships (citations, causality, hierarchy) | Queries are simple factual lookups against document content |
| Multi-hop reasoning is required (A caused B, B affected C) | Single-hop semantic similarity is sufficient |
| Structural authority matters (heavily cited documents, central nodes) | All documents have equal structural weight |
| You need entity disambiguation across a large corpus | Entities are unambiguous in your domain |
| Accuracy improvement of 20-30% justifies graph construction cost | You need fast time-to-production with minimal infrastructure |

### Domain examples

| Domain | Graph structure | Graph-augmented retrieval value |
| --- | --- | --- |
| **Healthcare** | Patients connect to diagnoses, treatments, and outcomes (clinical pathway graph) | Surface treatment protocols through multi-hop patient pathway traversal |
| **Drug discovery** | Molecules interact with proteins (interaction graph) | Find drug candidates through multi-hop protein pathway traversal |
| **Cybersecurity** | Vulnerabilities chain to exploits to assets (attack graph) | Trace lateral movement paths and identify high-risk exposure chains |
| **Enterprise knowledge** | People belong to teams, teams own services, services have incidents | Answer organizational questions that span multiple entity types |
| **Content recommendation** | Users interact with content, content links to creators and genres (preference graph) | Discover content through collaborative graph paths beyond embedding similarity |

## Architecture patterns

These patterns describe how graph retrieval augments vector search at query time. Each uses a different strategy for combining graph and vector signals, leading to different query architectures and trade-offs. Patterns are composable: a single knowledge graph can support multiple retrieval strategies depending on the query type.

### Pattern 1: Authority boosting

Use graph structure to rescore vector search results. Documents that are heavily cited, centrally connected, or structurally important get a higher rank even if their embedding similarity is moderate.

**Pick this when:** Structural importance (citation count, link density) is a stronger relevance signal than semantic similarity alone.

**Example domains:** Legal research (citation authority), academic papers (h-index, citation chains), patent prior art (reference density).

```sql
-- Boost vector results by graph authority (in-degree count)
-- For large graphs, pre-compute citation_authority as a materialized view
-- and refresh on a schedule rather than computing per query.
WITH vector_hits AS (
    SELECT id, content, embedding <=> query_embedding AS distance
    FROM documents
    ORDER BY embedding <=> query_embedding
    LIMIT 60
),
citation_authority AS (
    SELECT (g.doc_id::text::int) AS doc_id, count(*) AS cite_count
    FROM ag_catalog.cypher('citation_graph', $$
        MATCH ()-[:CITES]->(target)
        RETURN target.doc_id
    $$) AS g(doc_id agtype)
    GROUP BY g.doc_id::text::int
)
SELECT v.id, v.content,
    1.0 / (60 + ROW_NUMBER() OVER (ORDER BY v.distance)) +
    1.0 / (60 + ROW_NUMBER() OVER (ORDER BY COALESCE(a.cite_count, 0) DESC)) AS rrf_score
FROM vector_hits v
LEFT JOIN citation_authority a ON v.id = a.doc_id
ORDER BY rrf_score DESC
LIMIT 10;
```

### Pattern 2: Context expansion

Use graph traversal to discover relevant documents that vector search misses entirely. Extract entities from the query, traverse their neighborhood in the graph, and add connected documents to the retrieval set before ranking.

**Pick this when:** The answer lives in documents that are structurally connected to the query entities but semantically distant (different vocabulary, different document type).

**Example domains:** Enterprise knowledge (org hierarchy + service ownership), drug discovery (protein interaction pathways), cybersecurity (attack chain traversal).

```sql
-- Expand retrieval set via entity graph neighborhood
WITH vector_hits AS (
    SELECT id, content FROM documents
    ORDER BY embedding <=> query_embedding
    LIMIT 30
),
graph_hits AS (
    SELECT DISTINCT d.id, d.content
    FROM ag_catalog.cypher('knowledge_graph', $$
        MATCH (e:Entity {name: $entity})-[*1..2]->(neighbor)
        MATCH (neighbor)-[:MENTIONED_IN]->(doc)
        RETURN doc.id
    $$, jsonb_build_object('entity', :query_entity)::text::agtype) AS g(doc_id agtype)
    JOIN documents d ON d.id = g.doc_id::text::int
),
combined AS (
    SELECT id, content FROM vector_hits
    UNION
    SELECT id, content FROM graph_hits
)
SELECT c.id, c.content,
    rank_result.relevance_score
FROM combined c
JOIN azure_ai.rank(
    :user_query,
    (SELECT array_agg(content) FROM combined),
    (SELECT array_agg(id::text) FROM combined)
) AS rank_result ON c.id = rank_result.document_id::int
ORDER BY rank_result.relevance_score DESC
LIMIT 10;
```

### Pattern 3: Graph filtering

Use graph relationships to constrain vector search results before or after retrieval. The graph acts as a boundary (access control, team ownership, categorization) rather than a scoring signal.

**Pick this when:** Graph relationships represent permissions, organizational scope, or domain boundaries that must be enforced, not just weighted.

**Example domains:** Multitenant knowledge bases (team ownership boundaries), compliance (jurisdiction filtering), content platforms (user access graphs).

```sql
-- Vector search filtered by graph-derived scope
SELECT d.id, d.content
FROM documents d
JOIN ag_catalog.cypher('org_graph', $$
    MATCH (team:Team {name: $team})-[:OWNS]->(service)
    RETURN service.name
$$, jsonb_build_object('team', :team_name)::text::agtype) AS owned(service_name agtype)
ON d.service = trim(both '"' from owned.service_name::text)
ORDER BY d.embedding <=> query_embedding
LIMIT 10;
```

### Pattern 4: Path-based retrieval

Use graph traversal as the primary retrieval mechanism. The query maps directly to a graph path pattern (causal chains, dependency walks, multi-hop relationships), and vector search plays a supporting role or is skipped entirely.

**Pick this when:** The query is explicitly relational ("what caused X", "who owns the service that failed", "trace the dependency chain from A to B") and the answer IS the path, not a document.

**Example domains:** Incident root cause analysis (failure chains), supply chain tracing (tier-N dependencies), regulatory impact analysis (regulation-to-control-to-system paths).

```sql
-- Path-based: trace failure chain then retrieve attached documents
WITH path_services AS (
    SELECT DISTINCT trim(both '"' from g.service_name::text) AS service_name
    FROM ag_catalog.cypher('infra_graph', $$
        MATCH (s:Service {name: $service})<-[:CAUSED_FAILURE_IN*1..4]-(upstream)
        RETURN upstream.name AS service_name
    $$, jsonb_build_object('service', :affected_service)::text::agtype)
    AS g(service_name agtype)
)
SELECT d.content, ps.service_name
FROM path_services ps
JOIN documents d ON d.service = ps.service_name;
```

## Graph construction approaches

The most common barrier to graph-augmented RAG is building the knowledge graph itself. Azure HorizonDB provides multiple paths depending on your data and requirements.

### Approach 1: LLM-powered construction (unstructured text)

The full LLM-powered construction pipeline involves three stages:

1. **Extract** - Call `azure_ai.extract()` on each document to pull entities and relationship triples as structured JSON.
1. **Deduplicate** - Use `azure_ai.generate()` to normalize entity names into canonical forms and map aliases (for example, "PostgreSQL", "Postgres", and "PG" resolve to one node).
1. **Load into graph** - Create nodes and edges in Apache AGE using the deduplicated entities, then add structural edges (temporal chains, hub nodes) to connect related clusters.

For a step-by-step walkthrough, see [Tutorial: Build a knowledge graph from unstructured text using AI Functions and Apache AGE](build-knowledge-graph.md).

Best for: Support tickets, research papers, contracts, incident reports, meeting notes.

### Approach 2: Schema-driven construction (structured data)

Transform existing relational tables into graph nodes and edges. If you already have foreign key relationships, you already have a graph, not queryable as one.

```sql
-- Create nodes from relational tables
DO $do$
DECLARE rec RECORD;
BEGIN
    FOR rec IN SELECT id, name FROM customers LOOP
        PERFORM * FROM ag_catalog.cypher('app_graph', $$
            CREATE (:Customer {id: $id, name: $name})
        $$, jsonb_build_object('id', rec.id, 'name', rec.name)::text::agtype)
        AS (v agtype);
    END LOOP;
END $do$;

-- Create edges from foreign key relationships
DO $do$
DECLARE rec RECORD;
BEGIN
    FOR rec IN SELECT id, customer_id FROM orders LOOP
        PERFORM * FROM ag_catalog.cypher('app_graph', $$
            MATCH (c:Customer {id: $customer_id}), (o:Order {id: $order_id})
            CREATE (c)-[:PLACED]->(o)
        $$, jsonb_build_object('customer_id', rec.customer_id, 'order_id', rec.id)::text::agtype)
        AS (e agtype);
    END LOOP;
END $do$;
```

Best for: CRM data, organizational hierarchies, product catalogs, ERP systems.

### Approach 3: Microsoft Research GraphRAG library

Use the open-source [Microsoft GraphRAG library](https://github.com/microsoft/graphrag) for automated graph construction with community detection and entity summarization.

Best for: Large document corpora where you need multi-level summarization and community-based retrieval.

## Performance considerations

| Factor | Recommendation |
| --- | --- |
| **Vector index choice** | Use DiskANN for datasets over 1M vectors. Use HNSW for smaller datasets or when you need faster index build times. |
| **Graph index strategy** | Create GIN indexes on frequently filtered node properties. Use composite indexes for traversals that filter on edge properties. |
| **Candidate set size** | Retrieve 60-100 vector candidates before reranking. Larger sets improve recall but increase latency. |
| **Graph traversal depth** | Limit variable-length paths to 3-4 hops. Deeper traversals increase latency exponentially. |
| **RRF constant** | The standard RRF constant of 60 works well for most use cases. Adjust if one signal consistently dominates. |
| **Connection pooling** | Use built-in PgBouncer (port 6432) for applications with many concurrent RAG queries. |

## Known limitations

- **Cypher language subset.** Apache AGE implements a subset of openCypher. Features such as `MERGE ... ON CREATE SET`, `EXISTS` subqueries, and `datetime()` aren't available. Use `CREATE` with deduplication logic or PL/pgSQL wrappers for conditional create patterns.
- **Graph maintenance is manual.** Knowledge graphs require updates when source data changes. There's no built-in change-data-capture mechanism for automatic graph sync. Use PostgreSQL triggers on source tables or schedule periodic re-extraction jobs.
- **Variable-length path performance.** Cypher traversals (`[*1..N]`) beyond 3-4 hops can produce exponential path expansion. Constrain hop depth and add property filters on intermediate nodes to prune early.
- **No cross-database graph queries.** A graph created in one database can't be queried from another database on the same server. Plan your schema so that graph data and vector data coexist in the same database.

## Solution accelerators

Get started quickly with prebuilt solution accelerators:

| Accelerator | Description | Link |
| --- | --- | --- |
| **GraphRAG Legal Research Copilot** | End-to-end graph-augmented RAG with U.S. Case Law (500K cases). Includes vector search, semantic ranking, AGE graph, and RRF fusion. | [GitHub repo](https://github.com/Azure-Samples/graphrag-legalcases-postgres) |
| **Contract Intelligence Platform** | Graph-based contract analysis with entity extraction, obligation tracking, and conflict detection across counterparties and regions. | [GitHub repo](https://github.com/james-tn/graph/tree/main/contract_intelligence) |
| **Build Your Own Advanced AI Copilot** | End-to-end copilot template combining graph retrieval, vector search, and LLM generation. | [GitHub repo](https://github.com/Azure-Samples/postgres-sa-byoac) |
| **GraphRAG + Docker + AI Agents** | Containerized GraphRAG deployment with AI agent integration for automated graph construction and retrieval. | [GitHub repo](https://github.com/Azure-Samples/postgreSQL-graphRAG-docker) |
| **Implement GraphRAG Lab** | Hands-on Microsoft Learn module walking through graph-augmented RAG implementation step by step. | [Microsoft Learn](https://aka.ms/mslearn-graphrag) |

## Related content

- [Graph database capabilities with Apache AGE extension](../graph/age-overview.md)
- [Tutorial: Build a knowledge graph from unstructured text using AI Functions and Apache AGE](build-knowledge-graph.md)
- [Implement vector search in Azure HorizonDB using the pgvector extension](vector-search-pgvector.md)
