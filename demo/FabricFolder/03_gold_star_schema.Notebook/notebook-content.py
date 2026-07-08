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
# META         }
# META       ]
# META     }
# META   }
# META }

# MARKDOWN ********************

# # 03 - Gold Star Schema**Layer purpose:** Build the curated star schema (conformed dimensions + Sales and Targets fact tables with surrogate keys) and pre-aggregated metrics such as sales-vs-target attainment. Read-optimized with V-Order and Optimize Write for Power BI Direct Lake consumption.
