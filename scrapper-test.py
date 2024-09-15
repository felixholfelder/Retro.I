from __future__ import print_function
import re
import struct

try:
    import urllib2
except ImportError:  # Python 3
    import urllib.request as urllib2


def get_song_info(url):
    encoding = 'utf-8'
    request = urllib2.Request(url, headers={'Icy-MetaData': 1})
    response = urllib2.urlopen(request)
    #print(response.headers, file=sys.stderr)
    metaint = int(response.headers['icy-metaint'])
    for _ in range(10):
        response.read(metaint)
        metadata_length = struct.unpack('B', response.read(1))[0] * 16
        metadata = response.read(metadata_length).rstrip(b'\0')
        m = re.search(br"StreamTitle='([^']*)';", metadata)
        if m:
            title = m.group(1)
            if title:
                titleString = title.decode(encoding, errors='replace')
                try:
                    artist, title = titleString.split(" - ")
                except _:
                    artist, title = titleString.split(": ")

                return artist, title
    else:
        return "", ""


print(get_song_info("https://webstream.schlagerparadies.de/schlagerparadies128k.mp3"))
