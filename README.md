PuppysPen
=========

A visual math game for 4th graders written in Python for the XO laptop.

[Wiki for the project available on wiki.sugarlabs.org](http://wiki.sugarlabs.org/go/Puppy%27s_Pen)

### Requirements
	Python 2.7
	Pygame
	Gtk

How to Run
=========

Puppy's Pen can be played as a standalone Pygame app.

### Running as Pygame App

This game can be played as a desktop application, but only on a machine with Gtk (we recommend using Linux). As long as Python, Pygame, and Gtk are installed, simply run PuppysPen.py to play and test. This does not create a Sugar Activity build, but it will still run on an XO the same way.


File Explanations
=================

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

The Arvo font licensed under the [SIL Open Font License (OFL)](http://scripts.sil.org/cms/scripts/page.php?site_id=nrsi&id=OFL)

The Main puppy asset credit [Jackie Wiley](http://jlw6587.wix.com/portfolio)

All other art assets credit [Cole Cooper (lynxfive)](https://github.com/lynxfive)

[<img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" />](http://creativecommons.org/licenses/by-sa/4.0/")

All art for this project is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/).
