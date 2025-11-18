---
ms.topic: include
ms.date: 09/30/2025
---

List the Azure DocumentDB resources deployed to your resource group.

1. Use [`az resource list`](/cli/azure/resource#az-resource-list) to get a list of resources in your resource group.

    ```azurecli-interactive
    az resource list \
        --resource-group "<resource-group-name>" \
        --namespace "Microsoft.DocumentDB" \
        --resource-type "mongoClusters" \
        --query "[].name" \
        --output json
    ```

1. In the example output, look for resources that have a type of `Microsoft.DocumentDB/mongoClusters`. Here's an example of the type of output to expect:

    ```json
    [
      "msdocs-documentdb-example-cluster"
    ]
    ```
