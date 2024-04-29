from pathlib import Path

CURDIR = Path(__file__).parent

# Data sets path
DATA_18W01 = CURDIR / "data" / "18w01_Looks_vs_Personality.csv"
DATA_18W02 = CURDIR / "data" / "18W02_Sample_Superstore.csv"


if __name__ == "__main__":
    print(DATA_18W01)