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
del parts

# Reduce workflows:
changes = True
while changes:
    changes = False
    for w in workflows:
        if len(workflows[w]) == 1:
            continue
        results = [s[-1] for s in workflows[w]]
        if all([r == "A" for r in results]):
            workflows[w] = [tuple("A")]
            changes = True
        elif all([r == "R" for r in results]):
            workflows[w] = [tuple("R")]
            changes = True
        else:
            for i, r in enumerate(results):
                if r not in ["A", "R"] and len(workflows[r]) == 1:
                    workflows[w][i] = tuple(workflows[r][0][0]) if len(workflows[w][i]) == 1 else (workflows[w][i][0], workflows[r][0][0])
                    changes = True


count = 0
for x in range(1, 4001):
    for m in range(1, 4001):
        for a in range(1, 4001):
            for s in range(1, 4001):
                if check_part((x, m, a, s), "in"):
                    count += 1
