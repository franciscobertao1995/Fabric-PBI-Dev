# Enterprise Development on Microsoft Fabric

A hands-on reference for building **enterprise-grade development solutions on Microsoft Fabric** — covering professional Power BI development with source control, developing Fabric notebooks in Visual Studio Code, and agentic development with AI.

> Every technique in this repository is grounded exclusively in **official Microsoft Learn documentation** and **official Microsoft GitHub repositories**. Links to the source material are provided throughout so your teams can go deeper.

---

## Who this is for

Data platform teams, BI developers, and data engineers who want to move from *ad-hoc, single-author* development to a **repeatable, versioned, collaborative, and AI-assisted** engineering practice on Microsoft Fabric.

## What you'll learn

| # | Section | What it covers |
|---|---------|----------------|
| 1 | [Enterprise Power BI Development](docs/01-enterprise-power-bi-development.md) | Source control with Git integration, the PBIP folder structure and TMDL files, **Skills for Fabric** in VS Code, the **Power BI Modeling MCP Server**, and using GitHub Copilot to develop and optimize Power BI content. |
| 2 | [Develop Fabric Notebooks in VS Code](docs/02-fabric-notebooks-vscode.md) | Getting started with the **Fabric Data Engineering VS Code extension**, local vs. VFS mode, authoring and running notebooks, and the Fabric Notebook custom agent. |
| 3 | [Fabric Agentic Development](docs/03-fabric-agentic-development.md) | Using **Skills for Fabric** and MCP servers to build end-to-end Fabric solutions with AI agents. |

## Try it end-to-end

Follow the [**AdventureWorks end-to-end demo**](demo/README.md) to test all three capabilities on a single, realistic scenario — from a Git-versioned semantic model, to a medallion lakehouse built with notebooks, to an agent that assembles the whole solution. You can adapt each step to one of your own datasets.

---

## Prerequisites at a glance

- A **Microsoft Fabric capacity** (or a [free Fabric trial](https://learn.microsoft.com/fabric/fundamentals/fabric-trial)). Git integration requires Fabric capacity, Premium capacity, or PPU. See [Git integration prerequisites](https://learn.microsoft.com/fabric/cicd/git-integration/git-get-started#prerequisites).
- [**Visual Studio Code**](https://code.visualstudio.com/download).
- The [**GitHub Copilot Chat**](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot-chat) extension.
- [**Power BI Desktop**](https://www.microsoft.com/download/details.aspx?id=58494) (for authoring semantic models and reports as PBIP).
- An **Azure DevOps** organization or a **GitHub** account for the remote Git repository.
- [**Node.js**](https://nodejs.org/en) (for MCP servers) and the [**Azure CLI**](https://learn.microsoft.com/cli/azure/install-azure-cli) (`az login`) for Fabric authentication.

Detailed, tool-specific prerequisites are listed inside each section.

---

## Official sources referenced

- [Introduction to Git integration (Fabric)](https://learn.microsoft.com/fabric/cicd/git-integration/intro-to-git-integration)
- [Power BI Desktop projects (PBIP)](https://learn.microsoft.com/power-bi/developer/projects/projects-overview)
- [TMDL overview](https://learn.microsoft.com/analysis-services/tmdl/tmdl-overview)
- [Fabric Data Engineering VS Code extension](https://learn.microsoft.com/fabric/data-engineering/setup-vs-code-extension)
- [microsoft/skills-for-fabric](https://github.com/microsoft/skills-for-fabric)
- [microsoft/powerbi-modeling-mcp](https://github.com/microsoft/powerbi-modeling-mcp)

## Disclaimer

Some of the capabilities referenced (Power BI Desktop projects, the Power BI Modeling MCP Server, the Fabric Notebook custom agent, and parts of Skills for Fabric) are in **preview** and may change. Always confirm current behavior against the linked Microsoft Learn and Microsoft GitHub documentation. This repository is a community/enablement asset and is not an official Microsoft product.
