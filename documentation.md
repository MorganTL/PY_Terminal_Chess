# Documentation

>Highly recommended to read this file in a markdown reader

## Quick start Guide
    >> pip install click, time, json
    >> python main.py 

## Package used
1. `click` - for text styling in terminal and interact with terminal
2. `time` - for time.time() function
3. `json` - for saving game data in json format



# File structure

    .
    ├── main.py
    ├── readme.txt
    ├── documentation.md
    └───src
        ├── __init__.py
        ├── chess.py
        ├── local_play.py
        ├──  ai_play.py
        ├──  ai_vs_ai.py
        ├──  n_queen.py
        ├──  test.py
        └───save_file
            ├── ai_play.json
            ├── local_play.json
            ├── n_queen.json

## `Main.py`
- Host the title screen and allow player to select which mode to play in
    - Main title loop: selection of game mode
    - Sub title loop: selection of starting a new game or use pervious save data         
- Directly call functions from other files
    - `src.play_locally()`: start Player vs Player game loop (option to use pervious save data )
    - `src.play_with_AI`: start Player vs AI game loop (option to use pervious save data )
    - `src.play_n_queen()`: start N Queen puzzle game loop (option to use pervious save data )
    - `src.AI_vs_AI()`: start AI tech demo game loop

## `__init__`
- Make directory containing other python files as modules.

## `src/chess.py`
- Contains the `game_board` class: 
    - `make_board()`: generate size x size game board
    - `move_gen_xyz()`: generate all the legal move set of piece xyz
    - `move_generator()`: sister function that call move_gen_xyz
    - `print_board()`: print the game board
    - `print_board_moves_visualize()`: print game board and visualize the move of a piece
    - `avail_moves()`: all the available moves that player red or blue can do
    - `move_piece()`: teleport piece from_pos -> to_pos, does not provide move legal checking
    - `pawn_promotion_pos()`: return a list of pawn can be promoted by player red or blue
    - `pawn_promote()`: promote a pawn at a specify position
    - `undo()`: restore board to last X turns
    - ` king_is_dead()`: return True when one of the king is captured

## `src/local_play.py`
- Contain the singleplayer chess game
- `local_play` class will inherit `game_board` class from `chess.py`
- New class method include:
    - `start_game()`: start the Player_vs_Player gameplay loop
    - `ask_for_blue_name()`: blue player can select their name and confirm it
    - `ask_for_red_name()`: red player can select their name and confirm it
    - `move_piece()`: modify the json save file location to avoid overwriting other game mode savedata

## `src/ai_play.py`
- Import `chess.py`
- `chess_with_AI` class will inherit `game_board` class from `chess.py`
- New class method include:
    - `start_game()`: start the Player_vs_AI gameplay loop
    - `ask_for_AI_difficulties()`: player can select difficulties from 
        - beginner -> depth = 1
        - normal -> depth = 3
        - hal9000 -> depth = 5 (secret mode)
    - `ask_for_player_side()`: player can select which side to play on
    - `gen_eval_funcion()`: provide evaluation score of the game board
    - `negamax_eval()`: negamax algorithm that used score from - `gen_eval_funcion()`
    - `AI_turn`: use result from `negamax_eval()` to move pieces
    - `move_piece()`: modify the json save file location to avoid overwriting other game mode savedata


## `src/ai_vs_ai.py`
- A tech demo of the negamax chess AI
    - `start_AI_vs_AI()`: start AI_vs_AI gameplay loop
    - `move_piece()`: remove the gamefile saving function

## `src/n_queen.py` 
- Contain N Queen chessboard puzzle game
- 'n_queen' class will inherit `game_board` class from `chess.py`
- New class method include:
    - `start_game()`: start the N Queen puzzle gameplay loop
    - `ask_for_board_size()`: player can select the board size (4x4-9x9) as n = 2, 3 dont have any solution. And a >9x9 board is hard to play in terminal
    - `print_board_n_queen()`: modify `print_board()` to allow different color of each queen. It also combin `print_board_moves_visualize()` to highlight Queens that threaten each other
    - `move_piece()`: modify the json save file location to avoid overwriting other game mode savedata


## `src/save_file`
- This folder hold all the json save files produced during gameplay
