---
ms.service: azure-cosmos-db
ms.topic: include
ms.date: 11/24/2025
---

### Overview

The Azure Cosmos DB .NET SDK has a dependency on `Newtonsoft.Json` for JSON serialization operations. While this dependency is managed automatically in most scenarios, you may encounter version conflicts when using:

- Central Package Management (`Directory.Packages.props`)
- .NET Aspire or other Azure frameworks
- Multiple Azure SDKs with different version requirements

### Recommended Configuration

**Always explicitly specify `Newtonsoft.Json` version 13.0.4 or higher** when using the Azure Cosmos DB .NET SDK v3.

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

1. **Pin the version explicitly** - Don't rely on transitive dependency resolution
2. **Update together** - When upgrading the Cosmos DB SDK, check if `Newtonsoft.Json` requirements have changed
3. **Monitor warnings** - Treat NuGet package downgrade warnings (NU1109) as errors in CI/CD pipelines
4. **Test after updates** - Run your full test suite after updating either package

---