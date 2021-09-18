"""
Chess AI
"""
import math
import random

# niklasf/python-chess is licensed under GPL-3.0
import chess

VALUE = {
    chess.PAWN: 100,
    chess.KNIGHT: 300,
    chess.BISHOP: 350,
    chess.ROOK: 550,
    chess.QUEEN: 950,
    chess.KING: 400,
}

# Piece-square tables from Chess Programming Wiki
PIECE_SQUARE = {

    chess.PAWN: [
          0,  0,  0,  0,  0,  0,  0,  0,
          5, 10, 10,-20,-20, 10, 10,  5,
          5, -5,-10,  0,  0,-10, -5,  5,
          0,  0,  0, 20, 20,  0,  0,  0,
          5,  5, 10, 25, 25, 10,  5,  5,
         10, 10, 20, 30, 30, 20, 10, 10,
         50, 50, 50, 50, 50, 50, 50, 50,
          0,  0,  0,  0,  0,  0,  0,  0,
    ],

    chess.KNIGHT: [
        -50,-40,-30,-30,-30,-30,-40,-50,
        -40,-20,  0,  5,  5,  0,-20,-40,
        -30,  5, 10, 15, 15, 10,  5,-30,
        -30,  0, 15, 20, 20, 15,  0,-30,
        -30,  5, 15, 20, 20, 15,  5,-30,
        -30,  0, 10, 15, 15, 10,  0,-30,
        -40,-20,  0,  0,  0,  0,-20,-40,
        -50,-40,-30,-30,-30,-30,-40,-50,
    ],

    chess.BISHOP: [
        -20,-10,-10,-10,-10,-10,-10,-20,
        -10,  5,  0,  0,  0,  0,  5,-10,
        -10, 10, 10, 10, 10, 10, 10,-10,
        -10,  0, 10, 10, 10, 10,  0,-10,
        -10,  5,  5, 10, 10,  5,  5,-10,
        -10,  0,  5, 10, 10,  5,  0,-10,
        -10,  0,  0,  0,  0,  0,  0,-10,
        -20,-10,-10,-10,-10,-10,-10,-20,
    ],

    chess.ROOK:[
          0,  0,  0,  5,  5,  0,  0,  0,
         -5,  0,  0,  0,  0,  0,  0, -5,
         -5,  0,  0,  0,  0,  0,  0, -5,
         -5,  0,  0,  0,  0,  0,  0, -5,
         -5,  0,  0,  0,  0,  0,  0, -5,
         -5,  0,  0,  0,  0,  0,  0, -5,
          5, 10, 10, 10, 10, 10, 10,  5,
          0,  0,  0,  0,  0,  0,  0,  0,
    ],

    chess.QUEEN: [
        -20,-10,-10, -5, -5,-10,-10,-20,
        -10,  0,  5,  0,  0,  0,  0,-10,
        -10,  5,  5,  5,  5,  5,  0,-10,
          0,  0,  5,  5,  5,  5,  0, -5,
         -5,  0,  5,  5,  5,  5,  0, -5,
        -10,  0,  5,  5,  5,  5,  0,-10,
        -10,  0,  0,  0,  0,  0,  0,-10,
        -20,-10,-10, -5, -5,-10,-10,-20,
    ],

    chess.KING: [
         20, 30, 10,  0,  0, 10, 30, 20,
         20, 20,  0,  0,  0,  0, 20, 20,
        -10,-20,-20,-20,-20,-20,-20,-10,
        -20,-30,-30,-40,-40,-30,-30,-20,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
    ],
}

CHECKMATE_VALUE = 10 ** 6
SEARCH_DEPTH = 3


class ChessAI():

    def __init__(self):

        # Generate Zobrist table
        self.zobrist = []
        for _ in range(64):
            row = []
            for _ in range(12):
                row.append(random.randrange(2**64))
            self.zobrist.append(row)

        # Hash table
        self.table = {}

    def utility(self, board):
        """
        Evaluates the value of the board based on fixed piece valuations
        """
        utility = 0

        # Increment or decrement piece and piece-position values
        for square in board.piece_map():

            # For Black's pieces, start indexing the piece-square tables at the end
            position = (
                square if board.color_at(square) == chess.WHITE else
                -square - 1
            )

            if board.color_at(square) == chess.WHITE:
                utility += VALUE[board.piece_type_at(square)]
                utility += PIECE_SQUARE[board.piece_type_at(square)][position]
            else:
                utility -= VALUE[board.piece_type_at(square)]
                utility -= PIECE_SQUARE[board.piece_type_at(square)][position]

        # Incentive for attacking the opponent's King
        if board.is_checkmate():
            if board.outcome().winner == chess.WHITE:
                utility += CHECKMATE_VALUE
            else:
                utility -= CHECKMATE_VALUE

        return utility

    def minimax(self, board, depth=SEARCH_DEPTH):
        """
        Returns the optimal action for the current player on the board
        by using minimax strategy and alpha-beta pruning

        Pseudocode from Russell and Norvig (2021)
        """
        if board.turn == chess.WHITE:
            return self.max_value(board, depth)
        else:
            return self.min_value(board, depth)

    def max_value(self, board, depth, alpha=-math.inf, beta=math.inf):

        # Return value and decision from hash table if board position has already been encountered
        if (hash := self.zobrist_hash(board)) in self.table:
            if self.table[hash]['depth'] >= depth:
                return self.table[hash]['value'], self.table[hash]['decision']

        # Base condition
        if not depth or board.is_game_over():
            return self.utility(board), None

        value = -math.inf

        for action in board.legal_moves:
            board.push(action)
            score = self.min_value(board, depth - 1, alpha, beta)[0]
            board.pop()
            if score > value:
                value, decision = score, action
                alpha = max(alpha, value)
            if value > beta:
                self.record(hash, value, decision, depth)
                return value, decision
            elif value == beta:
                if random.randint(0, 1):
                    self.record(hash, value, decision, depth)
                    return value, decision

        self.record(hash, value, decision, depth)
        return value, decision

    def min_value(self, board, depth, alpha=-math.inf, beta=math.inf):

        # Return value and decision from hash table if board position has already been encountered
        if (hash := self.zobrist_hash(board)) in self.table:
            if self.table[hash]['depth'] >= depth:
                return self.table[hash]['value'], self.table[hash]['decision']

        # Base condition
        if not depth or board.is_game_over():
            return self.utility(board), None

        value = math.inf

        for action in board.legal_moves:
            board.push(action)
            score = self.max_value(board, depth - 1, alpha, beta)[0]
            board.pop()
            if score < value:
                value, decision = score, action
                beta = min(beta, value)
            if value < alpha:
                self.record(hash, value, decision, depth)
                return value, decision
            elif value == alpha:
                if random.randint(0, 1):
                    self.record(hash, value, decision, depth)
                    return value, decision

        self.record(hash, value, decision, depth)
        return value, decision

    def record(self, hash, value, decision, depth):
        """
        Loads board configuration to hash table
        """
        if hash not in self.table:
            self.table[hash] = {}

        # Add or update values
        self.table[hash]['value'] = value
        self.table[hash]['decision'] = decision
        self.table[hash]['depth'] = depth

    def zobrist_hash(self, board):
        """
        Generate a unique hash for a board position

        Hashing algorithm from Zobrist (1970)
        """
        pieces = board.piece_map()

        hash = 0
        for square in chess.SQUARES:
            if square in pieces:
                piece = pieces[square]
                piece_type = piece.piece_type + piece.color * 6 - 1
                hash ^= self.zobrist[square][piece_type]

        return hash
