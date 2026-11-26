'''

Write a game score system. Save the player's name and score to a file. Each time the program runs,
load existing scores and display the top 3.

'''

import csv

with open('main.csv', 'w') as file:
    file.write('name,score\n')  