import json

def delete_station(index):
    with open(f"./assets/radio-stations.json", "r+") as file:
        file_data = json.load(file)

        file_data.pop(index)

    open("./assets/radio-stations.json", "w").write(
        json.dumps(file_data, sort_keys=True, indent=4, separators=(',', ': '))
    )

delete_station(26)