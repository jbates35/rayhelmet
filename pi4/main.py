#!/usr/bin/python3

from threading import Thread
import sys
import signal
import pvrhino
from pvrecorder import PvRecorder
import pigpio

### COMMANDS FROM PI ###
jarvisidle_word = b'S 0 0 0'
jarvisactive_word = b'S 0 0 1'
helmetopen_word = b'S 0 1 0'
helmetclose_word = b'S 0 1 1'
sparker_word = b'S 0 2 0'
shutdown_word = b'S 0 3 0'
startup_word = b'S 0 3 1'
servos_open = b'S 0 4 0'
servos_close = b'S 0 4 1'

#Pi object for GPIO pins
pi = pigpio.pi()

#Rhino object that uses picovoice to send commands
rhino = pvrhino.create(
    access_key='nTlHPkxlJmGMB0KVeQy4RIrvEwHyrvmZaRrzJshJFdnTUUWwUifCvQ==',
    context_path='/home/pi/Desktop/rayhelmetctrl/Suit_en_raspberry-pi_v2_0_0.rhn',
    sensitivity=0.5
    )

#Run this script on exit - need to delete rhino pv object
def exitscript(sig, frame):
    print("Shutting down...")
    rhino.delete()
    sys.exit(0)

if not pi.connected:
    print("Error: Pi cannot connect")
    rhino.delete()
    sys.exit(0)

signal.signal(signal.SIGINT, exitscript)

#Script that reads the recorder, and interprets commands
def rhino_run():
    def get_next_audio_frame():
        return recorder.read()

    while True:
        is_finalized = rhino.process(get_next_audio_frame())

        #If commands are found, send messages through Serial to coordinate with esp32/pico
        if is_finalized:
            inference = rhino.get_inference()
            if inference.is_understood:
                intent = inference.intent
                slots = inference.slots
                if intent == 'helmet':
                    if slots['helmet'] == 'open':
                        print('Opening Helmet')
                        pi.serial_write(uart_port_1, helmetopen_word)
                    elif slots['helmet'] == 'close':
                        print('Closing Helmet')
                        pi.serial_write(uart_port_1, helmetclose_word)

                elif intent == 'shock':
                    if slots['shock'] == 'on':
                        print('Shocker ON')
                        pi.serial_write(uart_port_1, sparker_word)

                elif intent == 'system':
                    if slots['action'] == 'shutdown':
                        print('Shut System Down')
                        pi.serial_write(uart_port_1, shutdown_word)
                    elif slots['action'] == 'start':
                        print('Start System')
                        pi.serial_write(uart_port_1, startup_word)

if __name__ == "__main__":
    uart_port_1 = pi.serial_open("/dev/serial0", 115200)

    recorder = PvRecorder(device_index=0, frame_length=512)
    recorder.start()

    rhino_thread = Thread(target=rhino_run)
    rhino_thread.start()

    signal.signal(signal.SIGINT, exitscript)
    signal.pause()

