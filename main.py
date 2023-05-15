import chess
import chess.svg
import chess.polyglot
import pygame
import math
from copy import deepcopy


pygame.init()
screen = pygame.display.set_mode((820, 520))
pygame.display.set_caption('Humanized AI Engine')

currBoard = chess.Board()
moveCount = 0

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

startPos = list(chess.STARTING_BOARD_FEN.split("/"))
screen.fill("black")

def drawPieces(pos, started=False):
    if started:
        drawBoard(True)
    x = 20
    y = -40
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
    y = -40
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
pygame.display.flip()

def main(board):
    playing = True
    boardPos = list((board.fen()).split("/"))

    posMoves = []

    while playing:
        drawPieces(boardPos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                drawBoard(False)
                mousePos = pygame.mouse.get_pos()

                squareSelected = ((math.floor((mousePos[0] - 20)/60)) ,(math.floor((mousePos[1]- 20)/60)))
                print(squareSelected)
                index = (7-squareSelected[1])*8+(squareSelected[0])
                print(index)

                if index in posMoves:
                    move = moves[posMoves.index(index)]
                    board.push(move)

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
                                afterY = (60*(7-after//8)) + 20

                                pygame.draw.rect(screen,"blue",pygame.Rect(afterX,afterY,60,60),5)
                                pygame.display.flip()
                        posMoves = [a.to_square for a in moves]
        if board.outcome() != None:
            print(board.outcome())
            playing = False
            print(board)
    pygame.quit()

main(currBoard)
    # Board Coords
    # Top Left 20, 20 
    # Bottom Right 500, 500
    # Top Right 500, 20
    # Bottom Left 20, 500
    
        

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

def gameComplete(board):
        board = board
        outcome = board.outcome()
        if outcome:
            if outcome.winner == chess.WHITE:
                return 1
            elif outcome.winner == chess.BLACK:
                return 0
            else:
                return 2
        else:
            return -1

if moveCount % 2 == 0:
        getPLRmove(currBoard.legal_moves)
        currBoardFEN = list((currBoard.fen()).split("/"))
        drawPieces(currBoardFEN, True)
        moveCount += 1
elif moveCount % 2 != 0:
        currBoard.push(engineDepth(currBoard, 3))
        currBoardFEN = list((currBoard.fen()).split("/"))
        drawPieces(currBoardFEN, True)
        moveCount += 1
pygame.quit()