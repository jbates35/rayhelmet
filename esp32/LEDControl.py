import time


class LEDControl:
    
    count = 0
    
    PATTERN_MAX = 5
    DIM_MAX = 4
    SPEED_MAX = 2

    LED_MAX = 255

    COLOR_VALS = [
        [1, 1, 1],      # white
        [1, 0, 0],      # red
        [1, 0.5, 0],    # orange
        [1, 1, 0],      # yellow
        [0.5, 1, 0],    # lime
        [0, 1, 0],      # green
        [0, 1, 0.5],    # jade
        [0, 1, 1],      # teal
        [0, 0.5, 1],    # azure
        [0, 0, 1],      # blue
        [0.5, 0, 1],    # violet
        [1, 0, 1],      # purple
        [1, 0, 0.5],    # pink
    ]

    RED = 0
    GRN = 1
    BLU = 2

    def __init__(self):
        self.pattern = 0
        self.speed = 0
        self.color = 0
        self.dim = 0
        self.led = [0, 0, 0]
        self.ledout = (0, 0, 0)
        self.dir = [0, 0, 0]
        self.speedint = [40, 20, 10]
        self.colorvals = []
        self.switch_flag = False
        self.changeclr_flag = False
        self.COLOR_MAX = 0

    ############################# RUN SCRIPT ##########################
    def run(self):
        if self.pattern == 0: self.off()
        elif self.pattern == 1: self.solid()
        elif self.pattern == 2: self.fade(1) # fade up
        elif self.pattern == 3: self.fade(0) # fade down
        elif self.pattern == 4: self.fadex()
        elif self.pattern == 5: self.breathe()

    ############################# LED CONTROL #########################
    def off(self):
        if self.switch_flag == True:
            self.led = [0, 0, 0]
            self.ledout = (0, 0, 0)
            self.switch_flag = False

    # Fades in one direction only
    def fade(self, _dir):
        #Initial values
        if self.switch_flag == True:
            self.led = [0, 0, 0]
            self.color = 0
            self.colorvals = LEDControl.COLOR_VALS
            self.COLOR_MAX = len(self.colorvals)-1
            self.switch_flag = False
        #If color is changed
        if self.changeclr_flag == True:
            self.led = [0, 0, 0]
            self.changeclr_flag = False
        #Thread that runs
        for i in range(len(self.led)):
            if _dir == 1:
                self.led[i] = 0 if self.led[i] >= LEDControl.LED_MAX else self.led[i] + 1
            else:
                self.led[i] = LEDControl.LED_MAX if self.led[i] <= 0 else self.led[i] - 1
        self.ledout = tuple(int(x * y * (self.dim+5) / (self.DIM_MAX+5)) for x, y in zip(self.led, self.colorvals[self.color]))

    # Fades in both directions
    def fadex(self):
        # Initial values
        if self.switch_flag == True:
            self.led = [0, 0, 0]
            self.color = 0
            self.dir = [1, 1, 1]
            self.colorvals = LEDControl.COLOR_VALS
            self.COLOR_MAX = len(self.colorvals)-1
            self.switch_flag = False
        #If color is changed
        if self.changeclr_flag == True:
            self.led = [0, 0, 0]
            self.dir = [1, 1, 1]
            self.changeclr_flag = False
        #Thread that runs
        for i in range(len(self.led)):
            self.led[i] = self.led[i] + 1 if self.dir[i] == 1 else self.led[i] - 1
            if self.led[i] == self.LED_MAX:
                self.dir[i] = 0
            if self.led[i] == 0:
                self.dir[i] = 1
        self.ledout = tuple(int(x * y * (self.dim+5) / (self.DIM_MAX+5)) for x, y in zip(self.led, self.colorvals[self.color]))

    def solid(self):
        # Initial values
        if self.switch_flag == True:
            self.led = [255, 255, 255]
            self.colorvals = LEDControl.COLOR_VALS
            self.COLOR_MAX = len(self.colorvals)-1
            self.switch_flag = False
        #If color is changed
        if self.changeclr_flag == True:
            self.changeclr_flag = False
        self.ledout = tuple(int(x * y * (self.dim+5) / (self.DIM_MAX+5)) for x, y in zip(self.led, self.colorvals[self.color]))

    def breathe(self):
        #initial
        if self.switch_flag == True:
            self.led = [128, 0, 128]
            self.color = 0
            self.COLOR_MAX = 0
            self.dir = [1, 1, 0]
            self.switch_flag = False
        #Thread that runs
        for i in range(len(self.led)):
            self.led[i] = self.led[i] + 1 if self.dir[i] == 1 else self.led[i] - 1
            if self.led[i] >= self.LED_MAX * 3 / 2:
                self.dir[i] = 0
            if self.led[i] <= 0:
                self.dir[i] = 1
        self.ledouttemp = list(int(x-128) for x in self.led)
        self.ledouttemp = list(map(lambda x: x if x >= 0 else 0, self.ledouttemp))
        self.ledout = tuple(self.ledouttemp)
        
        
    ########### CONTROL FUNCTIONS ###########
    def changepattern_n(self, _val):
        self.pattern = _val
        self.switch_flag = True
    
    def changespeed_n(self, _val):
        self.speed = _val
    
    def changedim_n(self, _val):
        self.dim = _val
                
    def changecolor_n(self, _val):
        self.color = _val
        self.changeclr_flag = True

    ########### HELPER FUNCTIONS ###########
    # Function that converts 0-100 to 0-65536 for use from PWM
    def pwmconvert(self, x):
        return int(x * 65536 * self.dim / (LEDControl.LED_MAX*40))
