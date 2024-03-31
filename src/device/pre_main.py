# pre-main base programm

from network import WLAN, STA_IF, hostname
from machine import RTC, Pin

from lcd_display import *
from rgb_led import *
from pir_sensor import *

import ntptime
import urequests


TIMEZONE = 7
WIFI_SSID = 'SM-G960U'
WIFI_PASSWORD = 'House Always Wins'

led = RGB_LED(RED_PIN, GREEN_PIN, BLUE_PIN)
lcd = LCD_Display(scl_pin=SCL_PIN, sda_pin=SDA_PIN)
sensor = PIR_Sensor(SENSOR_PIN)
rtc = RTC()


def do_connect():
    sta_if = WLAN(STA_IF)
    if not sta_if.isconnected():
        print('Connecting to network...')
        lcd.print('Connecting to WI-FI')
        lcd.cursor(True)
        sta_if.active(True)
        led.set_color(0, 0, 1023)
        sta_if.connect(WIFI_SSID, WIFI_PASSWORD)
        i = 0
        while not sta_if.isconnected() and i < 20:
            led.pulse()
            i += 1
    if sta_if.isconnected():
        led.set_color(0, 1023, 0)
        print(f"Connect to {WIFI_SSID}")
        lcd.clear()
        lcd.print(f"Connect to {WIFI_SSID}\nHostname:{hostname()}")
        lcd.set_cursor(0, 2)
        lcd.print(f"IP:{sta_if.ifconfig()[0]}")
        print(sta_if.ifconfig())
        return sta_if
    else:
        led.set_color(1023, 0, 0)
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
        led.set_color(1023, 0, 0)
        lcd.clear()
        lcd.print("Time synchronization\nerror!")
    else:
        new_dt = list(rtc.datetime())
        print("Sync time", rtc.datetime())
        new_dt[4] += TIMEZONE
        rtc.datetime(new_dt)
        print("NSK time:", rtc.datetime())
        
def check_server_access():
    try:
        response = urequests.get('https://workspace-manager.onrender.com/reservations')
        if response.status_code == 200:
            print("Доступ к серверу есть.")
            return True
        else:
            print("Ошибка при проверке доступа в интернет. Статус ответа:", response.status_code)
            return False
    except Exception as e:
        print("Ошибка при отправке запроса:", e)
        return False
    finally:
        lcd.clear()
        lcd.print(f"Server response: {response.status_code}")
        if 'response' in locals() or 'response' in globals():
            response.close()

        
net = do_connect()

led.pulse()

time_sync()

# if check_server_access():
#     print("Устройство успешно подключено к серверу.")
# else:
#     print("Устройство не подключено к серверу.")



# sensor.observation_cycle()

