param(
    [string]$DataPath = (Join-Path $PSScriptRoot "..\data"),
    [string]$OutputPath = (Join-Path $PSScriptRoot "index.html")
)

$ErrorActionPreference = "Stop"
$culture = [Globalization.CultureInfo]::GetCultureInfo("en-US")

function Read-TabCsv([string]$Name) {
    Import-Csv (Join-Path $DataPath $Name) -Delimiter "`t"
}

function Convert-Currency([string]$Value) {
    [math]::Round([double]($Value -replace '[$,]', ''), 2)
}

$products = @(Read-TabCsv "Product.csv")
$regions = @(Read-TabCsv "Region.csv")
$salespeople = @(Read-TabCsv "Salesperson.csv")
$sales = @(Read-TabCsv "Sales.csv")
$targets = @(Read-TabCsv "Targets.csv")
$assignments = @(Read-TabCsv "SalespersonRegion.csv")

$productIndex = @{}
for ($index = 0; $index -lt $products.Count; $index++) { $productIndex[$products[$index].ProductKey] = $index }
$regionIndex = @{}
for ($index = 0; $index -lt $regions.Count; $index++) { $regionIndex[$regions[$index].SalesTerritoryKey] = $index }
$personIndex = @{}
$employeeIdIndex = @{}
for ($index = 0; $index -lt $salespeople.Count; $index++) {
    $personIndex[$salespeople[$index].EmployeeKey] = $index
    $employeeIdIndex[$salespeople[$index].EmployeeID] = $index
}

$packedSales = [Collections.Generic.List[object]]::new()
foreach ($row in $sales) {
    $date = [datetime]::Parse($row.OrderDate, $culture)
    $packedSales.Add([object[]]@(
        $date.ToString("yyyy-MM-dd"),
        $productIndex[$row.ProductKey],
        $regionIndex[$row.SalesTerritoryKey],
        $personIndex[$row.EmployeeKey],
        (Convert-Currency $row.Sales),
        (Convert-Currency $row.Cost),
        [int]$row.Quantity,
        $row.SalesOrderNumber
    ))
}

$packedTargets = [Collections.Generic.List[object]]::new()
foreach ($row in $targets) {
    $date = [datetime]::Parse($row.TargetMonth, $culture)
    $packedTargets.Add([object[]]@($date.ToString("yyyy-MM"), $employeeIdIndex[$row.EmployeeID], (Convert-Currency $row.Target)))
}

$personRegions = @{}
foreach ($row in $assignments) {
    $person = [string]$personIndex[$row.EmployeeKey]
    if (-not $personRegions.ContainsKey($person)) { $personRegions[$person] = @() }
    $personRegions[$person] += $regionIndex[$row.SalesTerritoryKey]
}

$productRows = [Collections.Generic.List[object]]::new()
$products | ForEach-Object { $productRows.Add([object[]]@($_.Product, $_.Subcategory, $_.Category)) }
$regionRows = [Collections.Generic.List[object]]::new()
$regions | ForEach-Object { $regionRows.Add([object[]]@($_.Region, $_.Country, $_.Group)) }
$personRows = [Collections.Generic.List[object]]::new()
$salespeople | ForEach-Object { $personRows.Add([object[]]@($_.Salesperson, $_.Title, $_.EmployeeID)) }

$payload = [ordered]@{
    generatedAt = [datetime]::UtcNow.ToString("yyyy-MM-ddTHH:mm:ssZ")
    products = $productRows
    regions = $regionRows
    people = $personRows
    personRegions = $personRegions
    sales = $packedSales
    targets = $packedTargets
}

$template = Get-Content (Join-Path $PSScriptRoot "index.template.html") -Raw
$json = $payload | ConvertTo-Json -Depth 8 -Compress
$html = $template.Replace("/*__RAYFIN_DATA__*/", "window.RAYFIN_DATA=$json;")
$outputDirectory = Split-Path $OutputPath -Parent
if ($outputDirectory -and -not (Test-Path $outputDirectory)) {
    New-Item -ItemType Directory -Path $outputDirectory | Out-Null
}
[IO.File]::WriteAllText($OutputPath, $html, [Text.UTF8Encoding]::new($false))

Write-Host "Built $OutputPath with $($sales.Count) sales rows and $($targets.Count) target rows."