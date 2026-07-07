# Phase 2 · Notebook Development

**Goal:** fill in the three empty notebooks scaffolded in [Phase 1](01-initial-architecture-setup.md) — `01_bronze_ingest`, `02_silver_transform`, `03_gold_star_schema` — using the **Fabric Data Engineering VS Code extension** and the **FabricNotebook** custom agent in GitHub Copilot Chat.

> Grounded in [Section 2 — Develop Fabric Notebooks in VS Code](../docs/02-fabric-notebooks-vscode.md).

---

## Prerequisites

- The [**Fabric Data Engineering VS Code extension**](https://marketplace.visualstudio.com/items?itemName=SynapseVSCode.synapse), signed in to your workspace.
- The three empty notebooks from Phase 1 and the raw CSVs staged in `aw_bronze` under `Files/raw/`.

---

## Choose your editing mode: Local vs VFS

The extension offers two ways to edit notebooks ([source](https://learn.microsoft.com/fabric/data-engineering/setup-vs-code-extension#choose-a-workspace)). Pick the one that fits your workflow.

| | **Local mode** | **VFS mode** |
|---|---------------|--------------|
| Where files live | Downloaded to a local folder, synced back | Edited in place as remote files |
| Multiple workspaces at once | One at a time | Multiple in one window |
| Best for | Offline editing, **Git-based workflows** | Quick cross-workspace edits |

**Local mode** (recommended for this demo — plays best with Git and Copilot):
1. Select the **Fabric Data Engineering** icon in the Activity Bar.
2. Select **Select Workspace** and pick your workspace.
3. Set where downloads go with **`Fabric Data Engineering: Set Local Work Folder`** from the Command Palette.
4. Open a notebook — it downloads locally and shows an `M` (modified) marker once you edit it.

**VFS mode** (edit remote files directly, across multiple workspaces):
1. **Open a Remote Window** → **Open Fabric Data Engineering Workspaces**.
2. Follow [Manage Fabric workspace with VS Code under VFS mode](https://learn.microsoft.com/fabric/data-engineering/manage-workspace-with-vs-code-vfs-mode).

→ Full details: [2.2 Local mode vs. VFS mode](../docs/02-fabric-notebooks-vscode.md#22-local-mode-vs-vfs-mode).

---

## Select the FabricNotebook agent

1. Open one of the notebooks in VS Code.
2. Open **GitHub Copilot Chat**.
3. In the **session type** selector, choose **Local** (the agent supports only Local).
4. In the **agent** selector, choose **FabricNotebook**.

→ [2.4 The Fabric Notebook custom agent](../docs/02-fabric-notebooks-vscode.md#24-the-fabric-notebook-custom-agent).

> **Fabric-aware reminders the agent follows:** reuse the built-in `spark` session, use **relative paths** for the default lakehouse (`aw_bronze`) and full **ABFSS paths** for the others (`aw_silver`, `aw_gold`).

---

## Notebook 1 — `01_bronze_ingest` (raw → Bronze)

Load every tab-separated CSV as-is into Bronze Delta tables.

```text
In this notebook, ingest the tab-separated CSVs from Files/raw/ in the default
lakehouse into Bronze Delta tables. For each of Sales, Targets, Product, Reseller,
Salesperson, Region, and SalespersonRegion, read with sep="\t", header=true, and
inferSchema=false (keep everything as strings at Bronze). Write each to a Delta
table named bronze_<name> (overwrite). Add an ingestion timestamp column
_ingested_at. Show the row count for each table when done.
```

✅ *Outcome:* `bronze_sales`, `bronze_targets`, `bronze_product`, `bronze_reseller`, `bronze_salesperson`, `bronze_region`, `bronze_salespersonregion`.

---

## Notebook 2 — `02_silver_transform` (Bronze → Silver)

Clean, typecast, and conform. This is where the messy AdventureWorks formatting gets fixed.

```text
Read the bronze_* tables and write cleaned Silver Delta tables (silver_*) to the
aw_silver lakehouse (use its ABFSS path). Apply these rules:
- Strip "$" and "," from Sales, Cost, Unit Price (Sales table), Standard Cost
  (Product), and Target (Targets), then cast to double.
- Parse the long text dates: Sales.OrderDate and Targets.TargetMonth are like
  "Friday, August 25, 2017" — convert to a proper date type.
- Cast all *Key and Quantity columns to int.
- Trim whitespace from every string column and drop exact duplicate rows.
- Rename columns with spaces or dashes to snake_case (e.g. "Standard Cost" ->
  standard_cost, "State-Province" -> state_province).
Show the schema and row count for each Silver table.
```

✅ *Outcome:* typed, deduplicated `silver_*` tables with clean numeric, date, and column names.

---

## Notebook 3 — `03_gold_star_schema` (Silver → Gold)

Shape the star schema described in [`data/README.md`](data/README.md), including a Date dimension.

```text
Read the silver_* tables and build the Gold star schema in the aw_gold lakehouse
(use its ABFSS path):
- Dimensions: dim_product, dim_reseller, dim_salesperson, dim_region — one row per
  key, descriptive attributes only.
- dim_date: generate a continuous date dimension covering the min/max of
  silver_sales.order_date and silver_targets.target_month, with columns date,
  year, quarter, month, month_name, year_month.
- Bridge: bridge_salesperson_region from silver_salespersonregion.
- Facts: fact_sales (grain: one row per sales order line, with a derived
  profit = sales - cost) and fact_targets (grain: one row per salesperson per month).
Keep foreign keys on the facts (product_key, reseller_key, employee_key,
salesterritory_key, order_date; and employee_id, target_month on targets).
Preview the top rows of each Gold table and report row counts.
```

✅ *Outcome:* a Gold star schema (`dim_*`, `dim_date`, `bridge_salesperson_region`, `fact_sales`, `fact_targets`) ready for Power BI.

---

## Run and validate

Run each notebook on **remote Spark** (no local cluster needed) and sanity-check the Gold layer:

```text
Explore fact_sales joined to dim_date: show total sales and total quantity by
year_month, and the three months with the highest total sales.
```

→ [2.3 Author and run notebooks](../docs/02-fabric-notebooks-vscode.md#23-author-and-run-notebooks).

✅ *Outcome:* a working Bronze → Silver → Gold pipeline over AdventureWorks reseller sales.

---

## Commit your work

In **Local mode**, the edited notebooks appear as changes in VS Code Git — commit on a feature branch and push. In **VFS mode**, use the workspace **Source control** panel to commit.

**Next:** [Phase 3 — Power BI Development & Optimization →](03-powerbi-development-optimization.md)
