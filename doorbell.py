import RPi.GPIO as GPIO
import os
import smtplib
from time import sleep

# config


# Use sms gateway provided by mobile carrier:
# at&t:     number@mms.att.net
# t-mobile: number@tmomail.net
# verizon:  number@vtext.com
# sprint:   number@page.nextel.com

# Establish a secure session with gmail's outgoing SMTP server using your gmail account
server = smtplib.SMTP( smtp_server, smtp_port )

server.starttls()

server.login( send_address, send_password )

GPIO.setmode(GPIO.BCM)

GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)

server.sendmail( send_address, email_addresses[0], 'Door bell alerts up' )

while True:
	if GPIO.input(channel):
		sleep(0.1)
	else:
		print('Input was LOW')
		os.system('mpg123 ' + door_bell_sound)
		# Send text message through SMS gateway of destination number
		try:
			server.sendmail( send_address, email_addresses[0], 'Ding Dong' )
			server.sendmail( send_address, email_addresses[1], 'Ding Dong' )
		except:
			continue

server.sendmail( send_address, email_addresses[0], 'Door bell alerts down.' )

GPIO.cleanup()
