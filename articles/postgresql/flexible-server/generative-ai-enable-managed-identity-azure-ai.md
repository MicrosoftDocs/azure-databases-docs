---
title: Enable SAMI for Azure AI Services with the Azure AI extension for PostgreSQL
description: Enable system assigned managed identity for Azure AI Services with the Azure AI extension for PostgreSQL .
author: jojohnso-msft
ms.author: jojohnso
ms.reviewer: maghan
ms.date: 05/19/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
ms.custom:
  - build-2025
# customer intent: As a user, I want to understand how to enable managed identity with the azure_ai extension for Azure Database for PostgreSQL flexible server.
---

# Enable SAMI for Azure AI Services with azure_ai extension

## How to enable Managed Identity with azure_ai for Azure Database for PostgreSQL

The Azure AI extension for Azure Database for PostgreSQL supports System Assigned Managed Identity (SAMI) with Azure AI Services, Azure OpenAI, and Azure Machine Learning, offering enhanced security benefits for customers. By leveraging Entra ID, users can authenticate without access keys, reducing the risk of unauthorized access and simplifying credential management. This integration ensures that identities and permissions are handled securely and efficiently, providing a robust framework for database security.

### Benefits Over Subscription Keys:
- **No Secrets to Store** – No need to manage or rotate subscription keys manually.
- **Improved Security** – No risk of exposing API keys in logs or code repositories.
- **Simpler Maintenance** – Azure handles authentication behind the scenes, reducing operational overhead.

### Step 1: Create a System Assigned Managed Identity for Azure Database for PostgreSQL Flexible Server
1. Navigate to the Azure Portal.
2. Within the Portal, select your Azure Database for PostgreSQL Flexible Server.
3. Enable Managed Identity:
   - From the left navigation menu of the server overview page, expand “Security” and select “Identity”.
   - Select the "On" radio button for "System assigned managed identity".
   - Click "Save" to enable the managed identity.
4. Learn more about ['Managed Identities'](https://learn.microsoft.com/azure/active-directory/managed-identities-azure-resources/overview)

### Step 2: Assign Managed Identity to the necessary roles
#### Access Control (IAM) for Azure AI Services:
1. Go to the Azure portal and select the Azure AI Services resource.
2. In the menu, select "Access control (IAM)".
3. Click "Add" and then "Add role assignment".
4. Choose the role "Cognitive Services User".
5. In the "Members" section, select "Managed identity".
6. Choose the subscription and the managed identity of your PostgreSQL server.
7. Click "Save" to assign the role.
8. Learn more about ['Managed Identity with Azure AI Services'](https://learn.microsoft.com/azure/active-directory/managed-identities-azure-resources/overview)

#### Access Control (IAM) for Azure OpenAI:
1. Go to the Azure portal and select the Azure OpenAI resource deployed in your subscription. You can filter the resources by type, Azure OpenAI, to quickly identify the resource.
2. In the resource's menu, select "Access control (IAM)".
3. Click "Add" and then "Add role assignment".
4. Choose the role "Cognitive Services OpenAI User".
5. In the "Members" section, select "Managed identity".
6. Choose the subscription and the managed identity of your PostgreSQL server.
7. Click "Save" to assign the role.
8. Learn more about [Managed Identity with Azure OpenAI'](https://learn.microsoft.com/azure/active-directory/managed-identities-azure-resources/overview)

#### Access Control (IAM) for Azure Machine Learning:
1. Go to the Azure portal and select the Azure Machine Learning resource.
2. In the resource's menu, select "Access control (IAM)".
3. Click "Add" and then "Add role assignment".
4. Choose the role "AzureML Data Scientist".
5. In the "Members" section, select "Managed identity".
6. Choose the subscription and the managed identity of your PostgreSQL server.
7. Click "Save" to assign the role.
8. Ensure that the authentication type of model endpoint is selected as “Microsoft Entra token-based”.

### Step 3: Update authorization setting in azure_ai within the database
#### Connect to PostgreSQL Database:
Use your preferred PostgreSQL client to connect to your database.

#### Set Authorization Type to Managed Identity:
- For OpenAI by executing the following SQL command:
  ```sql
  SELECT azure_ai.set_setting('azure_openai.auth_type', 'managed-identity');
  ```
- For Cognitive Services by executing the following SQL command:
  ```sql
  SELECT azure_ai.set_setting('azure_cognitive.auth_type', 'managed-identity');
  ```
- If you use translate services, you need to set resource id of the translator resource by executing the following SQL command:
  ```sql
  SELECT azure_ai.set_setting('azure_cognitive.translator_resource_id', '<Your_translator_resource_id>');
  ```
- For Machine Learning Services by executing the following SQL command:
  ```sql
  SELECT azure_ai.set_setting('azure_ml.auth_type', 'managed-identity');
  ```

#### Set Endpoint:
- For Azure OpenAI, execute the following SQL command to set the endpoint:
  ```sql
  SELECT azure_ai.set_setting('azure_openai.endpoint', '<Your_OpenAI_Endpoint>');
  ```

#### Verify Settings:
Ensure that the settings are correctly applied by querying the settings:
  ```sql
  SELECT azure_ai.get_setting('azure_openai.auth_type');
  SELECT azure_ai.get_setting('azure_openai.endpoint');
  ```

### Step 4: Test the Configuration
#### Test Cognitive Services:
Execute a sample function call to Azure AI Services, such as sentiment analysis:
  ```sql
  SELECT azure_cognitive.analyze_sentiment('Your text here');
  ```
Ensure that the function executes successfully without any authorization errors.

#### Test OpenAI Services:
Execute a sample function call to Azure OpenAI, such as getting embeddings:
  ```sql
  SELECT azure_openai.create_embedding('Your model deployment name', 'Your text here');
  ```
Ensure that the function executes successfully without any authorization errors.

#### Test Machine Learning Services:
Execute a model invoke call to Azure Machine Learning service such as:
  ```sql
  SELECT azure_ml.invoke('Your model input', 'Your model deployment name');
  ```
Ensure that the function executes successfully without any authorization errors.

### Step 5: Return to Subscription Key Auth
If you need to return to using key based auth, follow these steps.
#### Connect to PostgreSQL Database:
Use your preferred PostgreSQL client to connect to your database.

#### Set Authorization Type to Subscription Key:
- For OpenAI by executing the following SQL commands:
  ```sql
  SELECT azure_ai.set_setting('azure_openai.auth_type', 'subscription-key');
  SELECT azure_ai.set_setting('azure_openai.endpoint','https://<Your_OpenAI_Endpoint>');
  SELECT azure_ai.set_setting('azure_openai.subscription_key', '<Key>');
  ```
- For Cognitive Services by executing the following SQL commands:
  ```sql
  SELECT azure_ai.set_setting('azure_cognitive.auth_type', 'subscription-key');
  SELECT azure_ai.set_setting('azure_cognitive.endpoint','https://<endpoint>.cognitiveservices.azure.com');
  SELECT azure_ai.set_setting('azure_cognitive.subscription_key', '<Key>');
  ```
- For Machine Learning Services by executing the following SQL commands:
  ```sql
  SELECT azure_ai.set_setting('azure_ml.auth_type', 'subscription-key');
  SELECT azure_ai.set_setting('azure_ml.scoring_endpoint','<URI>');
  SELECT azure_ai.set_setting('azure_ml.endpoint_key', '<Key>');
  ```

