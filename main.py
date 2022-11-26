import random

#Declare variables to store suits, ranks and values
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

playing = True

#Hold the Deck-Cards, shuffle it and deal out
class Card:
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
        
    def __str__(self):
        return self.rank + ' of ' + self.suit

# In this class we will store our 52 cards
class Deck:
    def __init__(self) -> None:
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank)) # build Card objects and add them to the list

    def __str__(self) -> str:
        deck_comp = ''  # start with an empty string
        for card in self.deck:
            deck_comp += '\n '+card.__str__() # add each Card object's print string
        return 'The deck has:' + deck_comp

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        single_card = self.deck.pop()
        return single_card

test_deck = Deck()
print(test_deck)

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
        self.bet = 0
        while True:
            try:
                self.total = int(input("Please enter the total value of chips available for playing "))
                if self.total < 0:
                    raise ValueError #We want an integer that is positive as value of chips
            except ValueError:
                print('Sorry, the total amount of chips must be a positive integer!')
            else:
                break
        

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet



def take_bet(chips):
    
    while True:
        try:
            chips.bet = int(input('How many chips would you like to bet? '))
            if chips.bet < 1:
                raise ValueError #We want an integer that is positive as bet
        except ValueError:
            print('Sorry, a bet must be a positive integer!')
        else:
            if chips.bet > chips.total:
                print("Sorry, your bet can't exceed",chips.total)
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
    answer = ""
    while answer != True or answer != False:
        answer = input('Do you want to play again? Enter Yes or No: ').lower()
        if answer == 'yes':
            return True
        elif answer == 'no':
            return False
        else:
            print('Please provide a valid answer')


while True:
    # Print an opening statement
    print('Welcome to BlackJack! Get as close to 21 as you can without going over!\n\
    Dealer hits until she reaches 17. Aces count as 1 or 11.')
    
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
    player_chips = Chips()  # remember the default value is 100    
    
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
        
        #while dealer_hand.value < 17:
        #    hit(deck,dealer_hand)    
    
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
    print("\nPlayer's winnings stand at",player_chips.total)

    if not replay():
        break
    
    '''
    # Ask to play again
    new_game = input("Would you like to play another hand? Enter 'y' or 'n' ")
    
    if new_game.lower()=='y':
        playing=True
        continue
    else:
        print("Thanks for playing!")
        break

        '''

