Words With Friends Solver
*************************

Welcome to WWFS

Playing the Game
================

Quick start play, simply invoke from command line::

  $ wwfs [options] board tilebag rack

  board --> text file of board layout
  tilebag --> text file of tilebag contents
  rack --> tiles in your rack

Command switches::

  -p, --player1 takes turn
  -o, --player2 takes turn
  -c, --coord position on board to play word
  -d, --direction of positioned word

  -s, --save board state
  -l, --load board state



Installation
============

Install with pip, github or directly from distributed gzipped tarball.
A requirements file is provided in the archive::

    python setup.py develop
    pip install -e git+https://github.com/ian1roberts/wwfsolver.git
