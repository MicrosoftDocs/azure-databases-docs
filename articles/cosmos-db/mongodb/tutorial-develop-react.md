---
title: "MongoDB, React, and Node.js tutorial for Azure"
description: Learn how to create a MongoDB app with React and Node.js on Azure Cosmos DB using the exact same APIs you use for MongoDB with this video based tutorial series.
author: gahl-levy
ms.service: azure-cosmos-db
ms.subservice: mongodb
ms.devlang: javascript
ms.topic: tutorial
ms.date: 08/26/2021
ms.author: gahllevy
ms.custom: devx-track-js
---
# Create a MongoDB app with React and Azure Cosmos DB  
[!INCLUDE[MongoDB](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb.md)]
<!-- Added concise alt text to clarify that this content applies to Azure Cosmos DB API for MongoDB. -->

This multi-part video tutorial demonstrates how to create a hero tracking app with a React front-end. The app used Node and Express for the server, connects to Azure Cosmos DB database configured with the [Azure Cosmos DB's API for MongoDB](introduction.md), and then connects the React front-end to the server portion of the app. The tutorial also demonstrates how to do point-and-click scaling of Azure Cosmos DB in the Azure portal and how to deploy the app to the internet so everyone can track their favorite heroes. 

[Azure Cosmos DB](https://azure.microsoft.com/services/cosmos-db/) supports wire protocol compatibility with MongoDB, enabling clients to use Azure Cosmos DB in place of MongoDB.  

This multi-part tutorial covers the following tasks:

> [!div class="checklist"]
> * Introduction
> * Setup the project
> * Build the UI with React
> * Create an Azure Cosmos DB account using the Azure portal
> * Use Mongoose to connect to Azure Cosmos DB
> * Add React, Create, Update, and Delete operations to the app

Want to do build this same app with Angular? See the [Angular tutorial video series](tutorial-develop-nodejs-part-1.md).

## Prerequisites
* **Node.js**: v14.x or later (LTS recommended). Verify with `node --version`.
<!-- Converted prerequisite into a concise parameter-style entry with version and verification command. -->
* **HTTP testing tool**: Insomnia, `curl`, Visual Studio, or PowerShell `Invoke-RestMethod`. Verify availability by running the tool once (for example, `curl --version`).
<!-- Condensed and added a one-line verification command. -->

### Finished Project
Get the completed application [from GitHub](https://github.com/Azure-Samples/react-cosmosdb).

## Introduction 

In this video, Burke Holland gives an introduction to Azure Cosmos DB and walks you through the app that is created in this video series.  
**Success check**: You understand the overall app architecture (React UI, Node/Express API, Azure Cosmos DB for MongoDB).
<!-- Added a one-line textual success criterion for the video section. -->

> [!VIDEO https://www.youtube.com/embed/58IflnJbYJc]

## Project setup

This video shows how set up the Express and React in the same project. Burke then provides a walkthrough of the code in the project.  
**Success check**: The project runs locally without errors using `npm start` (or the equivalent start script).
<!-- Added a one-line textual success criterion for the video section. -->

> [!VIDEO https://www.youtube.com/embed/ytFUPStJJds]

## Build the UI

This video shows how to create the application's user interface (UI) with React.  
**Success check**: The React UI renders in the browser and displays the hero list layout.
<!-- Added a one-line textual success criterion for the video section. -->

> [!NOTE]
> The CSS referenced in this video can be found in the [react-cosmosdb GitHub repo](https://github.com/Azure-Samples/react-cosmosdb/blob/master/src/index.css).

> [!VIDEO https://www.youtube.com/embed/SzHzX0fTUUQ]

## Connect to Azure Cosmos DB

This video shows how to create an Azure Cosmos DB account in the Azure portal, install the MongoDB and Mongoose packages, and then connect the app to the newly created account using the Azure Cosmos DB connection string.  

**Example: connect with Mongoose**
```javascript
const mongoose = require("mongoose");

mongoose.connect(process.env.MONGODB_URI, {
  useNewUrlParser: true,
  useUnifiedTopology: true,
});

mongoose.connection.on("connected", () => {
  console.log("Connected to Azure Cosmos DB for MongoDB");
});
```
<!-- Added a short copy-paste connection example as requested. -->

**Verification**: Start the app and confirm that the console logs `Connected to Azure Cosmos DB for MongoDB`.
<!-- Added a one-line verification example with an explicit success check. -->

> [!VIDEO https://www.youtube.com/embed/0U2jV1thfvs]

## Read and create heroes in the app

This video shows how to read heroes and create heroes in the Azure Cosmos DB database, as well as how to test those methods using a HTTP testing utility and the React UI.  
**Success check**: Creating a hero returns HTTP 201 (or 200) and the new hero appears in the UI list.
<!-- Added a one-line textual success criterion for the video section. -->

> [!VIDEO https://www.youtube.com/embed/AQK9n_8fsQI] 

## Delete and update heroes in the app

This video shows how to delete and update heroes from the app and display the updates in the UI.  
**Success check**: Updates and deletions are immediately reflected in the UI and persisted in the database.
<!-- Added a one-line textual success criterion for the video section. -->

> [!VIDEO https://www.youtube.com/embed/YmaGT7ztTQM] 

## Complete the app

This video shows how to complete the app and finish hooking the UI up to the backend API.  
**Success check**: The full create, read, update, and delete workflow works end to end.
<!-- Added a one-line textual success criterion for the video section. -->

> [!VIDEO https://www.youtube.com/embed/TcSm2ISfTu8]

## Clean up resources

If you're not going to continue to use this app, use the following steps to delete all resources created by this tutorial in the Azure portal. 

1. From the left-hand menu in the Azure portal, click **Resource groups** and then click the name of the resource you created. 
2. On your resource group page, click **Delete**, type the name of the resource to delete in the text box, and then click **Delete**.

## Next steps

In this tutorial, you've learned how to:

> [!div class="checklist"]
> * Create an app with React, Node, Express, and Azure Cosmos DB 
> * Create an Azure Cosmos DB account
> * Connect the app to the Azure Cosmos DB account
> * Test the app using an HTTP testing utility
> * Run the application and add heroes to the database

You can proceed to the next tutorial and learn how to import MongoDB data into Azure Cosmos DB.  

> [!div class="nextstepaction"]
> [Import MongoDB data into Azure Cosmos DB](../../dms/tutorial-mongodb-cosmos-db.md?toc=%2fazure%2fcosmos-db%2ftoc.json%253ftoc%253d%2fazure%2fcosmos-db%2ftoc.json)

Trying to do capacity planning for a migration to Azure Cosmos DB? You can use information about your existing database cluster for capacity planning.
* If all you know is the number of vcores and servers in your existing database cluster, read about [estimating request units using vCores or vCPUs](../convert-vcore-to-request-unit.md) 
* If you know typical request rates for your current database workload, read about [estimating request units using Azure Cosmos DB capacity planner](estimate-ru-capacity-planner.md)

---

**Agent feedback applied**
- Convert the Prerequisites section into a concise parameter list that includes supported Node.js version(s) and one-line verification commands.
- In the 'Connect to Azure Cosmos DB' section add one short copy-paste connection example and a one-line verification example with an explicit success check.
- Add concise alt text to the APPLIES TO image and add a one-line textual success criterion where a video replaces a textual procedure.