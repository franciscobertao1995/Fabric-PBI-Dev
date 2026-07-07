# Fabric notebook source

# METADATA ********************

# META {
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "dc10a228-9c78-4cc2-895e-028cdfe33367",
# META       "default_lakehouse_name": "aw_bronze",
# META       "default_lakehouse_workspace_id": "f6894d78-6eeb-4014-a9ec-3e75ebe36ee8"
# META     }
# META   }
# META }

# MARKDOWN ********************

# # 01 - Bronze Ingest# # **Layer purpose:** Land the raw AdventureWorks reseller tab-separated CSVs (Sales, Targets, Product, Reseller, Salesperson, Region, SalespersonRegion) exactly as received into Delta tables. No type casting or deduplication - only metadata columns (ingestion_timestamp, source_file, batch_id) are added. Serves as the immutable audit/replay source.
