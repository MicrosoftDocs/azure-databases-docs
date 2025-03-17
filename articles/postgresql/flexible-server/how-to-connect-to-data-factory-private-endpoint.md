---
title: Connect from data factory via managed private endpoint
description: This article describes how to connect from Azure Data Factory to an instance of Azure Database for PostgreSQL flexible server using Private Link.
author: techlake
ms.author: hganten
ms.reviewer: maghan
ms.date: 02/05/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
---

# Connect from data factory via managed private endpoint

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

In this article, you create a linked service in Azure Data Factory to connect to an instance of Azure Database for PostgreSQL flexible server using a private endpoint.

[Azure Data Factory](/azure/data-factory/introduction) is a fully managed, serverless, data integration service built to orchestrate and operationalize complex hybrid extract-transform-load (ETL), extract-load-transform (ELT), and data integration projects. An Azure [integration runtime](/azure/data-factory/concepts-integration-runtime#azure-integration-runtime) supports connecting to data stores and compute services with public accessible endpoints. If you enable the managed virtual network feature of an Azure integration runtime, it supports connecting to data stores using Azure Private Link service in private network environments.

Data Factory offers an [Azure Database for PostgreSQL](/azure/data-factory/connector-azure-database-for-postgresql) connector with [support for various capabilities](/azure/data-factory/connector-azure-database-for-postgresql#supported-capabilities), depending on the integration runtime selected.

## Prerequisites

- An Azure Database for PostgreSQL flexible server instance with its network connectivity method configured as **Public access (allowed IP addresses)** so that you can create [private endpoints](../flexible-server/concepts-networking-private-link.md) to connect to it privately using Azure Private Link.
- An Azure integration runtime [created within a managed virtual network](/azure/data-factory/managed-virtual-network-private-endpoint).

## Create a private endpoint in Data Factory

Using the [Azure Database for PostgreSQL connector](/azure/data-factory/connector-azure-database-for-postgresql) you can connect to an instance of Azure Database for PostgreSQL flexible server routing all traffic privately, through a managed private endpoint.

You can create the managed private endpoint using the user interface provided for such purpose in the **Managed private endpoints** option, under the **Security** section of the **Manage** hub of [Azure Data Factory Studio](https://adf.azure.com), as described in [managed private endpoints](/azure/data-factory/managed-virtual-network-private-endpoint#managed-private-endpoints). As an alternative, you can use the corresponding Azure CLI command, [az datafactory managed-private-endpoint create](/cli/azure/datafactory/managed-private-endpoint), to create a managed private endpoint in Azure Data Factory.

After successfully deployed, the managed private endpoint shows like this in the **Managed private endpoints** page of [Azure Data Factory Studio](https://adf.azure.com):

:::image type="content" source="./media/how-to-connect-to-data-factory-private-endpoint/managed-private-endpoints-screen-provisioned.png" alt-text="Screenshot that presents the Managed private endpoints page in Azure Data Factory Studio showing a private endpoint, which is successfully provisioned and pending approval." lightbox="./media/how-to-connect-to-data-factory-private-endpoint/managed-private-endpoints-screen-provisioned.png":::

## Approve a private endpoint

After you deploy a private endpoint, you must approve it to permit incoming traffic through it. If you have access to the instance of Azure Data Factory and also have permissions to approve private endpoints created against the instance of Azure Database for PostgreSQL flexible server, you can use the **Managed private endpoints** page of [Azure Data Factory Studio](https://adf.azure.com), select the name of the managed private endpoint and, on the opening pane, select **Manage approvals in Azure portal**.

:::image type="content" source="./media/how-to-connect-to-data-factory-private-endpoint/managed-private-endpoints-screen-approval.png" alt-text="Screenshot that presents the Managed private endpoints page in Azure Data Factory Studio showing how to approve an endpoint." lightbox="./media/how-to-connect-to-data-factory-private-endpoint/managed-private-endpoints-screen-approval.png":::

The previous action takes you to the **Networking** page of the Azure Database for PostgreSQL flexible server to which the Azure Data Factory managed private endpoint is pointing.

If you don't have permissions to approve the private endpoint, ask someone with such permissions to approve the endpoint for you.

:::image type="content" source="./media/how-to-connect-to-data-factory-private-endpoint/managed-private-endpoints-screen-approving.png" alt-text="Screenshot that presents the Networking page of Azure Database for PostgreSQL Flexible Server showing how to approve a private endpoint." lightbox="./media/how-to-connect-to-data-factory-private-endpoint/managed-private-endpoints-screen-approving.png":::

It might take several minutes for the data factory to discover that the private endpoint is approved.

When the managed private endpoint is successfully deployed and approved, it shows like this in the **Managed private endpoints** page of [Azure Data Factory Studio](https://adf.azure.com):

:::image type="content" source="./media/how-to-connect-to-data-factory-private-endpoint/managed-private-endpoints-screen-approved.png" alt-text="Screenshot that presents the Managed private endpoints page in Azure Data Factory Studio showing successfully deployed and approved private endpoint." lightbox="./media/how-to-connect-to-data-factory-private-endpoint/managed-private-endpoints-screen-approved.png":::

## Add a linked service to connect to your Azure Database for PostgreSQL flexible server 

With the private endpoint deployed and approved, you can finally use the Azure Database for PostgreSQL connector in your data factory to create a linked service. Through that linked service you can connect to your instance of Azure Database for PostgreSQL flexible server.

1. In [Azure Data Factory Studio](https://adf.azure.com) select the **Manage** hub and, under the **Connections** section, select **Linked services**, and select **New** to create a new linked service:

   :::image type="content" source="./media/how-to-connect-to-data-factory-private-endpoint/data-factory-linked-service-create.png" alt-text="Screenshot that shows how to create a new linked service in Azure Data Factory." lightbox="./media/how-to-connect-to-data-factory-private-endpoint/data-factory-linked-service-create.png":::

1. Fill all required fields for the connector. Make sure that the integration runtime selected is the one on which you created the private endpoint in its managed virtual network. Also, make sure that the **Interactive authoring** feature is enabled on that integration runtime so that you can test the connection when all required information is provided.

   :::image type="content" source="./media/how-to-connect-to-data-factory-private-endpoint/data-factory-linked-service-create-postgresql-integration-runtime.png" alt-text="Screenshot that shows where to select integration runtime with managed virtual network." lightbox="./media/how-to-connect-to-data-factory-private-endpoint/data-factory-linked-service-create-postgresql-integration-runtime.png":::

1. Select an **Encryption method**. If you select **No encryption**, the connection only succeeds if the server parameter [require_secure_transport](server-parameters-table-tls.md?#require_secure_transport) is set to `off`, which isn't a recommended practice since it relaxes security.

   :::image type="content" source="./media/how-to-connect-to-data-factory-private-endpoint/data-factory-linked-service-create-postgresql-encryption-method.png" alt-text="Screenshot that shows options available for the encryption method field." lightbox="./media/how-to-connect-to-data-factory-private-endpoint/data-factory-linked-service-create-postgresql-encryption-method.png":::

1. Select **Test connection**. A **Connection successful** message should appear next to the **Test connection** button.

## Related content

- [Networking with Private Link in Azure Database for PostgreSQL flexible server](concepts-networking-private-link.md).
