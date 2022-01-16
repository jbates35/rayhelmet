import machine
import time
import LEDControl

### DEFINITIONS ###
LED_R_PIN = 17
LED_G_PIN = 18
LED_B_PIN = 19
EYELIGHTS_PIN = 21
SHOCKER_PIN = 5
SHOCKER_HOLDTIME = 1500

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

#Eye lights
eyelights = machine.Pin(EYELIGHTS_PIN, machine.Pin.OUT)
eyelights.value(0)

#Shocker
shocker_flag = False

shocker = machine.Pin(SHOCKER_PIN, machine.Pin.OUT)
shocker.value(0)

timer1 = machine.Timer(0)

def shocker_on():
    shocker.value(1)
    timer1.init(period=SHOCKER_HOLDTIME, mode=machine.Timer.ONE_SHOT, callback=lambda t: shocker.value(0))
    
#LEDs
LEDs = LEDControl.LEDControl()
rgb_vals = [ 0, 400, 800 ] 

red = machine.PWM(machine.Pin(LED_R_PIN))
red.freq(1000)

green = machine.PWM(machine.Pin(LED_G_PIN))
green.freq(1000)

blue = machine.PWM(machine.Pin(LED_B_PIN))
blue.freq(1000)

rgb = [ red , green , blue ]

def LEDsActive():
    global LEDs
    #Purple solid light
    LEDs.changepattern_n(1)
    LEDs.changedim_n(4)
    LEDs.changecolor_n(2)

def LEDsIdle():
    global LEDs
    #Breathing light pattern
    LEDs.changecolor_n(1)
    LEDs.changepattern_n(5)
    LEDs.changedim_n(4)

def LEDsOff():
    global LEDs
    #LEDs off
    LEDs.changepattern_n(0)
    
LEDsOff()

#LEDS timer
def timer2irq(timer):
    global LEDs
    global rgb
    LEDs.run()
    for i in range(len(rgb)):
        rgb[i].duty(LEDs.ledout[i]*4)
    
timer2 = machine.Timer(1)
timer2.init(freq=100, mode=machine.Timer.PERIODIC, callback=timer2irq)

#Flash timer - may be inefficient, revisit later
flash_flag = False
flash_timer = 0

def LEDFlash(timer):
    global flash_flag
    global flash_timer
    
    if flash_flag:
        flash_timer = flash_timer + 1
    else:
        flash_timer = 0
        
    if flash_timer == 1:
        LEDsActive()
    elif flash_timer == 401:
        LEDsOff()
    elif flash_timer == 801:
        LEDsActive()
    elif flash_timer == 1201:
        LEDsOff()
    elif flash_timer == 1601:
        LEDsActive()
    elif flash_timer == 2001:
        LEDsOff()
    elif flash_timer == 2401:
        LEDsIdle()
        flash_flag = 0
        flash_timer = 0

timer4 = machine.Timer(3)
timer4.init(freq=1000, mode=machine.Timer.PERIODIC, callback=LEDFlash)        
        
#UART
uart0 = machine.UART(1, baudrate=115200, tx=33, rx=32)
uart1 = machine.UART(2, baudrate=115200, tx=22, rx=23)

#Overall routines go here!!
#These are the functions that UART uses to drive the devices
def helmetopen():
    global flash_flag
    print("Helmet Open")
    flash_flag = True
    uart1.write(servos_open)
    eyelights.value(0)

def helmetclose():
    global flash_flag
    print("Helmet Close")
    flash_flag = True
    uart1.write(servos_close)
    eyelights.value(1)

def sparker():
    print("Sparker")
    LEDsIdle()
    shocker_on()

def shutdown():
    print("Shutdown")
    LEDsOff()
    uart1.write(servos_close)
    eyelights.value(0)

def startup():
    print("Startup")
    LEDsIdle()
    uart1.write(servos_close)
    eyelights.value(1)

#UART TIMER
def timer3irq(timer):
    rxData = bytes()
    if uart0.any() > 0:
        while uart0.any() > 0:
            rxData += uart0.read(1)
        if rxData == helmetopen_word: helmetopen()
        elif rxData == helmetclose_word: helmetclose()
        elif rxData == sparker_word: sparker()
        elif rxData == shutdown_word: shutdown()
        elif rxData == startup_word: startup()
        else: print("Error: Command not recognized.")
                
timer3 = machine.Timer(2)
timer3.init(freq=50, mode=machine.Timer.PERIODIC, callback=timer3irq)