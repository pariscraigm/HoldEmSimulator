import itertools
import Card


def flush(cards=[]):
    """
    Checks to see if the supplied cards are all of the same suit
    :param cards: A list if strings of the form "card_value" + "suit" e.g. "KH"
    :return: True if the given cards represent a flush, False otherwise
    """
    suit = cards[1][-1]
    for card in cards:
        if card[-1] != suit:
            return False
    return True


def is_royal(cards=[]):
    """
    Checks to see if all cards in the supplied list are 'royal'
    :param cards: A list of cards in the form "KH"
    :return: True if the cards are all royal
    """
    for card in cards:
        if card[:-1] not in ["10", "J", "Q", "K", "A"]:
            return False
    return True


def is_royal_flush(hand, hand_list=[]):
    """
    Determines if one of the hands in the given hand_list is a royal flush
    :param hand: a hand object
    :param hand_list: The list of all possible 5 card combinations comprised of the two cards in the hand and 5 cards
    on the table
    :return: True if there is a royal flush in the hand. false otherwise.
    """
    for i in hand_list:
        if flush(i) and is_royal(i):
            hand.best_cards = i
            return True
    return False


def straight(cards=[]):
    """
    Checks to see if the cards in the supplied list form a sequence.
    :param cards: a list of 5 cards
    :return: True if the cards form a straight. False otherwise.
    """
    value_list = []
    for card in cards:
        value_list.append(Card.getValue(card[:-1]))
    value_list = sorted(value_list)
    for card in range(len(value_list) - 1):
        if value_list[card] + 1 != value_list[card + 1]:
            return False
    return True


def straight_and_flush(cards=[]):
    """
    Determines if the cards comprise a straight flush.
    :param cards: a list of 5 cards
    :return: True if the cards are a straight flush. False otherwise.
    """
    if straight(cards) and flush(cards):
        return True


def get_highest(hands=[]):
    """
    Returns the list with the largest value.
    :param hands: The list of hands to compare.
    :return: The highest hand.
    """
    highest = []
    largest_val = 0
    for hand in hands:
        value_list = []
        for card in hand:
            value_list.append(Card.getValue(card[:-1]))
        if max(value_list) > largest_val:
            highest = hand
    return highest


def versatile_function(hand, func, hand_list=[]):
    """
    A function that can be utilized by multiple card checks.
    :param hand: the current hole hand.
    :param func: the function to use to compare the cards.
    :param hand_list: The list of different hands comprised of the hole cards and table cards.
    :return: True if one of the hands is found true by the function. False otherwise.
    """
    number_worked = []
    for i in hand_list:
        if func(i):
            number_worked.append(i)
    if len(number_worked) > 1:
        highest = get_highest(number_worked)
        hand.best_cards = highest
        hand.best_cards_value = sorted(Card.get_value_list(highest), reverse=True)
        return True
    elif len(number_worked) == 1:
        hand.best_cards = number_worked[0]
        hand.best_cards_value = sorted(Card.get_value_list(number_worked[0]), reverse=True)
        return True
    return False


def matches(match_num, hand, cards=[], match_count=1):
    """
    Used to check the hands for matching card values.
    :param match_num: The number of cards to match. (2 for pair, 3 for 3 of a kind, etc...)
    :param hand: the hole cards of interest.
    :param cards: A list of 5 cards
    :param match_count: How many to be matched (2 for 2 pair, etc...)
    :return: True if the matches are found, False otherwise.
    """
    counter = 0
    card_count = {}
    for card in cards:
        if card[:-1] not in card_count.keys():
            card_count[card[:-1]] = 1
        else:
            card_count[card[:-1]] += 1
    for key, value in card_count.items():
        if value == match_num:
            counter += 1
            hand.best_cards_value.append(Card.getValue(key))
            if counter == match_count:
                hand.kickers = sorted([Card.getValue(k) for k, v in card_count.items() if v != match_num], reverse=True)
                return True
    return False


def is_four_of_a_kind(hand, hand_list):
    """
    Checks to see if their is a four of kind in the hand_list
    :param hand: the hole cards
    :param hand_list: the list of combinations of 5 cards using the hole cards and table cards.
    :return: True if there is a four of a kind. False otherwise.
    """
    for i in hand_list:
        if matches(4, hand, i):
            hand.best_cards = i
            return True
    return False


def is_full_house(hand, hand_list):
    for i in hand_list:
        if matches(3, hand, i) and matches(2, hand, i):
            hand.best_cards = i
            return True
    return False


def is_three_of_a_kind(hand, hand_list):
    for i in hand_list:
        if matches(3, hand, i):
            hand.best_cards = i
            return True
    return False


def is_two_pair(hand, hand_list):
    for i in hand_list:
        if matches(2, hand, i, 2):
            hand.best_cards = i
            return True
    return False


def is_pair(hand, hand_list):
    for i in hand_list:
        if matches(2, hand, cards=i):
            hand.best_cards = i
            return True
    return False


def get_winner(player_hands, table_cards):
    """
    :type player_hands: list
    :type table_cards: list
    """
    for hand in player_hands:
        hand_str = [x for x in hand.cards]
        hand_list = list(itertools.combinations(hand_str + table_cards, 5))
        hand_list = [list(x) for x in hand_list]
        if is_royal_flush(hand, hand_list):
            return [hand]
        elif versatile_function(hand, straight_and_flush, hand_list):
            hand.value = 9
        elif is_four_of_a_kind(hand, hand_list):
            hand.value = 8
        elif is_full_house(hand, hand_list):
            hand.value = 7
        elif versatile_function(hand, flush, hand_list):
            hand.value = 6
        elif versatile_function(hand, straight, hand_list):
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
    winning_hand_list = []
    winning_hand = None

    for hand in player_hands:
        if hand.value > highest_value:
            highest_value = hand.value
            winning_hand_list = [hand]
        elif hand.value == highest_value:
            winning_hand_list.append(hand)

    if len(winning_hand_list) == 1:
        return winning_hand_list
    elif len(winning_hand_list) > 1:
        highest_card = 0
        if highest_value == 9:
            for hand in winning_hand_list:
                if hand.best_cards_value[0] > highest_card:
                    highest_card = hand.best_cards_value[0]
                    winning_hand = hand
            return [winning_hand]
        elif highest_value == 8:
            if winning_hand_list[0].best_cards_value[0] > winning_hand_list[1].best_cards_value[0]:
                return [winning_hand_list[0]]
            else:
                return [winning_hand_list[1]]
        elif highest_value == 7:
            full_li = []
            for hand in winning_hand_list:
                if hand.best_cards_value[0] > highest_card:
                    highest_card = hand.best_cards_value[0]
                    full_li = [hand]
                elif hand.best_cards_value[0] == highest_card:
                    full_li.append(hand)
            if len(full_li) > 1:
                value_list = []
                for hand in full_li:
                    value_list.append(hand.best_cards_value[1])
                high_val = max(value_list)
                j = 0
                while j < len(full_li):
                    if full_li[j].best_cards_value[1] < high_val:
                        del full_li[j]
                        j -= 1
                    j += 1
            return full_li
        elif highest_value == 6:
            for i in range(5):
                value_list = []
                for hand in winning_hand_list:
                    value_list.append(hand.best_cards_value[i])
                high_val = max(value_list)
                j = 0
                while j < len(winning_hand_list):
                    if winning_hand_list[j].best_cards_value[i] < high_val:
                        del winning_hand_list[j]
                        j -= 1
                    j += 1
            return winning_hand_list

        elif highest_value == 5:
            value_list = []
            for hand in winning_hand_list:
                value_list.append(hand.best_cards_value[0])
            high_val = max(value_list)
            j = 0
            while j < len(winning_hand_list):
                if winning_hand_list[j].best_cards_value[0] < high_val:
                    del winning_hand_list[j]
                    j -= 1
                j += 1
            return winning_hand_list

        elif highest_value == 4:
            value_list = []
            for hand in winning_hand_list:
                value_list.append(hand.best_cards_value[0])
            high_val = max(value_list)
            j = 0
            while j < len(winning_hand_list):
                if winning_hand_list[j].best_cards_value[0] < high_val:
                    del winning_hand_list[j]
                    j -= 1
                j += 1
            for i in range(2):
                value_list = []
                for hand in winning_hand_list:
                    value_list.append(hand.kickers[i])
                high_val = max(value_list)
                j = 0
                while j < len(winning_hand_list):
                    if winning_hand_list[j].kickers[i] < high_val:
                        del winning_hand_list[j]
                        j -= 1
                    j += 1
            return winning_hand_list
        elif highest_value == 3:
            for hand in winning_hand_list:
                hand.best_cards_value.sort(reverse=True)
            for i in range(2):
                value_list = []
                for hand in winning_hand_list:
                    value_list.append(hand.best_cards_value[i])
                high_val = max(value_list)
                j = 0
                while j < len(winning_hand_list):
                    if winning_hand_list[j].best_cards_value[i] < high_val:
                        del winning_hand_list[j]
                        j -= 1
                    j += 1
            value_list = []
            for hand in winning_hand_list:
                value_list.append(hand.kickers[0])
            high_val = max(value_list)
            j = 0
            while j < len(winning_hand_list):
                if winning_hand_list[j].kickers[0] < high_val:
                    del winning_hand_list[j]
                    j -= 1
                j += 1
            return winning_hand_list
        elif highest_value == 2:
            value_list = []
            for hand in winning_hand_list:
                value_list.append(hand.best_cards_value[0])
            high_val = max(value_list)
            j = 0
            while j < len(winning_hand_list):
                if winning_hand_list[j].best_cards_value[0] < high_val:
                    del winning_hand_list[j]
                    j -= 1
                j += 1
            for i in range(3):
                value_list = []
                for hand in winning_hand_list:
                    value_list.append(hand.kickers[i])
                high_val = max(value_list)
                j = 0
                while j < len(winning_hand_list):
                    if winning_hand_list[j].kickers[i] < high_val:
                        del winning_hand_list[j]
                        j -= 1
                    j += 1
            return winning_hand_list

        elif highest_value == 1:
            for hand in winning_hand_list:
                hand.best_cards_value = sorted(Card.get_value_list(hand.cards), reverse=True)
            for i in range(2):
                value_list = []
                for hand in winning_hand_list:
                    value_list.append(hand.best_cards_value[i])
                high_val = max(value_list)
                j = 0
                while j < len(winning_hand_list):
                    if winning_hand_list[j].best_cards_value[i] < high_val:
                        del winning_hand_list[j]
                        j -= 1
                    j += 1
            return winning_hand_list
