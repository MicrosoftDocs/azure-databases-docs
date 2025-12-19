---
title: Index documents for search (preview)
titleSuffix: Azure Cosmos DB for NoSQL
description: Index documents from Azure Blob Storage or Microsoft SharePoint for semantic search using Azure Logic Apps
author: jcodella
ms.author: jacodel
ms.service: azure-cosmos-db
ms.topic: how-to
ms.date: 4/30/2025
ms.update-cycle: 180-days
ms.collection:
  - ce-skilling-ai-copilot
appliesto:
  - ✅ NoSQL
ms.custom:
  - build-2025
---

# Document Indexer for Azure Cosmos DB (preview)

## Introduction

The **Document Indexer** is an easy-to-use connection to [Azure Logic Apps Standard](/azure/logic-apps/logic-apps-overview) templates to automate the process of transforming raw document files into searchable content within Azure Cosmos DB.

Document Indexer extracts text data from documents (PDFs, images, Microsoft Office documents, markdown, and plain text), then chunks the text, generates [vector embeddings using Azure OpenAI](/azure/ai-services/openai/how-to/embeddings), and writes the structured output to your Azure Cosmos DB container. This enables fast search experiences using full-text, vector, and hybrid search in Azure Cosmos DB.

It uses your own resources deployed in your Azure subscription, offering you flexibility and control over the workflow. 

There are four templates available index documents from 
- Azure Blob Storage using simple text parsing
- Azure Blob Storage using Azure Document Intelligence for OCR
- Microsoft SharePoint using simple text parsing
- Microsoft from SharePoint using Azure Document Intelligence for OCR

Generally, if your documents may contain text that's not easily parsable (certain PDFs, image files, etc.), you need to use [Azure Document Intelligence](/azure/ai-services/document-intelligence/overview) to perform OCR and extract the text. 

---

## Requirements
Before using the Document Indexer, make sure the following resources are created and configured in your Azure subscription:

- **Logic Apps Standard Resource**: Required to host and run the workflow.
- **Azure Cosmos DB for NoSQL Account**:
  - A database and container must be created.
  - The **Vector Search** feature must be enabled for the account.
  - A vector index must be defined on the target container.
- **Azure OpenAI Resource**:
  - An embedding model such as `text-embedding-3-large` must be deployed and accessible.
- **Azure Blob Storage**:
  - Documents to be indexed must be stored in a container, or inserted in the future.
- **Azure AI Document Intelligence (optional)**:
  - Used to extract structured text from complex file types such as scanned PDFs or images. You can choose a workflow template that either uses or doesn't use Azure AI Document Intelligence depending on whether or not your documents require it for text extraction.

---

## How to Use It

### 1. Configure in the Azure portal

 1. Go to your Azure Cosmos DB Resource and select **Integrations** from the left-hand navigation pane.
 2. Select **Document Indexer** to go to the next screen to create or manage your Document Indexer workflows.

:::image type="content" source="../media/document-indexer/document-indexer-navigation.png" lightbox="../media/document-indexer/document-indexer-navigation.png" alt-text="Screenshot of navigating to the Document Indexer from the Azure portal.":::

### 2. Create a new workflow
From here you can create new workflows, or manage existing workflows. Create a new workflow by selecting the "+ Create" button. 

:::image type="content" source="../media/document-indexer/document-indexer-overview.png" lightbox="../media/document-indexer/document-indexer-overview.png" alt-text="Screenshot of the Document Indexer overview screen to create a workflow.":::

### 3. Choose a starting template
You can select which of the four template options to set up your workflow: There are two for indexing documents from Azure Blob Storage (with or without using Azure Document Intelligence) and two for indexing documents from Azure Blob Storage (with or without using Azure Document Intelligence).

In this example, let's pick the template using Azure Blob Storage without Azure Document Intelligence.

  :::image type="content" source="../media/document-indexer/document-indexer-workflows.png" lightbox="../media/document-indexer/document-indexer-workflows.png" alt-text="Screenshot of Document Indexer workflow templates available to use.":::


### 4. Review template information
After selecting a template, read the description, evaluate the workflow diagram, and determine if it can satisfy your requirements. The workflow can always be customized once deployed if more flexibility is needed.
  :::image type="content" source="../media/document-indexer/document-indexer-example-description.png" lightbox="../media/document-indexer/document-indexer-workflows.png" alt-text="Screenshot of Document Indexer template descriptions and details.":::

### 5. Assign Azure details
Associate your selected workflow with an Azure subscription, resource group, and Azure Logic Apps deployment. 

  :::image type="content" source="../media/document-indexer/document-indexer-example-setup.png" lightbox="../media/document-indexer/document-indexer-example-setup.png" alt-text="Screenshot of Document Indexer setup for your Azure subscription, resource, group, and Azure Logic Apps resource.":::

### 6. Set up connection to resources
Connect your workflow to your Azure resources using the wizard.
  :::image type="content" source="../media/document-indexer/document-indexer-example-connections.png" lightbox="../media/document-indexer/document-indexer-example-connections.png" alt-text="Screenshot of Document Indexer connection to Azure resources needed for the workflow.":::

### 7. Fill in the details
Enter in the deployment details to ensure you're properly utilizing your resources correctly and the workflow can source data, perform actions, and insert data properly. 
  :::image type="content" source="../media/document-indexer/document-indexer-example-parameters.png" lightbox="../media/document-indexer/document-indexer-example-parameters.png" alt-text="Screenshot of Document Indexer template parameters.":::

### 8. Create the workflow
Select "Create" and test your workflow by adding document files to your sourced location. 


## Related content

- [About Azure Logic Apps](/azure/logic-apps/logic-apps-overview)
- [Azure Logic Apps workflows from templates](/azure/logic-apps/create-single-tenant-workflows-templates)
- [Vector search](../vector-search.md)
- [Full-text search](full-text-search.md)
- [Hybrid Search](hybrid-search.md)
