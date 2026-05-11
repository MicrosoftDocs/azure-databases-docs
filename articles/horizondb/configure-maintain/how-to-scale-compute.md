---
title: Scale Compute in Azure HorizonDB
description: This article describes how to scale the compute in Azure HorizonDB.
author: kabharati
ms.author: kabharati
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-database-postgresql
ms.subservice: scale-out
ms.topic: how-to
# customer intent: As a user, I want to learn how to scale the compute in Azure HorizonDB.
---

# Scale compute in Azure HorizonDB

This article provides step-by-step instructions to perform scaling operations for the compute in Azure HorizonDB.

When you request a scaling operation of the compute used by your Azure HorizonDB, your server undergoes a restart and so leaves your server unavailable for some time. For more information about how that process works, and the expected duration of the downtime, 

## Steps to scale compute

### [Portal](#tab/portal-scale-compute)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure HorizonDB.

1. In the resource menu, select **Compute + storage**.

   

1. If you want to select a different tier than the one currently selected, in the **Compute tier** group of radio buttons, select the option that best adjusts to your needs.


1. If the region of your server supports Intel and AMD processors, you can use the **Compute processor** radio button to filter the options listed in the **Compute size** dropdown list to only hardware produced by the manufacturer selected.



1. If you want to select a different machine size among the ones available in the same tier, expand the **Compute size** dropdown list and select the size that best suits your needs.


1. Once you choose your desired configuration, select **Save**.



> [!NOTE]  
> When you select **Save** you're not asked for confirmation to proceed with the changes. The operation is immediately initiated and can't be aborted.

1. A notification shows that a deployment is in progress.


1. When the scale process completes, a notification shows that the deployment succeeded.


### [CLI](#tab/cli-scale-compute)

You can initiate the scaling of your compute via the [az postgres flexible-server update](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-update) command.

```azurecli-interactive
az postgres horizondb-cluster update \
  --resource-group <resource_group> \
  --name <server> \
  --tier <tier> \
  --sku-name <sku_name>
```

> [!NOTE]  
> The previous command might need to be completed with other parameters whose presence and values would vary depending on how you want to configure other features of the existing server.

The list of allowed values for the `--sku-name` parameter is dependent of the value passed to the `--tier` parameter, and of the region in which you're trying to deploy your server.

If you pass an incorrect value to `--sku-name`, you get the following error with the list of

```output
Incorrect value for --sku-name. The SKU name does not match <tier> tier. Specify --tier if you did not. Or CLI will set GeneralPurpose as the default tier. Allowed values : ['<sku_name_1>', '<sku_name_2>', ..., '<sku_name_n>']
```

---

## Related content




