import RPi.GPIO as GPIO
import os
import smtplib
from time import sleep
import configparser


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

# Use sms gateway provided by mobile carrier:
# at&t:     number@mms.att.net
# t-mobile: number@tmomail.net
# verizon:  number@vtext.com
# sprint:   number@page.nextel.com

# Establish a secure session with gmail's outgoing SMTP server using your gmail account
server = smtplib.SMTP(smtp_server, smtp_port)

server.starttls()

server.login(send_address, send_password)

GPIO.setmode(GPIO.BCM)

GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)

server.sendmail(send_address, email_address1, 'Door bell alerts up')

while True:
    if GPIO.input(channel):
        sleep(0.1)
    else:
        print('Input was LOW')
        os.system('mpg123 ' + door_bell_sound)
        # Send text message through SMS gateway of destination number
        try:
            server.sendmail(send_address, email_address1, 'Ding Dong')
            server.sendmail(send_address, email_address2, 'Ding Dong')
        except:
            print('txt error')
            continue

server.sendmail(send_address, email_address1, 'Door bell alerts down.')

# GPIO.cleanup()
