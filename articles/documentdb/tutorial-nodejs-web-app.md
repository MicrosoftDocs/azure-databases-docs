---
title: |
  Tutorial: Build a Node.js web application
description: In this tutorial, create a Node.js web application that connects to a cluster in Azure DocumentDB and manages documents within a collection.
author: gahl-levy
ms.author: gahllevy
ms.topic: tutorial
ms.date: 10/17/2025
ms.custom:
  - devx-track-js
  - devx-track-azurecli
  - sfi-image-nochange
  - sfi-ropc-blocked
# Customer Intent: As a developer, I want to connect to Azure DocumentDB from my Node.js application, so I can build MERN stack applications.
---

# Tutorial: Connect a Node.js web app with Azure DocumentDB

In this tutorial, you build a Node.js web application that connects to Azure DocumentDB. The MongoDB, Express, React.js, Node.js (MERN) stack is a popular collection of technologies used to build many modern web applications. With Azure DocumentDB, you can build a new web application or migrate an existing application using MongoDB drivers that you're already familiar with. In this tutorial, you:

> [!div class="checklist"]
> - Set up your environment
> - Test the MERN application with a local MongoDB container
> - Test the MERN application with a cluster
> - Deploy the MERN application to Azure App Service

## Prerequisites

To complete this tutorial, you need the following resources:

[!INCLUDE[Prerequisite - Existing cluster](includes/prerequisite-existing-cluster.md)]

- A GitHub account with GitHub Codespaces entitlement

## Configure development environment

A development container environment is available with all dependencies required to complete every exercise in this project. You can run the development container in GitHub Codespaces or locally using Visual Studio Code.

### [GitHub Codespaces](#tab/github-browser)

GitHub Codespaces runs a development container managed by GitHub with Visual Studio Code for the Web as the user interface. For the most straightforward development environment, use GitHub Codespaces so that you have the correct developer tools and dependencies preinstalled to complete this training module.

> [!IMPORTANT]
> All GitHub accounts can use Codespaces for up to 60 hours free each month with two core instances.

1. Start the process to create a new GitHub Codespace on the `main` branch of the `azure-samples/msdocs-azure-cosmos-db-mongodb-mern-web-app` GitHub repository.

    [![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/Azure-Samples/msdocs-azure-cosmos-db-mongodb-mern-web-app?quickstart=1)

1. On the **Create codespace** page, review the codespace configuration settings, and then select **Create new codespace**

    :::image type="content" source="media/tutorial-nodejs-web-app/codespace-configuration.png" alt-text="Screenshot of the confirmation screen before creating a new codespace.":::

1. Wait for the codespace to start. This startup process can take a few minutes.

1. Open a new terminal in the codespace.

    > [!TIP]
    > You can use the main menu to navigate to the **Terminal** menu option and then select the **New Terminal** option.
    >
    > :::image type="content" source="media/tutorial-nodejs-web-app/open-terminal-option.png" lightbox="media/tutorial-nodejs-web-app/open-terminal-option.png" alt-text="Screenshot of the devcontainer menu option to open a new terminal.":::

1. Check the versions of the tools you use in this tutorial.

    ```console
    docker --version

    node --version

    npm --version

    az --version
    ```

    > [!NOTE]
    > This tutorial requires the following versions of each tool, which are preinstalled in your environment:
    >
    > | Tool | Version |
    > | --- | --- |
    > | Docker | &ge; 20.10.0 |
    > | Node.js | &ge; 18.0150 |
    > | npm | &ge; 9.5.0 |
    > | Azure CLI | &ge; 2.46.0 |
    >

1. Close the terminal.

1. The remaining steps in this tutorial take place in the context of this development container.

### [Visual Studio Code](#tab/visual-studio-code)

The **Dev Containers extension** for Visual Studio Code requires **Docker** to be installed on your local machine. The extension hosts the development container locally using the Docker host with the correct developer tools and dependencies preinstalled to complete this training module.

1. Open **Visual Studio Code** in the context of an empty directory.

1. Ensure that you have the **Dev Containers extension** installed in Visual Studio Code.

1. Open a new terminal in the editor.

    > [!TIP]
    > You can use the main menu to navigate to the **Terminal** menu option and then select the **New Terminal** option.
    >
    > :::image type="content" source="media/tutorial-nodejs-web-app/open-terminal-option.png" lightbox="media/tutorial-nodejs-web-app/open-terminal-option.png" alt-text="Screenshot of the menu option to open a new terminal.":::

1. Clone the `azure-samples/msdocs-azure-cosmos-db-mongodb-mern-web-app` GitHub repository into the current directory.

    ```bash
    git clone https://github.com/azure-samples/msdocs-azure-cosmos-db-mongodb-mern-web-app.git .
    ```

1. Open the **Command Palette**, search for the **Dev Containers** commands, and then select **Dev Containers: Reopen in Container**.

    :::image type="content" source="media/tutorial-nodejs-web-app/reopen-container-command-palette.png" alt-text="Screenshot of the Command Palette option to reopen the current folder within the context of a development container.":::

    > [!TIP]
    > Visual Studio Code might automatically prompt you to reopen the existing folder within a development container. This step is functionally equivalent to using the command palette to reopen the current workspace in a container.
    >
    > :::image type="content" source="media/tutorial-nodejs-web-app/reopen-container-toast.png" alt-text="Screenshot of a toast notification to reopen the current folder within the context of a development container.":::

1. Check the versions of the tools you use in this tutorial.

    ```console
    docker --version

    node --version

    npm --version

    az --version
    ```

    > [!NOTE]
    > This tutorial requires the following versions of each tool, which are preinstalled in your environment:
    >
    > | Tool | Version |
    > | --- | --- |
    > | Docker | &ge; 20.10.0 |
    > | Node.js | &ge; 18.0150 |
    > | npm | &ge; 9.5.0 |
    > | Azure CLI | &ge; 2.46.0 |
    >

1. Close the terminal.

1. The remaining steps in this tutorial take place in the context of this development container.

---

## Test the MERN application's API with the MongoDB container

Start by running the sample application's API with the local MongoDB container to validate that the application works.

1. Run a MongoDB container using Docker and publish the typical MongoDB port (`27017`).

    ```console
    docker pull mongo:6.0

    docker run --detach --publish 27017:27017 mongo:6.0
    ```

1. In the side bar, select the MongoDB extension.

    :::image type="content" source="media/tutorial-nodejs-web-app/select-mongodb-option.png" alt-text="Screenshot of the MongoDB extension in the side bar.":::

1. Add a new connection to the MongoDB extension using the connection string `mongodb://localhost`.

    :::image type="content" source="media/tutorial-nodejs-web-app/select-mongodb-add-connection.png" alt-text="Screenshot of the added connection button in the MongoDB extension.":::

1. Once the connection is successful, open the **data/products.mongodb** playground file.

1. Select the **Run all** icon to execute the script.

    :::image type="content" source="media/tutorial-nodejs-web-app/select-mongodb-playground-run-all.png" alt-text="Screenshot of the run all button in a playground for the MongoDB extension.":::

1. The playground run should result in a list of documents in the local MongoDB collection. Here's a truncated example of the output.

    ```json
    [
      {
        "_id": { "$oid": "640a146e89286b79b6628eef" },
        "name": "Confira Watch",
        "category": "watches",
        "price": 105
      },
      {
        "_id": { "$oid": "640a146e89286b79b6628ef0" },
        "name": "Diannis Watch",
        "category": "watches",
        "price": 98,
        "sale": true
      },
      ...
    ]
    ```

    > [!NOTE]
    > The object identifiers (`_id`) are randomly generated and differ from this truncated example output.

1. In the **server/** directory, create a new **.env** file.

1. In the **server/.env** file, add an environment variable for this value:

    | Environment Variable | Value |
    | --- | --- |
    | `CONNECTION_STRING` | The connection string to the Azure DocumentDB cluster. For now, use `mongodb://localhost:27017?directConnection=true`. |

    ```env
    CONNECTION_STRING=mongodb://localhost:27017?directConnection=true
    ```

1. Change the context of the terminal to the **server/** folder.

    ```console
    cd server
    ```

1. Install the dependencies from Node Package Manager (npm).

    ```console
    npm install
    ```

1. Start the Node.js &amp; Express application.

    ```console
    npm start
    ```

1. The API automatically opens a browser window to verify that it returns an array of product documents.

1. Close the extra browser tab/window.

1. Close the terminal.

## Test the MERN application with the Azure DocumentDB cluster

Now, let's validate that the application works seamlessly with Azure DocumentDB. For this task, populate the preexisting cluster with seed data using the MongoDB shell and then update the API's connection string.

1. Sign in to the Azure portal (<https://portal.azure.com>).

1. Navigate to the existing Azure DocumentDB cluster page.

1. From the Azure DocumentDB cluster page, select the **Connection strings** navigation menu option.

   :::image type="content" source="media/tutorial-nodejs-web-app/select-connection-strings-option.png" alt-text="Screenshot of the connection strings option on the page for a cluster.":::

1. Record the value from the **Connection string** field.

   :::image type="content" source="media/tutorial-nodejs-web-app/connection-string-value.png" alt-text="Screenshot of the connection string credential for a cluster.":::

    > [!IMPORTANT]
    > The connection string in the portal doesn't include the username and password values. You must replace the `<user>` and `<password>` placeholders with the credentials you used when you originally created the cluster.

1. Open a new terminal within your integrated development environment (IDE).

1. Start the MongoDB Shell using the `mongosh` command and the connection string you recorded earlier. Make sure you replace the `<user>` and `<password>` placeholders with the credentials you used when you originally created the cluster.

    ```console
    mongosh "<mongodb-cluster-connection-string>"
    ```

    > [!NOTE]
    >
    > You could need to encode specific values for the connection string. In this example, the name of the cluster is `msdocs-azure-documentdb-tutorial`, the username is `clusteradmin`, and the password is `P@ssw.rd`. In the password, the `@` character needs to be encoded using `%40`. An example connection string is provided here with the correct encoding of the password.
    >
    > ```output
    > CONNECTION_STRING=mongodb+srv://clusteradmin:P%40ssw.rd@msdocs-azure-documentdb-tutorial.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000
    > ```
    >

1. Within the shell, run the following commands to create your database, create your collection, and seed with starter data.

    :::code language="mongosh" source="~/azure-cosmos-db-mongodb-mern-web-app/data/products.mongodb" highlight="5-16":::

1. The commands should result in a list of documents in the local MongoDB collection. Here's a truncated example of the output.

    ```json
    [
      {
        "_id": { "$oid": "640a146e89286b79b6628eef" },
        "name": "Confira Watch",
        "category": "watches",
        "price": 105
      },
      {
        "_id": { "$oid": "640a146e89286b79b6628ef0" },
        "name": "Diannis Watch",
        "category": "watches",
        "price": 98,
        "sale": true
      },
      ...
    ]
    ```

    > [!NOTE]
    > The object identifiers (`_id`) are randomly generated and differ from this truncated example output.

1. Exit the MongoDB shell.

    ```console
    exit
    ```

1. In the **client/** directory, create a new **.env** file.

1. In the **client/.env** file, add an environment variable for this value:

    | Environment Variable | Value |
    | --- | --- |
    | `CONNECTION_STRING` | The connection string to the Azure DocumentDB cluster. Use the same connection string you used with the mongo shell. |

    ```output
    CONNECTION_STRING=<your-connection-string>
    ```

1. Validate that the application is using the database service by changing the context of the terminal to the **server/** folder, installing dependencies from Node Package Manager (npm), and then starting the application.

    ```console
    cd server

    npm install

    npm start
    ```

1. The API automatically opens a browser window to verify that it returns an array of product documents.

1. Close the extra browser tab/window. Then, close the terminal.

## Deploy the MERN application to Azure App Service

Prove that the application works end-to-end by deploying the service and client to Azure App Service. Use secrets in the web apps to store environment variables with credentials and API endpoints.

1. Within your integrated development environment (IDE), open a new terminal.

1. Create a shell variable for the name of the preexisting resource group named *resourceGroupName*.

    ```azurecli
    # Variable for resource group name
    resourceGroupName="<existing-resource-group>"
    ```

1. Create shell variables for the two web app named *serverAppName* and *clientAppName*.

    ```azurecli
    # Variable for randomnly generated suffix
    let suffix=$RANDOM*$RANDOM

    # Variable for web app names with a randomnly generated suffix
    serverAppName="server-app-$suffix"
    clientAppName="client-app-$suffix"
    ```

1. If you haven't already, sign in to the Azure CLI using the `az login --use-device-code` command.

1. Change the current working directory to the **server/** path.

    ```console
    cd server
    ```

1. Create a new web app for the server component of the MERN application with `az webapp up`.

    ```console
    az webapp up \
        --resource-group $resourceGroupName \
        --name $serverAppName \
        --sku F1 \
        --runtime "NODE|18-lts"
    ```

1. Create a new connection string setting for the server web app named `CONNECTION_STRING` with `az webapp config connection-string set`. Use the same value for the connection string you used with the MongoDB shell and **.env** file earlier in this tutorial.

    ```console
    az webapp config connection-string set \
        --resource-group $resourceGroupName \
        --name $serverAppName \
        --connection-string-type custom \
        --settings "CONNECTION_STRING=<mongodb-connection-string>"
    ```

1. Get the URI for the server web app with `az webapp show` and store it in a shell variable name d **serverUri**.

    ```azurecli
    serverUri=$(az webapp show \
        --resource-group $resourceGroupName \
        --name $serverAppName \
        --query hostNames[0] \
        --output tsv)
    ```

1. Use the `open-cli` package and command from NuGet with `npx` to open a browser window using the URI for the server web app. Validate that the server app is returning your JSON array data from the cluster.

    ```console
    npx open-cli "https://$serverUri/products" --yes
    ```

    > [!TIP]
    > Sometimes deployments can finish asynchronously. If you aren't seeing what you expect, wait another minute and refresh your browser window.

1. Change the working directory to the **client/** path.

    ```console
    cd ../client
    ```

1. Create a new web app for the client component of the MERN application with `az webapp up`.

    ```console
    az webapp up \
        --resource-group $resourceGroupName \
        --name $clientAppName \
        --sku F1 \
        --runtime "NODE|18-lts"
    ```

1. Create a new app setting for the client web app named `REACT_APP_API_ENDPOINT` with `az webapp config appsettings set`. Use the server API endpoint stored in the **serverUri** shell variable.

    ```console
    az webapp config appsettings set \
        --resource-group $resourceGroupName \
        --name $clientAppName \
        --settings "REACT_APP_API_ENDPOINT=https://$serverUri"
    ```

1. Get the URI for the client web app with `az webapp show` and store it in a shell variable name d **clientUri**.

    ```azurecli
    clientUri=$(az webapp show \
        --resource-group $resourceGroupName \
        --name $clientAppName \
        --query hostNames[0] \
        --output tsv)
    ```

1. Use the `open-cli` package and command from NuGet with `npx` to open a browser window using the URI for the client web app. Validate that the client app is rendering data from the server app's API.

    ```console
    npx open-cli "https://$clientUri" --yes
    ```

    > [!TIP]
    > Sometimes deployments can finish asynchronously. If you aren't seeing what you expect, wait another minute and refresh your browser window.

1. Close the terminal.

## Clean up resources

When you're working in your own subscription, at the end of a project, it's a good idea to remove the resources that you no longer need. Resources left running can cost you money. You can delete resources individually or delete the resource group to delete the entire set of resources.

1. To delete the entire resource group, use `az group delete`.

    ```azurecli
    az group delete \
        --name $resourceGroupName \
        --yes
    ```

1. Validate that the resource group is deleted using `az group list`.

    ```azurecli
    az group list
    ```

## Clean up dev environment

You might also wish to clean up your development environment or return it to its typical state.

### [GitHub Codespaces](#tab/github-browser)

Deleting the GitHub Codespaces environment ensures that you can maximize the amount of free per-core hours entitlement you get for your account.

1. Sign into the GitHub Codespaces dashboard (<https://github.com/codespaces>).

1. Locate your currently running development container sourced from the `azure-samples/msdocs-azure-cosmos-db-mongodb-mern-web-app` GitHub repository.

    :::image type="content" source="media/tutorial-nodejs-web-app/codespace-dashboard.png" alt-text="Screenshot of all the running devcontainers including their status and templates.":::

1. Open the context menu for the codespace and then select **Delete**.

    :::image type="content" source="media/tutorial-nodejs-web-app/codespace-delete.png" alt-text="Screenshot of the context menu for a single codespace with the delete option highlighted.":::

### [Visual Studio Code](#tab/visual-studio-code)

You aren't necessarily required to clean up your local environment, but you can stop the running development container and return to running Visual Studio Code in the context of a local workspace.

1. Open the **Command Palette**, search for the **Dev Containers** commands, and then select **Dev Containers: Reopen Folder Locally**.

    :::image type="content" source="media/tutorial-nodejs-web-app/reopen-local-command-palette.png" alt-text="Screenshot of the Command Palette option to reopen the current folder within your local environment.":::

> [!TIP]
> Visual Studio Code stops the running development container, but the container still exists in Docker in a stopped state. You always can delete the container instance, container image, and volumes from Docker to free up more space on your local machine.

---

## Next step

> [!div class="nextstepaction"]
> [Migrate your data](migration-options.md)
