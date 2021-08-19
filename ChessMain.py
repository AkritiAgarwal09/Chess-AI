import pygame as p
from Ches import ChessEngine

import math

width = height = 512
dim = 8  # Dimensions (8x8)
sqsize = height // dim
maxfps = 15
images = {}


def loadImages():
    pieces = ["wP", "wR", "wN", "wB", "wQ", "wK", "bP", "bR", "bN", "bB", "bQ", "bK"]
    for piece in pieces:
        images[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (sqsize, sqsize))


def main():
    p.init()
    screen = p.display.set_mode((width, height))
    clock = p.time.Clock()
    screen.fill(p.Color("White"))

    gs = ChessEngine.GameState()
    validMoves = gs.gVM()
    gameOver =  False
    moveMade = False
    animate = False
    loadImages()
    running = True

    sqSelected = ()
    playerClicks = []
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            elif e.type == p.MOUSEBUTTONDOWN and gs.whiteToMove:
                if not gameOver:

                    location = p.mouse.get_pos()
                    col = location[0] // sqsize
                    row = location[1] // sqsize
                    if sqSelected == (row, col):
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)

                    if len(playerClicks) == 2:
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.tomakeMove(validMoves[i])
                                moveMade = True
                                animate = True
                                sqSelected = ()
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]


            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = True
                    animate = False

        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.gVM()
            moveMade = False
            animate = False
        drawGameState(screen, gs,validMoves, sqSelected)

        if gs.checkMate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, 'Black wins by Checkmate')
            else:
                drawText(screen, 'White wins by Checkmate')
        elif gs.stalemate:
            gameOver = True
            drawText(screen, 'GAME DRAW')

        if not gs.whiteToMove and len(validMoves) != 0 and not moveMade:
            x = gs.getBestMove(2, False)
            gs.tomakeMove(x)
            moveMade = True
        clock.tick(maxfps)
        p.display.flip()


def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):  # sqSelected is the piece that can be moved
            # highlighting the selected square
            s = p.Surface((sqsize, sqsize))
            s.set_alpha(100)  # transperancy value
            s.fill(p.Color('blue'))
            screen.blit(s, (c * sqsize, r * sqsize))
            # highlight moves from that square
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol * sqsize, move.endRow * sqsize))
def animateMove(move, screen, board, clock):
    global colours
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 10 #speed of animation
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r, c =   (move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        #erase the piece from the ending square
        color = colours[(move.endRow + move.endCol)%2]
        endSquare = p.Rect(move.endCol*sqsize, move.endRow*sqsize, sqsize, sqsize)
        p.draw.rect(screen, color, endSquare)

        #draw captured piece onto rectangle
        if move.pieceCaptured != '--':
            screen.blit(images[move.pieceCaptured], endSquare)

        #draw moving piece
        screen.blit(images[move.pieceMoved], p.Rect(c*sqsize, r*sqsize, sqsize, sqsize))
        p.display.flip()
        clock.tick(60)
def drawText(screen, text):
    font = p.font.SysFont("Times New Roman", 32, True, False)
    textObject = font.render(text, 0, p.Color('White'))
    textLocation = p.Rect(0, 0, width, height).move(width/2 - textObject.get_width()/2, height/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color("Blue"))
    screen.blit(textObject, textLocation.move(2, 2))

def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)


def drawBoard(screen):
    global colours
    colours = [p.Color("white"), p.Color("brown")]
    for r in range(dim):
        for c in range(dim):
            colour = colours[((r + c) % 2)]
            p.draw.rect(screen, colour, p.Rect(c * sqsize, r * sqsize, sqsize, sqsize))


def drawPieces(screen, board):
    for r in range(dim):
        for c in range(dim):
            piece = board[r][c]
            if piece != "--":
                screen.blit(images[piece], p.Rect(c * sqsize, r * sqsize, sqsize, sqsize))


if __name__ == "__main__":
    main()