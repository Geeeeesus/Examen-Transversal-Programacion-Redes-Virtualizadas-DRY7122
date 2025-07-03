import requests, urllib.parse
API_KEY = "TU_API_KEY"

def geo(city):
    url=f"https://graphhopper.com/api/1/geocode?q={urllib.parse.quote(city)}&limit=1&key={API_KEY}"
    p=requests.get(url).json()["hits"][0]["point"]
    return p["lat"],p["lng"]

def ruta(o,d,modo):
    lo,co=geo(o); ld,cd=geo(d)
    params={"point":[f"{lo},{co}",f"{ld},{cd}"],"profile":modo,"locale":"es","instructions":"true","key":API_KEY}
    data=requests.get("https://graphhopper.com/api/1/route",params=params).json()["paths"][0]
    print(f"{data['distance']/1000:.1f} km | {data['time']/1000/60:.1f} min")
    for i in data["instructions"]: print(i["text"])

while True:
    o=input("Origen (s=salir): ")
    if o.lower()=='s': break
    d=input("Destino: ")
    modo=input("car/bike/foot: ") or "car"
    ruta(o,d,modo)
