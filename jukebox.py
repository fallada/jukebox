from nameko.rpc import rpc, RpcProxy
import os
import json
import random
from nameko.timer import timer


class JukeboxService:
    name = "jukebox_service"
    player_service = RpcProxy("player_service")
    # {"bla.mp3" : 12, ...}
    data = {}
    index = []
    
    def __init__(self):
        self._update()

    def _update(self):
        old_data = self.data.copy()
        #built from scratch, so the deleted files disapear
        self.data.clear()
        for f_name in os.listdir("mp3"):
            if f_name not in old_data.keys():
                #no likes yet
                self.data[f_name] = 0
            else:
                self.data[f_name] = old_data[f_name]
        self._update_index()
    
    def _update_index(self):
        self.index = []
        for k in self.data.keys():
            for o in range(self.data[k] + 1):
                self.index.append(k)

    @timer(interval=1)
    def poller(self):
        # method executed every second
        if not self.player_service.is_playing():
            self.play_next()

    @rpc
    def play_next(self):
        n = self.get_next_song()
        self.player_service.play(n)

    @rpc
    def get_index(self):
        return self.index

    @rpc
    def update(self):
        self._update()

    @rpc
    def get_all(self):
        return self.data

    @rpc
    def like(self, f_name):
        self.data[f_name] += 1
        self._update_index()
        
    @rpc
    def get_next_song(self):
        return random.choice(self.index)