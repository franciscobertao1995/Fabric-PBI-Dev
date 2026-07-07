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

# # 02 - Silver Transform# # **Layer purpose:** Clean and conform the Bronze data - cast types, standardize column names to snake_case, deduplicate on natural keys, handle nulls, validate ranges, and enforce referential integrity between facts and dimensions. Resolves the SalespersonRegion bridge. Output is schema-enforced, business-ready detail.
