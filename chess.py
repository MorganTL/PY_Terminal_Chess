import click

# click docs : https://click.palletsprojects.com/en/8.1.x/utils/
# Type "python chess.py" in terminal to run

class game_board():

    def __init__(self, size: int):
        self.size = size
        self.game_board = self.make_board(size)
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
        click.secho(alpha_st.center(self.size*3), fg="bright_white")
        click.echo()

        for i in range(self.size, 0, -1):            

            click.secho(f'{i}'.ljust(4), fg="bright_white", nl = False)

            for j in range(self.size):
                # Add color to game board and pieces
                if (self.game_board[(alphas[j])+str(i)]) == "·":
                    click.secho(f'{self.game_board[(alphas[j])+str(i)]} ', fg='green', nl = False)
                elif len(self.game_board[(alphas[j])+str(i)]) == 1:
                    click.secho(f'{self.game_board[(alphas[j])+str(i)]} ', fg='bright_white', nl = False)                
                elif (self.game_board[(alphas[j])+str(i)][0]) == "R":
                    click.secho(f'{self.game_board[(alphas[j])+str(i)][1]} ', fg='bright_red', nl = False)
                elif (self.game_board[(alphas[j])+str(i)][0]) == "B":
                    click.secho(f'{self.game_board[(alphas[j])+str(i)][1]} ', fg='bright_blue', nl = False)
                # print(self.game_board[(alphas[j])+str(i)],end=" ")

            click.secho(f'{i}'.rjust(3), fg="bright_white")
        click.echo()
        click.secho(alpha_st.center(self.size*3), fg="bright_white")
        return 0
    
    
    def move_piece(self, pos:str, to:str):
        """
        !!Dangerous!! This function does not provide movement checking\n
        Teleport piece on "pos" -> "to"       
        pos: string (e.g. "A1")
        to: string (e.g. "B1")

        return True when move is successful, False when pos is empty space
        """

        piece = self.game_board[pos]
        if piece == "·":
            return False
        
        self.game_board[to] = piece
        self.game_board[pos] = "·"
        return True


        pass

    def move_generator(self, pos: str):
        """        
        pos: string (e.g. "A1")\n
        return a list of legal moves that the pieces can do
        """
        if (self.game_board[pos]) == "·":
            return []
        piece = self.game_board[pos][1]
        
        # click.secho(f"At {pos}, there is {piece}", fg="green")

        if piece == "R":
            return self.move_gen_rook(pos)

        elif piece == "B":
            return self.move_gen_bishop(pos)
        
        elif piece == "Q":
            return self.move_gen_bishop(pos) + self.move_gen_rook(pos)
        
        elif piece == "K":
            return self.move_gen_king(pos)

        elif piece == "P":
            return self.move_gen_pawn(pos)

        elif piece == "N":
            return self.move_gen_knight(pos)
               

    def move_gen_rook(self, pos: str):
        """
        pos: string (e.g. "A1")\n
        return a list of legal move (include tile of enemy)       
        """
        player = self.game_board[pos][0]        
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
            
            if self.game_board[f"{x}{pos[1]}"] == "·":
                temp_moves.append(f"{x}{pos[1]}")

            elif self.game_board[f"{x}{pos[1]}"][0] == player:
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
            
            if self.game_board[f"{x}{pos[1]}"] == "·":
                temp_moves.append(f"{x}{pos[1]}")

            elif self.game_board[f"{x}{pos[1]}"][0] == player:
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

            if self.game_board[f"{pos[0]}{y}"] == "·":
                temp_moves.append(f"{pos[0]}{y}")

            elif self.game_board[f"{pos[0]}{y}"][0] == player:
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
            
            if self.game_board[f"{pos[0]}{y}"] == "·":
                temp_moves.append(f"{pos[0]}{y}")

            elif self.game_board[f"{pos[0]}{y}"][0] == player:
                temp_moves = []

            else:
                temp_moves = []
                temp_moves.append(f"{pos[0]}{y}")

        moves += temp_moves[::-1]
        return moves

    def move_gen_bishop(self, pos: str):
        """
        pos: string (e.g. "A1")\n
        return a list of legal move (include tile of enemy)       
        """
        player = self.game_board[pos][0]        
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

            if self.game_board[f"{alpha_st[pos0_index]}{pos1_index}"] == "·":
                temp_moves.append(f"{alpha_st[pos0_index]}{pos1_index}")

            elif self.game_board[f"{alpha_st[pos0_index]}{pos1_index}"][0] == player:
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

            if self.game_board[f"{alpha_st[pos0_index]}{pos1_index}"] == "·":
                temp_moves.append(f"{alpha_st[pos0_index]}{pos1_index}")

            elif self.game_board[f"{alpha_st[pos0_index]}{pos1_index}"][0] == player:
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

            if self.game_board[f"{alpha_st[pos0_index]}{pos1_index}"] == "·":
                temp_moves.append(f"{alpha_st[pos0_index]}{pos1_index}")

            elif self.game_board[f"{alpha_st[pos0_index]}{pos1_index}"][0] == player:
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

            if self.game_board[f"{alpha_st[pos0_index]}{pos1_index}"] == "·":
                temp_moves.append(f"{alpha_st[pos0_index]}{pos1_index}")

            elif self.game_board[f"{alpha_st[pos0_index]}{pos1_index}"][0] == player:
                break

            else:
                temp_moves.append(f"{alpha_st[pos0_index]}{pos1_index}")
                break
            pos0_index += 1
            pos1_index += 1
        moves += temp_moves[:] 

        return moves
            
    def move_gen_king(self, pos: str):
        """
        pos: string (e.g. "A1")\n
        return a list of legal move (include tile of enemy)       
        """       

        inside_board = lambda pos0, pos1: (pos0>=0) and (pos0<self.size) and (pos1>=1) and (pos1<=self.size)

        player = self.game_board[pos][0]        
        alpha_st = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:self.size]
        moves = []   

        # left and down 🡗, start from pos
        # if tile is a piece:
        # same player -> pop all element
        # enemey -> pop all elemnt + add current position
        pos0_index = alpha_st.find(pos[0])
        pos1_index = int(pos[1])

        # 🡐
        pos0_index -= 1
        # print(f"POS: {alpha_st[pos0_index]}{pos1_index}")
        if inside_board(pos0_index, pos1_index) and self.game_board[f"{alpha_st[pos0_index]}{pos1_index}"][0] != player:
            moves.append(f"{alpha_st[pos0_index]}{pos1_index}")
        
        # 🡔
        pos1_index += 1
        # print(f"POS: {alpha_st[pos0_index]}{pos1_index}")
        if inside_board(pos0_index, pos1_index) and self.game_board[f"{alpha_st[pos0_index]}{pos1_index}"][0] != player:
            moves.append(f"{alpha_st[pos0_index]}{pos1_index}")
          
        # 🡑
        pos0_index += 1
        # print(f"POS: {alpha_st[pos0_index]}{pos1_index}")
        if inside_board(pos0_index, pos1_index) and self.game_board[f"{alpha_st[pos0_index]}{pos1_index}"][0] != player:
            moves.append(f"{alpha_st[pos0_index]}{pos1_index}")

        # 🡕
        pos0_index += 1
        # print(f"POS: {alpha_st[pos0_index]}{pos1_index}")
        if inside_board(pos0_index, pos1_index) and self.game_board[f"{alpha_st[pos0_index]}{pos1_index}"][0] != player:
            moves.append(f"{alpha_st[pos0_index]}{pos1_index}")

        # 🡒
        pos1_index -= 1
        # print(f"POS: {alpha_st[pos0_index]}{pos1_index}")
        if inside_board(pos0_index, pos1_index) and self.game_board[f"{alpha_st[pos0_index]}{pos1_index}"][0] != player:
            moves.append(f"{alpha_st[pos0_index]}{pos1_index}")

        # 🡖
        pos1_index -= 1
        # print(f"POS: {alpha_st[pos0_index]}{pos1_index}")
        if inside_board(pos0_index, pos1_index) and self.game_board[f"{alpha_st[pos0_index]}{pos1_index}"][0] != player:
            moves.append(f"{alpha_st[pos0_index]}{pos1_index}")

        # 🡓
        pos0_index -= 1
        # print(f"POS: {alpha_st[pos0_index]}{pos1_index}")
        if inside_board(pos0_index, pos1_index) and self.game_board[f"{alpha_st[pos0_index]}{pos1_index}"][0] != player:
            moves.append(f"{alpha_st[pos0_index]}{pos1_index}")

        # 🡗
        pos0_index -= 1
        # print(f"POS: {alpha_st[pos0_index]}{pos1_index}")
        if inside_board(pos0_index, pos1_index) and self.game_board[f"{alpha_st[pos0_index]}{pos1_index}"][0] != player:
            moves.append(f"{alpha_st[pos0_index]}{pos1_index}")

        return moves

    def move_gen_pawn(self, pos: str):
        """
        Blue pawn can only move up, vice versa\n
        pos: string (e.g. "A1")\n
        return a list of legal move (include tile of enemy)       
        """
        # if in OG position, can move forward twice

        inside_board = lambda pos0, pos1: (pos0>=0) and (pos0<self.size) and (pos1>=1) and (pos1<=self.size)

        player = self.game_board[pos][0]        
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
        if inside_board(pos0_index, pos1_index) and self.game_board[f"{alpha_st[pos0_index]}{pos1_index}"] == "·":
            moves.append(f"{alpha_st[pos0_index]}{pos1_index}")

        # capture diagonal enemy
        pos0_index -= 1 # 🡐
        if inside_board(pos0_index, pos1_index) and self.game_board[f"{alpha_st[pos0_index]}{pos1_index}"][0] not in f"·{player}":
            moves.append(f"{alpha_st[pos0_index]}{pos1_index}")
        pos0_index += 2 # 🡒
        if inside_board(pos0_index, pos1_index) and self.game_board[f"{alpha_st[pos0_index]}{pos1_index}"][0] not in f"·{player}":
            moves.append(f"{alpha_st[pos0_index]}{pos1_index}")

        # forward twice (up or down) if in init position
        pos0_index = alpha_st.find(pos[0])
        pos1_index += 1 if player == "B" else -1

        if (pos in self.pieces_init_pos[self.game_board[pos]]):
            if inside_board(pos0_index, pos1_index) and self.game_board[f"{alpha_st[pos0_index]}{pos1_index}"] == "·":
                moves.append(f"{alpha_st[pos0_index]}{pos1_index}")

        return moves

    def move_gen_knight(self, pos: str):
        """
        pos: string (e.g. "A1")\n
        return a list of legal move (include tile of enemy)       
        """

        inside_board = lambda pos0, pos1: (pos0>=0) and (pos0<self.size) and (pos1>=1) and (pos1<=self.size)

        player = self.game_board[pos][0]        
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
        if inside_board(pos0_index, pos1_index) and self.game_board[f"{alpha_st[pos0_index]}{pos1_index}"][0] != player:
            moves.append(f"{alpha_st[pos0_index]}{pos1_index}")

        pos0_index +=1
        pos1_index +=1
        if inside_board(pos0_index, pos1_index) and self.game_board[f"{alpha_st[pos0_index]}{pos1_index}"][0] != player:
            moves.append(f"{alpha_st[pos0_index]}{pos1_index}")       

        # 🡕 2 move
        pos0_index +=2
        if inside_board(pos0_index, pos1_index) and self.game_board[f"{alpha_st[pos0_index]}{pos1_index}"][0] != player:
            moves.append(f"{alpha_st[pos0_index]}{pos1_index}")

        pos0_index +=1
        pos1_index -=1
        if inside_board(pos0_index, pos1_index) and self.game_board[f"{alpha_st[pos0_index]}{pos1_index}"][0] != player:
            moves.append(f"{alpha_st[pos0_index]}{pos1_index}")

        # 🡖 2 move
        pos1_index -=2
        if inside_board(pos0_index, pos1_index) and self.game_board[f"{alpha_st[pos0_index]}{pos1_index}"][0] != player:
            moves.append(f"{alpha_st[pos0_index]}{pos1_index}")

        pos0_index -=1
        pos1_index -=1
        if inside_board(pos0_index, pos1_index) and self.game_board[f"{alpha_st[pos0_index]}{pos1_index}"][0] != player:
            moves.append(f"{alpha_st[pos0_index]}{pos1_index}")

        # 🡗 2 move
        pos0_index-=2
        if inside_board(pos0_index, pos1_index) and self.game_board[f"{alpha_st[pos0_index]}{pos1_index}"][0] != player:
            moves.append(f"{alpha_st[pos0_index]}{pos1_index}")
        
        pos0_index -=1
        pos1_index +=1
        if inside_board(pos0_index, pos1_index) and self.game_board[f"{alpha_st[pos0_index]}{pos1_index}"][0] != player:
            moves.append(f"{alpha_st[pos0_index]}{pos1_index}")
        



        return moves
    

    def move_gen_castling(self, pos: str):
        """
        TODO: detect move is legal for castling\n
        pos: string (e.g. "A1")\n
        return a list of legal move (include tile of enemy)       
        """
        # king cannot be moves
        # rook cannot have moved
        # king cannot be checked
        # king cannot moved pass potential check/attack grid 
        pass


    def undo(self):
        """
        TODO: save perious state of gameboard and allow player to go back 
        """
        pass


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
        click.secho(alpha_st.center(self.size*3), fg="bright_white")
        click.echo()

        for i in range(self.size, 0, -1):            

            click.secho(f'{i}'.ljust(4), fg="bright_white", nl = False)

            for j in range(self.size):
                # Add color to game board and pieces

                # For empty spaces
                if (temp_game_board[(alphas[j])+str(i)]) == "·":
                    click.secho(f'{temp_game_board[(alphas[j])+str(i)]} ', fg='green', nl = False)
                elif len(temp_game_board[(alphas[j])+str(i)]) == 1:
                    click.secho(f'{temp_game_board[(alphas[j])+str(i)]} ', fg='bright_white', nl = False)

                # For pieces in kill range
                if (temp_game_board[(alphas[j])+str(i)][0]) == "R" and len((temp_game_board[(alphas[j])+str(i)])) == 3:
                    click.secho(f'{temp_game_board[(alphas[j])+str(i)][1]}',bg='white', fg='bright_red',bold=True, nl = False)
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

            click.secho(f'{i}'.rjust(3), fg="bright_white")
        click.echo()
        click.secho(alpha_st.center(self.size*3), fg="bright_white")
        return 0


def main():
    click.clear()
    game = game_board(8)
    # click.pause()
    game.game_board["B8"] = 'RK' #not recommended, use fill_pieces_on_board function instead
    game.game_board["G2"] = 'BK'

    #Blue at bottom, red on top
    game.fill_pieces_on_board({"BQ": ["C6"], "RR": ["C4", "H8"]})
    click.secho("-----------------------")
    game.print_board() 
    
    click.secho("-----------------------")
    game.print_board_moves_visualize(game.move_generator("C6"))
    game.move_piece("C6", "C4")

    click.secho("-----------------------")
    game.print_board()
    # game.print_board()

    # print(game.game_board)
    # click.clear()
    


if __name__ == "__main__":
    main()
    
