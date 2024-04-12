import random
import os
from termcolor import colored

def initialize_deck():
    """
    Initialize a standard deck of cards with ranks and suits.

    Returns:
        list: A list of tuples representing the deck of cards, where each tuple is (rank, suit, color).
    """
    # Define ranks and suits for a standard deck of cards
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    suits = ['\u2665', '\u2666', '\u2663', '\u2660']  # Hearts, Diamonds, Clubs, Spades

    # Define colors for different suits
    suits_colors = {
        '\u2665': 'red',    # Hearts
        '\u2666': 'red',    # Diamonds
        '\u2663': 'blue',   # Clubs
        '\u2660': 'blue'    # Spades
    }

    # Create the deck of cards with ranks, suits, and colors
    deck = [(rank, suit, suits_colors[suit]) for rank in ranks for suit in suits]
    return deck

def shuffle_deck(deck):
    """
    Shuffle the deck of cards in place.

    Args:
        deck (list): A list of tuples representing the cards in the deck.
    """
    random.shuffle(deck)

def deal_cards(deck):
    """
    Deal cards from the deck to the tableau and stockpile.

    Args:
        deck (list): A list representing the deck of cards.

    Returns:
        dict: A dictionary representing the initial game state with tableau and stockpile.
    """
    # Initialize empty tableau and stockpile
    tableau = {}
    stockpile = []

    # Deal cards to tableau
    cards_per_pile = 1
    for i in range(1, 8):
        tableau[i] = deck[:cards_per_pile]
        deck = deck[cards_per_pile:]
        cards_per_pile += 1

    # Set the rest of the deck as the stockpile
    stockpile = deck

    # Return the initial game state
    return {'tableau': tableau, 'stockpile': stockpile}

def display_game_state(game_state):
    """
    Display the current game state including tableau piles and a limited view of the stockpile.

    Args:
        game_state (dict): A dictionary containing the current game state with tableau and stockpile.
    """
    # Determine the maximum number of cards in any tableau pile
    max_pile_size = max(len(cards) for cards in game_state['tableau'].values())

    # Print the labels for each pile, aligned with the tableau piles
    for pile in range(1, len(game_state['tableau']) + 1):
        print(f"{pile}".center(4), end=" ")
    print()

    # Display a line of dashes below the labels
    print("-" * (6 * len(game_state['tableau'])))

    # Print the tableau piles vertically
    for i in range(max_pile_size):
        for pile, cards in game_state['tableau'].items():
            if i < len(cards):
                # Pad each card representation with spaces to maintain alignment
                card_str = f"{cards[i][0]}{cards[i][1]}"
                print(f"{card_str.center(4)}", end=" ")
            else:
                # If the tableau pile has fewer cards, add empty space to maintain alignment
                print("    ", end=" ")
        print()

    # Display a limited view of the stockpile with only the top 3 cards visible
    stockpile_top = game_state['stockpile'][:3]
    hidden_card_count = len(game_state['stockpile']) - 3
    print("\nStockpile (Top 3 visible):")
    for card in stockpile_top:
        print(f"{card[0]}{card[1]}")
    if hidden_card_count > 0:
        print(f"({hidden_card_count} hidden)")

def move_card(source, destination, game_state):
    """
    Move a card from the source pile to the destination pile.

    Args:
        source (int or str): The source tableau pile (either an integer from 1 to 7 or 'stockpile').
        destination (int): The destination tableau pile (an integer from 1 to 7).
        game_state (dict): A dictionary containing the current game state with tableau and stockpile.

    Returns:
        dict: A dictionary containing the updated game state after the card has been moved.
    """
    if source == 'stockpile':
        # Move card from stockpile to destination tableau pile
        if game_state['stockpile']:
            card = game_state['stockpile'].pop(0)
            game_state['tableau'][destination].append(card)
        else:
            print("Stockpile is empty.")
    else:
        # Move card from source tableau pile to destination tableau pile
        if game_state['tableau'][source]:
            source_card = game_state['tableau'][source][-1]  # Get the top card from the source pile
            dest_pile = game_state['tableau'][destination]  # Get the destination pile

            # Check if the move is valid
            if not dest_pile or (source_card[0] == 'K' and dest_pile[-1][0] == 'A') or \
               (source_card[0] == 'Q' and dest_pile[-1][0] == 'K') or \
               (source_card[0] == 'J' and dest_pile[-1][0] == 'Q') or \
               (source_card[0] == '10' and dest_pile[-1][0] == 'J') or \
               (source_card[0] == '9' and dest_pile[-1][0] == '10') or \
               (source_card[0] == '8' and dest_pile[-1][0] == '9') or \
               (source_card[0] == '7' and dest_pile[-1][0] == '8') or \
               (source_card[0] == '6' and dest_pile[-1][0] == '7') or \
               (source_card[0] == '5' and dest_pile[-1][0] == '6') or \
               (source_card[0] == '4' and dest_pile[-1][0] == '5') or \
               (source_card[0] == '3' and dest_pile[-1][0] == '4') or \
               (source_card[0] == '2' and dest_pile[-1][0] == '3'):
                card = game_state['tableau'][source].pop()  # Remove the card from the source pile
                game_state['tableau'][destination].append(card)  # Add the card to the destination pile
            else:
                print("Invalid move: The card cannot be placed on the destination pile.")
        else:
            print(f"Pile {source} is empty.")
    
    return game_state

def move_stack(source, destination, stack_size, game_state):
    """
    Move a stack of cards from one tableau pile to another.

    Args:
        source (int): The source tableau pile from which to move the stack.
        destination (int): The destination tableau pile to which to move the stack.
        stack_size (int): The number of cards in the stack to move.
        game_state (dict): The current game state.

    Returns:
        tuple: A tuple containing the updated game state after the move and an error message if applicable.
    """
    # Check if the source and destination piles are within the valid range
    if source not in game_state['tableau'] or destination not in game_state['tableau']:
        return game_state, "Invalid source or destination pile."

    source_pile = game_state['tableau'][source]
    destination_pile = game_state['tableau'][destination]

    # Check if the stack size exceeds the number of cards in the source pile
    if stack_size > len(source_pile):
        return game_state, "Stack size exceeds the number of cards in the source pile."

    # Check if the stack can be moved to the destination
    if not source_pile or (destination_pile and source_pile[-stack_size][0] != str(int(destination_pile[-1][0]) - 1) or source_pile[-stack_size][1] == destination_pile[-1][1]):
        return game_state, "Invalid move. The stack cannot be moved to the destination."

    # Move the stack of cards to the destination pile
    stack_to_move = source_pile[-stack_size:]
    game_state['tableau'][destination] += stack_to_move
    game_state['tableau'][source] = source_pile[:-stack_size]

    return game_state, None

def draw_card(game_state):
    """
    Draw a card from the stockpile and add it to the tableau piles if possible.

    Args:
        game_state (dict): A dictionary containing the current game state with tableau and stockpile.

    Returns:
        dict: A dictionary containing the updated game state after drawing and moving the card.
    """
    # Check if the stockpile is empty
    if not game_state['stockpile']:
        print("Stockpile is empty.")
        return game_state

    # Draw a card from the stockpile
    card = game_state['stockpile'].pop(0)

    # Check if the card can be added to any tableau pile
    for pile, cards in game_state['tableau'].items():
        if not cards or (cards[-1][0] == 'K' and not cards[-1][1] == card[1]):
            game_state['tableau'][pile].append(card)
            return game_state

    # If no tableau pile is eligible, return the card to the stockpile
    game_state['stockpile'].insert(0, card)
    return game_state, "No tableau pile is eligible for the drawn card."

def check_win_condition(game_state):
    """
    Check if the player has won the game.

    Args:
        game_state (dict): A dictionary containing the current game state with tableau and stockpile.

    Returns:
        bool: True if the player has won the game, False otherwise.
    """
    # Define the correct order of ranks
    correct_order = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    
    # Check if each foundation pile contains all cards of a single suit in correct order
    for suit in ['\u2665', '\u2666', '\u2663', '\u2660']:  # Hearts, Diamonds, Clubs, Spades
        foundation_pile = [card[0] for pile in game_state['tableau'].values() for card in pile if card[1] == suit]
        if len(foundation_pile) != 13:
            return False
        if foundation_pile != correct_order:
            return False
    return True

def main():
    """
    Main function to run the game of solitaire.
    """
    # Initialize deck, shuffle, and deal cards
    deck = initialize_deck()
    shuffle_deck(deck)
    game_state = deal_cards(deck)

    # Main game loop
    while True:
        # Clear the terminal screen
        os.system('cls' if os.name == 'nt' else 'clear')

        # Display game state
        display_game_state(game_state)

        # Prompt player for action
        action = input("How to play: \n• e.g, '1 to 2' to move a card from pile 1 to pile 2 \n• 'draw' to draw from stockpile \n• 'stack 1 to 2 3' to move a stack of 3 cards from pile 1 to pile 2 \n• 'quit' to end game\nEnter your move: ").strip().lower()

        # Process player action
        if action == 'quit':
            print("Thanks for playing!")
            break
        elif action == 'draw':
            # Draw a card from the stockpile
            game_state, draw_error = draw_card(game_state)
            if draw_error:
                print(draw_error)
                input("Press Enter to continue...")
                continue
        elif action.startswith('stack'):
            # Move a stack of cards between tableau piles
            try:
                _, source, destination, stack_size = action.split()
                source, destination, stack_size = int(source), int(destination), int(stack_size)
            except ValueError:
                print("Invalid move format. Please enter 'stack <source> <destination> <stack_size>' to move a stack of cards between tableau piles.")
                input("Press Enter to continue...")
                continue

            # Move the stack of cards
            game_state, stack_move_error = move_stack(source, destination, stack_size, game_state)
            if stack_move_error:
                print(stack_move_error)
                input("Press Enter to continue...")
                continue

        else:
            # Split action into source and destination piles
            try:
                source, destination = map(int, action.split(' to '))
                if not (1 <= source <= 7 and 1 <= destination <= 7):
                    raise ValueError("Invalid source or destination pile number.")
            except ValueError:
                print("Invalid move format. Please enter '1 to 2' to move a card from pile 1 to pile 2.")
                input("Press Enter to continue...")
                continue
            
            # Move card between tableau piles
            game_state = move_card(source, destination, game_state)

        # Check win condition
        if check_win_condition(game_state):
            # Clear the terminal screen before displaying the winning message
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Congratulations! You win!")
            break

# Run the game
if __name__ == "__main__":
    main()
