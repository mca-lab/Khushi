from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import os

RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"

def main():
    spark = SparkSession.builder.appName("PokemonCleaner").getOrCreate()

    print("\n🔍 Loading raw Pokémon CSV files...")

    # Load CSV files
    pokemon_df = spark.read.csv(f"{RAW_DIR}/pokemon.csv", header=True, inferSchema=True)
    species_df = spark.read.csv(f"{RAW_DIR}/pokemon_species.csv", header=True, inferSchema=True)

    print("📊 Rows loaded:")
    print(f"pokemon: {pokemon_df.count()}")
    print(f"species: {species_df.count()}")

    print("\n🧼 Cleaning data...")

    # Drop duplicate IDs
    pokemon_df = pokemon_df.dropDuplicates(["id"])
    species_df = species_df.dropDuplicates(["id"])

    # Rename the conflicting identifier column
    species_df = species_df.withColumnRenamed("identifier", "species_name")

    # Join on id
    joined_df = pokemon_df.join(species_df, "id", "inner")

    # Create cleaned final DataFrame
    cleaned = (
        joined_df
        .withColumn("name", col("species_name"))
        .drop("species_name")
    )

    # Ensure output folder exists
    os.makedirs(PROCESSED_DIR, exist_ok=True)

    # Save cleaned data
    cleaned.write.mode("overwrite").csv(PROCESSED_DIR, header=True)

    print(f"\n✅ Cleaned data saved to: {PROCESSED_DIR}")

    spark.stop()

if __name__ == "__main__":
    main()
