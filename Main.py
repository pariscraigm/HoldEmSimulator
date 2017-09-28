from Card import Card
from Hand import Hand
import getWinner
from random import seed, randint, shuffle
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd

def main():

    time1 = datetime.now()
    cards = [x + y for x in [str(z) for z in range(2,11)] + list("JQKA") for y in list("HSCD")]

    x = []
    y = []

    labels = [x for x in [str(y) for y in range(2, 11)] + list("JQKA")]
    labels.reverse()
    df = pd.DataFrame(0, index=labels, columns=labels)

    for i in range(10000000):
        if (i % 10000 == 0):
            print(i)
        seed(datetime.now())
        shuffle(cards)
        current_cards = list(cards)
        num_players = randint(2, 10)
        hand_list, table_cards = getDealtCards(num_players, current_cards)
        winning_hand = getWinner.get_winner(hand_list, table_cards)
        x = winning_hand.cards[0].card[:-1]
        y = winning_hand.cards[1].card[:-1]
        df.loc[x,y] += 1

    fig = plt.figure()
    ax = fig.add_subplot(111)
    cax = ax.matshow(df, cmap='hot')
    fig.colorbar(cax)
    ax.set_xticklabels(['']+labels)
    ax.set_yticklabels(['']+labels)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
    fig.savefig('holdem_simulation_results_10_million.png')
    plt.show()
    time2 = datetime.now()
    print(time2 - time1)

def getDealtCards(num_players, cards=[]):
    hand_list=[]
    for j in range(num_players):
        card_1 = Card(cards.pop())
        card_2 = Card(cards.pop())
        hand = Hand()
        hand.addCard(card_1)
        hand.addCard(card_2)
        hand_list.append(hand)

    return hand_list, cards[:5]


if __name__ == "__main__":
    main()