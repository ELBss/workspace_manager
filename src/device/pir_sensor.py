from machine import Pin
import utime


SENSOR_PIN = 23

class PIR_Sensor:
    def __init__(self, pin):
        self.pin = Pin(pin, Pin.IN)

    def is_movement_detected(self):
        return self.pin.value() == 1
    
    def calculate(self, numbers):
        mean = sum(numbers) / len(numbers)
        variance = sum((x - mean) ** 2 for x in numbers) / len(numbers)
        return variance ** 0.5, mean

    def observation_cycle(self):
        signals_list = []
        for _ in range(10):
            i = 0
            sens_list = []
            while i < 100:
                sens_list.append(self.is_movement_detected())
                i += 1
                utime.sleep_ms(25)
            print("True:", sens_list.count(1))
            signals_list.append(sens_list.count(1))
        return self.calculate(signals_list)

    