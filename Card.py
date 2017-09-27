class Card:

    def __init__(self, card):

        self.card = checkCard(self, card)
        self.value = getValue(card[:-1])
        self.suit = card[-1]

cards = [x + y for x in [str(z) for z in range(2, 11)] + list("JQKA") for y in list("HSCD")]

def getValue(card):
    if card not in "JQKA":
        return int(card)
    elif card == "J":
        return 11
    elif card == "Q":
        return 12
    elif card == "K":
        return 13
    elif card == "A":
        return 14


def checkCard(self, card):
    global cards
    if card not in cards:
        raise ValueError
    return card
