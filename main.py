import streams
import json
import requests
import mcu
import pwm

from wireless import wifi
from espressif.esp32net import esp32wifi as wifi_driver

from riverdi.displays.bt81x import ctp50
from bridgetek.bt81x import bt81x

from okdo.iot import iot
from okdo.iot import mqtt_client

import gui

# image resources
new_resource('images/gui_riverdi_logo.png')

# wifi credentials
ssid = "xx"                      # this is the SSID of the WiFi network
wifiPWD = "xx"               # this is the Password for WiFi

# okdo cloud
device_id = ""                          # this is the device identifier. Can be obtained from the OKDO cloud dashboard
device_token = ""  # this is the device token. Can be obtained from the OKDO cloud dashboard

# RPi statistics
cpu_load_cur = 0
cpu_temp_main = 0
mem_info_free = 0
mem_swap_free = 0

# RPi processes
rpi_top_proc_1 = "-|-|-"
rpi_top_proc_2 = "-|-|-"
rpi_top_proc_3 = "-|-|-"
rpi_top_proc_4 = "-|-|-"

# RPi sensors
rpi_temp_1 = 0
rpi_temp_2 = 0
rpi_temp_3 = 0
rpi_temp_4 = 0

# screen layouts/stages:
# 1 - mainmenu - sensors
# 2 - mainmenu - statistics
# 3 - mainmenu - processes

 # open serial channel to display debug messages
streams.serial()

# pwm buzzer
pinMode(D23.PWM,OUTPUT)

# short beep
def beep():
    pwm.write(D23.PWM,1000,1000//2,MICROS)
    sleep(50)
    pwm.write(D23.PWM,0,0)

# okDO handlers
def okdo_cb(asset,value, previous_value):
    
    global cpu_load_cur
    global cpu_temp_main
    global mem_info_free
    global mem_swap_free
    
    global rpi_top_proc_1
    global rpi_top_proc_2
    global rpi_top_proc_3
    global rpi_top_proc_4
    
    global rpi_temp_1
    global rpi_temp_2
    global rpi_temp_3
    global rpi_temp_4
    
    if (asset == 'rpi_cpu_load_cur'):
        cpu_load_cur = value
    elif (asset == 'rpi_cpu_temp_main'):
        cpu_temp_main = value
    elif (asset == 'rpi_mem_info_free'):
        mem_info_free = value
    elif (asset == 'rpi_mem_swap_free'):
        mem_swap_free = value
    elif (asset == 'rpi_top_proc_1'):
        rpi_top_proc_1 = value
    elif (asset == 'rpi_top_proc_2'):
        rpi_top_proc_2 = value
    elif (asset == 'rpi_top_proc_3'):
        rpi_top_proc_3 = value
    elif (asset == 'rpi_top_proc_4'):
        rpi_top_proc_4 = value
    elif (asset == 'rpi_temp_1'):
        rpi_temp_1 = value
    elif (asset == 'rpi_temp_2'):
        rpi_temp_2 = value
    elif (asset == 'rpi_temp_3'):
        rpi_temp_3 = value
    elif (asset == 'rpi_temp_4'):
        rpi_temp_4 = value

# buttons handler
def pressed(tag, tracked, tp):
    
    global screenLayout

    if ((tag > 0) and (tag < 3)):
        screenLayout = tag

# init display
bt81x.init(SPI0, D4, D33, D34)

# one callback for all tags
bt81x.touch_loop(((-1, pressed), ))

# [0] show logo
gui.loadImage('gui_riverdi_logo.png')
gui.showLogo()
sleep(4000)

# [1] show spinner - connecting with predefined WiFi network
gui.showSpinner("Connecting with predefined WiFi network...")

# [2] init wifi driver
wifi_driver.auto_init()

# [3] connect to predefined wifi network
for _ in range(0,5):
    try:
        wifi.link(ssid,wifi.WIFI_WPA2,wifiPWD)
        break
    except:
        gui.showSpinner("Trying to reconnect...")
else:
    gui.showSpinner("Connection Error - restarting...")
    mcu.reset()

# [4] connect and setup connection with OKdo cloud
device = iot.Device(device_id,device_token,mqtt_client.MqttClient) 
device.connect()

# [5] define the callbacks to call when an OKdo asset command is received

device.watch_command("rpi_mem_swap_free", okdo_cb)
device.watch_command("rpi_mem_info_free", okdo_cb)
device.watch_command("rpi_cpu_temp_main", okdo_cb)
device.watch_command("rpi_cpu_load_cur", okdo_cb)

device.watch_command("rpi_top_proc_1", okdo_cb)
device.watch_command("rpi_top_proc_2", okdo_cb)
device.watch_command("rpi_top_proc_3", okdo_cb)
device.watch_command("rpi_top_proc_4", okdo_cb)

device.watch_command("rpi_temp_1", okdo_cb)
device.watch_command("rpi_temp_2", okdo_cb)
device.watch_command("rpi_temp_3", okdo_cb)
device.watch_command("rpi_temp_4", okdo_cb)

device.run()

# [6] mainloop
screenLayout = 1

while True:

    if (screenLayout == 1):
        gui.showSensorsScreen(rpi_temp_1, rpi_temp_2, rpi_temp_3, rpi_temp_4)
    elif (screenLayout == 2):
        gui.showStatisticsScreen(cpu_load_cur, cpu_temp_main, mem_info_free, mem_swap_free)
    elif (screenLayout == 3):
        gui.showProcessMonitor(rpi_top_proc_1,rpi_top_proc_2,rpi_top_proc_3,rpi_top_proc_4)
    
    sleep(10)
