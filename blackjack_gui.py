# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
player = ''
dealer = ''
deck = ''
result = ''

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.hand_list = []

    def __str__(self):
        card_string = 'Hand is: '
        for card in self.hand_list:
            card_string = card_string + str(card) + ' '
        return card_string

    def add_card(self, card):
        self.hand_list.append(card)

    def get_value(self):
        self.hand_value = 0
        
        # rank_list to determine if 'A' in hand
        rank_list = [card.get_rank() for card in self.hand_list]
        for item in rank_list:
            self.hand_value += VALUES[item]
        
        # 'A' logic flow
        if 'A' not in rank_list:
            return self.hand_value
        else:
            if self.hand_value + 10 <= 21:
                return self.hand_value + 10
            else:
                return self.hand_value
                
   
    def draw(self, canvas, pos):
        i = 0
        for card in self.hand_list:
            card.draw(canvas, [pos[0] + (i*(80)), pos[1]])
            i += 1
        
# define deck class 
class Deck:
    def __init__(self):
        self.deck_list = [(suit + rank) for suit in SUITS for rank in RANKS]

    def shuffle(self):
        random.shuffle(self.deck_list)

    def deal_card(self):
        c = self.deck_list[-1]
        self.deck_list.pop()
        return Card(c[0], c[1])

    def __str__(self):
        return 'Deck list: ' + str(self.deck_list)


#define event handlers for buttons
def deal():
    global outcome, in_play, player, dealer, deck, score, result
    
    if in_play == True:
        score -= 1
    
    deck = Deck()
    deck.shuffle()
    print(deck)
    
    player = Hand()
    dealer = Hand()

    # alternate dealing between player and dealer
    player.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    player.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    
    result = ''
    
    in_play = True

def hit():
    global score, in_play, player, dealer, deck, result
    if in_play:
        player.add_card(deck.deal_card())
        
        # If player exceeds 21 after draw, pass. In play false
        if player.get_value() > 21:
            result = 'Player busted!'
            in_play = False
            score -= 1
    else:
        pass
       
def stand():
    global in_play, outcome, player, dealer, deck, score, result
    
    if in_play == False:
        if player.get_value() > 21:
            result = 'Player busted!'
        else:
            pass
    else:
        while dealer.get_value() < 17:
            dealer.add_card(deck.deal_card())
            
        # check results of dealer vs player and update score
        if dealer.get_value() > 21:
            result = 'Dealer has busted.'
            score += 1
        else:
            if dealer.get_value() < player.get_value():
                result = 'Player wins.'
                score += 1
            elif dealer.get_value() > player.get_value():
                result = 'Dealer wins.'
                score -= 1
            else:
                result = 'Draw. Dealer wins.'
                score -= 1

    in_play = False
   

def draw(canvas):

    player.draw(canvas, [40, 400])
    dealer.draw(canvas, [40, 200])

    # print outcome statement based on game state and cover dealer hole card 
    outcome = ''
    dealer_exposed = VALUES[dealer.hand_list[1].get_rank()]
    if in_play == True:
        outcome = 'Hit or stand?'
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [40 + CARD_BACK_CENTER[0],
                                                                        200 + CARD_BACK_CENTER[1]],
                                                                        CARD_BACK_SIZE)
        canvas.draw_text("DEALER'S HAND: " + str(dealer_exposed), [40, 180], 20, 'white')
    else:
        outcome = 'New deal?'
        canvas.draw_text("DEALER'S HAND: " + str(dealer.get_value()), [40, 180], 20, 'white')

    # other draw text statements
    canvas.draw_text("BLACKJACK", [220, 60], 30, 'red')    
    canvas.draw_text("PLAYER'S HAND: " + str(player.get_value()), [40, 380], 20, 'white')
    canvas.draw_text("Action: " + outcome, [100, 120], 20, 'white')
    canvas.draw_text("Score: " + str(score), [350, 120], 20, 'white')
    canvas.draw_text("Result: " + str(result), [350, 160], 20, 'white')



# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

deal()
frame.start()


# remember to review the gradic rubric
