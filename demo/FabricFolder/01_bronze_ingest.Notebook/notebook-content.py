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

# # 01 - Bronze Ingest
# 
# **Layer purpose:** Land the raw AdventureWorks reseller tab-separated CSVs (Sales, Targets, Product, Reseller, Salesperson, Region, SalespersonRegion) exactly as received into Delta tables. No type casting or deduplication - only metadata columns (ingestion_timestamp, source_file, batch_id) are added. Serves as the immutable audit/replay source.

# MARKDOWN ********************

# ## Setup and imports

# CELL ********************

from pyspark.sql.functions import current_timestamp, lit
from datetime import datetime

# Generate ingestion timestamp for this batch
ingestion_timestamp = datetime.now()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Define ingestion function
# 
# This function reads a tab-separated CSV file and writes it to a Bronze Delta table with an ingestion timestamp.

# CELL ********************

def ingest_csv_to_bronze(file_name, table_name):
    """
    Read a tab-separated CSV from Files/raw/ and write to a Bronze Delta table.
    Keep all columns as strings (inferSchema=false).
    Add an _ingested_at timestamp column.
    """
    # Read CSV with tab delimiter, header, and no schema inference (all strings)
    df = (spark.read
          .option("sep", "\t")
          .option("header", "true")
          .option("inferSchema", "false")
          .csv(f"Files/raw/{file_name}"))
    
    # Add ingestion timestamp
    df = df.withColumn("_ingested_at", lit(ingestion_timestamp))
    
    # Write to Delta table (overwrite mode)
    # Enable column mapping to allow spaces and special characters in column names
    (df.write
     .format("delta")
     .mode("overwrite")
     .option("delta.columnMapping.mode", "name")
     .saveAsTable(table_name))
    
    row_count = df.count()
    print(f"✓ Ingested {row_count:,} rows from {file_name} → {table_name}")
    
    return row_count

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Ingest all AdventureWorks CSV files
# 
# Ingest the seven tab-separated CSVs into Bronze Delta tables.

# CELL ********************

# Define the CSV files and their corresponding table names
files_to_ingest = [
    ("Sales.csv", "bronze_sales"),
    ("Targets.csv", "bronze_targets"),
    ("Product.csv", "bronze_product"),
    ("Reseller.csv", "bronze_reseller"),
    ("Salesperson.csv", "bronze_salesperson"),
    ("Region.csv", "bronze_region"),
    ("SalespersonRegion.csv", "bronze_salespersonregion")
]

# Ingest each file
print(f"Starting Bronze ingestion at {ingestion_timestamp}\n")
total_rows = 0

for file_name, table_name in files_to_ingest:
    row_count = ingest_csv_to_bronze(file_name, table_name)
    total_rows += row_count

print(f"\n✓ Bronze ingestion complete: {total_rows:,} total rows across {len(files_to_ingest)} tables")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Verify Bronze tables
# 
# Show the row count for each Bronze Delta table.

# CELL ********************

# Display row counts for all Bronze tables
print("Bronze table row counts:\n")
print(f"{'Table':<30} {'Rows':>10}")
print("-" * 42)

for _, table_name in files_to_ingest:
    count = spark.table(table_name).count()
    print(f"{table_name:<30} {count:>10,}")

print("-" * 42)
print(f"{'TOTAL':<30} {total_rows:>10,}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Sample rows from each Bronze table
# 
# Display the first 5 rows from each Bronze Delta table to verify the data structure.

# CELL ********************

# Display first 5 rows from each Bronze table
for file_name, table_name in files_to_ingest:
    print(f"\n{'='*80}")
    print(f"Sample from: {table_name}")
    print(f"{'='*80}")
    display(spark.table(table_name).limit(5))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
