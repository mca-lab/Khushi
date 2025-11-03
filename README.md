# Big Data Project: COVID-19 Impact vs World Population

## Project Overview
This project demonstrates a complete Big Data workflow using Python, PySpark, and Docker.
It automates data collection, cleaning, integration, and analysis using reproducible containerized pipelines.

The objective is to study how COVID-19 case trends vary with population size across different countries over time.

---

## Research Question
“How does the total population of a country relate to the number of confirmed COVID-19 cases and deaths over time?”

We aim to explore:

1. Whether population size correlates with total cases and deaths.

2. How per-capita infection and death rates vary across regions.

3. Temporal trends in COVID-19 spread among high- vs low-population countries.

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

