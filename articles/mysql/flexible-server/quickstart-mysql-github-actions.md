---
title: "Quickstart: Connect With GitHub Actions"
description: Use Azure Database for MySQL - Flexible Server from a GitHub Actions workflow.
author: juliakm
ms.author: jukullam
ms.reviewer: maghan
ms.date: 11/27/2024
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: quickstart
ms.custom:
  - github-actions-azure
  - mode-other
  - devx-track-azurecli
---

# Quickstart: Use GitHub Actions to connect to Azure Database for MySQL - Flexible Server

Get started with [GitHub Actions](https://docs.github.com/en/actions) by using a workflow to deploy database updates to [Azure Database for MySQL flexible server](https://azure.microsoft.com/services/mysql/).

## Prerequisites

You'll need:

- An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/free/?WT.mc_id=A261C142F).
- A GitHub account. If you don't have a GitHub account, [sign up for free](https://github.com/join).
- A GitHub repository with sample data (`data.sql`).

    > [!IMPORTANT]  
    > This quickstart assumes that you have cloned a GitHub repository to your computer so that you can add the associated IP address to a firewall rule, if necessary.

- An Azure Database for MySQL flexible server instance.
  - [Quickstart: Create an Azure Database for MySQL flexible server instance in the Azure portal](../single-server/quickstart-create-mysql-server-database-using-azure-portal.md)

## Workflow file overview

A GitHub Actions workflow is defined by a YAML (.yml) file in the `/.github/workflows/` path in your repository. This definition contains the various steps and parameters that make up the workflow.

The file has two sections:

| Section | Tasks |
| --- | --- |
| **Authentication** | 1. Generate deployment credentials. |
| **Deploy** | 1. Deploy the database. |

## Generate deployment credentials

[!INCLUDE [include](~/reusable-content/github-actions/generate-deployment-credentials.md)]

## Copy the MySQL connection string

In the Azure portal, go to your Azure Database for MySQL flexible server instance and open **Settings** > **Connection strings**. Copy the **ADO.NET** connection string. Replace the placeholder values for `your_database` and `your_password`.

> [!IMPORTANT]  
>  
> - For Azure Database for MySQL single server, use **Uid=adminusername@servername**. Note the **@servername** is required.
> - For Azure Database for MySQL flexible server, use **Uid=adminusername** without the @servername.

You'll use the connection string as a GitHub secret.

## Configure GitHub secrets

[!INCLUDE [include](~/reusable-content/github-actions/create-secrets-with-openid.md)]

## Add your workflow

1. Go to **Actions** for your GitHub repository.

1. Select **Set up your workflow yourself**.

1. Delete everything after the `on:` section of your workflow file. For example, your remaining workflow might look like this.

    ```csharp
    name: CI

    on:
    push:
        branches: [ main ]
    pull_request:
        branches: [ main ]
    ```

1. Rename your workflow `MySQL for GitHub Actions` and add the checkout and login actions. These actions check out your site code and authenticate with Azure using the `AZURE_CREDENTIALS` GitHub secret you created earlier.

    # [Service principal](#tab/userlevel)

    ```powershell
    name: MySQL for GitHub Actions

    on:
        push:
            branches: [ main ]
        pull_request:
            branches: [ main ]

    jobs:
        build:
            runs-on: windows-latest
            steps:
            - uses: actions/checkout@v1
            - uses: azure/login@v1
                with:
                    creds: ${{ secrets.AZURE_CREDENTIALS }}
      ```

    # [OpenID Connect](#tab/openid)

    ```powershell
    name: MySQL for GitHub Actions

    on:
        push:
            branches: [ main ]
        pull_request:
            branches: [ main ]

    jobs:
        build:
            runs-on: windows-latest
            steps:
            - uses: actions/checkout@v1
            - uses: azure/login@v1
                with:
                  client-id: ${{ secrets.AZURE_CLIENT_ID }}
                  tenant-id: ${{ secrets.AZURE_TENANT_ID }}
                  subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
    ```

    ___

1. Use the Azure MySQL Deploy action to connect to your MySQL instance. Replace `MYSQL_SERVER_NAME` with the name of your server. You should have a MySQL data file named `data.sql` at the root level of your repository.

    ```powershell
    - uses: azure/mysql@v1
      with:
        server-name: MYSQL_SERVER_NAME
        connection-string: ${{ secrets.AZURE_MYSQL_CONNECTION_STRING }}
        sql-file: './data.sql'
    ```

1. Complete your workflow by adding an action to sign out of Azure. Here's the completed workflow. The file appears in the `.github/workflows` folder of your repository.

    # [Service principal](#tab/userlevel)

    ```azurecli
    name: MySQL for GitHub Actions

    on:
      push:
          branches: [ main ]
      pull_request:
          branches: [ main ]
    jobs:
        build:
            runs-on: windows-latest
            steps:
              - uses: actions/checkout@v1
              - uses: azure/login@v1
                with:
                  creds: ${{ secrets.AZURE_CREDENTIALS }}

              - uses: azure/mysql@v1
                with:
                  server-name: MYSQL_SERVER_NAME
                  connection-string: ${{ secrets.AZURE_MYSQL_CONNECTION_STRING }}
                  sql-file: './data.sql'

                # Azure logout
              - name: logout
                run: |
                  az logout
    ```
    # [OpenID Connect](#tab/openid)

    ```azurecli
    name: MySQL for GitHub Actions

    on:
      push:
          branches: [ main ]
      pull_request:
          branches: [ main ]
    jobs:
        build:
            runs-on: windows-latest
            steps:
              - uses: actions/checkout@v1
              - uses: azure/login@v1
                with:
                  client-id: ${{ secrets.AZURE_CLIENT_ID }}
                  tenant-id: ${{ secrets.AZURE_TENANT_ID }}
                  subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
              - uses: azure/mysql@v1
                with:
                  server-name: MYSQL_SERVER_NAME
                  connection-string: ${{ secrets.AZURE_MYSQL_CONNECTION_STRING }}
                  sql-file: './data.sql'

                # Azure logout
              - name: logout
                run: |
                  az logout
    ```
    ___

## Review your deployment

1. Go to **Actions** for your GitHub repository.

1. Open the first result to see detailed logs of your workflow's run.

    :::image type="content" source="media/quickstart-mysql-github-actions/github-actions-run-mysql.png" alt-text="Screenshot of Log of GitHub Actions run.":::

## Clean up resources

When your Azure Database for MySQL flexible server database and repository are no longer needed, clean up the resources you deployed by deleting the resource group and your GitHub repository.

## Next step

> [!div class="nextstepaction"]
> [Learn about Azure and GitHub integration](/azure/developer/github/)
