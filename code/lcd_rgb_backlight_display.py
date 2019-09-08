#Libraries
import time
import RPi.GPIO as GPIO
import sys
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd

# Modify this if you have a different sized character LCD
lcd_columns = 20
lcd_rows = 4

# Raspberry Pi Pin Config:
lcd_rs = digitalio.DigitalInOut(board.D26)  # pin 4
lcd_en = digitalio.DigitalInOut(board.D19)  # pin 6
lcd_d7 = digitalio.DigitalInOut(board.D13)  # pin 14
lcd_d6 = digitalio.DigitalInOut(board.D6)  # pin 13
lcd_d5 = digitalio.DigitalInOut(board.D5)  # pin 12
lcd_d4 = digitalio.DigitalInOut(board.D25)  # pin 11
#lcd_backlight = digitalio.DigitalInOut(board.D4) #to read write not need it!!!!

red = digitalio.DigitalInOut(board.D21)
green = digitalio.DigitalInOut(board.D20)
blue = digitalio.DigitalInOut(board.D16)

# Initialise the LCD class
lcd = characterlcd.Character_LCD_RGB(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns,
                                     lcd_rows, red, green, blue)
#lcd.display = True
RED = [100, 0, 0]
GREEN = [0, 100, 0]
BLUE = [0, 0, 100]

def play_test():
    lcd.clear()
    lcd.message = "CircuitPython\nRGB Test: RED"
    lcd.color = RED
    time.sleep(1)

    lcd.clear()
    lcd.message = 'CircuitPython\nRGB Test: GREEN'
    lcd.color = RED
    time.sleep(1)

    lcd.clear()
    lcd.message = 'CircuitPython\nRGB Test: BLUE'
    lcd.color = RED
    time.sleep(1)

class Lcd_display:
    def __init__(self):
        self.lcd = lcd
        
    def set_bg_color(self, r, g, b):
        list = [r, g, b]
        self.lcd.color = list 
    
    def set_position(self, column, row):
        self.lcd.cursor_position(column, row)
    
    def input_text(self, string):
        lcd.message = string        
        
    def __del__(self):
        lcd.clear()


if __name__ == '__main__':
    try:
        while True:
            play_test()
            print("test.....")
            time.sleep(1)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("\nLed RGB display stopped by User")
        lcd.clear()
        sys.exit()
        
    finally:
        GPIO.setwarnings(False)
        GPIO.cleanup()