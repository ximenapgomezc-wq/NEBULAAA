from flask import Flask, render_template, request, jsonify
import pandas as pd
import os
import re

app = Flask(__name__, static_folder="static", template_folder="templates")

CSV_PATH = os.path.join("data", "weather_summary_intento18_2_2024_WORLD_CAPITALS_195_3days.csv")

def _normalize(name):
    return re.sub(r'[^a-z0-9]', '', name.lower() if isinstance(name, str) else "")

def map_columns(df):
    norm_map = { _normalize(c): c for c in df.columns }
    def find(key_parts):
        for norm, orig in norm_map.items():
            if all(k in norm for k in key_parts):
                return orig
        for norm, orig in norm_map.items():
            for k in key_parts:
                if k in norm:
                    return orig
        return None

    col_map = {}
    col_map['City'] = find(['city'])
    col_map['Latitude'] = find(['lat','lattitude'])
    col_map['Longitude'] = find(['lon','long'])
    col_map['Year'] = find(['year'])
    col_map['Month'] = find(['month'])
    col_map['Day'] = find(['day'])
    col_map['Temperature_K'] = find(['temperature','temperatura'])
    col_map['Precipitation_kgm2'] = find(['precipitation','precip'])
    col_map['Wind_speed_ms'] = find(['wind','speed'])
    col_map['Wind_dir_deg'] = find(['wind','dir'])
    col_map['Humidity_kgkg-1'] = find(['humid'])
    col_map['Cloud_top_temp_K'] = find(['cloud','top','temp'])
    return col_map

if not os.path.exists(CSV_PATH):
    raise FileNotFoundError(f"CSV not found at {CSV_PATH}. Coloca el archivo ahí.")

_raw = pd.read_csv(CSV_PATH)
_colmap = map_columns(_raw)
df = _raw.rename(columns={ _colmap[k]: k for k in _colmap if _colmap[k] is not None }).copy()

num_cols = ['Latitude','Longitude','Year','Month','Day',
            'Temperature_K','Precipitation_kgm2','Wind_speed_ms','Wind_dir_deg','Humidity_kgkg-1','Cloud_top_temp_K']
for c in num_cols:
    if c in df.columns:
        df[c] = pd.to_numeric(df[c], errors='coerce')

df['City'] = df['City'].astype(str)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/capitals", methods=["GET"])
def capitals():
    caps = df[['City','Latitude','Longitude']].dropna().drop_duplicates(subset=['City']).sort_values('City')
    return jsonify([{"City":r.City,"Latitude":float(r.Latitude),"Longitude":float(r.Longitude)} for _,r in caps.iterrows()])

@app.route("/predict", methods=["POST"])
def predict():
    payload = request.get_json(force=True)
    city = str(payload.get("city","")).strip()
    date_raw = payload.get("date")

    if not city:
        return jsonify({"error":"City is required"}),400

    month = None
    if date_raw:
        try:
            dt = pd.to_datetime(date_raw, errors='coerce')
            if dt is not pd.NaT:
                month = dt.month
        except: pass

    city_mask = df['City'].str.strip().str.lower()==city.lower()
    subset = df[city_mask]
    if subset.empty:
        return jsonify({"error": f"No data for city {city}"}),404
    if month:
        subset = subset[subset['Month']==month]
        if subset.empty:
            return jsonify({"error": f"No data for city {city} in month {month}"}),404

    vars_to_avg = ['Temperature_K','Precipitation_kgm2','Wind_speed_ms','Wind_dir_deg','Humidity_kgkg-1','Cloud_top_temp_K']
    means = subset[vars_to_avg].mean(numeric_only=True).to_dict()

    # Convert Cloud Top Temp to Celsius
    if 'Cloud_top_temp_K' in means and pd.notna(means['Cloud_top_temp_K']):
        means['Cloud_top_temp_K'] = means['Cloud_top_temp_K'] - 273.15

    lat = subset['Latitude'].mean() if 'Latitude' in subset.columns else None
    lon = subset['Longitude'].mean() if 'Longitude' in subset.columns else None

    subset_sorted = subset.sort_values(by=['Year','Month','Day'])
    top3 = {v: subset_sorted[v].head(3).tolist() for v in vars_to_avg}

    # Convert top3 Cloud Temp to Celsius
    top3['Cloud_top_temp_K'] = [round(x-273.15,2) for x in top3['Cloud_top_temp_K']]

    result = {
        "City":city,
        "Month_filtered": month,
        "Latitude": float(lat) if pd.notna(lat) else None,
        "Longitude": float(lon) if pd.notna(lon) else None,
    }
    # add averages
    for v in vars_to_avg:
        val = means[v]
        result[v+"_avg"] = round(float(val),2) if pd.notna(val) else None
        result[v+"_top3"] = top3[v]

    return jsonify(result)

if __name__=="__main__":
    app.run(debug=True)
