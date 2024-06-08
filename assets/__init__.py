from pathlib import Path

CURDIR = Path(__file__).parent
DATA_DIR = CURDIR / "data"

# Data sets path
DATA_18W01 = DATA_DIR / "18w01_Looks_vs_Personality.csv"
DATA_18W02 = DATA_DIR / "18W02_Sample_Superstore.csv"
DATA_18W03 = DATA_18W02
DATA_18W04 = DATA_18W02
DATA_18W05 = DATA_18W02
DATA_18W06 = DATA_18W02
DATA_18W07 = DATA_18W02
DATA_18W08 = DATA_DIR / "18W08_babynames1950+.csv"
DATA_18W09 = DATA_DIR / "18W09_MLB_Ethnicity_1947-2016.csv"
DATA_18W10 = DATA_18W02
DATA_18W11 = DATA_18W02
DATA_18W12 = DATA_18W02

if __name__ == "__main__":
    print(DATA_18W01)
