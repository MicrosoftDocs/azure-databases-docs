---
title: Delete a Server in Azure HorizonDB
description: This article describes the steps to delete an existing Azure HorizonDB instance.
author: avnishrastogimsft
ms.author: avrastog
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-database-postgresql
ms.subservice: configuration
ms.topic: how-to
# customer intent: As a user, I want to learn how to delete an Azure HorizonDB instance.
---

# Delete a server in Azure HorizonDB

This article provides step-by-step instructions to delete an Azure HorizonDB instance.

## Delete a server

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure HorizonDB instance.

2. In the resource menu, select **Overview**.

   :::image type="content" source="media/how-to-delete-server/overview.png" alt-text="Screenshot showing how to select the Overview page." lightbox="media/how-to-delete-server/overview.png":::

3. Select the **Delete** button.

   :::image type="content" source="media/how-to-delete-server/delete-server.png" alt-text="Screenshot showing how to delete an Azure HorizonDB instance." lightbox="media/how-to-delete-server/delete-server.png":::

4. In the **Delete *\<server\>*** panel, make sure that the name of the resource you're willing to delete, matches the one displayed.

   :::image type="content" source="media/how-to-delete-server/confirm-server-name.png" alt-text="Screenshot showing where to find the name of the server being deleted." lightbox="media/how-to-delete-server/confirm-server-name.png":::

5. Take the time to provide feedback about your experience with the service. Select the icon that best expresses your overall level of satisfaction with the service, and provide more details in free text form.

   :::image type="content" source="media/how-to-delete-server/provide-feedback.png" alt-text="Screenshot showing where to provide feedback." lightbox="media/how-to-delete-server/provide-feedback.png":::

6. You must check the **I have read and understand that this server, as well as any databases it contains, will be deleted.** box, so that the **Delete** button is enabled. Optionally, check the **You can contact me about this feedback.** box, if we can contact you about the feedback provided.

   :::image type="content" source="media/how-to-delete-server/accept-conditions.png" alt-text="Screenshot showing how to accept terms and consequences of triggering the deletion of an Azure HorizonDB instance." lightbox="media/how-to-delete-server/accept-conditions.png":::



7. Select **Delete** to proceed with the immediate deletion of the server.

   :::image type="content" source="media/how-to-delete-server/delete.png" alt-text="Screenshot showing the location of the Delete button to initiate the deletion of the server." lightbox="media/how-to-delete-server/delete.png":::

8. A notification informs you that the server is being deleted.

   :::image type="content" source="media/how-to-delete-server/notification-deleting-server.png" alt-text="Screenshot showing a server that's being deleted." lightbox="media/how-to-delete-server/notification-deleting-server.png":::

9. When the process completes, a notification informs you that the server was successfully deleted.

   :::image type="content" source="media/how-to-delete-server/notification-deleted-server.png" alt-text="Screenshot showing a server that was successfully deleted." lightbox="media/how-to-delete-server/notification-deleted-server.png":::



---

## Related content

- [Start compute of a server in Azure HorizonDB](how-to-start-server.md)
- [Stop compute of a server in Azure HorizonDB](how-to-stop-server.md)
- [Restart PostgreSQL engine in Azure HorizonDB](how-to-restart-server.md)


