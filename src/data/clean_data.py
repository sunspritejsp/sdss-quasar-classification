from pathlib import Path
import pandas as pd

proj_root = Path(__file__).resolve().parents[2]
raw_data_path = proj_root/"data"/"raw"/"sdss_raw.csv"
processed_path = proj_root/"data"/"processed"/"sdss_clean.csv"

bands = ['u', 'g', 'r', 'i', 'z']

def main() -> None:
    df = pd.read_csv(raw_data_path)
    initial_count = len(df)

    bad_sentinels = (df[bands] == -9999).any(axis=1)
    bad_faint = (df[bands] > 30).any(axis=1)
    bad_qso_z = (df['class'] == 'QSO') & (df['redshift'] < 0.05)

    bad_rows = bad_faint | bad_qso_z | bad_sentinels

    df_clean = df[~bad_rows].copy()
    final_count = len(df_clean)
    dropped_count = initial_count - final_count

    processed_path.parent.mkdir(parents=True, exist_ok=True)
    df_clean.to_csv(processed_path, index=False)

    print(f"Initial count: {initial_count}")
    print(f"Dropped count: {dropped_count}")
    print(f"Final count: {final_count}")

if __name__ == "__main__":
    main()