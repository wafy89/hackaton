from wikipedia import DisambiguationError
import random
from categories import show_categories, show_game_length
from color_format import COLOR_FORMAT_MAP
from data import game_logic
from default_text import WELCOME_TEXT


def show_welcome_message():
    print(COLOR_FORMAT_MAP["bright_magenta"][0]+f"\033[1m{WELCOME_TEXT}\033[0m"+COLOR_FORMAT_MAP["bright_magenta"][1])


def start_game(questions_count, topics,name):

    #Fetching game data
    try:
        print("Loading....\n")
        game_logic(questions_count, random.choice(topics),name)
    except DisambiguationError:
        print("Got an error trying again please wait....")
        start_game(questions_count, topics,name)

    #Asking the user to play again or quit
    replay = input("\nDo you want to play again?\nYes(Y) / No(N) ").lower()
    print()

    #Running the game loop again or quitting
    while replay not in ["y", "n"]:
        replay = input("Please enter either 'Y' or 'N' ").lower()
    if replay == "y":
        topics = show_categories()
        print("")
        questions_count = show_game_length()
        print("")
        start_game(questions_count, topics, name)
    else:
        return

def get_user_name():
    user_name = input("What is your name? ")
    if user_name == "" or len(user_name.strip()) <= 2:
       print("Please enter a valid name")
       return get_user_name()
    return user_name


def main():
    show_welcome_message()
    print("")

    name = get_user_name()
    print("")

    topics = show_categories()
    print("")

    questions_count = show_game_length()
    print("")

    start_game(questions_count, topics, name)



if __name__ == '__main__':
    main()


    