---
ms.topic: include
ms.date: 10/13/2025
---

[!INCLUDE[Prerequisites - Azure subscription](prerequisite-azure-subscription.md)]

- An existing Azure DocumentDB cluster

  - If you don't have a cluster, create a [new cluster](../quickstart-portal.md)
  
  - [Role Based Access Control (RBAC) enabled](../how-to-connect-role-based-access-control.md#enable-microsoft-entra-id-authentication)
  
  - [Firewall configured to allow access to your client IP address](../how-to-configure-firewall.md#grant-access-from-your-ip-address)

- [Azure OpenAI resource](/azure/ai-foundry/openai/how-to/create-resource?view=foundry-classic&pivots=cli#create-a-resource)

    - Custom domain configured

    - [Role Based Access Control (RBAC) enabled](/azure/developer/ai/keyless-connections)
  
    - `text-embedding-3-small` model deployed

    
- [Visual Studio Code](https://code.visualstudio.com/download)

    - [DocumentDB extension](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-documentdb)
    
[!INCLUDE[External - Azure CLI prerequisites](~/reusable-content/azure-cli/azure-cli-prepare-your-environment-no-header.md)]
