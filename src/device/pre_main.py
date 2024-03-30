# pre-main base programm

from network import WLAN, STA_IF, hostname
from machine import RTC

from lcd_display import *
from rgb_led import *


import ntptime

TIMEZONE = 7
WIFI_SSID = 'SM-G960U'
WIFI_PASSWORD = 'House Always Wins'

led = RGB_LED(RED_PIN, GREEN_PIN, BLUE_PIN, color_tuple=COLOR_BLUE)
lcd = LCD_Display(scl_pin=SCL_PIN, sda_pin=SDA_PIN)
rtc = RTC()


def do_connect():
    sta_if = WLAN(STA_IF)
    if not sta_if.isconnected():
        print('Connecting to network...')
        lcd.print('Connecting to WI-FI')
        lcd.cursor(True)
        sta_if.active(True)
        led.pulse()
        sta_if.connect(WIFI_SSID, WIFI_PASSWORD)
        i = 0
        while not sta_if.isconnected() and i < 20:
            led.pulse()
            i += 1
    if sta_if.isconnected():
        led.set_color(COLOR_GREEN)
        print(f"Connect to {WIFI_SSID}")
        lcd.clear()
        lcd.print(f"Connect to {WIFI_SSID}\nHostname:{hostname()}IP:{sta_if.ifconfig()[0]}")
        print(sta_if.ifconfig())
        return sta_if
    else:
        led.set_color(COLOR_RED)
        print("Can't connect!")
        lcd.set_cursor(0, 1)
        lcd.print("Can't connect!")
        print('network config:', sta_if.ifconfig())
        return None
        
def time_sync():
    print("First time:", rtc.datetime())
    try:
        ntptime.settime()
    except OSError:
        led.set_color(COLOR_RED)
        lcd.clear()
        lcd.print("Time synchronization\nerror!")
    else:
        new_dt = list(rtc.datetime())
        print("Sync time", rtc.datetime())
        new_dt[4] += TIMEZONE
        rtc.datetime(new_dt)
        print("NSK time:", rtc.datetime())
        
net = do_connect()

led.pulse(20)

time_sync()

