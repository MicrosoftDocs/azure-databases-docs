---
title: Vercel integration with Azure Cosmos DB
description: Integrate web applications using the Vercel platform with Azure Cosmos DB for NOSQL or MongoDB as a data source.
author: sajeetharan
ms.author: sasinnat
ms.service: azure-cosmos-db
ms.topic: how-to
ms.date: 05/28/2023
ms.custom: sfi-image-nochange, sfi-ropc-blocked
---

# Vercel Integration with Azure Cosmos DB

[!INCLUDE[NoSQL, MongoDB](./includes/appliesto-nosql-mongodb.md)]

Vercel offers a user-friendly and robust platform for web application development and deployment. This new integration improves productivity as developers can now easily create Vercel applications with a backend database already configured. This Integration helps developers transform their creative ideas into reality in real-time.

## Getting started with Integrating Azure Cosmos DB with Vercel

This documentation is designed for developers seeking to effectively combine the robust capabilities of Azure Cosmos DB - a globally distributed, multi-model database service - with Vercel's high-performance deployment and hosting solution.

This integration enables developers to apply the benefits of a versatile and high-performance NoSQL database, while capitalizing on Vercel's serverless architecture and development platform.

There are two ways to integrate Azure Cosmos DB.

- [Via Vercel Integrations Marketplace](https://vercel.com/integrations/azurecosmosdb)
- Via Command Line

## Integrate Cosmos DB with Vercel via Integration Marketplace

Use this guide if you have already identified the Vercel projects or want to integrate an existing vercel project with

## Prerequisites

- Vercel Account with Vercel Project – [Learn how to create a new Vercel Project](https://vercel.com/docs/concepts/projects/overview#creating-a-project)

- Azure Cosmos DB - [Quickstart: Create an Azure Cosmos DB account](../cosmos-db/nosql/quickstart-portal.md) or Create a free [Try Cosmos DB Account](https://aka.ms/trycosmosdbvercel)

- Some basic knowledge on Next.js, React, and TypeScript

## Steps for Integrating Azure Cosmos DB with Vercel

1. Select Vercel Projects for the Integration with Azure Cosmos DB. After you have the prerequisites ready, visit the Cosmos DB [integrations page on the Vercel marketplace](https://vercel.com/integrations/azurecosmosdb) and select Add Integration

   :::image type="content" source="./media/integrations/vercel/add-integration.png" alt-text="Screenshot shows the Azure Cosmos DB integration page on Vercel's marketplace." lightbox="./media/integrations/vercel/add-integration.png":::

2. Choose All projects or Specific projects for the integration. In this guide we proceed by choosing specific projects. Select Install to continue. 

   :::image type="content" source="./media/integrations/vercel/continue.png" alt-text="Screenshot shows to select vercel projects." lightbox="./media/integrations/vercel/continue.png":::

3. Sign in to your existing Microsoft account, or if you don’t have one, create a new account as depicted in next step.

   :::image type="content" source="./media/integrations/vercel/sign-in.png" alt-text="Screenshot shows to log in to Azure account." lightbox="./media/integrations/vercel/sign-in.png":::

4. Click on 'create one' to create a new Microsoft account.
> [!NOTE]
> Microsoft account is different from an Azure Cosmos DB account. We will be creating an Azure Cosmos DB account in following steps
>
   :::image type="content" source="./media/integrations/vercel/create-new.png" alt-text="Screenshot shows to create new Microsoft Account." lightbox="./media/integrations/vercel/create-new.png":::

5. If you want to use an existing Azure Cosmos DB account, choose the existing Directory, subscription and the Azure Cosmos DB Account(Skip to step 9) . To create a new Azure Try Cosmos DB account, click on 'Create new account'.
 
   :::image type="content" source="./media/integrations/vercel/create-new-azure-cosmosdb.png" alt-text="Screenshot shows to create new Azure Try Cosmos DB Account." lightbox="./media/integrations/vercel/create-new-azure-cosmosdb.png":::

6. Select API type (currently only NOSQL and MongoDB API are supported) and click on 'Create Account'.

   :::image type="content" source="./media/integrations/vercel/select-api.png" alt-text="Screenshot shows to select the type of API of the Azure Cosmos DB account." lightbox="./media/integrations/vercel/select-api.png":::

7.	After the successful Try Azure Cosmos DB account creation, click on 'Continue'

   :::image type="content" source="./media/integrations/vercel/account-continue.png" alt-text="Screenshot shows to continue with the integration." lightbox="./media/integrations/vercel/account-continue.png":::

8. Click on 'Accept' in the pop-up to access the Try Azure Cosmos DB account. (Mandatory to complete the Integration). 

   :::image type="content" source="./media/integrations/vercel/accept.png" alt-text="Screenshot shows to accept the access." lightbox="./media/integrations/vercel/accept.png":::

9. Select Integrate and you're done.

   :::image type="content" source="./media/integrations/vercel/integrate-new.png" alt-text="Screenshot shows to confirm the integration." lightbox="./media/integrations/vercel/integrate-new.png":::

## Integrate Cosmos DB with Vercel via npm & Command Line

1. Execute create-next-app with npm, yarn, or pnpm to bootstrap the example:

   ```bash
   npx create-next-app --example with-azure-cosmos with-azure-cosmos-app

   yarn create next-app --example with-azure-cosmos with-azure-cosmos-app

   pnpm create next-app --example with-azure-cosmos with-azure-cosmos-app
   ```

2. Modify pages/index.tsx to add your code.

   Make changes to pages/index.tsx according to your needs. You could check out the code at **lib/cosmosdb.ts** to see how the `@azure/cosmos` JavaScript client is initialized.

3. Push the changes to a GitHub repository.

### Set up environment variables

- COSMOSDB_CONNECTION_STRING - You need your Cosmos DB connection string. You can find these in the Azure portal in the keys section.

- COSMOSDB_DATABASE_NAME - Name of the database you plan to use. This should already exist in the Azure Cosmos DB account.

- COSMOSDB_CONTAINER_NAME - Name of the container you plan to use. This should already exist in the previous database.

## Integrate Cosmos DB with Vercel using marketplace template

We have an [Azure Cosmos DB Next.js Starter](https://aka.ms/azurecosmosdb-vercel-template), which a great ready-to-use template with guided structure and configuration, saving you time and effort in setting up the initial project setup. Click on Deploy to Deploy on Vercel and View Repo to view the [source code](https://github.com/Azure/azurecosmosdb-vercel-starter).

1. Choose the GitHub repository, where you want to clone the starter repo.
   :::image type="content" source="./media/integrations/vercel/create-git-repository.png" alt-text="Screenshot to create the repository." lightbox="./media/integrations/vercel/create-git-repository.png":::

2. Select the integration to set up Cosmos DB connection keys, these steps are described in detail in previous section.

   :::image type="content" source="./media/integrations/vercel/add-integrations.png" alt-text="Screenshot shows the required permissions." lightbox="./media/integrations/vercel/add-integrations.png":::

3. Set the environment variables for the database name and container name, and finally select Deploy

   :::image type="content" source="./media/integrations/vercel/configure-project.png" alt-text="Screenshot shows the required variables to establish the connection with Azure Cosmos DB." lightbox="./media/integrations/vercel/configure-project.png":::

4. Upon successful completion, the completion page would contain the link to the deployed app, or you go to the Vercel project's dashboard to get the link of your app. Now your app is successfully deployed to vercel.

## Next steps

- To learn more about Azure Cosmos DB, see [Welcome to Azure Cosmos DB](../cosmos-db/introduction.md).
- Create a new [Vercel project](https://vercel.com/dashboard).
- Learn about [Try Cosmos DB and limits](../cosmos-db/try-free.md).
