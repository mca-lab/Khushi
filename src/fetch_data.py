import os
import requests

DATASETS = {
    "pokemon": "https://raw.githubusercontent.com/veekun/pokedex/master/pokedex/data/csv/pokemon.csv",
    "species": "https://raw.githubusercontent.com/veekun/pokedex/master/pokedex/data/csv/pokemon_species.csv"
}

RAW_DIR = "data/raw"

def download_url(name, url, target_file):
    os.makedirs(RAW_DIR, exist_ok=True)
    print(f"\n📥 Downloading {name} from {url}")

    try:
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()

        with open(target_file, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"✅ SUCCESS: {name} saved to {target_file}")

    except Exception as e:
        print(f"❌ ERROR downloading {name}: {e}")

def main():
    download_url("Pokemon Dataset", DATASETS["pokemon"], os.path.join(RAW_DIR, "pokemon.csv"))
    download_url("Pokemon Species Dataset", DATASETS["species"], os.path.join(RAW_DIR, "pokemon_species.csv"))

if __name__ == "__main__":
    main()
