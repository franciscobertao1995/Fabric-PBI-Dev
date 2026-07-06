# Stage 1 prompts — Agentic scaffold (Section 3)

Use these with **GitHub Copilot** after installing [Skills for Fabric](https://github.com/microsoft/skills-for-fabric) and authenticating to Fabric (`az login`). See [Section 3](../../docs/03-fabric-agentic-development.md).

## Plan the architecture

```text
Use Microsoft Fabric skills to design a medallion architecture for Contoso
retail sales data. Explain the Bronze, Silver, and Gold responsibilities and
list the lakehouses and notebooks I will need. Keep it concise.
```

## Create the lakehouses

```text
Create three lakehouses in my Fabric workspace named contoso_bronze,
contoso_silver, and contoso_gold. Confirm each was created and show its ID.
```

## Outline the notebooks

```text
Outline three PySpark notebooks for this medallion flow:
1. Bronze: ingest Files/raw/contoso_sales_sample.csv into a Delta table bronze_sales.
2. Silver: clean, typecast, and deduplicate into silver_sales.
3. Gold: aggregate into gold_sales_by_month and gold_sales_by_product.
For each, describe the inputs, transformations, and outputs before writing code.
```

## Bring your own scenario

```text
My raw data is <describe your files, columns, and grain>. Design an equivalent
medallion architecture and adjust the notebook outline to match my schema.
```
