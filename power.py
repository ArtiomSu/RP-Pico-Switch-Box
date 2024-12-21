import time

class Power:
    def __init__(self, hardware):
        self.hardware = hardware
        self.order = [1,3,2,0]
        self.current_order = []
        self.frames_count = 0
        self.input_correct = False

    def check(self):
        self.hardware.enableSwitchInput()
        self.hardware.printLogo()
        switch_outs = self.hardware.getSwitchesOutput()
        #print("Switch outputs:", switch_outs)

        any_true = False
        # Iterate through the switches and check their state
        for i, switch_state in enumerate(switch_outs):
            if switch_state and i not in self.current_order:
                self.current_order.append(i)
            if switch_state:
                any_true = True

        if not any_true:
            self.current_order = []

        # Compare current order to expected order
        if self.current_order == self.order:
            #print("Order is correct! All switches activated in the right sequence.")
            self.input_correct = True
            self.hardware.powerOnAnimation()
            self.hardware.power_pc(True)
            time.sleep(2)
            self.hardware.turnOffAllLeds()
            self.hardware.display.clear()
            self.current_order = []
        # elif all(i in self.current_order for i in self.order):
        #     print("Order in progress. Current sequence:", self.current_order)
        # else:
        #     print("Sequence mismatch or incomplete. Current sequence:", self.current_order)

    def reset(self):
        self.current_order = []
        self.input_correct = False
        self.frames_count = 0
        self.hardware.turnOffAllLeds()
        self.hardware.display.clear()
        
    def run_next_check(self):
        if not self.input_correct:
            self.check()
            time.sleep(0.5)
        else:
            if self.hardware.deadState(self.frames_count):
                self.frames_count = -1
                self.input_correct = False
            time.sleep(1)

        self.frames_count += 1