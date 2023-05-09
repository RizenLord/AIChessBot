import chess
import chess.svg
import chess.polyglot
import random
from copy import deepcopy
from tkinter import *
from tkhtmlview import HTMLLabel

reader = chess.polyglot.open_reader("data/polyglot/baron30.bin")

currBoard = chess.Board()
print(currBoard.legal_moves)
moveCount = 0

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
                currBoard.push(plrMove)
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

moveCount = 0

while gameComplete(currBoard) == -1:
    print(currBoard)
    if moveCount % 2 == 0:
        getPLRmove(currBoard.legal_moves)
        moveCount += 1
    elif moveCount % 2 != 0:
        currBoard.push(engineDepth(currBoard, 3))
        moveCount += 1
