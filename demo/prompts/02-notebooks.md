# Stage 2 prompts — Fabric notebooks (Section 2)

Use these with the **FabricNotebook** custom agent in GitHub Copilot Chat (session type **Local**). See [Section 2](../../docs/02-fabric-notebooks-vscode.md#24-the-fabric-notebook-custom-agent).

> Fabric-aware reminders the agent should follow: reuse the built-in `spark` session, use **relative paths** for the default lakehouse and full **ABFSS paths** for others.

## Bronze — ingest raw CSV

```text
In this notebook, read Files/raw/contoso_sales_sample.csv from the default
lakehouse with header=true and inferSchema, then write it as a Delta table
named bronze_sales (overwrite). Show the row count and schema when done.
```

## Silver — clean and conform

```text
Read bronze_sales. Trim whitespace from string columns, cast OrderDate to date,
cast Quantity to int and UnitPrice to double, drop rows with a null CustomerId
or OrderId, and remove exact duplicate rows. Add a computed column
LineTotal = Quantity * UnitPrice. Write the result to a Delta table silver_sales.
```

## Gold — aggregate

```text
Read silver_sales. Create two Gold Delta tables:
1. gold_sales_by_month: total LineTotal and total Quantity grouped by
   year-month (from OrderDate).
2. gold_sales_by_product: total LineTotal and total Quantity grouped by
   ProductId, ProductName, and Category.
Write both with overwrite and preview the top rows.
```

## Validate

```text
Explore gold_sales_by_month: show schema, row count, and the three months with
the highest total LineTotal.
```
