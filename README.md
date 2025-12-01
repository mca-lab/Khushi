# Big Data Project: Pokemon and Pokemon species

## Project Overview
This project demonstrates a complete Big Data workflow using Python, PySpark, and Docker.
It automates data collection, cleaning, integration, and analysis using reproducible containerized pipelines.

The Pokémon dataset is widely used in ML/Data Cleaning demos because:

- It has mixed data types (text, numbers, categories). 
- It’s easy to visualize and test transformations.

---

## Research Question
“How do Pokémon attributes and species characteristics relate, and what patterns can be uncovered when combining both datasets?”

We aim to explore:

1. How Pokémon stats (HP, Attack, Defense, Speed, etc.) relate to species-level traits such as habitat, growth rate, capture rate, and color.

2. How merging the Pokémon and Pokémon Species datasets improves analysis, revealing broader patterns in characteristics and evolution.

3. What trends emerge across species groups, including stat differences by habitat, growth rate behavior, and type-based attribute patterns.

---

## Project Workflow

### Module 1. Data Collection & Ingestion
**Objective:** Automate dataset downloading and storage in a reproducible Docker environment.

**Tasks:**
- Fetch both datasets using Python requests.
- Store in `data/raw/` automatically when the Docker container runs.
- Support reproducible ingestion via `Dockerfile`.

**Deliverables:**
- `Dockerfile_fetch` + `requirements.txt`
- Scripts in `src/` (e.g., `fetch_data.py`)
- `data/raw/` populated when container runs

---

### Module 2. Data Cleaning & Integration
**Objective:** Prepare raw data for analysis using PySpark.

**Tasks:**
- Load both raw datasets using PySpark
- Clean missing, duplicates and inconsistent records.
- Join datasets on the country field.
- Derive metrics such as cases per million.
- Store processed data in `data/processed/`
- Docker container ensures reproducible cleaning pipeline

**Deliverables:**
- `Dockerfile_clean` + `requirements.txt`
- Scripts in `src/` (e.g., `clean_data.py`)
- Processed Parquet/CSV files in `data/processed/` ready for analysis

---

