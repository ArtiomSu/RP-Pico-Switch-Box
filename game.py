import time
from tools import generate_random_booleans, get_last_output_sum

class Game:
    def __init__(self, hardware):
        self.game_running = True
        self.game_dead_state = 100
        self.game_state = 0
        self.hardware = hardware
        self.update_interval = 100 * 1_000_000  # nanoseconds
        self.last_update_time = time.monotonic_ns()
        self.frames_count = 0
        self.level = 1
        self.level_max = 5
        self.seed = 0
        self.last_output_sum = -1
        self.got_level_seed = False
        self.level_seconds = 0
        self.game_seconds = 0
        self.game_started_time = 0
        self.level_started_time = 0

    def handle_levels(self):
        self.hardware.display.printText(f"Level {self.level}/{self.level_max}", "centre", 0, "centre")
        self.hardware.display.printText(f"{self.level_seconds} Seconds", "bottom", 1, "centre")
        switch_outs = self.hardware.getSwitchesOutput()
        now_output_sum = self.last_output_sum
        level_outs = generate_random_booleans(len(switch_outs), self.seed)

        if not self.got_level_seed:
            while now_output_sum == self.last_output_sum:
                self.seed += 1
                level_outs = generate_random_booleans(len(switch_outs), self.seed)
                if self.level >= self.level_max and not level_outs[len(self.hardware.switchAndLeds) - 1]:
                    now_output_sum = self.last_output_sum
                else:
                    now_output_sum = get_last_output_sum(level_outs)

            self.got_level_seed = True
            self.last_output_sum = now_output_sum

        num_correct = 0
        for i in range(len(switch_outs)):
            normal_led_index_to_use = i if i < 2 else i + 1
            if switch_outs[i] == level_outs[i]:
                num_correct += 1
                self.hardware.normalLeds[normal_led_index_to_use].setLed(True)
            else:
                self.hardware.normalLeds[normal_led_index_to_use].setLed(False)

        if num_correct == len(switch_outs):
            self.game_state += 1

    def reset(self):
        self.game_started_time = 0
        self.level_started_time = 0
        self.game_state = 0

    def run_game_next_state(self):
        current_time = time.monotonic_ns()
        delta_time = current_time - self.last_update_time

        if delta_time >= self.update_interval:
            if self.game_state == 0:
                if self.hardware.startupAnimation(self.frames_count):
                    self.game_state += 1
                    self.hardware.enableSwitchInput()
                    self.game_started_time = time.monotonic_ns()
                    self.level_started_time = time.monotonic_ns()
            elif self.game_state == 1:
                self.level_seconds = (current_time - self.level_started_time) // 1_000_000_000
                self.handle_levels()
            elif self.game_state == 2:
                if self.level >= self.level_max:
                    self.game_seconds = (current_time - self.game_started_time) // 1_000_000_000
                    self.hardware.display.printText("You Won", "centre", 0, "centre")
                    self.hardware.display.printText(f"In {self.game_seconds} Seconds", "bottom", 1, "centre")
                    time.sleep(5)
                    self.level = 1
                    self.got_level_seed = False
                    self.game_state = self.game_dead_state
                    self.hardware.turnOffAllLeds()
                    self.hardware.display.clear()
                else:
                    self.hardware.turnOffAllLeds()
                    self.hardware.normalLeds[2].setLed(True)
                    self.hardware.display.printText(f"Level {self.level} complete", "centre", 0, "centre")
                    self.level += 1
                    self.got_level_seed = False
                    time.sleep(1)
                    self.hardware.normalLeds[2].setLed(False)
                    self.hardware.enableSwitchInput()
                    self.game_state -= 1
                    self.level_started_time = time.monotonic_ns()
            elif self.game_state == self.game_dead_state:
                if self.hardware.deadState(self.frames_count):
                    self.frames_count = -1
                    self.game_state = 0

            self.last_update_time = current_time
            self.frames_count += 1

        if self.game_state == self.game_dead_state:
            time.sleep(1)
        else:
            time.sleep(0.001)