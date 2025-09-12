import re
import struct

import requests

try:
    import urllib2
except ImportError:
    import urllib.request as urllib2


class RadioHelper:
    def get_song_info(self, url):
        encoding = "utf-8"
        request = urllib2.Request(url, headers={"Icy-MetaData": 1})
        response = urllib2.urlopen(request)
        metaint = int(response.headers["icy-metaint"])
        for _ in range(10):
            response.read(metaint)
            metadata_length = struct.unpack("B", response.read(1))[0] * 16
            metadata = response.read(metadata_length).rstrip(b"\0")
            m = re.search(rb"StreamTitle='([^']*)';", metadata)
            if m:
                title = m.group(1)
                if title:
                    return title.decode(encoding, errors="replace")
        else:
            return ""

    def get_stations_by_name(self, name: str):
        url = f"https://de2.api.radio-browser.info/json/stations/byname/{name}?order=votes&reverse=true"
        response = requests.get(url)
        response.raise_for_status()  # ✅ will raise an error if the request failed

        stations = [
            {
                "name": entry.get("name", ""),
                "src": entry.get("url", ""),
                "logo": entry.get("favicon", ""),
                "color": "#46A94B",
            }
            for entry in response.json()
        ]

        return stations
