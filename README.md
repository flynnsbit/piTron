# piTron

For 27 inch LCD:
Change Recognizer animation to video

Better Stern Logo or Boot animation

It looks like this code is for a game that uses Pygame and a serial connection to communicate with an external device. The code initializes Pygame, sets up a display and some fonts, and creates a function for checking the presence of a file.

The code also defines a list of game modes and creates a dictionary of flags, one for each game mode, initialized to False. There is also a dictionary that maps state IDs to flags, which is used to reset flags to their default state when a ball is lost.

The code then sets up logging and attempts to communicate with the serial device to get its version number. If an error occurs during serial communication, it is logged and the program continues.

Next, the code enters the main game loop, which runs until the user quits the game. In each iteration of the loop, the code checks the serial connection for new input, parses the input to extract state information, and sets the flags in the dictionary accordingly.

The code also checks for user input and updates the game display based on the current game state. When the game is over, the code plays a game over sound and displays a game over screen.

Overall, the code looks functional, but it could benefit from some refactoring and clean-up. For example, the code uses a lot of global variables, which can make the code difficult to understand and maintain. It would be better to avoid using global variables and instead pass the necessary information as arguments to functions. Additionally, the code could be more organized and easier to read if it were broken up into smaller, more focused functions.



Bugs:
Why do some of the modes black out either disc lit (bank down) or Recognizer hit (bank up)

What is mode 19

Build Player 1 -4 videos and handle.  Could this be done in Mode 19

Build Non-Copywrite video versions of all mode states

Build itunes file mode ripper

Move tron pyc and media over to usb stick
Auto mount usb on boot



Finish stupid mini LCD mods

Print Vesa mount for Pi 3

Build null model cable to GPIO

Power Pi with GPIO


Handle player 1 -4 states tracking for each player


Add 19 ball ends to code

