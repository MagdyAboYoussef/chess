import copy
import PySimpleGUI as sg


class GameState():
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.BlackKingLocation = (0, 4)
        self.checkmate = False
        self.stalemate = False
        self.enpassantPossible = ()
        self.CurrentCastlingRights = CastleRights(True, True, True, True)
        self.castleRightsLog = [CastleRights
                                (self.CurrentCastlingRights.wks, self.CurrentCastlingRights.bks, self.CurrentCastlingRights.wqs, self.CurrentCastlingRights.bqs)]


    def makeMove(self, move):
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove
        if move.pieceMoved[1] == 'K':
            if move.pieceMoved[0] == 'b':
                self.BlackKingLocation = (move.end_row, move.end_col)
            if move.pieceMoved[0] == 'w':
                self.whiteKingLocation = (move.end_row, move.end_col)
        if move.isPawnPromotion:
            self.board[move.end_row][move.end_col] = f'{move.pieceMoved[0]}Q'
        if move.isEnPassantMove:
            self.board[move.start_row][move.end_col] = "--"

        if move.pieceMoved[1] == "P" and abs(move.end_row - move.start_row) == 2:
            self.enpassantPossible = (
                (move.start_row + move.end_row)//2, move.end_col)
        else:
            self.enpassantPossible = ()

        if move.isCastleMove:
            if move.end_col - move.start_col == 2:
                self.board[move.end_row][move.end_col -
                                         1] = self.board[move.end_row][move.end_col+1]
                self.board[move.end_row][move.end_col + 1] = "--"
            else:
                self.board[move.end_row][move.end_col +
                                         1] = self.board[move.end_row][move.end_col-2]
                self.board[move.end_row][move.end_col - 2] = "--"

        self.UpdateCastleRights(move)
        self.castleRightsLog.append(CastleRights(self.CurrentCastlingRights.wks, self.CurrentCastlingRights.bks,
                                    self.CurrentCastlingRights.wqs, self.CurrentCastlingRights.bqs))




    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.start_row][move.start_col] = move.pieceMoved
            self.board[move.end_row][move.end_col] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.start_row, move.start_col)
        elif move.pieceMoved == "bK":
            self.BlackKingLocation = (move.start_row, move.start_col)
        if move.isEnPassantMove:
            self.board[move.end_row][move.end_col] = '--'
            self.board[move.start_row][move.end_col] = move.pieceCaptured
            self.enpassantPossible = (move.end_row, move.end_col)
        if move.pieceMoved[1] == "P" and abs(move.start_row - move.end_row) == 2:
            self.enpassantPossible = ()
        self.castleRightsLog.pop()
        castle_rights = copy.deepcopy(self.castleRightsLog[-1])
        self.CurrentCastlingRights = castle_rights
        if move.isCastleMove:
            if move.end_col - move.start_col == 2:
                self.board[move.end_row][move.end_col +
                                         1] = self.board[move.end_row][move.end_col-1]
                self.board[move.end_row][move.end_col-1] = "--"
            else:
                self.board[move.end_row][move.end_col -
                                         2] = self.board[move.end_row][move.end_col+1]
                self.board[move.end_row][move.end_col+1] = "--"

    def UpdateCastleRights(self, move):
        if move.pieceMoved == "bK":
            self.CurrentCastlingRights.bks = False
            self.CurrentCastlingRights.bqs = False
        elif move.pieceMoved == "bR":
            if move.start_row == 0:
                if move.start_col == 0:
                    self.CurrentCastlingRights.bqs = False
                elif move.start_col == 7:
                    self.CurrentCastlingRights.bks = False

        elif move.pieceMoved == "wK":
            self.CurrentCastlingRights.wks = False
            self.CurrentCastlingRights.wqs = False
        elif move.pieceMoved == "wR":
            if move.start_row == 7:
                if move.start_col == 0:
                    self.CurrentCastlingRights.wqs = False
                elif move.start_col == 7:
                    self.CurrentCastlingRights.wks = False

    def getValidMoves(self):
        tempassant = self.enpassantPossible
        tempCastleRights = CastleRights(self.CurrentCastlingRights.wks, self.CurrentCastlingRights.bks,
                                        self.CurrentCastlingRights.wqs, self.CurrentCastlingRights.bqs)
        moves = self.getAllPossibleMoves()

        for i in range(len(moves)-1, -1, -1):
            self.makeMove(moves[i])
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i])

            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        if len(moves) == 0:
            if self.inCheck():
                self.checkmate = True
                print("Checkmate")
            else:
                self.stalemate = True
                print("Stalemate")
        else:
            self.checkmate = False
            self.stalemate = False
        if self.whiteToMove:
            self.getCastleMoves(
                self.whiteKingLocation[0], self.whiteKingLocation[1], moves)
        else:
            self.getCastleMoves(
                self.BlackKingLocation[0], self.BlackKingLocation[1], moves)
        self.enpassantPossible = tempassant
        self.CurrentCastlingRights = tempCastleRights

        return moves

    def inCheck(self):
        if self.whiteToMove:
            return self.squareAttacked(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareAttacked(self.BlackKingLocation[0], self.BlackKingLocation[1])

    def squareAttacked(self, r, c):
        self.whiteToMove = not self.whiteToMove
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        return any(m.end_row == r and m.end_col == c for m in oppMoves)

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board)):
                turn = self.board[r][c][0]
                piece = self.board[r][c][1]
                if turn == "w" and self.whiteToMove:
                    if piece == "P":
                        self.getPawnMoves(r, c, moves)
                    elif piece == "R":
                        self.getRookMoves(r, c, moves)
                    elif piece == "B":
                        self.getBishopMoves(r, c, moves)
                    elif piece == "N":
                        self.getKnightMoves(r, c, moves)
                    elif piece == "K":
                        self.getKingMoves(r, c, moves)
                    elif piece == "Q":
                        self.getQueenMoves(r, c, moves)
                elif turn == "b" and not self.whiteToMove:
                    if piece == "P":
                        self.getPawnMoves(r, c, moves)
                    elif piece == "R":
                        self.getRookMoves(r, c, moves)
                    elif piece == "B":
                        self.getBishopMoves(r, c, moves)
                    elif piece == "N":
                        self.getKnightMoves(r, c, moves)
                    elif piece == "K":
                        self.getKingMoves(r, c, moves)
                    elif piece == "Q":
                        self.getQueenMoves(r, c, moves)
        return moves

    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:
            if self.board[r-1][c] == "--":
                moves.append(move((r, c), (r-1, c), self.board))
            if r == 6 and self.board[r-2][c] == "--" and self.board[r-1][c] == "--":
                moves.append(move((r, c), (r-2, c), self.board))
            if c >= 1:
                if self.board[r-1][c-1][0] == "b":
                    moves.append(move((r, c), (r-1, c-1), self.board))
                elif (r-1, c-1) == self.enpassantPossible:
                    moves.append(
                        move((r, c), (r-1, c-1), self.board, isEnPassantMove=True))

            if c <= 6:
                if self.board[r-1][c+1][0] == "b":
                    moves.append(move((r, c), (r-1, c+1), self.board))
                elif (r-1, c+1) == self.enpassantPossible:
                    moves.append(
                        move((r, c), (r-1, c+1), self.board, isEnPassantMove=True))
        elif self.whiteToMove == False:
            if self.board[r+1][c] == "--":
                moves.append(move((r, c), (r+1, c), self.board))
            if r == 1 and self.board[r+2][c] == "--" and self.board[r+1][c] == "--":
                moves.append(move((r, c), (r+2, c), self.board))
            if c >= 1:
                if self.board[r+1][c-1][0] == "w":
                    moves.append(move((r, c), (r+1, c-1), self.board))
                elif (r+1, c-1) == self.enpassantPossible:
                    moves.append(
                        move((r, c), (r+1, c-1), self.board, isEnPassantMove=True))
            if c <= 6:
                if self.board[r+1][c+1][0] == "w":
                    moves.append(move((r, c), (r+1, c+1), self.board))
                elif (r+1, c+1) == self.enpassantPossible:
                    moves.append(
                        move((r, c), (r+1, c+1), self.board, isEnPassantMove=True))

    def getRookMoves(self, r, c, moves):
        white = "w"
        if self.whiteToMove:
            black = "b"
            enemy = black
        elif self.whiteToMove == False:
            enemy = white
        for _ in range(1, 8):
            if r+_ > 7:
                break
            if self.board[r+_][c] == "--":
                moves.append(move((r, c), (r+_, c), self.board))
            elif self.board[r+_][c][0] == enemy:
                moves.append(move((r, c), (r+_, c), self.board))
                break
            else:
                break

        for _ in range(1, 8):
            if r-_ < 0:
                break
            if self.board[r-_][c] == "--":
                moves.append(move((r, c), (r-_, c), self.board))
            elif self.board[r-_][c][0] == enemy:
                moves.append(move((r, c), (r-_, c), self.board))
                break
            else:
                break

        for _ in range(1, 8):
            if c+_ > 7:
                break
            if self.board[r][c+_] == "--":
                moves.append(move((r, c), (r, c+_), self.board))
            elif self.board[r][c+_][0] == enemy:
                moves.append(move((r, c), (r, c+_), self.board))
                break
            else:
                break
        for _ in range(1, 8):
            if c-_ < 0:
                break
            if self.board[r][c-_] == "--":
                moves.append(move((r, c), (r, c-_), self.board))
            elif self.board[r][c-_][0] == enemy:
                moves.append(move((r, c), (r, c-_), self.board))
                break
            else:
                break

    def getBishopMoves(self, r, c, moves):
        directions = (1, -1), (1, 1), (-1, 1), (-1, -1)
        enemy = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r+d[0]*i
                endCol = c+d[1]*i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endpiece = self.board[endRow][endCol]
                    if endpiece == "--":
                        moves.append(
                            move((r, c), (endRow, endCol), self.board))
                    elif endpiece[0] == enemy:
                        moves.append(
                            move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break

    def getKnightMoves(self, r, c, moves):
        directions = (-2, 1), (-2, -1), (-1, 2), (-1, -
                                                  2), (2, 1), (2, -1), (1, 2), (1, -2)
        ally = "w" if self.whiteToMove else "b"
        for d in directions:
            endRow = r+d[0]
            endCol = c+d[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endpiece = self.board[endRow][endCol]
                if endpiece[0] != ally:
                    moves.append(move((r, c), (endRow, endCol), self.board))

    def getKingMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 0), (-1, 1), (0, -1),
                      (0, 1), (1, -1), (1, 0), (1, 1))
        ally = "w" if self.whiteToMove else "b"
        for d in directions:
            endRow = r+d[0]
            endCol = c+d[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endpiece = self.board[endRow][endCol]
                if endpiece[0] != ally:
                    moves.append(move((r, c), (endRow, endCol), self.board))

    def getCastleMoves(self, r, c, moves):
        if self.squareAttacked(r, c):
            return
        if (self.whiteToMove and self.CurrentCastlingRights.wks) or (not self.whiteToMove and self.CurrentCastlingRights.bks):
            self.getKingSideCastleMoves(r, c, moves)
        if (self.whiteToMove and self.CurrentCastlingRights.wqs) or (not self.whiteToMove and self.CurrentCastlingRights.bqs):
            self.getQueenSideCastleMoves(r, c, moves)

    def getKingSideCastleMoves(self, r, c, moves):
        if (
            self.board[r][c + 1] == "--"
            and self.board[r][c + 2] == "--"
            and not self.squareAttacked(r, c + 1)
            and not self.squareAttacked(r, c + 2)
        ):
            moves.append(
                move((r, c), (r, c+2), self.board, isCastleMove=True))

    def getQueenSideCastleMoves(self, r, c, moves):
        if (
            self.board[r][c - 1] == "--"
            and self.board[r][c - 2] == "--"
            and self.board[r][c - 3] == "--"
            and not self.squareAttacked(r, c - 1)
            and not self.squareAttacked(r, c - 2)
        ):
            moves.append(
                move((r, c), (r, c-2), self.board, isCastleMove=True))

    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)


class CastleRights():
    def __init__(self, wKs, bKs, wQs, bQs):
        self.wks = wKs
        self.bks = bKs
        self.wqs = wQs
        self.bqs = bQs


class move():
    ranksToRows = {"1": 7, "2": 6, "3": 5,
                   "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2,
                   "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, StartSQ, EndSQ, board, isEnPassantMove=False, isCastleMove=False):
        self.start_row = StartSQ[0]
        self.start_col = StartSQ[1]
        self.end_row = EndSQ[0]
        self.end_col = EndSQ[1]
        self.pieceMoved = board[self.start_row][self.start_col]
        self.pieceCaptured = board[self.end_row][self.end_col]
        self.isPawnPromotion = False
        self.isEnPassantMove = isEnPassantMove
        self.isCastleMove = isCastleMove
        if self.isEnPassantMove:
            if self.pieceMoved == "bP":
                self.pieceCaptured = "wP"
            elif self.pieceMoved == "wP":
                self.pieceCaptured = "bP"
        self.moveID = self.start_row * 1000+self.start_col * \
            100 + self.end_row*10 + self.end_col

        if (self.pieceMoved == "wP" and self.end_row == 0) or (self.pieceMoved == "bP" and self.end_row == 7):
            self.isPawnPromotion = True

        if self.pieceMoved[1] == "P" and (self.end_row, self.end_col) == self.isEnPassantMove:
            self.isEnPassantMove = True

    def __eq__(self, other):
        return self.moveID == other.moveID if isinstance(other, move) else False

    def Notations(self):
        return self.getRankFile(self.start_row, self.start_col) + self.getRankFile(self.end_row, self.end_col)

    def getRankFile(self, r, c):
        return self.colsToFiles[c]+self.rowsToRanks[r]

    def __str__(self):
        return f"Move ID: {self.moveID}. {self.pieceMoved} Start: {self.start_row},{self.start_col} End: {self.end_row},{self.end_col}. Piece cap'd {self.pieceCaptured} \n"

    def __repr__(self):
        return str(self)
