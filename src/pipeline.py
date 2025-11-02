import subprocess

print("Starting Big Data pipeline...")

# Step 1: Fetch data
print("\nStep 1: Downloading raw datasets...")
subprocess.run(["python", "fetch_data.py"], check=True)

# Step 2: Clean and process data
print("\nStep 2: Cleaning and transforming datasets...")
subprocess.run(["python", "clean_data.py"], check=True)

print("\nPipeline completed successfully! All processed files are saved in data/processed/")
