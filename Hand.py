class Hand:

    def __init__(self, card1, card2):

        self.cards = [card1, card2]
        self.value = 0
        self.best_cards = None
        self.best_cards_value = []
        self.target_cards = []
        self.kickers = []

    def addCard(self, card):

        if len(self.cards) > 2:
            raise KeyError
        else:
            self.cards.append(card)