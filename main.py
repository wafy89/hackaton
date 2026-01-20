import random
from categories import show_categories, show_game_length
from data import game_logic

WELCOME_TEXT = "Welcome to the game"


def show_welcome_message():
    print(WELCOME_TEXT)


def get_user_name():
    user_name = input("What is your name? ")
    if user_name == "" or len(user_name) < 2:
       print("Please enter a valid name")
       get_user_name()
    return user_name

if __name__ == '__main__':
    show_welcome_message()
    print("")
    name = get_user_name()
    print("")

    topics = show_categories()
    print("")

    questions_count = show_game_length()
    print("")
    game_logic(questions_count, random.choice(topics))
    