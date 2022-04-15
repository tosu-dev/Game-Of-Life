# Game-Life

## What is it ?
The Game of Life is a game of cellular automaton created by John Horton Conway in 1970, a british mathematician.

There are cells in an initial state and they will evolve depending of some rules :
  - A cell dies if there are less than 2 cells around
  - A cell dies if there are more than 3 cells around
  - A cell is created or stay alive if there are exactly 3 cells around
 
 Here's a image of the game (not mine)
 
 <img src="Game-Lifegif.gif" alt="Game of Life image" width="400" height="400"/>
 
 If you want to see more of this game, here's a french video that explain the game (there are english subtitles) : 
 
 [Le Jeu de la Vie - ScienceEtonnante](https://www.youtube.com/watch?v=S-W0NX97DB0)
 
 
 ## How to play
 Lauch the file `main.py`. For this you need python to be installed and pygame. 
 
 I code this project with python 3.9.1.
 
 Download python : https://www.python.org/downloads/
 
 Install pygame : https://www.pygame.org/wiki/GettingStarted
 
 Keys :
  - Enter: Editor mode On/Off
  - Left/Right click: Put/Remove cells in editor mode
  - Backspace: Reset the game map in editor mode
  - Space: Pause/Unpause the simulation
  - Left/Right arrows: Naviguate betweens generations in simulation
  - o: Open options menu

 To launch the simulation, quit the editor mode and unpause.
 
 The option "Ticks" is the speed of the simulation
 
 The option "Cells color" must be write as `r, g, b`
