# YOUR PROJECT TITLE
#### Video Demo: https://www.youtube.com/watch?v=QWj0EYrDP_Y&feature=youtu.be
#### Description: This is a simple chess game in python using the pygame library
my project contains 2 .py fles 
chess.py and engine.py

chess.py contains each of these functions:

pieces: it takes images from local files and renders them using pygame
highlightSquares: this takes in the state of the game and renders a slightly transparent color to determine the possible moves
and it uses starting_square() to color only the initial position of the move
Draw_gs: which takes in everything that would be rendered (screen,gamestate,validmoves,squareselected (which determines the move to be played) and calls them to finalize how the board would look like

and engine.py: it basically handles all the logic behind movements and getting possible and valid moves. It contains the following classes:

gamestate:
which handles the logic and position of the game
and has the following functions:

makemove: it moves pieces according to logic and rules of chess and keeps track of king location after each move to determine if castling rights are lost
undomove: it removes the last move from the movelog and returns the board to previous state
updateCastlerights: removes the casting rights if the king is moved or a rook is moved
getAllpossiblemoves:returns all the possible moves even the illegal ones
which is then called inside of getvalidmoves to determine which moves are valid and which are not
incheck: returns true or false if the kind is check or not using a helper funcion squareattacked
getpawn: returns moves for pawn
getrook: returns moves for rook
get bishop: returns moves for bishop
get knightmoves: returns moves for knight
get kingmoves: returns moves for king
getcastlemoves: if casting rights arent false it returns moves for casting using 2 helper functions getKingSideCastleMovesand getQueenSideCastleMoves

class CastleRights: is used by gamestate to determine castling rights for each player
class move which handles how the board changes after every move and how an undo move would be done