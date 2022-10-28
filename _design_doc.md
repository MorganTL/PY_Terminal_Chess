# Design doc

## Quick start Guide
    >> pip install click, time
    >> python main.py

## Package used
1. **click** - for text styling in terminal and interact with terminal
2. **time** - for time.sleep() function

## Best practice
- Always command your code!!!
- Remember to use return in function 
- Remember to write test cases for your code
- Don't use global variable, try to use Object Oriented Programming (OOP)


# File structure

## Main.py
- This file will host the title screen and allow player to select which mode to play in

## chess.py
- This file will contain the game_board class and its functions including
    - **print_board** and **print_board_moves_visualize** (100% Done)    
    - **move_gen_xyz**: detect the move of xyz piece is legal or not (100% Done)
    - etc
- TODO:
    - **move_gen_castling**: detect valid castling move when move_gen is called for Rook and king
    - **move_piece**: return True when move is successful
    - **undo**: undo perious gameboard state (store at most 3 turns)

## local_play.py
- This file will import chess.py and contain the local multiple chess game
- TODO:
    - import chess.py game_board and setup while gameloop

## AI_play.py
- TBD, this will contain the singleplayer chess game
- TODO:
    - Add DFS algo for AI

## queen_game.py 
- This is the same as in assignment

## warpship_chessboard.py
- This is simlar to how warship players out but on a chess board?