# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
score1 = 0
score2 = 0
P_X = 10
P_Y = 340
D_X = 10
D_Y = 150


# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        self.suit=suit
        self.rank=rank
        

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    #draw the card_image
    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
     
    #draw the card_back
    def drawb(self, canvas, pos):
        
        canvas.draw_image(card_back, CARD_BACK_CENTER , CARD_BACK_SIZE, [pos[0] + CARD_BACK_CENTER[0], pos[1] + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)


# define hand class
class Hand:
    def __init__(self):
        self.hand = []
    
    def __str__(self):
        hand = ''
        for item in self.hand:
            hand = hand + " "+ str(item)
        return hand
    
    def add_card(self, card):
        self.hand.append(card)
        return self.hand
    
    def get_value(self):
        has_A = False
        v = 0
        for item in self.hand:
            v += VALUES[item.get_rank()]
        for item in self.hand:  
            if item.get_rank() == 'A':
                if v + 10 <= 21 :
                    v = v + 10   
        return v
    
    #draw the player card in play and both sides after paly
    # pos here is a list
    def draw(self, canvas, pos):
        i = 0
        for item in self.hand:
            item.draw(canvas, pos[i])
            i += 1
            
    #draw the dealer card in play
    def drawb(self, canvas, pos):
        the_first = True
        j = 1
        for item in self.hand:
            #the first did not show 
            if the_first :
               item.drawb(canvas, pos[0])
               the_first = False
            else :
               item.draw(canvas, pos[j])
               j += 1
                

class Deck:
    def __init__(self):
        # create a Deck object
        self.deck = []
        for i in SUITS:
            for j in RANKS:
                self.deck.append( i+j )
               
    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck)    # use random.shuffle()

    def deal_card(self):
        #return the Card object
        m = random.randrange(0,len(self.deck))
        t= self.deck.pop(m)
        return Card(t[0],t[1])
    
    def __str__(self):
        return str(self.deck)# return a string representing

#define event handlers for buttons
def deal():
    global outcome2, outcome1, p_hand, d_hand, dk , outcome
    global add_p_pos, add_d_pos, p_pos, d_pos
    global in_play, score1
    
    if not in_play:
      add_p_pos = 2
      add_d_pos = 2
      p_pos = [[P_X, P_Y],[P_X + 100, P_Y]]
      d_pos = [[D_X, D_Y],[D_X + 100, D_Y]]
      d_hand = Hand()
      p_hand = Hand()
      dk = Deck()
      dk.shuffle()
      for i in range(2):
         d_hand.add_card(dk.deal_card())
         p_hand.add_card(dk.deal_card())

      outcome2 = "Hit or stand ?"
      outcome1 = ""
      outcome =""
      in_play = True 
            
      state = 1
            
    else:
          outcome1 = "You deal in play.Lose"
          outcome2 = ""
          outcome = str(d_hand.get_value())+":"+str(p_hand.get_value())
          score1 += 1
          in_play = False
        
     
    
def hit():
   # if the hand is in play, hit the player
   # if busted, assign a message to outcome, update in_play and score
    global outcome1,outcome2, in_play, score1, outcome
    
    if in_play:
        global add_p_pos
        p_hand.add_card(dk.deal_card())
        p_pos.append([P_X + add_p_pos * 100, P_Y])
        add_p_pos += 1
        if p_hand.get_value() > 21 :
           outcome1 = "You went bust and lose"
           outcome2 = "New deal ?"
           outcome  = str(d_hand.get_value())+":"+str(p_hand.get_value())
           score1 += 1
           in_play = False
        else :
           outcome2 = "Hit or stand ?"
    
      
def stand():
   # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
   # assign a message to outcome, update in_play and score
    global outcome1, outcome2, in_play,score1, score2, outcome
    
    if in_play :
        global add_d_pos
        while d_hand.get_value() < 17:
            d_hand.add_card(dk.deal_card())
            d_pos.append([D_X + add_d_pos * 100, D_Y])
            add_d_pos += 1
        
        if d_hand.get_value() > 21:
            outcome1 = "You win! The dealer bust!"
            score2 += 1
        else:
            if d_hand.get_value() > p_hand.get_value():
                outcome1 = "You lose" 
                score1 += 1
            elif d_hand.get_value() < p_hand.get_value():
                outcome1 = "You win!" 
                score2 += 1
            else:
                outcome1 = "It is a tie"
                score1 += 1
        outcome=str(d_hand.get_value())+":"+str(p_hand.get_value())      
    in_play = False
    outcome2 = "New deal?"            
            

# draw handler    
def draw(canvas):
    canvas.draw_text('Blackjack',[10,80],50,'Black')
    canvas.draw_text('dealer',[10,140],30,'Black')
    canvas.draw_text('player',[10,330],30,'Black')
    canvas.draw_text(outcome2,[200,330],30,'Black')
    canvas.draw_text(outcome1,[200,140],30,'Black')
    canvas.draw_text(outcome ,[250,500],60,'Blue')
    canvas.draw_text("Dealer "+str(score1) + " : " +" Player "+str(score2),[300,80],30,'Red')
    
    p_hand.draw(canvas,p_pos)
    if in_play:
        d_hand.drawb(canvas,d_pos)
    else :
        d_hand.draw(canvas,d_pos)
        
# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()

