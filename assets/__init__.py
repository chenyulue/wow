from pathlib import Path

CURDIR = Path(__file__).parent

# Data sets path
DATA_18W01 = CURDIR / "data" / "18w01_Looks_vs_Personality.csv"
DATA_18W02 = CURDIR / "data" / "18W02_Sample_Superstore.csv"
DATA_18W03 = DATA_18W02
DATA_18W04 = DATA_18W02


if __name__ == "__main__":
    print(DATA_18W01)
