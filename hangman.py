import os.path
import time
import requests

HANGMAN_ASCII_ART = """Welcome to the game Hangman: \n _    _                                         
| |  | |                                        
| |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __  
|  __  |/ _` | '_ \ / _` | '_ ` _ \ / _` | '_ \ 
| |  | | (_| | | | | (_| | | | | | | (_| | | | |
|_|  |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                     __/ |                      
                     |___/ 
"""
MAX_TRIES = 6

HANGMAN_PHOTOS = {
0: "x-------x",
1: """x-------x 
|
|
|
|
|""",
2: """x-------x
|       |
|       0
|
|
|""",
3: """x-------x
|       |
|       0
|       |
|
|""",
4: """x-------x
|       |
|       0
|      /|\\
|
|""",
5: """x-------x
|       |
|       0
|      /|\\
|      /
|""",
6: 
"""x-------x
|       |
|       0
|      /|\\
|      / \\
|"""
}

def hangman_opening_screen():
    """Print the opening screen of the hangamn game,
    and the maximum number of failed attempts allowed in the game.
    """
    print("{}\nYou have {} attempts in the game.".format(HANGMAN_ASCII_ART, MAX_TRIES))

def get_data_from_api():
    """Get a random word from random-word-api.
    :return: The secret word
    :rtype: string
    """
    # https://random-word-api.herokuapp.com/home
    response = requests.get("https://random-word-api.herokuapp.com/word")   
    secret_word = str(response.json()[0])
    return secret_word

def get_data_from_user():
    """Get from the user the file path and the index of the word, 
    which will be used as the secret word for guessing.
    :return: A tuple of the file path and the index of the word. 
    :rtype: tuple
    """
    # := using Walrus Operator     
    while not os.path.exists(file_path := input("Enter file path: ")):
        print("The path is not valid or doesn't exist. Please try again...")

    while True:
        try:
            index = int(input("Enter index: "))
            break
        except ValueError:
            print("That was no valid number. Please try again...")

    return(file_path, index)

def choose_word(file_path, index):
    """Picks one word from a list of words, read from a file, according to a given index in the list.
    :param: file_path: the path of the file that contains a word list
    :param: index: the position of the word to be picked
    :type: file_path: string
    :type: index: int
    :return: The word in the index position, which will be used as the secret word for guessing.
    :rtype: string
    """ 
    with open(file_path, "r") as read_file:
        my_list = read_file.read().split()
    secret_word = my_list[(index - 1) % len(my_list)]
    return secret_word

def choose_data_source():
    """The user choose the data source type, 'file' or 'api'.
    :return: A string representing the user's choice of data source.
    :rtype: string
    """
    while True:
        data_source = input("Choose data source (file or api): ").lower()
        if data_source in ["file", "api"]:
            if data_source == "file":
                return "file"
            else:
                return "api"
        else:
            print("Invalid choice. Please enter 'file' or 'api'.")

def print_hangman(num_of_tries):
    """Print one of seven situations of the hangman.
    :param num_of_tries: number between 0-6, represents one of seven situations of the hangman.
    :type num_of_tries: int
    """
    print("{}".format(HANGMAN_PHOTOS[num_of_tries]))

def show_hidden_word(secret_word, old_letters_guessed):
    """Show the player his progress in guessing the secret word.
    :param secret_word: represents the secret word that the player need to guess.
    :param old_letters_guessed: contains the letters the player has guessed so far.
    :type secret_word: string
    :type old_letters_guessed: list
    :return: A string consisting of letters and underscores.
    :rtype: string
    """
    underscore = "_" * len(secret_word.strip())
    for i in range(len(secret_word)):
        if secret_word[i] in old_letters_guessed:
            underscore = underscore[:i] + secret_word[i] + underscore[i + 1:]
    underscore = underscore.replace('', ' ').replace(' ', '', 1)
    return underscore.strip()

def guessing_letter_from_user(secret_word, old_letters_guessed, num_of_tries):
    """The user guess a letter for the secret word.
    :param secret_word: the word to be guessed.
    :param old_letters_guessed: list of letters guessed by the user.
    :param num_of_tries: number of incorrect guesses made by the user.
    :type secret_word: string
    :type old_letters_guessed: list
    :type num_of_tries: int
    :return: A tuple containing the updated list of guessed letters and the updated number of incorrect guesses.
    :rtype: tuple
    """
    letter_guessed = input("Guess a letter: ").lower()
    # Checks if the character is valid.
    while not try_update_letter_guessed(letter_guessed, old_letters_guessed):
        letter_guessed = input("Guess a letter: ").lower()
    # Add the letter to to the list     
    old_letters_guessed.append(letter_guessed)
    if letter_guessed not in secret_word:
        print(":(") 
        num_of_tries += 1
        print_hangman(num_of_tries)
    print(show_hidden_word(secret_word, old_letters_guessed))
    return old_letters_guessed, num_of_tries

def try_update_letter_guessed(letter_guessed, old_letters_guessed):
    """Checks the validation of input (character).
    :param letter_guessed: represents the character received from the player.
    :param old_letters_guessed: contains the letters the player has guessed so far.
    :type letter_guessed: string
    :type old_letters_guessed: list
    :return: A Boolean value representing the correctness of the string and if the user has already guessed the character before.
    :rtype: boolean
    """
    if check_valid_input(letter_guessed, old_letters_guessed):
        return True
    else:
        NOT_UPDATED_STR = "X\n{}"
        if old_letters_guessed == []:
            print(NOT_UPDATED_STR[0])
        else:
            print(NOT_UPDATED_STR.format(' -> '.join(sorted(old_letters_guessed))))
    return False

def is_english_letter(letter_guessed):
    """Checks if the input character is an English letter.
    :param letter_guessed: Represents the character received from the user.
    :type letter_guessed: string
    :return: True if the character is an English letter, False otherwise.
    :rtype: boolean
    """
    return letter_guessed.isascii()

def check_valid_input(letter_guessed, old_letters_guessed):
    """Checks the validation of user input (one letter).
    :param letter_guessed: user input
    :param old_letters_guessed: list of the letters that the player has guessed so far.
    :type letter_guessed: string
    :type old_letters_guessed: list
    :return: A Boolean value representing the correctness of the string and if the user has already guessed the character before.
    :rtype: boolean
    """
    old_letters_guessed = [char.lower() for char in old_letters_guessed]
    return (len(letter_guessed) == 1) and (letter_guessed.isalpha()) and (not letter_guessed.lower() in old_letters_guessed) and (is_english_letter(letter_guessed))

def check_win(secret_word, old_letters_guessed):
    """checks whether the player was able to guess the secret word.
    :param secret_word: represents the secret word that the player need to guess.
    :param old_letters_guessed: contains the letters the player has guessed so far.
    :type secret_word: string
    :type old_letters_guessed: list
    :return: True if the user guessed right, False if not.
    :rtype: boolean
    """
    check_compare = all([char in old_letters_guessed for char in secret_word])
    return check_compare

def play_again():
    """Checks if the player want to play the game again.
    :return: True if the player wants to play again, otherwise it returns False.
    :rtype: boolean
    """
    play_again = input("Do you want to play again (yes or no)? ")
    return play_again.lower().startswith('y')

def play_game():
    """Starts and manages a single round of the Hangman game.
    This function initializes the game, displays the Hangman figure,
    and provides feedback on the game outcome (win or lose).
    :return: True if the player wins the game, False otherwise.
    :rtype: boolean
    """
    old_letters_guessed = []
    num_of_tries = 0
    start_time = time.time()
    hangman_opening_screen()
    if choose_data_source() == "api":
        secret_word = get_data_from_api()
    else: 
        file_path, index = get_data_from_user()
        secret_word = choose_word(file_path, index)
    print("\nLet’s start!\n")
    print_hangman(num_of_tries)
    print(show_hidden_word(secret_word, old_letters_guessed))
    
    while num_of_tries < MAX_TRIES:
        old_letters_guessed, num_of_tries = guessing_letter_from_user(secret_word, old_letters_guessed, num_of_tries)
        if check_win(secret_word, old_letters_guessed):
            print("WIN")
            result = "win"
            break

    if num_of_tries == MAX_TRIES:
        print("LOSE")
        result = "lose"

    end_time = time.time()
    full_time = end_time - start_time
    print("Time taken to {}: {:.2f} seconds".format(result, full_time))
    return True    

def main():
    while play_game():
        if not play_again():
            break

if __name__ == "__main__":
    main()
