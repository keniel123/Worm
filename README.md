#This worm was made solely for educational purposes as such it should only be used for learning.
# Worm
Worm implemented in Python. Worm utilizes the client-server architecture to create a backdoor on a clients machine where attacker will have a reverse shell on their machine.
The worm makes all .txt files readonly, hides all .exe files and deletes any other file these files are also encrypted using AES.
The worm copies it self into various "copy folders" and also can copy itself to the C drive of the victims machine.
