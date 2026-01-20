categories = {
    "1": "sports",
    "2": "animals",
    "3": "countries",
}

menu = {
    "sports": ["football", "basketball"],
    "animals": ["cat", "dog"],
    "countries": ["germany", "spain", "italy"]
}


def show_options(title, options_dict):
    for key, val in options_dict.items():
        print(key + ": " + val)
    try:
        selected_option = input(title)
        if selected_option in options_dict.keys():
            return options_dict[selected_option]
        else:
            print("Please enter a valid category")
            return show_options(title, options_dict)
    except ValueError:
        print("Please enter a valid category")
        show_options(title, options_dict)


def show_categories():
    selected_category = show_options("Please enter a category ", categories)
    return menu[selected_category]


game_length_options = {
    "1": "short ( 3 rounds )",
    "2": "medium ( 5 rounds )",
    "3": "long ( 10 rounds )",
}

def show_game_length():
    game_length = show_options("how many round would you like to play? ", game_length_options)
    return int(game_length.split("rounds")[0].split("(")[1].strip())


