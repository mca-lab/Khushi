"""from pyspark.sql import SparkSession
from pyspark.sql.functions import col, year, when, lit, coalesce
import os

# --- Configuration ---
# Data will be mounted here in the Docker container
RAW_DIR = "data/raw"
CLEAN_DIR = "data/cleaned_docker" 

COVID_RAW_PATH = os.path.join(RAW_DIR, "covid19.csv")
POPULATION_RAW_PATH = os.path.join(RAW_DIR, "world_population.csv")
CLEANED_DATA_PATH = os.path.join(CLEAN_DIR, "cleaned_data_docker.parquet") 


def create_spark_session():
    
    # NOTE: When run inside Docker, the environment variables (JAVA_HOME, SPARK_HOME, etc.) 
    # are set by the Dockerfile, so we do not need to set them here.
    
    try:
        # Spark session configuration: Master is local[*]
        spark = SparkSession.builder \
            .appName("DockerPySparkDataCleaning") \
            .master("local[*]") \
            .getOrCreate()
        print("[INFO] Spark session started successfully in Docker.")
        return spark
    except Exception as e:
        print(f"[ERROR] Failed to start Spark session. Check Docker environment setup.")
        print(f"Details: {e}")
        return None

def load_and_clean_population(spark, filepath):
    print(f"[STATUS] Starting cleaning for Population data from {filepath}...")
    
    try:
        df_pop = spark.read.csv(filepath, header=True, inferSchema=True)
    except Exception as e:
        print(f"[ERROR] Could not load Population file. Details: {e}")
        return None

    # 1. Select and Rename columns for consistency
    df_pop = df_pop.select(
        col('Country Name').alias('Country'),
        col('Year'),
        col('Population')
    )

    # 2. Drop rows with missing Country or Population
    df_pop = df_pop.na.drop(subset=['Country', 'Population'])

    # 3. Ensure data types are correct
    df_pop = df_pop.withColumn("Year", col("Year").cast("int"))
    df_pop = df_pop.withColumn("Population", col("Population").cast("long"))

    print("[SUCCESS] Population data cleaned.")
    return df_pop


def load_and_clean_covid(spark, filepath):
    print(f"[STATUS] Starting cleaning for COVID-19 data from {filepath}...")
    
    try:
        df_covid = spark.read.csv(filepath, header=True, inferSchema=True)
    except Exception as e:
        print(f"[ERROR] Could not load COVID-19 file. Details: {e}")
        return None

    # 1. Rename columns to standard names
    df_covid = df_covid.toDF('Date', 'Country', 'Confirmed', 'Recovered', 'Deaths')

    # 2. Convert 'Date' column to date type and extract Year
    df_covid = df_covid.withColumn('Date', col('Date').cast('date'))
    df_covid = df_covid.withColumn('Year', year(col('Date')))

    # 3. Remove non-country entities like 'Diamond Princess'
    df_covid = df_covid.filter(col('Country') != lit('Diamond Princess'))
    
    # 4. Cast numeric columns (Confirmed, Recovered, Deaths) to long integers
    df_covid = df_covid.withColumn('Confirmed', col('Confirmed').cast('long'))
    df_covid = df_covid.withColumn('Recovered', col('Recovered').cast('long'))
    df_covid = df_covid.withColumn('Deaths', col('Deaths').cast('long'))

    print("[SUCCESS] COVID-19 data cleaned.")
    return df_covid


def main():
    spark = create_spark_session()
    if not spark:
        return

    # 1. Load and clean individual datasets
    df_pop = load_and_clean_population(spark, POPULATION_RAW_PATH)
    df_covid = load_and_clean_covid(spark, COVID_RAW_PATH)

    if df_pop is None or df_covid is None:
        spark.stop()
        return

    # 2. Merge the two datasets (Left join to keep all COVID data)
    print("[STATUS] Joining datasets on Country and Year...")
    
    df_merged = df_covid.join(
        df_pop, 
        on=['Country', 'Year'], 
        how='left' 
    )

    # 3. Final Cleaning and Transformation on Merged Data
    
    # Calculate Active Cases: Confirmed - (Recovered + Deaths)
    df_merged = df_merged.withColumn(
        'Active', 
        col('Confirmed') - coalesce(col('Recovered'), lit(0)) - coalesce(col('Deaths'), lit(0))
    )
    
    # Calculate cases per 100,000 people (normalized metric)
    df_merged = df_merged.withColumn(
        'Confirmed_per_100k',
        when(col('Population').isNotNull() & (col('Population') > 0), 
             (col('Confirmed') / col('Population')) * 100000
        ).otherwise(lit(0.0))
    )
    
    # Final cleanup: fill any remaining Population nulls with 0 after the join
    df_final = df_merged.na.fill(value=0, subset=['Population'])
    
    # 4. Save the final cleaned dataset
    os.makedirs(CLEAN_DIR, exist_ok=True)
    
    # Save as a single Parquet file to the clean directory
    df_final.coalesce(1).write.mode('overwrite').parquet(CLEANED_DATA_PATH)

    print("\n-------------------------------------------------------------")
    print("PySpark Data Cleaning Complete (inside Docker)!")
    print(f"Rows Processed: {df_final.count()}")
    print(f"Output saved as PARQUET to: {CLEANED_DATA_PATH}")
    print("-------------------------------------------------------------")

    # Stop the Spark session
    spark.stop()


if __name__ == "__main__":
    main()"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, year, when

def start_spark():
    """Start or get an existing Spark session."""
    return SparkSession.builder \
        .appName("COVIDPopulationCleaning") \
        .master("local[*]") \
        .getOrCreate()

def clean_covid(spark):
    """Clean COVID dataset."""
    df = spark.read.option("header", True).csv("data/raw/covid_data.csv")

    # Rename columns for consistency
    rename_map = {
        "Country": "country",
        "Date": "date",
        "Cases": "cases",
        "Deaths": "deaths"
    }
    for old, new in rename_map.items():
        if old in df.columns:
            df = df.withColumnRenamed(old, new)

    # Format date column
    if "date" in df.columns:
        df = df.withColumn("date", to_date(col("date"), "yyyy-MM-dd"))

    # Convert numeric columns
    for colname in ["cases", "deaths"]:
        if colname in df.columns:
            df = df.withColumn(colname, col(colname).cast("int"))

    # Remove null or missing country names
    df = df.na.drop(subset=["country"])
    
    # Drop duplicates
    df = df.dropDuplicates(["country", "date"])

    return df

def clean_population(spark):
    """Clean population dataset."""
    df = spark.read.option("header", True).csv("data/raw/population_data.csv")

    # Rename for consistency
    rename_map = {
        "Country Name": "country",
        "Year": "year",
        "Population": "population"
    }
    for old, new in rename_map.items():
        if old in df.columns:
            df = df.withColumnRenamed(old, new)

    # Convert to correct types
    if "year" in df.columns:
        df = df.withColumn("year", col("year").cast("int"))
    if "population" in df.columns:
        df = df.withColumn("population", col("population").cast("long"))

    # Drop nulls and duplicates
    df = df.na.drop(subset=["country"])
    df = df.dropDuplicates(["country", "year"])

    return df

def merge_datasets(covid_df, population_df):
    """Join on country and year."""
    if "date" in covid_df.columns:
        covid_df = covid_df.withColumn("year", year(col("date")))

    merged = covid_df.join(population_df, on=["country", "year"], how="inner")
    merged = merged.dropDuplicates(["country", "year", "date"])
    return merged

def main():
    spark = start_spark()
    print("✅ Spark session started successfully")

    covid_df = clean_covid(spark)
    population_df = clean_population(spark)

    merged_df = merge_datasets(covid_df, population_df)
    print(f"✅ Combined dataset rows: {merged_df.count()}")

    # Save to cleaned outputs
    merged_df.write.mode("overwrite").csv("data/processed/cleaned_covid_population.csv", header=True)
    merged_df.write.mode("overwrite").parquet("data/processed/cleaned_covid_population.parquet")

    print("🎉 Cleaned & merged data saved to data/processed/")
    spark.stop()

if __name__ == "__main__":
    main()
