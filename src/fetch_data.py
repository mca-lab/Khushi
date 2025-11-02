import os
import requests

DATASETS = {
    "covid19": "https://raw.githubusercontent.com/datasets/covid-19/main/data/countries-aggregated.csv",
    "world_population": "https://raw.githubusercontent.com/datasets/population/master/data/population.csv"
}

RAW_DIR = "data/raw"

def download_url(name, url, target_file):
    os.makedirs(RAW_DIR, exist_ok=True)
    
    print(f"Attempting to download {name} dataset from {url}")
    
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(target_file, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"**[SUCCESS]** {name} dataset saved to {target_file}")
    else:
        print(f"**[WARNING]** Couldn't download {name} automatically. Please download manually from {url} and place it in {target_file}")

def main():
    download_url("covid19", DATASETS["covid19"], os.path.join(RAW_DIR, "covid19.csv"))
    download_url("world_population", DATASETS["world_population"], os.path.join(RAW_DIR, "world_population.csv"))

if __name__ == "__main__":
    main()