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
# META       "default_lakehouse_workspace_id": "f6894d78-6eeb-4014-a9ec-3e75ebe36ee8",
# META       "known_lakehouses": [
# META         {
# META           "id": "dc10a228-9c78-4cc2-895e-028cdfe33367"
# META         },
# META         {
# META           "id": "0b09704d-576a-4f87-8321-741e6d791735"
# META         },
# META         {
# META           "id": "097c1a29-7fe3-44c2-9382-e9a691e9a90e"
# META         }
# META       ]
# META     }
# META   }
# META }

# MARKDOWN ********************

# # 03 - Gold Star Schema**Layer purpose:** Build the curated star schema (conformed dimensions + Sales and Targets fact tables with surrogate keys) and pre-aggregated metrics such as sales-vs-target attainment. Read-optimized with V-Order and Optimize Write for Power BI Direct Lake consumption.

# MARKDOWN ********************

# ## Step 1: Read Silver Tables from aw_silver Lakehouse

# CELL ********************

# Define ABFSS paths for aw_silver and aw_gold lakehouses
silver_path = "abfss://f6894d78-6eeb-4014-a9ec-3e75ebe36ee8@onelake.dfs.fabric.microsoft.com/097c1a29-7fe3-44c2-9382-e9a691e9a90e/Tables"
gold_path = "abfss://f6894d78-6eeb-4014-a9ec-3e75ebe36ee8@onelake.dfs.fabric.microsoft.com/0b09704d-576a-4f87-8321-741e6d791735/Tables"

# Read all Silver tables from aw_silver lakehouse
df_silver_product = spark.read.format("delta").load(f"{silver_path}/silver_product")
df_silver_region = spark.read.format("delta").load(f"{silver_path}/silver_region")
df_silver_reseller = spark.read.format("delta").load(f"{silver_path}/silver_reseller")
df_silver_sales = spark.read.format("delta").load(f"{silver_path}/silver_sales")
df_silver_salesperson = spark.read.format("delta").load(f"{silver_path}/silver_salesperson")
df_silver_salespersonregion = spark.read.format("delta").load(f"{silver_path}/silver_salespersonregion")
df_silver_targets = spark.read.format("delta").load(f"{silver_path}/silver_targets")

print("✅ Silver tables loaded successfully from aw_silver lakehouse")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Step 2: Create Dimension Tables

# CELL ********************

from pyspark.sql.functions import col

# dim_product
dim_product = df_silver_product.select(
    col("product_key"),
    col("product"),
    col("standard__cost").alias("standard_cost"),
    col("color"),
    col("subcategory"),
    col("category"),
    col("background__color__format").alias("background_color_format"),
    col("font__color__format").alias("font_color_format")
).dropDuplicates(["product_key"])

# dim_reseller
dim_reseller = df_silver_reseller.select(
    col("reseller_key"),
    col("business__type").alias("business_type"),
    col("reseller"),
    col("city"),
    col("state__province").alias("state_province"),
    col("country__region").alias("country_region")
).dropDuplicates(["reseller_key"])

# dim_salesperson  — actual columns: employee_key, employee_i_d, salesperson, title, u_p_n
dim_salesperson = df_silver_salesperson.select(
    col("employee_key"),
    col("employee_i_d").alias("employee_id"),
    col("salesperson"),
    col("title"),
    col("u_p_n").alias("upn")
).dropDuplicates(["employee_key"])

# dim_region  — actual column: sales_territory_key → aliased to salesterritory_key
dim_region = df_silver_region.select(
    col("sales_territory_key").alias("salesterritory_key"),
    col("region"),
    col("country"),
    col("group")
).dropDuplicates(["salesterritory_key"])

print("✅ Dimension tables created:")
print(f"   - dim_product:     {dim_product.count():,} rows")
print(f"   - dim_reseller:    {dim_reseller.count():,} rows")
print(f"   - dim_salesperson: {dim_salesperson.count():,} rows")
print(f"   - dim_region:      {dim_region.count():,} rows")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Step 3: Create Date Dimension (dim_date)

# CELL ********************

from pyspark.sql.functions import col, year, quarter, month, date_format
from datetime import timedelta

# Find min and max dates from both sales and targets
# Silver column names: order_date (from order + date split), target_month (from target + month split)
min_sales_date = df_silver_sales.agg({"order_date": "min"}).collect()[0][0]
max_sales_date = df_silver_sales.agg({"order_date": "max"}).collect()[0][0]
min_targets_date = df_silver_targets.agg({"target_month": "min"}).collect()[0][0]
max_targets_date = df_silver_targets.agg({"target_month": "max"}).collect()[0][0]

# Find overall min and max dates
overall_min_date = min(min_sales_date, min_targets_date)
overall_max_date = max(max_sales_date, max_targets_date)

print(f"Date range: {overall_min_date} to {overall_max_date}")

# Generate continuous date dimension
date_range = []
current_date = overall_min_date
while current_date <= overall_max_date:
    date_range.append((current_date,))
    current_date += timedelta(days=1)

# Create DataFrame from date range
dim_date = spark.createDataFrame(date_range, ["date"])

# Add date dimension columns
dim_date = dim_date \
    .withColumn("year", year(col("date"))) \
    .withColumn("quarter", quarter(col("date"))) \
    .withColumn("month", month(col("date"))) \
    .withColumn("month_name", date_format(col("date"), "MMMM")) \
    .withColumn("year_month", date_format(col("date"), "yyyy-MM"))

print(f"✅ dim_date created: {dim_date.count():,} rows")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Step 4: Create Bridge Table

# CELL ********************

# bridge_salesperson_region — actual columns: employee_key, sales_territory_key
bridge_salesperson_region = df_silver_salespersonregion.select(
    col("employee_key"),
    col("sales_territory_key").alias("salesterritory_key")
).dropDuplicates()

print(f"✅ bridge_salesperson_region created: {bridge_salesperson_region.count():,} rows")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Step 5: Create Fact Tables

# CELL ********************

# fact_sales - one row per sales order line with derived profit
fact_sales = df_silver_sales.select(
    col("sales_order_number"),
    col("order_date"),
    col("product_key"),
    col("reseller_key"),
    col("employee_key"),
    col("sales_territory_key").alias("salesterritory_key"),
    col("quantity"),
    col("unit__price").alias("unit_price"),
    col("sales"),
    col("cost"),
    (col("sales") - col("cost")).alias("profit")
)

# fact_targets - one row per salesperson per month
# actual columns: employee_i_d, target, target_month
fact_targets = df_silver_targets.select(
    col("employee_i_d").alias("employee_id"),
    col("target_month"),
    col("target")
)

print("✅ Fact tables created:")
print(f"   - fact_sales:    {fact_sales.count():,} rows")
print(f"   - fact_targets:  {fact_targets.count():,} rows")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Step 6: Write Gold Tables to aw_gold Lakehouse

# CELL ********************

# Write dimension tables to aw_gold lakehouse
print("Writing dimension tables to aw_gold...")
dim_product.write.format("delta").mode("overwrite").save(f"{gold_path}/dim_product")
print("  ✓ dim_product written")

dim_reseller.write.format("delta").mode("overwrite").save(f"{gold_path}/dim_reseller")
print("  ✓ dim_reseller written")

dim_salesperson.write.format("delta").mode("overwrite").save(f"{gold_path}/dim_salesperson")
print("  ✓ dim_salesperson written")

dim_region.write.format("delta").mode("overwrite").save(f"{gold_path}/dim_region")
print("  ✓ dim_region written")

dim_date.write.format("delta").mode("overwrite").save(f"{gold_path}/dim_date")
print("  ✓ dim_date written")

# Write bridge table to aw_gold lakehouse
bridge_salesperson_region.write.format("delta").mode("overwrite").save(f"{gold_path}/bridge_salesperson_region")
print("  ✓ bridge_salesperson_region written")

# Write fact tables to aw_gold lakehouse
fact_sales.write.format("delta").mode("overwrite").save(f"{gold_path}/fact_sales")
print("  ✓ fact_sales written")

fact_targets.write.format("delta").mode("overwrite").save(f"{gold_path}/fact_targets")
print("  ✓ fact_targets written")

print("\n✅ All Gold tables successfully written to aw_gold lakehouse!")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Step 7: Preview Gold Tables and Report Row Counts

# CELL ********************

# Preview dim_product
print("=" * 80)
print("DIM_PRODUCT")
print("=" * 80)
print(f"Row count: {dim_product.count():,}")
dim_product.show(5, truncate=False)

# Preview dim_reseller
print("\n" + "=" * 80)
print("DIM_RESELLER")
print("=" * 80)
print(f"Row count: {dim_reseller.count():,}")
dim_reseller.show(5, truncate=False)

# Preview dim_salesperson
print("\n" + "=" * 80)
print("DIM_SALESPERSON")
print("=" * 80)
print(f"Row count: {dim_salesperson.count():,}")
dim_salesperson.show(5, truncate=False)

# Preview dim_region
print("\n" + "=" * 80)
print("DIM_REGION")
print("=" * 80)
print(f"Row count: {dim_region.count():,}")
dim_region.show(5, truncate=False)

# Preview dim_date
print("\n" + "=" * 80)
print("DIM_DATE")
print("=" * 80)
print(f"Row count: {dim_date.count():,}")
dim_date.show(5, truncate=False)

# Preview bridge_salesperson_region
print("\n" + "=" * 80)
print("BRIDGE_SALESPERSON_REGION")
print("=" * 80)
print(f"Row count: {bridge_salesperson_region.count():,}")
bridge_salesperson_region.show(5, truncate=False)

# Preview fact_sales
print("\n" + "=" * 80)
print("FACT_SALES")
print("=" * 80)
print(f"Row count: {fact_sales.count():,}")
fact_sales.show(5, truncate=False)

# Preview fact_targets
print("\n" + "=" * 80)
print("FACT_TARGETS")
print("=" * 80)
print(f"Row count: {fact_targets.count():,}")
fact_targets.show(5, truncate=False)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Summary of all Gold tables
print("\n" + "=" * 80)
print("GOLD STAR SCHEMA SUMMARY")
print("=" * 80)

summary_data = [
    ("dim_product", dim_product.count()),
    ("dim_reseller", dim_reseller.count()),
    ("dim_salesperson", dim_salesperson.count()),
    ("dim_region", dim_region.count()),
    ("dim_date", dim_date.count()),
    ("bridge_salesperson_region", bridge_salesperson_region.count()),
    ("fact_sales", fact_sales.count()),
    ("fact_targets", fact_targets.count())
]

summary_df = spark.createDataFrame(summary_data, ["Table Name", "Row Count"])
summary_df.show(truncate=False)

print("\n✅ Gold star schema successfully created in aw_gold lakehouse!")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
