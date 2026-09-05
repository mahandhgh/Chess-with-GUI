# ♟️ Chess Game with Python & Tkinter

A desktop **Chess Game** implemented in Python using **Object-Oriented Programming (OOP)** and the built-in **Tkinter** GUI library.

The project provides a graphical 8×8 chess board where two players can play against each other. The program implements the movement rules for all standard chess pieces and includes several important chess rules such as **check, checkmate, castling, en passant, and pawn promotion**.

The main purpose of this project is to demonstrate how a relatively complex game can be designed using **classes, inheritance, object-oriented programming, and event-driven GUI programming** in Python.

---

## 🎯 Project Overview

This project implements a playable two-player chess game with a graphical user interface.

The game starts with the standard chess arrangement:

```text
♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜
♟ ♟ ♟ ♟ ♟ ♟ ♟ ♟
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
♙ ♙ ♙ ♙ ♙ ♙ ♙ ♙
♖ ♘ ♗ ♕ ♔ ♗ ♘ ♖
```

Players enter or select the starting and ending squares of a move.

For example:

```text
Start Position: a2
End Position: a4
```

The program validates the move before applying it to the board.

---

# ✨ Features

### ♟️ Standard Chess Pieces

The project implements all six standard chess piece types:

- ♔ King
- ♕ Queen
- ♖ Rook
- ♗ Bishop
- ♘ Knight
- ♙ Pawn

Each piece is implemented as a separate Python class.

---

### 🎮 Graphical User Interface

The game uses **Tkinter** to provide:

- An interactive 8×8 chess board
- Clickable board squares
- Start-position input
- End-position input
- Submit Move button
- Current-player indicator
- Check notification
- Error messages
- Game-over notifications

---

### ♔ King Movement

The King can move one square in any direction:

```text
↖ ↑ ↗
← K →
↙ ↓ ↘
```

The implementation also supports **castling**.

---

### ♕ Queen Movement

The Queen can move any number of squares:

```text
↑
↖   ↗
← Q →
↙   ↘
↓
```

Its movement is implemented using the board's directional-movement helper.

---

### ♖ Rook Movement

The Rook can move horizontally or vertically:

```text
    ↑
    │
←── R ──→
    │
    ↓
```

---

### ♗ Bishop Movement

The Bishop moves diagonally:

```text
↖     ↗

   B

↙     ↘
```

---

### ♘ Knight Movement

The Knight follows its standard L-shaped movement:

```text
  X   X
X       X
    N
X       X
  X   X
```

Unlike sliding pieces, the Knight can jump over other pieces.

---

### ♙ Pawn Movement

The Pawn supports:

- One-square forward movement
- Two-square movement from its starting position
- Diagonal captures
- En passant
- Promotion

White and Black pawns move in opposite directions.

---

# 🏗️ Object-Oriented Design

One of the main aspects of this project is its object-oriented architecture.

The game is divided into several classes.

```text
                    Piece
                      │
       ┌──────────────┼──────────────┐
       │      │       │       │      │
      King  Queen   Rook   Bishop  Knight
                      │
                    Pawn

                     +
                     │
                   Board
                     │
                     ▼
                 ChessSet
                     │
                     ▼
                 ChessGUI
```

---

## `Position`

The `Position` class represents a coordinate on the chess board.

```python
Position(row, col)
```

For example:

```text
Position(1, 0)
```

represents a specific square in the internal board representation.

The class also implements equality comparison so that two positions can be compared directly.

---

# `Piece`

`Piece` is the base class for chess pieces.

It stores common information such as:

```python
self.color
self.board
self.has_moved
self.position
```

Every specific chess piece inherits from this class.

The base class also provides the general `move()` behavior.

---

# `King`

The `King` class inherits from `Piece`.

It implements:

- Standard one-square movement
- Kingside castling
- Queenside castling

The King also uses the board's attack-detection functionality to determine whether castling is allowed.

---

# `Queen`

The Queen combines:

- Horizontal movement
- Vertical movement
- Diagonal movement

The implementation uses:

```python
get_directional_moves()
```

to calculate its possible moves.

---

# `Rook`

The Rook uses four directions:

```text
↑
↓
←
→
```

Its movement continues until:

- The board boundary is reached
- A friendly piece blocks the path
- An enemy piece is encountered

An enemy piece can be captured, but movement stops after the capture.

---

# `Bishop`

The Bishop moves in four diagonal directions:

```text
↖
↗
↙
↘
```

Like the Rook, its movement stops when another piece blocks its path.

---

# `Knight`

The Knight uses eight possible L-shaped offsets:

```text
(+2, +1)
(+2, -1)
(-2, +1)
(-2, -1)

(+1, +2)
(+1, -2)
(-1, +2)
(-1, -2)
```

The Knight does not require a clear path between its starting and ending squares.

---

# `Pawn`

The Pawn has more complex movement rules.

It supports:

### Normal Movement

```text
    ↑
    P
```

### Initial Double Move

A pawn can move two squares from its starting position if both squares are empty.

### Capturing

Pawns capture diagonally:

```text
X   X
 \ /
  P
```

### En Passant

The implementation keeps track of:

```python
self.en_passant_target
```

so that a pawn can perform an en passant capture when the corresponding condition is satisfied.

---

# ♜ Board Management

The `Board` class is responsible for managing the actual chess position.

It contains an 8×8 matrix:

```python
self.board = [[None for _ in range(8)] for _ in range(8)]
```

Each element contains either:

- A chess piece
- `None`

For example:

```text
[
    [R, N, B, Q, K, B, N, R],
    [P, P, P, P, P, P, P, P],
    [., ., ., ., ., ., ., .],
    ...
]
```

---

## Board Responsibilities

The `Board` class handles:

- Adding pieces
- Removing pieces
- Moving pieces
- Checking whether a square is empty
- Checking whether a square contains an enemy piece
- Checking board boundaries
- Detecting attacks
- Detecting check
- Simulating moves
- Castling
- En passant

---

# 🔎 Move Validation

Before a move is executed, several checks are performed.

The general flow is:

```text
Player selects a move
        │
        ▼
Is the input valid?
        │
        ▼
Does a piece exist?
        │
        ▼
Is the destination a legal move
for that piece?
        │
        ▼
Would the move leave
the player's King in check?
        │
        ▼
Execute the move
```

If any validation fails, the user receives an error message.

---

# ⚔️ Check Detection

The project includes a mechanism for determining whether a King is under attack.

The method:

```python
is_check(color)
```

locates the King's position and checks whether an opponent's piece can attack that square.

Conceptually:

```text
Opponent pieces
      │
      ▼
Can any piece attack
the King?
      │
   ┌──┴──┐
  Yes    No
   │      │
   ▼      ▼
 Check   Safe
```

When a player is in check, the GUI displays:

```text
Check!
```

---

# 💀 Checkmate Detection

The `ChessSet` class includes:

```python
is_checkmate(color)
```

The algorithm first checks whether the King is currently in check.

If it is, the program examines possible moves for the player's pieces.

If no legal move can remove the check, the game declares checkmate.

```text
King in Check?
      │
 ┌────┴────┐
No         Yes
│           │
▼           ▼
Continue   Try legal moves
              │
        ┌─────┴─────┐
        │           │
      Move       No valid
      exists      move
        │           │
        ▼           ▼
      Not        Checkmate
    Checkmate
```

When checkmate is detected, the program displays the winning player and closes the game.

---

# 🏰 Castling

The implementation supports both types of castling:

### Kingside Castling

```text
King: e1 → g1
Rook: h1 → f1
```

### Queenside Castling

```text
King: e1 → c1
Rook: a1 → d1
```

The program checks whether:

- The King has not moved
- The corresponding Rook has not moved
- The squares between them are empty
- The relevant squares are not under attack

The `has_moved` property of pieces is used to track whether the King or Rook has previously moved.

---

# 🔄 En Passant

The game also implements the special Pawn capture known as **en passant**.

When a Pawn moves two squares from its starting position, the board stores the appropriate intermediate square:

```python
self.en_passant_target
```

An opposing Pawn can then use this target square for an en passant capture when permitted.

After subsequent moves, the target is cleared unless another valid two-square Pawn move creates a new target.

---

# 👑 Pawn Promotion

When a Pawn reaches the final rank, the player is asked to choose a promotion piece.

The available choices are:

```text
bishop
knight
rook
queen
```

For example:

```text
Pawn Promotion

Choose promotion:
queen
```

The original Pawn is replaced by the selected piece.

---

# 🖱️ GUI Interaction

The graphical interface is implemented using Tkinter.

The board consists of 64 buttons:

```text
┌───┬───┬───┬───┬───┬───┬───┬───┐
│ ♜ │ ♞ │ ♝ │ ♛ │ ♚ │ ♝ │ ♞ │ ♜ │
├───┼───┼───┼───┼───┼───┼───┼───┤
│ ♟ │ ♟ │ ♟ │ ♟ │ ♟ │ ♟ │ ♟ │ ♟ │
├───┼───┼───┼───┼───┼───┼───┼───┤
│   │   │   │   │   │   │   │   │
├───┼───┼───┼───┼───┼───┼───┼───┤
│   │   │   │   │   │   │   │   │
├───┼───┼───┼───┼───┼───┼───┼───┤
│   │   │   │   │   │   │   │   │
├───┼───┼───┼───┼───┼───┼───┼───┤
│   │   │   │   │   │   │   │   │
├───┼───┼───┼───┼───┼───┼───┼───┤
│ ♙ │ ♙ │ ♙ │ ♙ │ ♙ │ ♙ │ ♙ │ ♙ │
├───┼───┼───┼───┼───┼───┼───┼───┤
│ ♖ │ ♘ │ ♗ │ ♕ │ ♔ │ ♗ │ ♘ │ ♖ │
└───┴───┴───┴───┴───┴───┴───┴───┘
```

A player can click a square to select the starting position and then click another square to select the destination.

---

# 🔤 Algebraic Notation

The GUI accepts chess positions in a simple algebraic-style format such as:

```text
a2
e4
g8
```

The project converts this notation into internal row/column coordinates.

For example:

```text
a2
```

is converted into a `Position` object.

The conversion is handled by:

```python
from_algebraic()
```

and:

```python
to_algebraic()
```

---

# 🔁 Turn Management

The game starts with:

```text
White's Turn
```

After a valid move, the turn changes:

```text
White → Black → White → Black → ...
```

The current player's turn is displayed in the GUI.

The program also prevents a player from selecting an opponent's piece through the board-click interface.

---

# 🧱 Project Architecture

The main components communicate approximately as follows:

```text
                    ChessGUI
                       │
                       ▼
                   ChessSet
                       │
                       ▼
                     Board
                       │
          ┌────────────┼────────────┐
          │            │            │
          ▼            ▼            ▼
       Position      Pieces      Game Rules
                         │
        ┌────────────────┼────────────────┐
        │        │       │       │        │
      King     Queen    Rook   Bishop   Knight
                                      │
                                     Pawn
```

This separation makes it possible to keep:

- GUI logic
- Board management
- Piece movement
- Chess rules

as separate responsibilities.

---

# 📁 Project Structure

```text
chess-game/
│
├── chessGUI.py
└── README.md
```

### `chessGUI.py`

The main Python source file containing:

- Chess piece classes
- Board implementation
- Chess game logic
- Move validation
- Check/checkmate detection
- Special chess moves
- Tkinter graphical interface

---

# 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Tkinter | Graphical user interface |
| OOP | Game architecture |
| Recursion / Simulation | Move and check validation |
| Unicode Chess Symbols | Piece visualization |

Tkinter is part of Python's standard library, so no external GUI package is required.

---

# ⚙️ Requirements

You need:

- Python 3.x
- Tkinter

On most standard Python installations, Tkinter is already included.

You can check your Python installation with:

```bash
python --version
```

---

# 🚀 Installation & Usage

## 1. Clone the Repository

```bash
git clone https://github.com/mahandhgh/Chess-with-GUI.git
```

## 2. Navigate to the Project

```bash
cd chess-game
```

## 3. Run the Game

```bash
python chessGUI.py
```

The chess window should open automatically.

---

# 🎮 How to Play

### Method 1 — Using the Input Fields

Enter the starting square:

```text
a2
```

Then enter the destination:

```text
a4
```

Click:

```text
Submit Move
```

The program validates and executes the move.

---

### Method 2 — Clicking the Board

You can also select the starting and ending squares directly by clicking on the board.

First click your own piece.

Then click the destination square.

The selected positions will be placed into the input fields.

---

# 🧪 Example Move

At the beginning of the game, White can move the pawn from:

```text
a2
```

to:

```text
a4
```

The input would be:

```text
Start Position: a2
End Position: a4
```

After submitting the move, the board is updated and the turn changes to Black.

---

# ⚠️ Current Limitations

This project focuses on implementing the core game mechanics and GUI, so some advanced features are not included.

### Not Included

- Chess AI / computer opponent
- Minimax algorithm
- Alpha-Beta pruning
- Move history
- Undo / redo
- Save / load game
- Chess clocks
- Draw by threefold repetition
- Fifty-move rule
- Full insufficient-material draw detection
- PGN import/export
- Online multiplayer
- Network play

The game is designed primarily as a **local two-player desktop application**.

---

# 🚀 Possible Improvements

The project can be extended significantly.

## 🤖 1. Add a Chess AI

A computer opponent could be implemented using:

```text
Minimax
   +
Alpha-Beta Pruning
```

The AI could evaluate board positions and select the best available move.

---

## 🎨 2. Improve the GUI

Possible improvements include:

- Traditional chessboard colors
- Highlighting legal moves
- Highlighting the selected piece
- Highlighting the last move
- Better piece graphics
- Captured-piece display
- Improved layout
- Chessboard coordinates

---

## ↩️ 3. Add Undo / Redo

A move-history system could store previous board states and allow players to undo or redo moves.

---

## 💾 4. Save and Load Games

The game could support saving the current position and loading it later.

A standard format such as **FEN** could be used for board positions.

---

## 📜 5. Move History

The GUI could display moves such as:

```text
1. e4 e5
2. Nf3 Nc6
3. Bb5 a6
```

---

## 🌐 6. Online Multiplayer

The game could eventually be converted into a network-based application where two players connect through a server.

---

# 🎓 Learning Objectives

This project demonstrates several important software-development concepts.

### Object-Oriented Programming

The project uses:

- Classes
- Inheritance
- Encapsulation
- Object relationships
- Polymorphic behavior

For example:

```python
class King(Piece):
```

allows the King to inherit common functionality from the `Piece` class while implementing its own movement rules.

---

### Data Structures

The chessboard is represented using a two-dimensional list:

```python
board[row][column]
```

Objects representing pieces are stored inside the board.

---

### Event-Driven Programming

Tkinter buttons trigger functions when the user interacts with the GUI.

For example:

```text
User clicks square
       ↓
square_clicked()
       ↓
Select position
       ↓
Submit move
       ↓
Validate move
       ↓
Update board
```

---

### Algorithmic Thinking

The project requires handling several non-trivial problems:

- Legal movement
- Collision detection
- Capturing
- Board boundaries
- Attack detection
- Check detection
- Checkmate detection
- Special moves
- State changes

---

# 📊 Design Principles

The implementation follows a simple separation of responsibilities:

| Component | Responsibility |
|---|---|
| `Position` | Represents board coordinates |
| `Piece` | Common piece behavior |
| `King` | King movement and castling |
| `Queen` | Queen movement |
| `Rook` | Rook movement |
| `Bishop` | Bishop movement |
| `Knight` | Knight movement |
| `Pawn` | Pawn movement and special rules |
| `Board` | Board state and move validation |
| `ChessSet` | Game state and higher-level rules |
| `ChessGUI` | User interface and interaction |

---

⭐ If you found this project useful for learning Python, OOP, or GUI programming, consider giving the repository a star!
