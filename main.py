import chess
import chess.svg
import chess.polyglot
import pygame
import math
from copy import deepcopy
import time

pygame.init()
screen = pygame.display.set_mode((820, 580), pygame.NOFRAME)
pygame.display.set_caption('Clownfish 1 Engine')
font = pygame.font.Font('data/fonts/calibri.ttf', 24)

currBoard = chess.Board()

DARKORANGE = (183, 65, 14)
LIGHTORANGE = (140,65,0)

pieces = {'p': pygame.image.load('data/images/b_pawn.png'),
          'n': pygame.image.load('data/images/b_knight.png'),
          'b': pygame.image.load('data/images/b_bishop.png'),
          'r': pygame.image.load('data/images/b_rook.png'),
          'q': pygame.image.load('data/images/b_queen.png'),
          'k': pygame.image.load('data/images/b_king.png'),
          'P': pygame.image.load('data/images/w_pawn.png'),
          'N': pygame.image.load('data/images/w_knight.png'),
          'B': pygame.image.load('data/images/w_bishop.png'),
          'R': pygame.image.load('data/images/w_rook.png'),
          'Q': pygame.image.load('data/images/w_queen.png'),
          'K': pygame.image.load('data/images/w_king.png'),
          
          }

wSquare = pygame.image.load('data/images/w_square.png')
dSquare = pygame.image.load('data/images/d_square.png')
engineIcon = pygame.image.load('data/images/clownfishengine.png')
x60Icon = pygame.image.load('data/images/60x60engine.png') 

startPos = list(chess.STARTING_BOARD_FEN.split("/"))

aiText = font.render('Black: Clownfish Depth 3', True, 'white')
plrText = font.render('White: Player', True, 'white')
titleText = font.render('Clownfish 1 Engine', True, 'white')

screen.fill(LIGHTORANGE)

    # Board Coords
    # Top Left 20, 80 
    # Bottom Right 500, 560
    # Top Right 500, 80
    # Bottom Left 20, 560

        
def drawTaskbar():
    pygame.draw.rect(screen,(DARKORANGE), pygame.Rect(20,20,780,40))
    screen.blit(x60Icon, (10,12.5))
    screen.blit(titleText, (80,30))
    pygame.draw.rect(screen,'black', pygame.Rect(760,20,40,40))

def drawSidebar():
    screen.blit(plrText, (520, 90))
    screen.blit(aiText, (520, 130))


def drawPieces(pos, started=False):
    if started:
        drawBoard(True)
    x = 20
    y = 20
    for i in range(len(pos)):
        x = 20
        y += 60
        currRow = pos[i]
        if i == 7:
            lastRow = currRow.split(" ")
            currRow = lastRow[0]
            #print(f"last row: {lastRow[0]}")
        for j in range(len(currRow)):
            if currRow[j] in pieces.keys():
                screen.blit(pieces[currRow[j]], (x,y))
            elif currRow[j].isdigit():
                if currRow[j] == '8':
                    break
                else:
                    x += ((int(currRow[j])) * 60) - 60
            x += 60



def drawBoard(started=False):
    x = 20
    y = 20
    for i in range(8):
        x = 20
        y += 60
        for j in range(8):
            if (i % 2) == (j % 2):
                screen.blit(wSquare, (x,y))
            else:
                screen.blit(dSquare, (x,y))
            x += 60
    if started == False:
        drawPieces(startPos, False)
    started = True


drawBoard(False)
drawSidebar()
drawTaskbar()
pygame.display.flip()
        

    # Opening Book, Purely so the Engine can make intelligent Opening Moves
reader = chess.polyglot.open_reader("data/polyglot/baron30.bin")

pieceValues = {'p': -1,
            'n': -3,
            'b': -3,
            'r': -5,
            'q': -9,
            'k': 0,
            'P': 1,
            'N': 3,
            'B': 3,
            'R': 5,
            'Q': 9,
            'K': 0,
            
            }


def boardEval(BOARD):
        eval = 0
        pieces = BOARD.piece_map()
        for key in pieces:
            eval += pieceValues[str(pieces[key])]
        return eval

def spaceEval(BOARD):
        noMoves = len(list(BOARD.legal_moves))
        value = (noMoves / (20 + noMoves))

        if BOARD.turn == True:
            return value
        else:
            return -value

def getBestMove(BOARD, DEPTH):
        openingMove = reader.get(BOARD)
        if openingMove == None:
            pass
        else:
            return openingMove.move
        
        posMoves = list(BOARD.legal_moves)
        scores = []

        for move in posMoves:
            tmpBoard = deepcopy(BOARD)
            tmpBoard.push(move)

            outcome = tmpBoard.outcome()

            if outcome == None:
                if DEPTH > 1:
                    tmpBestMove = getBestMove(tmpBoard, DEPTH-1)
                    tmpBoard.push(tmpBestMove)
                scores.append(boardEval(tmpBoard))

            elif tmpBoard.is_checkmate():
                return move
            
            else:
                # Super High Number to Discourage Draws
                val = 1000
                if BOARD.turn == True:
                    scores.append(-val)
                else:
                    scores.append(val)
            
            scores[-1] = scores[-1] + spaceEval(tmpBoard)

        
        if BOARD.turn == True:
            bestMove = posMoves[scores.index(max(scores))]
        else:
            bestMove = posMoves[scores.index(min(scores))]

        return bestMove

def engineDepth(BOARD, DEPTH):
        return(getBestMove(BOARD, DEPTH)) 

def getPLRmove(legalMoves): 
        while True:
            try:
                plrMove = input("Your Move: ")
                if chess.Move.from_uci(plrMove) not in legalMoves:
                    print("Please Enter a Legal Move\n")
                else:
                    currBoard.push_san(plrMove)
                    break
            except ValueError:
                print("Please Enter a String")
                continue
        return plrMove

def main(board, aiColor):
    playing = True
    boardPos = list((board.fen()).split("/"))

    posMoves = []

    while playing:
        drawPieces(boardPos)

        if board.turn == aiColor:
            aiMove = engineDepth(currBoard, 3)
            time.sleep(1)
            board.push(aiMove)
            boardPos = list((board.fen()).split("/"))
            drawPieces(boardPos, True)
            aiBeforeX = (60*((aiMove.from_square)%8)) + 20
            aiBeforeY = (60*(7-(aiMove.from_square)//8)) + 80
            aiAfterX = (60*((aiMove.to_square)%8)) + 20
            aiAfterY = (60*(7-(aiMove.to_square)//8)) + 80
            pygame.draw.rect(screen,"green",pygame.Rect(aiBeforeX, aiBeforeY,60,60),5)
            pygame.draw.rect(screen,"green",pygame.Rect(aiAfterX, aiAfterY,60,60),5)
            pygame.display.flip()
        else:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    playing = False
                if event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_ESCAPE) or  (event.type == pygame.QUIT):
                        playing = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    drawPieces(boardPos, True)
                    mousePos = pygame.mouse.get_pos()
                    print(mousePos)
                    if ((mousePos[0] >= 20) and (mousePos[0] <= 500)) and ((mousePos[1] >= 80) and (mousePos[1] <= 560)):
                        squareSelected = ((math.floor((mousePos[0]- 20)/60)) ,(math.floor((mousePos[1]-80)/60)))
                        #print(squareSelected)
                        index = (7-squareSelected[1])*8+(squareSelected[0])
                        #print(index)
                        if index in posMoves:
                            move = moves[posMoves.index(index)]
                            board.push(move)
                            before = move.from_square
                            beforeX = (60*(before%8)) + 20
                            beforeY = (60*(7-before//8)) + 80
                            MafterX = (60*((move.to_square)%8)) + 20
                            MafterY = (60*(7-(move.to_square)//8)) + 80
                            boardPos = list((board.fen()).split("/"))
                            drawPieces(boardPos, True)
                            pygame.draw.rect(screen,"green",pygame.Rect(beforeX, beforeY,60,60),5)
                            pygame.draw.rect(screen,"green",pygame.Rect(MafterX, MafterY,60,60),5)
                            pygame.display.flip()

                            index = None
                            posMoves = []
                        
                        else:
                            pieceSelected = board.piece_at(index)

                            if pieceSelected == None:
                                pass
                            else:
                                legalMoves = list(board.legal_moves)
                                moves = []
                                for i in legalMoves:
                                    if i.from_square == index:
                                        moves.append(i)
                                        after = i.to_square
                                        afterX = (60*(after%8)) + 20
                                        afterY = (60*(7-after//8)) + 80
                                        
                                        pygame.draw.rect(screen,"blue",pygame.Rect(afterX,afterY,60,60),5)
                                        pygame.display.flip()
                                posMoves = [a.to_square for a in moves]
                                #print(posMoves)
                    elif ((mousePos[0] >= 760) and (mousePos[0] <= 800)) and ((mousePos[1] >= 20) and (mousePos[1] <= 60)):
                        playing = False
                    else:
                        pass
            if board.outcome() != None:
                print(board.outcome())
                playing = False
                print(board)
    pygame.quit()

main(currBoard, False)