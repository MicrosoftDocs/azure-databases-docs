---
 ms.service: azure-cosmos-db
 ms.topic: include
 ms.date: 08/23/2024
---

## <a id="addregion"></a>Add global database regions using the Azure portal
Azure Cosmos DB is available in all [Azure regions][azureregions] worldwide. After selecting the default consistency level for your database account, you can associate one or more regions (depending on your choice of default consistency level and global distribution needs).

1. In the [Azure portal](https://portal.azure.com/), in the left bar, click **Azure Cosmos DB**.
2. In the **Azure Cosmos DB** page, select the database account to modify.
3. In the account page, click **Replicate data globally** from the menu.
4. In the **Replicate data globally** page, select the regions to add or remove by clicking regions in the map, and then click **Save**. There is a cost to adding regions, see the [pricing page](https://azure.microsoft.com/pricing/details/cosmos-db/) or the [Distribute data globally with Azure Cosmos DB](../distribute-data-globally.md) article for more information.
   
    ![Click the regions in the map to add or remove them][1]
    
Once you add a second region, the **Manual Failover** option is enabled on the **Replicate data globally** page in the portal. You can use this option to test the failover process or change the primary write region. Once you add a third region, the **Failover Priorities** option is enabled on the same page so that you can change the failover order for reads.  

### Selecting global database regions
There are two common scenarios for configuring two or more regions:

1. Delivering low-latency access to data to end users no matter where they are located around the globe
2. Adding regional resiliency for business continuity and disaster recovery (BCDR)

For delivering low-latency to end users, it is recommended that you deploy both the application and Azure Cosmos DB in the regions that correspond to where the application's users are located.

For BCDR, it is recommended to add regions based on the region pairs described in the [Cross-region replication in Azure: Business continuity and disaster recovery](/azure/reliability/cross-region-replication-azure) article.

[1]: ./media/cosmos-db-tutorial-global-distribution-portal/azure-cosmos-db-add-region.png
[2]: ./media/cosmos-db-tutorial-global-distribution-portal/azure-cosmos-db-manual-failover-1.png
[3]: ./media/cosmos-db-tutorial-global-distribution-portal/azure-cosmos-db-manual-failover-2.png

[consistency]: ../consistency-levels.md
[azureregions]: https://azure.microsoft.com/regions/#services
[offers]: https://azure.microsoft.com/pricing/details/cosmos-db/
