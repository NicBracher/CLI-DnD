"""
This is a dnd program that will run a CLI dnd game. This program will act as the main body of the game

"""

PLAYER_DATA_FILE = "data/player_data.csv"
START_MENU = """
====================================
   WELCOME TO DND GAME
====================================
   1. Create character
   2. Load character
   3. Exit
====================================
"""
LOAD_CHARACTER_MENU = """
====================================
       LOAD CHARACTER MENU
====================================
    1. Select character
    2. Delete character
    3. Display character info
    4. Exit to main menu
====================================
"""



def main():
    print(START_MENU)
    start_menu_choice = get_valid_integer("Enter your choice (1-3): ", 1, 3)
    while start_menu_choice != 3:
        # Create new character
        if start_menu_choice == 1:
            print("Creating a new character...")
            # Initialize new character logic here

        # Load existing character
        elif start_menu_choice == 2:
            print("Loading character...")
            available_player_characters = load_data(PLAYER_DATA_FILE)
            print(f"Available characters: \n")

            for i, (player, (character_name, character_stats, character_ability_scores)) in enumerate(available_player_characters.items()):
                print(f"Player {i+1}: {player} \n \t Character: {character_name}")
            
            print(LOAD_CHARACTER_MENU)
            load_character_choice = get_valid_integer("Enter your choice (1-4): ", 1, 4)

            while load_character_choice != 4:
                if load_character_choice == 1:
                    print("Selecting character...")
                    # Select character logic here


                elif load_character_choice == 2:
                    print("Deleting character...")
                    # Delete character logic here


                elif load_character_choice == 3:
                    print("Displaying character info...")
                    # Display character info logic here


                load_character_choice = get_valid_integer("Enter your choice (1-4): ", 1, 4)

            

            

        # Load character logic here


        else:
            print("Invalid choice. Please try again.")

    print("Exiting game. Goodbye!")

################################# - FUNCTIONS - #################################

def get_valid_integer(prompt, min=None, max=None):
    is_valid_input = False
    while not is_valid_input:
        try:
            user_input = int(input(prompt))
            if min is not None and user_input < min:
                print(f"Number must be >= {min}")
            elif max is not None and user_input > max:
                print(f"Number must be <= {max}")
            else:
                is_valid_input = True
        except ValueError:
            print("Invalid (not an integer)")
    return user_input


def load_data(filename):
    character_stats = []
    character_ability_scores = []
    player_name_to_character = {}

    in_file = open(filename, "r")
    in_file.readline()  # Skip header line
    for line in in_file:
        line = line.strip()
        data = line.split(",")
        player_name = data[0]
        character_name = data[1]
        character_stats = data[2:8]  # Select character stats
        character_ability_scores = data[8:]  # Select ability scores
        data = character_name, character_stats, character_ability_scores  # Combine stats and ability scores as tuple
        player_name_to_character[player_name] = data  # Map player name to character data

    in_file.close()
    """ EXAMPLE DATA FORMAT
    [0] player name, [1] character name, [2] class, [3] level, [4] current health, 
    [5] max health, [6] current spell slots, [7] max spell slots, [8] armour, 
    [9] dexterity, [10] constitution, [11] charisma, [12] wisdom, [13] intelligence, [14] strength
    """

    # print(player_name_to_character)  # For debugging purposes
    print("====================================")
    for player, character_data in player_name_to_character.items():
        print(f"Player: {player}, Character Data: {character_data}")

    return player_name_to_character


if __name__ == "__main__":
    main()