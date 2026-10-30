from pathlib import Path
from astroquery.sdss import SDSS
import pandas as pd

#test script from sdss documentation
#pos = coords.SkyCoord('0h8m05.63s +14d50m23.3s', frame='icrs')
#xid = SDSS.query_region(pos, radius='5 arcsec', spectro=True, data_release=16)
#print(xid)

# actual data gathering script

# balanced query, simply calling for top 100000 returns this:
# class
# QSO 92454
# STAR 7546

stars = """
    SELECT TOP 50000
        p.objID, s.specObjID, s.z AS redshift, s.class,
        p.u, p.g, p.r, p.i, p.z, p.ra, p.dec
    FROM SpecObj AS s
    JOIN PhotoPrimary AS p ON p.objID = s.bestObjID
    WHERE s.class = 'STAR' AND p.clean = 1 AND s.zWarning = 0
    """

qsos = """
    SELECT TOP 50000
        p.objID, s.specObjID, s.z AS redshift, s.class,
        p.u, p.g, p.r, p.i, p.z, p.ra, p.dec
    FROM SpecObj AS s
    JOIN PhotoPrimary AS p ON p.objID = s.bestObjID
    WHERE s.class = 'QSO' AND p.clean = 1 AND s.zWarning = 0
"""


result_stars = SDSS.query_sql(stars, data_release = 16)
result_qsos = SDSS.query_sql(qsos, data_release = 16)


df_stars = result_stars.to_pandas()
df_qsos = result_qsos.to_pandas()

df = pd.concat([df_stars, df_qsos], ignore_index=True)
df = df.sample(frac=1, random_state=13).reset_index(drop=True)

proj_root = Path(__file__).resolve().parents[2]

raw_dir = proj_root / "data" / "raw"
raw_dir.mkdir(parents=True, exist_ok=True)
raw_data_path = raw_dir / "sdss_raw.csv"

df.to_csv(raw_data_path, index=False)
print(f"Saved {len(df)} rows to {raw_data_path}")
print(df["class"].value_counts())