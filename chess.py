from datetime import datetime
from itertools import product

PIECES = {
        'K': '♔',  # White King
        'Q': '♕',  # White Queen
        'R': '♖',  # White Rook
        'B': '♗',  # White Bishop
        'N': '♘',  # White Knight
        'P': '♙',  # White Pawn
        'k': '♚',  # Black King
        'q': '♛',  # Black Queen
        'r': '♜',  # Black Rook
        'b': '♝',  # Black Bishop
        'n': '♞',  # Black Knight
        'p': '♟'   # Black Pawn
}

class IllegalMoveException(Exception):
    """
    Handle invalid move choices.
    """
    pass

class InvalidCoordinatesException(IllegalMoveException):
    pass

class BlockedByPieceException(IllegalMoveException):
    pass

class InCheckException(IllegalMoveException):
    """
    Handle cases where a player is in check, and tries to make a move that does not take them out of check.
    Also handle cases where a player tries to make a move that would reveal an attack on their King.
    """
    pass

class Piece:
    def __init__(self, piece_id: str) -> None:
        self.piece_id = piece_id

        try:
            self.icon = PIECES[piece_id]

        except KeyError:
            print(f"Error: piece_id must be one of {list(PIECES.keys())}")

        self.move_count = 0

    def __str__(self) -> str:
        return self.icon
    
    def __repr__(self) -> str:
        return str(self)
    
    def move(self, coordinates: str) -> None:
        """
        Move the piece to a specified location on the current game Board.
        Increment move_count. This is needed for Castling and En Passant.
        """
        if coordinates not in Board.coords:
            raise InvalidCoordinatesException("Invalid coordinates. Coordinates must be of the form `a1`, for a-h and 1-8.")

        match self.piece_id:

            case 'p' | 'P':
                print(f"Moved pawn to {coordinates}")

class Board:
    # Rows
    ranks = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    # Columns
    files = range(1,10)
    coords = [ ''.join(tup) for tup in list(product(ranks, [str(x) for x in files])) ]

    def __init__(self) -> None:
        self.board = [
            # Black
            [ Piece('r'), Piece('n'), Piece('b'), Piece('q'), Piece('k'), Piece('b'), Piece('n'), Piece('r') ],
            [ Piece('p') for x in range(8) ],

            # Board center
            [ '' for i in range(8) ],
            [ '' for i in range(8) ],
            [ '' for i in range(8) ],
            [ '' for i in range(8) ],

            # White
            [ Piece('P') for j in range(8) ],
            [ Piece('R'), Piece('N'), Piece('B'), Piece('Q'), Piece('K'), Piece('B'), Piece('N'), Piece('R') ]
        ]

        # Controls whether to use piece icons or not.
        # To toggle, use the switch_icons method.
        self.icons = True

    def __str__(self) -> str:
        """
        Nicely prints the current board.
        """
        ranks = []

        if self.icons:
            for rank in self.board:
                rank_str = " ".join(element.icon if isinstance(element, Piece) else ' ' for element in rank)
                ranks.append(rank_str)

        else:
            for rank in self.board:
                rank_str = " ".join(element.piece_id if isinstance(element, Piece) else ' ' for element in rank)
                ranks.append(rank_str)

        return "\n" + "\n".join(ranks) + "\n"
    
    def __repr__(self) -> str:
        return str(self)
    
    def flip(self) -> None:
        """
        Flips the board to the opposite side.
        """

        for i in range(2):
            self.board = list(zip(*self.board[::-1]))

        print(self)

    def switch_icons(self) -> None:
        """
        Swap between viewing piece icons or IDs.
        """
        self.icons = not self.icons

        print(self)

class PGNHandler:
    """
    A class to handle Portable Game Notation (PGN)
    Every move of the game should be recorded according to the format,
    which can then be viewed and exported by the player(s) at the end.

    Example format from https://en.wikipedia.org/wiki/Portable_Game_Notation :

    [Event "F/S Return Match"]
    [Site "Belgrade, Serbia JUG"]
    [Date "1992.11.04"]
    [Round "29"]
    [White "Fischer, Robert J."]
    [Black "Spassky, Boris V."]
    [Result "1/2-1/2"]

    1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 {This opening is called the Ruy Lopez.}
    4. Ba4 Nf6 5. O-O Be7 6. Re1 b5 7. Bb3 d6 8. c3 O-O 9. h3 Nb8 10. d4 Nbd7
    11. c4 c6 12. cxb5 axb5 13. Nc3 Bb7 14. Bg5 b4 15. Nb1 h6 16. Bh4 c5 17. dxe5
    Nxe4 18. Bxe7 Qxe7 19. exd6 Qf6 20. Nbd2 Nxd6 21. Nc4 Nxc4 22. Bxc4 Nb6
    23. Ne5 Rae8 24. Bxf7+ Rxf7 25. Nxf7 Rxe1+ 26. Qxe1 Kxf7 27. Qe3 Qg5 28. Qxg5
    hxg5 29. b3 Ke6 30. a3 Kd6 31. axb4 cxb4 32. Ra5 Nd5 33. f3 Bc8 34. Kf2 Bf5
    35. Ra7 g6 36. Ra6+ Kc5 37. Ke1 Nf4 38. g3 Nxh3 39. Kd2 Kb5 40. Rd6 Kc5 41. Ra6
    Nf2 42. g4 Bd3 43. Re6 1/2-1/2
    """
    def __init__(
            self,
            event = "Python Chess Game",
            site = "A Computer Terminal",
            date = datetime.today().strftime("%Y.%m.%d"),
            round_num = 1,
            white = "White",
            black = "Black",
            result = ""
        ) -> None:
        
        self.event = event
        self.site = site
        self.date = date
        self.round_num = round_num
        self.white = white
        self.black = black
        self.result = result