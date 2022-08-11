import random
import os
def clear(): os.system('cls')

class Player():
    def __init__(self):
        self.hands = [[]]
        self.bank = 200
        self.bet = 0
        self.hand_values = [0]
        self.statuses = ["Playing"]
    def clear(self):
        self.hands = [[]]
        self.bet = 0
        self.hand_values = [0]
        self.statuses = ["Playing"]

class Dealer():
    def __init__(self):
        self.hand = []
        self.hand_value = 0
    def clear(self):
        self.hand = []
        self.hand_value = 0

class Card:
    def __init__(self, suit, rank):
        self.suit = "Hearts" if suit == 1 else "Diamonds" if suit == 2 else "Clubs" if suit == 3 else "Spades"
        self.rank = "Ace" if rank == 1 else rank if rank < 11 else "Jack" if rank == 11 else "Queen" if rank == 12 else "King"
        self.value = 11 if self.rank == "Ace" else self.rank if rank < 11 else 10

    def __str__(self):
        return f"{self.rank} of {self.suit}"

    def __int__(self):
        return self.value

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

        card = self.deck[0]
        self.deck.remove(self.deck[0])
        return card

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

def printHand(hand):
    for card in hand:
        print(card)

def bogoSort(data):
    while not isSorted(data):
        random.shuffle(data)
    return data

def isSorted(data):
    for i in range(len(data) - 1):
        if int(data[i]) > int(data[i + 1]):
            return False
    return True

def checkDealerBlackjack(hand):
    if hand[0].value == 11:
        print("Checking for blackjack...")
        if hand[1].value > 9:
            return True
        else:
            print("No Blackjack")
    elif hand[0].value > 9:
        print("Checking for blackjack...")
        if hand[1].value == 11:
            return True
        else:
            print("No Blackjack")
    else:
        return False

deck = Deck()
deck.shuffle()

nPlayers = int(input("Number of players: "))
players = [Player() for i in range(nPlayers)]
dealer = Dealer()
clear()
running = True
while running == True:
    # Deal player cards
    for player in players:
        player.clear()
    dealer.clear()
    # Get bets
    for player in players:
        for i in range(len(players)):
            player.bet = int(input(f"Player {i+1} bet ({player.bank} in bank): "))
            player.bank -= player.bet
    clear()

    # Deal dealer cards
    for i in range(2):
        dealer.hand.append(deck.draw())
        for player in players:
            player.hands[0].append(deck.draw())

    # Check for blackjack
    print("Dealer's hand: ")
    print(dealer.hand[0])
    if checkDealerBlackjack(dealer.hand):
        print(f"{dealer.hand[1]}\nDealer has blackjack! Everyone loses.")
        for player in players:
            player.statuses[0] = "Lost"


    print()

    # Show player hands
    if players[0].statuses[0] != "Lost":
        for i in range(nPlayers):
            print(f"Player {i+1}'s hand:")
            printHand(players[i].hands[0])

            players[i].hand_values[0] = sum([card.value for card in players[i].hands[0]])

            # Check for double aces and adjust hand value
            if players[i].hand_values == 22:
                bogoSort(players[i].hands[0])

                if players[i].hands[0][len(players[i].hands[0]) - 1].value == 11:
                    players[i].hands[0][len(players[i].hands[0]) - 1].value = 1
                    players[i].hand_values[0] = sum([card.value for card in players[i].hands[0]])

            print(f"Value: {players[i].hand_values[0]}")

            if players[i].hands[0][1].value == 1:
                players[i].hands[0][1].value = 11

            # Check for player blackjack
            if players[i].hand_values[0] == 21:
                print(f"Blackjack! Player {i+1} wins.")
                players[i].statuses[0] = "Blackjack"
                players[i].bank += players[i].bet * 2.5
            
            # Check for doubles
            if players[i].hands[0][0].value == players[i].hands[0][1].value:
                players[i].hands.append("Split")
            print()

        input("Press enter to continue...")

    # Standard hand play
    for i in range(nPlayers):
        clear()
        if players[i].statuses[0] == "Playing":
            print(f"Player {i+1}'s turn.\nHand:")
            printHand(players[i].hands[0])
            print(f"Value: {players[i].hand_values[0]}")

        while players[i].statuses[0] == "Playing":
            choice = int(input("1. Hit\n2. Stand\n" + ("3. Split\n" if len(players[i].hands) == 2 else "")))
            clear()

            if choice == 1:
                players[i].hands[0].append(deck.draw())
                print("Hand:")
                printHand(players[i].hands[0])
                print()
                players[i].hand_values[0] = sum([card.value for card in players[i].hands[0]])

                if players[i].hand_values[0] == 21:
                    print(f"Value: 21\n")
                    players[i].statuses[0] = "Done"
                elif players[i].hand_values[0] > 21:
                    bogoSort(players[i].hands[0])

                    if players[i].hands[0][len(players[i].hands[0]) - 1].value == 11:
                        players[i].hands[0][len(players[i].hands[0]) - 1].value = 1
                        players[i].hand_values[0] = sum([card.value for card in players[i].hands[0]])

                    if players[i].hand_values[0] > 21:
                        print(f"Value: {players[i].hand_values[0]}\nBust")
                        players[i].statuses[0] = "Lost"
                        input("Press enter to continue...")
                        break

                print(f"Value: {players[i].hand_values[0]}")
                input("Press enter to continue...")

            elif choice == 2:
                players[i].statuses[0] = "Done"
            
            elif choice == 3 and players[i].hands[2] == "Split":
                players[i].hands.remove("Split")
                players[i].hands[0].remove(players[i].hands[0][0])
                players[i].hands.append([players[i].hands[0][0]])
                players[i].hand_values[0] = sum([card.value for card in players[i].hands[0]])
                players[i].hand_values[1] = sum([card.value for card in players[i].hands[1]])
                players[i].bet += players[i].bet
                players[i].bank -= players[i].bet
                players[i].statuses[0] = "Split"
                clear()
        
        # Split hand play
        if players[i].statuses[0] == "Split":
            for j in range(2):
                print(f"Player {i+1}'s {'first' if j == 0 else 'second'} hand:")
                printHand(players[i].hands[j])
                print(f"Value: {players[i].hand_values[j]}")

                while players[i].statuses[0] == "Split":
                    choice = int(input("1. Hit\n2. Stand\n"))
                    clear()

                    if choice == 1:
                        players[i].hands[j].append(deck.draw())
                        print("Hand:")
                        printHand(players[i].hands[j])
                        print()
                        players[i].hand_values[j] = sum([card.value for card in players[i].hands[j]])

                        if players[i].hand_values[j] == 21:
                            print(f"Value: 21\n")
                            players[i].statuses.append("Done")
                        elif players[i].hand_values[j] > 21:
                            bogoSort(players[i].hands[j])

                            if players[i].hands[j][len(players[i].hands[j]) - 1].value == 11:
                                players[i].hands[j][len(players[i].hands[j]) - 1].value = 1
                                players[i].hand_values[j] = sum([card.value for card in players[i].hands[j]])

                            if players[i].hand_values[j] > 21:
                                print(f"Value: {players[i].hand_values[j]}\nBust")
                                players[i].statuses.append("Lost")
                                input("Press enter to continue...")
                                break

                        print(f"Value: {players[i].hand_values[j]}")
                        input("Press enter to continue...")

                    elif choice == 2:
                        players[i].statuses.append("Done")
                        break



    dealer.hand_value = sum([card.value for card in dealer.hand])
    print("Dealer's turn.\nHand:")
    printHand(dealer.hand)
    print(f"Value: {dealer.hand_value}")
    input("Press enter to continue...")

    # Dealer hand play
    while dealer.hand_value < 16:
        clear()

        print("Dealer's turn.\nHand:")
        dealer.hand.append(deck.draw())
        printHand(dealer.hand)

        dealer.hand_value = sum([card.value for card in dealer.hand])
        bogoSort(dealer.hand)
        if dealer.hand_value > 21 and dealer.hand[len(dealer.hand) - 1].value == 11:
            dealer.hand[len(dealer.hand) - 1].value = 1
            dealer.hand_value = sum([card.value for card in dealer.hand])

        print(f"Value: {dealer.hand_value}")
        input("Press enter to continue...")

    if dealer.hand_value > 21:
        print("Dealer busts")
        for player in players:
            for i in range(len(player.statuses)):
                player.statuses[i] = "Push" if player.statuses[i] == "Lost" else "Won"
    # Final win/loss check
    else:
        for i in range(len([players[x].hands[y] for x in range(len(players)) for y in range(len(players[x].hands))])):
            if i < nPlayers and players[i].statuses[0] == "Done":
                clear()
                print(f"Player {i+1}'s {'' if len(players[i].hands) == 1 else 'first'} Hand:")
                printHand(players[i].hands[0])
                print(f"Value: {players[i].hand_values[0]}\n")
                print("Dealer's Hand:")
                printHand(dealer.hand)
                print(f"Value: {dealer.hand_value}")
                players[i].statuses[0] = "Won" if players[i].hand_values[0] > dealer.hand_value else "Push" if players[i].hand_values[0] == dealer.hand_value else "Lost"
                print("Dealer wins" if players[i].statuses[0] == "Lost" else "Push" if players[i].statuses[0] == "Push" else f"Player {i+1} wins")
                input("Press enter to continue...")
            # Split hand win/loss check
            else:
                if players[i].statuses[0] != "Lost":
                    clear()
                    print(f"Player {(i - nPlayers) + 1}'s second hand:")
                    printHand(players[(i - nPlayers) + 1].hands[1])
                    print(f"Value: {players[(i - nPlayers) + 1].hand_values[1]}\n")
                    print("Dealer's Hand:")
                    printHand(dealer.hand)
                    print(f"Value: {dealer.hand_value}")
                    players[(i - nPlayers) + 1].statuses[1] = "Won" if players[(i - nPlayers) + 1].hand_values[1] > dealer.hand_value else "Push" if players[(i - nPlayers) + 1].hand_values[1] == dealer.hand_value else "Lost"
                    print("Dealer wins" if players[(i - nPlayers) + 1].statuses[1] == "Lost" else "Push" if players[(i - nPlayers) + 1].statuses[1] == "Push" else f"Player {(i - nPlayers) + 1} wins")


    
    for i in range(len([players[x].hands[y] for x in range(len(players)) for y in range(len(players[x].hands))])):
        if i < nPlayers:
            players[i].bank += players[i].bet * (2 if players[i].statuses[0] == "Won" else 0 if players[i].statuses[0] == "Lost" else 1)
        else:
            players[(i - nPlayers) + 1].bank += players[(i - nPlayers) + 1].bet * (2 if players[(i - nPlayers) + 1].statuses[1] == "Won" else 0 if players[(i - nPlayers) + 1].statuses[1] == "Lost" else 1)
    running = False if int(input("1. Play again\n2. Exit\n")) == 2 else True
clear()