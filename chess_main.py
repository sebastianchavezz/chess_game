
import pygame as p
from chess_engine import Game_State, Move

WIDTH = HEIGHT = 512
DIMENSION = 8 #dimension fo the board

SQ_SIZE = WIDTH // DIMENSION #square size
MAX_FPS = 20 #frames per second
IMAGES = {}#dic full of the images

#init the dic full of images as a variables; only 1 time

def loadImages():
    pieces = ['wP','wR','wN','wB','wQ','wK','bP','bR','bN','bB','bQ','bK',]

    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(f'./images/{piece}.png'),(SQ_SIZE,SQ_SIZE))
    
    #use image by using the dic


def main():
    p.init()
    screen = p.display.set_mode((WIDTH,HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color('white'))
    game_state= Game_State()
    validMoves = game_state.get_validMoves()#reference to legal valid mover per object
    moveMade = False #flag variable for when a move is made
    loadImages()
    running = True
    sqSelected = ()#keep track of the last pos as tuple,(rol,col)
    playerClicks = []#keep track of players click as two tuples
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()#get x,y from mouse
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                
                if sqSelected == (row,col): #player clicked the same square twice
                    
                    sqSelected = ()#deseleced
                    playerClicks = []#clear player clicks
                else:
                    sqSelected = (row,col)
                    playerClicks.append(sqSelected)
                
                if len(playerClicks) ==  2:
                    #after player clicks
                    move = Move(playerClicks[0],playerClicks[1],game_state.board) #generade move
                    #print(move.getChessNotation())
                    if move in validMoves: #if move is in legal moves
                        game_state.makeMove(move)
                        moveMade = True #check if move is check
                        sqSelected = () #reset user input
                        playerClicks = []

                    else:
                        playerClicks = [sqSelected]
            
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: #undo when Z is pressed
                    game_state.undo_move()
                    moveMade = True #calls moveMade

        if moveMade: #generate new validMoves 
            validMoves = game_state.get_validMoves()
            moveMade = False      
        drawGameState(screen,game_state)
        clock.tick(MAX_FPS) 
        p.display.flip()

#responsibles of the gamestate
def drawGameState(screen,game_state):
    drawBoard(screen)# draw lines and board
    drawPieces(screen, game_state.board) #draw the pieces on the board    


#draw board
def drawBoard(screen):
    colors = [p.Color('white'),p.Color('gray')]
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colors[((row+col)%2)]
            p.draw.rect(screen,color,p.Rect(col*SQ_SIZE,row*SQ_SIZE,SQ_SIZE,SQ_SIZE))


#draw pieces
def drawPieces(screen, board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            #get name of piece in board; this name is also the file name
            piece = board[row][col]
            if piece != '--':
                screen.blit(IMAGES[piece],p.Rect(col*SQ_SIZE,row*SQ_SIZE,SQ_SIZE,SQ_SIZE))

if __name__ == "__main__":
    main()



