---
title: Azure Cosmos DB pricing & discounts with Reserved Capacity
description: Azure Cosmos DB pricing allows for various forms of optimization. You may receive discounts of up to 63% savings with Reserved Capacity.
author: aliuy
ms.service: azure-cosmos-db
ms.topic: concept-article
ms.date: 12/16/2025
ms.author: andrl
---

# Azure Cosmos DB pricing & discounts with Reserved Capacity
[!INCLUDE[NoSQL, MongoDB, Cassandra, Gremlin, Table](includes/appliesto-nosql-mongodb-cassandra-gremlin-table.md)]

Azure Cosmos DB Reserved Capacity allows you to benefit from discounted prices on the throughput provisioned for your Azure Cosmos DB resources. You can enjoy up to 63% savings by committing to a reservation for Azure Cosmos DB resources for either one year or three years. Examples of resources are databases and containers (tables, collections, and graphs). It doesn’t cover networking or storage.

## How Azure Cosmos DB pricing and discounts work with Reserved Capacity

The size of the Reserved Capacity purchase should be based on the total amount of throughput that the existing or soon-to-be-deployed Azure Cosmos DB resources use on an hourly basis.

For example: Purchase 10,000 RU/s Reserved Capacity if that is your consistent hourly usage pattern. In this case, provisioned throughput exceeding 10,000 RU/s is billed with your pay-as-you-go rate. However, if your usage pattern is consistently below 10,000 RU/s in an hour, you should reduce your Reserved Capacity accordingly to avoid waste. 

Note that:

 * There is no limit to the number of reservations.
 * It's possible to buy more reservations at any moment.
 * It's possible to buy different reservations in the same purchase.

After you buy a reservation, it's applied immediately to any existing Azure Cosmos DB resources that match the terms of the reservation. If you don’t have any existing Azure Cosmos DB resources, the reservation applies when you deploy a new Azure Cosmos DB instance that matches the terms of the reservation. In both cases, the period of the reservation starts immediately after a successful purchase.

When your reservation expires, your Azure Cosmos DB instances continue to run and are billed at the regular pay-as-you-go rates.
You can buy Azure Cosmos DB Reserved Capacity from the [Azure portal](https://portal.azure.com). Pay for the reservation [upfront or with monthly payments](/azure/cost-management-billing/reservations/prepare-buy-reservation). 

## Unused Reserved Capacity and reservations exchange

A reservation discount is *use-it-or-lose-it*. So, if you don't have matching resources for any hour, then you lose a reservation quantity for that hour. You can't carry forward unused reserved hours.

When you shut down a resource, the reservation discount automatically applies to another matching resource in the specified scope. If no matching resources are found in the specified scope, then the reserved hours are *lost*.

Stopped resources are billed and continue to use reservation hours. To use your available reservation hours with other workloads, deallocate or delete resources or scale-in other resources.

Customers can use a self-service process to exchange reservations, migrating existing ones for bigger or smaller options. There is no penalty for exchanges that are processed as a refund and a repurchase. Different transactions are created for the cancellation and the new reservation purchase. The prorated reservation amount is refunded for the reservations that's traded-in. You're charged fully for the new purchase. The prorated reservation amount is the daily prorated residual value of the reservation being returned. For more information about reservations exchanges, check the [exchanges and refunds](/azure/cost-management-billing/reservations/exchange-and-refund-azure-reservations) documentation.


## Required permissions

The required permissions to purchase Reserved Capacity for Azure Cosmos DB are:

* To buy a reservation, you must have owner role or reservation purchaser role on an Azure subscription.
* For Enterprise subscriptions, **Add Reserved Instances** must be enabled in the [EA portal](https://ea.azure.com). Or, if that setting is disabled, you must be an EA Admin on the subscription.
* For the Cloud Solution Provider (CSP) program, only admin agents or sales agents can buy Azure Cosmos DB Reserved Capacity.

## Reservation discount per region
The reservation discount applies to throughput usage in different regions using the following ratios:

|Region |Ratio  |
|---------|---------|
|    IN South     |    1.0375    |
|   CA East      |    1.1      |
|   JA East      |    1.125     |
|     JA West    |   1.125       |
|    IN West    |    1.1375     |
|   IN Central     |  1.1375       |
|    AU East    |   1.15       |
| CA Central       |   1.2       |
|   FR Central      |    1.25      |
| BR South       |   1.5      |
|  AU Central      |   1.5      |
| AU Central 2        |    1.5     |
|   FR South     |    1.625     |
| All other regions | 1.0 |

The Azure billing system assigns the reservation billing benefit to the first region that was added to the database account and that matches the reservation configuration. Please check the examples.


## Azure Cosmos DB pricing discount tiers with Reserved Capacity

Azure Cosmos DB Reserved Capacity can significantly reduce your Azure Cosmos DB costs, up to 63% on regular prices, with a one-year or three-year upfront commitment. Reserved capacity provides a billing discount and doesn't affect the state of your Azure Cosmos DB resources, including performance and availability.

We offer both fixed and progressive discounts options. Note that you can mix and match different reservations options and sizes in the same purchase.

### Fixed discounts reservations

This option, using multiples of the 100 RU/s, allows you to reserve any capacity between 100 and 999,900 RU/s, with fixed discounts:

| Reservation | One-Year Single Discount  | Three-Years  Discount
|---------|---------|---------|
| 100 RU/s |  20% | 30% |
| 100 Multi-master RU/s |  20% | 30% |

For more than 999,900 RU/s, you can reduce costs with progressive discounts.

### Progressive discounts reservations

This option, using multiples of our bigger reservation sizes, allows you to reserve any capacity starting on 1,000,000 RU/s, with progressive discounts:

| Reservation  | One-Year Discount  | Three-Years Discount |
|---------|---------|---------|
| 1,000,000 RU/s | 27.0% | 39.5% | 
| 1,000,000 Multi-master | 32.0% | 44.5% |
| 2,000,000 RU/s | 28.5% | 42.3% |
| 2,000,000 Multi-master RU/s | 33.5% | 47.3% |
| 3,000,000 RU/s | 29.0% | 43.2% |
| 3,000,000 Multi-master RU/s | 34.0% | 48.2% |
| 5,000,000 RU/s | 35.4% | 49.9% |
| 5,000,000 Multi-master RU/s |  40.4% | 54.9% |
| 10,000,000 RU/s | 40.2% | 55.0% | 
| 10,000,000 Multi-master RU/s | 45.2% | 60.0% |
| 20,000,000 RU/s | 42.6% | 57.5% |
| 20,000,000 Multi-master RU/s | 47.6% | 62.5% |
| 30,000,000 RU/s | 43.4% | 58.3% |
| 30,000,000 Multi-master RU/s | 48.4% | 63.3% |

You can maximize savings with the biggest reservation for your scenario. Example: You need 2,000,000 RU/s, one year term. If you purchase two units of the 1,000,000 RU/s reservation, your discount is 27.0%. If you purchase one unit of the 2,000,000 RU/s reservation, you have exactly the same Reserved Capacity, but a 28.5% discount.

You can combine multiple reservations to fit quantities that don't have a dedidcated SKU. For example, you can reserve 6,000,000 RU/s by adding 5,000,000 RU/s + 1,000,000 RU/s reservation.

Reservations larger than or equal to 1,000,000 RU/sec are hidden by default. You can access large reservations in the Azure Portal through this [link](https://portal.azure.com/?allCosmosDbSkus=true#view/Microsoft_Azure_Reservations/CreateBlade/referrer/PurchaseNowButton/productType/Reservation).

## Azure Pricing Calculator

The [Azure Pricing Calculator](https://azure.microsoft.com/pricing/calculator) uses multiples of 100 RU/s minimum reservation to predict the price. If you check the price for 100 RU/s in autoscale mode, due to the 1.5 multiplication factor, you will need 150 RU/s. And for 150 RU/s, the calculator will use 2 units of 100 RU/s reservation. And 2 units of 100 RU/s reservation are more expensive than 100 RU/s. But this is a calculator specific behavior. For the same situation, you can purchase only 1 unit of the 100 RU/s minimum reservation and pay as you go the other 50 RU/s required RU/s. 

Also, when you use the calculator for autoscale scenarios with less than 100% utilization, you may see that a reservation could be more expensive. This issue happens because of the fact that reservations always use 100% utilization. The Reservations system has a recommendation engine so that you can choose the best reservation size for your scenario.
 


## Reservations consumption

As soon as you buy a reservation, the throughput charges that match the reservation attributes are no longer charged at the pay-as-you go rates. For more information on reservations, see the [Azure reservations](/azure/cost-management-billing/reservations/save-compute-costs-reservations) article.

Please note that single write region autoscale database operations use RU/s with a 1.5 multiplier factor. With that, we have the following formulas for the reservations consumption:

 * Single region standard throughput: RUs * Regional Ratio
 * Multi region standard throughput: RUs * Regional Ratio for each region, in the order that the regions were added to the database account.
 * Single region autoscale throughput: RUs * 1.5 * Regional Ratio
 * Multi region autoscale throughput: RUs * 1.5 * Regional Ratio for each region, in the order that the regions were added to the database account.

### Consumption examples

Consider the following requirements for a reservation:

* Required throughput per region: 50,000 RU/s  
* Regions used: 2

In this case, your total on-demand charges are for 500 quantity of 100 RU/s meter in these two regions. The total RU/s consumption is 100,000 every hour.

#### Example 1 - Two regions with a 1.0 ratio and standard throughput

For example, assume that you need Azure Cosmos DB standard throughput deployments in the US North Central and US West regions. Each region has a throughput consumption of 50,000 RU/s. A reservation purchase of 100,000 RU/s would completely balance your on-demand charges. The discount that a reservation covers is computed as: throughput consumption * reservation_discount_ratio_for_that_region. For the US North Central and US West regions, the reservation discount ratio is 1.0. So, the total discounted RU/s are 100,000. This value is computed as: 50,000 * 1.0 + 50,000 * 1.0 = 100,000 RU/s. You don't have to pay any other charges at the regular pay-as-you-go rates.

|Meter description | Quantity|Region |Region ratio |Throughput consumption (RU/s) |Reservation consumption formula| Reservation discount applied to RU/s | Pay as you go RU/s|
|---------|---------|---------|---------|---------|---------|---------|---------|
|Azure Cosmos DB - 100 RU/s/Hour - US North Central  | 500|US North Central| 1.0  | 50,000   |50,000 * 1.0 = 50,000 | 50,000 of the reservation| 0 |
|Azure Cosmos DB - 100 RU/s/Hour - US West  | 500  | US West               |1.0   |  50,000  |50,000 * 1.0 = 50,000 | The remaining 50,000 of the reservation | 0 |

#### Example 2 - Two regions with different ratios and standard throughput

For example, assume that you need Azure Cosmos DB standard throughput deployments in the AU Central 2 and FR South regions. Each region has a throughput consumption of 50,000 RU/s. A reservation purchase of 100,000 RU/s would be applicable as follows (assuming that AU Central 2 usage was added first to the database account):

|Meter description | Quantity|Region |Region ratio |Throughput consumption (RU/s) |Reservation consumption formula|Final reservation discount applied to RU/s |  Pay as You go RU/s|
|---------|---------|---------|---------|---------|---------|---------|---------|
|Azure Cosmos DB - 100 RU/s/Hour - AU Central 2  | 500 | AU Central 2 |1.5  |  50,000 | 50,000 * 1.5 = 75,000 | 75,000 of the 100,000 reservation   | 0 |
|Azure Cosmos DB - 100 RU/s/Hour - FR South  | 500 |FR South   |1.625 | 50,000 | 50,000 * 1.625 = 81,250 | The remaining 25,000 of the reservation| (81,250 - 25,000) / 1.625 = 34,616|

*  A usage of 50,000 units in the AU Central 2 region corresponds to 75,000 RU/s of billable reservation usage (or normalized usage). This value is computed as: throughput consumption * reservation_discount_ratio_for_that_region. The computation equals 75,000 RU/s of billable or normalized usage. This value is computed as: 50,000 * 1.5 = 75,000 RU/s.

* A usage of 50,000 units in the FR South region corresponds to  50,000 * 1.625 = 81,250 RU/s reservation is needed.

* Total reservation purchase is 100,000. Because AU central2 region uses 75,000 RU/s, which leaves 25,000 RU/s for the other region.

* For the FR south region, a 25,000 RU/s reservation purchase is used and it leaves 56,250 reservation RU/s (81,250 – 25,000 = 56,250 Ru/s).

* 56,250 RU/s are required when using reservation. To pay for the RU/s with regular pricing, you need to convert it into regular RU/s by dividing with the reservation ratio 56,250 / 1.625 = 34,616 RU/s. Regular RU/s are charged at the normal pay-as-you-go rates.

#### Example 3 - Two regions with a 1.0 ratio and autoscale throughput

For example, assume that you need Azure Cosmos DB autoscale throughput deployments in the US North Central and US West regions. Each region has a throughput consumption of 50,000 RU/s. A reservation purchase of 100,000 RU/s won't completely balance your on-demand charges. The discount that a reservation covers is computed as: throughput consumption * reservation_discount_ratio_for_that_region * autoscale_ratio. For the US North Central and US West regions, the reservation discount ratio is 1.0.

|Meter description | Quantity|Region |Region ratio |Autoscale ratio |Throughput consumption (RU/s) |Reservation consumption formula| Reservation discount applied to RU/s | Pay as you go RU/s|
|---------|---------|---------|---------|---------|---------|---------|---------|---------|
|Azure Cosmos DB - 100 RU/s/Hour - US North Central  | 500|US North Central| 1.0  | 1.5 |50,000  |50,000 * 1.0 * 1.5 = 75,000 |75,000 of the 100,000 reservation | 0 |
|Azure Cosmos DB - 100 RU/s/Hour - US West  | 500  | US West               |1.0   | 1.5 |50,000  |50,000 * 1.0 * 1.5 = 75,000| The remaining 25,000  of the reservation | (75,000-25,000)/1.0 = 50,000 |

## Purchase sample scenario 1

Imagine this hypothetical scenario: A company is working on a new application but isn't sure about the throughput requirements, they purchased RU/s on 3 different days.

* On day 1 they purchased Reserved Capacity for their development environment:
  * Total of 800 RU/s: eight units of the 100 RU/s option, with a 20% discount. 
  * Scoped to the development resource group.
  * One year term, since the project lasts for nine months.
  * They paid upfront, it's a small value.
* On day 30 they purchased Reserved Capacity for their tests environment:
  * 750,000 RU/s: 7,500 units of the 100 RU/s option, with a 20% discount.
  * Scoped to the test subscription.
  * One year term.
  * They choose to pay monthly.
* On day 180 they purchased Reserved Capacity for the production environment:
  * 3,500,000 RU/s: One unit of the 3,000,000 RU/s option, with a 43.2% discount. And 5,000 units of the 100 RU/s option, with a 20% discount.
  * Scoped to the production subscription.
  * Three-years term, to maximize the discounts.
  * They choose to pay monthly too.

## Purchase sample scenario 2

Imagine this hypothetical scenario: A company needs a 10,950,000 three-years reservation. In the same purchase they got:

 * One unit of the 10,000,000 RU/s reservation, paid monthly.
 * 9,000 units of the 100 RU/s reservation, paid monthly.
 * 500 units of the 100 RU/s reservation, paid upfront.

## Determine the required throughput before purchase

We calculate purchase recommendations based on your hourly usage pattern. Usage over the last 7, 30, and 60 days is analyzed, and Reserved Capacity purchase that maximizes your savings is recommended. You can view recommended reservation sizes in the Azure portal using the following steps:

1. Sign in to the [Azure portal](https://portal.azure.com).

2. Select **All services** > **Reservations** > **Add**.

3. From the **Purchase reservations** pane, choose **Azure Cosmos DB**.

4. Select the **Recommended** tab to view recommended reservations:

You can filter recommendations by the following attributes:

- **Term** (One year or Three years)
- **Billing frequency** (Monthly or Upfront)
- **Throughput Type** (RU/s vs multi-region write RU/s)

Additionally, you can scope recommendations to be within a single resource group, single subscription, or your entire Azure enrollment. 

Here's an example recommendation:

:::image type="content" source="./media/reserved-capacity/reserved-capacity-recommendation.png" alt-text="Reserved Capacity recommendations":::

This recommendation to purchase a 30,000 RU/s reservation indicates that, among three year reservations, a 30,000 RU/s reservation size maximizes your savings. In this case, the recommendation is calculated based on the past 30 days of Azure Cosmos DB usage. If this recommendation, based on the past 30 days of Azure Cosmos DB usage, isn't representative of future use, then choose another recommendation period.

For a 30,000 RU/s reservation, in standard provisioned throughput, you should buy 300 units of the 100 RU/s option.


## How to buy Reserved Capacity

1. Divide the reservation size you want by 100 to calculate the number of units of the 100 RU/s option you need. The maximum quantity is 9,999 units, or 999,900 RU/s. Large reservations for >= 1 million RU/s can be found using the following [link](https://portal.azure.com/?allCosmosDbSkus=true#view/Microsoft_Azure_Reservations/CreateBlade/referrer/PurchaseNowButton/productType/Reservation).

2. Sign in to the [Azure portal](https://portal.azure.com).

3. Select **All services** > **Reservations** > **Add**.  

4. From the **Purchase reservations** pane, choose **Azure Cosmos DB** to buy a new reservation.  

5. Select the correct scope, billing subscription, management group if applicable, resource group if applicable, and the reservation size. The following table explains all options:


   |Field  |Description  |
   |---------|---------|
   |Scope   |  	Option that controls how many subscriptions can use the billing benefit associated with the reservation. It also controls how the reservation is applied to specific subscriptions. <br/><br/>  If you select **Shared**, the reservation discount is applied to Azure Cosmos DB instances that run in any subscription within your billing context. The billing context is based on how you signed up for Azure. For enterprise customers, the shared scope is the enrollment and includes all subscriptions within the enrollment. For pay-as-you-go customers, the shared scope is all individual subscriptions with pay-as-you-go rates created by the account administrator. </br></br>If you select **Management group**, the reservation discount is applied to Azure Cosmos DB instances that run in any of the subscriptions that are a part of both the management group and billing scope. <br/><br/>  If you select **Single subscription**, the reservation discount is applied to Azure Cosmos DB instances in the selected subscription. <br/><br/> If you select **Single resource group**, the reservation discount is applied to Azure Cosmos DB instances in the selected subscription and the selected resource group within that subscription. <br/><br/> You can change the reservation scope after you buy the Reserved Capacity.  |
   |Subscription  |   Subscription used to pay for the Azure Cosmos DB Reserved Capacity. The payment method on the selected subscription is used in charging the costs. The subscription must be one of the following types: <br/><br/>  Enterprise Agreement (offer numbers: MS-AZR-0017P or MS-AZR-0148P): For an Enterprise subscription, the charges are deducted from the enrollment's Azure Prepayment (previously called monetary commitment) balance or charged as overage. <br/><br/> Individual subscription with pay-as-you-go rates (offer numbers: MS-AZR-0003P or MS-AZR-0023P): For an individual subscription with pay-as-you-go rates, the charges are billed to the credit card or invoice payment method on the subscription.    |
   | Resource Group | Resource group to which the Reserved Capacity discount is applied. |
   |Term  |   One year or three years.   |
   |Throughput Type   |  Throughput is provisioned as request units. You can buy a reservation for the provisioned throughput for both setups - single region writes and multi-master writes. The throughput type has two values to choose from: 100 RU/s per hour and 100 multi-region writes RU/s per hour.|
   | Reserved Capacity Units| The amount of throughput that you want to reserve. You can calculate this value by determining the throughput needed for all your Azure Cosmos DB resources (for example, databases or containers) per region. You then multiply it by the number of regions that you associate with your Azure Cosmos DB database. For example: If you have five regions with 1 million RU/sec in every region, select 5 million RU/s for the reservation capacity purchase. |


6. Click on the **Add to cart** blue button on the lower right corner, and then on **View Cart** when you are done. The quantities are defined next. Note that you can add different options to the cart. Example: If you need 1,100,000 RU/s, you should add both the 1,000,000 RU/s and the 100 RU/s options to the cart. 

7. In the **Purchase reservations** pane, review the billing frequency, the quantity, the discount, and the price of the reservation. This reservation price applies to Azure Cosmos DB resources with throughput provisioned across all regions. Example: You need 500,000 RU/s with auto-renew for your production environment within a specific scope, 82,000 RU/s for your tests resource group, and 10,000 RU/s for the development subscription. You can see in the image how a reservations shopping cart looks like for this scenario.

   :::image type="content" source="./media/reserved-capacity/reserved-capacity-summary.png" alt-text="Reserved capacity summary":::

10. Select **Review + buy** and then **buy now**.

## Cancel, exchange, or refund reservations

You can cancel, exchange, or refund reservations with certain limitations. For more information, see [Self-service exchanges and refunds for Azure Reservations](/azure/cost-management-billing/reservations/exchange-and-refund-azure-reservations).

### Exceeding Reserved Capacity

When you reserve capacity for your Azure Cosmos DB resources, you are reserving [provisioned throughput](set-throughput.md). If the provisioned throughput is exceeded, requests beyond that provisioning amount are billed using pay-as-you go rates. For more information on reservations, see the [Azure reservations](/azure/cost-management-billing/reservations/save-compute-costs-reservations) article. For more information on provisioned throughput, see [provisioned throughput types](how-to-choose-offer.md#overview-of-provisioned-throughput-types).

## Limitations

 * Currently we don't support reservations for Serverless accounts.
 * Currently we don't support reservations for storage or network.

## Next steps

The reservation discount is applied automatically to the Azure Cosmos DB resources that match the reservation scope and attributes. You can update the scope of the reservation through the Azure portal, PowerShell, Azure CLI, or the API.

*  To learn how Reserved Capacity discounts are applied to Azure Cosmos DB, see [Understand the Azure reservation discount](/azure/cost-management-billing/reservations/understand-cosmosdb-reservation-charges).

* To learn more about Azure reservations, see the following articles:

   * [What are Azure reservations?](/azure/cost-management-billing/reservations/save-compute-costs-reservations)  
   * [Manage Azure reservations](/azure/cost-management-billing/reservations/manage-reserved-vm-instance)  
   * [Understand reservation usage for your Enterprise enrollment](/azure/cost-management-billing/reservations/understand-reserved-instance-usage-ea)  
   * [Understand reservation usage for your pay-as-you-go subscription](/azure/cost-management-billing/reservations/understand-reserved-instance-usage)
   * [Azure reservations in the Partner Center CSP program](/partner-center/azure-reservations)

Trying to do capacity planning for a migration to Azure Cosmos DB? You can use information about your existing database cluster for capacity planning.
* If all you know is the number of vCores and servers in your existing database cluster, read about [estimating request units using vCores or vCPUs](convert-vcore-to-request-unit.md) 
* If you know typical request rates for your current database workload, read about [estimating request units using Azure Cosmos DB capacity planner](estimate-ru-with-capacity-planner.md)

## Need help? Contact us.

If you have questions or need help, [create a support request](https://portal.azure.com/#blade/Microsoft_Azure_Support/HelpAndSupportBlade/newsupportrequest).
