class Hand:

    def __init__(self):

        self.cards = []
        self.value = 0
        self.best_cards = None
        self.target_cards = []
        self.kickers = []

    def addCard(self, card):

        if len(self.cards) > 2:
            raise KeyError
        else:
            self.cards.append(card)