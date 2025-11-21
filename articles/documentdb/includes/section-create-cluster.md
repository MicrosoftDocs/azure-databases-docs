---
ms.topic: include
ms.date: 09/29/2025
---

To get started, you first need to create an Azure DocumentDB cluster, which serves as the foundation for storing and managing your NoSQL data.

1. Sign in to the **Azure portal** (<https://portal.azure.com>).

1. From the Azure portal menu or the **Home page**, select **Create a resource**.

1. On the **New** page, search for and select **Azure DocumentDB**.

    :::image type="content" source="media/quickstart-portal/select-azure-documentdb.png" alt-text="Screenshot showing search for Azure DocumentDB.":::

1. On the **Create Azure DocumentDB cluster** page and within the **Basics** section, select the **Configure** option within the **Cluster tier** section.

    :::image type="content" source="media/quickstart-portal/select-configure-option.png" alt-text="Screenshot showing Configure cluster option.":::

1. On the **Scale** page, configure these options and then select **Save** to persist your changes to the cluster tier.

    | | Value |
    | --- | --- |
    | **Cluster tier** | `M30 tier, 2 vCore, 8-GiB RAM` |
    | **Storage per shard** | `128 GiB` |

    :::image type="content" source="media/quickstart-portal/configure-compute-and-storage.png" alt-text="Screenshot of configuration options for compute and storage for a new Azure DocumentDB cluster.":::


1. Back in the **Basics** section, configure the following options:

    | | Value |
    | --- | --- |
    | **Subscription** | Select your Azure subscription |
    | **Resource group** | Create a new resource group or select an existing resource group |
    | **Cluster name** | 	Provide a globally unique name |
    | **Location** | Select a supported Azure region for your subscription |
    | **MongoDB version** | Select `8.0` |
    | **Admin username** | Create a username to access the cluster as a user administrator |
    | **Password** | Use a unique password associated with the username |

    :::image type="content" source="media/quickstart-portal/enter-cluster-configurations.png" alt-text="Screenshot showing cluster parameters.":::

    > [!TIP]
    > Record the values you use for **username** and **password**. These values are used later in this guide. For more information about valid values, see [cluster limitations](../limitations.md).


1. Select **Next: Networking**.

1. In the **Firewall rules** section on the **Networking** tab, configure these options:

    | | Value |
    | --- | --- |
    | **Connectivity method** | `Public access` |
    | **Allow public access from Azure services and resources within Azure to this cluster** | *Enabled* |

1. Add a firewall rule for your current client device to grant access to the cluster by selecting **+ Add current client IP address**.

    :::image type="content" source="media/quickstart-portal/select-networking.png" alt-text="Screenshot showing network configurations.":::

    > [!TIP]
    > In many corporate environments, developer machine IP addresses are hidden due to a VPN or other corporate network settings. In these cases, you can temporarily allow access to all IP addresses by adding the `0.0.0.0` - `255.255.255.255` IP address range as a firewall rule. Use this firewall rule only temporarily as a part of connection testing and development.


1. Select **Review + create**.

1. Review the settings you provide, and then select **Create**. It takes a few minutes to create the cluster. Wait for the resource deployment is complete.

1. Finally, select **Go to resource** to navigate to the Azure DocumentDB cluster in the portal.

:::image type="content" source="media/quickstart-portal/go-to-resource.png" alt-text="Screenshot showing goto resource options.":::
