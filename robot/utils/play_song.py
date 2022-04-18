import vlc


def play_song(file_name: str) -> vlc.MediaPlayer:
    media_player = vlc.MediaPlayer()
    media = vlc.Media(file_name)
    media_player.set_media(media)
    media_player.play()


def stop_song(media_player: vlc.MediaPlayer):
    media_player.stop()
