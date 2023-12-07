import fileinput
from collections import Counter
from enum import Enum
from operator import itemgetter


class Type(Enum):
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    THREE_KIND = 3
    FULL_HOUSE = 4
    FOUR_KIND = 5
    FIVE_KIND = 6

    def __lt__(self, other):
        return self.value < other.value


def map_values(x: str):
    if x.isdigit():
        return int(x)
    match x:
        case "T":
            return 10
        case "J":
            return 1
        case "Q":
            return 12
        case "K":
            return 13
        case "A":
            return 14


def hand_type(hand: list[int]) -> Type:
    hand_count = Counter(hand)
    most_common = [card for card in hand_count.most_common() if card[0] != 1]

    match (most_common[0][1] if most_common else 0) + hand_count.get(1, 0):
        case 5:  # Five of a kind
            return Type.FIVE_KIND
        case 4:  # Four of a kind
            return Type.FOUR_KIND
        case 3:  # Full house or three of a kind
            if hand_count.most_common(2)[1][1] == 2:  # Full house
                return Type.FULL_HOUSE
            else:  # Three of a kind
                return Type.THREE_KIND
        case 2:  # Two pair or one pair
            if hand_count.most_common(2)[1][1] == 2:  # Two pair
                return Type.TWO_PAIR
            else:  # One pair
                return Type.ONE_PAIR
        case 1:  # High card
            return Type.HIGH_CARD
        case _:
            assert False


hands: list[tuple[Type, list[int], int]] = []

for line in fileinput.input():
    hand, bid = line.strip().split(" ")
    hand = list(map(map_values, hand))

    bid = int(bid)

    hands.append((hand_type(hand), hand, bid))
del hand, bid

hands.sort(key=itemgetter(0, 1))
winnings = 0
for rank, hand in enumerate(hands, start=1):
    winnings += rank * hand[2]

print(winnings)
