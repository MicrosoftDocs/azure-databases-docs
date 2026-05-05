---
title: Delete a Server in Azure HorizonDB
description: This article describes the steps to delete an existing Azure HorizonDB instance.
author: avnishrastogimsft
ms.author: avrastog
ms.reviewer: maghan
ms.date: 05/05/2026
ms.service: azure-database-postgresql
ms.subservice: configuration
ms.topic: how-to
# customer intent: As a user, I want to learn how to delete an Azure HorizonDB instance.
---

# Delete a server in Azure HorizonDB

This article provides step-by-step instructions to delete an Azure HorizonDB instance.

## Delete a server

### [Portal](#tab/portal-delete-server)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure HorizonDB instance.

1. In the resource menu, select **Overview**.

   :::image type="content" source="media/how-to-delete-server/overview.png" alt-text="Screenshot showing how to select the Overview page." lightbox="media/how-to-delete-server/overview.png":::

1. Select the **Delete** button.

   :::image type="content" source="media/how-to-delete-server/delete-server.png" alt-text="Screenshot showing how to delete an Azure HorizonDB instance." lightbox="media/how-to-delete-server/delete-server.png":::

1. In the **Delete *\<server\>*** panel, make sure that the name of the resource you're willing to delete, matches the one displayed.

   :::image type="content" source="media/how-to-delete-server/confirm-server-name.png" alt-text="Screenshot showing where to find the name of the server being deleted." lightbox="media/how-to-delete-server/confirm-server-name.png":::

1. Take the time to provide feedback about your experience with the service. Select the icon that best expresses your overall level of satisfaction with the service, and provide more details in free text form.

   :::image type="content" source="media/how-to-delete-server/provide-feedback.png" alt-text="Screenshot showing where to provide feedback." lightbox="media/how-to-delete-server/provide-feedback.png":::

1. You must check the **I have read and understand that this server, as well as any databases it contains, will be deleted.** box, so that the **Delete** button is enabled. Optionally, check the **You can contact me about this feedback.** box, if we can contact you about the feedback provided.

   :::image type="content" source="media/how-to-delete-server/accept-conditions.png" alt-text="Screenshot showing how to accept terms and consequences of triggering the deletion of an Azure HorizonDB instance." lightbox="media/how-to-delete-server/accept-conditions.png":::

1. If the server has private endpoints configured, you also have to check the **I acknowledge that the deletion of the server doesn't delete any private endpoints associated with this server. After the server is deleted, make sure that you delete these private endpoints.** box, so that the **Delete** button is enabled.

   :::image type="content" source="media/how-to-delete-server/accept-conditions-private-endpoints.png" alt-text="Screenshot showing how to accept terms and consequences of triggering the deletion of an Azure HorizonDB instance when there are private endpoints." lightbox="media/how-to-delete-server/accept-conditions-private-endpoints.png":::

1. If the server is VNET integrated, you also have to check the **I acknowledge that the deletion of the server doesn't delete the virtual network in which the server is integrated. After the server is deleted, consider if you should also delete the virtual network.** box, so that the **Delete** button is enabled.

   :::image type="content" source="media/how-to-delete-server/accept-conditions-vnet-integration.png" alt-text="Screenshot showing how to accept terms and consequences of triggering the deletion of an Azure HorizonDB instance when it's VNET integrated." lightbox="media/how-to-delete-server/accept-conditions-vnet-integration.png":::

1. Select **Delete** to proceed with the immediate deletion of the server.

   :::image type="content" source="media/how-to-delete-server/delete.png" alt-text="Screenshot showing the location of the Delete button to initiate the deletion of the server." lightbox="media/how-to-delete-server/delete.png":::

1. A notification informs you that the server is being deleted.

   :::image type="content" source="media/how-to-delete-server/notification-deleting-server.png" alt-text="Screenshot showing a server that's being deleted." lightbox="media/how-to-delete-server/notification-deleting-server.png":::

1. When the process completes, a notification informs you that the server was successfully deleted.

   :::image type="content" source="media/how-to-delete-server/notification-deleted-server.png" alt-text="Screenshot showing a server that was successfully deleted." lightbox="media/how-to-delete-server/notification-deleted-server.png":::

### [CLI](#tab/cli-reset-admin-password)

You can delete a server via the [az postgres flexible-server delete](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-delete) command.

```azurecli-interactive
az postgres flexible-server delete \
  --resource-group <resource_group> \
  --name <server>
```

If you run the previous command, it requires you to explicitly confirm, responding with a `y` (yes):

```output
Are you sure you want to delete the server '<server>' in resource group '<resource_group>' (y/n):
```

If you want to run the command without needing the user interaction, you can add the `--yes` parameter like this:

```azurecli-interactive
az postgres flexible-server delete \
  --resource-group <resource_group> \
  --name <server> \
  --yes
```

---

## Related content

- [Start compute of a server in Azure HorizonDB](how-to-start-server.md)
- [Stop compute of a server in Azure HorizonDB](how-to-stop-server.md)
- [Restart PostgreSQL engine in Azure HorizonDB](how-to-restart-server.md)
- [Reset administrator password in Azure HorizonDB](../security/security-reset-admin-password.md)
- [Configure storage autogrow in Azure HorizonDB](../scale/how-to-auto-grow-storage.md)
