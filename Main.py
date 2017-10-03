from Hand import Hand
import getWinner
from random import seed, randint, shuffle
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
from progress.bar import IncrementalBar

def main():

    simulation_number = 100

    cards = [x + y for x in [str(z) for z in range(2, 11)] + list("JQKA") for y in list("HSCD")]

    labels = [x for x in [str(y) for y in range(2, 11)] + list("JQKA")]
    labels.reverse()
    df = pd.DataFrame(0.0, index=labels, columns=labels)

    bar = IncrementalBarHours('Simulating', max=simulation_number)

    for i in range(simulation_number):
        seed(datetime.now())
        shuffle(cards)
        current_cards = list(cards)
        num_players = randint(2, 10)
        hand_list, table_cards = get_dealt_cards(num_players, current_cards)
        winning_hand_list = getWinner.get_winner(hand_list, table_cards)
        if len(winning_hand_list) == 1:
            x = winning_hand_list[0].cards[0][:-1]
            y = winning_hand_list[0].cards[1][:-1]
            df.loc[x, y] += 1.0
            df.loc[y, x] += 1.0
        else:
            for hand in winning_hand_list:
                x = hand.cards[0][:-1]
                y = hand.cards[1][:-1]
                df.loc[x, y] += 1.0 / len(winning_hand_list)
                df.loc[y, x] += 1.0 / len(winning_hand_list)
        bar.next()

    # total = df.sum()
    # df = df/total
    fig = plt.figure()
    ax = fig.add_subplot(111)
    cax = ax.matshow(df, cmap='hot')
    fig.colorbar(cax)
    ax.set_xticklabels(['']+labels)
    ax.set_yticklabels(['']+labels)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
    fig.savefig('holdem_simulation_results_' + "{:,}".format(simulation_number) + '.png')
    plt.title('{:,}'.format(simulation_number) + " simulations")
    bar.finish()
    plt.show()


def get_dealt_cards(num_players, cards=[]):
    hand_list=[]
    for j in range(num_players):
        hand = Hand(cards.pop(),cards.pop())
        hand_list.append(hand)

    return hand_list, cards[:5]


class IncrementalBarHours(IncrementalBar):

    suffix = '%(percent).1f%% | %(remaining_mins)dm |'

    @property
    def remaining_mins(self):
        return self.eta // 60

if __name__ == "__main__":
    main()
