import Adafruit_DHT
from main.SQL import TempHandler
import time

class Temps():
    def __init__(self):
        self.sensor = Adafruit_DHT.DHT11
        self.pin = 17
        self.humidity = 0
        self.temperature = 0

    def getDHT(self):
        self.humidity, self.temperature = Adafruit_DHT.read_retry(self.sensor, self.pin)
        dic ={}
        if self.humidity is not None and self.temperature is not None:
            dic['temperature'] = self.temperature
            dic['humidity'] = self.humidity
            temp = TempHandler.Temp(temperature=self.temperature, humidity=self.humidity)
            TempHandler.insert(temp)
            return dic
        else:
            return 'Failed to get reading. Try again!'

