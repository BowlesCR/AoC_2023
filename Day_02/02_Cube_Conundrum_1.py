import fileinput
import re

re_game = re.compile(r'^Game (\d+): (.+)\n$')
re_cube = re.compile(r'(\d+) (red|blue|green)')

sum_ = 0

for line in fileinput.input():
    gamenum, gamestr = re_game.match(line).groups()
    rounds = gamestr.split(';')
    impossible = False
    for r in rounds:
        for cube in re_cube.findall(r):
            if cube[1] == 'red' and int(cube[0]) > 12:
                impossible = True
                break
            elif cube[1] == 'green' and int(cube[0]) > 13:
                impossible = True
                break
            elif cube[1] == 'blue' and int(cube[0]) > 14:
                impossible = True
                break
        if impossible:
            print(f"Game {gamenum} is impossible")
            break
    if not impossible:
        print(f"Game {gamenum} is possible")
        sum_ += int(gamenum)
print(sum_)