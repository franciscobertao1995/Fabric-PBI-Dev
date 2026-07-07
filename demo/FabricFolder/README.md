# FabricFolder

This folder hosts the **Fabric code** for the demo — the items that are authored locally in VS Code and synced to a Microsoft Fabric workspace via Git integration.

Expect content such as:

- **Notebooks** — the `01_bronze_ingest`, `02_silver_transform`, and `03_gold_star_schema` notebooks that implement the medallion pipeline (see [Phase 2 — Notebook Development](../02-notebook-development.md)).
- **Lakehouse items** — metadata for the `aw_bronze`, `aw_silver`, and `aw_gold` lakehouses (see [Phase 1 — Initial Architecture Setup](../01-initial-architecture-setup.md)).
- Other Fabric items (Spark job definitions, environments, pipelines) added as the demo grows.

These artifacts are created and edited with the [Fabric Data Engineering VS Code extension](https://marketplace.visualstudio.com/items?itemName=SynapseVSCode.synapse) and kept under source control so every change is a reviewable commit.
