# Solitaire Console Game

This is a console-based implementation of Solitaire, developed as a school project. The project was completed in one day and provides a basic framework for a Solitaire game, with some missing features.

## Features

- **Deck Initialization**: Creates a standard 52-card deck with suits and colors.
- **Shuffling**: Randomly shuffles the deck.
- **Dealing**: Deals cards to the tableau and stockpile.
- **Game Display**: Displays the current game state, including the tableau and a limited view of the stockpile.
- **Card Movements**: 
  - Move cards between tableau piles.
  - Draw cards from the stockpile.
  - Move stacks of cards between tableau piles.
- **User Input**: Accepts user commands to perform actions in the game.
- **Basic Win Condition Check**: Checks if the player has won the game.

## How to Play

1. **Setup**: The game initializes with a shuffled deck, dealing cards to the tableau and stockpile.
2. **User Input**: Enter commands to move cards:
   - `1 to 2` - Move a card from tableau pile 1 to tableau pile 2.
   - `draw` - Draw a card from the stockpile.
   - `stack 1 to 2 3` - Move a stack of 3 cards from tableau pile 1 to tableau pile 2.
   - `quit` - Exit the game.
3. **Objective**: Move all cards to foundation piles (currently not implemented) in ascending order from Ace to King.

## Current State

- The game is in an early, incomplete stage. The main missing feature is the implementation of the foundation piles (where cards are stacked in order from Ace to King for each suit). Without this, a true win condition is not possible.
- The user can move cards between tableau piles and draw cards from the stockpile, but no moves to foundation piles are possible.

## Missing Features and Future Improvements

1. **Foundation Piles**: Implement foundation piles to allow the player to stack cards in order from Ace to King by suit.
2. **Move Validation**: Improve the validation of moves, including checks for valid stacking (e.g., alternating colors in tableau piles).
3. **User Interface Enhancements**: 
   - Display more detailed game state, possibly with card faces.
   - Add more intuitive user commands.
4. **Additional Game Logic**: 
   - Implement a proper draw-three feature from the stockpile.
   - Add a scoring system.

## How to Run

1. Ensure Python and the `termcolor` library are installed.
2. Run the game with the following command:
   ```bash
   python solitaire.py
