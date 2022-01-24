# Rayhelmet
## Ramon's helmet project 

This project is a voice activated helmet, video can be found [here](https://www.youtube.com/watch?v=Rqv2LhUGKxs)

This is a group project between Tom Kuzma, Ramon Vicencio, and myself. The three folders are for the script on the Raspberry Pi 4 and the 2 microcontrollers to drive the devices, ESP32 for the LEDs and Pi Pico for the servos.

The RPi4 takes care of the microphone processing and voice activation script. It uses a picovoice module which was then incorporated with a rhino object. It then uses UART to talk to the ESP32 which then defers more tasks to the Pico.

There are two servos that are controlled by the Pico. And a main 12V LED strip at the front that is controlled by the ESP32.
