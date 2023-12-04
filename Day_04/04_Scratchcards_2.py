import fileinput
import re
from functools import lru_cache


class Card:
    num: int
    winning: set[int]
    have: set[int]

    def __init__(self, num: int, winning: set[int], have: set[int]):
        self.num = num
        self.winning = winning
        self.have = have

    def __str__(self):
        return f"Card {self.num}"

    def num_matches(self):
        return len(self.have.intersection(self.winning))


@lru_cache
def count_cards(card: Card):
    count = 1
    for i in range(card.num_matches()):
        count += count_cards(cards[card.num + i])
    return count


cards: list[Card] = []

for num, line in enumerate(fileinput.input(), start=1):
    halves = line.split(":")[1].split("|")
    winning: set[int] = set(map(int, re.findall(r"(\d+)", halves[0])))
    have: set[int] = set(map(int, re.findall(r"(\d+)", halves[1])))

    cards.append(Card(num, winning, have))

num_cards = 0

for card in cards:
    num_cards += count_cards(card)

print(num_cards)
