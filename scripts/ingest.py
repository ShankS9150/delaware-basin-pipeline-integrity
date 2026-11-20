"""Load raw RRC and Census data into PostGIS (EPSG:26913)."""
import glob
from pathlib import Path

import geopandas as gpd
from sqlalchemy import create_engine

ENGINE = create_engine("postgresql+psycopg2://localhost/pipeline")
TARGET_CRS = 26913          # NAD83 / UTM zone 13N, meters
DATA = Path("Data")


def to_postgis(gdf, table, source_crs):
    """Reproject, lowercase column names, and write to raw.<table>."""
    if gdf.crs is None:
        gdf = gdf.set_crs(source_crs)
    gdf = gdf.to_crs(TARGET_CRS)
    gdf.columns = [c.lower() for c in gdf.columns]
    gdf = gdf.rename_geometry("geom")
    gdf.to_postgis(table, ENGINE, schema="raw", if_exists="replace", index=False)
    print(f"  raw.{table:<20} {len(gdf):>8,} features  {gdf.geom_type.unique().tolist()}")


def load_folder(folder, prefix, source_crs=4267):   # RRC data is NAD27 lat/long
    files = sorted(glob.glob(str(DATA / folder / "*.shp")))
    if not files:
        raise FileNotFoundError(f"No shapefiles in Data/{folder}")
    for f in files:
        table = f"{prefix}_{Path(f).stem.lower()}"
        to_postgis(gpd.read_file(f), table, source_crs)


print("RRC pipelines")
load_folder("pipeline389", "pipe")

print("RRC wells")
load_folder("well389", "well")

print("Reeves County boundary")
counties = gpd.read_file(DATA / "tl_2026_us_county" / "tl_2026_us_county.shp")
to_postgis(counties[counties["GEOID"] == "48389"], "county", 4269)

roads = glob.glob(str(DATA / "tl_2026_48389_roads" / "*.shp"))
if roads:
    print("Roads")
    to_postgis(gpd.read_file(roads[0]), "roads", 4269)
else:
    print("Roads: skipped (not downloaded)")

print("Done.")
