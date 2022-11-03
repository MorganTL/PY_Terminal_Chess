## Quick start Guide
    >> pip install click, time, json    # Only if you run it on bare metal
    >> python main.py                   # To start title screen

## Pieces legend 
- P: Pawn
- R: Rook
- N: Knight
- B: Bishop
- Q: Queen
- K: King

## Main feature
1. A local PvP chess game - `Local multiplayer`
    - Features pieces move set preview (for self and oppoent pieces)
        - The move preview also highlight pieces that can be capture
    - Ability to continue last game (type `E` during turn to exit to title and save game)
    - Feature a last move message incase player forget what move their oppoent did just now
2. Player vs AI chess game - `Play with AI`
    - Player play against a negamax algorithm AI
    - Player can choose the AI difficulties level (beginner, normal)
    - Feature a last move message incase player forget what move AI did just now
    - Ablility to undo last turn (type `U` during player turn)
    - Ability to continue last game (type `E` during turn to exit to title and save game)
3. N Queen Puzzle - `N Queen`
    - Player can choose a 4x4 - 9x9 chessboard to play N Queen puzzle game on
    - Ability to continue last game (type `E` during turn to exit to title and save game)
4. AI vs AI - `AI vs AI`
    - Serve as a tech demo for the negamax AI
    - Player can choose the AI difficulties level on both side (beginner, normal)
    - User can see the processing time and move the AI do
        - The refresh time is slow down a minimum of 0.2s to allow user to see each move
## General Tips
1. Blue side go first
2. You can type opponent piece coordinate to see their move set 
3. You can promote your pawn when it reach its last rank 
4. There are no special move like Castling, En Passant Capture
5. There is a secret AI difficulties level 'hal9000' for `Play with AI` and `AI vs AI`, but the typical processing time is around 20s/

