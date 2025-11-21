---
title: Connect Azure Database for PostgreSQL to Azure AI Foundry Using MCP
description: Learn how to integrate Azure Database for PostgreSQL with Azure AI Foundry using Model Context Protocol (MCP) to enable AI agents to interact with your database through natural language queries.
author: abeomor
ms.author: abeomorogbe
ms.reviewer: maghan
ms.date: 11/18/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
ms.collection:
  - ce-skilling-ai-copilot
ms.update-cycle: 180-days
ms.custom:
  - ignite-2025
---

# Connect Azure Database for PostgreSQL to Azure AI Foundry with MCP

The Azure Database for PostgreSQL MCP (Model Context Protocol) server enables AI agents in Azure AI Foundry to interact with PostgreSQL databases through natural language queries. This integration supports SQL operations, vector search, schema discovery, and data analysis with enterprise-grade security.

This article shows you how to set up and configure the Azure PostgreSQL Server MCP with Azure AI Foundry agents for natural language database interactions.

## What is MCP and how does it work?

Model Context Protocol (MCP) is an open standard that enables AI applications to securely connect to external data sources and tools. The Azure PostgreSQL MCP Server acts as a bridge between Azure AI Foundry agents and your PostgreSQL database.

The system uses three main components:

- **Azure AI Foundry Agent** (Client): Authenticates to the Azure PostgreSQL MCP Server by using its managed identity
- **Azure PostgreSQL MCP Server** (Server): Runs in Azure Container Apps, using managed identity for PostgreSQL access  
- **PostgreSQL Database** (Target): Azure Database for PostgreSQL with Microsoft Entra ID authentication

This architecture ensures proper security isolation with separate managed identities for client authentication and database access.

## Features and capabilities

The Azure PostgreSQL MCP Server provides comprehensive database integration capabilities:

- **SQL Operations** - Execute queries and manage data. Perform analytics through natural language
- **Vector Search** - Use AI-powered embeddings for similarity search
- **Schema Discovery** - Automatic table and column analysis with relationship mapping
- **Enterprise Security** - Azure managed identity and Microsoft Entra ID authentication  
- **Natural Language** - Query databases by using conversational AI without SQL knowledge
- **Easy Deployment** - Easy Azure deployment with complete infrastructure setup

### Example use cases

With the MCP integration, your AI agents can handle queries like:

- "List all customers who placed orders in the last 30 days"
- "Show me the top five best-selling products by quantity"
- "What's the schema of the orders table?"
- "Calculate average order value by customer segment"
- "Find tables that contain customer information"

## Prerequisites

Before you begin, make sure you have the required tools, accounts, and permissions in place to deploy and configure the MCP PostgreSQL Server. Having these prerequisites ready minimizes interruptions and helps ensure a smooth integration with Azure AI Foundry.

- [Azure CLI](/cli/azure/install-azure-cli) (latest version)
- [Docker Desktop](https://www.docker.com/products/docker-desktop)
- [Azure Database for PostgreSQL Flexible Server](/azure/postgresql/flexible-server/overview) with Microsoft Entra ID authentication enabled
- [Azure AI Foundry project](/azure/ai-services/agents/quickstart?pivots=ai-foundry-portal)
- [Microsoft .NET](https://dotnet.microsoft.com/download)
- An Azure subscription with appropriate permissions to create resources

## Quick start deployment

Deploy the complete Azure MCP PostgreSQL Server infrastructure by using Azure Developer CLI (azd):

### Step 1: Deploy with azd up

The fastest way to get started is by using the automated deployment script. First, clone [the repo](https://github.com/Azure-Samples/azure-postgres-mcp-demo):

```bash
# Clone the repository
git clone https://github.com/Azure-Samples/azure-mcp-postgresql-server
cd azure-mcp-postgresql-server
```

Deploy the complete infrastructure with a single script. Before running the `azd up` command, set the [environment](/azure/developer/azure-developer-cli/manage-environment-variables?tabs=bash#set-environment-variables) variable to connect to the Postgres server you want to access from AI Foundry, and the AI Foundry resource you want to connect to.

Find your Azure Database for PostgreSQL subscription ID, resource group, and server name in your Azure portal:

:::image type="content" source="media/generative-ai-foundry-integration/azure-postgres-details.png" alt-text="Screenshot of Azure details page.":::

Find your Azure AI Foundry project name, subscription ID, and parent resource name in your Azure portal:

:::image type="content" source="media/generative-ai-foundry-integration/azure-foundry-details.png" alt-text="Screenshot of Azure AI Foundry details.":::

```bash
# Set environment variables for your existing PostgreSQL server
azd env set POSTGRES_RESOURCE_ID "/subscriptions/<subscription-id>/resourceGroups/<postgres-resource-group>/providers/Microsoft.DBforPostgreSQL/flexibleServers/<postgres-server-name>"

# Set environment variables for your AI Foundry project
azd env set AIF_PROJECT_RESOURCE_ID "/subscriptions/<subscription-id>/resourceGroups/<aifoundry-resource-group>/providers/Microsoft.CognitiveServices/accounts/<parent-resource-name>/projects/<aifoundry-project-name>"

# Deploy the infrastructure
azd up
```

This deployment creates:
- Azure Container Apps instance for the MCP server
- Managed Identity for secure authentication
- Microsoft Entra ID App Registration with proper Role-based access control (RBAC) configuration
- All necessary networking and security configurations

:::image type="content" source="media/generative-ai-foundry-integration/azure-portal-resources.png" alt-text="Screenshot of Azure resources." lightbox="media/generative-ai-foundry-integration/azure-portal-resources.png":::

### Step 2: Configure database access

After deployment completes, grant the MCP server access to your PostgreSQL database:

1. Connect to your PostgreSQL server using `psql` or your preferred PostgreSQL client:

   Set the following environment variables by copying and pasting the lines into your bash terminal (WSL, Azure Cloud Shell, etc.).

   ```bash
   export PGHOST=<your-database-host-name>
   export PGUSER=<your-admin-username>
   export PGPORT=5432
   export PGDATABASE=<your-database-name>
   export PGPASSWORD="$(az account get-access-token --resource https://ossrdbms-aad.database.windows.net --query accessToken --output tsv)" 
   ```

   Then run:

   ```bash
   psql
   ```

   Alternatively, you can connect via the [Connect and query a database with the PostgreSQL extension for Visual Studio Code](../extensions/vs-code-extension/quickstart-connect.md).

1. Create the database principal for the MCP server's managed identity:

   ```sql
   SELECT * FROM pgaadauth_create_principal('<ACA_MI_DISPLAY_NAME>', false, false);
   ```

   Replace `<ACA_MI_DISPLAY_NAME>` with the managed identity name from your deployment output (typically `azure-mcp-postgres-server`).

1. Grant appropriate permissions to the managed identity:

   ```sql
   -- Grant SELECT on a specific table
   GRANT SELECT ON TABLE_NAME TO "<ACA_MI_DISPLAY_NAME>";
   ```

   > [!TIP]  
   > Use `azd env get-values` to find the exact `ACA_MI_DISPLAY_NAME` value from your deployment.

## Configure Azure AI Foundry integration

After you deploy your MCP server, connect it to Azure AI Foundry:

### Connect via Azure AI Foundry portal

1. Go to your Azure AI Foundry project in the Azure portal.

1. Go to **Build** → **Create agent**.

1. In the tools section, select **+ Add**.

1. Select the **Custom** tab and choose **Model Context Protocol**.

   :::image type="content" source="media/generative-ai-foundry-integration/ai-foundry-ui-mcp-connect.png" alt-text="Screenshot of MCP connect.":::

1. Select **Microsoft Entra** → **Project Managed Identity** as the authentication method.

   :::image type="content" source="media/generative-ai-foundry-integration/ai-foundry-entra-connect.png" alt-text="Screenshot of Managed Identity page.":::

1. Enter your `ENTRA_APP_CLIENT_ID` as the audience (from your deployment output).

   > [!TIP]  
   > Use `azd env get-values` to find the `ENTRA_APP_CLIENT_ID` value.

1. Add instructions to your agent:

   ```text
   You are a helpful agent that can use MCP tools to assist users. Use the available MCP tools to answer questions and perform tasks.

   Use these parameters when calling PostgreSQL MCP tools:
   - database: <YOUR_DATABASE_NAME>
   - resource-group: <YOUR_RESOURCE_GROUP>
   - server: <YOUR_SERVER_NAME>
   - subscription: <YOUR_SUBSCRIPTION_ID>
   - user: <ACA_MI_DISPLAY_NAME>
   ```

### Test the integration

After you connect, test your MCP integration with natural language queries.

You can discover tables.

```copilot-prompt
List all tables in my PostgreSQL database
```

You can retrieve records with natural language.

```copilot-prompt
Show me the latest 10 records from the orders table
```

```copilot-prompt
Find customers who placed orders in the last 30 days
```

You can do vector search and specify example queries to improve accuracy.

```copilot-prompt
Do a vector search for "product for customer that love to hike"
```

This is an example of a vector search.

```sql
- `SELECT id, name, price, embedding <=> azure_openai.create_embeddings(
'text-embedding-3-small',
'query example'
)::vector AS similarity
FROM public.products
ORDER BY similarity
LIMIT 10;
```

The AI agent automatically translates these requests into appropriate database operations through the MCP server.

### Connect via Azure AI Foundry SDK

For programmatic access, use the following MCP configuration in your Python code:

```python
mcp_tool_config = {
    "type": "mcp",
    "server_url": "<MCP_SERVER_URL>",
    "server_label": "<MCP_SERVER_LABEL>",
    "server_authentication": {
        "type": "connection",
        "connection_name": "<CONNECTION_NAME>",
    }
}

mcp_tool_resources = {
    "mcp": [
        {
            "server_label": "<MCP_SERVER_LABEL>",
            "require_approval": "never"
        }
    ]
}
```

[Full SDK sample](https://github.com/Azure-Samples/azure-postgres-mcp-demo/blob/main/client/agents_mcp_sample.py) in the `client` folder in GitHub Repo.

## Security

When using the Azure MCP PostgreSQL Server, be aware of the following security considerations:

### Data access and exposure

- Connected AI agents can potentially access any data accessible to the MCP server
- The server can execute SQL queries on accessible databases and tables, however the MCP server is restricted to read only operations.
- Connected agents can request and receive data through natural language queries

### Security features

You can use the following [security features](../security/security-overview.md#access-control) to protect your data:

- **Managed Identity**: No credentials stored in container images.
- **Microsoft Entra ID Authentication**: Secure database authentication.
- **RBAC**: Role-based access control for database operations.
- **Row Level Security**: Fine-grained access control at the row level.

### Best practices

- **Grant database permissions ONLY to specific schemas and tables** needed for AI agents.
- Use principle of least privilege - don't grant broad database access.
- Regularly review and audit permissions granted to the MCP server's managed identity.
- Consider using dedicated databases or schemas for AI agent access.
- Start with a test database containing only nonsensitive sample data.

## Troubleshoot

If you encounter problems with the MCP PostgreSQL Server integration, this troubleshooting section helps you quickly identify root causes and remediate common issues. Begin with the health check and logs, then verify managed identity authentication, network connectivity, and database permission.

### Health check

Verify your MCP server status:

```bash
curl https://your-mcp-server.azurecontainerapps.io/health
```

### Limitations and considerations

**Authentication errors**
- Error: `Unauthorized` or `Forbidden`
- Solution: Verify managed identity configuration and PostgreSQL access permissions

**Connection issues**
- Error: `Connection timeout` or `Cannot connect to server`
- Solution: Check PostgreSQL firewall rules and network configuration

**Permission errors**
- Error: `Permission denied for relation`
- Solution: Grant appropriate permissions to the MCP server's managed identity:

```sql
GRANT SELECT ON my_table TO "<ACA_MI_DISPLAY_NAME>";
```

### Debug with logs

View Container Apps logs for troubleshooting:

```bash
# Stream logs
az containerapp logs tail --name your-mcp-server --resource-group your-resource-group

# Check deployment status
az containerapp show --name your-mcp-server --resource-group your-resource-group
```

## Related content

- [Azure MCP Server documentation](/azure/developer/azure-mcp-server/)
- [Model Context Protocol specification](https://spec.modelcontextprotocol.io/)
- [Azure AI Foundry documentation](/azure/ai-foundry/)
- [Azure Database for PostgreSQL integrations for AI applications](generative-ai-frameworks.md)
- [Azure AI extension in Azure Database for PostgreSQL](generative-ai-azure-overview.md)
- [Enable and use pgvector in Azure Database for PostgreSQL](../extension-module/how-to-use-pgvector.md)
