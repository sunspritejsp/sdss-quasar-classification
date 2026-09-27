"""
Feature Engineering for SDSS DR16 Star Quasar Classification

derives astronomical color indices (u_g, g_r, r_i, i_z), encodes the target class (QSO =1; STAR = 0),
segregates features and metadata.
"""

import argparse
import logging
from pathlib import Path
import numpy as np
import pandas as pd

# SCHEMA CONSTANTS
RAW_BANDS: list[str] = ["u", "g", "r", "i", "z"]
COLOR_FEATURES: list[str] = ["u_g", "g_r", "r_i", "i_z"]
FEATURE_COLS: list[str] = RAW_BANDS + COLOR_FEATURES
METADATA_COLS: list[str] = ["objID", "specObjID", "ra", "dec", "redshift"]
TARGET_COL: str = "target"
CLASS_MAPPING: dict[str, int] = {"STAR": 0, "QSO": 1}

logger = logging.getLogger("SDSS Feature Engineering Pipeline LOG")

def load_data(filepath: Path) -> pd.DataFrame:
    """Load raw cleaned SDSS dataset."""
    
    if not filepath.exists():
        logger.warning("File path does not exist.")
        raise FileNotFoundError(f"Input file does not exist: {filepath}")
    
    logger.info(f"Loading data from: {filepath}!")
    df = pd.read_csv(filepath) 
    logger.info(f"Loaded dataset with shape {df.shape}")

    return df


def compute_colors(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate adjacent photometric color indices (u-g, g-r, r-i, i-z)."""

    df = df.copy()
    logger.info("Created a copy of the dataframe!")

    logger.info("Computing adjacent color indices (u-g, g-r, r-i, i-z)...")
    df["u_g"] = df["u"] - df["g"]
    df["g_r"] = df["g"] - df["r"]
    df["r_i"] = df["r"] - df["i"]
    df["i_z"] = df["i"] - df["z"]

    return df


def encode_target(df: pd.DataFrame) -> pd.DataFrame:
    """Map string classes ('STAR', 'QSO') to binary integers (0, 1)."""
    if "class" not in df.columns:
        raise KeyError("Column 'class' missing from dataframe")
    
    df = df.copy()
    df[TARGET_COL] = df["class"].map(CLASS_MAPPING)

    if df[TARGET_COL].isna().any():
        unmapped = df.loc[df[TARGET_COL].isna(), "class"].unique()
        raise ValueError(f"Found unexpected classes that could not be mapped: {unmapped}")

    df[TARGET_COL] = df[TARGET_COL].astype(int)
    return df


def validate_data(df: pd.DataFrame, expected_rows: int = 99954) -> None:
    """
    Validate row counts, ensure no NaN or inf values exist in FEATURE_COLS or TARGET_COL,
    and verify the target distribution.
    """

    required_cols = set(FEATURE_COLS + METADATA_COLS + [TARGET_COL])
    missing_cols = required_cols - set(df.columns)

    if missing_cols:
        raise KeyError(f"Missing required columns in dataset: {missing_cols}")

    unique_targets = set(df[TARGET_COL].unique())
    expected_targets = {0, 1}


    cols_to_check = FEATURE_COLS + [TARGET_COL]
    if not  len(df) == expected_rows:
        raise ValueError(f"Row quantity mismatch, {expected_rows} expected, got {len(df)}")

    if df[cols_to_check].isna().any().any():
        raise ValueError("Found unexpected NaN values in features or target.")
    
    if not np.isfinite(df[cols_to_check].to_numpy()).all():
        raise ValueError("Non-finite values (NaN, inf, or -inf) detected in features or target.")

    if not unique_targets.issubset(expected_targets):
        raise ValueError(f"Invalid target values detected: {unique_targets - expected_targets}")

    logger.info("Target class distribution:\n%s", df[TARGET_COL].value_counts(normalize=True))

def save_data(df: pd.DataFrame, output_path: Path) -> None:
    """Save the engineered dataset with index=False, containing only features and target."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    export_cols = FEATURE_COLS + [TARGET_COL]
    df[export_cols].to_csv(output_path, index=False)
    logger.info(f"Saved dataset with shape {df[export_cols].shape} to {output_path}.")


def main() -> None:
    """Orchestrate the feature engineering pipeline via CLI arguments."""
    logging.basicConfig(
        level = logging.INFO,
        format = "%(asctime)s [%(levelname)s] %(message)s",
        datefmt = "%Y-%m-%d %H:%M:%S",
    )
    parser = argparse.ArgumentParser(description="SDSS Feature Engineering Pipeline")

    parser.add_argument(
        "--input",
        type = Path,
        default = Path("data/processed/sdss_clean.csv"),
        help = "Path to the cleaned SDSS input CSV",
    )

    parser.add_argument(
        "--output",
        type = Path,
        default = Path("data/processed/sdss_features.csv"),
        help = "Path where engineered features will be saved",
    )

    args = parser.parse_args()

    df = load_data(args.input)
    df = compute_colors(df)
    df = encode_target(df)

    validate_data(df)
    save_data(df, args.output)

if __name__ == "__main__":
    main()