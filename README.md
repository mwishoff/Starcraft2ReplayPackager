# Starcraft2ReplayPackager
Packages replays from Starcraft2 Legacy of the void based on patch.

#Usage:

1.) open powershell/terminal

2.) clone the repository "clone https://github.com/mwishoff/Starcraft2ReplayPackager.git"

3.) cd into the cloned repository

4.) run this command "python SC2_Replay_packager.py"

5.) You'll be prompted for the directory in which your starcraft2 files are.

Here's an example of mine: C:\Users\mwish\Documents\StarCraft II\Accounts\73609262\1-S2-1-2874319\Replays\Multiplayer

6.) Next you'll be prompted for your StarCraft2 handle.

Here's an example of mine: WoBWoB

After you're replays will be parsed through and sorted into their respective patches. In those directories You'll find
the match ups you played, and custom maps will be in a directory called "custom maps".

You can see an example of the input/output of the program in the repository. I've added replays from tournaments Serral
has played in. They're labeled "Serral Replays Before", the output is a directory called "Serral Replays After".

Example:
PS C:\Users\mwish\dev\Starcraft2ReplayPackager> python .\SC2_Replay_Packager.py
Where are your StarCraft replays? C:\Users\mwish\Dev\WCS Replays\Serral
What is your StarCraft handle? Serral