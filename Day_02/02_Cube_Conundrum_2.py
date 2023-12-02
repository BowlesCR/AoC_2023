import fileinput
import re

re_game = re.compile(r'^Game (\d+): (.+)\n$')
re_cube = re.compile(r'(\d+) (red|blue|green)')

sum_ = 0

for line in fileinput.input():
    gamenum, gamestr = re_game.match(line).groups()
    rounds = gamestr.split(';')

    red = 0
    green = 0
    blue = 0

    for r in rounds:
        for cube in re_cube.findall(r):
            if cube[1] == 'red':
                red = max(red, int(cube[0]))
            elif cube[1] == 'green':
                green = max(green, int(cube[0]))
            elif cube[1] == 'blue':
                blue = max(blue, int(cube[0]))

    power = red * blue * green
    print(power)
    sum_ += power

print(sum_)