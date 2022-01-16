import machine
import time
import LEDControl

### DEFINITIONS ###
SERVO_1_PIN = 16
SERVO_2_PIN = 17

SERVO_IDLE = 0
SERVO_OPEN = 1
SERVO_CLOSE = 2

SERVO_1_MAX = 170
SERVO_1_MIN = 10
SERVO_2_MAX = 90
SERVO_2_MIN = 30
SERVO_TIMER_FREQ = 90

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

led = machine.Pin(25, machine.Pin.OUT)
led.value(1)

#SERVO
def setServo(servo, servo_pos):
    pwm_pos = (6500 * servo_pos)/180 + 1000
    servo.duty_u16(int(pwm_pos))
    
servos = [ machine.PWM(machine.Pin(SERVO_1_PIN)), machine.PWM(machine.Pin(SERVO_2_PIN)) ]
servos_max = [ SERVO_1_MAX, SERVO_2_MAX ]
servos_min = [ SERVO_1_MIN, SERVO_2_MIN ]
servos_val = servos_min.copy()
servos_flag = [ SERVO_IDLE, SERVO_IDLE ]

for i in range(len(servos)):
    servos[i].freq(50)
    setServo(servos[i], servos_val[i])

def servo1open():
    servos_flag[0] = SERVO_OPEN
    
def servo1close():
    servos_flag[0] = SERVO_CLOSE
    
def servo2open():
    servos_flag[1] = SERVO_OPEN

def servo2close():
    servos_flag[1] = SERVO_CLOSE

#SERVO UPDATE SCRIPT
def servorun(i):
    if servos_flag[i] == SERVO_OPEN:
        if servos_val[i] < servos_max[i]:
            servos_val[i] = servos_val[i] + 1
        else:
            servos_val[i] = servos_max[i]
            servos_flag[i] = SERVO_IDLE
        setServo(servos[i], servos_val[i])
    elif servos_flag[i] == SERVO_CLOSE:
        if servos_val[i] > servos_min[i]:
            servos_val[i] = servos_val[i] - 1
        else:
            servos_val[i] = servos_min[i]
            servos_flag[i] = SERVO_IDLE
        setServo(servos[i], servos_val[i])
        
#SERVO TIMER
def timer1irq(timer):
    servorun(0)
    servorun(1)

timer1 = machine.Timer()
timer1.init(freq=SERVO_TIMER_FREQ, mode=machine.Timer.PERIODIC, callback=timer1irq)

#COMMAND FUNCTIONS
def helmetopen():
    print("Helmet Open")
    servo1open()
    servo2open()

def helmetclose():
    print("Helmet Close")
    servo1close()
    servo2close()

# #UART
uart0 = machine.UART(0, baudrate=115200, tx=machine.Pin(0), rx=machine.Pin(1))

#UART TIMER
def timer2irq(timer):
    rxData = bytes()
    if uart0.any() > 0:
        while uart0.any() > 0:
            rxData += uart0.read(1)
        if rxData == servos_open: helmetopen()
        elif rxData == servos_close: helmetclose()
        else: print("Error: Command not recognized.")
                
timer2 = machine.Timer()
timer2.init(freq=50, mode=machine.Timer.PERIODIC, callback=timer2irq)

