import math

class PWM_value():
    def __init__(self, max_value, direction):
        self.value = 0
        self.scaled_value = 0
        self.center_value = 307
        self.direction = direction
        self._max = max_value
        self._min = -max_value

    def clean(self):
        if self.value > 100:
            self.value = 100
        if self.value < -100:
            self.value = -100
    
    def cleanForward(self):
        if self.value > 100:
            self.value = 100
        if self.value < 0:
            self.value = 0

    def prep_for_send(self, value, forward):
        self.value = value
        if forward:
            self.cleanForward()
        else: 
            self.clean()
        
        self.scaled_value = math.floor((self.value * self._max)/100) * self.direction + self.center_value
        
