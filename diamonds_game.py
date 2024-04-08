import pygame
import random

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Initialize Pygame
pygame.init()

# Set window size
width = 800
height = 600
screen = pygame.display.set_mode((width, height))

# Define card class (replace with card images later)
class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
    
    def draw(self, x, y):
        pygame.draw.rect(screen, WHITE, (x, y, 70, 100))
        font = pygame.font.Font(None, 32)
        text = f"{self.value}{self.suit}"
        text_surface = font.render(text, True, BLACK)
        screen.blit(text_surface, (x + 5, y + 5))

# Function to display player and AI cards
def draw_cards(player_cards, ai_cards, x_offset, y_offset, selected_card=None):
    for i, card in enumerate(player_cards):
        if card == selected_card:
            pygame.draw.rect(screen, GREEN, (x_offset + i * 80, y_offset, 70, 100))  # Highlight selected card
        else:
            card.draw(x_offset + i * 80, y_offset)
    for i, card in enumerate(ai_cards):
        pygame.draw.rect(screen, BLACK, (width - x_offset - (i + 1) * 80, y_offset, 70, 100))  # Hide AI cards

# Function to create a deck of cards
def create_deck():
    suits = ["Spades", "Hearts", "Clubs", "Diamonds"]
    values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    deck = []
    for suit in suits:
        for value in values:
            deck.append(Card(suit, value))
    return deck

# Simple AI function to choose a card (replace with more sophisticated logic)
def ai_choose_card(player_bid, ai_cards):
    # Choose a card with the same value as the player's bid (if available)
    for card in ai_cards:
        if card.value == player_bid.value:
            return card
    # If no matching value, choose a random card
    return random.choice(ai_cards)

# Function to determine the winning trick (replace with more logic)
def determine_winner(player_card, ai_card, current_diamond):
    # Check if either card is a Diamond
    if player_card.suit == "Diamonds" or ai_card.suit == "Diamonds":
        # Diamond wins, regardless of value
        return "Diamond"
    elif player_card.suit == current_diamond:
        # Player's suit matches current diamond, player wins
        return "Player"
    elif ai_card.suit == current_diamond:
        # AI's suit matches current diamond, AI wins
        return "AI"
    else:
        # Neither suit matches current diamond, higher card value wins
        if card_value_to_number(player_card.value) > card_value_to_number(ai_card.value):
            return "Player"
        else:
            return "AI"

# Function to convert card value to a number (replace with logic for face cards)
def card_value_to_number(value):
    try:
        return int(value)
    except ValueError:
        # Handle face cards (replace with appropriate values)
        if value == "J":
            return 11
        elif value == "Q":
            return 12
        elif value == "K":
            return 13
        else:
            return 14  # Placeholder for Ace

running = True
player_cards = []
ai_cards = []
deck = create_deck()
random.shuffle(deck)  # Shuffle deck
player_cards = deck[:5]  # Deal 5 cards to player
ai_cards = deck[5:10]  # Deal 5 cards to AI
current_diamond = None  # Initialize current diamond
player_tricks = 0  # Track player's won tricks
ai_tricks = 0  # Track AI's won tricks
selected_card =  None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if player clicked on their cards and handle selection
            pos = pygame.mouse.get_pos()
            x, y = pos
            if 50 < x < 50 + 70 * len(player_cards) and 100 < y < 200:
                card_index = (x - 50) // 80
                if 0 <= card_index < len(player_cards):
                    selected_card = player_cards[card_index]

    # Implement bidding logic based on selected card (placeholder)
    player_bid = selected_card
    print(f"Player bid: {player_bid.value}{player_bid.suit}")

    # AI chooses card
    if selected_card is not None:
        ai_chosen_card = ai_choose_card(player_bid, ai_cards)
        print(f"AI chose: {ai_chosen_card.value}{ai_chosen_card.suit}")


    # Determine the winning trick
    winner = determine_winner(player_card=player_bid, ai_card=ai_chosen_card, current_diamond=current_diamond)

    # Update current diamond if necessary (replace with more logic)
    if winner == "Diamond":
        # A Diamond was played, set it as the current diamond
        current_diamond = player_bid.suit if player_bid.suit == "Diamonds" else ai_chosen_card.suit
    elif winner == "Player":
        # Player won the trick, potentially update current diamond based on their card
        if player_bid.suit != current_diamond:
            current_diamond = player_bid.suit

    # Remove played cards
    player_cards.remove(selected_card)
    ai_cards.remove(ai_chosen_card)
    selected_card = None  # Reset selection for next round

    # Award trick to winner (update counts)
    if winner == "Player":
        player_tricks += 1
    elif winner == "AI":
        ai_tricks += 1

    # Check for game end conditions (replace with more logic)
    if len(player_cards) == 0 or len(ai_cards) == 0:
        # One player ran out of cards, declare winner
        if player_tricks > ai_tricks:
            print("Player Wins!")
        else:
            print("AI Wins!")
        running = False  # Set running to False to exit the loop

    # Update game state (e.g., display winner of the trick, update score)
    # ... (replace with your visualization and scorekeeping logic)

    # Draw UI elements
    screen.fill(WHITE)
    draw_cards(player_cards, ai_cards, 50, 100, selected_card)

    # Update display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
