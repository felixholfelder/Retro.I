import requests


def get_stations_by_name(name):
    response = requests.get(f"https://de1.api.radio-browser.info/json/stations/byname/{name}?order=votes&reverse=true")

    l = []
    for e in response.json():
        l.append({"name": e["name"], "src": e["url"], "logo": e["favicon"], "color": "#00ff00"})

    return l


print(get_stations_by_name("Antenne bayern"))
