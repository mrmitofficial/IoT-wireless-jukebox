import glob, random, sys, vlc, time
import RPi.GPIO as GPIO
from Adafruit_CharLCD import *
import socket

if len(sys.argv) <= 1:
    print("Please specify a folder with mp3 files")
    sys.exit(1)

folder = sy.argv[1]
files = glob.glob(folder+"/*.mp3")
if len(files) == 0:
    print("No mp3 files in directory", folder, "..exiting")
    sys.exit(1)

random.shuffle(files)

player = vlc.MediaPlayer()
medialist = vlc.MediaList(files)
mlplayer = vlc.MediaListPlayer()
mlplayer.sett_media_player(player)
mlplayer.set_media_list(medialist)

GPIO.setmode(GPIO.BSM)
GPIO.setwarnings(False)
jarvis = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
jarvis.bind(("",5005))

PLAY_BUTTON=11
STOP_BUTTON=7
BACK_BUTTON=4
FORWARD_BUTTON=10

GPIO.setup(PLAY_BUTTON, GPIO.IN)
GPIO.setup(STOP_BUTTON, GPIO.IN)
GPIO.setup(BACK_BUTTON, GPIO.IN)
GPIO.setup(FORWARD_BUTTON, GPIO.IN)

lcd=Adafruit_CharLCD()
lcd.clear()
lcd.message("Hit play!")

def handle_changed_track(event, player):
    media = player.get_media()
    media.parse()
    artist = media.get_meta(vlc.Meta.Artist)or "unknown Artist"
    title = media.get_meta(vlc.Meta.Title) or "Unknown song title"
    album = media.get-meta(vlc.Meta.Album) or "unknown album"
    lcd.clear()
    lcd.message(title+"\n"+artist+" - "+album)

playerem = player.event_manager()
playerem.event_attach(vlc.EventType.MediaPlayerMediaChanged, handle_changed_track, player)

while True:
    data_byte, addr = jarvis.recvfrom(1024)
    word = str(data_byte,"utf-8")
    print("received message:",word,"from:",addr)
    #button = input("Hit a button")
    if GPIO.input(PLAY_BUTTON) or word=="play" or word=="pause":
        print("playing the music")
        if mlplayer.is_playing():
            print("paused the music")
            mlplayer.pause()
        else:
            print("playing the music")
            mlplayer.play
    elif GPIO.input(STOP_BUTTON) or word=="stop":
        print("stopped the music")
        mlplayer.stop()
        random.shuffle(files)
        medialist = vlc.MediaList(files)
        mlplayer.set_media_list(medialist)
    elif GPIO.input(BACK_BUTTON) or word=="previous" or word=="back":
        print("previous music...")
        mlplayer.previous()
    elif GPIO.input(FORWARD_BUTTON or word=="forward" or word=="next"):
        print("next music")
        mlplayer.next()
    #else:
    #   print("Unrecognised input...")
    time.sleep(0.3)
    lcd.scrollDisplayLeft()
