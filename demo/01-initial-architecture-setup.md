# Phase 1 · Initial Architecture Setup

**Goal:** stand up the medallion architecture — three lakehouses (`aw_bronze`, `aw_silver`, `aw_gold`) — and scaffold **three empty notebooks** ready to be filled in during [Phase 2](02-notebook-development.md). You drive all of this agentically with **Skills for Fabric** and GitHub Copilot.

> Grounded in [Section 3 — Fabric Agentic Development](../docs/03-fabric-agentic-development.md). Nothing here writes transformation logic yet — this phase only provisions infrastructure and creates placeholders.

---

## Prerequisites

- A Fabric-enabled workspace connected to Git (see [1.1 Source control with Git integration](../docs/01-enterprise-power-bi-development.md#11-source-control-with-git-integration)).
- VS Code with **GitHub Copilot Chat**.
- **Skills for Fabric** installed and authenticated:
  ```bash
  git clone https://github.com/microsoft/skills-for-fabric.git
  az login
  az account get-access-token --resource https://api.fabric.microsoft.com
  ```
  ```text
  /plugin marketplace add microsoft/skills-for-fabric
  /plugin install fabric-skills@fabric-collection
  ```
  → Details: [3. Fabric Agentic Development — setup](../docs/03-fabric-agentic-development.md).

---

## Step 1 — Plan the architecture

Ask the agent to lay out the medallion design before creating anything.

```text
Use Microsoft Fabric skills to design a medallion architecture for AdventureWorks
reseller sales. The source is a set of tab-separated CSVs: Sales and Targets (facts),
and Product, Reseller, Salesperson, Region, and SalespersonRegion (dimensions/bridge).
Explain the Bronze, Silver, and Gold responsibilities and list the lakehouses and
notebooks I will need. Keep it concise.
```

✅ *Outcome:* a clear plan — Bronze (raw), Silver (cleaned/typed), Gold (star schema).

---

## Step 2 — Create the medallion lakehouses

```text
Create three lakehouses in my Fabric workspace named aw_bronze, aw_silver, and
aw_gold. Confirm each was created and show its ID.
```

✅ *Outcome:* `aw_bronze`, `aw_silver`, and `aw_gold` exist in the workspace.

---

## Step 3 — Upload the raw data to Bronze

Upload every file from [`data/`](data/) into the **`aw_bronze`** lakehouse under `Files/raw/`:

```
Files/raw/Sales.csv
Files/raw/Targets.csv
Files/raw/Product.csv
Files/raw/Reseller.csv
Files/raw/Salesperson.csv
Files/raw/Region.csv
Files/raw/SalespersonRegion.csv
```

> Reminder: these files are **tab-separated** (`\t`), not comma-separated — the notebooks in Phase 2 read them with `sep="\t"`. See [`data/README.md`](data/README.md).

✅ *Outcome:* raw CSVs staged in the Bronze lakehouse.

---

## Step 4 — Scaffold empty notebooks

Create the three notebooks as **empty placeholders** — you fill them in during [Phase 2](02-notebook-development.md).

```text
Create three empty PySpark notebooks in my Fabric workspace and attach aw_bronze
as the default lakehouse:
1. 01_bronze_ingest
2. 02_silver_transform
3. 03_gold_star_schema
Do not add transformation code yet — just create the notebooks with a single
title markdown cell describing each layer's purpose.
```

✅ *Outcome:* three empty, named notebooks wired to the lakehouse, ready for development.

---

## Step 5 — Commit the scaffold

In the Fabric workspace, use **Source control → Commit** to version the new items, or sync via Git integration and open a commit in VS Code.

→ [The daily inner loop](../docs/01-enterprise-power-bi-development.md#the-daily-inner-loop).

✅ *Outcome:* the empty architecture is checked into Git as a reviewable starting point.

---

## Bring your own scenario

```text
My raw data is <describe your files, columns, and grain>. Design an equivalent
medallion architecture, name the lakehouses appropriately, and list the empty
notebooks I should scaffold.
```

**Next:** [Phase 2 — Notebook Development →](02-notebook-development.md)
