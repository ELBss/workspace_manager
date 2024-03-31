# demo version

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


def do_connect():
    "Подключение к Wi-Fi"
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

# ESP32 нуждается в периодической синхронизации RTC
def time_sync():
    "Синхронизация RTC устройства с ntp сервером"
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
    "Проверка доступа к серверу"
    try:
        response = urequests.get('https://workspace-manager.onrender.com/reservations') # Хорошо бы передавать адрес аргументом. Но не сегодня. 
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



def main():
    
    net = do_connect()
    if net.isconnected():
        led.pulse()
        time_sync()
        if check_server_access():
            print("Устройство успешно подключено к серверу.")
            sensor.observation_cycle()
#             здесь должен быть основной рабочий цикл устройства, включающий в себя:
#             обновление информации о бронированиях комнаты на ближайшее время
#             периодическая синхронизация внутренних часов микроконтроллера функцией time_sync()
#             в случае периода бронирования мониторинг показаний датчика sensor.observation_cycle()
#             отправка на сервер сигнало о превышении лимита времени пользователем
#             или в случае незарегестрированного нахождения в комнате
        else:
            print("Устройство не подключено к серверу.")
            led.set_color(1023, 0, 0)
            lcd.clear()
            lcd.print("Please contact\nSupport")

# инициализация подключенных устройсв
led = RGB_LED(RED_PIN, GREEN_PIN, BLUE_PIN)
lcd = LCD_Display(scl_pin=SCL_PIN, sda_pin=SDA_PIN)
sensor = PIR_Sensor(SENSOR_PIN)
rtc = RTC()

main()
