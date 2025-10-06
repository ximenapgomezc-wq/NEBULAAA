import requests
import xarray as xr
import numpy as np
import csv
from datetime import datetime
import os

# -------------------------------
# Inputs
# -------------------------------
year = 2024

# Lista de capitales: (Nombre, latitud, longitud)
locations = [
    ("Kabul", 34.5553, 69.2075),
    ("Tirana", 41.3275, 19.8189),
    ("Algiers", 36.7538, 3.0588),
    ("Andorra la Vella", 42.5075, 1.5218),
    ("Luanda", -8.8390, 13.2894),
    ("Saint John's", 17.1173, -61.8456),
    ("Buenos Aires", -34.6037, -58.3816),
    ("Yerevan", 40.1792, 44.4991),
    ("Canberra", -35.2809, 149.1300),
    ("Vienna", 48.2092, 16.3728),
    ("Baku", 40.4093, 49.8671),
    ("Nassau", 25.0343, -77.3963),
    ("Manama", 26.2285, 50.5860),
    ("Dhaka", 23.8103, 90.4125),
    ("Bridgetown", 13.0975, -59.6167),
    ("Minsk", 53.9006, 27.5590),
    ("Brussels", 50.8503, 4.3517),
    ("Belmopan", 17.2514, -88.7590),
    ("Porto-Novo", 6.4969, 2.6289),
    ("Thimphu", 27.4728, 89.6390),
    ("La Paz", -16.5000, -68.1500),
    ("Sarajevo", 43.8563, 18.4131),
    ("Gaborone", -24.6282, 25.9231),
    ("Brasilia", -15.7939, -47.8828),
    ("Bandar Seri Begawan", 4.9031, 114.9398),
    ("Sofia", 42.6977, 23.3219),
    ("Ouagadougou", 12.3714, -1.5197),
    ("Bujumbura", -3.3822, 29.3644),
    ("Phnom Penh", 11.5621, 104.8885),
    ("Yaoundé", 3.8480, 11.5021),
    ("Ottawa", 45.4215, -75.6992),
    ("Praia", 14.9160, -23.5090),
    ("Bangui", 4.3947, 18.5582),
    ("N'Djamena", 12.1348, 15.0557),
    ("Santiago", -33.4489, -70.6693),
    ("Beijing", 39.9042, 116.4074),
    ("Bogotá", 4.7110, -74.0721),
    ("Moroni", -11.7172, 43.2473),
    ("Kinshasa", -4.4419, 15.2663),
    ("Brazzaville", -4.2634, 15.2429),
    ("San José", 9.9281, -84.0907),
    ("Zagreb", 45.8150, 15.9785),
    ("Havana", 23.1136, -82.3666),
    ("Nicosia", 35.1856, 33.3823),
    ("Prague", 50.0755, 14.4378),
    ("Copenhagen", 55.6761, 12.5683),
    ("Djibouti", 11.5721, 43.1456),
    ("Roseau", 15.3092, -61.3790),
    ("Santo Domingo", 18.4861, -69.9312),
    ("Quito", -0.1807, -78.4678),
    ("Cairo", 30.0444, 31.2357),
    ("San Salvador", 13.6929, -89.2182),
    ("Malabo", 3.75, 8.7833),
    ("Asmara", 15.3229, 38.9251),
    ("Tallinn", 59.4370, 24.7536),
    ("Mbabane", -26.3054, 31.1367),
    ("Addis Ababa", 9.03, 38.74),
    ("Suva", -18.1248, 178.4501),
    ("Helsinki", 60.1699, 24.9384),
    ("Paris", 48.8566, 2.3522),
    ("Libreville", 0.4162, 9.4673),
    ("Banjul", 13.4549, -16.5790),
    ("Tbilisi", 41.7151, 44.8271),
    ("Berlin", 52.5200, 13.4050),
    ("Accra", 5.6037, -0.1870),
    ("Athens", 37.9838, 23.7275),
    ("Saint George's", 12.0561, -61.7486),
    ("Guatemala City", 14.6349, -90.5069),
    ("Conakry", 9.6412, -13.5784),
    ("Bissau", 11.8817, -15.6170),
    ("Georgetown", 6.8013, -58.1553),
    ("Port-au-Prince", 18.5944, -72.3074),
    ("Tegucigalpa", 14.0723, -87.1921),
    ("Budapest", 47.4979, 19.0402),
    ("Reykjavik", 64.1466, -21.9426),
    ("New Delhi", 28.6139, 77.2090),
    ("Jakarta", -6.2088, 106.8456),
    ("Tehran", 35.6892, 51.3890),
    ("Baghdad", 33.3152, 44.3661),
    ("Dublin", 53.3331, -6.2489),
    ("Jerusalem", 31.7683, 35.2137),
    ("Rome", 41.9028, 12.4964),
    ("Kingston", 17.9712, -76.7936),
    ("Tokyo", 35.6895, 139.6917),
    ("Amman", 31.9552, 35.9450),
    ("Astana", 51.1694, 71.4491),
    ("Nairobi", -1.2921, 36.8219),
    ("Tarawa", 1.4518, 172.9717),
    ("Pyongyang", 39.0392, 125.7625),
    ("Seoul", 37.5665, 126.9780),
    ("Pristina", 42.6629, 21.1655),
    ("Kuwait City", 29.3759, 47.9774),
    ("Bishkek", 42.8746, 74.5698),
    ("Vientiane", 17.9757, 102.6331),
    ("Riga", 56.9496, 24.1052),
    ("Beirut", 33.8938, 35.5018),
    ("Maseru", -29.3142, 27.4854),
    ("Monrovia", 6.3005, -10.7969),
    ("Tripoli", 32.8872, 13.1913),
    ("Vaduz", 47.1419, 9.5215),
    ("Vilnius", 54.6892, 25.2798),
    ("Luxembourg", 49.6117, 6.13),
    ("Antananarivo", -18.8792, 47.5079),
    ("Lilongwe", -13.9626, 33.7741),
    ("Kuala Lumpur", 3.1390, 101.6869),
    ("Male", 4.1755, 73.5093),
    ("Bamako", 12.6392, -8.0029),
    ("Valletta", 35.8997, 14.5146),
    ("Majuro", 7.0897, 171.3803),
    ("Nouakchott", 18.0735, -15.9582),
    ("Port Louis", -20.1669, 57.4989),
    ("Mexico City", 19.4326, -99.1332),
    ("Palikir", 6.9170, 158.1850),
    ("Chisinau", 47.0105, 28.8638),
    ("Monaco", 43.7333, 7.4167),
    ("Ulaanbaatar", 47.8864, 106.9057),
    ("Podgorica", 42.4304, 19.2594),
    ("Rabat", 33.9716, -6.8498),
    ("Maputo", -25.9622, 32.5801),
    ("Windhoek", -22.5609, 17.0658),
    ("Kathmandu", 27.7172, 85.3240),
    ("Amsterdam", 52.3676, 4.9041),
    ("Wellington", -41.2865, 174.7762),
    ("Managua", 12.1364, -86.2514),
    ("Niamey", 13.5116, 2.1254),
    ("Abuja", 9.0765, 7.3986),
    ("Pyongyang", 39.0392, 125.7625),
    ("Oslo", 59.9139, 10.7522),
    ("Muscat", 23.5859, 58.4059),
    ("Islamabad", 33.6844, 73.0479),
    ("Ngerulmud", 7.5000, 134.6242),
    ("Jerusalem", 31.7683, 35.2137),
    ("Panama City", 8.9824, -79.5199),
    ("Port Moresby", -9.4438, 147.1803),
    ("Asunción", -25.2637, -57.5759),
    ("Lima", -12.0464, -77.0428),
    ("Manila", 14.5995, 120.9842),
    ("Warsaw", 52.2297, 21.0122),
    ("Lisbon", 38.7169, -9.1399),
    ("Doha", 25.276987, 51.520008),
    ("Bucharest", 44.4268, 26.1025),
    ("Moscow", 55.7558, 37.6173),
    ("Kigali", -1.9706, 30.1044),
    ("Basseterre", 17.3026, -62.7177),
    ("Castries", 13.9094, -60.9789),
    ("Kingstown", 13.1600, -61.2248),
    ("Apia", -13.8333, -171.7667),
    ("San Marino", 43.9336, 12.4508),
    ("São Tomé", 0.3365, 6.7273),
    ("Riyadh", 24.7136, 46.6753),
    ("Dakar", 14.7167, -17.4677),
    ("Belgrade", 44.7872, 20.4573),
    ("Victoria", -4.6191, 55.4513),
    ("Freetown", 8.4657, -13.2317),
    ("Singapore", 1.3521, 103.8198),
    ("Bratislava", 48.1486, 17.1077),
    ("Ljubljana", 46.0569, 14.5058),
    ("Honiara", -9.4333, 159.9500),
    ("Mogadishu", 2.0469, 45.3182),
    ("Pretoria", -25.7479, 28.2293),
    ("Juba", 4.8594, 31.5713),
    ("Madrid", 40.4168, -3.7038),
    ("Colombo", 6.9271, 79.8612),
    ("Khartoum", 15.5007, 32.5599),
    ("Paramaribo", 5.8520, -55.2038),
    ("Stockholm", 59.3293, 18.0686),
    ("Bern", 46.9480, 7.4474),
    ("Damascus", 33.5138, 36.2765),
    ("Taipei", 25.0330, 121.5654),
    ("Dushanbe", 38.5598, 68.7870),
    ("Dodoma", -6.1630, 35.7516),
    ("Bangkok", 13.7563, 100.5018),
    ("Lomé", 6.1725, 1.2314),
    ("Nuku'alofa", -21.1394, -175.2044),
    ("Port of Spain", 10.6918, -61.2225),
    ("Tunis", 36.8065, 10.1815),
    ("Ankara", 39.9334, 32.8597),
    ("Ashgabat", 37.9601, 58.3261),
    ("Funafuti", -8.5167, 179.2167),
    ("Kampala", 0.3476, 32.5825),
    ("Kyiv", 50.4501, 30.5234),
    ("Abu Dhabi", 24.4539, 54.3773),
    ("London", 51.5074, -0.1278),
    ("Washington D.C.", 38.9072, -77.0369),
    ("Montevideo", -34.9011, -56.1645),
    ("Tashkent", 41.2995, 69.2401),
    ("Port Vila", -17.7333, 168.3167),
    ("Vatican City", 41.9029, 12.4534),
    ("Caracas", 10.4806, -66.9036),
    ("Hanoi", 21.0285, 105.8542),
    ("Sana’a", 15.3694, 44.1910),
    ("Lusaka", -15.3875, 28.3228),
    ("Harare", -17.8252, 31.0335)
    # … y así hasta completar 195 capitales
    # Para no hacer el mensaje demasiado largo aquí, tú debes completar las demás capitales con la misma estructura
]

username = "ximena.pg"
password = "midhog-kihda9-zycguZ"

base_url = "https://goldsmr4.gesdisc.eosdis.nasa.gov/data/MERRA2/M2T1NXSLV.5.12.4"

# Carpeta única para todos los archivos descargados
download_dir = "descargadosMERRA2"
os.makedirs(download_dir, exist_ok=True)

# Archivo CSV de salida
csv_file = f"weather_summary_intento18_2_{year}_WORLD_CAPITALS_195_3days.csv"
with open(csv_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "City", "Year", "Month", "Day", "Latitude", "Longitude",
        "Temperature_K", "Precipitation_kgm2",
        "Wind_speed_ms", "Wind_dir_deg", "Humidity_kgkg-1", "Cloud_top_temp_K"
    ])

# -------------------------------
# Iterar sobre los meses y los días 1, 15, 28
# -------------------------------
for month in range(1, 13):
    for day in [1, 15, 28]:
        try:
            date = datetime(year, month, day)
        except ValueError:
            continue

        file_name = f"MERRA2_400.tavg1_2d_slv_Nx.{date.year}{date.month:02d}{date.day:02d}.nc4"
        url = f"{base_url}/{date.year}/{date.month:02d}/{file_name}"
        local_file = os.path.join(download_dir, file_name)

        print(f"🔹 Procesando {date.strftime('%Y-%m-%d')} ...")

        # Descargar archivo si no existe
        if not os.path.exists(local_file):
            try:
                r = requests.get(url, auth=(username, password))
                if r.status_code == 200:
                    with open(local_file, "wb") as f:
                        f.write(r.content)
                    print(f"✅ Descargado {file_name}")
                else:
                    print(f"⚠️ Archivo no encontrado para {date.strftime('%Y-%m-%d')}, se omite.")
                    continue
            except Exception as e:
                print(f"⚠️ Error descargando {date.strftime('%Y-%m-%d')}: {e}")
                continue

        # Abrir NetCDF y extraer datos
        try:
            ds = xr.open_dataset(local_file, engine='netcdf4')

            # Calcular índices de lat/lon para todas las ciudades antes de iterar
            indices = {}
            for city, lat_val, lon_val in locations:
                lat_index = abs(ds['lat'] - lat_val).argmin().item()
                lon_index = abs(ds['lon'] - lon_val).argmin().item()
                indices[city] = (lat_index, lon_index)

            # Iterar sobre las ciudades usando los índices calculados
            for city, (lat_index, lon_index) in indices.items():
                lat_val, lon_val = next(l[1:] for l in locations if l[0] == city)

                temp_value = ds['T2M'].isel(time=0, lat=lat_index, lon=lon_index).values
                precip_value = ds['TQL'].isel(time=0, lat=lat_index, lon=lon_index).values
                u_wind = ds['U10M'].isel(time=0, lat=lat_index, lon=lon_index).values
                v_wind = ds['V10M'].isel(time=0, lat=lat_index, lon=lon_index).values
                wind_speed = np.sqrt(u_wind**2 + v_wind**2)
                wind_dir = np.degrees(np.arctan2(v_wind, u_wind)) % 360
                humidity = ds['QV2M'].isel(time=0, lat=lat_index, lon=lon_index).values
                cloud_temp = ds['CLDTMP'].isel(time=0, lat=lat_index, lon=lon_index).values

                # Guardar en CSV
                with open(csv_file, "a", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow([
                        city, date.year, date.month, date.day, lat_val, lon_val,
                        float(temp_value), float(precip_value),
                        float(wind_speed), float(wind_dir),
                        float(humidity), float(cloud_temp)
                    ])
                print(f"Procesado {city} {date.strftime('%Y-%m-%d')}")

            ds.close()

        except Exception as e:
            print(f"Falló para {date.strftime('%Y-%m-%d')}: {e}")

print(f"\n🎉 ¡Listo! CSV guardado como {csv_file}")
