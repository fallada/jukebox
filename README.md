# jukebox
Jukebox for Parties: Everybody can upload songs and vote them up with "likes". Jukebox plays randomly all songs and takes into account how many likes a song has.

Tested on Ubuntu and Raspbian with Raspberry Pi 4

You will need:

    pip3 install nameko
    pip3 install python-vlc
    pip3 install Jinja2
    apt install docker.io
    apt install alsa-base pulseaudio
    apt install vlc
    docker run -d -p 5672:5672 rabbitmq:3

Start the jukebox with:

    sudo nameko run web player jukebox

and find the jukebox under:
    
    http://localhost:8000
