import itertools
import Card

def flush(cards=[]):
    suit = cards[1][-1]
    for card in cards:
        if card[-1] != suit:
            return False
    return True

def is_royal(cards=[]):
    for card in cards:
        if card[:-1] not in ["10","J","Q","K","A"]:
            return False
    return True

def is_royal_flush(hand, hand_list=[]):
    for i in hand_list:
        if flush(i) and is_royal(i):
            hand.best_cards = i
            return True
    return False

def straight(cards = []):
    value_list = []
    for card in cards:
        value_list.append(Card.getValue(card[:-1]))
    value_list = sorted(value_list)
    for card in range(len(value_list)-1):
        if value_list[card] + 1 != value_list[card+1]:
            return False
    return True

def straight_and_flush(cards=[]):
    if straight(cards) and flush(cards):
        return True

def get_highest(hands = []):
    highest= []
    largest_val = 0
    for i in hands:
        value_list = []
        for card in i:
            value_list.append(Card.getValue(card[:-1]))
        if max(value_list) > largest_val:
            highest = i
    return highest

def versatile_function(hand, hand_list=[], func=max):
    number_worked = []
    for i in hand_list:
        if func(i):
            number_worked.append(i)
    if len(number_worked) > 1:
        highest = get_highest(number_worked)
        hand.best_cards = highest
        return True
    elif len(number_worked) == 1:
        hand.best_cards = number_worked[0]
        return True
    return False

def matches(match_num, cards=[], match_count = 1):
    counter = 0
    card_count = {}
    for card in cards:
        if card[:-1] not in card_count.keys():
            card_count[card[:-1]] = 1
        else:
            card_count[card[:-1]] += 1
    for value in card_count.values():
        if value == match_num:
            counter += 1
            if counter == match_count:
                return True
    return False


def is_four_of_a_kind(hand, hand_list):
    for i in hand_list:
        if matches(4, i):
            hand.best_cards = i
            return True
    return False

def is_full_house(hand, hand_list):
    for i in hand_list:
        if matches(3,i) and matches(2, i):
            hand.best_cards = i
            return True
    return False

def is_three_of_a_kind(hand, hand_list):
    for i in hand_list:
        if matches(3, i):
            hand.best_cards = i
            return True
    return False

def is_two_pair(hand, hand_list):
    for i in hand_list:
        if matches(2, i, 2):
            hand.best_cards = i
            return True
    return False

def is_pair(hand, hand_list):
    for i in hand_list:
        if matches(2, i):
            hand.best_cards = i
            return True
    return False

def get_winner(player_hands, table_cards):
    """
    :type player_hands: list
    :type table_cards: list
    """
    for hand in player_hands:
        hand_str = [x.card for x in hand.cards]
        hand_list = list(itertools.combinations(hand_str + table_cards, 5))
        hand_list = [list(x) for x in hand_list]
        if is_royal_flush(hand, hand_list):
            hand.value = 10
        elif versatile_function(hand, hand_list, straight_and_flush):
            hand.value = 9
        elif is_four_of_a_kind(hand, hand_list):
            hand.value = 8
        elif is_full_house(hand, hand_list):
            hand.value = 7
        elif versatile_function(hand, hand_list, flush):
            hand.value = 6
        elif versatile_function(hand, hand_list, straight):
            hand.value = 5
        elif is_three_of_a_kind(hand, hand_list):
            hand.value = 4
        elif is_two_pair(hand, hand_list):
            hand.value = 3
        elif is_pair(hand, hand_list):
            hand.value = 2
        else:
            hand.value = 1

    highest_value = 0
    winning_hand = None

    for hand in player_hands:
        if hand.value > highest_value:
            highest_value = hand.value
            winning_hand = hand

    return winning_hand
