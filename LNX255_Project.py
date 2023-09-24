#!/usr/bin/python3

# Author:  M. Heidenreich
# Adapted by: Tuan Lam Nguyen, 08-10-2023

from signal import signal, SIGTERM, SIGHUP, pause
from gpiozero import PWMLED, Button
from threading import Thread
from time import sleep
from random import randrange
from rpi_lcd import LCD
from smbus import SMBus
from math import log10


patterns = [
                [1, 0, 0, 0, 0, 0],
                [1, 1, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0],
                [1, 1, 1, 1, 0, 0],
                [1, 1, 1, 1, 1, 0],
                [1, 0, 1, 0, 1, 0]
            ]

leds = [PWMLED(13), PWMLED(19), PWMLED(26), PWMLED(20), PWMLED(16), PWMLED(12)]
button = Button(21)
lcd = LCD()
bus = SMBus(1)
ads7830_commands = (0x84, 0xc4, 0x94, 0xd4, 0xa4, 0xe4, 0xb4, 0xf4)

is_running = True
delay = 0.1
steps = 255
fade_factor = (steps * log10(2))/(log10(steps))
index = 0
led_in = 5
led_out = 0
bright_port = 0
spd_port = 1


def safe_exit(signum, frame):
    exit(1)


def read_ads7830(input):
    bus.write_byte(0x4b, ads7830_commands[input])
    return bus.read_byte(0x4b)


def show_pattern():
    while is_running:
        bright = (pow(2, (read_ads7830(bright_port)/fade_factor))-1)/steps
        for id in range(6):
            leds[id].value = patterns[index][id] * bright
        speed = read_ads7830(spd_port) / 255.0
        token = patterns[index].pop(led_out)
        patterns[index].insert(led_in, token)

        sleep(delay*speed)


def change_direction():
    global led_in, led_out, index

    led_in, led_out = led_out, led_in

    while True:
        new_index = randrange(0, len(patterns))

        if new_index != index:
            index = new_index
            break


def lcd_display():
    while is_running:
        lcd.text(f"Pattern: {index+1}/6. {'>>' if led_in == 5 else '<<'}", 1)
        lcd.text(f"B:{(read_ads7830(bright_port) / 255.0)*100:.1f}%,"
                 f"S:{delay* (read_ads7830(spd_port) / 255.0):.2f}s", 2)
        sleep(delay)


try:
    signal(SIGTERM, safe_exit)
    signal(SIGHUP, safe_exit)

    button.when_pressed = change_direction
    index = randrange(0, len(patterns))
    worker = Thread(target=show_pattern, daemon=True)
    screen = Thread(target=lcd_display, daemon=True)
    worker.start()
    screen.start()

    pause()

except KeyboardInterrupt:
    pass

finally:
    is_running = False
    worker.join()
    screen.join()
    lcd.clear()

    for id in range(6):
        leds[id].close()
