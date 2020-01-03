from nameko.web.handlers import http
from nameko.rpc import rpc, RpcProxy
from werkzeug.wrappers import Response
from jinja2 import Template
import os

class WebService:
    name = "web_service"
    jukebox_service = RpcProxy("jukebox_service")
    player_service = RpcProxy("player_service")
    with open("index.html") as f:
        index_html = f.read()
    
    @http('GET', '/')
    def index(self, request):
        all_songs = self.jukebox_service.get_all()
        all_songs_sorted_by_value = sorted(all_songs.items(), key=lambda kv: kv[1])
        all_songs_sorted_by_value.reverse()
        now_playing = self.player_service.get_now_playing()
        template = Template(self.index_html)
        h = template.render(all_songs = all_songs_sorted_by_value, now_playing = now_playing)
        r = Response(h)
        r.content_type = "text/html"
        return r

    @http('GET', '/like/<string:f_name>')
    def like(self, request, f_name):
        self.jukebox_service.like(f_name)
        return 302, {'Location': '/'}, ""

    @http('GET', '/delete/<string:f_name>')
    def delete(self, request, f_name):
        os.remove(os.path.join("mp3", f_name))
        self.jukebox_service.update()
        return 302, {'Location': '/'}, ""

    @http('GET', '/play/<string:f_name>')
    def play(self, request, f_name):
        self.player_service.play(f_name)
        return 302, {'Location': '/'}, ""
        
    @http('GET', '/playnext/')
    def playnext(self, request):
        self.jukebox_service.play_next()
        return 302, {'Location': '/'}, ""
        
    @http('GET', '/stop_playing/')
    def stop_playing(self, request):
        self.player_service.pause()
        return 302, {'Location': '/'}, ""
        
    @http('POST', '/upload_files')
    def upload_files(self, request):
        for f in request.files.getlist("mp3_files"):
            if f.filename.endswith(".mp3"):
                f_name = os.path.join("mp3", f.filename)
                f.save(f_name)
        self.jukebox_service.update()
        return 302, {'Location': '/'}, ""