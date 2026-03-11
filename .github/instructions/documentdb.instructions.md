---
description: Code review and content authoring guidelines for Azure DocumentDB documentation
applyTo: "articles/documentdb/**/*.md"
---

# Azure DocumentDB documentation guidelines

## Terminology

Product naming and branding rules for prose text in documentation.

### Product naming

| Correct | Incorrect |
| --- | --- |
| Azure DocumentDB | DocumentDB (for the managed service) |
| Azure DocumentDB | Azure Cosmos DB for MongoDB (vCore) |
| Azure DocumentDB | Cosmos DB for MongoDB vCore |
| Azure DocumentDB | vCore-based Azure Cosmos DB for MongoDB |

Always use "Azure DocumentDB" for the managed Azure service. Use "DocumentDB" (without "Azure") only when referring to the [open-source project](https://github.com/documentdb/documentdb).

### Exceptions

The following metadata fields are acceptable and should not be changed:

- `ms.service` and `ms.subservice` values - Microsoft Learn taxonomy values

## Content formatting

Code blocks, queries, and documentation structure guidelines.

### Content completeness

- Verify MongoDB shell commands and connection strings use correct Azure DocumentDB syntax
- Ensure cluster creation steps reference the correct Azure portal experience

### Code blocks

- Always specify the language identifier for syntax highlighting
- Use `javascript` or `typescript` for Node.js samples
- Use `azurecli` for Azure CLI commands
- Use `json` for configuration files and API responses

```javascript
// Correct: language identifier specified
const client = new MongoClient(connectionString);
```

## Technical review

Best practices to verify when reviewing content for technical accuracy.

### Connection and authentication

- Verify connection strings use the correct Azure DocumentDB format
- Ensure authentication examples show both connection string and Microsoft Entra ID options where applicable
- Prioritize Microsoft Entra ID authentication in examples, as connection string auth is not preferred
- Check that cluster tier references (M10, M30, etc.) are accurate for the documented features

### MongoDB compatibility

- Verify documented MongoDB features are supported by Azure DocumentDB
- Check that MongoDB driver version requirements are accurate
- Ensure aggregation pipeline examples use supported stages and operators

### Security

- Disable public network access and use private endpoints exclusively for production deployments
- Configure IP-based firewall rules when private endpoints aren't feasible (clusters are locked down by default)
- Use managed identities for Azure service-to-service authentication - avoid embedding credentials in code
- Separate Azure identities for control plane (cluster management) and data plane (data operations)
- Use Azure RBAC for control plane operations and native RBAC for data plane access

### High availability and replication

- Recommend enabling HA for production clusters (achieves 99.99% SLA)
- HA with cross-region replication achieves 99.995% SLA
- HA provides automatic failover with zero data loss - no manual intervention required
- In availability zone regions, HA provisions primary-standby pairs across zones
- Non-production clusters can disable HA to reduce costs
- Use cross-region replication for disaster recovery (active-passive configuration)
- Replica clusters can be promoted during regional outages
- Use replica clusters for read scaling to offload heavy read operations

### Indexing

- Always create indexes for queryable fields - absence of indexes forces expensive document scans
- Azure DocumentDB only indexes `_id` by default - all other fields must be explicitly indexed
- Avoid wildcard indexing unless query patterns are unpredictable
- For bulk data migrations, create indexes after data load to minimize write overhead
- Use nonblocking `createIndex` commands when indexing historical data on large clusters
- Create compound indexes for queries with predicates on multiple fields
- Track index build progress using `db.currentOp()`
- Enable large index keys for documents with deeply nested structures or long key values
- Use `{ "blocking": true }` option when indexes must complete before data writes begin
