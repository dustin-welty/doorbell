import RPi.GPIO as GPIO
import os
import smtplib
from time import sleep
import configparser
from pathlib import Path
import simpleaudio as sa
import datetime
import time


# config
config_parse = configparser.RawConfigParser()
configFilePath = 'config.txt'
config_parse.read(configFilePath)

channel = int(config_parse.get('door_bell_config', 'channel'))
email_address1 = config_parse.get('door_bell_config', 'email_address1')
email_address2 = config_parse.get('door_bell_config', 'email_address2')
smtp_server = config_parse.get('door_bell_config', 'smtp_server')
smtp_port = int(config_parse.get('door_bell_config', 'smtp_port'))
send_address = config_parse.get('door_bell_config', 'send_address')
send_password = config_parse.get('door_bell_config', 'send_password')
door_bell_sound = config_parse.get('door_bell_config', 'door_bell_sound')


def dingdong(ch):
    if ch == channel:
        st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %Hh%Mm%Ss')
        message = 'Ding Done ' + st
        print(message)
        play_obj = wave_obj.play()
        # Send text message through SMS gateway of destination number
        try:
            server.sendmail(send_address, email_address1 + ';' + email_address2, message)
        except:
            print('txt error')
        play_obj.wait_done()


# Use sms gateway provided by mobile carrier:
# at&t:     number@mms.att.net
# t-mobile: number@tmomail.net
# verizon:  number@vtext.com
# sprint:   number@page.nextel.com

# Establish a secure session with gmail's outgoing SMTP server using your gmail account
server = smtplib.SMTP(smtp_server, smtp_port)
server.starttls()
server.login(send_address, send_password)
time_stamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %Hh%Mm%Ss')
message = 'Door bell alerts up ' + time_stamp
print(message)
server.sendmail(send_address, email_address1, message)

wave_obj = sa.WaveObject.from_wave_file(door_bell_sound)

GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(channel, GPIO.FALLING, callback=dingdong, bouncetime=200)

my_file = Path("stop_loop")

while not my_file.exists():
    sleep(0.1)

time_stamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %Hh%Mm%Ss')
message = 'Door bell alerts down ' + time_stamp
print(message)
try:
    server.sendmail(send_address, email_address1, message)
except:
    pass

try:
    server.quit()
except:
    pass
GPIO.cleanup()
