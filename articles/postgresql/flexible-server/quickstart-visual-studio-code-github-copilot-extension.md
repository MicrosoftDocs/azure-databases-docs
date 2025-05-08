---
title: "Quickstart: Guide for GitHub Copilot Feature for Visual Studio Code PostgreSQL Extension"
description: Learn how to use the GitHub Copilot integration in the PostgreSQL extension for Visual Studio Code.
author: jjfrost
ms.author: jfrost
ms.reviewer: maghan
ms.date: 05/19/2025
ms.service: azure-database-postgresql
ms.topic: quickstart
ms.collection:
  - ce-skilling-ai-copilot
ms.custom:
  - copilot
  - vs-code
---

# Quickstart: GitHub Copilot for PostgreSQL extension in Visual Studio Code preview

The PostgreSQL extension for Visual Studio Code now includes GitHub Copilot integration, enhancing your database workflows with AI-assisted development. Once connected to a PostgreSQL database, Copilot accesses contextual information from your live connection. This enables the `@pgsql` Copilot chat participant to generate accurate, schema-aware SQL queries and insights, streamlining development and minimizing context-switching within Visual Studio Code.

## Prerequisites

Before you begin, verify you have the proper tools and resources downloaded and installed.

These tools and resources help you follow along with this article and make the most of the GitHub Copilot integration for the PostgreSQL extension in Visual Studio Code.

- [Visual Studio Code](https://code.visualstudio.com/) installed on your machine.
- PostgreSQL database installed locally or hosted in the [cloud](quickstart-create-server.md).
- [PostgreSQL extension](https://marketplace.visualstudio.com/items?itemName=ms-ossdata.vscode-postgresql) installed in Visual Studio Code.
- [GitHub Copilot extension](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot) and the [GitHub Copilot Chat extension](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot-chat) installed.
- [Azure account](how-to-deploy-on-azure-free-account.md) for connecting to cloud-hosted databases (optional).

## Install the GitHub Copilot and GitHub Copilot Chat extensions

1. If you do not already have the GitHub Copilot extension installed in Visual Studio Code:

1. Select the **Extensions** icon in Visual Studio Code, search for **GitHub Copilot**, and select **Install**.

1. The GitHub Copilot Chat extension is automatically installed along with GitHub Copilot.

## Sign in to GitHub in Visual Studio Code

1. Ensure you have a GitHub account and an active GitHub Copilot subscription:
   - [Create GitHub account](https://www.github.com)
   - [Enable GitHub Copilot Subscription](https://github.com/settings/copilot)

1. In Visual Studio Code, select the **Account** icon and choose **Sign in with GitHub to use GitHub Copilot**.

## Getting started with GitHub Copilot for PostgreSQL

1. Right-click on a PostgreSQL databases and select **Chat with this database**.

1. If prompted, select **Allow** to enable GitHub Copilot to access the database connection context.

1. When the Copilot chat interface opens, you can start asking questions using the `@pgsql` prefix to specify that you want to interact with the PostgreSQL database.

    Try a prompt like:

    ```copilot-prompt
    @pgsql tell me about the tables in the HR schema
    ```

    :::image type="content" source="media/quickstart-visual-studio-code-github-copilot-extension/pgsql-hr-schema-response.png" alt-text="Screenshot of Copilot Chat response showing a detailed breakdown of tables and columns in the HR schema of a PostgreSQL database.":::

1. Copilot responds with a detailed description of your schema's tables.

    :::image type="content" source="media/quickstart-visual-studio-code-github-copilot-extension/pgsql-hr-schema-response.png" alt-text="Screenshot of Copilot Chat response showing a detailed breakdown of tables and columns in the HR schema of a PostgreSQL database.":::

## Using read/write capabilities

> [!NOTE]  
> The GitHub Copilot Chat integration for PostgreSQL is a powerful tool that can make changes to your database. It is important to use this feature with caution, especially in staging and production environments. Always review the generated SQL code before executing it, and consider testing it in a safe environment first.

1. Try a more advanced prompt.

    ```copilot-prompt
    @pgsql convert the hr.employees table to use a JSONB column for the address field
    ```

    - Copilot might respond with SQL suggestions and ask permission to make changes.

1. To approve execution:

    ```copilot-prompt
    @pgsql Yes, please make the JSONB column for me
    ```

    - Then Copilot asks for confirmation:

        ```copilot-prompt
        @pgsql Yes, I confirm
        ```

## Using context menu options

- In addition to right-clicking on a database, you can select SQL code in the editor and right-click to access GitHub Copilot context menu options like **Explain Query**, **Rewrite Query**, or **Analyze Query Performance**.

## Additional ideas and prompt recipes

There are many prompts and things you can do with GitHub Copilot for PostgreSQL - the limit is only your imagination! To help jumpstart some ideas, here are some concept prompts you can try or modify to match your database context and development environment:

### Query optimization

Below are examples of prompts you can use to guide Copilot in addressing specific query optimization challenges, helping you achieve efficient and reliable database operations.

```copilot-prompt
I'm working on optimizing my database for high-concurrency workloads. The table is called transactions with millions of records, and I'm experiencing deadlocks under a heavy load. Help me optimize my table schema and queries.

I need help writing a query. The data is stored in the orders table, which uses the columns customer_id, order_date, and total_price. I also need to include a rolling 3-month average of customer spending using a window function.

I'm getting this error: 'ERROR: column `orders.total_price` must appear in the GROUP BY clause or be used in an aggregate function.
```

### Performance optimization

Below are examples of prompts you can use to guide Copilot in addressing specific performance optimization challenges, helping you achieve faster and more efficient database operations.

```copilot-prompt
Provide the Explain Plan for my most recent query, and please explain each step.

Can you run some performance metrics on my database and tell me how it performs?

My orders table has 10 million records, and queries on customer_id and order_date are slow. How can I optimize indexing, partitioning, and schema design for performance?
```

### App development

Below are examples of prompts you can use to guide Copilot in addressing app development challenges.

```copilot-prompt
Generate a FastAPI endpoint to fetch orders from the ecom.orders table with pagination.

Generate an ETL pipeline script to clean and normalize the customer table data.

Generate a FastAPI project with my database using SQLAlchemy.
```

## Clean up

To ensure a smooth experience, clean up any temporary resources or configurations created during this quickstart. For example:

- Disconnect from the PostgreSQL database in Visual Studio Code.
- Remove any test databases or tables created during the session.
- Close any open connections to avoid unnecessary resource usage.

## Support and feedback

For additional assistance or to report issues, use the built-in feedback tool in Visual Studio Code:

- Go to **Help > Report Issue**

    :::image type="content" source="media/quickstart-visual-studio-code-github-copilot-extension/report-issue.png" alt-text="Screenshot of Visual Studio Code Help menu with the 'Report Issue' option highlighted for submitting feedback or problems." lightbox="media/quickstart-visual-studio-code-github-copilot-extension/report-issue.png":::

- Or open the Command Palette with `Ctrl + Shift + P` and run: `PGSQL: Give Feedback`.

    :::image type="content" source="media/quickstart-visual-studio-code-github-copilot-extension/feedback-command-palette.png" alt-text="Screenshot of Visual Studio Code Command Palette with 'PGSQL: Give Feedback' command entered and highlighted." lightbox="media/quickstart-visual-studio-code-github-copilot-extension/feedback-command-palette.png":::

## Related content

- [Azure Database for PostgreSQL documentation](overview.md)
- [PostgreSQL extension for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-ossdata.vscode-postgresql)
- [GitHub Copilot extension](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot)
- [GitHub Copilot Chat extension](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot-chat)
- [MSSQL extension for Visual Studio Code?](/sql/tools/visual-studio-code-extensions/mssql/mssql-extension-visual-studio-code)
