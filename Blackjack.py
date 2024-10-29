from random import shuffle, randint

# Constants
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'King', 'Queen', 'Ace')
values = {
    'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7,
    'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10,
    'Ace': 11
}

class WrongInput(Exception):
    pass

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]
        
    def __str__(self):
        return self.rank + ' of ' + self.suit
    
class Deck:
    def __init__(self):
        self.all_cards = [Card(suit, rank) for suit in suits for rank in ranks]
    
    def shuffle(self):
        shuffle(self.all_cards)
        
    def deal_one(self):
        return self.all_cards.pop() if self.all_cards else None
    
class Dealer:
    def __init__(self, name):
        self.name = name
        self.all_cards = []
        
    def dealer_choice(self):
        return randint(1, 2)  # 1 for hit, 2 for stay
    
    def dealer_hit_stay(self, new_card):
        choice = self.dealer_choice()
        if choice == 1:
            self.all_cards.append(new_card)
                
    def __str__(self):
        if len(self.all_cards) >= 2:
            hidden_hand = ['*' * len(str(self.all_cards[1]))] + [str(self.all_cards[0])]
            return f"Dealer's hand: {hidden_hand}"
        return str(self.all_cards)
    
    def score(self):
        total_score = 0
        aces = 0
        for card in self.all_cards:
            total_score += card.value
            if card.rank == 'Ace':
                aces += 1
        
        while total_score > 21 and aces:
            total_score -= 10
            aces -=1
            
        return total_score

class Player:
    def __init__(self, name):
        self.name = name
        self.all_cards = []
        
    def player_choice(self):
        choice = input('1. Hit to receive another card. \n2. Stay with current cards: ')
        while choice not in ['1', '2']:
            try:
                raise WrongInput('Invalid input. Please choose 1 or 2.')
            except WrongInput as e:
                print(e)
                choice = input('1. Hit to receive another card. \n2. Stay with current cards: ')
        return choice

    def player_hit(self, new_card):
        self.all_cards.append(new_card)
                
    def __str__(self):
        
        cards_str = ', '.join([str(card) for card in self.all_cards])  # Convert each card to a string
        return f"{self.name}'s hand: {cards_str}."
    
    def score(self):
        total_score = 0
        aces = 0
        for card in self.all_cards:
            total_score += card.value
            if card.rank == 'Ace':
                aces += 1
        
        while total_score > 21 and aces:
            total_score -= 10
            aces -=1
            
        return total_score

game_on = True
my_deck = Deck()
my_deck.shuffle()
dealer = Dealer('Machine')
player = Player('Jose')
player_turn = True
dealer_turn = False  
first_round = True

while game_on:\
    
    while player_turn:
        if first_round:
            
            for x in range(2):
                player.player_hit(my_deck.deal_one())
                dealer.dealer_hit_stay(my_deck.deal_one())
            
            first_round = False
            print(player)
            
            print(dealer)
        else:
            action = input("Do you want to 'hit' or 'stay'? ").lower()
            
            if action == 'hit':
                player.player_hit(my_deck.deal_one())
                print(player)
                
                player_total_score = player.score()
                if player_total_score > 21:
                    print("DEALER WINS DUE TO PLAYER'S BAD LUCK")
                    game_on = False
                    player_turn = False  
            elif action == 'stay':
                print('Player stays.')
                print(player)
                player_total_score = player.score()
                player_turn = False  
                dealer_turn = True   
                
                if player_total_score == 21:
                    print('PLAYER WINS!')
                    game_on = False
                elif player_total_score > 21:
                    print("DEALER WINS DUE TO PLAYER'S BAD LUCK")
                    game_on = False
            else:
                print('Invalid input, please choose "hit" or "stay".')

    
    while dealer_turn and game_on:
        
        print("Dealer's turn:")
        print(f"Dealer reveals hidden card: {', '.join([str(card) for card in dealer.all_cards])}")
        
        choice = dealer.dealer_choice()
        
        if choice == 1:  
            dealer.dealer_hit_stay(my_deck.deal_one())
            print(dealer)
            
            dealer_total_score = dealer.score()
            if dealer_total_score > 21:
                print("PLAYER WINS DUE TO DEALER'S BAD LUCK")
                game_on = False
                dealer_turn = False  
        elif choice == 2:  
            print('Dealer stays.')
            print(dealer)
            dealer_total_score = dealer.score()
            dealer_turn = False  
            
            if dealer_total_score == 21:
                print('DEALER WINS!')
                game_on = False
            elif dealer_total_score > 21:
                print("PLAYER WINS DUE TO DEALER'S BAD LUCK")
                game_on = False

    if not game_on:
        break
