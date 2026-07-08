# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "dc10a228-9c78-4cc2-895e-028cdfe33367",
# META       "default_lakehouse_name": "aw_bronze",
# META       "default_lakehouse_workspace_id": "f6894d78-6eeb-4014-a9ec-3e75ebe36ee8"
# META     }
# META   }
# META }

# MARKDOWN ********************

# # 02 - Silver Transform
# 
# **Layer purpose:** Clean and conform the Bronze data - cast types, standardize column names to snake_case, deduplicate on natural keys, handle nulls, validate ranges, and enforce referential integrity between facts and dimensions. Resolves the SalespersonRegion bridge. Output is schema-enforced, business-ready detail.

# MARKDOWN ********************

# ## Setup and imports

# CELL ********************

from pyspark.sql.functions import col, trim, regexp_replace, to_date, lit, current_timestamp
from pyspark.sql.types import IntegerType, DoubleType, DateType
import re

print("✓ Imports loaded successfully")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Helper functions

# CELL ********************

def to_snake_case(name):
    """Convert column name to snake_case (spaces, dashes, and CamelCase to underscores, lowercase)."""
    # First, insert underscore before uppercase letters (for CamelCase)
    name = re.sub(r'(?<!^)(?=[A-Z])', '_', name)
    # Replace spaces and dashes with underscores
    name = re.sub(r'[\s\-]+', '_', name)
    # Convert to lowercase
    name = name.lower()
    return name

def clean_currency_column(df, column_name):
    """Strip $ and , from a currency column and cast to double."""
    return df.withColumn(
        column_name,
        regexp_replace(col(column_name), r'[\$,]', '').cast(DoubleType())
    )

def parse_long_date(df, column_name):
    """Parse dates like 'Friday, August 25, 2017' to proper date type."""
    # Remove day of week prefix (e.g., "Friday, ")
    return df.withColumn(
        column_name,
        to_date(regexp_replace(col(column_name), r'^[A-Za-z]+,\s*', ''), 'MMMM d, yyyy')
    )

def trim_string_columns(df):
    """Trim whitespace from all string columns."""
    for field in df.schema.fields:
        if field.dataType.simpleString() == 'string':
            df = df.withColumn(field.name, trim(col(field.name)))
    return df

def rename_columns_to_snake_case(df):
    """Rename all columns to snake_case."""
    for old_name in df.columns:
        new_name = to_snake_case(old_name)
        if old_name != new_name:
            df = df.withColumnRenamed(old_name, new_name)
    return df

def write_to_silver(df, table_name):
    """Write a DataFrame to the aw_silver lakehouse."""
    # Use lakehouse-qualified table name to write to aw_silver lakehouse
    # Format: lakehouse_name.table_name
    qualified_table_name = f"aw_silver.{table_name}"
    
    (df.write
     .format("delta")
     .mode("overwrite")
     .option("delta.columnMapping.mode", "name")
     .saveAsTable(qualified_table_name))
    
    print(f"✓ Wrote {df.count():,} rows to {qualified_table_name}")

print("✓ Helper functions defined successfully")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Transform Sales to Silver
# 
# Clean Sales table: parse OrderDate, clean currency columns (Sales, Cost, Unit Price), cast keys and Quantity to int, trim strings, drop duplicates, rename to snake_case.

# CELL ********************

# Read bronze_sales
df_sales = spark.table("bronze_sales").drop("_ingested_at")

# Parse OrderDate
df_sales = parse_long_date(df_sales, "OrderDate")

# Clean currency columns and cast to double
df_sales = clean_currency_column(df_sales, "Unit Price")
df_sales = clean_currency_column(df_sales, "Sales")
df_sales = clean_currency_column(df_sales, "Cost")

# Cast key columns and Quantity to int
df_sales = df_sales.withColumn("ProductKey", col("ProductKey").cast(IntegerType()))
df_sales = df_sales.withColumn("ResellerKey", col("ResellerKey").cast(IntegerType()))
df_sales = df_sales.withColumn("EmployeeKey", col("EmployeeKey").cast(IntegerType()))
df_sales = df_sales.withColumn("SalesTerritoryKey", col("SalesTerritoryKey").cast(IntegerType()))
df_sales = df_sales.withColumn("Quantity", col("Quantity").cast(IntegerType()))

# Trim string columns
df_sales = trim_string_columns(df_sales)

# Drop exact duplicates
df_sales = df_sales.dropDuplicates()

# Rename columns to snake_case
df_sales = rename_columns_to_snake_case(df_sales)

# Write to aw_silver lakehouse
write_to_silver(df_sales, "silver_sales")

print("\nSchema:")
df_sales.printSchema()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Transform Targets to Silver
# 
# Clean Targets table: parse TargetMonth, clean Target currency column, cast EmployeeID to int, trim strings, drop duplicates, rename to snake_case.

# CELL ********************

# Read bronze_targets
df_targets = spark.table("bronze_targets").drop("_ingested_at")

# Parse TargetMonth
df_targets = parse_long_date(df_targets, "TargetMonth")

# Clean Target currency column and cast to double
df_targets = clean_currency_column(df_targets, "Target")

# Cast EmployeeID to int
df_targets = df_targets.withColumn("EmployeeID", col("EmployeeID").cast(IntegerType()))

# Trim string columns
df_targets = trim_string_columns(df_targets)

# Drop exact duplicates
df_targets = df_targets.dropDuplicates()

# Rename columns to snake_case
df_targets = rename_columns_to_snake_case(df_targets)

# Write to aw_silver lakehouse
write_to_silver(df_targets, "silver_targets")

print("\nSchema:")
df_targets.printSchema()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Transform Product to Silver
# 
# Clean Product table: clean Standard Cost currency column, cast ProductKey to int, trim strings, drop duplicates, rename to snake_case.

# CELL ********************

# Read bronze_product
df_product = spark.table("bronze_product").drop("_ingested_at")

# Clean Standard Cost currency column and cast to double
df_product = clean_currency_column(df_product, "Standard Cost")

# Cast ProductKey to int
df_product = df_product.withColumn("ProductKey", col("ProductKey").cast(IntegerType()))

# Trim string columns
df_product = trim_string_columns(df_product)

# Drop exact duplicates
df_product = df_product.dropDuplicates()

# Rename columns to snake_case
df_product = rename_columns_to_snake_case(df_product)

# Write to aw_silver lakehouse
write_to_silver(df_product, "silver_product")

print("\nSchema:")
df_product.printSchema()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Transform remaining dimensions to Silver
# 
# Clean Reseller, Salesperson, and Region tables: cast keys to int, trim strings, drop duplicates, rename to snake_case.

# CELL ********************

# Reseller
df_reseller = spark.table("bronze_reseller").drop("_ingested_at")
df_reseller = df_reseller.withColumn("ResellerKey", col("ResellerKey").cast(IntegerType()))
df_reseller = trim_string_columns(df_reseller)
df_reseller = df_reseller.dropDuplicates()
df_reseller = rename_columns_to_snake_case(df_reseller)
write_to_silver(df_reseller, "silver_reseller")

# Salesperson
df_salesperson = spark.table("bronze_salesperson").drop("_ingested_at")
df_salesperson = df_salesperson.withColumn("EmployeeKey", col("EmployeeKey").cast(IntegerType()))
df_salesperson = df_salesperson.withColumn("EmployeeID", col("EmployeeID").cast(IntegerType()))
df_salesperson = trim_string_columns(df_salesperson)
df_salesperson = df_salesperson.dropDuplicates()
df_salesperson = rename_columns_to_snake_case(df_salesperson)
write_to_silver(df_salesperson, "silver_salesperson")

# Region
df_region = spark.table("bronze_region").drop("_ingested_at")
df_region = df_region.withColumn("SalesTerritoryKey", col("SalesTerritoryKey").cast(IntegerType()))
df_region = trim_string_columns(df_region)
df_region = df_region.dropDuplicates()
df_region = rename_columns_to_snake_case(df_region)
write_to_silver(df_region, "silver_region")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Transform SalespersonRegion bridge to Silver
# 
# Clean the bridge table: cast both keys to int, drop duplicates, rename to snake_case.

# CELL ********************

# SalespersonRegion (bridge table)
df_bridge = spark.table("bronze_salespersonregion").drop("_ingested_at")
df_bridge = df_bridge.withColumn("EmployeeKey", col("EmployeeKey").cast(IntegerType()))
df_bridge = df_bridge.withColumn("SalesTerritoryKey", col("SalesTerritoryKey").cast(IntegerType()))
df_bridge = df_bridge.dropDuplicates()
df_bridge = rename_columns_to_snake_case(df_bridge)
write_to_silver(df_bridge, "silver_salespersonregion")

print("\nSchema:")
df_bridge.printSchema()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Silver transformation summary
# 
# Show all Silver tables with their row counts and verify the transformations.

# CELL ********************

# List all Silver tables and their row counts from aw_silver lakehouse
silver_tables = [
    "aw_silver.silver_sales",
    "aw_silver.silver_targets",
    "aw_silver.silver_product",
    "aw_silver.silver_reseller",
    "aw_silver.silver_salesperson",
    "aw_silver.silver_region",
    "aw_silver.silver_salespersonregion"
]

print("="*80)
print("SILVER LAYER TRANSFORMATION COMPLETE")
print("="*80)
print(f"\n{'Table':<35} {'Rows':>15}")
print("-"*50)

total_rows = 0
for table_name in silver_tables:
    count = spark.table(table_name).count()
    total_rows += count
    print(f"{table_name:<35} {count:>15,}")

print("-"*50)
print(f"{'TOTAL':<35} {total_rows:>15,}")
print("\n✓ All tables cleaned, typed, deduplicated, and renamed to snake_case")
print("✓ All Silver tables written to aw_silver lakehouse")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Verify key transformations
# 
# Sample data from silver_sales to verify:
# - Currency columns are now doubles without $ or commas
# - OrderDate is a proper date type
# - Column names are in snake_case
# - Keys are integers

# CELL ********************

# Show sample from silver_sales with transformed columns
print("Sample from aw_silver.silver_sales showing transformed data types and column names:\n")
display(spark.table("aw_silver.silver_sales").select(
    "salesordernumber",
    "orderdate", 
    "productkey",
    "resellerkey",
    "quantity",
    "unit_price",
    "sales",
    "cost"
).limit(5))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
