from machine import Pin, PWM
import utime

RED_PIN = 15
GREEN_PIN = 12
BLUE_PIN = 14

COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_WHITE = (255, 255, 255)


class RGB_LED:
    def __init__(self, red_pin, green_pin, blue_pin, freq=1000, duty_range=4, color_tuple = (255, 255, 255)):
        self.red = PWM(Pin(red_pin), freq=freq, duty=0)
        self.green = PWM(Pin(green_pin), freq=freq, duty=0)
        self.blue = PWM(Pin(blue_pin), freq=freq, duty=0)
        self.duty_range = duty_range
        self.color_tuple = color_tuple
        
    def color_down(self):
        while self.red.duty() != 0 or self.green.duty() != 0 or self.blue.duty() != 0:
            self.red.duty(self.red.duty() - 1)
            self.green.duty(self.green.duty() - 1)
            self.blue.duty(self.blue.duty() - 1)
            
    def color_up(self, color_tuple):
        tmp_red = color_tuple[0] * self.duty_range
        tmp_green = color_tuple[1] * self.duty_range
        tmp_blue = color_tuple[2] * self.duty_range
        while self.red.duty() != tmp_red or self.green.duty() != tmp_green or self.blue.duty() != tmp_blue:
            if tmp_red != 0 and self.red.duty() != tmp_red:
                self.red.duty(self.red.duty() + 1)
            if tmp_green != 0 and self.green.duty() != tmp_green:
                self.green.duty(self.green.duty() + 1)
            if tmp_blue != 0 and self.blue.duty() != tmp_blue:
                self.blue.duty(self.blue.duty() + 1)


    def set_color(self, color_tuple):
        self.color_tuple = color_tuple
        self.color_down()
        self.color_up(color_tuple)

    def off(self):
        self.red.duty(0)
        self.green.duty(0)
        self.blue.duty(0)

    def on(self):
        self.red.duty(self.red.duty())
        self.green.duty(self.green.duty())
        self.blue.duty(self.blue.duty())

    def pulse(self, count):
        for i in range(count):
            self.set_color(self.color_tuple)

rgb_led = RGB_LED(RED_PIN, GREEN_PIN, BLUE_PIN)

rgb_led.set_color(COLOR_RED)

rgb_led.pulse(1)
rgb_led.set_color(COLOR_BLUE)