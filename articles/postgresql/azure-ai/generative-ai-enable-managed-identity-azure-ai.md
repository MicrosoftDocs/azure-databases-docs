---
title: Enable Managed Identity for Azure AI Services with the Azure AI Extension for PostgreSQL
description: Enable system assigned managed identity for Azure AI Services with the Azure AI extension for PostgreSQL.
author: shreyaaithal
ms.author: shaithal
ms.reviewer: maghan
ms.date: 05/19/2025
ms.update-cycle: 180-days
ms.service: azure-database-postgresql
ms.topic: how-to
ms.collection:
  - ce-skilling-ai-copilot
ms.custom:
  - build-2025
# customer intent: As a user, I want to understand how to enable managed identity with the azure_ai extension for my Azure Database for PostgreSQL flexible server instance.
---

# Enable Managed Identity for Azure AI services with the azure_ai extension preview

The Azure AI extension for Azure Database for PostgreSQL supports System Assigned Managed Identity (SAMI) with Azure AI Services, Azure OpenAI, and Azure Machine Learning, offering enhanced security benefits for customers. By using Microsoft Entra ID, users can authenticate without access keys, reducing the risk of unauthorized access and simplifying credential management. This integration ensures that identities and permissions are handled securely and efficiently, providing a robust framework for database security.

## Subscription key benefits

- **No Secrets to Store** – No need to manually manage or rotate subscription keys.
- **Improved Security** – No risk of exposing API keys in logs or code repositories.
- **Simpler Maintenance** – Azure handles authentication behind the scenes, reducing operational overhead.

## Create a system-assigned managed identity 

1. Navigate to the Azure portal.
1. Select your Azure Database for PostgreSQL flexible server instance within the Portal.
1. Enable Managed Identity:
 - From the left navigation menu of the server overview page, expand **Security** and select **Identity**.
 - Select the **On** radio button for **System assigned managed identity**.
 - Select **Save** to enable the managed identity.

To learn more about it, visit [Managed Identities](/azure/active-directory/managed-identities-azure-resources/overview)

## Assign managed identities

1. Go to the Azure portal and select the Azure AI Services resource.
1. In the menu, select **Access control (IAM)**.
1. Select **Add** and then **Add role assignment**.
1. Choose the role **Cognitive Services User**.
1. In the **Members** section, select **Managed identity**.
1. Choose the subscription and the managed identity of your PostgreSQL server.
1. Select **Save** to assign the role.
1. Return to the server's Overview page and click the Restart button to reboot the server.

To learn more, visit  ['Managed Identity with Azure AI Services'](/azure/active-directory/managed-identities-azure-resources/overview)

### Access Control (IAM) for Azure OpenAI

1. Go to the Azure portal and select the Azure OpenAI resource deployed in your subscription. To quickly identify the resource, you can filter the resources by type, Azure OpenAI.
1. In the resource's menu, select **Access control (IAM)**.
1. Select **Add** and then **Add role assignment**.
1. Choose the role **Cognitive Services OpenAI User**.
1. In the **Members** section, select **Managed identity**.
1. Choose the subscription and the managed identity of your PostgreSQL server.
1. Select **Save** to assign the role.

To learn more, visit [Managed Identity with Azure OpenAI'](/azure/active-directory/managed-identities-azure-resources/overview)

### Access Control (IAM) for Azure Machine Learning

1. Go to the Azure portal and select the Azure Machine Learning resource.
1. In the resource's menu, select **Access control (IAM)**.
1. Select **Add** and then **Add role assignment**.
1. Choose the role **Azure Machine Learning Data Scientist**.
1. In the **Members** section, select **Managed identity**.
1. Choose the subscription and the managed identity of your PostgreSQL server.
1. Select **Save** to assign the role.
1. Ensure that the authentication type of model endpoint is selected as **Microsoft Entra token-based**.

## Update database authorization settings in azure_ai

You need to update the database authorization settings to configure the Azure AI extension for PostgreSQL to use managed identity or subscription key authentication. This process ensures the extension is correctly authenticated with Azure AI Services, Azure OpenAI, or Azure Machine Learning. Follow the steps below to set your use case's appropriate authorization type and endpoint.

### Set Authorization Type to Managed Identity

- For OpenAI, by executing the following SQL command:

 ```sql
  SELECT azure_ai.set_setting('azure_openai.auth_type', 'managed-identity');
 ```
- For Cognitive Services, by executing the following SQL command:

 ```sql
  SELECT azure_ai.set_setting('azure_cognitive.auth_type', 'managed-identity');
 ```
- If you use translate services, you need to set the resource ID of the translator resource by executing the following SQL command:

 ```sql
  SELECT azure_ai.set_setting('azure_cognitive.translator_resource_id', '<Your_translator_resource_id>');
 ```
- For Machine Learning Services, by executing the following SQL command:

 ```sql
  SELECT azure_ai.set_setting('azure_ml.auth_type', 'managed-identity');
 ```

### Set Endpoint

- For Azure OpenAI, execute the following SQL command to set the endpoint:

 ```sql
  SELECT azure_ai.set_setting('azure_openai.endpoint', 'https://<Your_openai_account>.openai.azure.com'); 
 ```

### Verify settings

After configuring the Azure AI extension for PostgreSQL, it's important to confirm that the settings have been applied correctly. Verifying the settings ensures the integration is properly configured and ready to interact with Azure AI Services, Azure OpenAI, or Azure Machine Learning. Use the following SQL commands to check the current configuration and validate that the correct authorization type and endpoints are in place.

 ```sql
  SELECT azure_ai.get_setting('azure_openai.auth_type');
  SELECT azure_ai.get_setting('azure_openai.endpoint');
 ```

## Test the configuration

After setting up the managed identity and configuring the Azure AI extension for PostgreSQL, verifying that the integration works as expected is essential. Testing ensures the database can authenticate successfully with Azure AI Services, Azure OpenAI, and Azure Machine Learning. The following examples demonstrate how to execute sample function calls to validate the configuration and confirm that the services function without authorization errors.

 ```sql
  SELECT azure_cognitive.analyze_sentiment('Your text here');
 ```

Ensure that the function executes successfully without any authorization errors.

### Test OpenAI services

Testing OpenAI services ensures that the integration between the Azure AI extension for PostgreSQL and Azure OpenAI is functioning correctly. By executing sample function calls, you can validate that the managed identity or subscription key authentication is configured correctly and that the database can successfully interact with OpenAI models. Follow the example below to test the embedding creation functionality and confirm that the service works without authorization errors.

 ```sql
  SELECT azure_openai.create_embeddings('Your model deployment name', 'Your text here');
 ```

Ensure that the function executes successfully without any authorization errors.

### Test machine learning services

Testing machine learning services ensures that the integration between the Azure AI extension for PostgreSQL and Azure Machine Learning is functioning as expected. You can validate that the managed identity or subscription key authentication is correctly configured by executing sample function calls. This step confirms that the database can successfully interact with deployed machine learning models, enabling seamless execution of predictions or other model operations. Use the example below to test the model invocation functionality and verify that the service works without authorization errors.

 ```sql
  SELECT azure_ml.invoke('Your model input', 'Your model deployment name');
 ```

Ensure that the function executes successfully without any authorization errors.

 ```sql
  SELECT azure_ml.invoke('Your model input', 'Your model deployment name');
 ```

Ensure that the function executes successfully without any authorization errors.

## Subscription key authentication

If you need to revert to using subscription key authentication, follow the steps below. This is useful if you want to switch back to using subscription keys for authentication instead of managed identity.

### Connect to PostgreSQL Database

Use your preferred PostgreSQL client to connect to your database.

### Set subscription key authorization types 

- For OpenAI, by executing the following SQL commands:

 ```sql
  SELECT azure_ai.set_setting('azure_openai.auth_type', 'subscription-key');
  SELECT azure_ai.set_setting('azure_openai.endpoint','https://<Your_OpenAI_Endpoint>');
  SELECT azure_ai.set_setting('azure_openai.subscription_key', '<Key>');
 ```
- For Cognitive Services, by executing the following SQL commands:

 ```sql
  SELECT azure_ai.set_setting('azure_cognitive.auth_type', 'subscription-key');
  SELECT azure_ai.set_setting('azure_cognitive.endpoint','https://<endpoint>.cognitiveservices.azure.com');
  SELECT azure_ai.set_setting('azure_cognitive.subscription_key', '<Key>');
 ```
- For Machine Learning Services, by executing the following SQL commands:

 ```sql
  SELECT azure_ai.set_setting('azure_ml.auth_type', 'subscription-key');
  SELECT azure_ai.set_setting('azure_ml.scoring_endpoint','<URI>');
  SELECT azure_ai.set_setting('azure_ml.endpoint_key', '<Key>');
 ```

## Related content

- [Azure Database for PostgreSQL documentation](../overview.md)
- [PostgreSQL extension for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-ossdata.vscode-postgresql)
- [GitHub Copilot extension](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot)
- [GitHub Copilot Chat extension](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot-chat)
- [MSSQL extension for Visual Studio Code?](/sql/tools/visual-studio-code-extensions/mssql/mssql-extension-visual-studio-code)
