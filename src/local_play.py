from src.chess import game_board

import click, json

class local_play(game_board):

    def __init__(self, size: int, cache_size: int = 6):
        super().__init__(size, cache_size)
        self.blue_name = ""
        self.red_name = ""

        self.enemy_last_move = []
    
    def start_game(self, use_save_data = False, Test_mode = False):
        """
        1) Load perious save file (if use_save_data == True)
        2) ask blue and red player name
        3) Main gameplay loop
        4) Exit game and save or empty save file when one player win        
        """


        if self.size != 8:
            raise ValueError(f"Game board size must be 8x8 (Current size = {self.size}x{self.size})")

        if use_save_data:
            data = json.load(open("./src/save_file/local_play.json"))
            self.game_board, self.current_turn, self.blue_name, self.red_name = data["game_board"].copy(), data["current_turn"], data["blue_name"], data["red_name"]
        elif Test_mode:
            self.blue_name = "Aoi"
            self.red_name = "Aka"
        else:
            click.clear()
            self.print_board()
            self.ask_for_blue_name()
            self.ask_for_red_name()
            #override save data
            data = {"game_board": self.game_board.copy(), "current_turn" : "B", "blue_name" : self.blue_name, "red_name": self.red_name}
            json.dump(data, open("./src/save_file/local_play.json", "w"))
        
        # Prepare local variable
        winner = ""
        Exit_game = False
        promote_message = ""

        # Main game loop
        while True:
            click.clear()
            self.print_board()
            
            # Coloring the Player side message
            if any(self.enemy_last_move):
                enemy_full_name = self.blue_name if self.current_turn == "R" else self.red_name
                enemy_color = "blue" if self.current_turn == "R" else "red"

                enemy_message = click.style(f"\n({enemy_full_name} - {enemy_color.capitalize()})", fg=enemy_color)
                move_message = click.style(f" Move {self.game_board[self.enemy_last_move[1]][1]} {self.enemy_last_move[0]} -> {self.enemy_last_move[1]} ") #(name- Red) Move Bishop C1 -> A3
                
                if promote_message:
                    click.echo( enemy_message + move_message + promote_message)
                    promote_message = ""
                else:
                    click.echo( enemy_message + move_message + promote_message)


            full_name = self.blue_name if self.current_turn == "B" else self.red_name
            color = "Blue" if self.current_turn == "B" else "Red"


            player_message = click.style(f"\n({full_name} - {color})", fg=color.lower())
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
                    click.echo("3) To go back to menu, type 'E'")
                # Exit game
                elif user_input == "E":
                    Exit_game = True
                    break

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
                    if [from_pos, to_pos] in self.avail_moves(color[0].upper()):
                        self.enemy_last_move = [from_pos, to_pos]
                        self.move_piece(from_pos, to_pos)
                        click.clear()
                        break
                    elif self.game_board[from_pos][0] != color[0].upper():
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
                winner = self.current_turn
                break           

            
            #check for player pawn position and ask user to choose promotion
            pawn_promote_pos = self.pawn_promotion_pos(color[0].upper())
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

                promote_message = f"and promote P at {pawn_promote_pos[0]} to {user_input}"
                # save board after promotion
                next_turn = "B" if self.current_turn == "R" else "R"
                data = {"game_board": self.game_board.copy(), "current_turn" : next_turn, "blue_name" : self.blue_name, "red_name": self.red_name} # we want to save next turn data
                json.dump(data, open("./src/save_file/local_play.json", "w"))

            
            self.current_turn = "R" if self.current_turn == "B" else "B"


        # Empty json save file to prevent continue option in menu screen
        if not Exit_game:
            data = {}
            json.dump(data, open("./src/save_file/local_play.json", "w")) #TODO:modify json file name
            # Print end game message and go back to menu screen
            if winner == "B":
                message = click.style(f"\nCongregation!") + click.style(f" {self.blue_name} ", fg= "blue") + click.style(f"you won against") + click.style(f" {self.red_name} ", fg= "red")
            elif winner == "R":
                message = click.style(f"\nCongregation!") + click.style(f" {self.red_name} ", fg= "red") + click.style(f"you won against") + click.style(f" {self.blue_name} ", fg= "blue")
            self.print_board()
            click.echo(message)
            
        click.pause("Press any key to go back to menu screen...")

    def ask_for_blue_name(self):
        """
        Ask for the blue player name
        return 0
        """
        system_message = "\nWelcome! "
        click.echo(system_message + click.style("Blue player", fg = "blue") + " what's your name: ", nl=False)
        name = input()
        self.blue_name = name

        system_message = click.style(f"\nHello {self.blue_name}!", fg = "blue")
        # ask player to type their name again to confirm or rename
        while True:
            click.echo(system_message + f" type '{self.blue_name}' again to confirm or 'NO' to rename: ", nl=False)
            confirm = input()

            if confirm == self.blue_name:
                break
            elif confirm == "NO":
                system_message = "\nWelcome again! "
                click.echo(system_message + click.style("Blue player", fg = "blue") + " what's your name: ", nl=False)
                name = input()
                self.blue_name = name
                system_message = click.style(f"\nHello {self.blue_name}!", fg = "blue")
            else:
                system_message = click.style("\nInvalid input!", fg = "bright_green")

        return 0

    def ask_for_red_name(self):
        """
        Ask for the red player name
        return 0
        """
        system_message = "\nWelcome! "
        click.echo(system_message + click.style("Red player", fg = "red") + " what's your name: ", nl=False)
        name = input()
        self.red_name = name

        system_message = click.style(f"\nHello {self.red_name}!", fg = "red")
        # ask player to type their name again to confirm or rename
        while True:
            click.echo(system_message + f" type '{self.red_name}' again to confirm or 'NO' to rename: ", nl=False)
            confirm = input()

            if confirm == self.red_name:
                break
            elif confirm == "NO":
                system_message = "\nWelcome again! "
                click.echo(system_message + click.style("Red player", fg = "red") + " what's your name: ", nl=False)
                name = input()
                self.red_name = name
                system_message = click.style(f"\nHello {self.red_name}!", fg = "red")
            else:
                system_message = click.style("\nInvalid input!", fg = "bright_green")

        return 0

    # modify move_piece json save file name
    def move_piece(self, pos:str, to:str, game_board: dict = None, cache_size: dict = None):
        """
        !!Dangerous!! This function does not provide movement checking\n
        Teleport piece on "pos" -> "to" and store perious board into game_board_cache\n
        And store the perious game board to cache and current board to json
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
            next_turn = "B" if self.current_turn == "R" else "R"
            data = {"game_board": self.game_board.copy(), "current_turn" : next_turn, "blue_name" : self.blue_name, "red_name": self.red_name} # we want to save next turn data
            json.dump(data, open("./src/save_file/local_play.json", "w"))
        return True

def play_locally(load_save_data = False, Test_mode = False):
    #Blue at bottom, red on top
    game = local_play(8)
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
        "BP" : ["A2","B2","C2","D2","E2","F2","G2","H2"],
    }
    game.fill_pieces_on_board(board_set)
    game.start_game(load_save_data, Test_mode)

if __name__ == "__main__":
    play_locally(False, True)