# aw_gold Semantic Model

A **Direct Lake** Power BI semantic model (PBIP / TMDL format) built over the **`aw_gold`** Fabric Lakehouse. It exposes the Adventure Works reseller-sales star schema for analysis and is fully Git-syncable via Fabric Git integration (see `.platform`).

## Storage mode

**Direct Lake on OneLake.** A single shared named expression (`DirectLake - aw_gold`) connects to the lakehouse using the `AzureStorage.DataLake` connector:

```
https://onelake.dfs.fabric.microsoft.com/f6894d78-6eeb-4014-a9ec-3e75ebe36ee8/0b09704d-576a-4f87-8321-741e6d791735
```

| | |
|---|---|
| Workspace ID | `f6894d78-6eeb-4014-a9ec-3e75ebe36ee8` |
| Lakehouse ID (aw_gold) | `0b09704d-576a-4f87-8321-741e6d791735` |

Every table uses an `EntityPartitionSource` (`mode: directLake`) mapping model columns to the Delta table columns via `sourceColumn` — no Power Query/import.

## Star schema

| Model table | Source (gold) table | Role | Notes |
|---|---|---|---|
| **Product** | `dim_product` | Dimension | `Category → Subcategory → Product` hierarchy |
| **Reseller** | `dim_reseller` | Dimension | Geography hierarchy; `City`/`State Province`/`Country Region` geo data categories |
| **Salesperson** | `dim_salesperson` | Dimension | |
| **Region** | `dim_region` | Dimension | `Group → Country → Region` hierarchy |
| **Date** | `dim_date` | Date dimension | Marked as date table (`dataCategory: Time`); `Month` sorted by month number; `Calendar` hierarchy; auto date/time disabled |
| **Salesperson Region** | `bridge_salesperson_region` | Bridge | Salesperson ↔ sales territory (many-to-many) |
| **Sales** | `fact_sales` | Fact | Grain = sales order line |
| **Targets** | `fact_targets` | Fact | Grain = salesperson + month |

### Relationships (9)

- `Sales[Product Key] → Product[Product Key]`
- `Sales[Reseller Key] → Reseller[Reseller Key]`
- `Sales[Employee Key] → Salesperson[Employee Key]`
- `Sales[Sales Territory Key] → Region[Sales Territory Key]`
- `Sales[Order Date] → Date[Date]`
- `Targets[Target Month] → Date[Date]`
- `Targets[Employee ID] → Salesperson[Employee ID]`
- `Salesperson Region[Employee Key] → Salesperson[Employee Key]`
- `Salesperson Region[Sales Territory Key] → Region[Sales Territory Key]`

### Measures

On **Sales**: `Total Sales`, `Total Cost`, `Total Profit`, `Profit Margin %`, `Total Quantity`, `Order Count`.
On **Targets**: `Total Target`.
On each dimension: a distinct-count measure (e.g. `Product Count`).

All measures have a `formatString` and a description; foreign-key and aggregated base columns are hidden; `discourageImplicitMeasures` is enabled to steer users toward the explicit measures.

## Design notes & things to verify before first refresh

1. **Monetary columns typed as `double`** — `Sales Amount`, `Cost Amount`, `Profit Amount`, `Unit Price`, `Standard Cost`, `Target`. The gold notebook writes these as Spark/Delta doubles, and Direct Lake requires the model column type to match the physical Delta type. This intentionally overrides the usual "prefer Decimal over Double" modeling guideline.
2. **`Employee ID` typed as `int64`** (on both `Salesperson` and `Targets`, which are joined on it). If the underlying Delta column is actually stored as a string, change **both** columns to `string` so the relationship and Direct Lake mapping resolve.
3. **Bridge relationships are single-direction** (safe default, no ambiguity). To let a **Region** slicer filter salespeople (and thus their sales) through the bridge, set both `Salesperson Region` relationships to `bothDirections`.
4. **Column type matching** — Direct Lake fails at query/refresh time if any `dataType` disagrees with the Delta column. If a refresh reports a type mismatch, align the offending column's `dataType` in the table's `.tmdl` file.

## Validation performed

The TMDL was deserialized and validated with the Tabular Object Model (TOM): **8 tables, 9 relationships, 1 Direct Lake expression**, all partitions in `DirectLake` mode. No structural errors.

## Folder layout

```
aw_gold.SemanticModel/
├── .platform                     # Fabric item metadata (Git integration)
├── definition.pbism              # Semantic model settings
└── definition/
    ├── database.tmdl             # Compatibility level 1702
    ├── model.tmdl                # Model props + Direct Lake named expression + table refs
    ├── relationships.tmdl        # 9 relationships
    └── tables/                   # One .tmdl per table
```

## How to deploy / sync

- **Git**: commit this folder and sync to the Fabric workspace via Git integration.
- **Power BI Desktop**: open as part of a PBIP (pair with a `.Report` and `.pbip` if you want a report layer).
- After deploy, run an initial refresh to bind the Direct Lake columns; if credentials are required, configure the lakehouse connection in the Fabric/Power BI Service portal.
