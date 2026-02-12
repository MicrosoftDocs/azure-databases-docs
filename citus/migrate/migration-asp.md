---
title: "ASP.NET"
description: This article describes how to build multitenant ASP.NET applications that work with a Citus storage backend.
ms.date: 02/11/2026
ms.service: postgresql-citus
ms.topic: reference
monikerRange: "citus-13 || citus-14"
---

# ASP.NET

In [Identify a distribution strategy](migration-schema.md), we discussed the framework-agnostic database changes required for using Citus in the multitenant use case. This article investigates how to build multitenant ASP.NET applications that work with a Citus storage backend.

## Example app

To make this migration section concrete, let's consider a simplified version of StackExchange.

### Schema

We start with two tables:

```sql
CREATE TABLE tenants (
    id uuid NOT NULL,
    domain text NOT NULL,
    name text NOT NULL,
    description text NOT NULL,
    created_at timestamptz NOT NULL,
    updated_at timestamptz NOT NULL
);

CREATE TABLE questions (
    id uuid NOT NULL,
    tenant_id uuid NOT NULL,
    title text NOT NULL,
    votes int NOT NULL,
    created_at timestamptz NOT NULL,
    updated_at timestamptz NOT NULL
);

ALTER TABLE tenants ADD PRIMARY KEY (id);
ALTER TABLE questions ADD PRIMARY KEY (id, tenant_id);
```

Each tenant of our demo application connects via a different domain name. ASP.NET Core inspects incoming requests and looks up the domain in the `tenants` table. You could also look up tenants by subdomain (or any other scheme you want).

Notice how the `tenant_id` is also stored in the `questions` table. This structure makes it possible to colocate the data. With the tables created, use `create_distributed table` to tell Citus to shard on the tenant ID:

```sql
SELECT create_distributed_table('tenants', 'id');
SELECT create_distributed_table('questions', 'tenant_id');
```

Next include some test data.

```sql
INSERT INTO tenants VALUES (
    'c620f7ec-6b49-41e0-9913-08cfe81199af',
    'bufferoverflow.local',
    'Buffer Overflow',
    'Ask anything code-related!',
    now(),
    now());

INSERT INTO tenants VALUES (
    'b8a83a82-bb41-4bb3-bfaa-e923faab2ca4',
    'dboverflow.local',
    'Database Questions',
    'Figure out why your connection string is broken.',
    now(),
    now());

INSERT INTO questions VALUES (
    '347b7041-b421-4dc9-9e10-c64b8847fedf',
    'c620f7ec-6b49-41e0-9913-08cfe81199af',
    'How do you build apps in ASP.NET Core?',
    1,
    now(),
    now());

INSERT INTO questions VALUES (
    'a47ffcd2-635a-496e-8c65-c1cab53702a7',
    'b8a83a82-bb41-4bb3-bfaa-e923faab2ca4',
    'Using postgresql for multitenant data?',
    2,
    now(),
    now());
```

Now that our database structure and sample data are complete, we can move on to setting up ASP.NET Core.

### ASP.NET Core project

If you don't have ASP.NET Core installed, install the [.NET Core SDK from Microsoft](https://dot.net/core). These instructions use the `dotnet` CLI, but you can also use Visual Studio 2017 or newer if you are on Windows.

Create a new project from the MVC template with `dotnet new`:

```dotnetcli
dotnet new mvc -o QuestionExchange
cd QuestionExchange
```

You can preview the template site with `dotnet run` if you'd like. The Model-View-Controller (MVC) template includes almost everything you need to get started, but PostgreSQL support isn't included out of the box. You can add support by installing the [Npgsql.EntityFrameworkCore.PostgreSQL](https://www.nuget.org/packages/Npgsql.EntityFrameworkCore.PostgreSQL/) package:

```dotnetcli
dotnet add package Npgsql.EntityFrameworkCore.PostgreSQL
```

This package adds PostgreSQL support to Entity Framework Core, the default object-relational mapping (ORM) and database layer in ASP.NET Core. Open the `Startup.cs` file and add these lines anywhere in the `ConfigureServices` method:

``` csharp
var connectionString = "connection-string";

services.AddEntityFrameworkNpgsql()
    .AddDbContext<AppDbContext>(options => options.UseNpgsql(connectionString));
```

You also need to add these declarations at the top of the file:

``` csharp
using Microsoft.EntityFrameworkCore;
using QuestionExchange.Models;
```

Replace `connection-string` with your Citus connection string. Mine looks like this:

`Server=myformation.db.citusdata.com;Port=5432;Database=citus;Userid=citus;Password=mypassword;SslMode=Require;Trust Server Certificate=true;`

Next, you need to define a database context.

## Adding Tenancy to the app

Now that you have the database structure and sample data, you need to configure your ASP.NET Core application to recognize and handle different tenants. SaasKit provides middleware that intercepts incoming requests and identifies which tenant is making the request based on the domain name. This section walks you through setting up the tenant resolver and integrating it into your application pipeline.

### Define the Entity Framework Core context and models

The database context class provides an interface between your code and your database. Entity Framework Core uses it to understand what your [data schema](https://msdn.microsoft.com/library/jj679962(v=vs.113).aspx#Anchor_2) looks like, so you need to define what tables are available in your database.

Create a file called `AppDbContext.cs` in the project root, and add the following code:

``` csharp
using System.Linq;
using Microsoft.EntityFrameworkCore;
using QuestionExchange.Models;
namespace QuestionExchange
{
    public class AppDbContext : DbContext
    {
        public AppDbContext(DbContextOptions<AppDbContext> options)
            : base(options)
        {
        }

        public DbSet<Tenant> Tenants { get; set; }

        public DbSet<Question> Questions { get; set; }
    }
}
```

The two `DbSet` properties specify which C# classes to use to model the rows of each table. You create these classes next, but before you do that, add a new method below the `Questions` property:

``` csharp
protected override void OnModelCreating(ModelBuilder modelBuilder)
{
    var mapper = new Npgsql.NpgsqlSnakeCaseNameTranslator();
    var types = modelBuilder.Model.GetEntityTypes().ToList();

    // Refer to tables in snake_case internally
    types.ForEach(e => e.Relational().TableName = mapper.TranslateMemberName(e.Relational().TableName));

    // Refer to columns in snake_case internally
    types.SelectMany(e => e.GetProperties())
        .ToList()
        .ForEach(p => p.Relational().ColumnName = mapper.TranslateMemberName(p.Relational().ColumnName));
}
```

C# classes and properties are PascalCase by convention, but your PostgreSQL tables and columns are lowercase (and snake_case). The `OnModelCreating` method lets you override the default name translation and let Entity Framework Core know how to find the entities in your database.

Now you can add classes that represent tenants and questions. Create a `Tenant.cs` file in the Models directory:

``` csharp
using System;

namespace QuestionExchange.Models
{
    public class Tenant
    {
        public Guid Id { get; set; }

        public string Domain { get; set; }

        public string Name { get; set; }

        public string Description { get; set; }

        public DateTimeOffset CreatedAt { get; set; }

        public DateTimeOffset UpdatedAt { get; set; }
    }
}
```

And a `Question.cs` file, also in the Models directory:

``` csharp
using System;

namespace QuestionExchange.Models
{
    public class Question
    {
        public Guid Id { get; set; }

        public Tenant Tenant { get; set; }

        public string Title { get; set; }

        public int Votes { get; set; }

        public DateTimeOffset CreatedAt { get; set; }

        public DateTimeOffset UpdatedAt { get; set; }
    }
}
```

Notice the `Tenant` property. In the database, the question table contains a `tenant_id` column. Entity Framework Core is smart enough to figure out that this property represents a one-to-many relationship between tenants and questions. You use this property later when you query your data.

So far, you set up Entity Framework Core and the connection to Citus. The next step is adding multitenant support to the ASP.NET Core pipeline.

### Install SaasKit

[SaasKit](https://github.com/saaskit/saaskit) is an excellent piece of open-source ASP.NET Core middleware. This package makes it easy to make your `Startup` request pipeline [tenant-aware](http://benfoster.io/blog/asp-net-5-multitenancy), and is flexible enough to handle many different multi-tenancy use cases.

Install the [SaasKit.Multitenancy](https://www.nuget.org/packages/SaasKit.Multitenancy/) package:

```dotnetcli
dotnet add package SaasKit.Multitenancy
```

SaasKit needs two things to work: a tenant model and a tenant resolver. You already have the former (the `Tenant` class you created earlier), so create a new file in the project root called `CachingTenantResolver.cs`:

``` csharp
using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Caching.Memory;
using Microsoft.Extensions.Logging;
using SaasKit.Multitenancy;
using QuestionExchange.Models;

namespace QuestionExchange
{
    public class CachingTenantResolver : MemoryCacheTenantResolver<Tenant>
    {
        private readonly AppDbContext _context;

        public CachingTenantResolver(
            AppDbContext context, IMemoryCache cache, ILoggerFactory loggerFactory)
             : base(cache, loggerFactory)
        {
            _context = context;
        }

        // Resolver runs on cache misses
        protected override async Task<TenantContext<Tenant>> ResolveAsync(HttpContext context)
        {
            var subdomain = context.Request.Host.Host.ToLower();

            var tenant = await _context.Tenants
                .FirstOrDefaultAsync(t => t.Domain == subdomain);

            if (tenant == null) return null;

            return new TenantContext<Tenant>(tenant);
        }

        protected override MemoryCacheEntryOptions CreateCacheEntryOptions()
            => new MemoryCacheEntryOptions().SetAbsoluteExpiration(TimeSpan.FromHours(2));

        protected override string GetContextIdentifier(HttpContext context)
            => context.Request.Host.Host.ToLower();

        protected override IEnumerable<string> GetTenantIdentifiers(TenantContext<Tenant> context)
            => new string[] { context.Tenant.Domain };
    }
}
```

The `ResolveAsync` method does the heavy lifting. Given an incoming request, it queries the database and looks for a tenant matching the current domain. If it finds one, it passes a `TenantContext` back to SaasKit. All of the tenant resolution logic is up to you - you could separate tenants by subdomains, paths, or anything else you want.

This implementation uses a [tenant caching strategy](http://benfoster.io/blog/aspnet-core-multi-tenancy-tenant-lifetime) so you don't hit the database with a tenant lookup on every incoming request. After the first lookup, tenants are cached for two hours (you can change this interval to whatever makes sense).

With a tenant model and a tenant resolver ready to go, open up the `Startup` class and add this line anywhere inside the `ConfigureServices` method:

``` csharp
services.AddMultitenancy<Tenant, CachingTenantResolver>();
```

Next, add this line to the `Configure` method, underneath `UseStaticFiles` but **above** `UseMvc`:

``` csharp
app.UseMultitenancy<Tenant>();
```

The `Configure` method represents your actual request pipeline, so order matters!

### Update views

Now that all the pieces are in place, you can start referring to the current tenant in your code and views. Open up the `Views/Home/Index.cshtml` view and replace the whole file with this markup:

``` html
@inject Tenant Tenant
@model QuestionListViewModel

@{
    ViewData["Title"] = "Home Page";
}

<div class="row">
    <div class="col-md-12">
        <h1>Welcome to <strong>@Tenant.Name</strong></h1>
        <h3>@Tenant.Description</h3>
    </div>
</div>

<div class="row">
    <div class="col-md-12">
        <h4>Popular questions</h4>
        <ul>
            @foreach (var question in Model.Questions)
            {
                <li>@question.Title</li>
            }
        </ul>
    </div>
</div>
```

The `@inject` directive gets the current tenant from SaasKit, and the `@model` directive tells ASP.NET Core that this view is backed by a new model class (that you're going to create). Create the `QuestionListViewModel.cs` file in the Models directory:

``` csharp
using System.Collections.Generic;

namespace QuestionExchange.Models
{
    public class QuestionListViewModel
    {
    public IEnumerable<Question> Questions { get; set; }
    }
}
```

### Query the database

The `HomeController` is responsible for rendering the index view you just edited. Open it up and replace the `Index()` method with this one:

``` csharp
public async Task<IActionResult> Index()
{
    var topQuestions = await _context
        .Questions
        .Where(q => q.Tenant.Id == _currentTenant.Id)
        .OrderByDescending(q => q.UpdatedAt)
        .Take(5)
        .ToArrayAsync();

    var viewModel = new QuestionListViewModel
    {
        Questions = topQuestions
    };

    return View(viewModel);
}
```

This query gets the newest five questions for this tenant (granted, there's only one question right now) and populates the view model.

> [!NOTE]  
> For a large application, you'd typically put data access code in a service or repository layer and keep it out of your controllers. This is just a simple example!

The code you added needs `_context` and `_currentTenant`, which aren't available in the controller yet. You can make these members available by adding a constructor to the class:

``` csharp
public class HomeController : Controller
{
    private readonly AppDbContext _context;
    private readonly Tenant _currentTenant;

    public HomeController(AppDbContext context, Tenant tenant)
    {
        _context = context;
        _currentTenant = tenant;
    }

    // Existing code...
```

To keep the compiler from complaining, add this declaration at the top of the file:

``` csharp
using Microsoft.EntityFrameworkCore;
```

### Test the app

The test tenants you added to the database were tied to the (fake) domains `bufferoverflow.local` and `dboverflow.local`. To test these tenants on your local machine, edit your hosts file to add the domains:

- `127.0.0.1 bufferoverflow.local`
- `127.0.0.1 dboverflow.local`

Start your project with `dotnet run` or by selecting Start in Visual Studio and the application begins listening on a URL like `localhost:5000`. If you visit that URL directly, you see an error because your [default tenant behavior](http://benfoster.io/blog/handling-unresolved-tenants-in-saaskit) isn't set up yet.

Instead, when you visit `http://bufferoverflow.local:5000` you can see one tenant of your multitenant application! Switch to `http://dboverflow.local:5000` to view the other tenant. Adding more tenants is now a simple matter of adding more rows in the `tenants` table.

## Related content

- [Multitenant schema migration](migration-schema.md)
- [Multitenant query migration](migration-query.md)
- [Migration overview](migrating.md)
