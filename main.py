import openai
import chess

openai.api_key = "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"

board = chess.Board()
moves = []
moveCount = 0

def getGPTmove(moves, legalMoves):
    while True:
        try:
            selectedMove = openai.Completion.create(
                model="gpt-3.5-turbo",
                temperature=0,
                max_tokens=6,
                prompt="Play Chess: " + ', '.join(moves),
            )
            if chess.Move.from_uci(selectedMove) in legalMoves:
                board.push_san(selectedMove)
                print(selectedMove)
                break
        except ValueError:
            print("AI Entered Invalid String")
            print(selectedMove)
            continue

    return selectedMove

def getPLRmove(legalMoves): 
    while True:
        try:
            plrMove = input("Your Move: ")
            if chess.Move.from_uci(plrMove) not in legalMoves:
                print("Please Enter a Legal Move\n")
            else:
                board.push_san(plrMove)
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
            
while gameComplete(board) == -1:
    print(board)
    if moveCount % 2 == 0:
        moves.append(getPLRmove(board.legal_moves))
        moveCount += 1
    elif moveCount % 2 != 0:
        moves.append(getGPTmove(moves, board.legal_moves))
        moveCount += 1
