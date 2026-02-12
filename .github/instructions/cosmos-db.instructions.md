---
description: Code review and content authoring guidelines for Azure Cosmos DB documentation
applyTo: "articles/cosmos-db/**/*.md"
---

# Azure Cosmos DB documentation guidelines

## Terminology

Product naming and branding rules for prose text in documentation.

### Product naming

| Correct | Incorrect |
| --- | --- |
| Azure Cosmos DB | Cosmos DB |
| Azure Cosmos DB | Azure Cosmos DB for NoSQL |
| Azure Cosmos DB | Cosmos DB for NoSQL |

Always use "Azure Cosmos DB" as the full product name in prose text.

### Exceptions

The following metadata fields are acceptable and should not be changed:

- `ms.service: azure-cosmos-db` - Microsoft Learn taxonomy value
- `ms.subservice: nosql` - Microsoft Learn taxonomy value
- `appliesto: ✅ NoSQL` - Standard documentation badge

## Content formatting

Code blocks, queries, and documentation structure guidelines.

### Content completeness

- Ensure account creation steps reference the correct Azure portal experience

### Code blocks

Use the appropriate fenced code block with the corresponding language identifier for SDK samples. Supported languages:

- `csharp` - .NET SDK
- `javascript` - Node.js SDK (JavaScript)
- `typescript` - Node.js SDK (TypeScript)
- `python` - Python SDK
- `java` - Java SDK
- `go` - Go SDK
- `rust` - Rust SDK

Example pattern:

````markdown
```csharp
using Microsoft.Azure.Cosmos;
CosmosClient client = new(endpoint, credential);
```
```

### Multi-language SDK samples

Use consecutive fenced code blocks with language identifiers for SDK samples. Supported languages:

Example pattern:

````markdown
```csharp
using Microsoft.Azure.Cosmos;
CosmosClient client = new(endpoint, credential);
```

```python
from azure.cosmos import CosmosClient
client = CosmosClient(endpoint, credential)
```

```javascript
const { CosmosClient } = require('@azure/cosmos');
const client = new CosmosClient({ endpoint, aadCredentials: credential });
```
````

### NoSQL queries

- Use `nosql` for Azure Cosmos DB query language
- Use `json` for query results or document examples

````markdown
```nosql
SELECT c.id, c.name FROM c WHERE c.status = "active"
```

```json
[
  { "id": "1", "name": "Example" }
]
```
````

### Azure CLI and infrastructure

- Use `azurecli` for Azure CLI commands
- Use `json` for ARM/Bicep output
- Use zone pivots (`zone_pivot_groups`) for portal/CLI/PowerShell/Bicep variations

## Technical review

Best practices to verify when reviewing content for technical accuracy.

### Data modeling

- Items must stay well under 2MB limit - flag content suggesting large documents or unbounded arrays
- Embed related data retrieved together - flag N+1 query patterns (multiple lookups for related data)
- Use type discriminators (`type` property) when storing multiple entity types in one container
- Reference data when items grow large - use separate documents for unbounded relationships (comments on posts)
- Version document schemas - include `schemaVersion` field for safe schema evolution

### Partition key design

- Plan for 20GB logical partition limit - flag partition keys that could accumulate unbounded data
- Choose high-cardinality keys - flag low-cardinality keys like `status`, `region`, or boolean fields
- Align partition key with query patterns - most frequent queries should be single-partition
- Consider hierarchical partition keys for multi-tenant scenarios
- Create synthetic partition keys when no single field works (combine fields)

Examples of problematic partition key choices:

| Problematic | Why | Better alternative |
| --- | --- | --- |
| `/status` | Only few values, creates hot partitions | `/customerId` or `/tenantId` |
| `/createdDate` | All current writes hit same partition | `/userId` with time-bucketing |
| `/region` | Uneven distribution, large countries become hot | `/customerId` |

### Query optimization

- Include partition key in WHERE clause - flag cross-partition queries without justification
- Project only needed fields - flag `SELECT *` in production code
- Use parameterized queries - flag string concatenation in query building
- Use continuation tokens for pagination - flag OFFSET/LIMIT for deep pagination
- Order filters by selectivity - most selective filters first in WHERE clause

```csharp
// Incorrect - vulnerable to injection, no query plan caching
var query = $"SELECT * FROM c WHERE c.id = '{userId}'";

// Correct - parameterized
var query = new QueryDefinition("SELECT c.id, c.name FROM c WHERE c.id = @id")
    .WithParameter("@id", userId);
```

### SDK usage

- CosmosClient must be singleton - flag creating new clients per request
- Use async APIs - flag `.Result` or `.Wait()` blocking calls
- Use Direct connection mode for production - Gateway mode adds latency
- Configure preferred regions for multi-region accounts
- Log diagnostics for slow or failed operations
- Handle 429 errors - verify retry configuration is documented

```csharp
// Incorrect - creates connection per request
public Order GetOrder(string id) {
    using var client = new CosmosClient(connectionString); // Wrong!
    // ...
}

// Correct - singleton via DI
public class OrderService {
    private readonly CosmosClient _client; // Injected singleton
    // ...
}
```
### Connection and authentication

- Verify connection strings use the correct Azure Cosmos DB format
- Ensure authentication examples show both connection string and Microsoft Entra ID options where applicable
- Prioritize Microsoft Entra ID authentication in examples, as connection string auth is not preferred

### Security

- Disable public network access and use private endpoints exclusively for production deployments
- Enable Network Security Perimeter (NSP) for additional network isolation boundaries
- Use managed identities for Azure service-to-service authentication - avoid embedding credentials in code
- Separate Azure identities for control plane (account management) and data plane (data operations)
- Use Azure RBAC for control plane operations and native RBAC for data plane access
- Enforce TLS 1.3 for transport security - use minimum TLS version configuration

### Indexing

- Exclude unused paths from indexing - reduces write RU cost by 20-80%
- Add composite indexes for multi-property ORDER BY - prevents query failures
- Verify indexing policy matches documented query patterns
- Use spatial indexes for geospatial queries

### Throughput and scaling

- Use autoscale for variable workloads - scales between 10-100% of max RU/s
- Consider serverless for dev/test environments - pay only for consumed RU
- Understand burst capacity - unused RU accumulates for short spikes
- Choose container vs database throughput based on isolation needs

### Global distribution

- Configure automatic failover for high availability
- Choose appropriate consistency level - Session is default and recommended for most scenarios
- Configure multi-region writes for globally distributed applications
- Enable zone redundancy for single-region high availability (99.995% SLA)

| Consistency level | Use case |
| --- | --- |
| Strong | Financial transactions, inventory management |
| Bounded staleness | Stock tickers, leaderboards |
| Session (default) | User sessions, shopping carts |
| Eventual | Analytics, non-critical reads |

### Change feed patterns

- Use change feed for materialized views - eliminates expensive cross-partition queries
- Implement event-driven architectures with change feed processor
- Use lease container to track processor progress

### Monitoring and diagnostics

- Track P99 latency, not just average - average hides tail latency issues affecting user experience
- Monitor RU consumption per operation - enables cost optimization and capacity planning
- Set up alerts for 429 throttling - indicates under-provisioned throughput
- Enable diagnostic logging (DataPlaneRequests, QueryRuntimeStatistics, PartitionKeyStatistics)
- Log SDK diagnostics for slow or failed operations - includes retry info, regions contacted, connection details
- Monitor normalized RU consumption - alert if sustained above 90%

### Local development with emulator

- Use Gateway connection mode with emulator - Direct mode has SSL certificate issues
- Import emulator SSL certificate for Java SDK - required for HTTPS connections
- Use well-known emulator key: `C2y6yDjf5/R+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw/Jw==`
- Override environment variables to avoid cloud connection conflicts - use `load_dotenv(override=True)` in Python or environment-specific config files

### SDK-specific requirements

Apply these checks only when reviewing articles with code samples in the corresponding language.

#### .NET SDK articles

When an article includes .NET/C# code samples using `Microsoft.Azure.Cosmos`:

- Verify the article includes a note about the explicit `Newtonsoft.Json` package dependency
- The SDK requires this package (version 13.0.3+) but doesn't install it automatically
- Flag .NET quickstarts or tutorials that don't include this prerequisite

Example note to include:

```markdown
> [!IMPORTANT]
> The `Microsoft.Azure.Cosmos` SDK requires an explicit reference to `Newtonsoft.Json` version 13.0.3 or higher. Add this package to your project using `dotnet add package Newtonsoft.Json`.
```

#### Java SDK articles

When an article includes Java code samples using `com.azure:azure-cosmos`:

- Verify Spring Boot version compatibility is documented:
  - Spring Boot 3.x requires Java 17+
  - Spring Boot 2.7.x works with Java 8, 11, or 17
- Flag Java quickstarts that don't mention Java version requirements
- For emulator usage: document that Gateway mode is required (Direct mode has SSL issues)

| Spring Boot | Minimum Java | Recommended |
| --- | --- | --- |
| 3.2.x, 3.1.x, 3.0.x | Java 17 | Java 17 or 21 |
| 2.7.x | Java 8 | Java 11 or 17 |
