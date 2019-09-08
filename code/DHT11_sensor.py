#Libraries
import RPi.GPIO as GPIO
import Adafruit_DHT
import time
import sys

DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4

def info_test():
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        print(u"Temp: {0}\u00B0C Humidity: {1}%".format(int(temperature), int(humidity)))


class DHT11_sensor:
    def __init__(self):
        self.sensor = DHT_SENSOR
        self.pin = DHT_PIN
        
    def info(self):
        humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.pin)
        if humidity is not None and temperature is not None:
            return u"Temp: {0}C Lv: {1}%".format(int(temperature), int(humidity))
        
    
    
if __name__ == '__main__':
    try:
        while True:
            info_test()
            time.sleep(5)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("DHT11 sensor stopped by User")
        sys.exit()
        
    finally:
        GPIO.setwarnings(False)
        GPIO.cleanup()