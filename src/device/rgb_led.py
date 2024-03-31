from machine import Pin, PWM
import utime

RED_PIN = 19
GREEN_PIN = 18
BLUE_PIN = 5

class RGB_LED:
    def __init__(self, red_pin, green_pin, blue_pin):
        self.red = PWM(Pin(red_pin))
        self.green = PWM(Pin(green_pin))
        self.blue = PWM(Pin(blue_pin))
        
        # Настройка частоты и разрешения для PWM
        self.red.freq(1000)
        self.green.freq(1000)
        self.blue.freq(1000)
        # Инициализация цвета в 0 (выключено)
        self.set_color(0, 0, 0)
    
    def set_color(self, red, green, blue):
        self.red.duty(red)
        self.green.duty(green)
        self.blue.duty(blue)
        utime.sleep_ms(1)

    def pulse(self):
        color = (int(bool(self.red.duty())), int(bool(self.green.duty())), int(bool(self.blue.duty())))
        print(color)
        for i in range(1023, 0, -2):
            self.set_color(color[0] * i, color[1] * i, color[2] * i)
            utime.sleep_ms(1)
        for i in range(0, 1024, 2):
            self.set_color(color[0] * i, color[1] * i, color[2] * i)
            utime.sleep_ms(1)
            

# Инициализация RGB светодиода
led = RGB_LED(19, 18, 5)
