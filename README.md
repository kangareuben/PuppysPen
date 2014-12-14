PuppysPen
=========

A visual math game for 4th graders written in Python for the XO laptop.

### Requirements
	Python 2.7
	Pygame

How to Run
=========

Puppy's Pen can be played as a standalone pygame app.

### Running as Pygame App

This game can be played as a desktop application. As long as python and pygame are installed, simply run Planetary.py to play and test. Please note, this method does NOT use any XO or sugargame components. This can only be done using Linux.



File Explanations
=================

<!--### activity.py (Entry point)-->


### PuppysPen.py (Pygame App)
Manages the game state and data. Switches and interacts with screen objects

### Screens.py
Holds all the screen specific interactions, most of the game logic is implemented here.

### Level.py
Hold alls the data for a level, takes care of level generation.

### Constants.py
Conatins game-wide constants



License
=======

Puppy's Pen is licensed under the MIT license, found here -  https://raw.githubusercontent.com/kangareuben/PuppysPen/master/LICENSE

Base application taken from https://github.com/FOSSRIT/sugar-quickstart.

Used https://github.com/brendanwhitfield/planetary as a guide for further application structure

Main Puppy asset credit [Jackie Wiley](http://jlw6587.wix.com/portfolio)

Other art assets credit [lynxfive](https://github.com/lynxfive)

[<img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" />](http://creativecommons.org/licenses/by-sa/4.0/")

This work is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/).
