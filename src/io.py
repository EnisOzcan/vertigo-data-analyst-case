from pathlib import Path
import pandas as pd

def load_gz_csvs(raw_dir: Path) -> pd.DataFrame:
    """
    Load and concatenate all .csv.gz files in the given directory.
    """
    raw_dir = Path(raw_dir)
    dfs = []

    gz_files = sorted(raw_dir.glob("*.csv.gz"))

    if not gz_files:
        raise FileNotFoundError(f"No .csv.gz files found in {raw_dir}")

    for path in gz_files:
        print(f"Loading: {path.name}")
        df_part = pd.read_csv(path, compression="gzip")
        dfs.append(df_part)

    return pd.concat(dfs, ignore_index=True)