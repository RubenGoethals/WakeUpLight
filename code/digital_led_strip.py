#Libraries
import RPi.GPIO as GPIO
import time
import board
import webcolors
import sys
import adafruit_dotstar as dotstar

numpixels = 77 # Number of LEDs in strip
bn = 0.5 # Brightness
led_on_test = True
dots = dotstar.DotStar(board.SCK, board.MOSI, numpixels, brightness=bn)

def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.css3_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]

def get_colour_name(requested_colour):
    try:
        closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        closest_name = closest_colour(requested_colour)
        actual_name = None
    return actual_name, closest_name

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def ledstrip_test(r, g, b):
        dots.fill((r, g, b))
        dots.show()

def ledstrip_brightness(value):
        dots.brightness = value

class Ledstrip:
    def __init__(self):
        self.dots = dots
        
    def ledstrip_color(self, hex_color):
        self.dots.fill(hex_to_rgb(hex_color))
 
    def ledstrip_brightness(self, value):
        self.dots.brightness = value
    
    def ledstrip_state(self, led_on):
        if led_on:
            self.dots.brightness = 0.1
        else:
            self.dots.brightness = 0.0
            
    def __del__(self):
        dots.brightness = 0.0
        


if __name__ == '__main__':
    try:
        while True:
            red_color = int(input("Enter the red color value: "))
            green_color = int(input("Enter the green color value: "))
            blue_color = int(input("Enter the blue color value: "))
            
            ledstrip_test(red_color, green_color, blue_color)
            requested_colour = (red_color, green_color, blue_color)
            actual_name, closest_name = get_colour_name(requested_colour)

            print("Actual colour name:", actual_name, ", closest colour name:", closest_name)
            
            ledstrip_brightness(0.5)
            time.sleep(2)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("\nLedstrip stopped by User")
        sys.exit()
        
    finally:
        GPIO.setwarnings(False)
        GPIO.cleanup()