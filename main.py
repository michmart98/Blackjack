#from functions import playing, Card, Deck, Hand, Chips, take_bet, hit, hit_or_stand, show_some, show_all, player_busts, player_wins, dealer_busts ,dealer_wins, push, replay 

import random

#Declare variables to store suits, ranks and values
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

playing = True
replay_count = 0
total = 0

#Hold the Deck-Cards, shuffle it and deal out
class Card:
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
        
    def __str__(self):
        return self.rank + ' of ' + self.suit

# In this class we will store our 52 cards
class Deck:
    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank)) # build Card objects and add them to the list

    def __str__(self):
        deck_comp = ''  # start with an empty string
        for card in self.deck:
            deck_comp += '\n '+card.__str__() # add each Card object's print string
        return 'The deck has:' + deck_comp

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        single_card = self.deck.pop()
        return single_card

#What are we holding
class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0 #counter for aces

    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces +=1 #increase aces count

    def adjust_for_ace(self): #the ace has double role, if the sum is over 21, we take ace as if the sum is over 21 we can choose to count
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1 


#In this class we adjust the value of the Chips, winning or losing bets
class Chips:

    def __init__(self):
        global total
        global replay_count
        self.bet = 0
        while True:
            try:
                ######### FIRST TIME PLAYING #########
                if replay_count == 0:
                    total = int(input("Please enter the total value of chips available for playing "))
                else:
                    ######### REPLAY #########
                    extra_chips = 0
                    add_chips = input('Do you want to add chips? Enter Yes or No: ').lower()
                    while True:
                        if add_chips == 'yes':
                            print(f"You are currently holding {total} chips")
                            try:
                                extra_chips = int(input("Add the amount of chips you want to include in your total amount "))
                                if extra_chips <= 0:
                                    raise ValueError("We want an positive integer for the extra chips we want to add") 
                                else:
                                    total = extra_chips + total
                                    break
                            except ValueError:
                                print('Sorry, the total amount of chips must be a positive integer!2')
  
                        elif add_chips == 'no':
                            break
                        else:
                            print('Please provide a valid answer')
                ######### BOTH FOR PLAYING 1ST TIME AND REPLAY #########
                if total <= 0:
                    raise ValueError("We want a positive integer for the total amount of chips") 
                replay_count += 1
            except ValueError:
                print('Sorry, the total amount of chips must be a positive integer!')
            else:
                break
    
    def win_bet(self):
        global total
        total += self.bet

    def lose_bet(self):
        global total
        total -= self.bet



def take_bet(chips):
    global total
    while True:
        try:
            chips.bet = int(input('How many chips would you like to bet? '))
            if chips.bet <= 0:
                raise ValueError #We want an integer that is positive as bet
        except ValueError:
            print('Sorry, a bet must be a positive integer!')
        else:
            if chips.bet > total:
                print("Sorry, your bet can't exceed",total)
            else:
                break
            

def hit(deck,hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()


def hit_or_stand(deck,hand):
    global playing 
    while True:
        x = input('Would you Hit or Stand? Type your decision: ')
        if x.capitalize() == "Hit":
            hit(deck,hand) 
        elif x.capitalize() ==  "Stand":
            print("Player chooses to stand. It's Dealer's turn")
            playing = False
        else:
            print("Sorry, please insert a valid option, Hit or Stand.")
            continue
        break


def show_some(player,dealer):
    print("\nDealer's Hand:")
    print(" <card hidden>")
    print('',dealer.cards[1])  
    print("\nPlayer's Hand:", *player.cards, sep='\n ')


def show_all(player,dealer):
    print("\nDealer's Hand:", *dealer.cards, sep='\n ')
    print("Dealer's Hand =",dealer.value)
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    print("Player's Hand =",player.value)

def player_busts(player,dealer,chips):
    print("Player busts!")
    chips.lose_bet()

def player_wins(player,dealer,chips):
    print("Player wins!")
    chips.win_bet()

def dealer_busts(player,dealer,chips):
    print("Dealer busts!")
    chips.win_bet()
    
def dealer_wins(player,dealer,chips):
    print("Dealer wins!")
    chips.lose_bet()
    
def push(player,dealer):
    print("Dealer and Player tie! It's a push.")


### Replay function
def replay():
    global playing 
    answer = ""
    while answer != True or answer != False:
        answer = input('Do you want to play again? Enter Yes or No: ').lower()
        if answer == 'yes':
            playing = True
            answer = True
            return True
        elif answer == 'no':
            break
        else:
            print('Please provide a valid answer')



while True:
    # Print an opening statement
    print('Welcome to BlackJack! Get as close to 21 as you can without going over!\n\
    Aces count as 1 or 11.')
    
    # Create & shuffle the deck, deal two cards to each player
    deck = Deck()
    deck.shuffle()
    
    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
            
    # Set up the Player's chips
    player_chips = Chips()    
    
    # Prompt the Player for their bet
    take_bet(player_chips)
    
    # Show cards (but keep one dealer card hidden)
    show_some(player_hand,dealer_hand)
    
    while playing:  # recall this variable from our hit_or_stand function
        
        # Prompt for Player to Hit or Stand
        hit_or_stand(deck,player_hand) 
        
        # Show cards (but keep one dealer card hidden)
        show_some(player_hand,dealer_hand)  
        
        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player_hand.value > 21:
            player_busts(player_hand,dealer_hand,player_chips)
            break        


    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17 
    if player_hand.value <= 21:  
    
        # Show all cards
        show_all(player_hand,dealer_hand)
        
        # Run different winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_hand,dealer_hand,player_chips)

        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand,dealer_hand,player_chips)

        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand,dealer_hand,player_chips)

        else:
            push(player_hand,dealer_hand)        

    
    # Inform Player of their chips total 
    print("\nPlayer's winnings stand at",total)

    if not replay():
       break