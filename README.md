# chess50

A chess AI built using minimax, alpha-beta-pruning, and Zobrist hashing algorithms

## Distribution

The directory comprises three files and a subdirectory:
1. [`runner.py`](runner.py), which contains the code to run chess50's graphical user interface
1. [`chess50.py`](chess50.py), which contains the code to implement the chess AI
1. [`requirements.txt`](requirements.txt), which contains the list of dependencies
1. [`assets/`](assets/), the folder containing the fonts and images used in the project

## Setup

Open the Terminal, go to the `chess50/` directory, and run `pip install -r requirements.txt`.

## Running chess50

In the `chess50/` directory, run `python runner.py` in the Terminal.

## Features

1. **Choosing a side**. Once the `pygame` window opens, choose the side you want to play or you can let chess50 choose a side for you in a pseudorandom manner.

1. **Moving a chess piece**. To move a chess piece, click the piece you want to move and click the square to which you want it to move.

1. **Playing another game**. When the game is over, click "PLAY AGAIN" if you want to play another game.

1. **Resigning a game**. During your turn, click the flag icon below the chessboard to resign a game.

## Code authorship

2021 © Jessan Rendell G. Belenzo

## Terms of use

Licensed under the GNU General Public License v3.0. See [LICENSE](LICENSE).

<br>

### Acknowledgements

Russell, S., & Norvig, P. (2021). *Artificial Intelligence: A Modern Approach, Global Edition 4th*. Foundations, 19, 23.  

Zobrist, A. L. (1970). *A new hashing method with application for game playing*. ICGA Journal, 13(2), 69-73.  

Fiekas, N. (2021). [*niklasf/python-chess*](https://github.com/niklasf/python-chess). GitHub.  

Lefler, M., et al. (2021). [*Simplified evaluation function*](https://www.chessprogramming.org/Simplified_Evaluation_Function). Chess Programming Wiki.  

Burnett, C. (2012). [*Category:SVG chess pieces*](https://commons.wikimedia.org/wiki/Category:SVG_chess_pieces). Wikimedia Commons.

Smashicons (n.d.). [*Flag free icon*](https://www.flaticon.com/free-icon/flag_660154). Flaticon.

