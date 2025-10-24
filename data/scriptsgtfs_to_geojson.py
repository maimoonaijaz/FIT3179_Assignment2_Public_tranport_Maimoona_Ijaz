import pandas as pd, json, sys

# paths
stops = "data/gtfs/stops.txt"         # put your GTFS stops.txt here
routes = "data/gtfs/routes.txt"       # optional (to tag lines)
# OUTPUT
out_geojson = "data/rail_stations.geojson"

# Load stops
df = pd.read_csv(stops)

# Keep stations / stops only (location_type: 0=stop/platform, 1=station)
if "location_type" in df.columns:
    df = df[df["location_type"].isin([0,1])]

# Minimal fields
df = df.rename(columns={"stop_name":"name","stop_lon":"lon","stop_lat":"lat"})
df = df[["name","lon","lat"]].dropna()

# Build GeoJSON FeatureCollection
features = []
for r in df.to_dict(orient="records"):
    features.append({
        "type":"Feature",
        "properties":{"name": r["name"]},   # add "line" later if you want
        "geometry":{"type":"Point","coordinates":[float(r["lon"]), float(r["lat"])]}
    })

fc = {"type":"FeatureCollection","features":features}
with open(out_geojson,"w",encoding="utf-8") as f:
    json.dump(fc,f,ensure_ascii=False)
print(f"Wrote {out_geojson}, features: {len(features)}")

