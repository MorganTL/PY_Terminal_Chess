from src.chess import game_board

import click, json

class n_queen(game_board):

    def __init__(self, size: int, cache_size: int = 6):
        super().__init__(size, cache_size)
        self.queen_pos = {} 
        self.queen_conflict = []
        self.queen_color = {
            "1" : "blue",
            "2" : "red",
            "3" : "yellow",
            "4" : "magenta",
            "5" : "cyan",
            "6" : "green",
            "7" : "blue",
            "8" : "red",
            "9" : "yellow",
        }
        
    
    def start_game(self, use_save_data = False, Test_mode = False):
        """
        1) Load perious save file (if use_save_data == True)
        2) ask blue and red player name
        3) Main gameplay loop
        4) Exit game and save or empty save file when one player win        
        """

        if self.size <= 3 or self.size >= 10:
            raise ValueError(f"Game board size must be 3<n<10 (Current size = {self.size}x{self.size})")


        if use_save_data:
            data = json.load(open("./src/save_file/n_queen.json"))
            self.queen_pos, self.size, self.queen_conflict = data["queen_pos"], data["size"], data["queen_conflict"]
            self.game_board = self.make_board(self.size)
            self.fill_pieces_on_board(self.queen_pos)
        elif Test_mode:
            pass # not saving json
        else:
            #override save data
            self.ask_for_board_size()
            data = {"queen_pos": self.queen_pos.copy(), "size" : self.size, "queen_conflict" : []}
            json.dump(data, open("./src/save_file/n_queen.json", "w"))
        
        # Prepare local variable
        Exit_game = False

        # Main game loop
        while True:
            #detection win condition
            if len(self.queen_pos) == self.size and not any(self.queen_conflict):
                break

            click.clear()
            self.print_board_n_queen(self.queen_conflict) 
            
            # Print all queen position if any
            if any(self.queen_pos):                
                
                prefix_message = "\n❮ You already filled "
                pos_message = ""
                for queen in self.queen_pos:
                    pos_message += click.style(f"{self.queen_pos[queen][0]} ", fg=self.queen_color[queen[0]])
                
                if self.size - len(self.queen_pos) == 1:
                    ending_message = f"- {self.size - len(self.queen_pos)} Queen left ❯"
                else:
                    ending_message = f"- {self.size - len(self.queen_pos)} Queens left ❯"

                click.echo( prefix_message + pos_message + ending_message)

            # Print out all queen conflict
            if any(self.queen_conflict):
                
                # sort the queen conflict list
                queen_threaten_ls = []
                for pos in self.queen_conflict:
                    key_ls = list(self.queen_pos.keys())
                    val_ls = list(self.queen_pos.values())
                    queen_threaten_ls += [key_ls[val_ls.index([pos])]]
                queen_threaten_ls.sort()


                prefix_message = "❮ Queens at "
                pos_message = ""
                for queen in queen_threaten_ls:
                    pos_message += click.style(f"{self.queen_pos[queen][0]} ", fg=self.queen_color[queen[0]])
                
                ending_message = f"threaten each other ❯"
                click.echo( prefix_message + pos_message + ending_message)
               



            player_message = click.style(f"\n( Player )", fg="blue")
            system_message = click.style(f" It's your turn, Type '?' for help: ") 
            message = player_message + system_message 
            click.echo(message, nl=False)
            user_input = input().upper() # input correction incase user enter lower case coordinate

            #user input loop
            while True:
                if user_input == "?":
                    click.echo("There are three input options")
                    click.echo("1) To put queens on board, type their unique coordinate (E.g. 'A1 B2 C3')")
                    click.echo("2) To remove all queen from board, type 'R'")
                    click.echo("3) To go back to menu, type 'E'")
                # Exit game
                elif user_input == "E":
                    Exit_game = True
                    break

                # Remove all queen from board
                elif user_input == "R":
                    self.queen_pos = {}
                    self.queen_conflict = [] #reset conflict 
                    self.game_board = self.make_board(self.size) # clear board
                    break

                elif len(user_input.split()) > self.size:
                    system_message = click.style(f" Too many positions, Type '?' for help: ") 

                elif len(user_input.split()) != len(set(user_input.split())):
                    system_message = click.style(f" Duplicate positions, Type '?' for help: ") 

                elif all(queen in self.game_board.keys() for queen in user_input.split()):
                    self.game_board = self.make_board(self.size) # clear board                    
                    i = 1
                    board_set = {}
                    for queen in user_input.split():
                        board_set[f"{i}Q"] = [queen]
                        i += 1
                    self.queen_pos = board_set
                    self.fill_pieces_on_board(board_set)

                    # Colflict detection
                    pos_list = []
                    conflict_list = []
                    for queen in self.queen_pos:
                        pos_list += self.queen_pos[queen]
                        move_set = self.move_generator(self.queen_pos[queen][0])
                        for move in move_set:
                            if move in pos_list:
                                conflict_list += [move]
                                conflict_list += self.queen_pos[queen]
                    self.queen_conflict = list(set(conflict_list)) # remove duplicate

                    break                 
                else:
                    system_message = click.style(f" Invalid input, Type '?' for help: ") 

                message = player_message + system_message 
                click.echo(message, nl=False)
                user_input = input().upper()

            if Exit_game:
                break

            #Save data to json
            data = {"queen_pos": self.queen_pos.copy(), "size" : self.size, "queen_conflict" : self.queen_conflict}
            json.dump(data, open("./src/save_file/n_queen.json", "w"))
            


        # Empty json save file to prevent continue option in menu screen
        if not Exit_game:
            data = {}
            json.dump(data, open("./src/save_file/n_queen.json", "w"))
            # Print end game message and go back to menu screen
            message = click.style(f"\nCongregation!") + click.style(f" Player ", fg= "blue") + click.style(f"you successfully fill {self.size}x{self.size} board with {self.size} Queen :D")
            click.clear()
            self.print_board_n_queen()
            click.echo(message)
        click.pause("Press any key to go back to menu screen...")

    def ask_for_board_size(self):
        """
        Ask player to set board size
        return 0
        """


        player_message =  click.style("\nWelcome Player!", fg = "blue") 
        system_message = " what chessboard size you want to play in (4-9): "
        message = player_message + system_message
        click.echo(message, nl=False)
        num = (input().lower()).strip()

        while True:
            if not num.isnumeric():
                player_message = click.style("\nPlease enter a number!" ,fg="red")
            elif int(num) <= 3 or int(num) >= 10:
                player_message = click.style("\nNumber out of range!" ,fg="red")
            else:
                self.size = int(num)
                self.game_board = self.make_board(self.size) # make new board
                break
            message = player_message + system_message
            click.echo(message, nl=False)
            num = input()
        return 0

    # modify print board to print different queen colour 
    def print_board_n_queen(self, moves:list = []):
        """
        Print game board with terminal coloring

        return 0
        """

        temp_game_board = self.game_board.copy()
        for pos in moves:
            if temp_game_board[pos] == "·":
                temp_game_board[pos] = "x"
            else:
                temp_game_board[pos] += "x"
        alphas = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


        alphas = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        alpha_st = " ".join(alphas[:self.size])
        click.secho(" "*4+alpha_st)
        click.echo()

        for i in range(self.size, 0, -1):

            click.secho(f'{i}'.ljust(4), nl = False)

            for j in range(self.size):
                # Add color to game board and pieces
                if (temp_game_board[(alphas[j])+str(i)]) == "·":
                    click.secho(f'{temp_game_board[(alphas[j])+str(i)]} ', fg='green', nl = False)
                elif len(temp_game_board[(alphas[j])+str(i)]) == 1:
                    click.secho(f'{temp_game_board[(alphas[j])+str(i)]} ', nl = False)
                elif len((temp_game_board[(alphas[j])+str(i)])) == 3: #tagged                    
                    click.secho(click.style(f'{temp_game_board[(alphas[j])+str(i)][1]}', fg=self.queen_color[temp_game_board[(alphas[j])+str(i)][0]], bg = "white") + " ", nl = False)
                else:
                    click.secho(f'{temp_game_board[(alphas[j])+str(i)][1]} ', fg=self.queen_color[temp_game_board[(alphas[j])+str(i)][0]], nl = False)

            click.secho(f'{i}'.rjust(3))
        click.echo()
        click.secho(" "*4+alpha_st)
        return 0

    #change player name to 1-9 and queen only
    def fill_pieces_on_board(self, pieces: dict):
        """
        pieces: a dictionary key = pieces name, value = list of init position
        E.g. {"1Q": ["D8"], "2Q": ["A1"]}
        return True if successful
        """

        for k in pieces.keys():
            if (k[0] not in "123456789") or (k[1] not in "Q"):
                raise NameError("The pieces are not name correctly")

            self.pieces_init_pos[k] = pieces[k][:]
            for pos in pieces[k]:
                self.game_board[pos] = k

        return True

def play_n_queen(board_size:int = 8,load_save_data = False, Test_mode = False):
    if Test_mode:
        board_set = {
            "1Q": ["A1"],
            "2Q": ["B4"],
            "3Q": ["C1"],
            # "4Q": ["D3"],
            # "5Q": ["E5"],
            # "6Q": ["F6"],
            # "7Q": ["G7"],
            # "8Q": ["H8"],
            # "9Q": ["I9"],
        }
        game = n_queen(board_size)
        game.fill_pieces_on_board(board_set)
        game.queen_pos = board_set.copy()
    else:
        game = n_queen(board_size)
    game.start_game(load_save_data, Test_mode)

if __name__ == "__main__":
    play_n_queen(4, False, True)