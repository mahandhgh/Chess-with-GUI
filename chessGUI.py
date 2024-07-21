import tkinter as tk 
from tkinter import messagebox
from tkinter import simpledialog

class Position:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __eq__(self, other):
        if other is None:
            return False
        return self.row == other.row and self.col == other.col


class Piece:
    def __init__(self, color, board, position=None):
        self.color = color
        self.board = board
        self.has_moved = False
        self.position = position

    def possible_moves(self):
        pass

    def move(self, end_pos):
        possible_moves = self.possible_moves()
        if end_pos in possible_moves:
            if self.board.move_piece(self.position, end_pos):
                self.has_moved = True
                return True
            else:
                messagebox.showerror("Invalid move")
                return False
        else:
            messagebox.showerror("Invalid move")
            return False

    def __str__(self):
        pass


class King(Piece):
    def __init__(self, color, board, position=None):
        super().__init__(color, board, position)
        self.piece_type = "king"

    def possible_moves(self):
        moves = []
        offsets = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, -1), (-1, 1), (1, 1), (-1, -1)]
        for dr, dc in offsets:
            new_pos = Position(self.position.row + dr, self.position.col + dc)
            if self.board.is_inside_board(new_pos) and (
                    self.board.is_square_empty(new_pos) or self.board.is_enemy_piece(new_pos, self.color)):
                moves.append(new_pos)
        # Castling
        if not self.has_moved:
            # Check kingside castling
            if self.board.is_kingside_castle_possible(self.color):
                moves.append(Position(self.position.row, self.position.col + 2))
            # Check queenside castling
            if self.board.is_queenside_castle_possible(self.color):
                moves.append(Position(self.position.row, self.position.col - 2))
        return moves

    def __str__(self):
        return "♔" if self.color == "White" else "♚"


class Bishop(Piece):
    def __init__(self, color, board, position=None):
        super().__init__(color, board, position)
        self.piece_type = "bishop"

    def possible_moves(self):
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        return self.board.get_directional_moves(self.position, directions, self.color)

    def __str__(self):
        return "♗" if self.color == "White" else "♝"


class Pawn(Piece):
    def __init__(self, color, board, position=None):
        super().__init__(color, board, position)
        self.piece_type = "pawn"
        self.direction = 1 if self.color == "White" else -1
        self.start_row = 1 if self.color == "White" else 6

    def possible_moves(self):
        moves = []
        # Regular forward move
        front_pos = Position(self.position.row + self.direction, self.position.col)
        if self.board.is_inside_board(front_pos) and self.board.is_square_empty(front_pos):
            moves.append(front_pos)
            # Double move from starting position
            if self.position.row == self.start_row:
                double_front_pos = Position(self.position.row + 2 * self.direction, self.position.col)
                if self.board.is_inside_board(double_front_pos) and self.board.is_square_empty(double_front_pos):
                    moves.append(double_front_pos)
        # Capturing moves
        for dc in [-1, 1]:
            diag_pos = Position(self.position.row + self.direction, self.position.col + dc)
            if self.board.is_inside_board(diag_pos):
                if self.board.is_enemy_piece(diag_pos, self.color) or diag_pos == self.board.en_passant_target:
                    moves.append(diag_pos)

        return moves

    def __str__(self):
        return "♙" if self.color == "White" else "♟️"


class Rook(Piece):
    def __init__(self, color, board, position=None):
        super().__init__(color, board, position)
        self.piece_type = "rook"

    def possible_moves(self):
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        return self.board.get_directional_moves(self.position, directions, self.color)

    def __str__(self):
        return "♖" if self.color == "White" else "♜"


class Knight(Piece):
    def __init__(self, color, board, position=None):
        super().__init__(color, board, position)
        self.piece_type = "knight"

    def possible_moves(self):
        offsets = [(2, 1), (1, 2), (-2, 1), (1, -2), (-1, 2), (2, -1), (-2, -1), (-1, -2)]
        moves = []
        for dr, dc in offsets:
            new_pos = Position(self.position.row + dr, self.position.col + dc)
            if self.board.is_inside_board(new_pos) and (
                    self.board.is_square_empty(new_pos) or self.board.is_enemy_piece(new_pos, self.color)):
                moves.append(new_pos)
        return moves

    def __str__(self):
        return "♘" if self.color == "White" else "♞"


class Queen(Piece):
    def __init__(self, color, board, position=None):
        super().__init__(color, board, position)
        self.piece_type = "queen"

    def possible_moves(self):
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        return self.board.get_directional_moves(self.position, directions, self.color)

    def __str__(self):
        return "♕" if self.color == "White" else "♛"


class Board:
    def __init__(self, gui=None):
        self.board = [[None for _ in range(8)] for _ in range(8)]  # initialize the board
        self.gui = gui
        self.en_passant_target = None
        
    def place_piece(self, piece, position):
        self.board[position.row][position.col] = piece
        piece.position = position

    def remove_piece(self, piece):
        self.board[piece.position.row][piece.position.col] = None
        piece.position = None

    def move_piece(self, start_pos, end_pos):
        moving_piece = self.board[start_pos.row][start_pos.col]
        if not moving_piece:
            messagebox.showerror("Invalid move", "No piece at the starting position.")
            return False

        if end_pos not in moving_piece.possible_moves():
            messagebox.showerror("Invalid move", "The move is not allowed.")
            return False

        # Check if the move puts the king in check
        if self.move_puts_self_in_check(moving_piece, end_pos):
            messagebox.showerror("Invalid move", "This move would put or leave your king in check.")
            return False

        # If reaching here, the move is valid and can be processed
        self.execute_move(moving_piece, start_pos, end_pos)

        opponent_color = "White" if moving_piece.color == "Black" else "Black"
        if self.is_check(opponent_color):
            print("Check!")

        return True

    def execute_move(self, piece, start_pos, end_pos):
        # Handle special pawn move for en passant capture
        if isinstance(piece, Pawn) and end_pos == self.en_passant_target:
            captured_pawn_row = start_pos.row
            captured_pawn_col = end_pos.col
            self.board[captured_pawn_row][captured_pawn_col] = None  # Remove the captured pawn

        # Handle castling
        if isinstance(piece, King) and abs(start_pos.col - end_pos.col) == 2:
            self.handle_castling(piece, start_pos, end_pos)
        else:
            # Regular move or capture
            self.board[start_pos.row][start_pos.col] = None
            self.board[end_pos.row][end_pos.col] = piece
            piece.position = end_pos
            piece.has_moved = True

        # Clear en passant target after the move is executed
        if not isinstance(piece, Pawn) or abs(start_pos.row - end_pos.row) != 2:
            self.en_passant_target = None

        # Set en passant target if pawn moves two squares from its initial position
        if isinstance(piece, Pawn) and abs(start_pos.row - end_pos.row) == 2:
            middle_row = (start_pos.row + end_pos.row) // 2
            self.en_passant_target = Position(middle_row, start_pos.col)
    
    def is_check(self, color):
        king_position = self.get_king(color).position
        return self.is_position_under_attack(king_position, color)

    def move_puts_self_in_check(self, piece, end_pos):
        original_position = piece.position
        original_piece = self.board[end_pos.row][end_pos.col]

        # Simulate move
        self.board[original_position.row][original_position.col] = None
        self.board[end_pos.row][end_pos.col] = piece
        piece.position = end_pos

        # Check if moving the piece puts the king in check
        king = self.get_king(piece.color)
        in_check = self.is_position_under_attack(king.position, piece.color)

        # Revert move
        self.board[original_position.row][original_position.col] = piece
        self.board[end_pos.row][end_pos.col] = original_piece
        piece.position = original_position

        return in_check

    def get_king(self, color):
        for row in self.board:
            for piece in row:
                if isinstance(piece, King) and piece.color == color:
                    return piece
        return None

    def is_position_under_attack(self, position, color):
        for row in self.board:
            for piece in row:
                if piece and piece.color != color:
                    if position in piece.possible_moves():
                        return True
        return False

    def is_square_empty(self, position):
        return self.board[position.row][position.col] is None

    def is_enemy_piece(self, position, color):
        piece = self.board[position.row][position.col]
        return piece and piece.color != color

    def is_inside_board(self, position):
        return 0 <= position.row < 8 and 0 <= position.col < 8

    def is_kingside_castle_possible(self, color):
        king_row = 0 if color == "White" else 7
        king_col = 4
        rook_col = 7
        return self.is_castling_possible(color, king_row, king_col, rook_col)

    def is_queenside_castle_possible(self, color):
        king_row = 0 if color == "White" else 7
        king_col = 4
        rook_col = 0
        return self.is_castling_possible(color, king_row, king_col, rook_col)


    def is_king_side_clear(self, row, king_col):
        for col in range(king_col + 1, 7):
            if not self.is_square_empty(Position(row, col)):
                return False
        return True

    def is_queen_side_clear(self, row, king_col):
        for col in range(1, king_col):
            if not self.is_square_empty(Position(row, col)):
                return False
        return True
    
    def is_castling_possible(self, color, king_row, king_col, rook_col):
        # Check if the king and rook have not moved
        king = self.board[king_row][king_col]
        rook = self.board[king_row][rook_col]
        if not isinstance(king, King) or not isinstance(rook, Rook):
            return False
        if king.has_moved or rook.has_moved:
            return False
    
        # Check if all squares between king and rook are empty
        step = 1 if rook_col > king_col else -1
        for col in range(king_col + step, rook_col, step):
            if self.board[king_row][col] is not None:
                return False
    
        # Check if the squares are not under attack
        for col in range(king_col, rook_col + 1, step):
            if self.is_position_under_attack(Position(king_row, col), color):
                return False
    
        return True
    
    def get_directional_moves(self, position, directions, color):
        moves = []
        for dr, dc in directions:
            for i in range(1, 8):
                new_row = position.row + i * dr
                new_col = position.col + i * dc
                new_pos = Position(new_row, new_col)
                if self.is_inside_board(new_pos):
                    if self.is_square_empty(new_pos) or self.is_enemy_piece(new_pos, color):
                        moves.append(new_pos)
                        if not self.is_square_empty(new_pos) and self.is_enemy_piece(new_pos, color):
                            break
                    else:
                        break
                else:
                    break
        return moves
    
    def handle_castling(self, king, start_pos, end_pos):
        # Determine if it's kingside or queenside castling
        if end_pos.col == start_pos.col + 2:  # Kingside castling
            rook_start_pos = Position(start_pos.row, 7)
            rook_end_pos = Position(start_pos.row, end_pos.col - 1)
        else:  # Queenside castling
            rook_start_pos = Position(start_pos.row, 0)
            rook_end_pos = Position(start_pos.row, end_pos.col + 1)
    
        # Move the king
        self.board[start_pos.row][start_pos.col] = None
        self.board[end_pos.row][end_pos.col] = king
        king.position = end_pos
        king.has_moved = True
    
        # Move the rook
        rook = self.board[rook_start_pos.row][rook_start_pos.col]
        self.board[rook_start_pos.row][rook_start_pos.col] = None
        self.board[rook_end_pos.row][rook_end_pos.col] = rook
        rook.position = rook_end_pos
        rook.has_moved = True 
    
    
    def get_piece_at(self, position):
        return self.board[position.row][position.col]


    def print_board(self):
        print("  a b c d e f g h")
        print(" +----------------")
        for i, row in enumerate(self.board):
            row_str = str(i) + "|"
            for piece in row:
                if piece:
                    row_str += f"{piece} "
                else:
                    row_str += ". "
            print(row_str)
        print(" +----------------")
        print("  a b c d e f g h")


class ChessSet:
    def __init__(self):
        self.board = Board()
        self.setup_board()
        self.current_player = "White"

    def setup_board(self):
        piece_chesses = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for i in range(8):
            self.board.place_piece(Pawn("White", self.board), Position(1, i))
            self.board.place_piece(Pawn("Black", self.board), Position(6, i))
            self.board.place_piece(piece_chesses[i]("White", self.board), Position(0, i))
            self.board.place_piece(piece_chesses[i]("Black", self.board), Position(7, i))

    def print_board(self):
        self.board.print_board()
        

    def is_checkmate(self, color):
        # Check if the king is in check
        if self.board.is_check(color):
            # Check if there are any moves the player can make to get out of check
            for row in self.board.board:
                for piece in row:
                    if piece and piece.color == color:
                        possible_moves = piece.possible_moves()
                        for move in possible_moves:
                            if not self.board.move_puts_self_in_check(piece, move):
                                return False
            return True
        return False
    
    def is_check(self, color):
        king_position = self.get_king(color).position
        return self.is_position_under_attack(king_position, color)
    
    def get_king(self, color):
        for row in self.board.board:
            for piece in row:
                if isinstance(piece, King) and piece.color == color:
                    return piece
        return None
    
    def is_position_under_attack(self, position, color):
        for row in self.board.board:
            for piece in row:
                if piece and piece.color != color:
                    if position in piece.possible_moves():
                        return True
        return False
    
    def promote_pawn(self, position, color):
        piece_types = ["bishop", "knight", "rook", "queen"]
        promotion_choice = simpledialog.askstring("Pawn Promotion", f"Choose promotion for {color} pawn (bishop, knight, rook, queen):")
        while promotion_choice.lower() not in piece_types:
            messagebox.showerror("Invalid Promotion", "Invalid promotion choice. Choose from bishop, knight, rook, or queen.")
            promotion_choice = simpledialog.askstring("Pawn Promotion", f"Choose promotion for {color} pawn (bishop, knight, rook, queen):")
        piece_class = {
            "bishop": Bishop,
            "knight": Knight,
            "rook": Rook,
            "queen": Queen
        }[promotion_choice.lower()]
        self.board.remove_piece(self.board.get_piece_at(position))
        self.board.place_piece(piece_class(color, self.board, position=position), position)
        self.board.gui.update_board()
        
        # Switch turn to the opponent
        self.board.gui.switch_turn()
        self.board.gui.turn_label.config(text=f"{self.current_player}'s Turn")
        
    def switch_turn(self):
        self.current_player = "Black" if self.current_player == "White" else "White"
        self.board.gui.turn_label.config(text=f"{self.current_player}'s Turn")
        
        
        
class ChessGUI:
    def __init__(self, root, chess_set):
        self.root = root
        self.root.title("Chess Game")
        self.chess_set = chess_set
        self.create_board()

        self.current_player = "White"
        self.start_pos_entry = tk.Entry(root)
        self.end_pos_entry = tk.Entry(root)
        self.submit_button = tk.Button(root, text="Submit Move", command=self.submit_move)
        self.turn_label = tk.Label(root, text=f"{self.current_player}'s Turn")
        self.check_label = tk.Label(root, text="")

        self.setup_widgets()
        self.update_board()

    def create_board(self):
        self.board_frame = tk.Frame(root)
        self.board_buttons = []
        for i in range(8):
            row_buttons = []
            for j in range(8):
                button = tk.Button(self.board_frame, width=4, height=2, command=lambda row=i, col=j: self.square_clicked(row, col))
                button.grid(row=i, column=j)
                row_buttons.append(button)
            self.board_buttons.append(row_buttons)
        self.board_frame.pack()

    def setup_widgets(self):
        start_pos_label = tk.Label(self.root, text="Start Position (e.g., 'a2'):")
        end_pos_label = tk.Label(self.root, text="End Position (e.g., 'a4'):")
        start_pos_label.pack()
        self.start_pos_entry.pack()
        end_pos_label.pack()
        self.end_pos_entry.pack()
        self.submit_button.pack()
        self.check_label.pack()
        self.turn_label.pack()

    def square_clicked(self, row, col):
        position = Position(row, col)
        piece = self.chess_set.board.board[row][col]
        
        # Check if there's already a selected start position
        if not self.start_pos_entry.get():
            if piece and piece.color == self.current_player:
                self.start_pos_entry.delete(0, tk.END)
                self.start_pos_entry.insert(0, self.to_algebraic(position))
        else:
            # If there's a start position selected, select end position
            self.end_pos_entry.delete(0, tk.END)
            self.end_pos_entry.insert(0, self.to_algebraic(position))
            
    def promote_pawn(self, position, color):
        piece_types = ["bishop", "knight", "rook", "queen"]
        promotion_choice = simpledialog.askstring("Pawn Promotion", f"Choose promotion for {color} pawn (bishop, knight, rook, queen):")
        while promotion_choice.lower() not in piece_types:
            messagebox.showerror("Invalid Promotion", "Invalid promotion choice. Choose from bishop, knight, rook, or queen.")
            promotion_choice = simpledialog.askstring("Pawn Promotion", f"Choose promotion for {color} pawn (bishop, knight, rook, queen):")
        piece_class = {
            "bishop": Bishop,
            "knight": Knight,
            "rook": Rook,
            "queen": Queen
        }[promotion_choice.lower()]
        self.board.remove_piece(self.board.get_piece_at(position))
        self.board.place_piece(piece_class(color, self.board, position=position), position)
        self.board.gui.update_board()
        
        # Switch turn to the opponent
        self.switch_turn()
        self.board.gui.turn_label.config(text=f"{self.current_player}'s Turn")

        
    def switch_turn(self):
        self.current_player = "Black" if self.current_player == "White" else "White"
        self.chess_set.board.gui.turn_label.config(text=f"{self.current_player}'s Turn")
    
            
    def submit_move(self):
        start_pos = self.start_pos_entry.get()
        end_pos = self.end_pos_entry.get()
        if self.is_valid_input(start_pos, end_pos):
            start_pos = self.from_algebraic(start_pos)
            end_pos = self.from_algebraic(end_pos)
            if self.chess_set.board.move_piece(start_pos, end_pos):
                piece_at_end_pos = self.chess_set.board.get_piece_at(end_pos)
                if isinstance(piece_at_end_pos, Pawn):
                    if (piece_at_end_pos.color == "White" and end_pos.row == 7) or \
                       (piece_at_end_pos.color == "Black" and end_pos.row == 0):
                        self.chess_set.promote_pawn(end_pos, piece_at_end_pos.color)
                        return
                    
                self.chess_set.switch_turn()
                self.update_board()
                
                if self.chess_set.is_check(self.current_player):
                    if self.chess_set.is_checkmate(self.current_player):
                        winning_player = "Black" if self.current_player == "White" else "White"
                        messagebox.showinfo("Game Over", f"Checkmate! {winning_player} wins!")
                        self.root.destroy()
                    else:
                        self.check_label.config(text="Check!")
                else:
                    self.check_label.config(text="")
                    
                # Check for pawn promotion
                piece_at_end_pos = self.chess_set.board.get_piece_at(end_pos)
                if isinstance(piece_at_end_pos, Pawn):
                    # Check if the pawn reached the last rank
                    if (piece_at_end_pos.color == "White" and end_pos.row == 7) or \
                       (piece_at_end_pos.color == "Black" and end_pos.row == 0):
                        self.chess_set.promote_pawn(end_pos, piece_at_end_pos.color)
                        self.update_board()  # Update the board after promotion
                        return  # Return to prevent further execution
                    
                self.current_player = "Black" if self.current_player == "White" else "White"
                self.turn_label.config(text=f"{self.current_player}'s Turn")  # Update turn label
                self.start_pos_entry.delete(0, tk.END)  # Clear start position entry
                self.end_pos_entry.delete(0, tk.END)  # Clear end position entry
                self.update_board()
        else:
            messagebox.showerror("Invalid Input", "Invalid input format. Please enter positions in algebraic notation (e.g., 'a2').")



    def update_board(self):
        for i in range(8):
            for j in range(8):
                piece = self.chess_set.board.board[i][j]
                if piece:
                    self.board_buttons[i][j].config(text=str(piece))
                else:
                    self.board_buttons[i][j].config(text="")
                    
        if self.chess_set.is_check(self.current_player):
            self.check_label.config(text="Check!")
        else:
            self.check_label.config(text="")
        
        if self.chess_set.is_checkmate(self.current_player):
            winning_player = "Black" if self.current_player == "White" else "White"
            messagebox.showinfo("Game Over", f"Checkmate! {winning_player} Wins!")
            self.root.destroy()

    def is_valid_input(self, start_pos, end_pos):
        if len(start_pos) == len(end_pos) == 2 and start_pos[0].isalpha() and start_pos[1].isdigit() and \
                end_pos[0].isalpha() and end_pos[1].isdigit():
            return True
        else:
            return False

    def from_algebraic(self, algebraic_notation):
        col = ord(algebraic_notation[0]) - ord("a")
        row = int(algebraic_notation[1])
        return Position(row, col)

    def to_algebraic(self, position):
        col = chr(ord("a") + position.col)
        row = str(position.row)
        return col + row


if __name__ == "__main__":
    root = tk.Tk()
    chess_set = ChessSet()
    chess_gui = ChessGUI(root, chess_set)
    chess_gui.chess_set.board.gui = chess_gui
    chess_set.board.gui = chess_gui
    root.mainloop()
