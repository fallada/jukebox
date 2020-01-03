from nameko.rpc import rpc
import vlc
import os
import json

class PlayerService:
    name = "player_service"
    data ={}
    data["current_song"] = ""
    PLAYER = vlc.MediaPlayer()

    @rpc
    def play(self, file_name):
        self.PLAYER.set_mrl(os.path.join("mp3", file_name))
        self.PLAYER.play()
        self.data["current_song"] = file_name

    @rpc
    def get_now_playing(self):
        return self.data["current_song"] 
        
    @rpc
    def pause(self):
        self.PLAYER.pause()

    @rpc
    def unpause(self):
        self.PLAYER.play()

    @rpc
    def is_playing(self):
        if self.PLAYER.get_state() == vlc.State.Paused:
            return True
        else:
            return bool(self.PLAYER.is_playing())
        
