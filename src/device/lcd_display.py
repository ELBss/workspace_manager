from machine import Pin, I2C
from lcd_i2c import LCD


SDA_PIN = 21
SCL_PIN = 22


class LCD_Display:
    def __init__(self, scl_pin, sda_pin, rows=4, cols=20):
        self.i2c = I2C(scl=Pin(scl_pin), sda=Pin(sda_pin))
        self.dev_addr = self.find_i2c_device()
        self.lcd = LCD(addr=self.dev_addr, cols=cols, rows=rows, i2c=self.i2c)
        self.rows = rows
        self.cols = cols
        self.lcd.begin()

    def find_i2c_device(self):
        devices = self.i2c.scan()
        if len(devices) == 0:
            print("No I2C device!")
        else:
            print('I2C devices found:',len(devices))
            for device in devices:
                print("At address: ",hex(device))
            return devices[0]

    def clear(self):
        self.lcd.clear()
        self.lcd.home()

    def set_cursor(self, row, col):
        self.lcd.set_cursor(row, col)

    def backlight(self, state):
        self.lcd.set_backlight(state)
        
    def print(self, text):
        lines = text.split('\n')
        for i, line in enumerate(lines):
            if i + self.lcd.cursor_position[1] < self.rows:
                self.lcd.print(line)
                if len(lines) > 1 and line != '':
                    self.lcd.cursor_position = (0, self.lcd.cursor_position[1] + 1)
            else:
                self.lcd.clear()
                print("The message is too big!")
                self.print("The message is \ntoo big!")
                break

    def blink(self, state):
        if state:
            self.lcd.blink()
        else:
            self.lcd.no_blink()
            
    def cursor(self, state):
        if state:
            self.lcd.cursor_on()
        else:
            self.lcd.cursor_off()