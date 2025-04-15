---
title: How to Connect from Azure Data Factory to Azure Database for PostgreSQL
description: Guide on how to connect an Azure Database for PostgreSQL flexible server from Azure Data Factory using the Azure Database for PostgreSQL connector
author: MitchellGale
ms.author: v-mgale
ms.reviewer: dabukhari, maghan
ms.date: 04/11/2025 
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
---

# Connect Azure Database for PostgreSQL to Azure Data Factory and Synapse Analytics

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

> [!IMPORTANT]
> The Azure Database for PostgreSQL version 2.0 provides an improved native Azure Database for PostgreSQL support. If you use the Azure Database for PostgreSQL version 1.0 in your solution, you should upgrade your Azure Database for PostgreSQL linked service at your earliest convenience.

## What is Azure Data Factory

[Azure Data Factory](/azure/data-factory/introduction) is a fully managed, serverless, data integration service built to orchestrate and operationalize complex hybrid extract-transform-load (ETL), extract-load-transform (ELT), and data integration projects. An Azure [integration runtime](/azure/data-factory/concepts-integration-runtime#azure-integration-runtime) supports connecting data stores and computing services with publicly accessible endpoints. If you enable the managed virtual network feature of an Azure integration runtime, it supports connecting to data stores using Azure Private Link service in private network environments.

Azure Data Factory offers an [Azure Database for PostgreSQL](/azure/data-factory/connector-azure-database-for-postgresql) connector with [support for various capabilities](/azure/data-factory/connector-azure-database-for-postgresql#supported-capabilities), depending on the integration runtime selected.

## Linked service

In Azure Data Factory, a [linked service](/azure/data-factory/concepts-linked-services) is a connection to a data source. When working with Azure Database for PostgreSQL, you can define a linked service using JSON to specify the connection details programmatically. This approach is useful for automation, version control, and deployment scenarios. The JSON definition includes properties such as the server name, database name, authentication type, and other connection parameters. By creating a linked service, you can easily connect to your Azure Database for PostgreSQL instance and perform data integration tasks within Azure Data Factory.

You can create a linked service using the Azure Data Factory UI or programmatically using JSON. The linked service allows you to connect to your Azure Database for PostgreSQL instance and perform data integration tasks within Azure Data Factory.

### Prerequisites

- An Azure Database for PostgreSQL flexible server instance. To learn more, go to [Create an Azure Database for PostgreSQL flexible server](/azure/postgresql/flexible-server/quickstart-create-server).
- (Optional) An Azure integration runtime [created within a managed virtual network](/azure/data-factory/managed-virtual-network-private-endpoint).

### Create a linked service via the Azure portal

You can create a linked service using the Azure Data Factory UI or programmatically using JSON. The linked service allows you to connect to your Azure Database for PostgreSQL instance and perform data integration tasks within Azure Data Factory.

1. Browse to the **Manage** tab in your Azure Data Factory or Synapse workspace and select **Linked Services**, then select **New**:

    #### [Azure Data Factory](#tab/data-factory)
    
    :::image type="content" source="media/how-to-connect-data-factory/new-linked-service.png" alt-text="Screenshot of Create a new linked service with Azure Data Factory UI." lightbox="media/how-to-connect-data-factory/new-linked-service.png":::
    
    #### [Azure Synapse](#tab/synapse-analytics)
    
    :::image type="content" source="media/how-to-connect-data-factory/new-linked-service-synapse.png" alt-text="Screenshot of Create a new linked service with Azure Synapse UI." lightbox="media/how-to-connect-data-factory/new-linked-service-synapse.png":::
    

1. From the linked services page, create a new linked service by selecting **+ New**. This opens a window with a list of all Azure Data Factory connectors. Search for **Azure Database for PostgreSQL**, select it, and then select **Continue**.

    :::image type="content" source="media/how-to-connect-data-factory/linked-service-search.png" alt-text="Screenshot of Searching for 'Azure Database for PostgreSQL' in new linked service field." lightbox="media/how-to-connect-data-factory/linked-service-search.png":::

1. Make sure that **Version 2.0** is selected.

    :::image type="content" source="media/how-to-connect-data-factory/linked-service.png" alt-text="Screenshot of New linked service window for Azure Database for PostgreSQL connector." lightbox="media/how-to-connect-data-factory/linked-service.png":::

#### Authentication

There are two supported methods for authentication: service principal and basic authentication.

##### Basic Authentication

1. Select **Basic auth** as the Authentication type and make sure to enter your Azure PostgreSQL flexible server connection details, including **Server name**, **Username**, and **Password**.

    :::image type="content" source="media/how-to-connect-data-factory/authentication-basic-auth.png" alt-text="Screenshot of a new linked service window for Azure Database for PostgreSQL connector with basic authentication type." lightbox="media/how-to-connect-data-factory/authentication-basic-auth.png":::

1. Select between **From Azure subscription** or **Enter manually** in **Account selection method**

    ###### [Azure subscription](#tab/from-azure-subscription)
    
    Select the **Azure subscription**, **Server name**, and **Database name**. Also, enter the **Port**.
    
    :::image type="content" source="media/how-to-connect-data-factory/authentication-account-selection-method.png" alt-text="Screenshot of Account selection method Azure subscription." lightbox="media/how-to-connect-data-factory/authentication-account-selection-method.png":::

    ###### [Enter manually](#tab/enter-manually)
    
    Enter the **Fully qualified domain name**, **Port**, and **Database name**.
    
    :::image type="content" source="media/how-to-connect-data-factory/authentication-username-password.png" alt-text="Screenshot of Account selection method Enter manually." lightbox="media/how-to-connect-data-factory/authentication-username-password.png":::

1. Enter the **Username** and **Password**.

:::image type="content" source="media/how-to-connect-data-factory/authentication-username-password.png" alt-text="Screenshot of Username and password." lightbox="media/how-to-connect-data-factory/authentication-username-password.png":::

##### Service principal authentication

Following the steps below requires setting up a linked service in Azure Data Factory or Synapse Analytics to connect to your Azure Database for PostgreSQL. This process involves selecting the appropriate authentication method, configuring connection details, and verifying the connection. Ensure you have the necessary prerequisites and permissions before proceeding.

1. [Register a Microsoft Entra app and create a service principal](/entra/identity-platform/howto-create-service-principal-portal).

1. Select **Service Principal** on Authentication type.

    There are two types of Service principal credential types, and both service principal methods require a **"Tenant"**, **"Service principal ID"**, and **"Azure Cloud Type"** values.

    :::image type="content" source="media/how-to-connect-data-factory/linked-service-authentication-service-principal.png" alt-text="Screenshot of New linked service window for Azure Database for PostgreSQL connector with service principal authentication type." lightbox="media/how-to-connect-data-factory/linked-service-authentication-service-principal.png":::

1. Select between **From Azure subscription** or **Enter manually** in **Account selection method**.

    ###### [Azure subscription](#tab/from-azure-subscription)
    
    Select the **Azure subscription**, **Server name**, and **Database name**. Also, enter the **Port**.
    
    :::image type="content" source="media/how-to-connect-data-factory/authentication-account-selection-method.png" alt-text="Screenshot of Account selection method Azure subscription." lightbox="media/how-to-connect-data-factory/authentication-account-selection-method.png":::

    ###### [Enter manually](#tab/enter-manually)
    
    Enter the **Fully qualified domain name**, **Port**, and **Database name**.
    
    :::image type="content" source="media/how-to-connect-data-factory/authentication-username-password.png" alt-text="Screenshot of Account selection method Enter manually." lightbox="media/how-to-connect-data-factory/authentication-username-password.png":::

1. Enter your **Service Principal Name**, also shown as the **Display Name** for your service principal key.

1. Select **Inline** in the **Authentication reference method**.

    :::image type="content" source="media/how-to-connect-data-factory/linked-service-authentication-service-principal-inline.png" alt-text="Screenshot of Service principal inline authentication reference method." lightbox="media/how-to-connect-data-factory/linked-service-authentication-service-principal-inline.png":::

1. Enter the **Tenant**. The tenant ID is in Azure, where the Service Principal Name was created.

    :::image type="content" source="media/how-to-connect-data-factory/azure-tenant-id.png" alt-text="Screenshot of Service principal tenant on Azure." lightbox="media/how-to-connect-data-factory/azure-tenant-id.png":::

1. Enter the **Service principal ID**. You can find the client ID in Azure, where the Service Principal Name was created.

    :::image type="content" source="media/how-to-connect-data-factory/azure-service-principal-id.png" alt-text="Screenshot of Service principal ID on Azure." lightbox="media/how-to-connect-data-factory/azure-service-principal-id.png":::

1. Select **Service Principal Certificate** or **Service Principal Key** in the **Service principal credential type**.

    ###### [Service Principal Certificate](#tab/service-principal-certificate)
    
    **Service principal certificate** authentication requires a **service principal certificate** and optionally a **service principal password**.
    
    :::image type="content" source="media/how-to-connect-data-factory/authentication-service-principal-certificate.png" alt-text="Screenshot of New linked service window for Azure Database for PostgreSQL connector with service principal certificate authentication type." lightbox="media/how-to-connect-data-factory/authentication-service-principal-certificate.png":::

    ###### [Service Principal Key](#tab/service-principal-key)
    
    **Service principal key** authentication requires a **service principal key**.
    
    The service principal key where the Service Principal Name was created is the **Value** under Client secrets.
    
    :::image type="content" source="media/how-to-connect-data-factory/service-principal-key.png" alt-text="Screenshot of Where to find the service principal key." lightbox="media/how-to-connect-data-factory/service-principal-key.png":::
    
    1. Fill **Service principal key** in Data Factory.
    
        :::image type="content" source="media/how-to-connect-data-factory/linked-service-authentication-service-principal-key.png" alt-text="Screenshot of New linked service window for Azure Database for PostgreSQL connector with service principal key authentication type." lightbox="media/how-to-connect-data-factory/linked-service-authentication-service-principal-key.png":::
    
1. Select your **Azure cloud type**.

1. Once all required connection fields are filled in, the bottom right-hand corner should display a **Test connection** button. The test connection button verifies that the linked service can connect to your Azure Database for PostgreSQL server.

    :::image type="content" source="media/how-to-connect-data-factory/linked-service-test-connection.png" alt-text="Screenshot of New linked service window for Azure Database for PostgreSQL connector test connection.":::

### Linked service JSON

The following table describes the properties of the linked service for Azure Database for PostgreSQL flexible server. The properties are defined in JSON format, which is used to create the linked service programmatically.

| Property | Description | Required |
| --- | --- | --- |
name | Name of the linked service. See [Naming rules](/azure/data-factory/naming-rules) |  Yes |
type | Type of the linked service. It should be **AzurePostgreSql** | Yes |
server | Full qualified host name for Azure database for PostgreSQL flexible server | Yes |
port | The Azure database for PostgreSQL flexible server port number | Yes |
database | Database name | Yes |
sslMode | A numeric value representing the SSL connection configuration. **0** for Disabled, **1** for Allow, **2** for Prefer, **3** for Require, **4** for VerifyCA and **5** for VerifyFull | Yes |
authenticationType | Specify the authentication to be used. **BasicAuth** or **ServicePrincipal** | Yes |
username | username for basic auth or Service principal name for service principal authentication | Yes |
password | Username password for the Basic Auth | Required when **BasicAuth**. Otherwise isn't required |
tenant | Tenant ID | Required for **ServicePrincipal** authentication type |
servicePrincipalId | Service Principal ID | Required for **ServicePrincipal** authentication type |
servicePrincipalCredentialType | Service Principal Type. **ServicePrincipalCert** or **ServicePrincipalKey**| Yes |
servicePrincipalEmbeddedCert | The service principal certificate | Required when **ServicePrincipalCert**. Otherwise isn't required |
servicePrincipalEmbeddedCertPassword | The service principal certificate password | No |
servicePrincipalKey | The service Principal key | Required if **ServicePrincipalKey** is the servicePrincipalCredentialType. Otherwise isn't required |

Depending on the type of authentication, different fields require a different JSON payload.

Here are JSON configuration examples for different authentication methods, including Basic Authentication, Service Principal Certificate, and Service Principal Key. These JSON templates can be customized to suit your specific requirements.

A linked service using **BasicAuth** is defined in JSON format as follows:

```json
{
    "name": "<Name of the linked service>",
    "properties": {
        "type": "AzurePostgreSql",
        "version": "2.0",
        "typeProperties": {
            "server": "<server host name>",
            "port": 5432,
            "database": "<database name>",
            "sslMode": 2,
            "username": "<Service Principal Name>",
            "authenticationType": "BasicAuth",
            "password": "<username password>"
        }
    }
}
```

A linked service using **Service Principal certificate** is defined in JSON format as follows:

```json
{
    "name": "<Name of the linked service>",
    "properties": {
        "type": "AzurePostgreSql",
        "version": "2.0",
        "typeProperties": {
            "server": "<server host name>",
            "port": 5432,
            "database": "<database name>",
            "sslMode": 2,
            "username": "<Service Principal Name>",
            "authenticationType": "ServicePrincipal",
            "tenant": "<Tenant ID>",
            "servicePrincipalId": "<SP ID>",
            "servicePrincipalCredentialType": "ServicePrincipalCert",
            "servicePrincipalEmbeddedCert": "<Embedded certificate>",
            "servicePrincipalEmbeddedCertPassword": "<Service Principal certificate password>"
        }
    }
}
```

A linked service using **Service Principal key** is defined in JSON format as follows:

```json
{
    "name": "<Name of the linked service>",
    "properties": {
        "type": "AzurePostgreSql",
        "version": "2.0",
        "typeProperties": {
            "server": "<server host name>",
            "port": 5432,
            "database": "<database name>",
            "sslMode": 2,
            "username": "<Service Principal Name>",
            "authenticationType": "ServicePrincipal",
            "tenant": "<Tenant ID>",
            "servicePrincipalId": "<SP ID>",
            "servicePrincipalCredentialType": "ServicePrincipalKey",
            "servicePrincipalKey": "<Service Principal Key>"
        }
    }
}
```

### Create linked services via API

Linked services can be created in the Azure Data Factory Portal via the [management hub](/azure/data-factory/author-management-hub) and any activities, datasets, or data flows that reference them.

You can create linked services by using one of these tools: [.NET API](/azure/data-factory/quickstart-create-data-factory-dot-net), [PowerShell](/azure/data-factory/quickstart-create-data-factory-powershell), [REST API](/azure/data-factory/quickstart-create-data-factory-rest-api), [Azure Resource Manager Template](/azure/data-factory/quickstart-create-data-factory-resource-manager-template), and [Azure portal](/azure/data-factory/quickstart-create-data-factory-portal).

When creating a linked service, the user needs appropriate authorization for the designated service. If sufficient access isn't granted, the user can't see the available resources and must use the manual entry option.

## Activities

Activities are tasks within a pipeline that can execute specific tasks. With script activity, users can run PostgreSQL scripts to query or modify their databases.

- Script Activity: [Transform data using the Script activity in Azure Data Factory or Synapse Analytics](/azure/data-factory/transform-data-using-script).

- Copy Activity: [Copy activity in Azure Data Factory and Azure Synapse Analytics](/azure/data-factory/copy-activity-overview).

- Lookup Activity: [Control flow lookup activity](/azure/data-factory/control-flow-lookup-activity).

## Related content

- [How to connect to data factory private endpoint](how-to-connect-data-factory-private-endpoint.md)
- [Networking with Private Link in Azure Database for PostgreSQL flexible server](concepts-networking-private-link.md)
