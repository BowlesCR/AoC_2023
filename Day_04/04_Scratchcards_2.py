import fileinput
import re
from functools import lru_cache

re_split = re.compile(r"^Card\s+(\d+): (.+) \| (.*)\n$")
re_nums = re.compile(r"(\d+)")


class Card:
    num: int
    winning: set[int]
    have: set[int]

    def __init__(self, line: str):
        parts = re_split.match(line)
        self.num = int(parts.group(1))
        self.winning: set[int] = set(map(int, re_nums.findall(parts.group(2))))
        self.have: set[int] = set(map(int, re_nums.findall(parts.group(3))))

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


if __name__ == "__main__":
    cards: list[Card] = []

    for line in fileinput.input():
        cards.append(Card(line))
    del line

    num_cards = 0

    for card in cards:
        num_cards += count_cards(card)

    print(num_cards)
