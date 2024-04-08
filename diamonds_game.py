import pygame
import random
import os

pygame.init()
# Initialize Pygame
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set the screen dimensions
SCREEN_WIDTH = 1050
SCREEN_HEIGHT = 700

# Set desired card dimensions (adjusted for smaller size)
CARD_WIDTH = 80
CARD_HEIGHT = 112  # Adjusted proportionally based on CARD_WIDTH

# Set font
FONT = pygame.font.Font(None, 36)
# Dictionary mapping cards to their values
CARD_VALUES = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, '11': 11, '12': 12, '13': 13, '1': 14}

# Function to generate a unique random diamond card
def generate_diamond_card(remaining_cards, used_diamonds):
    while True:
        card = random.choice(remaining_cards)
        if card not in used_diamonds:
            used_diamonds.append(card)
            return card

def generate_computer_bid(computer_deck, revealed_diamonds):
    # Sort computer's deck based on card values
    sorted_computer_deck = sorted(computer_deck, key=lambda card: CARD_VALUES[card])

    # Find the optimal card to bid based on revealed diamond cards
    for card in sorted_computer_deck:
        if card not in revealed_diamonds:
            return card
    
    # If no optimal card found (unlikely due to revealed diamonds tracking)
    return sorted_computer_deck[0]  # Choose the lowest card as fallback

def load_card_images_suit(card_dir, suit):
    card_images = {}
    suit_dir = os.path.join(card_dir, suit)
    full_path = os.path.join(os.path.dirname(__file__), suit_dir)
    for card_file in os.listdir(full_path):
        if card_file.endswith(".png"):
            card_name = card_file.split('_')[1].split('.')[0]
            image_path = os.path.join(full_path, card_file)
            card_image = pygame.image.load(image_path).convert_alpha()
            scaled_card_image = pygame.transform.scale(card_image, (CARD_WIDTH, CARD_HEIGHT))
            card_images[card_name] = scaled_card_image
    return card_images

# Function to display text on the screen
def display_text(screen, text, position, color):
    text_surface = FONT.render(text, True, color)
    screen.blit(text_surface, position)

# Main function to run the game
def main():
    # Initialize screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Diamonds Game")

    # Initialize game variables
    diamond_cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '1']
    player_deck = diamond_cards.copy()
    computer_deck = diamond_cards.copy()
    player_score = 0
    computer_score = 0
    round_number = 1
    used_diamonds = []

    running = True
    # Main game loop
    while diamond_cards:
        
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Diamonds Game")

        if not(diamond_cards):
            break
        current_diamond = generate_diamond_card(diamond_cards, used_diamonds)
        # Clear the screen
        screen.fill(WHITE)

        diamond_images = load_card_images_suit("cards", "diamonds")
        spade_images = load_card_images_suit("cards", "spades")
        club_images = load_card_images_suit("cards", "clubs")
        current_diamond_image = diamond_images.get(str(current_diamond), None)
        
        if current_diamond_image:
            screen.blit(current_diamond_image, (SCREEN_WIDTH // 2 - CARD_WIDTH // 2, SCREEN_HEIGHT // 2 - CARD_HEIGHT // 2))

        card_spacing = 2
        # Display text asking for player's bid
        display_text(screen, "Choose a card to bid:", (10, SCREEN_HEIGHT), BLACK)

        
        for i, card in enumerate(player_deck):
            card_image = spade_images.get(card, None)
            if card_image:
                card_x = i * (CARD_WIDTH - card_spacing)  # Adjusted spacing between cards
                card_x = min(card_x, SCREEN_WIDTH - CARD_WIDTH)  # Ensure cards fit within screen width
                screen.blit(card_image, (card_x, SCREEN_HEIGHT - CARD_HEIGHT + 20))
                
        for i, card in enumerate(computer_deck):
            card_image = club_images.get(card, None)
            if card_image:
                card_x = i * (CARD_WIDTH - card_spacing)  # Adjusted spacing between cards
                card_x = min(card_x, SCREEN_WIDTH - CARD_WIDTH)  # Ensure cards fit within screen width
                screen.blit(card_image, (card_x, SCREEN_HEIGHT - CARD_HEIGHT - 500))

        
        display_text(screen, f"Player Score: {player_score}", (10, 10), BLACK)
        display_text(screen, f"Computer Score: {computer_score}", (10, 50), BLACK)
        pygame.display.flip()

        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if SCREEN_HEIGHT - CARD_HEIGHT <= mouse_y <= SCREEN_HEIGHT:
                        selected_card_index = (mouse_x // CARD_WIDTH) % len(player_deck)
                        selected_card = player_deck.pop(selected_card_index)

                        computer_card = generate_computer_bid(computer_deck, used_diamonds)
                        computer_deck.remove(computer_card)
                        
                        # Determine winner of the round and update scores
                        if CARD_VALUES[computer_card[0]] > CARD_VALUES[selected_card[0]]:
                            computer_score += CARD_VALUES[current_diamond]
                            text = "Computer Won this round"
                        elif CARD_VALUES[computer_card[0]] == CARD_VALUES[selected_card[0]]:
                            computer_score += CARD_VALUES[current_diamond]//2
                            player_score += CARD_VALUES[current_diamond]//2
                            text = "This round is a tie"
                        else:
                            player_score += CARD_VALUES[current_diamond]
                            text = "You won this round"

                        # Display computer's bid and round result
                        display_text(screen, f"Computer's bid: {computer_card}   You bid: {selected_card}", (10, SCREEN_HEIGHT - 200), BLACK)
                        display_text(screen, text, (10, SCREEN_HEIGHT - 250), BLACK)
                        pygame.display.flip()
                        pygame.time.delay(3000)
                break

        # Update round number
        round_number += 1

    # Display final scores and winner
    screen.fill(WHITE)
    display_text(screen, f"Player Score: {player_score}", (10, 10), BLACK)
    display_text(screen, f"Computer Score: {computer_score}", (10, 50), BLACK)

    if player_score > computer_score:
        text = "You won!"
    elif player_score == computer_score:
        text = "It's a tie!"
    else:
        text = "Computer won!"
    
    display_text(screen, text, (300, 300), BLACK)

    pygame.display.flip()
    # Quit Pygame

    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:    
            pygame.quit()
            break

if __name__ == "__main__":
    main()
