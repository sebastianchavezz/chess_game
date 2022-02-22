import os
class Game_State():
    
    def __init__(self):
        #the first char is the color of the piece
        #the board is a 8x8 list
        # '--' represents an empty space
        self.board = [
            ['bR','bN','bB','bQ','bK','bB','bN','bR'],
            ['bP','bP','bP','bP','bP','bP','bP','bP'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['wP','wP','wP','wP','wP','wP','wP','wP'],
            ['wR','wN','wB','wQ','wK','wB','wN','wR']
        ]
        self.moveFunctions = {'P':self.getPawnMoves,'R':self.getRookMoves,'B':self.getBishopMoves,'N':self.getNightMoves,'Q':self.getQueenMoves,'K':self.getKingMoves}

                                
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7,4)
        self.blackKingLocation = (0,4)
        self.print_board()
        self.checkMate = False
        self.staleMate =False

    """
    makes move, this move is an object 
    """    
    def makeMove(self,move):
        #get piece moved
        self.board[move.startSqRow][move.startSqCol] = '--'
        #set the piece moved
        self.board[move.endSqRow][move.endSqCol] = move.pieceMoved
        #self.print_board()
        #print board
        self.moveLog.append(move)#append the move in log
        self.whiteToMove = not self.whiteToMove # switch turns
        #update kings location
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endSqRow, move.endSqCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endSqRow,move.endSqCol)

    """
    undo moves, thus it get the last move object and its attributes
    """
    def undo_move(self):
        if len(self.moveLog)!=0:
            move = self.moveLog.pop()
            self.board[move.startSqRow][move.startSqCol] = move.pieceMoved
            #set the piece moved
            self.board[move.endSqRow][move.endSqCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startSqRow, move.startSqCol)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startSqRow,move.startSqCol)
    """
    get valid moves considering checks
    """
    def get_validMoves(self):
        #1 generate all possible moves
        moves = self.get_all_possible_moves()
        #2 for each move, make move
        for i in range(len(moves)-1,-1,-1):# best way to remove a element from list
            self.makeMove(moves[i])
        #3 generate all opponent's move
            
        #4 for each of opponents moves, see if king is attacked
            self.whiteToMove = not self.whiteToMove
        #5 not valid if king is attacked
            if self.inCheck():
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove #switch turns back to original
            self.undo_move()
        #if there are no valid moves over, its either checkmate or stalemate
        if len(moves) == 0:
            if self.inCheck():
                self.checkMate = True
            else: 
                self.staleMate = True
        else:
            self.checkMate =False
            self.staleMate = False
        
        return moves

    """
    check is player is in check
    """
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0],self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0],self.blackKingLocation[1])

    '''
    determine if enemy can attack the square r, c
    '''
    def squareUnderAttack(self,r,c):
        self.whiteToMove = not self.whiteToMove #switch turns
        oppMoves = self.get_all_possible_moves()
        self.whiteToMove = not self.whiteToMove #switch turns back to original
        for move in oppMoves:
            if move.endSqRow == r and move.endSqCol == c:
                return True
        return False
        

    """
    generating all the possible legal moves for a specific piece
    """
    def get_all_possible_moves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if(turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r,c,moves) #call the oppropriate move function
        return moves
      
    """
    Add all legal moves for pawn
    """
    def getPawnMoves(self,r,c,moves):
        
        if self.whiteToMove:
            
            if self.board[r-1][c] == '--':#1sq pawn advance
                moves.append(Move((r,c),(r-1,c),self.board))
                #advance 2 squares
                if self.board[r-2][c] == '--' and r == 6:
                    moves.append(Move((r,c),(r-2,c),self.board))
            
            if c-1 >= 0:#must be in the bord
                if self.board[r-1][c-1][0] == 'b': #enemy piece to capture
                    moves.append((Move((r,c),(r-1,c-1),self.board)))
    
            if c+1 < len(self.board):#captures to the right
                if self.board[r-1][c+1][0]=='b':
                    moves.append((Move((r,c),(r-1,c+1),self.board)))
        
        else:#black pawn moves
            
            if self.board[r+1][c] == '--':
                moves.append(Move((r,c),(r+1,c),self.board))
                if self.board[r+2][c] == '--' and r == 1:
                    moves.append(Move((r,c),(r+2,c),self.board))

            if c-1 >= 0:#must be in the bord
                if self.board[r+1][c-1][0] == 'w': #enemy piece to capture
                    moves.append((Move((r,c),(r+1,c-1),self.board)))
                

            if c+1 < len(self.board):#captures to the right
                if self.board[r+1][c+1][0]=='w':
                    moves.append((Move((r,c),(r+1,c+1),self.board)))
    """
    Add all legal moves for rook
    """
    def getRookMoves(self,r,c,moves):
        if self.whiteToMove:
            #move UP
            for i in range(1,len(self.board)):
                if r+i >7 or self.board[r+i][c][0] == 'w':
                    break
                moves.append(Move((r,c),(r+i,c),self.board))
                if self.board[r+i][c][0] == 'b':
                    break

         #move DOWN
            for i in range(1,len(self.board)):
                if r-i <0 or self.board[r-i][c][0] == 'w':
                    break
                moves.append(Move((r,c),(r-i,c),self.board))
                if self.board[r-i][c][0] == 'b':
                    break
    
            #move to right
            for i in range(1,len(self.board)):
                if c+i > 7 or self.board[r][c+i][0] == 'w':
                    break
                moves.append(Move((r,c),(r,c+i),self.board))
                if self.board[r][c+i][0] == 'b':
                    break     
            #move to left
            for i in range(1,len(self.board)):
                if c-i < 0 or self.board[r][c-i][0] == 'w':
                    break
                moves.append(Move((r,c),(r,c-i),self.board))
                if self.board[r][c-i][0] == 'b':
                    break
        else: #black piece to play
            #move UP
            for i in range(1,len(self.board)):
                if r+i>7 or self.board[r+i][c][0] == 'b':
                    break
                moves.append(Move((r,c),(r+i,c),self.board))
                if self.board[r+i][c][0] == 'w':
                    break

            #move DOWN
            for i in range(1,len(self.board)):
                if r-i<0 or self.board[r-i][c][0] == 'b':
                    break
                moves.append(Move((r,c),(r-i,c),self.board))
                if self.board[r-i][c][0] == 'w':
                    break
    
            #move to right
            for i in range(1,len(self.board)):
                if c+i >7 or self.board[r][c+i][0] == 'b':                    
                    break
                moves.append(Move((r,c),(r,c+i),self.board))
                if self.board[r][c+i][0] == 'w':
                    break     
            #move to left
            for i in range(1,len(self.board)):
                if c-i<0 or self.board[r][c-i][0] == 'b':
                    break
                moves.append(Move((r,c),(r,c-i),self.board))
                if self.board[r][c-i][0] == 'w':
                    break        
     
    """             
    Add all legal moves for knight
    """
    def getNightMoves(self,r,c,moves):
        
        if self.whiteToMove:
            # L movement Under right
            if r+1<=7 and c+2<=7 and  (self.board[r+1][c+2] == '--' or self.board[r+1][c+2][0] == 'b'):
                moves.append(Move((r,c),(r+1,c+2),self.board))
            if r+2 <= 7 and c+1 <=7 and (self.board[r+2][c+1] == '--' or self.board[r+2][c+1][0] == 'b'):
                moves.append(Move((r,c),(r+2,c+1),self.board))

            #L movement UP right
            if r-1 >=0 and c+2 <=7 and (self.board[r-1][c+2] == '--' or self.board[r-1][c+2][0] == 'b'):
                moves.append(Move((r,c),(r-1,c+2),self.board))
            if r-2 >=0 and c+1 <=7 and (self.board[r-2][c+1] == '--' or self.board[r-2][c+1][0] == 'b'):
                moves.append(Move((r,c),(r-2,c+1),self.board))

            #L movement Under left
            if r+1<=7 and c-2 >=0 and  (self.board[r+1][c-2] == '--' or self.board[r+1][c-2][0] == 'b'):
                moves.append(Move((r,c),(r+1,c-2),self.board))
            if r+2 <= 7 and c-1 >=0 and (self.board[r+2][c-1] == '--' or self.board[r+2][c-1][0] == 'b'):
                moves.append(Move((r,c),(r+2,c-1),self.board))
            
            #L movement UP left
            if r-1>=0 and c-2>=0 and  (self.board[r-1][c-2] == '--' or self.board[r-1][c-2][0] == 'b'):
                moves.append(Move((r,c),(r-1,c-2),self.board))
            if r-2 >= 0 and c-1 >=0 and (self.board[r-2][c-1] == '--' or self.board[r-2][c-1][0] == 'b'):
                moves.append(Move((r,c),(r-2,c-1),self.board))

        else:
            if r+1<=7 and c+2<=7 and  (self.board[r+1][c+2] == '--' or self.board[r+1][c+2][0] == 'w'):
                moves.append(Move((r,c),(r+1,c+2),self.board))
            if r+2 <= 7 and c+1 <=7 and (self.board[r+2][c+1] == '--' or self.board[r+2][c+1][0] == 'w'):
                moves.append(Move((r,c),(r+2,c+1),self.board))
            
            #L movement UP right
            if r-1 >=0 and c+2 <=7 and (self.board[r-1][c+2] == '--' or self.board[r-1][c+2][0] == 'w'):
                moves.append(Move((r,c),(r-1,c+2),self.board))
            if r-2 >=0 and c+1 <=7 and (self.board[r-2][c+1] == '--' or self.board[r-2][c+1][0] == 'w'):
                moves.append(Move((r,c),(r-2,c+1),self.board))

            #L movement Under left
            if r+1<=7 and c-2 >=0 and  (self.board[r+1][c-2] == '--' or self.board[r+1][c-2][0] == 'w'):
                moves.append(Move((r,c),(r+1,c-2),self.board))
            if r+2 <= 7 and c-1 >=0 and (self.board[r+2][c-1] == '--' or self.board[r+2][c-1][0] == 'w'):
                moves.append(Move((r,c),(r+2,c-1),self.board))
            
            #L movement UP left
            if r-1>=0 and c-2>=0 and  (self.board[r-1][c-2] == '--' or self.board[r-1][c-2][0] == 'w'):
                moves.append(Move((r,c),(r-1,c-2),self.board))
            if r-2 >= 0 and c-1 >=0 and (self.board[r-2][c-1] == '--' or self.board[r-2][c-1][0] == 'w'):
                moves.append(Move((r,c),(r-2,c-1),self.board))

    """
    Add all legal moves for bishop
    """
    def getBishopMoves(self,r,c,moves):
        if self.whiteToMove:
            #move UP
            for i in range(1,len(self.board)):
                if r+i >7 or c+i >7 or self.board[r+i][c+i][0] == 'w':
                    break
                moves.append(Move((r,c),(r+i,c+i),self.board))
                if self.board[r+i][c+i][0] == 'b':
                    break

            #move DOWN
            for i in range(1,len(self.board)):
                if r-i <0 or c-i<0 or self.board[r-i][c-i][0] == 'w':
                    break
                moves.append(Move((r,c),(r-i,c-i),self.board))
                if self.board[r-i][c-i][0] == 'b':
                    break
    
            #move to right
            for i in range(1,len(self.board)):
                if r-i <0 or c+i > 7 or self.board[r-i][c+i][0] == 'w':
                    break
                moves.append(Move((r,c),(r-i,c+i),self.board))
                if self.board[r-i][c+i][0] == 'b':
                    break     
            #move to left
            for i in range(1,len(self.board)):
                if r+i >7 or c-i < 0 or self.board[r+i][c-i][0] == 'w':
                    break
                moves.append(Move((r,c),(r+i,c-i),self.board))
                if self.board[r+i][c-i][0] == 'b':
                    break
        else: #black piece to play
            #move UP
            for i in range(1,len(self.board)):
                if r+i >7 or c+i >7 or self.board[r+i][c+i][0] == 'b':
                    break
                moves.append(Move((r,c),(r+i,c+i),self.board))
                if self.board[r+i][c+i][0] == 'w':
                    break

            #move DOWN
            for i in range(1,len(self.board)):
                if r-i <0 or c-i<0 or self.board[r-i][c-i][0] == 'b':
                    break
                moves.append(Move((r,c),(r-i,c-i),self.board))
                if self.board[r-i][c-i][0] == 'w':
                    break
    
            #move to right
            for i in range(1,len(self.board)):
                if r-i <0 or c+i > 7 or self.board[r-i][c+i][0]  == 'b':                    
                    break
                moves.append(Move((r,c),(r-i,c+i),self.board))
                if self.board[r-i][c+i][0] == 'w':
                    break     
            #move to left
            for i in range(1,c+1):
                if r+i >7 or c-i < 0 or self.board[r+i][c-i][0] == 'b':
                    break
                moves.append(Move((r,c),(r+i,c-i),self.board))
                if self.board[r+i][c-i][0] == 'w':
                    break      
    """
    Add all legal moves for queen
    """
    def getQueenMoves(self,r,c,moves):
        self.getRookMoves(r,c,moves)
        self.getBishopMoves(r,c,moves)
    """
    Add all legal moves for king
    """
    def getKingMoves(self,r,c,moves):
        king_moves = ((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1))
        ally_color = 'w' if self.whiteToMove else 'b'
        for i in range(8):
            endRow = r + king_moves[i][0]
            endCol = c + king_moves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != ally_color:
                    moves.append(Move((r,c),(endRow,endCol),self.board))
    """
    Print the board
    """
    def print_board(self):
        os.system('cls')
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                print(self.board[i][j],end=' ')
            print(end='\n')
class Move():
    # maps keys to value
    #key, value
    ranksToRows = {'1':7,'2':6,'3':5,'4':4,'5':3,'6':2,'7':1,'8':0}
    rowsToRanks= {v:k for k,v in ranksToRows.items()}

    filesToCols = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'e':6,'h':7}
    colsToFiles = {v:k for k,v in filesToCols.items()}
    """
    Initialize the move object, every move made is an object
    """
    def __init__(self, startSq, endSq, board):
        self.startSqRow = startSq[0]
        #print(f'p1 row:{self.startSqRow}')
        self.startSqCol = startSq[1]
        #print(f'p1 col:{self.startSqCol}')
        self.endSqRow = endSq[0]
        #print(f'p2 row:{self.endSqRow}')
        self.endSqCol = endSq[1]
        #print(f'p2 col:{self.endSqCol}')
        
        
        self.pieceMoved = board[self.startSqRow][self.startSqCol]
        #print(f'move.pieve :{self.pieceMoved}')
        self.pieceCaptured = board[self.endSqRow][self.endSqCol]
        #unique id for a specific move
        self.moveID = self.startSqCol*1000+self.startSqCol *100+self.endSqRow*10+self.endSqCol
        
    """
    Overriding the equals method
    """
    def __eq__(self,other):
        if isinstance(other,Move):
            return self.moveID == other.moveID
        return False
    
    def getChessNotation(self)->str:
        #this prints real notation
        x = self.getRankFile(self.startSqRow, self.startSqCol)
        y = self.getRankFile(self.endSqRow,self.endSqCol)
        z = x+y
        return z


    def getRankFile(self,row,col)->str:
        x = self.colsToFiles[col]
        y =self.rowsToRanks[row]
        z = x+y
        return z
