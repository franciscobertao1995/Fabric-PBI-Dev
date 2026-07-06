# Stage 3 prompts — Model, optimize, document (Section 1)

Use these with the **Power BI Modeling MCP Server** in GitHub Copilot Chat, after connecting to your PBIP. See [Section 1.4](../../docs/01-enterprise-power-bi-development.md#14-the-power-bi-modeling-mcp-server) and [1.5](../../docs/01-enterprise-power-bi-development.md#15-developing-with-github-copilot-on-top-of-pbip).

> ⚠️ Back up your PBIP before running modeling operations. Review each TMDL diff in Git before committing.

## Connect

```text
Open semantic model from PBIP folder
'<path>/Contoso.SemanticModel/definition'
```

## Add core measures

```text
Add these measures to the appropriate table, each with a proper format string
and a "Key Measures" display folder. Validate each with a DAX query before applying:
- Total Sales = sum of LineTotal
- Total Quantity = sum of Quantity
- Sales YoY % = year-over-year growth of Total Sales
- Sales 3M Avg = rolling 3-month average of Total Sales
```

## Annotate the model (notes/descriptions)

```text
Add concise, consistent descriptions to every table, column, and measure that
explain their business purpose. For measures, also summarize the DAX logic in
plain language.
```

## Enforce naming conventions

```text
Analyze the naming convention of the main fact table and apply the same pattern
consistently across the entire model. Show me the TMDL diff before applying.
```

## Refactor time intelligence

```text
Refactor the time-intelligence measures into a calculation group with items for
YoY %, 3M Avg, and add new variants 6M Avg and 12M Avg. Keep existing measures working.
```

## Document the model

```text
Generate a Markdown document that fully documents this semantic model: a mermaid
diagram of table relationships, every measure with its DAX and a plain-language
description, any row-level security filters, and the data sources inferred from
the Power Query code. Save it as MODEL.md.
```

## Optimize DAX

```text
Review the DAX for all measures and flag any that iterate unnecessarily or could
be simplified. Propose optimized rewrites, validate them with DAX queries, and
apply only the ones that pass.
```
