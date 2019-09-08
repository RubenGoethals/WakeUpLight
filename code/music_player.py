#Libraries
import RPi.GPIO as GPIO
from pygame import mixer as pm
import time
import glob
import random
import sys

soundfiles = glob.glob("music_player/*.mp3")

def play_music():
    pm.init()
    pm.music.load(random.choice(soundfiles))
    pm.play()
    
    
if __name__ == '__main__':
    try:
        while True:
            play_music()
            time.sleep(5)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Music player stopped by User")
        pm.stop()
        sys.exit()
        
    finally:
        GPIO.setwarnings(False)
        GPIO.cleanup()