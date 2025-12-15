---
title: Vercel Integration
titleSuffix: Azure Cosmos DB
description: Integrate web applications using the Vercel platform with Azure Cosmos DB for NOSQL or MongoDB as a data source.
author: sajeetharan
ms.author: sasinnat
ms.service: azure-cosmos-db
ms.topic: how-to
ms.date: 09/03/2025
ms.custom: sfi-image-nochange, sfi-ropc-blocked
appliesto:
  - ✅ NoSQL
  - ✅ MongoDB
---

# Vercel integration with Azure Cosmos DB

Vercel offers a user-friendly and robust platform for web application development and deployment. This new integration improves productivity as developers can now easily create Vercel applications with a backend database already configured. This Integration helps developers transform their creative ideas into reality in real-time.

## Getting started with Integrating Azure Cosmos DB with Vercel

This documentation is designed for developers seeking to effectively combine the robust capabilities of Azure Cosmos DB - a globally distributed, multi-model database service - with Vercel's high-performance deployment and hosting solution.

This integration enables developers to apply the benefits of a versatile and high-performance NoSQL database, while capitalizing on Vercel's serverless architecture and development platform.

There are two ways to integrate Azure Cosmos DB.

- [Vercel Integrations Marketplace](https://vercel.com/integrations/azurecosmosdb)
- Command Line

## Integrate Cosmos DB with Vercel via Integration Marketplace

Use this guide if you already know which Vercel projects to integrate or want to connect an existing Vercel project with Azure Cosmos DB.

## Prerequisites

- Vercel Account with Vercel Project – [Learn how to create a new Vercel Project](https://vercel.com/docs/concepts/projects/overview#creating-a-project)

- Azure Cosmos DB - [Quickstart: Create an Azure Cosmos DB account](nosql/quickstart-portal.md) or Create a free [Try Cosmos DB Account](https://aka.ms/trycosmosdbvercel)

- Some basic knowledge on Next.js, React, and TypeScript

## Steps for Integrating Azure Cosmos DB with Vercel

1. Select Vercel Projects for the Integration with Azure Cosmos DB. After you have the prerequisites ready, visit the Cosmos DB [integrations page on the Vercel marketplace](https://vercel.com/integrations/azurecosmosdb) and select Add Integration

    :::image type="content" source="media/vercel-integration/add-integration.png" alt-text="Screenshot shows the Azure Cosmos DB integration page on Vercel's marketplace." lightbox="media/vercel-integration/add-integration.png":::

1. Choose All projects or Specific projects for the integration. In this guide, we proceed by choosing specific projects. Select Install to continue. 

    :::image type="content" source="media/vercel-integration/continue.png" alt-text="Screenshot shows how to select vercel projects." lightbox="media/vercel-integration/continue.png":::

1. Sign in to your existing Microsoft account, or if you don’t have one, create a new account as depicted in next step.

    :::image type="content" source="media/vercel-integration/sign-in.png" alt-text="Screenshot shows how to sign-in to Azure account." lightbox="media/vercel-integration/sign-in.png":::

1. Select 'create one' to create a new Microsoft account.

    > [!NOTE]
    > A Microsoft account is different from an Azure Cosmos DB account. We're creating an Azure Cosmos DB account in the following steps.

    :::image type="content" source="media/vercel-integration/create-new.png" alt-text="Screenshot shows how to create new Microsoft Account." lightbox="media/vercel-integration/create-new.png":::

1. If you want to use an existing Azure Cosmos DB account, choose the existing Directory, subscription and the Azure Cosmos DB Account, and then skip to step 9. To create a new Azure Try Cosmos DB account, select **Create new account**.
 
    :::image type="content" source="media/vercel-integration/create-new-azure-cosmosdb.png" alt-text="Screenshot shows how to create new Azure Try Cosmos DB Account." lightbox="media/vercel-integration/create-new-azure-cosmosdb.png":::

1. Select API type (currently only NOSQL and MongoDB API are supported) and Select **Create Account**.

    :::image type="content" source="media/vercel-integration/select-api.png" alt-text="Screenshot shows how to select the type of API of the Azure Cosmos DB account." lightbox="media/vercel-integration/select-api.png":::

1.	After the successful Try Azure Cosmos DB account creation, Select **Continue**.

    :::image type="content" source="media/vercel-integration/account-continue.png" alt-text="Screenshot shows how to continue with the integration." lightbox="media/vercel-integration/account-continue.png":::

1. Select **Accept** in the pop-up to access the Try Azure Cosmos DB account.

    :::image type="content" source="media/vercel-integration/accept.png" alt-text="Screenshot shows how to accept the access." lightbox="media/vercel-integration/accept.png":::

1. Select Integrate and you're done.

    :::image type="content" source="media/vercel-integration/integrate-new.png" alt-text="Screenshot shows how to confirm the integration." lightbox="media/vercel-integration/integrate-new.png":::

## Integrate Cosmos DB with Vercel via npm & Command Line

1. Execute create-next-app with npm, yarn, or pnpm to bootstrap the example:
    
    ```bash
    npx create-next-app --example with-azure-cosmos with-azure-cosmos-app
    
    yarn create next-app --example with-azure-cosmos with-azure-cosmos-app
    
    pnpm create next-app --example with-azure-cosmos with-azure-cosmos-app
    ```

1. Modify pages/index.tsx to add your code. Make changes to pages/index.tsx according to your needs. You could check out the code at **lib/cosmosdb.ts** to see how the `@azure/cosmos` JavaScript client is initialized.

1. Push the changes to a GitHub repository.

### Set up environment variables

- `COSMOSDB_CONNECTION_STRING` - You need your Cosmos DB connection string. You can find this credential in the Azure portal in the **Keys** section.

- `COSMOSDB_DATABASE_NAME` - Name of the database you plan to use. This value should already exist in the Azure Cosmos DB account.

- `COSMOSDB_CONTAINER_NAME` - Name of the container you plan to use. This value should already exist in the previous database.

## Integrate Cosmos DB with Vercel using marketplace template

We have an [Azure Cosmos DB Next.js Starter](https://aka.ms/azurecosmosdb-vercel-template), which a great ready-to-use template with guided structure and configuration, saving you time and effort in setting up the initial project setup. Select Deploy to Deploy on Vercel and View Repo to view the [source code](https://github.com/Azure/azurecosmosdb-vercel-starter).

1. Choose the GitHub repository, where you want to clone the starter repo.
    :::image type="content" source="media/vercel-integration/create-git-repository.png" alt-text="Screenshot to create the repository." lightbox="media/vercel-integration/create-git-repository.png":::

1. Select the integration to set up Cosmos DB connection keys, these steps are described in detail in previous section.

    :::image type="content" source="media/vercel-integration/add-integrations.png" alt-text="Screenshot shows the required permissions." lightbox="media/vercel-integration/add-integrations.png":::

1. Set the environment variables for the database name and container name, and finally select Deploy

    :::image type="content" source="media/vercel-integration/configure-project.png" alt-text="Screenshot shows the required variables to establish the connection with Azure Cosmos DB." lightbox="media/vercel-integration/configure-project.png":::

1. Upon successful completion, the completion page would contain the link to the deployed app, or you go to the Vercel project's dashboard to get the link of your app. Now your app is successfully deployed to vercel.

## Next steps

- To learn more about Azure Cosmos DB, see [Welcome to Azure Cosmos DB](introduction.md).
- Create a new [Vercel project](https://vercel.com/dashboard).
