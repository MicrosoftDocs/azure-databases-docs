---
title: Upgrade a cluster
description: Steps to upgrade Azure DocumentDB cluster from a lower version to latest version.
author: suvishodcitus
ms.author: suvishod
ms.custom:
  - sfi-image-nochange
ms.topic: how-to
ms.date: 07/22/2024
---

# Upgrade a cluster in Azure DocumentDB

Azure DocumentDB provide customers with a convenient self-service option to upgrade to the latest MongoDB version. This feature ensures a seamless upgrade path with just a click, allowing businesses to continue their operations without interruption.

## Prerequisites

[!INCLUDE[Prerequisite - Existing cluster](includes/prerequisite-existing-cluster.md)]

## Upgrade a cluster

Here are the detailed steps to upgrade a cluster to latest version:

1. Sign in to the [Azure portal](https://portal.azure.com).

2. Go to the **Overview** blade of your Azure DocumentDB cluster and click the **Upgrade** button as illustrated below.

   :::image type="content" source="media/how-to-scale-cluster/upgrade-overview-page.png" alt-text="Screenshot of the overview page.":::

   > [!NOTE]
   > The upgrade button will stay disabled if you're already using the latest version.

3. A new window will appear on the right, allowing you to choose the MongoDB version you wish to upgrade to. Select the appropriate version and submit the upgrade request.

   :::image type="content" source="media/how-to-scale-cluster/upgrade-side-window.png" alt-text="Screenshot of server upgrade page.":::

## Next steps

In this guide, we'll learn more about point in time restore(PITR) on Azure DocumentDB.

> [!div class="nextstepaction"]
> [Restore cluster](how-to-restore-cluster.md)
