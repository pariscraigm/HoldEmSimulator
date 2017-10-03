

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


def get_value_list(cards=[]):

    card_li = []
    for card in cards:
        card_li.append(getValue(card[:-1]))
    card_li.sort()
    return card_li


def checkCard(self, card):
    global cards
    if card not in cards:
        raise ValueError
    return card
