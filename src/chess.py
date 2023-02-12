import click

# click docs : https://click.palletsprojects.com/en/8.1.x/utils/
# This is a package, run any function in this file

class game_board():

    def __init__(self, size: int, cache_size: int = 6):
        self.size = size
        self.game_board = self.make_board(size)
        self.current_turn = "B" 

        self.game_board_cache = [] # Does not store current game_board
        self.cache_size = cache_size

        self.pieces_init_pos = {}
        self.player_moves = []
        self.killed_pieces = []


    def make_board(self, size):
        """
        Generate size x size gameboard dictionary
        Each fill with ·
        """
        alphas = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        board = {}
        for i in range(size):
            for j in range(1,size+1):
                st = (alphas[i])+str(j)
                board[st]="·"
        return board

    def fill_pieces_on_board(self, pieces: dict):
        """
        pieces: a dictionary key = pieces name, value = list of init position
        E.g. {"RK": ["D8"], "BR": ["A1", "H1"]}
        return True if successful
        """

        for k in pieces.keys():
            if (k[0] not in "RB") or (k[1] not in "RBQKPN"):
                raise NameError("The pieces are not name correctly")

            self.pieces_init_pos[k] = pieces[k][:]
            for pos in pieces[k]:
                self.game_board[pos] = k

        return True

    def print_board(self):
        """
        Print game board with terminal coloring

        return 0
        """
        alphas = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        alpha_st = " ".join(alphas[:self.size])
        click.secho(alpha_st.center(self.size*3))
        click.echo()

        for i in range(self.size, 0, -1):

            click.secho(f'{i}'.ljust(4), nl = False)

            for j in range(self.size):
                # Add color to game board and pieces
                if (self.game_board[(alphas[j])+str(i)]) == "·":
                    click.secho(f'{self.game_board[(alphas[j])+str(i)]} ', fg='green', nl = False)
                elif len(self.game_board[(alphas[j])+str(i)]) == 1:
                    click.secho(f'{self.game_board[(alphas[j])+str(i)]} ', nl = False)
                elif (self.game_board[(alphas[j])+str(i)][0]) == "R":
                    click.secho(f'{self.game_board[(alphas[j])+str(i)][1]} ', fg='bright_red', nl = False)
                elif (self.game_board[(alphas[j])+str(i)][0]) == "B":
                    click.secho(f'{self.game_board[(alphas[j])+str(i)][1]} ', fg='bright_blue', nl = False)
                # print(self.game_board[(alphas[j])+str(i)],end=" ")

            click.secho(f'{i}'.rjust(3))
        click.echo()
        click.secho(alpha_st.center(self.size*3))
        return 0

    def move_generator(self, pos: str, game_board:dict = None):
        """
        Genearte a list of legal moves for the pieces on pos
        pos: string (e.g. "A1")\n
        return a list of legal moves that the pieces can do
        """
        if game_board == None:
            game_board = self.game_board

        if (game_board[pos]) == "·":
            return []
        piece = game_board[pos][1]

        # click.secho(f"At {pos}, there is {piece}", fg="green")

        if piece == "R":
            return self.move_gen_rook(pos, game_board)

        elif piece == "B":
            return self.move_gen_bishop(pos, game_board)

        elif piece == "Q":
            return self.move_gen_bishop(pos, game_board) + self.move_gen_rook(pos, game_board)

        elif piece == "K":
            return self.move_gen_king(pos, game_board)

        elif piece == "P":
            return self.move_gen_pawn(pos, game_board)

        elif piece == "N":
            return self.move_gen_knight(pos, game_board)

    def move_gen_rook(self, pos: str, game_board:dict):
        """
        pos: string (e.g. "A1")\n
        return a list of legal move (include tile of enemy)
        """
        player = game_board[pos][0]
        alpha_st = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:self.size]
        moves = []

        # horzontial from right to left
        # if tile is a piece:
        # same player -> pop all element
        # enemey -> pop all elemnt + add current position
        temp_moves = []
        for x in alpha_st:
            if x == pos[0]:
                break

            if game_board[f"{x}{pos[1]}"] == "·":
                temp_moves.append(f"{x}{pos[1]}")

            elif game_board[f"{x}{pos[1]}"][0] == player:
                temp_moves = []

            else:
                temp_moves = []
                temp_moves.append(f"{x}{pos[1]}")

        moves += temp_moves[:]

        # horzontial from left to right
        temp_moves = []
        for x in alpha_st[::-1]:
            if x == pos[0]:
                break

            if game_board[f"{x}{pos[1]}"] == "·":
                temp_moves.append(f"{x}{pos[1]}")

            elif game_board[f"{x}{pos[1]}"][0] == player:
                temp_moves = []

            else:
                temp_moves = []
                temp_moves.append(f"{x}{pos[1]}")

        moves += temp_moves[::-1]


        # vertical from bottom to top
        # if tile is a piece:
        # same player -> pop all element
        # enemey -> pop all elemnt + add current position
        temp_moves = []
        for y in map(str, range(1, self.size+1)):
            if y == pos[1]:
                break

            if game_board[f"{pos[0]}{y}"] == "·":
                temp_moves.append(f"{pos[0]}{y}")

            elif game_board[f"{pos[0]}{y}"][0] == player:
                temp_moves = []

            else:
                temp_moves = []
                temp_moves.append(f"{pos[0]}{y}")

        moves += temp_moves[:]

        # vertical from top to bottom
        temp_moves = []
        for y in map(str, range(self.size, 0, -1)):
            if y == pos[1]:
                break

            if game_board[f"{pos[0]}{y}"] == "·":
                temp_moves.append(f"{pos[0]}{y}")

            elif game_board[f"{pos[0]}{y}"][0] == player:
                temp_moves = []

            else:
                temp_moves = []
                temp_moves.append(f"{pos[0]}{y}")

        moves += temp_moves[::-1]
        return moves

    def move_gen_bishop(self, pos: str, game_board:dict):
        """
        pos: string (e.g. "A1")\n
        return a list of legal move (include tile of enemy)
        """
        player = game_board[pos][0]
        alpha_st = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:self.size]
        moves = []

        # left and down 🡗, start from pos
        # if tile is a piece:
        # same player -> pop all element
        # enemey -> pop all elemnt + add current position
        temp_moves = []
        pos0_index = alpha_st.find(pos[0])-1
        pos1_index = int(pos[1])-1
        while (pos0_index >= 0) and (pos1_index >= 1):
            # print(f"POS: {alpha_st[pos0_index]}{pos1_index}")

            if game_board[f"{alpha_st[pos0_index]}{pos1_index}"] == "·":
                temp_moves.append(f"{alpha_st[pos0_index]}{pos1_index}")

            elif game_board[f"{alpha_st[pos0_index]}{pos1_index}"][0] == player:
                break

            else:
                temp_moves.append(f"{alpha_st[pos0_index]}{pos1_index}")
                break
            pos0_index -= 1
            pos1_index -= 1
        moves += temp_moves[:]

        # left and up 🡔, start from pos
        temp_moves = []
        pos0_index = alpha_st.find(pos[0])-1
        pos1_index = int(pos[1])+1
        while (pos0_index >= 0) and (pos1_index <= self.size):
            # print(f"POS: {alpha_st[pos0_index]}{pos1_index}")

            if game_board[f"{alpha_st[pos0_index]}{pos1_index}"] == "·":
                temp_moves.append(f"{alpha_st[pos0_index]}{pos1_index}")

            elif game_board[f"{alpha_st[pos0_index]}{pos1_index}"][0] == player:
                break

            else:
                temp_moves.append(f"{alpha_st[pos0_index]}{pos1_index}")
                break
            pos0_index -= 1
            pos1_index += 1
        moves += temp_moves[:]

        # right and down 🡖, start from pos
        temp_moves = []
        pos0_index = alpha_st.find(pos[0])+1
        pos1_index = int(pos[1])-1
        while (pos0_index < self.size) and (pos1_index >= 1):

            if game_board[f"{alpha_st[pos0_index]}{pos1_index}"] == "·":
                temp_moves.append(f"{alpha_st[pos0_index]}{pos1_index}")

            elif game_board[f"{alpha_st[pos0_index]}{pos1_index}"][0] == player:
                break

            else:
                temp_moves.append(f"{alpha_st[pos0_index]}{pos1_index}")
                break
            pos0_index += 1
            pos1_index -= 1
        moves += temp_moves[:]

        # right and up 🡗, start from pos
        temp_moves = []
        pos0_index = alpha_st.find(pos[0])+1
        pos1_index = int(pos[1])+1
        while (pos0_index < self.size) and (pos1_index <= self.size):

            if game_board[f"{alpha_st[pos0_index]}{pos1_index}"] == "·":
                temp_moves.append(f"{alpha_st[pos0_index]}{pos1_index}")

            elif game_board[f"{alpha_st[pos0_index]}{pos1_index}"][0] == player:
                break

            else:
                temp_moves.append(f"{alpha_st[pos0_index]}{pos1_index}")
                break
            pos0_index += 1
            pos1_index += 1
        moves += temp_moves[:]

        return moves

    def move_gen_king(self, pos: str, game_board:dict):
        """
        pos: string (e.g. "A1")\n
        return a list of legal move (include tile of enemy)
        """

        inside_board = lambda pos0, pos1: (pos0>=0) and (pos0<self.size) and (pos1>=1) and (pos1<=self.size)

        player = game_board[pos][0]
        alpha_st = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:self.size]
        moves = []

        # start from top and right 🡔 of pos
        # if tile is a piece:
        # same player -> pop all element
        # enemey -> pop all elemnt + add current position
        pos0_index = alpha_st.find(pos[0]) - 1
        pos1_index = int(pos[1]) - 1

        
        for i in range(3):
            for j in range(3): 
                if inside_board(pos0_index+i, pos1_index+j) and game_board[f"{alpha_st[pos0_index+i]}{pos1_index+j}"][0] != player and (pos0_index+i, pos1_index+j) != (pos0_index, pos1_index):
                    moves.append(f"{alpha_st[pos0_index+i]}{pos1_index+j}")

        return moves

    def move_gen_pawn(self, pos: str, game_board:dict):
        """
        Blue pawn can only move up, vice versa\n
        pos: string (e.g. "A1")\n
        return a list of legal move (include tile of enemy)
        """
        # if in OG position, can move forward twice

        inside_board = lambda pos0, pos1: (pos0>=0) and (pos0<self.size) and (pos1>=1) and (pos1<=self.size)

        player = game_board[pos][0]
        alpha_st = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:self.size]
        moves = []


        # if tile is a piece:
        # same player -> pop all element
        # enemey -> pop all elemnt + add current position
        pos0_index = alpha_st.find(pos[0])
        pos1_index = int(pos[1])

        # forward (up or down)
        # print(f"POS: {alpha_st[pos0_index]}{pos1_index}")
        pos1_index += 1 if player == "B" else -1
        if inside_board(pos0_index, pos1_index) and game_board[f"{alpha_st[pos0_index]}{pos1_index}"] == "·":
            moves.append(f"{alpha_st[pos0_index]}{pos1_index}")

        # capture diagonal enemy
        pos0_index -= 1 # 🡐
        if inside_board(pos0_index, pos1_index) and game_board[f"{alpha_st[pos0_index]}{pos1_index}"][0] not in f"·{player}":
            moves.append(f"{alpha_st[pos0_index]}{pos1_index}")
        pos0_index += 2 # 🡒
        if inside_board(pos0_index, pos1_index) and game_board[f"{alpha_st[pos0_index]}{pos1_index}"][0] not in f"·{player}":
            moves.append(f"{alpha_st[pos0_index]}{pos1_index}")

        # forward twice (up or down) if in init position
        pos0_index = alpha_st.find(pos[0])
        pos1_index += 1 if player == "B" else -1

        if (pos in self.pieces_init_pos[game_board[pos]]):
            if inside_board(pos0_index, pos1_index) and game_board[f"{alpha_st[pos0_index]}{pos1_index}"] == "·":
                moves.append(f"{alpha_st[pos0_index]}{pos1_index}")

        return moves

    def move_gen_knight(self, pos: str, game_board:dict):
        """
        pos: string (e.g. "A1")\n
        return a list of legal move (include tile of enemy)
        """

        inside_board = lambda pos0, pos1: (pos0>=0) and (pos0<self.size) and (pos1>=1) and (pos1<=self.size)

        player = game_board[pos][0]
        alpha_st = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:self.size]
        moves = []


        # if tile is a piece:
        # same player -> pop all element
        # enemey -> pop all elemnt + add current position
        pos0_index = alpha_st.find(pos[0])
        pos1_index = int(pos[1])


        # 🡔 2 move
        pos0_index -=2
        pos1_index +=1
        if inside_board(pos0_index, pos1_index) and game_board[f"{alpha_st[pos0_index]}{pos1_index}"][0] != player:
            moves.append(f"{alpha_st[pos0_index]}{pos1_index}")

        pos0_index +=1
        pos1_index +=1
        if inside_board(pos0_index, pos1_index) and game_board[f"{alpha_st[pos0_index]}{pos1_index}"][0] != player:
            moves.append(f"{alpha_st[pos0_index]}{pos1_index}")

        # 🡕 2 move
        pos0_index +=2
        if inside_board(pos0_index, pos1_index) and game_board[f"{alpha_st[pos0_index]}{pos1_index}"][0] != player:
            moves.append(f"{alpha_st[pos0_index]}{pos1_index}")

        pos0_index +=1
        pos1_index -=1
        if inside_board(pos0_index, pos1_index) and game_board[f"{alpha_st[pos0_index]}{pos1_index}"][0] != player:
            moves.append(f"{alpha_st[pos0_index]}{pos1_index}")

        # 🡖 2 move
        pos1_index -=2
        if inside_board(pos0_index, pos1_index) and game_board[f"{alpha_st[pos0_index]}{pos1_index}"][0] != player:
            moves.append(f"{alpha_st[pos0_index]}{pos1_index}")

        pos0_index -=1
        pos1_index -=1
        if inside_board(pos0_index, pos1_index) and game_board[f"{alpha_st[pos0_index]}{pos1_index}"][0] != player:
            moves.append(f"{alpha_st[pos0_index]}{pos1_index}")

        # 🡗 2 move
        pos0_index-=2
        if inside_board(pos0_index, pos1_index) and game_board[f"{alpha_st[pos0_index]}{pos1_index}"][0] != player:
            moves.append(f"{alpha_st[pos0_index]}{pos1_index}")

        pos0_index -=1
        pos1_index +=1
        if inside_board(pos0_index, pos1_index) and game_board[f"{alpha_st[pos0_index]}{pos1_index}"][0] != player:
            moves.append(f"{alpha_st[pos0_index]}{pos1_index}")




        return moves

    def avail_moves(self, player:str ,game_board:dict = None):
        """
        Generate a list of legal moves that player can do \n
        return a nested list of moves (E.g. [["A2", "A4"], [from_pos, to_pos], ...])
        """

        if player not in ["B", "R"]:
            raise ValueError(f"player variable is not B or R (player was {player})")

        if game_board == None:
            game_board = self.game_board

        move_set = []

        moveable_pieces = []
        pawn_pos = []
        knight_pos = []
        bishop_pos = []
        queen_pos = []
        rook_pos = []
        king_pos = []

        # Generate a list of moveable pieces
        for pos in game_board.keys():
            if game_board[pos][0] != f"{player}":
                continue
            if game_board[pos][1] == "P":
                pawn_pos += [pos]

            elif game_board[pos][1] == "N":
                knight_pos += [pos]

            elif game_board[pos][1] == "B":
                bishop_pos += [pos]

            elif game_board[pos][1] == "Q":
                queen_pos += [pos]

            elif game_board[pos][1] == "R":
                rook_pos += [pos]

            elif game_board[pos][1] == "K":
                king_pos += [pos]

        # prioritize pawn move over others
        moveable_pieces =   pawn_pos + knight_pos +   bishop_pos +  queen_pos + rook_pos + king_pos


        # Get all the moves the pieces can do
        for from_pos in moveable_pieces:
            for to_pos in self.move_generator(from_pos, game_board):
                move_set += [[from_pos, to_pos]]

        return move_set

    def undo(self, turn: int):
        """
        Return perious state of gameboard and allow player to go back
        turn: the number of turn player want to go back must < self.cache_size
        return 0
        """
        # this can be use when player make a checkmate move

        if turn > self.cache_size:
            return 0

        self.game_board = self.game_board_cache[-turn].copy()
        self.game_board_cache = self.game_board_cache[:-turn].copy()
        return 0

    def print_board_moves_visualize(self, moves: list):
        """
        Print game board and visualize the legal move of the pieces with terminal coloring\n
        moves: a list that contains all the legal move of that pieces\n
        return 0
        """

        temp_game_board = self.game_board.copy()
        for pos in moves:
            if temp_game_board[pos] == "·":
                temp_game_board[pos] = "x"
            else:
                temp_game_board[pos] += "x"
        alphas = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        alpha_st = " ".join(alphas[:self.size])
        click.secho(alpha_st.center(self.size*3))
        click.echo()

        for i in range(self.size, 0, -1):

            click.secho(f'{i}'.ljust(4), nl = False)

            for j in range(self.size):
                # Add color to game board and pieces

                # For empty spaces
                if (temp_game_board[(alphas[j])+str(i)]) == "·":
                    click.secho(f'{temp_game_board[(alphas[j])+str(i)]} ', fg='green', nl = False)
                elif len(temp_game_board[(alphas[j])+str(i)]) == 1:
                    click.secho(f'{temp_game_board[(alphas[j])+str(i)]} ', nl = False)

                # For pieces in kill range
                if (temp_game_board[(alphas[j])+str(i)][0]) == "R" and len((temp_game_board[(alphas[j])+str(i)])) == 3:
                    click.secho(f'{temp_game_board[(alphas[j])+str(i)][1]}',bg='white', fg='bright_red', nl = False)
                    click.secho(' ', nl = False)
                elif (temp_game_board[(alphas[j])+str(i)][0]) == "B" and len((temp_game_board[(alphas[j])+str(i)])) == 3:
                    click.secho(f'{temp_game_board[(alphas[j])+str(i)][1]}',bg='white',fg='bright_blue',nl = False)
                    click.secho(' ', nl = False)
                # For safe pieces
                elif (temp_game_board[(alphas[j])+str(i)][0]) == "R":
                    click.secho(f'{temp_game_board[(alphas[j])+str(i)][1]} ', fg='bright_red', nl = False)
                elif (temp_game_board[(alphas[j])+str(i)][0]) == "B":
                    click.secho(f'{temp_game_board[(alphas[j])+str(i)][1]} ', fg='bright_blue', nl = False)
                # print(temp_game_board[(alphas[j])+str(i)],end=" ")

            click.secho(f'{i}'.rjust(3))
        click.echo()
        click.secho(alpha_st.center(self.size*3))
        return 0

    def pawn_promotion_pos(self, player:str):
        """
        Detect any pawn that can be promoted\n
        return list of position of pawn that can be promoted
        """
        # Blue at bottom, red on top
        # scan boundary area for opposite size pawm

        alpha_st = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:self.size]
        pawn_2be_promoted = []

        col = 1 if player == "R" else self.size

        for row in alpha_st:
            if self.game_board[f"{row}{col}"] == f"{player}P":             
                pawn_2be_promoted += [f"{row}{col}"]

        return pawn_2be_promoted
        
    def pawn_promote(self, pos:str, promotion:str):
        """
        !!!Dangerous!!! This function does NOT check for pawn promotion condition \n
        Promote pawn to other pieces\n
        return bool: True if pawn has successfully promoted
        """
        if self.game_board[pos] == "·":
            return False
        elif promotion not in ["Q", "N", "R", "B"]:
            return False

        player = self.game_board[pos][0]
        self.game_board[pos] = player+promotion
        return True
    
    def king_is_dead(self,  game_board:dict = None):
        if game_board == None:
            game_board = self.game_board
        
        Red_king_is_dead = True
        Blue_king_is_dead = True

        for pos in game_board.keys():
            if game_board[pos] == "RK":
                Red_king_is_dead = False
            elif game_board[pos] == "BK":
                Blue_king_is_dead = False
        
        return Blue_king_is_dead or Red_king_is_dead

