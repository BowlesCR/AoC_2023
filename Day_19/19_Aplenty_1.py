import fileinput
import re

def check_part(part: tuple[int, int, int, int], workflow: str) -> bool:
    for step in workflows[workflow][:-1]:
        if eval(step[0]):
            if step[1] == 'R':
                return False
            elif step[1] == 'A':
                return True
            else:
                return check_part(part, step[1])
    step = workflows[workflow][-1]
    if step[0] == 'R':
        return False
    elif step[0] == 'A':
        return True
    else:
        return check_part(part, step[0])


re_workflow = re.compile(r"^(\w+)\{(.+)}$")
re_part = re.compile(r"^\{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}$")


workflows: dict[str, list[tuple[str | str, str]]] = {}
parts: list[tuple[int, int, int, int]] = []

for line in fileinput.input():
    m = re_workflow.match(line)
    if line.strip() == "":
        continue
    elif m:
        steps = [tuple(s.split(":")) for s in m.group(2).split(",")]
        workflows[m.group(1)] = steps
    else:
        m = re_part.match(line)
        parts.append(tuple(map(int, m.groups())))

total = 0
for part in parts:
    if check_part(part, "in"):
        total += sum(part)

print(total)