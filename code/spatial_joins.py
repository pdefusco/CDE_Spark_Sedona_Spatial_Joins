#****************************************************************************
# (C) Cloudera, Inc. 2020-2025
#  All rights reserved.
#
#  Applicable Open Source License: GNU Affero General Public License v3.0
#
#  NOTE: Cloudera open source products are modular software products
#  made up of hundreds of individual components, each of which was
#  individually copyrighted.  Each Cloudera open source product is a
#  collective work under U.S. Copyright Law. Your license to use the
#  collective work is as provided in your written agreement with
#  Cloudera.  Used apart from the collective work, this file is
#  licensed for your use pursuant to the open source license
#  identified above.
#
#  This code is provided to you pursuant a written agreement with
#  (i) Cloudera, Inc. or (ii) a third-party authorized to distribute
#  this code. If you do not have a written agreement with Cloudera nor
#  with an authorized and properly licensed third party, you do not
#  have any rights to access nor to use this code.
#
#  Absent a written agreement with Cloudera, Inc. (“Cloudera”) to the
#  contrary, A) CLOUDERA PROVIDES THIS CODE TO YOU WITHOUT WARRANTIES OF ANY
#  KIND; (B) CLOUDERA DISCLAIMS ANY AND ALL EXPRESS AND IMPLIED
#  WARRANTIES WITH RESPECT TO THIS CODE, INCLUDING BUT NOT LIMITED TO
#  IMPLIED WARRANTIES OF TITLE, NON-INFRINGEMENT, MERCHANTABILITY AND
#  FITNESS FOR A PARTICULAR PURPOSE; (C) CLOUDERA IS NOT LIABLE TO YOU,
#  AND WILL NOT DEFEND, INDEMNIFY, NOR HOLD YOU HARMLESS FOR ANY CLAIMS
#  ARISING FROM OR RELATED TO THE CODE; AND (D)WITH RESPECT TO YOUR EXERCISE
#  OF ANY RIGHTS GRANTED TO YOU FOR THE CODE, CLOUDERA IS NOT LIABLE FOR ANY
#  DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, PUNITIVE OR
#  CONSEQUENTIAL DAMAGES INCLUDING, BUT NOT LIMITED TO, DAMAGES
#  RELATED TO LOST REVENUE, LOST PROFITS, LOSS OF INCOME, LOSS OF
#  BUSINESS ADVANTAGE OR UNAVAILABILITY, OR LOSS OR CORRUPTION OF
#  DATA.
#
# #  Author(s): Paul de Fusco
#***************************************************************************/

#from sedona.spark.register import SedonaRegistrator
#from sedona.spark.utils import SedonaKryoRegistrator, KryoSerializer
#from sedona.spark.sql.types import GeometryType
import pyspark.sql.functions as F
from sedona.spark import *
from pyspark.sql import SparkSession

'''
# Create a Spark session with Sedona configuration
config = SedonaContext.builder().\
    config('spark.jars.packages',
           'org.apache.sedona:sedona-spark-shaded-3.5_2.12:1.7.0,'
           'org.datasyslab:geotools-wrapper:1.7.0-28.5').\
    getOrCreate()
'''

config = SedonaContext.builder() \
    .config('spark.jars.packages',
        'org.apache.sedona:sedona-spark-shaded-3.5_2.12:1.8.0,'
        'org.datasyslab:geotools-wrapper:1.8.0-33.1')\
    .getOrCreate()

sedona = SedonaContext.create(config)

# Function to read CSV and convert WKT to geometry column
def read_sedona_csv(filepath, schema_cols):
    df = sedona.read.csv(filepath, header=True, inferSchema=True)
    # Convert WKT column to geometry
    df = df.withColumn("geometry", F.expr("ST_GeomFromWKT(wkt)"))
    # Show schema and first rows
    print(f"Data from {filepath}:")
    df.printSchema()
    df.show(5, truncate=False)
    return df

# Paths to your files
pii_path = "/app/mount/las_vegas_customer_pii.csv"
accidents_path = "/app/mount/las_vegas_accidents.csv"
streets_path = "/app/mount/las_vegas_streets.csv"
pois_path = "/app/mount/las_vegas_casino_pois.csv"
neighborhoods_path = "/app/mount/las_vegas_neighborhoods.csv"

# Read and show accidents
df_accidents = read_sedona_csv(accidents_path, None)
df.createOrReplaceTempView("accidents")
df_accidents.show()

# Read and show street network
df_streets = read_sedona_csv(streets_path, None)
df.createOrReplaceTempView("streets")
df_streets.show()

# Read and show points of interest
df_pois = read_sedona_csv(pois_path, None)
df.createOrReplaceTempView("pois")
df_pois.show()

# Read and show accidents
df_neighborhoods = read_sedona_csv(neighborhoods_path, None)
df.createOrReplaceTempView("neighborhoods")
df_neighborhoods.show()

# Read and show accidents
df_pii = read_sedona_csv(accidents_path, None)
df.createOrReplaceTempView("pii")
df_pii.show()

# SPATIAL JOINS

# Find all points within the provided polygons
# Find all accidents taking place in each neighborhood
#
sedona.sql(
    """SELECT
        accidents.accident_id as accident_id,
        neighborhoods.name as neighborhood
    FROM accidents
    JOIN neighborhoods ON ST_Within(accidents.wkt, neighborhoods.geometry);"""
).show()

# Find all lines within the provided polygons
# Find all roads travelling through each neighborhood
#
sedona.sql(
    """SELECT
        streets.name as street_name,
        neighborhoods.name as neighborhood
    FROM streets
    LEFT JOIN neighborhoods ON ST_Crosses(streets.wkt, neighborhoods.geometry);"""
).show()

# Spatial join K-nearest neighbors
# For each accident location find the two nearest points of interest
#
sedona.sql(
    """SELECT
        accidents.accident_id as accident_id,
        pois.name AS poi_name
    FROM accidents
    JOIN pois
    ON ST_KNN(accidents.wkt, pois.geometry, 2)"""
).show()

# Spatial distance join
# For each accident find all the points of interest that are within 2.5 kilometers of the point
#
sedona.sql(
    """SELECT
        accidents.accident_id as accident_id,
        pois.name AS poi_name
    FROM accidents
    JOIN pois
    ON ST_DWithin(accidents.geometry, pois.geometry, 2500, useSpheroid = true)"""
).show()
