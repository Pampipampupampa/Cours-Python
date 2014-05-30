#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""
    The game of the Hangman.
    More or less game.
"""

########################################
#### Classes and Methods imported : ####
########################################

from random import choice, randint

#####################
#### Constants : ####
#####################

mots = ['tillage', 'facilitation', 'emouchasse', 'masquaient', 'rubanons']

#######################################
#### Classes, Methods, Functions : ####
#######################################


# Check if word found or if player hanged up ---> game ended
check = lambda word, n_turns: word.isupper() or n_turns == 0
# Print result according to game state
result = lambda word: "\n" + word.upper() + ("\nWon" if word.isupper() else "\nLose")
# Print word at current state
printer = lambda word: " ".join(char if char.isupper() else "*" for char in word)


def hangman(word, n_turns):
    """
        Recursive hangman game loop.
        Upper characters used to check characters found by player.
    """
    if check(word, n_turns):
        print(result(word))
    else:
        print("\n" + printer(word) + "\t{} turns before dying".format(n_turns))
        new_char = input("New character please ...").strip().lower()
        if new_char in word:
            word = "".join(new_char.upper()
                           if char == new_char
                           else char for char in word)
        return hangman(word, n_turns - 1)


def more_or_less(target=randint(0, 100), nbr=-1):
    """
        Recursive more or less game loop.
        Dict used as switcher.
    """
    if target == nbr:
        print("\nGood job")
    else:
        more_or_less(target=target,
                     nbr=int(input({nbr < target: "More \t",
                                    nbr > target: "Less \t",
                                    nbr < 0: "Start\t"}[True])))

########################
#### Main Program : ####
########################

if __name__ == '__main__':
    # Random game
    hangman(choice(mots), 14)
    more_or_less()
