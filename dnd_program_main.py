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
CHARACTER_MENU = """
====================================
       CHARACTER MENU
====================================
    1. Select character
    2. Delete character and player
    3. Display character info
    4. Go back
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
            print("Loading characters...")
            available_player_characters = load_data(PLAYER_DATA_FILE)
            print(f"Available characters: \n")

            for i, (
                player,
                (character_name, character_stats, character_ability_scores),
            ) in enumerate(available_player_characters.items()):
                print(f"Player {i+1}: {player} \n \t Character: {character_name}")

            print(CHARACTER_MENU)
            character_menu_choice = get_valid_integer("Enter your choice (1-4): ", 1, 4)

            while character_menu_choice != 4:
                if character_menu_choice == 1:
                    print("Select character:")
                    character_selection = get_valid_integer(
                        "Enter the player number to select their character: ",
                        1,
                        len(available_player_characters),
                    )
                    selected_player = list(available_player_characters.keys())[
                        character_selection - 1
                    ]
                    print(
                        f"Selected character for player {selected_player}: {available_player_characters[selected_player][0]}"
                    )
                    write_to_file(
                        selected_player,
                        available_player_characters[selected_player],
                        f"player_{selected_player}_character.csv",
                    )

                    # Select character logic here

                elif character_menu_choice == 2:
                    print("Deleting character...")
                    # Delete character logic here

                elif character_menu_choice == 3:
                    print("Select character to display info:")
                    character_selection = get_valid_integer(
                        "Enter the player number to select their character: ",
                        1,
                        len(available_player_characters),
                    )
                    selected_player = list(available_player_characters.keys())[
                        character_selection - 1
                    ]
                    display_character_info(available_player_characters[selected_player])

                else:
                    print("Invalid choice. Please try again.")
                character_menu_choice = get_valid_integer(
                    "Enter your choice (1-4): ", 1, 4
                )
            print("Exiting character menu.")

        # Load character logic here

        else:
            print("Invalid choice. Please try again.")

    print("Exiting game. Goodbye!")


################################# - FUNCTIONS - #################################


def get_valid_integer(prompt, min=None, max=None):
    """Gets a valid integer input from the user within optional min and max bounds."""
    is_valid_input = False
    while not is_valid_input:
        try:
            user_input = int(input(prompt))
            if min is not None and user_input < min:
                print(f"Number must be {min} or higher")
            elif max is not None and user_input > max:
                print(f"Number must be {max} or lower")
            else:
                is_valid_input = True
        except ValueError:
            print("Invalid (not an integer)")
    return user_input


def load_data(filename):
    """Loads data from a CSV file and returns a dictionary mapping player names to their character data."""
    character_stats = []
    character_ability_scores = []
    player_name_to_character = {}

    in_file = open(filename, "r")
    in_file.readline()  # Skip header line
    for line in in_file:
        line = line.strip()
        data = line.split(",")
        # Basic validation: we expect at least 15 columns per the header/example
        if len(data) < 15:
            print(
                f"Warning: skipping malformed row (expected >=15 columns, got {len(data)}): {data}"
            )
            continue
        player_name = data[0]
        character_name = data[1]
        character_stats = data[
            2:9
        ]  # class, level, current health, max health, current spell slots, max spell slots, armour
        character_ability_scores = data[
            9:
        ]  # dexterity, constitution, charisma, wisdom, intelligence, strength

        # Format the lists as joined strings so alignment works like the character name
        stats_str = ", ".join(map(str, character_stats))
        abilities_str = ", ".join(map(str, character_ability_scores))
        print(
            f"Character Name: {character_name:<20} Stats: {stats_str:<30} Abilities: {abilities_str}"
        )  # Debug print

        data = (
            character_name,
            character_stats,
            character_ability_scores,
        )  # Combine stats and ability scores as tuple
        player_name_to_character[player_name] = (
            data  # Map player name to character data
        )

    in_file.close()
    """--------------------  EXAMPLE DATA FORMAT  --------------------
    [0] player name, [1] character name, [2] class, [3] level, [4] current health, 
    [5] max health, [6] current spell slots, [7] max spell slots, [8] armour, 
    [9] dexterity, [10] constitution, [11] charisma, [12] wisdom, [13] intelligence, [14] strength"""

    print("====================================")
    for player, character_data in player_name_to_character.items():
        print(f"Player: {player}, Character Data: {character_data}")

    return player_name_to_character


def write_to_file(player_name, character_data, filename):
    """Write the selected character data to a CSV file."""
    out_file = open(filename, "w")
    out_file.write(
        "Player Name,Character Name,Class,Level,Current Health,Max Health,Current Spell Slots,Max Spell Slots,Armour,Dexterity,Constitution,Charisma,Wisdom,Intelligence,Strength\n"
    )
    out_file.write(
        f"{player_name},{character_data[0]},{','.join(character_data[1])},{','.join(character_data[2])}\n"
    )
    out_file.close()


def display_character_info(character_data):
    """Displays the character information in a readable format."""
    character_name, character_stats, character_ability_scores = format_character_info(
        character_data
    )
    print(character_name)
    print(f"Stats: \n{character_stats}")
    print(f"Abilities: \n{character_ability_scores}")


def format_character_info(character_data):
    """Formats character data for display."""
    character_name = f"====================================\nName: {character_data[0]}\n===================================="
    character_stats = f"====================================\n  Class: {character_data[1][0]} \t Level: {character_data[1][1]} \t HP: {character_data[1][2]}/{character_data[1][3]} \n  Spell Slots: {character_data[1][4]}/{character_data[1][5]} \t AC: {character_data[1][6]}\n===================================="
    character_ability_scores = f"====================================\n  DEX: {character_data[2][0]} \t CON: {character_data[2][1]}\t CHA: {character_data[2][2]} \n  WIS: {character_data[2][3]} \t INT: {character_data[2][4]}\t STR: {character_data[2][5]}\n====================================\n"
    return character_name, character_stats, character_ability_scores


if __name__ == "__main__":
    main()
