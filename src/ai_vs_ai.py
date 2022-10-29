import click, json, time

from src.ai_play import chess_with_AI 

class AI_against_AI(chess_with_AI):
    # def __init__(self, size: int, cache_size: int = 6, AI_side:str = "B"):
    #     super().__init__(size, cache_size)
    #     self.AI_side = AI_side
    #     self.AI_last_move = []

    #     # To optimize run time, the Piece-Square Tables are store in the class instead
    #     # The table is provided by https://www.chessprogramming.org/Piece-Square_Tables
    #     self.pawn_table = {
    #         'A8': 0, 'B8': 0, 'C8': 0, 'D8': 0, 'E8': 0, 'F8': 0, 'G8': 0, 'H8': 0,
    #         'A7': 50, 'B7': 50, 'C7': 50, 'D7': 50, 'E7': 50, 'F7': 50, 'G7': 50, 'H7': 50,
    #         'A6': 10, 'B6': 10, 'C6': 20, 'D6': 30, 'E6': 30, 'F6': 20, 'G6': 10, 'H6': 10,
    #         'A5': 5, 'B5': 5, 'C5': 10, 'D5': 25, 'E5': 25, 'F5': 10, 'G5': 5, 'H5': 5,
    #         'A4': 0, 'B4': 0, 'C4': 0, 'D4': 20, 'E4': 20, 'F4': 0, 'G4': 0, 'H4': 0,
    #         'A3': 5, 'B3': -5, 'C3': -10, 'D3': 0, 'E3':0, 'F3': -10, 'G3': -5, 'H3': 5,
    #         'A2': 5, 'B2': 10, 'C2': 10, 'D2': -20, 'E2': -20, 'F2': 10, 'G2': 10, 'H2': 5,
    #         'A1': 0, 'B1': 0, 'C1': 0, 'D1': 0, 'E1': 0, 'F1': 0, 'G1': 0, 'H1': 0
    #     }
    #     self.knight_table = {
    #         'A8': -50, 'B8': -40, 'C8': -30, 'D8': -30, 'E8': -30, 'F8': -30, 'G8': -40, 'H8': -50,
    #         'A7': -40, 'B7': -20, 'C7': 0, 'D7': 0, 'E7': 0, 'F7': 0, 'G7': -20, 'H7': -40,
    #         'A6': -30, 'B6': 0, 'C6': 10, 'D6': 15, 'E6': 15, 'F6': 10, 'G6': 0, 'H6': -30,
    #         'A5': -30, 'B5': 5, 'C5': 15, 'D5': 20, 'E5': 20, 'F5': 15, 'G5': 5, 'H5': -30,
    #         'A4': -30, 'B4': 0, 'C4': 15, 'D4': 20, 'E4': 20, 'F4': 15, 'G4': 0, 'H4': -30,
    #         'A3': -30, 'B3': 5, 'C3': 10, 'D3': 15, 'E3': 15, 'F3': 10, 'G3': 5, 'H3': -30,
    #         'A2': -40, 'B2': -20, 'C2': 0, 'D2': 5, 'E2': 5, 'F2': 0, 'G2': -20, 'H2': -40,
    #         'A1': -50, 'B1': -40, 'C1': -30, 'D1': -30, 'E1': -30, 'F1': -30, 'G1': -40, 'H1': -50
    #     }
    #     self.bishop_table = {
    #         'A8': -20, 'B8': -10, 'C8': -10, 'D8': -10, 'E8': -10, 'F8': -10, 'G8': -10, 'H8': -20,
    #         'A7': -10, 'B7': 0, 'C7': 0, 'D7': 0, 'E7': 0, 'F7': 0, 'G7': 0, 'H7': -10,
    #         'A6': -10, 'B6': 0, 'C6': 5, 'D6': 10, 'E6': 10, 'F6': 5, 'G6': 0, 'H6': -10,
    #         'A5': -10, 'B5': 5, 'C5': 5, 'D5': 10, 'E5': 10, 'F5': 5, 'G5': 5, 'H5': -10,
    #         'A4': -10, 'B4': 0, 'C4': 10, 'D4': 10, 'E4': 10, 'F4': 10, 'G4': 0, 'H4': -10,
    #         'A3': -10, 'B3': 10, 'C3': 10, 'D3': 10, 'E3': 10, 'F3': 10, 'G3': 10, 'H3': -10,
    #         'A2': -10, 'B2': 5, 'C2': 0, 'D2': 0, 'E2': 0, 'F2': 0, 'G2': 5, 'H2': -10,
    #         'A1': -20, 'B1': -10, 'C1': -10, 'D1': -10, 'E1': -10, 'F1': -10, 'G1': -10, 'H1': -20
    #     }
    #     self.rook_table = {
    #         'A8': 0, 'B8': 0, 'C8': 0, 'D8': 0, 'E8': 0, 'F8': 0, 'G8': 0, 'H8': 0,
    #         'A7': 5, 'B7': 10, 'C7': 10, 'D7': 10, 'E7': 10, 'F7': 10, 'G7': 10, 'H7': 5,
    #         'A6': -5, 'B6': 0, 'C6': 0, 'D6': 0, 'E6': 0, 'F6': 0, 'G6': 0, 'H6': -5,
    #         'A5': -5, 'B5': 0, 'C5': 0, 'D5': 0, 'E5': 0, 'F5': 0, 'G5': 0, 'H5': -5,
    #         'A4': -5, 'B4': 0, 'C4': 0, 'D4': 0, 'E4': 0, 'F4': 0, 'G4': 0, 'H4': -5,
    #         'A3': -5, 'B3': 0, 'C3': 0, 'D3': 0, 'E3': 0, 'F3': 0, 'G3': 0, 'H3': -5,
    #         'A2': -5, 'B2': 0, 'C2': 0, 'D2': 0, 'E2': 0, 'F2': 0, 'G2': 0, 'H2': -5,
    #         'A1': 0, 'B1': 0, 'C1': 0, 'D1': 5, 'E1': 5, 'F1': 0, 'G1': 0, 'H1': 0
    #     }
    #     self.queen_table = {
    #         'A8': -20, 'B8': -10, 'C8': -10, 'D8': -5, 'E8': -5, 'F8': -10, 'G8': -10, 'H8': -20,
    #         'A7': -10, 'B7': 0, 'C7': 0, 'D7': 0, 'E7': 0, 'F7': 0, 'G7': 0, 'H7': -10,
    #         'A6': -10, 'B6': 0, 'C6': 5, 'D6': 5, 'E6': 5, 'F6': 5, 'G6': 0, 'H6': -10,
    #         'A5': -5, 'B5': 0, 'C5': 5, 'D5': 5, 'E5': 5, 'F5': 5, 'G5': 0, 'H5': -5,
    #         'A4': 0, 'B4': 0, 'C4': 5, 'D4': 5, 'E4': 5, 'F4': 5, 'G4': 0, 'H4': -5,
    #         'A3': -10, 'B3': 5, 'C3': 5, 'D3': 5, 'E3': 5, 'F3': 5, 'G3': 0, 'H3': -10,
    #         'A2': -10, 'B2': 0, 'C2': 5, 'D2': 0, 'E2': 0, 'F2': 0, 'G2': 0, 'H2': -10,
    #         'A1': -20, 'B1': -10, 'C1': -10, 'D1': -5, 'E1': -5, 'F1': -10, 'G1': -10, 'H1': -20
    #     }
    #     self.king_table = {
    #         'A8': -30, 'B8': -40, 'C8': -40, 'D8': -50, 'E8': -50, 'F8': -40, 'G8': -40, 'H8': -30,
    #         'A7': -30, 'B7': -40, 'C7': -40, 'D7': -50, 'E7': -50, 'F7': -40, 'G7': -40, 'H7': -30,
    #         'A6': -30, 'B6': -40, 'C6': -40, 'D6': -50, 'E6': -50, 'F6': -40, 'G6': -40, 'H6': -30,
    #         'A5': -30, 'B5': -40, 'C5': -40, 'D5': -50, 'E5': -50, 'F5': -40, 'G5': -40, 'H5': -30,
    #         'A4': -20, 'B4': -30, 'C4': -30, 'D4': -40, 'E4': -40, 'F4': -30, 'G4': -30, 'H4': -20,
    #         'A3': -10, 'B3': -20, 'C3': -20, 'D3': -20, 'E3': -20, 'F3': -20, 'G3': -20, 'H3': -10,
    #         'A2': 20, 'B2': 20, 'C2': 0, 'D2': 0, 'E2': 0, 'F2': 0, 'G2': 20, 'H2': 20,
    #         'A1': 20, 'B1': 30, 'C1': 10, 'D1': 0, 'E1': 0, 'F1': 10, 'G1': 30, 'H1': 20
    #     }
    #     self.material_dicts = {
    #         "P" : 100,
    #         "N" : 320,
    #         "B" : 330,
    #         "R" : 500,
    #         "Q" : 900,
    #         "K" : 20000
    #     }

    #     self.row_alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:self.size]
    #     self.col_num = list(range(1, self.size))
    def __init__(self, size: int, cache_size: int = 6, AI_side: str = "B"):
        super().__init__(size, cache_size, AI_side)


    def start_AI_vs_AI(self, Blue_depth:int, Red_depth:int, turn_limit = 1000):
        """
        Start a AI vs AI game, a tech demo
        Blue_depth: negamax search depth for Blue AI
        Red_depth: negamx serach depth for Red AI
        """
        # Empty json content to prevent "Permission denied issue" ./src/save_file/ai_play.json
        data = {}
        json.dump(data, open("./src/save_file/ai_play.json", "w"))

        color = "B"
        depth = Blue_depth
        full_name = {"B":"Blue", "R": "Red"}
        counter = {"B": 0, "R": 0}
        winner = ""

        for i in range(turn_limit):

            click.clear()
            self.print_board()

            enemy = "Red" if color == "B" else "Blue"

            if any(self.AI_last_move):
                message = "\n❮" + click.style(f" {enemy} AI", fg =enemy.lower()) + click.style(f" move {self.game_board[self.AI_last_move[1]][1]} {self.AI_last_move[0]} -> {self.AI_last_move[1]} ❯")
                click.echo(message)


            message = click.style(f"\n{full_name[color]} AI", fg =full_name[color].lower()) + click.style(f" is computing its next move")
            click.echo(message)

            if counter[color] != 0:
                time_message = click.style(f"{full_name[color]} AI", fg =full_name[color].lower()) + click.style(f" used {counter[color]}s to compute last turn")
                click.echo(time_message)

            t1 = time.time()
            self.AI_turn(color, depth)
            t2 = time.time()

            # Allow user to see the moves
            if t2-t1 < 0.2:
                time.sleep(0.2)

            counter[color] = t2-t1


            if self.king_is_dead():
                winner = color
                break

            color = "R" if color == "B" else "B"
            depth = Red_depth if color == "R" else Blue_depth


        # Empty json save file to prevent continue option in menu screen
        data = {}
        json.dump(data, open("./src/save_file/ai_play.json", "w"))

        if winner == "B":
            message = click.style(f"\nCongregation!") + click.style(f" Blue AI", fg ="blue") + click.style(" won against") + click.style(f" Red AI", fg ="red")
        elif winner == "R":
            message = click.style(f"\nCongregation!") + click.style(f" Red AI", fg ="red") + click.style(" won against") + click.style(f" Blue AI", fg ="blue")
        else:
            message = click.style(f"\nStalemate, reach turn limit!")

        click.clear()
        self.print_board()
        click.echo(message)
        click.pause("Press any key to go back to menu screen...")
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
            data = {"game_board": self.game_board.copy(), "AI_side" : self.AI_side}
            json.dump(data, open("./src/save_file/ai_vs_ai.json", "w"))
        return True



def AI_vs_AI(Test_mode = False):
    if not Test_mode:
        AI_difficulties = {"BEGINNER":1, "NORMAL":3, "HAL9000":5} # HAL9000 is secret mode, required long run time
        click.secho("\nSelect Blue AI difficulty (Beginner or Normal): ", nl=False, fg = "blue")
        while True:
            string = input().upper()
            if string in AI_difficulties:
                blue_depth = AI_difficulties[string]
                break
            click.echo("\nInvalid Input!" + click.style(" Select Blue AI difficulty again (Beginner or Normal): ", fg = "blue"),  nl=False)
        
        click.secho("\nSelect Red AI difficulty (Beginner or Normal): ", nl=False, fg = "red")
        while True:
            string = input().upper()
            if string in AI_difficulties:
                red_depth = AI_difficulties[string]
                break
            click.echo("\nInvalid Input!" + click.style(" Select Red AI difficulty again (Beginner or Normal): ", fg = "red"),  nl=False)
    else:
        red_depth, blue_depth = 3, 3

        
    game = AI_against_AI(8)
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
    game.start_AI_vs_AI(blue_depth, red_depth, 1000)

if __name__ == "__main__":
    AI_vs_AI()


 

