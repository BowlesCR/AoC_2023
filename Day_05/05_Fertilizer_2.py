import fileinput
import re
import sys
from collections import defaultdict

re_nums = re.compile(r"(\d+)")

seeds: list[range] = []

mappings: defaultdict[str, dict[range, int]] = defaultdict(dict)

state = "seeds"

for line in fileinput.input():
    if line == "\n":
        continue

    statechange = True
    match line.split(" ")[0]:
        case "seeds:":
            seedline = list(map(int, re_nums.findall(line)))
            for i in range(0, len(seedline), 2):
                seeds.append(range(seedline[i], seedline[i] + seedline[i + 1]))
        case "seed-to-soil":
            state = "seed_soil"
        case "soil-to-fertilizer":
            state = "soil_fert"
        case "fertilizer-to-water":
            state = "fert_water"
        case "water-to-light":
            state = "water_light"
        case "light-to-temperature":
            state = "light_temp"
        case "temperature-to-humidity":
            state = "temp_humid"
        case "humidity-to-location":
            state = "humid_loc"
        case _:
            statechange = False
    if statechange:
        continue

    nums = list(map(int, re_nums.findall(line)))
    mappings[state].update(
        {
            range(nums[1], nums[1] + nums[2]): nums[0] - nums[1],
        }
    )

min_loc = sys.maxsize
for seedrange in seeds:
    for seed in seedrange:
        num = seed
        for state in ["seed_soil", "soil_fert", "fert_water", "water_light", "light_temp", "temp_humid", "humid_loc"]:
            for r in mappings[state]:
                if num in r:
                    num += mappings[state][r]
                    break
        min_loc = min(min_loc, num)
    print(min_loc)
print(f"final: {min_loc}")
