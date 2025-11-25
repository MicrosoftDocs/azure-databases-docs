---
ms.service: azure-cosmos-db
ms.topic: include
ms.date: 11/24/2025
---

### Overview

The Azure Cosmos DB .NET SDK has a dependency on `Newtonsoft.Json` for JSON serialization operations. **This dependency is not managed automatically** - you must explicitly add `Newtonsoft.Json` as a direct dependency in your project.

The SDK internally depends on version 10.x of Newtonsoft.Json, which has a known security vulnerability. However, the SDK has been verified to work with both 10.x and 13.x versions. The patched 13.x versions include breaking changes, but the SDK's usage patterns are compatible with these changes.

> [!IMPORTANT]
> This dependency is required even when using `System.Text.Json` for user-defined types via [CosmosClientOptions.UseSystemTextJsonSerializerWithOptions](/dotnet/api/microsoft.azure.cosmos.cosmosclientoptions.usesystemtextjsonserializerwithoptions?view=azure-dotnet&preserve-view=true), because the SDK's internal operations still use Newtonsoft.Json for system types.

### Recommended Configuration

**Always explicitly add `Newtonsoft.Json` version 13.0.4 or higher as a direct dependency** when using the Azure Cosmos DB .NET SDK v3. We recommend using version 13.x for the security patch unless you have specific compatibility concerns with the breaking changes introduced in 13.x.

#### For Projects Using Central Package Management

If your project uses `Directory.Packages.props`:

```xml
<Project>
  <ItemGroup>
    <PackageVersion Include="Microsoft.Azure.Cosmos" Version="3.47.0" />
    <PackageVersion Include="Newtonsoft.Json" Version="13.0.4" />
  </ItemGroup>
</Project>
```

#### For Standard .csproj Projects

```xml
<ItemGroup>
  <PackageReference Include="Microsoft.Azure.Cosmos" Version="3.47.0" />
  <PackageReference Include="Newtonsoft.Json" Version="13.0.4" />
</ItemGroup>
```

### Troubleshooting Version Conflicts

If you encounter build errors like:

```
error NU1109: Detected package downgrade: Newtonsoft.Json from 13.0.4 to centrally defined 13.0.3
```

**Solution:**

1. **Identify the required version** by checking which packages need newer versions:
   ```powershell
   dotnet list package --include-transitive | Select-String "Newtonsoft.Json"
   ```

2. **Update your centralized package version** to match or exceed the highest required version:
   ```xml
   <PackageVersion Include="Newtonsoft.Json" Version="13.0.4" />
   ```

3. **Clean and rebuild**:
   ```powershell
   dotnet clean
   dotnet restore
   dotnet build
   ```

### Version Compatibility

| Cosmos DB SDK Version | Minimum Newtonsoft.Json | Recommended |
|----------------------|------------------------|-------------|
| 3.47.0+              | 13.0.3                 | 13.0.4      |
| 3.54.0+              | 13.0.4                 | 13.0.4      |

> [!TIP]
> When using .NET Aspire 13.0.0 or later, ensure `Newtonsoft.Json` is at version 13.0.4 to avoid conflicts with Aspire's Azure components.

### Best Practices

1. **Always add as a direct dependency** - The SDK does not automatically manage this dependency for you
2. **Use version 13.x for security** - Version 10.x has known security vulnerabilities. The SDK is compatible with both 10.x and 13.x, so use 13.x unless breaking changes affect your application
3. **Required even with System.Text.Json** - You must include Newtonsoft.Json even when using `UseSystemTextJsonSerializerWithOptions`, as the SDK uses it internally for system types
4. **Pin the version explicitly** - Don't rely on transitive dependency resolution
5. **Monitor warnings** - Treat NuGet package downgrade warnings (NU1109) as errors in CI/CD pipelines

---