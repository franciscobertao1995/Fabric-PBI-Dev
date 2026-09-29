# Rayfin Sales Pulse

Self-contained HTML reporting demo built from the Adventure Works CSV files in `../data`.

## Build

```powershell
.\build.ps1
```

Open `index.html` directly in a browser. Re-run the build whenever the source CSV files change.

## Deploy to Fabric

Use Node.js 20, 22, or 24, then run:

```powershell
npm install
npx rayfin up --workspace-id 74b4ddf4-fc3c-42f4-b152-eea2c152fbc4 --yes
```

Rayfin runs the `build` script and deploys `dist/index.html` as a Fabric App.

## Included views

- Sales, profit, margin, and target KPI cards
- Monthly sales versus target trend
- Region and product cross-filtering
- Year, region, category, and salesperson filters
- Salesperson ranking and transaction detail
- Current-view CSV export
- Responsive light and dark themes