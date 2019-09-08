#Libraries
import time
import RPi.GPIO as GPIO
import sys
import os
import board
import digitalio
import socket
#import pygame
#from omxplayer.player import OMXPlayer
import vlc
import mysql.connector
from datetime import datetime
import adafruit_character_lcd.character_lcd as characterlcd

from DbClass import DbClass
from lcd_rgb_backlight_display import Lcd_display
from DHT11_sensor import DHT11_sensor
from digital_led_strip import Ledstrip
from ultrasonic_distance import Ultrasonic


sensor1_update = True
timer = 0
naturepath = "/home/pi/Documents/Flask_web/static/music/nature music/"
playlist = "/home/pi/Documents/Flask_web/static/music/playlist/"
wakeup_time = 0

if __name__ == '__main__':
    try:
        #initialize classes
        lcd = Lcd_display()
        d11_sensor = DHT11_sensor()
        ledstrip = Ledstrip()
        dbclass = DbClass()
        ultrasonic = Ultrasonic()
        #pygame.mixer.init()
        
        #music
        music_state = dbclass.get_music()[0][1]
        music_name = dbclass.get_music()[0][2]
        
        player = vlc.MediaPlayer(playlist + music_name)
        if music_state == "on":
            player.play()
            #player.audio_set_volume(70)
        
        #leds
        state = dbclass.get_light()[0][1]
        ledcolor = dbclass.get_light()[0][2]
        
        if state == "on":
            ledstrip.ledstrip_state(True)
        else:
            ledstrip.ledstrip_state(False)
        
        ledstrip.ledstrip_color(ledcolor)
        
        #lcd
        lcd.set_bg_color(70, 0, 0)
        sensor1 = d11_sensor.info()
        
        gw = os.popen("ip -4 route show default").read().split()
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((gw[2], 0))
        ipaddr = s.getsockname()[0]
        
        while True:
            wakeup = dbclass.get_wakeup()
            wakeup_date = wakeup[0][3].strftime("%Y-%m-%d %H:%M:%S")
            wakeup_color = wakeup[0][1]
            wakeup_music = wakeup[0][2]
            
            now = datetime.now()
            wakeup_sync = now.strftime("%Y-%m-%d %H:%M:%S")
            print(now)
            print(wakeup_date)
            if wakeup_date == wakeup_sync:
                i = 0
                u = 34
                #pygame.mixer.music.load(naturepath + wakeup_music)
                player.release()
                player = vlc.MediaPlayer(naturepath + wakeup_music)
                player.play()
                ledstrip.ledstrip_color(wakeup_color)
                ledcolor = wakeup_color
                while i != 60:
                    tijd = datetime.now().strftime("%H:%M:%S  %a %d %b")
                    lcd.input_text(tijd + "\n"  + "\n" + sensor1 + "\n" + ipaddr)
                    ledstrip.ledstrip_brightness(i/60)
                    player.audio_set_volume(u)
                    #pygame.mixer.music.set_volume(u/1.5)
                    i += 1
                    if u <= 75:
                        u += 1
                        print(u)
                    time.sleep(0.9)
                    
                i = 0
                while i != 10:
                    tijd = datetime.now().strftime("%H:%M:%S  %a %d %b")
                    lcd.input_text(tijd + "\n"  + "\n" + sensor1 + "\n" + ipaddr)
                    i += 1
                    time.sleep(0.9)
                    
                player.stop()
                #pygame.mixer.music.stop()
                #pygame.mixer.music.unload()
            else:
                distance = ultrasonic.distance()
                print("Measured Distance = %.1f cm" % distance)
                if distance < 30:
                    timer += 1
                    if timer == 3:
                         dbclass.set_light("off") if state == "on" else dbclass.set_light("on")
                         timer = 0

                else:
                    timer = 0
                
                if sensor1_update and now.strftime("%S") == 30:
                    sensor1 = d11_sensor.info()
                    sensor1_update = False
                
                #music
                
                music_state_change = dbclass.get_music()[0][1]
                music_name_change = dbclass.get_music()[0][2]
                
                if music_state != music_state_change:
                    player.play() if music_state_change == "on" else player.stop()
                    music_state = music_state_change
                    
                if music_name_change != music_name:
                    if music_state == "on":
                        player.stop()
                    player.release()
                    player = vlc.MediaPlayer(playlist + music_name_change)
                    #player.audio_set_volume(70)
                    if music_state == "on":
                        player.play()
                    music_name = music_name_change
            
                #leds
                change = dbclass.get_light()[0][1]
                ledcolor_1 = dbclass.get_light()[0][2]
                print(ledcolor)
        
                if state != change:                
                    ledstrip.ledstrip_state(True) if change == "on" else ledstrip.ledstrip_state(False)
                    state = change
            
                if ledcolor != ledcolor_1:                
                    ledstrip.ledstrip_color(ledcolor_1)
                    ledcolor = ledcolor_1
            
                tijd = now.strftime("%H:%M:%S  %a %d %b")
                lcd.input_text(tijd + "\n"  + "\n" + sensor1 + "\n" + ipaddr)
            
                print("test.....")
                time.sleep(0.8)

        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("\nApp stopped by User")
        #ledstrip.ledstrip_state(False)
        sys.exit()
        
    finally:
        #pygame.mixer.music.stop()
        player.release()
        ledstrip.ledstrip_state(False)
        GPIO.setwarnings(False)
        GPIO.cleanup()