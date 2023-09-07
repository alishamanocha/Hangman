from random import choice, random
import random

dictionary_file = "dictionary.txt" # dictionary file with extensive list of words

# dictionary keys are word sizes (1, 2, 3, 4, …, 12), and values are lists of words
# for example, dictionary = { 2 : ['Ms', 'ad'], 3 : ['cat', 'dog', 'sun'] }
# if a word has the size more than 12 letters, put it into the list with the key equal to 12

def import_dictionary(filename):
    dictionary = {}
    max_size = 12
    try:
        dict_file=open(filename, "r") # open the file
        dict_list=dict_file.readlines() # put lines in file into list
        for line in dict_list:
            line = line.strip() # remove extra spaces from lines
            key = len(line) # set the key to the word length
            if key>max_size: # words greater than 12 letters go into list with key equal to 12
                key=max_size
            if key in dictionary: # add word into existing key
                dictionary[key].append(line)
            else:
                dictionary[key]=[line] # add word into new key
    except FileNotFoundError:
        print("The file could not be found.")
    return dictionary

# print the dictionary
def print_dictionary(dictionary):
    max_size=12
    print(dictionary)

# get options size and lives from the user, uses try-except statements for wrong input
def get_game_options():
    print("Please choose a size of a word to be guessed [3 - 12, default any size]:")
    size_input=input()
    try:
        size=int(size_input)
        if size<3 or size>12: # incorrect input --> set size to random integer
            print("A dictionary word of any size will be chosen.\nPlease choose a number of lives [1 - 10, default 5]:")
            size=random.randint(3,12)
        else: # correct input
            print("The word size is set to " + str(size) + ".\nPlease choose a number of lives [1 - 10, default 5]:")
    except ValueError: # input not an integer --> set size to random integer
        print("A dictionary word of any size will be chosen.\nPlease choose a number of lives [1 - 10, default 5]:")
        size=random.randint(3,12)
    lives_input=input()
    try:
        lives=int(lives_input)
        if lives<1 or lives>10: # incorrect input --> set lives to 5
            lives=5
    except: # input not an integer --> set lives to 5
        lives=5
    print("You have " + str(lives) + " lives.")
    return (size, lives)

# MAIN

if __name__ == '__main__' :

    # make a dictionary from a dictionary file
    dictionary = import_dictionary(dictionary_file)

    # print a game introduction
    print("Welcome to the Hangman Game!")

    # START MAIN LOOP (OUTER PROGRAM LOOP)
    continue_playing = True

    while (continue_playing == True):

        # set up game options
        game_options=get_game_options() # tuple with size and lives
        
        size=game_options[0] 
        
        lives=game_options[1]

        # select a word from a dictionary (according to the game options)
        
        wordList1=dictionary[size] #wordList1 is a list of words of the same size from the dictionary
        correct_word=random.choice(wordList1) #randomly select a word from list of words with selected size
        
        # START GAME LOOP   (INNER PROGRAM LOOP)
        guessed_letters = [] # list of letters that have been guessed
        word_letters = [] # list of letters in correct word
        for x in range(size):
            word_letters.append(correct_word[x])
        original_lives = lives
        copy_word_letters=[]
        for x in range(len(word_letters)):
            copy_word_letters.append(word_letters[x])
            
        while (lives > 0 and len(copy_word_letters)>0 and copy_word_letters!=["-"]):

                # format and print the game interface:
                # Letters chosen: E, S, P                list of chosen letters
                # __ P P __ E    lives: 4   XOOOO        hidden word and lives
                print("Letters chosen: ", end='')
                if len(guessed_letters)==0:
                    print("")
                for x in range(len(guessed_letters)):
                    if x<(len(guessed_letters)-1):
                        print(guessed_letters[x]+", ", end='')
                    else:
                        print(guessed_letters[x])
                              
                for x in range(len(word_letters)): #use word to print underscores, dashes, and letters
                    if word_letters[x].upper() in guessed_letters:
                        print(word_letters[x].upper(), end='')
                    elif word_letters[x]=="-": #if dash is in word
                        print("-", end='')
                    else:
                        print("__", end='')

                    if x<(len(word_letters)-1):
                        print("  ", end='')

                print("   lives: " + str(lives) + " ", end='')
                print("X"*(original_lives-lives) + "O"*(lives))
                
                # ask the user to guess a letter
                print("Please choose a new letter >")
                chosen_letter=input()
                while chosen_letter.upper() in guessed_letters:
                    print("You have already chosen this letter.\nPlease choose a new letter >")
                    chosen_letter = input()
                while (chosen_letter.isalpha()==False or len(chosen_letter)!=1):
                    print("Please choose a new letter >")
                    chosen_letter = input()
                guessed_letters.append(chosen_letter.upper()) # update the list of chosen letters
                    
                # if the letter is correct update the hidden word,
                if (chosen_letter.upper() in word_letters or chosen_letter.lower() in word_letters):
                    print("You guessed right!")
                    while (chosen_letter.upper() in copy_word_letters):
                        copy_word_letters.remove(chosen_letter.upper())
                    while (chosen_letter.lower() in copy_word_letters):
                        copy_word_letters.remove(chosen_letter.lower())
                        
                # else update the number of lives
                else:
                    print("You guessed wrong, you lost one life.")
                    lives-=1  

            # END GAME LOOP   (INNER PROGRAM LOOP)

        print("Letters chosen: ", end='')
        if len(guessed_letters)==0:
            print("")
        for x in range(len(guessed_letters)):
            if x<(len(guessed_letters)-1):
                print(guessed_letters[x]+", ", end='')
            else:
                print(guessed_letters[x])
                              
        for x in range(len(word_letters)):
            if word_letters[x].upper() in guessed_letters:
                print(word_letters[x].upper(), end='')
            elif word_letters[x]=="-":
                print("-", end='')
            else:
                print("__", end='')

            if x<(len(word_letters)-1):
                print("  ", end='')

        print("   lives: " + str(lives) + " ", end='')
        print("X"*(original_lives-lives) + "O"*(lives))

        # check if the user guesses the word correctly or lost all lives,
        # if yes finish the game

        if (len(copy_word_letters)==0 or copy_word_letters==["-"]):
            print("Congratulations!!! You won! The word is " + correct_word.upper() + "!")

        elif (lives==0):
            print("You lost! The word is " + correct_word.upper() + "!")

        # END MAIN LOOP (OUTER PROGRAM LOOP)

    # ask if the user wants to continue playing, 
    # if yes start a new game, otherwise terminate the program  
        print("Would you like to play again [Y/N]?")
        play_again = input()
        if play_again=='Y' or play_again=='y':
            continue_playing=True
        else:
            print("Goodbye!")
            continue_playing=False
