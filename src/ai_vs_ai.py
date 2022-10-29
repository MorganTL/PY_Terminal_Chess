import click, time

from src.ai_play import chess_with_AI 

class AI_against_AI(chess_with_AI): 
    def __init__(self, size: int, cache_size: int = 6, AI_side: str = "B"):
        super().__init__(size, cache_size, AI_side)


    def start_AI_vs_AI(self, Blue_depth:int, Red_depth:int, turn_limit = 1000):
        """
        Start a AI vs AI game, a tech demo
        Blue_depth: negamax search depth for Blue AI
        Red_depth: negamx serach depth for Red AI
        """


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

 

