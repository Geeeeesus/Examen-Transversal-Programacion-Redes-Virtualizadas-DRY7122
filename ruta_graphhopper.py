import requests, urllib.parse

API_KEY = "SU_API_KEY"

def geocode_city(ciudad):
    url = f"https://graphhopper.com/api/1/geocode?q={urllib.parse.quote(ciudad)}&limit=1&key={API_KEY}"
    resp = requests.get(url)
    data = resp.json()
    if resp.status_code == 200 and data.get("hits"):
        p = data["hits"][0]["point"]
        return p["lat"], p["lng"]
    else:
        return None

def obtener_ruta(lat_o, lon_o, lat_d, lon_d, vehiculo):
    base_url = "https://graphhopper.com/api/1/route"
    params = {
        "point": [f"{lat_o},{lon_o}", f"{lat_d},{lon_d}"],
        "profile": vehiculo,
        "locale": "es",
        "instructions": "true",
        "key": API_KEY
    }
    resp = requests.get(base_url, params=params)
    if resp.status_code == 200:
        data = resp.json()
        if data.get("paths"):
            return data["paths"][0]
    return None

print("=== Calculadora de Rutas (GraphHopper) ===")
print("Ingrese 's' en cualquier momento para salir.\n")
while True:
    origen = input("Ciudad de Origen: ")
    if origen.lower() == 's':
        break
    destino = input("Ciudad de Destino: ")
    if destino.lower() == 's':
        break
    vehiculo = input("Medio de transporte [car/bike/foot]: ").lower()
    if vehiculo not in ("car", "bike", "foot"):
        print("Medio de transporte no válido, usando 'car' por defecto.")
        vehiculo = "car"
    # Geocodificación
    coords_origen = geocode_city(origen)
    coords_dest = geocode_city(destino)
    if not coords_origen or not coords_dest:
        print("No se encontraron coordenadas para alguna de las ciudades. Intente nuevamente.")
        continue
    # Routing
    ruta = obtener_ruta(coords_origen[0], coords_origen[1], coords_dest[0], coords_dest[1], vehiculo)
    if ruta is None:
        print("No se pudo calcular la ruta, intente con otras ciudades.")
        continue
    # Mostrar resultados
    dist_m = ruta["distance"]
    dist_km = dist_m/1000.0
    dist_mi = dist_km/1.60934
    time_ms = ruta["time"]
    hrs = int(time_ms/1000//3600); mins = int(time_ms/1000%3600//60); secs = int(time_ms/1000%60)
    print(f"\nDistancia: {dist_mi:.1f} millas / {dist_km:.1f} km")
    print(f"Duración: {hrs:02d}:{mins:02d}:{secs:02d} (hh:mm:ss)")
    print("-"*50)
    for instr in ruta["instructions"]:
        texto = instr["text"]; tramo_m = instr["distance"]
        tramo_km = tramo_m/1000.0; tramo_mi = tramo_km/1.60934
        print(f"{texto} ({tramo_km:.1f} km / {tramo_mi:.1f} millas)")
    print("="*50 + "\n")
