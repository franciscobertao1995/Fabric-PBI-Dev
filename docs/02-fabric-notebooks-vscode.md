# 2. Develop Fabric Notebooks in Visual Studio Code

The **Fabric Data Engineering VS Code extension** brings Microsoft Fabric development into Visual Studio Code. With it you can author and run Fabric notebooks, create Spark job definitions, explore lakehouses, and manage Spark environments — all from your local editor, with full Git and Copilot support.

Source: [Get started with the Fabric Data Engineering VS Code extension](https://learn.microsoft.com/fabric/data-engineering/setup-vs-code-extension)

This section covers:

1. [Get started with the extension](#21-get-started-with-the-extension)
2. [Local mode vs. VFS mode](#22-local-mode-vs-vfs-mode)
3. [Author and run notebooks](#23-author-and-run-notebooks)
4. [The Fabric Notebook custom agent](#24-the-fabric-notebook-custom-agent)

---

## 2.1 Get started with the extension

### What you can do with the extension

The extension supports the following Fabric items and tasks ([source](https://learn.microsoft.com/fabric/data-engineering/setup-vs-code-extension#what-you-can-do-with-the-extension)):

| Capability | Description |
|-----------|-------------|
| **Workspaces** | Manage one or more Fabric workspaces directly in VS Code. See [Manage Fabric workspace with VS Code under VFS mode](https://learn.microsoft.com/fabric/data-engineering/manage-workspace-with-vs-code-vfs-mode). |
| **Notebooks** | Create, edit, and run Fabric notebooks locally and execute them on remote Spark compute. See [Create and manage Fabric notebooks in VS Code](https://learn.microsoft.com/fabric/data-engineering/author-notebook-with-vs-code). |
| **Spark job definitions** | Create and manage Spark job definitions with full CRUD support. See [Create and manage Spark job definitions in VS Code](https://learn.microsoft.com/fabric/data-engineering/author-sjd-with-vs-code). |
| **Environments** | Explore and inspect Spark environments — hardware profiles, libraries, and Spark configuration. See [Explore and inspect Spark environments with VS Code](https://learn.microsoft.com/fabric/data-engineering/manage-environment-with-vs-code). |

### Install the extension

1. Install [Visual Studio Code](https://code.visualstudio.com/download).
2. Install the [**Fabric Data Engineering VS Code extension**](https://marketplace.visualstudio.com/items?itemName=SynapseVSCode.synapse) from the Marketplace.
3. Sign in to Fabric from the extension and select a workspace (see modes below).

> **Fastest path from the portal:** on any notebook authoring page in the Fabric portal, select **Open in VS Code**. The extension activates and your workspace connects automatically. See [Create and manage Fabric notebooks in VS Code](https://learn.microsoft.com/fabric/data-engineering/author-notebook-with-vs-code#open-a-notebook-with-the-data-engineering-extension).

### Other ways to run the extension

- **VS Code for the Web** — no install required. Go to [vscode.dev](https://vscode.dev) (or use **Open in VS Code (Web)** from the portal), search for **Fabric Data Engineering**, and install. Changes apply to the workspace immediately. See [Notebooks in VS Code for the web](https://learn.microsoft.com/fabric/data-engineering/author-notebook-with-vs-code-web).
- **Dev Containers (Docker)** — a prebuilt image includes JDK, Conda, and the Jupyter extension so you skip local setup. See [Use Docker containers with the extension](https://learn.microsoft.com/fabric/data-engineering/set-up-vs-code-extension-with-docker-image).

---

## 2.2 Local mode vs. VFS mode

The extension offers two authoring modes ([source](https://learn.microsoft.com/fabric/data-engineering/setup-vs-code-extension#choose-a-workspace)):

### Local mode

You download notebooks and other items to a local working directory, edit them locally, and sync changes back to your Fabric workspace.

1. Select the **Fabric Data Engineering** icon in the Activity Bar to open the side bar.
2. Select **Select Workspace** (or the **Switch Workspace** arrows icon) and pick a workspace.
3. Browse items in the side bar. When you edit an item like a notebook, it's downloaded to a local folder.
4. To choose where downloaded items are stored, run **`Fabric Data Engineering: Set Local Work Folder`** from the Command Palette.

### VFS (Virtual File System) mode

You open and edit workspace items **directly as remote files**, without downloading them. VFS mode also lets you add **multiple Fabric workspaces** to a single VS Code window and work across them side by side.

1. Select **Open a Remote Window** in VS Code.
2. Select **Open Fabric Data Engineering Workspaces**.
3. Follow the full setup in [Manage Fabric workspace with VS Code under VFS mode](https://learn.microsoft.com/fabric/data-engineering/manage-workspace-with-vs-code-vfs-mode).

| | Local mode | VFS mode |
|---|-----------|----------|
| Where files live | Downloaded to a local folder | Edited in place as remote files |
| Multiple workspaces at once | One at a time | Multiple in one window |
| Best for | Offline editing, Git-based workflows | Quick cross-workspace edits |

---

## 2.3 Author and run notebooks

The extension fully supports **create, read, update, delete (CRUD)** notebook operations, plus synchronization between local and remote, and running notebooks on **remote Apache Spark compute** ([source](https://learn.microsoft.com/fabric/data-engineering/author-notebook-with-vs-code)).

### Notebook states in the tree

In local mode, the notebook list uses colors/characters to show each notebook's state:

- **Default** (white, no marker) — exists remotely, not yet downloaded.
- **Modified** (`M`, yellow) — downloaded and edited locally, not yet published.
- (Additional states indicate new/published items.)

### The notebook folder and resources

Fabric notebooks support **notebook resources** — store `.py` modules and data files (`.csv`, images, etc.) in a resource folder and access them as a local file system ([source](https://learn.microsoft.com/fabric/data-engineering/author-notebook-resource-with-vs-code)):

1. After downloading a notebook, select **Open Notebook Folder** to see the notebook file and its resource folder.
2. Create new files/subfolders under the predefined **`builtin`** folder (files created outside `builtin` are **not** uploaded to the notebook resource).
3. Import local modules into the notebook, e.g. a `builtin/localLib/util.py`.

### Fabric-aware Spark code

When authoring notebook code, follow Fabric's data-access patterns (see [Fabric notebook docs](https://learn.microsoft.com/fabric/data-engineering/lakehouse-notebook-explore)):

- Use the pre-created `spark` session variable — don't create a new one.
- Use **relative paths** for the **default lakehouse** and full **ABFSS paths** for non-default lakehouses.

```python
# Read a Delta table from the default lakehouse
df = spark.read.format("delta").load("Tables/dbo/sales")

# Read a file from the default lakehouse Files area
raw = spark.read.option("header", True).csv("Files/raw/sales.csv")

# Write a curated Delta table
(df.write.format("delta").mode("overwrite").saveAsTable("gold_sales"))
```

### Run on remote Spark

With a workspace connected, run cells directly against Fabric's managed Spark compute — no local Spark cluster needed. Results stream back into VS Code.

---

## 2.4 The Fabric Notebook custom agent

The **Fabric Notebook custom agent** is a specialized agent in **GitHub Copilot Chat** that authors Fabric notebooks with Fabric-aware suggestions and code generation.

Source: [Develop Fabric notebooks with the Fabric Notebook custom agent in VS Code](https://learn.microsoft.com/fabric/data-engineering/notebook-custom-agent-with-vs-code) *(currently in preview)*

### Why a custom agent?

Unlike a general-purpose coding agent, it understands Fabric notebook patterns. For example, it recognizes the built-in `spark` variable representing your current Spark session (so it reuses the session instead of creating one), and it applies the correct data-access patterns (relative paths for the default lakehouse, full ABFSS paths for others).

**Use it for:** generating Spark code, refining notebook logic, and troubleshooting notebook code with Fabric-specific context.
**Use other extension features for:** browsing Fabric items, opening notebooks, and managing resources.

### Prerequisites

- Install the [Fabric Data Engineering VS Code extension](https://marketplace.visualstudio.com/itemdetails?itemName=SynapseVSCode.synapse) — the custom agent only appears when this extension is installed.

### Select the agent

1. Open a Fabric notebook in VS Code.
2. Open **GitHub Copilot Chat**.
3. In the **session type** selector, choose **Local** (the agent supports only the Local session type).
4. In the **agent** selector, choose **FabricNotebook**.
5. In the **model** picker, choose a supported base model (per the docs: **Claude Sonnet 4.5**, **Claude Opus 4.6**, or **GPT-5.2**).

### Use the agent

Type your own prompts to start immediately. Optional helpers live in the **FABRIC DATA ENGINEERING** extension view:

1. In the Activity Bar, open the **FABRIC DATA ENGINEERING** view.
2. Expand **AGENT PROMPTS - FABRIC DATA ENGINEERING** for sample prompts (exploring/validating data, cleaning/preparing data, and similar workflows).
3. Expand **Saved Prompts** to store and reuse your own prompts.

**Example prompts**
```text
Explore the bronze_sales Delta table: show schema, row count, null counts
per column, and the min/max order date.
```
```text
Clean the bronze_sales table: trim string columns, cast OrderDate to date,
drop rows with a null CustomerId, and write the result to silver_sales.
```

---

## Where to go next

- **[Section 3 — Fabric Agentic Development](03-fabric-agentic-development.md)** — orchestrate whole solutions with AI.
- **[Contoso end-to-end demo](../demo/README.md)** — build a medallion lakehouse with these tools.
