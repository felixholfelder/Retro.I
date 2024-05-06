import vlc


class RadioStream:
    def stream(link):
        p = vlc.MediaPlayer(link)
        p.play()
