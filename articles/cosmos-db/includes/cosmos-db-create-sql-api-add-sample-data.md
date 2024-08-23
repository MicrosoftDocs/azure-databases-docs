---
 services: cosmos-db
 ms.service: azure-cosmos-db
 ms.topic: include
 ms.date: 08/23/2024
---
You can now add data to your new container using Data Explorer.

1. From the **Data Explorer**, expand the **Tasks** database, expand the **Items** container. Select **Items**, and then select **New Item**.

   ![Create new documents in Data Explorer in the Azure portal](./media/cosmos-db-create-sql-api-add-sample-data/azure-cosmosdb-data-explorer-new-document.png)
  
2. Now add a document to the container with the following structure.

     ```json
     {
         "id": "1",
         "category": "personal",
         "name": "groceries",
         "description": "Pick up apples and strawberries.",
         "isComplete": false
     }
     ```

3. Once you've added the json to the **Documents** tab, select **Save**.

    ![Copy in json data and select Save in Data Explorer in the Azure portal](./media/cosmos-db-create-sql-api-add-sample-data/azure-cosmosdb-data-explorer-save-document.png)

4.  Create and save one more document where you insert a unique value for the `id` property, and change the other properties as you see fit. Your new documents can have any structure you want as Azure Cosmos DB doesn't impose any schema on your data.