from src.chess import game_board

import click, json, time



class chess_with_AI(game_board):
    def __init__(self, size: int, cache_size: int = 6, AI_side:str = "B"):
        super().__init__(size, cache_size)
        self.AI_side = AI_side
        self.AI_depth = 3
        self.AI_last_move = []

        # To optimize run time, the Piece-Square Tables are store in the class instead
        # The table is provided by https://www.chessprogramming.org/Piece-Square_Tables
        self.pawn_table = {
            'A8': 0, 'B8': 0, 'C8': 0, 'D8': 0, 'E8': 0, 'F8': 0, 'G8': 0, 'H8': 0,
            'A7': 50, 'B7': 50, 'C7': 50, 'D7': 50, 'E7': 50, 'F7': 50, 'G7': 50, 'H7': 50,
            'A6': 10, 'B6': 10, 'C6': 20, 'D6': 30, 'E6': 30, 'F6': 20, 'G6': 10, 'H6': 10,
            'A5': 5, 'B5': 5, 'C5': 10, 'D5': 25, 'E5': 25, 'F5': 10, 'G5': 5, 'H5': 5,
            'A4': 0, 'B4': 0, 'C4': 0, 'D4': 20, 'E4': 20, 'F4': 0, 'G4': 0, 'H4': 0,
            'A3': 5, 'B3': -5, 'C3': -10, 'D3': 0, 'E3':0, 'F3': -10, 'G3': -5, 'H3': 5,
            'A2': 5, 'B2': 10, 'C2': 10, 'D2': -20, 'E2': -20, 'F2': 10, 'G2': 10, 'H2': 5,
            'A1': 0, 'B1': 0, 'C1': 0, 'D1': 0, 'E1': 0, 'F1': 0, 'G1': 0, 'H1': 0
        }
        self.knight_table = {
            'A8': -50, 'B8': -40, 'C8': -30, 'D8': -30, 'E8': -30, 'F8': -30, 'G8': -40, 'H8': -50,
            'A7': -40, 'B7': -20, 'C7': 0, 'D7': 0, 'E7': 0, 'F7': 0, 'G7': -20, 'H7': -40,
            'A6': -30, 'B6': 0, 'C6': 10, 'D6': 15, 'E6': 15, 'F6': 10, 'G6': 0, 'H6': -30,
            'A5': -30, 'B5': 5, 'C5': 15, 'D5': 20, 'E5': 20, 'F5': 15, 'G5': 5, 'H5': -30,
            'A4': -30, 'B4': 0, 'C4': 15, 'D4': 20, 'E4': 20, 'F4': 15, 'G4': 0, 'H4': -30,
            'A3': -30, 'B3': 5, 'C3': 10, 'D3': 15, 'E3': 15, 'F3': 10, 'G3': 5, 'H3': -30,
            'A2': -40, 'B2': -20, 'C2': 0, 'D2': 5, 'E2': 5, 'F2': 0, 'G2': -20, 'H2': -40,
            'A1': -50, 'B1': -40, 'C1': -30, 'D1': -30, 'E1': -30, 'F1': -30, 'G1': -40, 'H1': -50
        }
        self.bishop_table = {
            'A8': -20, 'B8': -10, 'C8': -10, 'D8': -10, 'E8': -10, 'F8': -10, 'G8': -10, 'H8': -20,
            'A7': -10, 'B7': 0, 'C7': 0, 'D7': 0, 'E7': 0, 'F7': 0, 'G7': 0, 'H7': -10,
            'A6': -10, 'B6': 0, 'C6': 5, 'D6': 10, 'E6': 10, 'F6': 5, 'G6': 0, 'H6': -10,
            'A5': -10, 'B5': 5, 'C5': 5, 'D5': 10, 'E5': 10, 'F5': 5, 'G5': 5, 'H5': -10,
            'A4': -10, 'B4': 0, 'C4': 10, 'D4': 10, 'E4': 10, 'F4': 10, 'G4': 0, 'H4': -10,
            'A3': -10, 'B3': 10, 'C3': 10, 'D3': 10, 'E3': 10, 'F3': 10, 'G3': 10, 'H3': -10,
            'A2': -10, 'B2': 5, 'C2': 0, 'D2': 0, 'E2': 0, 'F2': 0, 'G2': 5, 'H2': -10,
            'A1': -20, 'B1': -10, 'C1': -10, 'D1': -10, 'E1': -10, 'F1': -10, 'G1': -10, 'H1': -20
        }
        self.rook_table = {
            'A8': 0, 'B8': 0, 'C8': 0, 'D8': 0, 'E8': 0, 'F8': 0, 'G8': 0, 'H8': 0,
            'A7': 5, 'B7': 10, 'C7': 10, 'D7': 10, 'E7': 10, 'F7': 10, 'G7': 10, 'H7': 5,
            'A6': -5, 'B6': 0, 'C6': 0, 'D6': 0, 'E6': 0, 'F6': 0, 'G6': 0, 'H6': -5,
            'A5': -5, 'B5': 0, 'C5': 0, 'D5': 0, 'E5': 0, 'F5': 0, 'G5': 0, 'H5': -5,
            'A4': -5, 'B4': 0, 'C4': 0, 'D4': 0, 'E4': 0, 'F4': 0, 'G4': 0, 'H4': -5,
            'A3': -5, 'B3': 0, 'C3': 0, 'D3': 0, 'E3': 0, 'F3': 0, 'G3': 0, 'H3': -5,
            'A2': -5, 'B2': 0, 'C2': 0, 'D2': 0, 'E2': 0, 'F2': 0, 'G2': 0, 'H2': -5,
            'A1': 0, 'B1': 0, 'C1': 0, 'D1': 5, 'E1': 5, 'F1': 0, 'G1': 0, 'H1': 0
        }
        self.queen_table = {
            'A8': -20, 'B8': -10, 'C8': -10, 'D8': -5, 'E8': -5, 'F8': -10, 'G8': -10, 'H8': -20,
            'A7': -10, 'B7': 0, 'C7': 0, 'D7': 0, 'E7': 0, 'F7': 0, 'G7': 0, 'H7': -10,
            'A6': -10, 'B6': 0, 'C6': 5, 'D6': 5, 'E6': 5, 'F6': 5, 'G6': 0, 'H6': -10,
            'A5': -5, 'B5': 0, 'C5': 5, 'D5': 5, 'E5': 5, 'F5': 5, 'G5': 0, 'H5': -5,
            'A4': 0, 'B4': 0, 'C4': 5, 'D4': 5, 'E4': 5, 'F4': 5, 'G4': 0, 'H4': -5,
            'A3': -10, 'B3': 5, 'C3': 5, 'D3': 5, 'E3': 5, 'F3': 5, 'G3': 0, 'H3': -10,
            'A2': -10, 'B2': 0, 'C2': 5, 'D2': 0, 'E2': 0, 'F2': 0, 'G2': 0, 'H2': -10,
            'A1': -20, 'B1': -10, 'C1': -10, 'D1': -5, 'E1': -5, 'F1': -10, 'G1': -10, 'H1': -20
        }
        self.king_table = {
            'A8': -30, 'B8': -40, 'C8': -40, 'D8': -50, 'E8': -50, 'F8': -40, 'G8': -40, 'H8': -30,
            'A7': -30, 'B7': -40, 'C7': -40, 'D7': -50, 'E7': -50, 'F7': -40, 'G7': -40, 'H7': -30,
            'A6': -30, 'B6': -40, 'C6': -40, 'D6': -50, 'E6': -50, 'F6': -40, 'G6': -40, 'H6': -30,
            'A5': -30, 'B5': -40, 'C5': -40, 'D5': -50, 'E5': -50, 'F5': -40, 'G5': -40, 'H5': -30,
            'A4': -20, 'B4': -30, 'C4': -30, 'D4': -40, 'E4': -40, 'F4': -30, 'G4': -30, 'H4': -20,
            'A3': -10, 'B3': -20, 'C3': -20, 'D3': -20, 'E3': -20, 'F3': -20, 'G3': -20, 'H3': -10,
            'A2': 20, 'B2': 20, 'C2': 0, 'D2': 0, 'E2': 0, 'F2': 0, 'G2': 20, 'H2': 20,
            'A1': 20, 'B1': 30, 'C1': 10, 'D1': 0, 'E1': 0, 'F1': 10, 'G1': 30, 'H1': 20
        }
        self.material_dicts = {
            "P" : 100,
            "N" : 320,
            "B" : 330,
            "R" : 500,
            "Q" : 900,
            "K" : 20000
        }

    def start_game(self, use_save_data = False, Test_mode = False):
        """
        1) Load perious save file (if use_save_data == True)
        2) ask AI difficulties
        3) ask Player to choose a side
        4) Main gameplay loop
        5) Exit game and save or empty save file when one player win           
        """
        if self.size != 8:
            raise ValueError(f"Game board size must be 8x8 (Current size = {self.size}x{self.size})")

        if use_save_data:
            # assume AI already did its move, no need to call AI_turn again
            data = json.load(open("./src/save_file/ai_play.json"))
            self.AI_side = data["AI_side"]
            self.AI_depth = data["AI_depth"]
            self.game_board = data["game_board"].copy()
        elif Test_mode:
            self.AI_side = "R"
        else:
            click.clear()
            self.print_board()
            self.ask_for_AI_difficulties()
            self.ask_for_player_side()
            #override save data
            data = {"game_board": self.game_board.copy(), "AI_side" : self.AI_side, "AI_depth" : self.AI_depth}
            json.dump(data, open("./src/save_file/ai_play.json", "w"))
            # Blue AI make the first move
            if self.AI_side == "B":
                self.AI_turn(self.AI_side, self.AI_depth)
        
        # Prepare local variable
        player_name = "Red" if  self.AI_side == "B" else "Blue"
        winner = ""
        Exit_game = False

        # Main game loop
        while True:
            click.clear()
            self.print_board()
            
            # Coloring the Player side message
            if any(self.AI_last_move):
                AI_full_name = "Blue" if self.AI_side == "B" else "Red"
                AI_message = click.style(f"\n({AI_full_name} AI)", fg=f"{AI_full_name.lower()}")
                move_message = click.style(f" Move {self.game_board[self.AI_last_move[1]][1]} {self.AI_last_move[0]} -> {self.AI_last_move[1]} ") # Red AI move Bishop C1 -> A3
                click.echo( AI_message + move_message)

            player_message = click.style(f"\n({player_name} player)", fg=f"{player_name.lower()}")
            system_message = click.style(f" It's your turn, Type '?' for help: ") 
            message = player_message + system_message 
            click.echo(message, nl=False)
            user_input = input().upper() # input correction incase user enter lower case coordinate

            #user input loop
            while True:
                if user_input == "?":
                    click.echo("There are three input options")
                    click.echo("1) To show piece moveset, type its coordinate (E.g. 'B2')")
                    click.echo("2) To move piece, type its coordinate and move location (E.g. 'B2B4')")
                    click.echo(f"3) To undo turn, type 'U#' where # is the number of turns to undo, (maximum {int(self.cache_size/2)} turns)")
                    click.echo(f"4) To go back to menu, type 'E'")
                # Exit game
                elif user_input == "E":
                    Exit_game = True
                    break
                # Undo mode
                elif len(user_input) == 2 and user_input[0] == "U":
                    undo_turn = int(user_input[1])*2 # as game_board_cache store every move, and each turn Red & Blue move onces
                    if undo_turn > len(self.game_board_cache): 
                        system_message = click.style(f" Only last {int(len(self.game_board_cache)/2)} turn are stored, please enter again: ") 
                    else:
                        self.undo(undo_turn)
                        click.clear()
                        self.print_board()       
                        system_message = click.style(f" Undo successful, it's your turn: ") 

                # To show piece moveset, remain in user input loop
                elif len(user_input) == 2 and user_input in self.game_board.keys():                
                    if self.game_board[user_input][0] != "·":
                        click.clear()
                        self.print_board_moves_visualize(self.move_generator(user_input))
                        system_message = click.style(f" Showing {user_input} moveset. It's your turn, Type '?' for help: ") 
                    else:
                        system_message = click.style(f" Invalid input, Type '?' for help: ") 

                # To move piece and break out user input loop
                elif len(user_input) == 4 and user_input[:2] in self.game_board.keys():
                    
                    from_pos = user_input[:2]
                    to_pos = user_input[2:]
                    if [from_pos, to_pos] in self.avail_moves(player_name[0]):
                        self.move_piece(from_pos, to_pos)
                        click.clear()
                        break
                    elif self.game_board[from_pos][0] != player_name[0]:
                        system_message = click.style(f" {from_pos} are not yours, please choose other piece: ") 
                    else:
                        system_message = click.style(f" Invalid move, Type '{from_pos}' to show legal move: ") 
                else:
                    system_message = click.style(f" Invalid input, Type '?' for help: ") 

                message = player_message + system_message 
                click.echo(message, nl=False)
                user_input = input().upper()

            if Exit_game:
                break


            if self.king_is_dead():
                winner = "Player"
                break           

            
            #check for player pawn position and ask user to choose promotion
            pawn_promote_pos = self.pawn_promotion_pos(player_name[0])
            if pawn_promote_pos:
                self.print_board()                
                system_message = click.style(f" A pawn reach {pawn_promote_pos[0]}, which pieces you want to promote to (Q, B, N or R): ")     
                message = player_message + system_message 
                click.echo(message, nl=False)
                user_input = input().upper()

                while True:

                    if self.pawn_promote(pawn_promote_pos[0],user_input):
                        break
                    else:
                        system_message = click.style(f" Invalid input, which pieces you want to promote to (Q, B, N or R): ")     
                        message = player_message + system_message 
                        click.echo(message, nl=False)
                        user_input = input().upper()
                

            self.AI_turn(self.AI_side, self.AI_depth)

            if self.king_is_dead():
                winner = "AI"
                break
        

        # Empty json save file to prevent continue option in menu screen
        if not Exit_game:
            data = {}
            json.dump(data, open("./src/save_file/ai_play.json", "w"))
            # Print end game message and go back to menu screen
            if winner == "Player":
                message = click.style(f"\nCongregation!") + click.style(f" {player_name} player ", fg=f"{player_name.lower()}") + click.style(f"you won against AI :D")
            elif winner == "AI":
                message = click.style(f"AI won, better luck next time!") + click.style(f" {player_name} player ", fg=f"{player_name.lower()}")   
            self.print_board()
            click.echo(message)
            
        click.pause("Press any key to go back to menu screen...")

    def ask_for_AI_difficulties(self):
        """
        Ask for player to choose AI difficulties: beginner, normal, hal9000(secret mode)
        return 0
        """
        click.secho("\nWelcome! Choose the AI difficulties (beginner or normal): ", nl=False)
        player = input().lower()
        while True:
            if player == "beginner":
                self.AI_depth = 1
                return 0
            elif player == "normal":
                self.AI_depth = 3
                return 0
            elif player == "hal9000":
                self.AI_depth = 5
                return 0
            # Ask for user input again
            click.secho("\nInvalid input! ",fg = "bright_red", nl=False)
            click.secho("Choose the AI difficulties (beginner or nomral):  ", nl=False)
            player = input()
        return 0

    def ask_for_player_side(self):
        """
        Ask for player to choose a side and set self.AI_side value\n
        return 0
        """
        click.secho("\nTips: Blue go first", fg = "bright_green")
        click.echo("And which side you want to play as ( "+ click.style("B", fg="blue") + " or " + click.style("R", fg="red") +  " ): ", nl=False)
        player = input().lower()
        while True:
            if player == "r":
                self.AI_side = "B"
                return 0
            elif player == "b":
                self.AI_side = "R"
                return 0
            # Ask for user input again
            click.secho("\nInvalid input! ",fg = "bright_red", nl=False)
            click.echo("And which side you want to play as ( "+ click.style("B", fg="blue") + " or " + click.style("R", fg="red") +  " ): ", nl=False)
            player = input()
        return 0

    def AI_turn(self, AI_side:str, depth:int = 3):
        """
        Do negamax evaluation and move the board using negamax algo
        AI_side: "B" or "R"
        depth: search depth \n
        return 0
        """
        side_color = 1 if AI_side == "B" else -1
        self.AI_last_move = (self.negamax_eval(self.game_board, depth , side_color, -100000, 100000)[1])
        self.move_piece(*self.AI_last_move)
        return 0

    def gen_eval_function(self, game_board: dict):
        """
        Generation the evaluation score for the board, default its for blue player (bottom)\n
        Material score: the different strength between two players (i.e. the most powerful piece are player has, the higher the score)\n
        Piece table: the position advantage of pieces
        board: game board dictionary
        player: string "B" or "R"\n
        return score (material score + piece table)
        """

        eval_score = 0
        material_score = 0

        for pos in game_board:
            if game_board[pos] == "·":
                continue
            else:
                piece = game_board[pos][1]
                piece_player = game_board[pos][0]

                # calculate material score differenet
                if piece_player == "R":
                    material_score -= self.material_dicts[piece]
                elif piece_player == "B":
                    material_score += self.material_dicts[piece]

                    # calculate Blue side position advantage
                    # not need to calculate for Red side as Blue disadvantage = Red advantage
                    if piece == "P":
                        eval_score += self.pawn_table[pos]
                    elif piece == "N":
                        eval_score += self.knight_table[pos]
                    elif piece == "B":
                        eval_score += self.bishop_table[pos]
                    elif piece == "R":
                        eval_score += self.rook_table[pos]
                    elif piece == "Q":
                        eval_score += self.queen_table[pos]
                    elif piece == "K":
                        eval_score += self.king_table[pos]

        eval_score += material_score

        # favorable condition for Blue side = unfavorable condition for Red, and vice versa
        return eval_score

    def negamax_eval(self, game_board:dict, depth: int, blue_turn: int, alpha: int, beta:int, ):
        """
        Out put the best move that a player can do, using negamax algorithm \n
        game_board: game board dictionary
        depth: how deep the negamax need to search
        alpha: -∞ for optimizing run time
        beta: +∞ for optimizing run time
        blue_turn: 1 = blue to move, -1 red turn to move
        return [eval, [list of moves]]
        """

        if depth == 0 or self.king_is_dead(game_board):
            return [ blue_turn*self.gen_eval_function(game_board), [] ]


        player_turn = "B" if blue_turn == 1 else "R"


        value = -100000
        move_set = []

        # loop over each board combination and do recursive function
        for from_pos, to_pos in self.avail_moves(player_turn, game_board):

                game_board_temp = game_board.copy()
                self.move_piece(from_pos, to_pos, game_board_temp, self.cache_size)
                # alternate to emeny side
                cal_eval = - self.negamax_eval(game_board_temp, depth-1, - blue_turn, -beta, -alpha)[0]
                if cal_eval > value:
                    value = cal_eval
                    move_set = [from_pos, to_pos]

                if alpha < value:
                    alpha = value
                # purge
                if alpha >= beta:
                    break
        return [value, move_set]

    # modify move_piece to alter save_file name
    def move_piece(self, pos:str, to:str, game_board: dict = None, cache_size: dict = None):
        """
        !!Dangerous!! This function does not provide movement checking\n
        Teleport piece on "pos" -> "to" and store perious board into game_board_cache
        pos: string (e.g. "A1")
        to: string (e.g. "B1")

        return True when move is successful, False when pos has no pieces
        """
        if game_board == None:
            game_board = self.game_board
        if cache_size == None:
            cache_size = self.cache_size

        piece = game_board[pos]
        if piece == "·":
            return False


        # Cache game board before move
        if self.game_board not in self.game_board_cache: 
            self.game_board_cache += [game_board.copy()]
            if len(self.game_board_cache) > cache_size:
                self.game_board_cache.pop(0)       

        #modify game board
        game_board[to] = piece
        game_board[pos] = "·"

        # save current board to json file
        if game_board == self.game_board: 
            data = {"game_board": self.game_board.copy(), "AI_side" : self.AI_side, "AI_depth" : self.AI_depth}
            json.dump(data, open("./src/save_file/ai_play.json", "w"))
        return True

def play_with_AI(load_save_data = False, Test_mode = False):    
    """
    load_save_data: True = load json save game from save_file
    Test_mode: True = Player always on Blue
    """
    game = chess_with_AI(8)
    board_set = {
        "RR": ["A8", "H8"],
        "RN": ["B8", "G8"],
        "RB" : ["C8", "F8"],
        "RQ" : ["D8"],
        "RK" : ["E8"],
        "RP" : ["A7","B7","C7","D7","E7","F7","G7","H7"],
        "BR": ["A1", "H1"],
        "BN": ["B1", "G1"],
        "BB" : ["C1", "F1"],
        "BQ" : ["D1"],
        "BK" : ["E1"],
        "BP" : ["A2","B2","C2","D2","E2","F2","G2","H2"] 
    }
    game.fill_pieces_on_board(board_set)
    game.print_board()
    game.start_game(load_save_data, Test_mode)
  

if __name__ == "__main__":
    play_with_AI()
    # main(False, True)
    pass


 

