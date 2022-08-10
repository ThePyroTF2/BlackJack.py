import random

class Card:
    def __init__(self, suit, rank):
        self.suit = "Hearts" if suit == 1 else "Diamonds" if suit == 2 else "Clubs" if suit == 3 else "Spades"
        self.rank = "Ace" if rank == 1 else rank if rank < 11 else "Jack" if rank == 11 else "Queen" if rank == 12 else "King"

    def __str__(self):
        return f"{self.rank} of {self.suit}"

class Deck:
    def __init__(self):
        self.deck = []
        for suit in range(1, 5):
            for rank in range(1, 14):
                self.deck.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.deck)

    def draw(self):
        if len(self.deck) == 0:
            self.repop()

        self.deck.remove(self.deck[0])
        return self.deck[0]

    def repop(self):
        self.deck = []
        for suit in range(1, 5):
            for rank in range(1, 14):
                self.deck.append(Card(suit, rank))
        self.shuffle()

    def sort(self):
        self.deck = []
        for suit in range(1, 5):
            for rank in range(1, 14):
                self.deck.append(Card(suit, rank))

    def print(self):
        for card in self.deck:
            print(card)

deck = Deck()
deck.shuffle()

nPlayers = int(input("Number of players: "))

dHand = []
pHands = [[] for i in range(nPlayers)]

for n in range(2):
    dHand.append(deck.draw())
    for i in range(nPlayers):
        pHands[i].append(deck.draw())

print("Dealer's hand: ")
for card in dHand:
    print(card)

print()

for i in range(nPlayers):
    print(f"Player {i+1}'s hand:")
    for card in pHands[i]:
        print(card)
    print()
