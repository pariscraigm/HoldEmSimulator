from Card import Card
from Hand import Hand
import getWinner
from random import seed, randint, shuffle
from datetime import datetime

def main():

    cards = [x + y for x in [str(z) for z in range(2,11)] + list("JQKA") for y in list("HSCD")]

    for i in range(100):
        seed(datetime.now())
        shuffle(cards)
        current_cards = list(cards)
        num_players = randint(2, 10)
        hand_list, table_cards = getDealtCards(num_players, current_cards)
        winning_hand = getWinner.get_winner(hand_list, table_cards)

        print(winning_hand.cards[0].card ," ", '\t\t',
              winning_hand.cards[1].card, '\t',
              winning_hand.value, '\t',
              winning_hand.best_cards)

def getDealtCards(num_players, cards=[]):
    hand_list=[]
    for j in range(num_players):
        card_1 = Card(cards.pop())
        card_2 = Card(cards.pop())
        hand = Hand()
        hand.addCard(card_1)
        hand.addCard(card_2)
        hand_list.append(hand)
        table_cards = [Card(x) for x in cards[:5]]

    return hand_list, table_cards


if __name__ == "__main__":
    main()