## Quick start Guide
    >> python -m venv ./                #activate virtual environment
    >> pip install click, time, json    
    >> python main.py                   # To start title screen

## Pieces legend 
- `P`: Pawn
- `R`: Rook
- `N`: Knight
- `B`: Bishop
- `Q`: Queen
- `K`: King

## Notable feature
1. A local PvP chess game - `Local multiplayer`
    - Features pieces move set preview (for self and opponent pieces)
        - The move preview also highlights pieces that can be captured
    - Ability to continue last game (type `E` during turn to exit to title and save game)
    - Feature a last move message in case player forget what move their opponent did just now
2. Player vs AI chess game - `Play with AI`
    - Player play against a negamax algorithm AI
    - Player can choose the AI difficulties level (beginner, normal)
    - Feature a last move message in case player forget what move AI did just now
    - Ability to undo last turn (type `U` during player's turn)
    - Ability to continue last game (type `E` during turn to exit to title and save game)
3. N Queen Puzzle - `N Queen`
    - Player can choose a 4x4 - 9x9 chessboard to play N Queen puzzle game on
    - Ability to continue last game (type `E` during turn to exit to title and save game)
4. AI vs AI - `AI vs AI`
    - Serve as a tech demo for the negamax AI
    - Player can choose the AI difficulties level on both sides (beginner, normal)
    - User can see the processing time and move the AI do
        - The refresh time is slowed down a minimum of 0.2s to allow user to see each move
## General Tips
1. Blue side goes first
2. You can type opponent piece coordinate to see their move set 
3. You can promote your pawn when it reaches its last rank 
4. There are no special moves like Castling, En Passant CaptureThere are a secret AI difficulties level 'hal9000' for `Play with AI` and `AI vs AI`, but the typical processing time is around 20s/

