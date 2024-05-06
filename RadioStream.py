import vlc


class RadioStream:
    def stream(self, link):
        p = vlc.MediaPlayer(link)
        p.play()
