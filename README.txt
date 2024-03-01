This is the development space for Gurbani App using banidb library in python. Text me on whatsapp to contribute.

Pre-requisites
- Make sure you install the banidb module for the program to run
- Install command: pip install banidb

Usage:
- Clone the repository using the https or ssh key
- Run the main.py file

----------------------------------------------------
Operating the program:
- Once you have the main.py file opened, run it
- It will prompt you to enter shabad
- Enter initial letters of every word in shabad that you want to find
- If shabad found, it will show you all the possible matches
- Select the shabad number that you want.
- Finally, it will print the selected shabad.
----------------------------------------------------

**New Operating Procedures with voice search:
- Once you have the main.py file opened, run it
- It will show that the program is listening
- Recite the shabad that you want (complete shabad, not the initial letters of every word)
- Approx one second after you are done, it will show the list of possible matches
- Select the shabad number that you want.
- Finally, it will print the selected shabad

------------TODO-----------------
- Currently, the getShabadMatches() function is not taking any parameter which it was taking in last update
- It should be modified in such a way that it still takes argument. Maybe by using reccursions