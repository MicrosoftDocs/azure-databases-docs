---
title: Autoscale on Azure DocumentDB
description: Autoscale on Azure DocumentDB.
author: suvishodcitus
ms.author: suvishod
ms.topic: concept-article
ms.date: 11/18/2024
ms.custom:
  - references_regions
# CustomerIntent: As a PM, we wanted to offer our customers a feature that allows database adapts immediately to changing workloads, eliminating performance bottlenecks 
---

# Autoscale for Azure DocumentDB

Managing databases with fluctuating workloads can be complex and costly, especially when unpredictable traffic spikes require overprovisioning resources. To address this 
challenge, Azure DocumentDB introduces Autoscale for its clusters. Autoscale is designed to handle variable workloads by dynamically adjusting capacity 
in real-time, scaling up or down based on application demands.

Unlike other managed MongoDB solutions, which often experience delays of several hours when scaling up and more than 24 hours 
for scaling down, Azure DocumentDB's Autoscale offers instant scalability. This feature ensures that your database adapts 
immediately to changing workloads, eliminating performance bottlenecks and avoiding unnecessary costs.

## Get started

Follow this document to [create a new Azure DocumentDB](quickstart-portal.md) cluster and select the 'M200-Autoscale tier' from the list of SKUs. 
Alternatively, you can also use [Bicep template](quickstart-bicep.md) to provision the resource.

:::image type="content" source="media/how-to-scale-cluster/provision-autoscale-tier.jpg" alt-text="Screenshot of the free tier provisioning.":::

## Benefits

- **Instant Scale**

  - Automatically adjusts capacity without downtime, maintaining performance during unexpected workload spikes.
  - Eliminates the need for manual scaling, reducing the risk of service disruptions.

- **Cost Efficiency**

  - Reduces expenses by preventing overprovisioning, utilizing resources only when necessary.
  - Pay-as-you-use pricing ensures that you’re only billed for actual usage, maximizing resource utilization.

- **Predictable Pricing**

  - Core-based pricing with transparent cost calculations makes budgeting and forecasting easier.
  - Flexible pricing model adapts to workload demands, avoiding unexpected cost spikes.

## Pricing Model

For simplicity it uses a core-based pricing model, where charges are based on the higher of CPU or memory usage 
in the last hour, compared to a 35% utilization threshold.

* Upto 35% Utilization: Minimum price applies.
* Above 35% Utilization: Maximum price applies.
* Autoscale clusters incur a 50% premium over the base tier due to their instant scaling capabilities.
* Billing Frequency: Costs are calculated and billed hourly, ensuring you only pay for the capacity you use.

### Example:
In a scenario where an application experiences usage spikes for 10% of its runtime:

* Without Autoscale: An overprovisioned M200 cluster would cost $1,185.24.
* With Autoscale: An M200-Autoscale cluster would cost only $968.41, offering a saving of 18.29%.

This flexible pricing model helps reduce costs while maintaining optimal performance during peak demand.

## Restrictions

- Currently, only the M200 Autoscale tier is supported, allowing scaling within the range of M80 to M200 tiers.
- Autoscale applies only to compute resources. Storage capacity must still be scaled manually.
- Upgrades or downgrades between the General Tier and Autoscale Tier aren't supported at this time.

## Frequently Asked Questions (FAQs)

### Which clusters support Autoscale?  
Currently, Autoscale is only available for the M200 tier, with scaling capabilities from **M80 to M200**.  

### Does Autoscale manage both compute and storage scaling?  
No, Autoscale only manages compute resources. Storage must be scaled manually.  

### Can I switch between the General Tier and Autoscale Tier?  
Yes, upgrades and downgrades between the General Tier and Autoscale Tier are supported. However, downscaling from M200-Autoscale to M200 isn't available at this time. 

### Is there any downtime when Autoscale adjusts capacity?  
No, Autoscale adjusts capacity instantly and seamlessly, without any downtime or performance impact.  

### What happens if my workload exceeds the M200 tier limits?  
If your workload consistently exceeds M200 limits, consider a higher tier or alternative scaling strategies, as Autoscale currently supports up to M200.  

### Is Autoscale available in all Azure regions?  
Autoscale availability varies by region. Check the Azure portal for support in your preferred region.  

### How can I verify the charges incurred with Autoscale?  
To ensure cost transparency, we’ve introduced a new metric called 'Autoscale Utilization Percentage'. 
This metric shows the maximum of CPU or memory usage over time, helping you compare it against the charges incurred.  

<a href="media/how-to-scale-cluster/autoscale-metric.jpg" target="_blank">
  <img src="media/how-to-scale-cluster/autoscale-metric.jpg" alt="Screenshot for autoscale usage metric." width="600">
</a>


## Next steps

Having explored the capabilities of the Autoscale tier in Azure DocumentDB, the next step is to dive into the migration journey. This involves understanding how to conduct a migration assessment and planning a seamless transfer of your existing MongoDB workloads to Azure.

> [!div class="nextstepaction"]
> [Migration options for Azure DocumentDB](migration-options.md)
