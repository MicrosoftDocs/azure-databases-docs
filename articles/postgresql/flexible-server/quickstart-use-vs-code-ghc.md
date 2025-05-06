---
title: Quickstart: Guide for GitHub Copilot Feature for VS Code PostgreSQL Extension
description: Learn how to use the GitHub Copilot integration in the PostgreSQL extension for Visual Studio Code.
author: jjfrost
ms.author: jjfrost
ms.date: 05/05/2025
ms.service: azure-database-postgresql
ms.topic: quickstart
ms.custom:
  - copilot
  - vs-code
---

# Quickstart: GitHub Copilot for PostgreSQL Extension in Visual Studio Code

## Overview

Building on the robust database connection and management features of the PostgreSQL extension for Visual Studio Code, this extension also provides GitHub Copilot integration that brings AI-assisted development directly into your database workflows.

Once connected to a PostgreSQL database, the extension enables Copilot to access contextual information from your live database connection. This allows the `@pgsql` Copilot chat participant to generate more accurate, schema-aware SQL queries and insights based on your actual database structure, streamlining development and reducing context-switching within Visual Studio Code.

## Prerequisites

- Visual Studio Code installed on your machine.
- PostgreSQL database installed locally or hosted in the cloud.
- PostgreSQL extension installed in Visual Studio Code.
- GitHub Copilot and GitHub Copilot Chat extension installed.
- Azure account for connecting to cloud-hosted databases (optional).

## Step 1: Install GitHub Copilot and GitHub Copilot Chat Extension

1. If you do not already have the GitHub Copilot extension installed in VS Code:

2. Click the **Extensions** icon in VS Code, search for **GitHub Copilot**, and click **Install**.

    !(./media/quickstart-use-vs-code-ghc/install-ghc.png)
    
    <!--:::image type="content" source="./media/quickstart-use-vs-code-ghc/install-ghc.png" alt-text="Screenshot of Visual Studio Code Extensions Marketplace showing GitHub Copilot and GitHub Copilot Chat with the Install buttons highlighted. The search bar contains the text 'GitHub Copilot'." lightbox="./media/quickstart-use-vs-code-ghc/install-ghc.png":::-->

3. The GitHub Copilot Chat extension is automatically installed along with GitHub Copilot.

## Step 2: Sign In to GitHub within VS Code

1. Ensure you have a GitHub account and an active GitHub Copilot subscription:
   - [Create GitHub account](https://www.github.com)
   - [Enable GitHub Copilot Subscription](https://github.com/settings/copilot)

2. In VS Code, click the **Account** icon and choose **Sign in with GitHub to use GitHub Copilot**.

    !(./media/quickstart-use-vs-code-ghc/sign-in-ghc.png)
    
    <!--:::image type="content" source="./media/quickstart-use-vs-code-ghc/sign-in-ghc.png" alt-text="Screenshot of Visual Studio Code with the Account icon selected and the option 'Sign in with GitHub to use GitHub Copilot' highlighted in the account menu." lightbox="./media/quickstart-use-vs-code-ghc/sign-in-ghc.png":::-->

## Step 3: Getting Started with GitHub Copilot for PostgreSQL

1. Right-click one of your PostgreSQL databases and select **Chat with this database**.

2. If prompted, click **Allow** to enable GitHub Copilot to access the database connection context.

3. The Copilot chat interface will open. Try a prompt like:

    - `@pgsql tell me about the tables in the HR schema`

        !(./media/quickstart-use-vs-code-ghc/pgsql-tell-me-about.png)
        
        <!--:::image type="content" source="./media/quickstart-use-vs-code-ghc/pgsql-tell-me-about.png" alt-text="Screenshot of GitHub Copilot Chat in VS Code with the user prompt '@pgsql tell me about the tables in the HR schema' typed in the chat input." lightbox="./media/quickstart-use-vs-code-ghc/pgsql-tell-me-about.png":::-->

4. Copilot will respond with a detailed description of your schema's tables.

    !(./media/quickstart-use-vs-code-ghc/pgsql-hr-schema-response.png)
        
    <!--:::image type="content" source="./media/quickstart-use-vs-code-ghc/pgsql-hr-schema-response.png" alt-text="Screenshot of Copilot Chat response showing a detailed breakdown of tables and columns in the HR schema of a PostgreSQL database." lightbox="./media/quickstart-use-vs-code-ghc/pgsql-hr-schema-response.png":::-->

## Step 4: Using Read/Write Capabilities

> **Caution**: Use this feature carefully on staging or production databases.

1. Try a more advanced prompt like:

    - `@pgsql please convert the employees table to use JSONB`

    - Copilot may respond with SQL suggestions and ask for permission to make changes.

        !(./media/quickstart-use-vs-code-ghc/hr-schema-jsonb-confirm.png)
        
        <!--:::image type="content" source="./media/quickstart-use-vs-code-ghc/hr-schema-jsonb-confirm.png" alt-text="Screenshot of Copilot Chat displaying a generated SQL script to convert the employees table to JSONB, with detailed steps and optional index creation." lightbox="./media/quickstart-use-vs-code-ghc/hr-schema-jsonb-confirm.png":::-->

2. To approve execution:

    - `@pgsql Yes, please make the JSONB column for me`

    - Copilot will ask for confirmation:

    - `@pgsql Yes I confirm`

        !(./media/quickstart-use-vs-code-ghc/hr-schema-after-jsonb.png)
        
        <!--:::image type="content" source="./media/quickstart-use-vs-code-ghc/hr-schema-after-jsonb.png" alt-text="Screenshot of GitHub Copilot Chat in VS Code showing confirmation and results of converting the hr.employees table to use a JSONB column." lightbox="./media/quickstart-use-vs-code-ghc/hr-schema-after-jsonb.png":::-->

## Step 5: Using Context Menu Options

- In addition to right-clicking on a database, you can also select SQL code in the editor and right-click to access GitHub Copilot context menu options like **Explain Query**, **Rewrite Query**, or **Analyze Query Performance**.

    !(./media/quickstart-use-vs-code-ghc/ghc-context-menus.png)
        
    <!--:::image type="content" source="./media/quickstart-use-vs-code-ghc/ghc-context-menus.png" alt-text="Screenshot of a PostgreSQL function opened in VS Code with a context menu expanded, showing GitHub Copilot options such as 'Explain Query' and 'Analyze Query Performance'." lightbox="./media/quickstart-use-vs-code-ghc/ghc-context-menus.png":::-->

## Additional Ideas and Prompt Recipes

There are a nearly infinite number of prompts and things you can do with GitHub Copilot for PostgreSQL - the limit is only your imagination! To help jumpstart some ideas, here are some concept prompts you can try or modify to match your database context and development environment:

### Query Optimization

- "I'm working on optimizing my database for high-concurrency workloads. The table called transactions with millions of records, and I'm experiencing deadlocks under heavy load. Help me optimize my table schema and queries."
- "I need help writing a query. The data is stored in the orders table, which uses the columns customer_id, order_date, and total_price. I also need to include a rolling 3-month average of customer spending using a window function."
- "I'm getting this error: 'ERROR: column `orders.total_price` must appear in the GROUP BY clause or be used in an aggregate function.'"

### Performance Optimization

- "Provide the Explain Plan for my most recent query, and please provide additional explain of each step."
- "Can you run some performance metrics on my database and tell me how it is performing?"
- "My orders table has 10 million records, and queries on customer_id and order_date are slow. How can I optimize indexing, partitioning, and schema design for performance?"

### App Development

- "Generate a FastAPI endpoint to fetch orders from the ecom.orders table with pagination."
- "Generate an ETL pipeline script to clean and normalize the customer table data."
- "Generate a FastAPI project with my database using SQLAlchemy."

## Submit Feedback

For bugs, feature requests, and issues please use the built-in feedback tool in Visual Studio Code. This can be completed via the VS Code Help menu or the PGSQL Command Palette.

- In Visual Studio Code, go to **Help > Report Issue**

    !(./media/quickstart-use-vs-code-ghc/report-issue.png)
        
    <!--:::image type="content" source="./media/quickstart-use-vs-code-ghc/report-issue.png" alt-text="Screenshot of VS Code Help menu with the 'Report Issue' option highlighted for submitting feedback or problems." lightbox="./media/quickstart-use-vs-code-ghc/report-issue.png":::-->

- Or open the Command Palette with `Ctrl + Shift + P` and run:

    !(./media/quickstart-use-vs-code-ghc/feedback-command-palette.png)
        
    <!--:::image type="content" source="./media/quickstart-use-vs-code-ghc/feedback-command-palette.png" alt-text="Screenshot of VS Code Command Palette with 'PGSQL: Give Feedback' command entered and highlighted." lightbox="./media/quickstart-use-vs-code-ghc/feedback-command-palette.png":::-->