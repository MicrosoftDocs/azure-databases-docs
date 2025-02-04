---
# Required metadata
# For more information, see https://review.learn.microsoft.com/en-us/help/platform/learn-editor-add-metadata?branch=main
# For valid values of ms.service, ms.prod, and ms.topic, see https://review.learn.microsoft.com/en-us/help/platform/metadata-taxonomies?branch=main

title: Use azure_local_ai extension to generate vector embeddings in PostgreSQL with locally deployed LLM
description: Generate text embeddings in PostgreSQL for retrieval augmented generation (RAG) patterns with the azure_local_ai extension and locally deployed LLM.
author:      jojohnso-msft # GitHub alias
ms.author: jojohnso
ms.service: azure-database-postgresql
ms.topic: how-to
ms.date: 12/08/2024
ms.collection: ce-skilling-ai-copilot
ms.subservice: flexible-server
ms.custom:
  - build-2024
---

# Generate vector embeddings in Azure Database for PostgreSQL - Flexible Server with locally deployed LLM (Preview)

## Prerequisites

1. An Azure Database for PostgreSQL Flexible Server instance running on a memory optimized VM SKU. Learn more about Azure memory optimized VMs here: [Azure VM sizes - Memory - Azure Virtual Machines](/azure/virtual-machines/sizes-memory)

1. You may want to enable the [vector](how-to-use-pgvector.md) extension, as it provides functionality to store and efficiently index text embeddings in your database.

## Enable the extension

Before you can enable azure_local_ai on your Azure Database for PostgreSQL flexible server instance, you need to allowlist the `azure_local_ai` extension as described in [allow an extension](../extensions/how-to-allow-extensions.md#allow-extensions).

> [!IMPORTANT]
> Hosting language models in the database requires a large memory footprint. To support this requirement, `azure_local_ai` is only supported on **memory-optimized** Azure VM SKUs with a minimum of **4 vCores**.
> If you are using a VM that does not meet the minimum requirements, the `azure_local_ai` extension will not appear in the list of allowed values for the `azure.extensions` server parameter.

Once the extension is allowlisted, you can follow the instructions provided in [create extensions](../extensions/how-to-allow-extensions.md#allow-extensions) to install the extension in each  database from where you want to use it.

> [!NOTE]  
> Enabling Azure Local AI will deploy the [multilingual-e5-small](https://huggingface.co/intfloat/multilingual-e5-small) model to your Azure Database for PostgreSQL Flexible Server instance. The linked documentation provides licensing terms from the e5 team.
> Additional third-party open-source models might become available for installation on an ongoing basis.

Installing the extension `azure_local_ai` creates a schema called `azure_local_ai` in which the extension stores tables, functions, and any other SQL-related objects it requires to implement and expose its functionality.

> [!IMPORTANT]  
> You may want to enable the [vector extension](how-to-use-pgvector.md), as it is required to store text embeddings in your PostgreSQL database.

## Functions provided by the extension

The `azure_local_ai` extension provides a set of functions. These functions allow you to create vector embeddings from text data, making it easier to develop generative AI applications. The extension offers functions for creating embeddings, getting settings, and more. By using these functions, you can simplify the development process and reduce latency by eliminating the need for additional remote API calls to AI embedding models hosted outside of the PostgreSQL boundary.

|  Schema  |  Name  |  Result data type  |  Argument data types  |  
|---|---|---|---|
| azure_local_ai  |  create_embeddings  |  TABLE(embedding real[])  |  model_uri text, inputs text[],   batch_size bigint DEFAULT 128, timeout_ms integer DEFAULT 3600000  |  
| azure_local_ai  |  create_embeddings  |  real[]  |  model_uri text, input text,   timeout_ms integer DEFAULT 3600000  |  
| azure_local_ai  |  get_setting  |  jsonb  |  keys text[] DEFAULT   ARRAY[]::text[], timeout_ms integer DEFAULT 3600000  |  
| azure_local_ai  |  get_setting  |  text  |  key text, timeout_ms integer   DEFAULT 3600000  |  
| azure_local_ai  |  model_metadata  |  jsonb  |  model_uri text  |  

These functions can be displayed using the following psql meta-command:

```sql
\df azure_local_ai.*
```

## azure_local_ai.create_embeddings

The `azure_local_ai` extension allows you to create and update embeddings both in scalar and batch format, invoking the locally deployed LLM.

```sql
azure_local_ai.create_embeddings(model_uri text, input text, batch_size bigint DEFAULT 128, timeout_ms integer DEFAULT 3600000);
```
```sql
azure_local_ai.create_embeddings(model_uri text, array[inputs [text]], batch_size bigint DEFAULT 128, timeout_ms integer DEFAULT 3600000);
```

### Arguments

#### model_uri

`text` name of the text embedding model invoked to create the embedding.

#### input

`text` or `text[]` single text or array of texts, depending on the overload of the function used, for which embeddings are created.

#### batch_size

`bigint DEFAULT 128` number of records to process at a time (only available for the overload of the function for which parameter `input` is of type `text[]`).

#### timeout_ms

`integer DEFAULT 3600000` timeout in milliseconds after which the operation is stopped.


###  azure_local_ai.get_setting

Used to obtain current values of configuration options.

```sql
SELECT azure_local_ai.get_setting(key TEXT)
```

`azure_local_ai` supports reviewing the configuration parameters of ONNX Runtime thread-pool within the ONNX Runtime Service. Changes aren't allowed at this time. [See ONNX Runtime performance tuning.](https://onnxruntime.ai/docs/performance/tune-performance/threading.html)


#### Arguments

##### Key

Valid values are:

- `intra_op_parallelism`: Sets total number of threads used for parallelizing single operator by ONNX Runtime thread-pool. By default, we maximize the number of intra ops threads as much as possible as it improves the overall throughput much (all available cpus by default).
- `inter_op_parallelism`: Sets total number of threads used for computing multiple operators in parallel by ONNX Runtime thread-pool. By default, we set it to minimum possible thread, which is 1. Increasing it often hurts performance due to frequent context switches between threads.
- `spin_control`: Switches ONNX Runtime thread-pool's spinning for requests. When disabled, it uses less cpu and hence causes more latency. By default, it's set to true (enabled).

#### Return type

`TEXT` representing the current value of the selected setting.


## Examples

### Create embeddings from existing texts

Following is an example that can be used in your own environment to test embedding generation with the locally deployed multilingual-e5 model. 

```sql
-- Create documents table
CREATE TABLE documents(doc_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, doc_contents TEXT NOT NULL, last_update TIMESTAMPTZ DEFAULT now());

--Insert data into the docs table
INSERT INTO documents(doc_contents) VALUES
  ('Create in-database embeddings with azure_local_ai extension.'),
  ('Enable RAG patterns with in-database embeddings and vectors on Azure Database for PostgreSQL - Flexible server.'),
  ('Generate vector embeddings in PostgreSQL with azure_local_ai extension.'),
  ('Generate text embeddings in PostgreSQL for retrieval augmented generation (RAG) patterns with azure_local_ai extension and locally deployed LLM.'),
  ('Use vector indexes and Azure OpenAI embeddings in PostgreSQL for retrieval augmented generation.');


-- Add a vector column and generate vector embeddings from locally deployed model
ALTER TABLE documents
  ADD COLUMN doc_vector vector(384) -- multilingual-e5 embeddings are 384 dimensions
  GENERATED ALWAYS AS (azure_local_ai.create_embeddings('multilingual-e5-small:v1', doc_contents)::vector) STORED; -- TEXT string sent to local model

--View floating point entries in the doc_vector column
SELECT doc_vector FROM documents;

-- Add a single record to the documents table and the vector embedding using azure_local_ai and locally deployed model will be automatically generated
INSERT INTO documents(doc_contents) VALUES
  ('Semantic Search with Azure Database for PostgreSQL - Flexible Server and Azure OpenAI');

--View all document entries, their contents, embeddings and last time the row was updated
SELECT doc_contents, doc_vector, last_update FROM documents;

-- The following command leverages the overload of azure_local_ai.create_embeddings function which accepts and array of TEXT
-- and produces a table for which each row contains the embedding of one element in the input array
SELECT azure_local_ai.create_embeddings('multilingual-e5-small:v1', array['Recommendation System with Azure Database for PostgreSQL - Flexible Server and Azure OpenAI.', 'Generative AI with Azure Database for PostgreSQL - Flexible Server.']);

```


### Generate embeddings upon insertion of new text

Following is an example that can be used in your own environment to test embedding generation with the locally deployed multilingual-e5 model.

```sql
-- Create documents table
CREATE TABLE documents(doc_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, doc_contents TEXT NOT NULL, last_update TIMESTAMPTZ DEFAULT now(), doc_vector vector(384)	GENERATED ALWAYS AS (azure_local_ai.create_embeddings('multilingual-e5-small:v1', doc_contents)::vector) STORED);

-- Insert data into the documents table
INSERT INTO documents(doc_contents) VALUES
  ('Create in-database embeddings with azure_local_ai extension.'),
  ('Enable RAG patterns with in-database embeddings and vectors on Azure Database for PostgreSQL - Flexible server.'),
  ('Generate vector embeddings in PostgreSQL with azure_local_ai extension.'),
  ('Generate text embeddings in PostgreSQL for retrieval augmented generation (RAG) patterns with azure_local_ai extension and locally deployed LLM.'),
  ('Use vector indexes and Azure OpenAI embeddings in PostgreSQL for retrieval augmented generation.');

-- Query embedding text, list results by descending similarity score
WITH all_documents AS (
 SELECT doc_id, doc_contents, doc_vector FROM documents
),
target_documents AS (
 SELECT azure_local_ai.create_embeddings('multilingual-e5-small:v1', 'Generate text embeddings in PostgreSQL.') doc_vector
)
SELECT all_documents.doc_id, all_docs.doc_contents , 1 - (all_documents.doc_vector::vector <=> target_documents.doc_vector::vector) AS similarity
 FROM target_documents, all_documents
 ORDER BY similarity DESC
 LIMIT 2;
```

## Related content

- [Integrate Azure Database for PostgreSQL - Flexible Server with Azure Cognitive Services](generative-ai-azure-cognitive.md).
- [Integrate Azure Database for PostgreSQL with Azure Machine Learning Services](generative-ai-azure-machine-learning.md).
- [Generate vector embeddings with Azure OpenAI in Azure Database for PostgreSQL - Flexible Server](generative-ai-azure-openai.md).
- [Azure AI extension in Azure Database for PostgreSQL - Flexible Server](generative-ai-azure-overview.md).
- [Generative AI with Azure Database for PostgreSQL - Flexible Server](generative-ai-overview.md).
- [Recommendation System with Azure Database for PostgreSQL - Flexible Server and Azure OpenAI](generative-ai-recommendation-system.md).
- [Semantic Search with Azure Database for PostgreSQL - Flexible Server and Azure OpenAI](generative-ai-semantic-search.md).
- [Enable and use pgvector in Azure Database for PostgreSQL - Flexible Server](how-to-use-pgvector.md).
