# Phase 3 · Power BI Development & Optimization

**Goal:** turn the Gold star schema from [Phase 2](02-notebook-development.md) into a governed, optimized, documented Power BI semantic model. You build the initial model in **Power BI Desktop**, save it as a **PBIP (with TMDL)**, and then iterate with GitHub Copilot and the **Power BI Modeling MCP Server** — modeling, optimizing, documenting, tuning performance, and validating DAX.

> Grounded in [Section 1 — Enterprise Power BI Development](../docs/01-enterprise-power-bi-development.md).

---

## Prerequisites

- [**Power BI Desktop**](https://www.microsoft.com/download/details.aspx?id=58494).
- The [**TMDL VS Code extension**](https://marketplace.visualstudio.com/items?itemName=analysis-services.TMDL).
- The **Power BI Modeling MCP Server** ([VS Code extension](https://aka.ms/powerbi-modeling-mcp-vscode)).
- The Gold lakehouse (`aw_gold`) tables from Phase 2.

---

## Step 1 — Build the initial model in Power BI Desktop

1. In Power BI Desktop, **Get data → Fabric → Lakehouses** and connect to the **`aw_gold`** tables:
   `fact_sales`, `fact_targets`, `dim_product`, `dim_reseller`, `dim_salesperson`, `dim_region`, `dim_date`, `bridge_salesperson_region`.
2. In **Model view**, create the star-schema relationships:
   - `dim_date[date]` → `fact_sales[order_date]`
   - `dim_product[product_key]` → `fact_sales[product_key]`
   - `dim_reseller[reseller_key]` → `fact_sales[reseller_key]`
   - `dim_salesperson[employee_key]` → `fact_sales[employee_key]`
   - `dim_region[salesterritory_key]` → `fact_sales[salesterritory_key]`
   - `dim_date[date]` → `fact_targets[target_month]`
   - `dim_salesperson[employee_id]` → `fact_targets[employee_id]`
   - `bridge_salesperson_region` between `dim_salesperson` and `dim_region` (many-to-many).
3. Mark `dim_date` as a **date table**.
4. Build a simple starter report page (a couple of visuals) so the model has something to render.

✅ *Outcome:* a working starter model + report in Power BI Desktop.

---

## Step 2 — Save as PBIP + TMDL

1. **File → Options and settings → Options → Preview features:** enable **Power BI Project (.pbip) save option** and **Store semantic model using TMDL format**.
2. **File → Save as → Power BI Project (.pbip)** and save into your Git repo.
3. Open the PBIP folder in VS Code (with the TMDL extension installed).

→ [1.2 The PBIP folder structure and TMDL files](../docs/01-enterprise-power-bi-development.md#12-the-pbip-folder-structure-and-tmdl-files).

✅ *Outcome:* the model is now reviewable, diff-able TMDL text under source control.

---

## Step 3 — Connect the Power BI Modeling MCP Server

Install the [VS Code extension](https://aka.ms/powerbi-modeling-mcp-vscode), then in Copilot Chat:

```text
Open semantic model from PBIP folder
'<path>/AdventureWorks.SemanticModel/definition'
```

→ [1.4 The Power BI Modeling MCP Server](../docs/01-enterprise-power-bi-development.md#14-the-power-bi-modeling-mcp-server).

> ⚠️ Back up your PBIP before running modeling operations, and review each **TMDL diff** in Git before committing.

---

## Step 4 — Model: add core measures

```text
Add these measures to the appropriate table, each with a proper format string and a
"Key Measures" display folder. Validate each with a DAX query before applying:
- Total Sales = sum of fact_sales[sales]
- Total Cost = sum of fact_sales[cost]
- Total Profit = Total Sales - Total Cost
- Profit Margin % = Total Profit / Total Sales
- Total Quantity = sum of fact_sales[quantity]
- Total Target = sum of fact_targets[target]
- Target Achievement % = Total Sales / Total Target
- Sales YoY % = year-over-year growth of Total Sales
- Sales 3M Avg = rolling 3-month average of Total Sales
```

---

## Step 5 — Document the model

```text
Add concise, consistent descriptions to every table, column, and measure that
explain their business purpose. For measures, also summarize the DAX logic in
plain language.
```

```text
Generate a Markdown document that fully documents this semantic model: a mermaid
diagram of table relationships, every measure with its DAX and a plain-language
description, any row-level security filters, and the data sources inferred from the
Power Query code. Save it as MODEL.md.
```

---

## Step 6 — Optimize & enforce conventions

```text
Analyze the naming convention of the fact and dimension tables and apply the same
pattern consistently across the entire model. Show me the TMDL diff before applying.
```

```text
Refactor the time-intelligence measures into a calculation group with items for
YoY %, 3M Avg, and add new variants 6M Avg and 12M Avg. Keep existing measures working.
```

---

## Step 7 — Improve performance

```text
Review the DAX for all measures and flag any that iterate unnecessarily or could be
simplified. Propose optimized rewrites, validate them with DAX queries, and apply
only the ones that pass.
```

```text
Inspect the model for performance issues: unused columns, high-cardinality columns
that could be dropped or split, columns that should be hidden, and missing
relationships. Recommend changes and show the TMDL diff for each.
```

---

## Step 8 — Test with DAX queries

```text
Write and run DAX queries to validate the model returns correct results:
1. Total Sales, Total Profit, and Profit Margin % by dim_date[year].
2. Top 5 dim_product[category] by Total Sales.
3. Target Achievement % by dim_salesperson[salesperson] for the latest year.
Show the query results and confirm the numbers are reasonable.
```

---

## Step 9 — Ship it through a pull request

1. Review the **TMDL diff** for all model changes in VS Code.
2. Commit on a feature branch and **push**.
3. Open a **pull request**; if configured, let a [PBIP build pipeline](https://learn.microsoft.com/power-bi/developer/projects/projects-build-pipelines) run as a quality gate.
4. Merge to `main`, then in the Fabric workspace use **Source control → Update all**.

→ [The daily inner loop](../docs/01-enterprise-power-bi-development.md#the-daily-inner-loop).

✅ *Outcome:* an optimized, documented, source-controlled semantic model — reviewed and deployed like software.

---

## Bring your own scenario

```text
My Gold tables are <list your fact and dimension tables and keys>. Suggest the
relationships, core measures, and a calculation group appropriate for my model,
and validate each measure with a DAX query.
```

**Back to:** [Demo overview](README.md)
