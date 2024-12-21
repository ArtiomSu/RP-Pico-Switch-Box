from game import Game
from hardware import Hardware

hardware = Hardware()

# 0 is running game
# 1 is running pc power.
run_mode = 0

if __name__ == "__main__":
    game = Game(hardware)
    while True:
        if run_mode == 0:
            game.run_game_next_state()