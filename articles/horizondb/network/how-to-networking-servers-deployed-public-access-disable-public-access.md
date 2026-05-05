---
title: Disable Public Access in Azure HorizonDB
description: This article describes how to disable public access in Azure HorizonDB.
author: avnishrastogimsft
ms.author: avrastog
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-database-postgresql
ms.subservice: networking
ms.topic: how-to
# customer intent: As a user, I want to learn how to disable public network access in Azure HorizonDB.
---

# Disable public access in Azure HorizonDB

If you disable public access, connectivity to the server is only possible via private endpoints.

You must configure those private endpoints so that hosts that can route traffic to the Azure virtual network in which you inject the private endpoints, can access your Azure HorizonDB.

When public access is disabled, any firewall rules you created while public access was enabled, aren't enforced.

Also, any modifications made to the firewall rules are discarded.

## [Portal](#tab/portal-disable-public-access)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure HorizonDB.

1. In the resource menu, select **Networking**.

   :::image type="content" source="media/how-to-networking/public-access-networking-enabled.png" alt-text="Screenshot showing the Networking page." lightbox="media/how-to-networking/public-access-networking-enabled.png":::

1. Clear the **Allow public access to this resource through the internet using a public IP address** checkbox.

1. Select **Save**.

1. A notification informs you that the changes are being applied.

1. Also, the status of the server changes to **Updating**.

1. When the process completes, a notification informs you that the changes were applied.

1. Also, the status of the server changes to **Ready**.

<!--

## [CLI](#tab/CLI-disable-public-access)

You can disable public access on a server via the [az postgres flexible-server update](/CLI/azure/postgres/flexible-server#az-postgres-flexible-server-update) command.

```azurecli-interactive
az postgres flexible-server update \
  --resource-group <resource_group> \
  --name <server> \
  --public-access disabled
```
-->

If you attempt to disable public access on a server which isn't in `Ready` state, you receive an error like this:

```output
Code:
Message: Server <server> is busy with other operations. Please try later
```

If you attempt to disable public access on a server which wasn't deployed with networking mode public access (allowed IP addresses), you don't receive an error. The request to change that configuration is ignored.

<!--
To determine if a server has public access disabled or enabled, run the following command:

```azurecli-interactive
az postgres flexible-server show \
  --resource-group <resource_group> \
  --name <server> \
  --query '{"publicAccess":network.publicNetworkAccess}'
```
-->

---

## Related content

- [Networking in Azure HorizonDB](how-to-networking.md)
- [Enable public access in Azure HorizonDB](how-to-networking-servers-deployed-public-access-enable-public-access.md)
- [Add firewall rules in Azure HorizonDB](how-to-networking-servers-deployed-public-access-add-firewall-rules.md)
- [Delete firewall rules in Azure HorizonDB](how-to-networking-servers-deployed-public-access-delete-firewall-rules.md)
- [Add private endpoint connections in Azure HorizonDB](how-to-networking-servers-deployed-public-access-add-private-endpoint.md)
- [Delete private endpoint connections in Azure HorizonDB](how-to-networking-servers-deployed-public-access-delete-private-endpoint.md)
- [Approve private endpoint connections in Azure HorizonDB](how-to-networking-servers-deployed-public-access-approve-private-endpoint.md)
- [Reject private endpoint connections in Azure HorizonDB](how-to-networking-servers-deployed-public-access-reject-private-endpoint.md)
