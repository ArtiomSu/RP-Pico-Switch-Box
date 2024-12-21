from game import Game
from power import Power
from hardware import Hardware

hardware = Hardware()

# 0 is running game
# 1 is running pc power.
run_mode = 1

def checkRunMode():
    global run_mode
    last_run_mode = run_mode
    current = hardware.get_setting()
    if current:
        run_mode = 1
    else:
        run_mode = 0

    if last_run_mode != run_mode:
        return True
    
    return False

if __name__ == "__main__":
    game = Game(hardware)
    power = Power(hardware)
    checkRunMode()
    while True:
        if checkRunMode():
            game.reset()
            power.reset()
        if run_mode == 0:
            game.run_game_next_state()
        else:
            power.run_next_check()