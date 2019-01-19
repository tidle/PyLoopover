# PyLoopover
PyLoopover is an implimentation of carykh's loopover game.
## Features
- Timer
- Move counter
- Colorfull!
## Controlls
1. Move your mouse over a square, and then use W to move it up, A to move it left, S to move it down, or Dto move it right
2. Just click and drag with the mouse
## Running
### Linux
1. Make sure you have python **3** installed
2. Make sure you have pip (for python 3) installed
3. Run setup.sh, or run `pip3 install pygame`
4. Make sure main.py is executable, then use `./main.py` to run it
### Windows
1. Install python 3 [here](https://www.python.org/downloads/release/python-372/)
2. Open a command prompt
3. Navigate to the folder that you downloaded PyLoopover to using `cd`
4. Run `pip install pygame`
5. Close the command prompt
6. Open the PyLoopover folder, and double click main.py to start
### MacOS
1. Install python 3
2. I have no idea how to do this on a mac.
3. Run setup.sh, i suppose
4. It might work
5. No guarantees
6. Run `python3 main.py`, and cross your fingers
### BSD
1. ...
2. See Linux
## High DPI
**How to make High DPI screens display PyLoopover**
1. Open `config.py` in a text editor
2. Find the lines that say `width=`, `height=`, and `stats_height=`
3. Double the numbers after the =
4. Run main.py. The window should be the right size. (If it is still too small, double the numbers again)
