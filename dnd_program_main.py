"""
This is a dnd program that will run a CLI dnd game. This program will act as the main body of the game

"""

################################# - IMPORTS - #################################
import random

################################# - CONSTANTS - #################################

PLAYER_DATA_FILE = "data/player_data.csv"
MENU_LINE_SEPARATOR = "===================================="
SUBMENU_LINE_SEPARATOR = "------------------------------------"
START_MENU = f"""
====================================
   WELCOME TO DND GAME
====================================
   1. Create character
   2. Load character
   3. Random encounter
   7. Display selected character sheet
   8. Test Area
   9. Exit
====================================
"""
CHARACTER_MENU = f"""
====================================
       CHARACTER MENU
====================================
    1. Select character
    2. Delete character and player
    3. Display character info
    9. Go back
====================================
"""
CHARACTER_CLASS_MENU = f"""
====================================
       CHARACTER CLASS MENU
====================================
    1. Fighter
    2. Wizzard
    3. Rogue
    4. Cleric
    5. Ranger
    6. Bard
    7. Paladin
    8. Druid
    9. Go back
====================================
"""
SMALL_INDENT = "  "
MEDIUM_INDENT = "    "
LARGE_INDENT = "      "


################################# - MAIN - #################################


def main():
    print(START_MENU)
    # fmt: off
    start_menu_choice = get_valid_integer("Enter your choice (1-3): ", 1, 9, f"\nInvalid choice. select from the menu.\n{START_MENU}")
    # fmt: on
    selected_player = None
    while start_menu_choice != 9:
        # Create new character
        if start_menu_choice == 1:
            print("Creating a new character...")
            character_data = create_character()
            print("Character created successfully!")
            write_to_file(character_data["player_name"], (character_data["character_name"], [
                character_data["character_class"],
                str(character_data["character_level"]),
                str(character_data["current_health"]),
                str(character_data["maximum_health"]),
                str(character_data["current_spell_slots"]),
                str(character_data["maximum_spell_slots"]),
                str(character_data["armour_class"]),
            ], [
                str(character_data["ability_scores"].get("DEX", 0)),
                str(character_data["ability_scores"].get("CON", 0)),
                str(character_data["ability_scores"].get("CHA", 0)),
                str(character_data["ability_scores"].get("WIS", 0)),
                str(character_data["ability_scores"].get("INT", 0)),
                str(character_data["ability_scores"].get("STR", 0)),
            ]), temporary_filename := f"player_{character_data['player_name']}_character.csv")

            character_data = load_data(temporary_filename).get(character_data["player_name"])
            display_character_info(character_data)

            print(f"Is this correct? (y/n)")
            confirmation = input().strip().lower()
            if confirmation == "y":
                print("Character confirmed.")
                old_data = load_data(PLAYER_DATA_FILE)
                new_data = {**old_data, **{character_data[0]: character_data}}
                out_file = open(PLAYER_DATA_FILE, "w")
                # fmt: off
                out_file.write("Player Name,Character Name,Class,Level,Current Health,Max Health,Current Spell Slots,Max Spell Slots,Armour,Dexterity,Constitution,Charisma,Wisdom,Intelligence,Strength\n")
                for player_name, (char_name, char_stats, char_ability_scores) in new_data.items():
                    out_file.write(f"{player_name},{char_name},{','.join(char_stats)},{','.join(char_ability_scores)}\n")
                # fmt: on
                out_file.close()
            else:
                print("Character creation cancelled.")

        # Load existing character
        elif start_menu_choice == 2:
            available_player_characters = load_data(PLAYER_DATA_FILE)
            print(f"\n{MENU_LINE_SEPARATOR}\n  Available characters: \n")

            display_players(available_player_characters)

            print(CHARACTER_MENU)
            character_menu_choice = get_valid_integer("Enter your choice (1-9): ", 1, 9)

            while character_menu_choice != 9:

                # Select character
                if character_menu_choice == 1:
                    print(f"\n{MENU_LINE_SEPARATOR}\nCharacter Selection:\n")
                    # fmt: off
                    display_players(available_player_characters)
                    character_selection = get_valid_integer(f"{MENU_LINE_SEPARATOR}\n\nEnter the player number to select their character (1-{len(available_player_characters)}): ", 1, len(available_player_characters),  f"INVALID CHOICE: Input number that corresponds to a player.\n")
                    selected_player = list(available_player_characters.keys())[character_selection - 1]
                    print(f"MESSAGE: Selected character for player {selected_player}: {available_player_characters[selected_player][0]}")
                    write_to_file(selected_player, available_player_characters[selected_player], f"player_{selected_player}_character.csv")
                    # fmt: on

                # Delete character
                elif character_menu_choice == 2:
                    print("Deleting character...")

                # Display character info
                elif character_menu_choice == 3:
                    # fmt: off
                    print(f"Select character to display info\n\n{MENU_LINE_SEPARATOR}\n  Available characters: \n")
                    display_players(available_player_characters)
                    character_selection = get_valid_integer(f"\n{MENU_LINE_SEPARATOR}\n\nEnter the player number to select their character: ",1,len(available_player_characters), f"INVALID CHOICE. Input number that corresponds to a player.\n{MENU_LINE_SEPARATOR}")
                    selected_player = list(available_player_characters.keys())[character_selection - 1]
                    display_character_info(available_player_characters[selected_player])
                    # fmt: on

                else:
                    print("MESSAGE: Not currently an option.")
                # fmt: off
                print(CHARACTER_MENU)
                character_menu_choice = get_valid_integer("Enter your choice (1-9): ", 1, 9)
                # fmt: on
            print("MESSAGE: Exiting character menu.")

        # Load character logic here

        elif start_menu_choice == 3:
            print("Starting a random encounter...")
            # Random encounter logic here

        elif start_menu_choice == 7:
            # fmt: off
            print("Displaying selected character sheet...")
            if selected_player:
                print(f"MESSAGE: Displaying character sheet for selected player: {selected_player}")
                character_data = load_data(PLAYER_DATA_FILE).get(selected_player)
                if character_data:
                    display_character_info(character_data)
                else:
                    print(f"MESSAGE: No character data found for player: {selected_player}")
            else:
                print("MESSAGE: No player selected. Please select a player first.")
            # fmt: on

        elif start_menu_choice == 8:
            print("MESSAGE: Entering Test Area...")
            if selected_player:
                print(f"MESSAGE: Testing with selected player: {selected_player}")
            else:
                print(
                    "MESSAGE: No player selected for testing. Returning to main menu."
                )
            # Test area logic here

        else:
            print("INVALID CHOICE. Please try again.")
        print(START_MENU)
        # fmt: off
        start_menu_choice = get_valid_integer("Enter your choice (1-3): ", 1, 9, f"\nInvalid choice. select from the menu.\n{START_MENU}")
        # fmt: on
    print("Exiting game. Goodbye!")



################################# - FUNCTIONS - #################################

def create_character():
    player_name = input("Enter player name: ").title()
    print(f"Player Name: {player_name}")
    character_classes_to_selection = {1: "Fighter", 2: "Wizzard", 3: "Rogue", 4: "Cleric", 5: "Ranger", 6: "Bard", 7: "Paladin", 8: "Druid", 9: "Sorcerer"}
    character_name = input("Enter character name: ").title()
    print(f"Character Name: {character_name}")
    character_class = get_valid_integer(CHARACTER_CLASS_MENU + "\nEnter character class (1-9): ", 1, 9)
    print(f"Character Class: {character_classes_to_selection[character_class]}")
    character_level = get_valid_integer("Enter character level (1-20): ", 1, 20)
    print(f"Character Level: {character_level}")
    unassigned_scores = []
    for i in range(6):
        score = random.randint(8, 18)
        unassigned_scores.append(score)
    print(f"The following scores have been rolled, assign them to abilities as you see fit: {unassigned_scores}")
    assigned_scores = {}
    abilities = ["DEX", "CON", "CHA", "WIS", "INT", "STR"]
    for score in unassigned_scores:
        ability = input(f"Assign score {score} to which ability ({', '.join(abilities)}): ").upper()
        assigned_scores[ability] = score
        abilities.remove(ability)
    print(f"Assigned scores: {assigned_scores}")
    con_modifier = calculate_modifier(assigned_scores.get("CON", 0))
    dex_modifier = calculate_modifier(assigned_scores.get("DEX", 0))
    current_health = calculate_health(con_modifier, character_level)
    maximum_health = current_health
    print(f"Maximum Health: {maximum_health}")
    current_spell_slots = 0
    maximum_spell_slots = 0
    armour_class = calculate_armour_class(dex_modifier)
    print(f"Armour Class: {armour_class}")
    character_details_to_details = {
        "player_name": player_name,
        "character_name": character_name,
        "character_class": character_classes_to_selection[character_class],
        "character_level": character_level,
        "current_health": current_health,
        "maximum_health": maximum_health,
        "current_spell_slots": current_spell_slots,
        "maximum_spell_slots": maximum_spell_slots,
        "armour_class": armour_class,
        "ability_scores": assigned_scores,
    }
    return character_details_to_details

    # Here you would store the assigned scores appropriately


def get_valid_integer(prompt, min=None, max=None, error_message=""):
    """Gets a valid integer input from the user within optional min and max bounds."""
    is_valid_input = False
    while not is_valid_input:
        try:
            user_input = int(input(prompt))
            if min is not None and user_input < min:
                print(
                    error_message
                    if error_message
                    else f"\nNumber must be {min} or higher"
                )
            elif max is not None and user_input > max:
                print(
                    error_message
                    if error_message
                    else f"\nNumber must be {max} or lower"
                )
            else:
                is_valid_input = True
        except ValueError:
            print(f"Invalid {error_message if error_message else '(not an integer)'}")
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
        player_name = data[0]
        character_name = data[1]
        # fmt: off
        character_stats = data[2:9]  # class, level, current health, max health, current spell slots, max spell slots, armour
        character_ability_scores = data[9:]  # dexterity, constitution, charisma, wisdom, intelligence, strength
        data = (character_name, character_stats, character_ability_scores)  # Combine stats and ability scores as tuple
        player_name_to_character[player_name] = (data)  # Map player name to character data
        # fmt: on

    in_file.close()
    """--------------------  EXAMPLE DATA FORMAT  --------------------
    [0] player name, [1] character name, [2] class, [3] level, [4] current health, 
    [5] max health, [6] current spell slots, [7] max spell slots, [8] armour, 
    [9] dexterity, [10] constitution, [11] charisma, [12] wisdom, [13] intelligence, [14] strength"""

    return player_name_to_character


def write_to_file(player_name, character_data, filename):
    """Write the selected character data to a CSV file."""
    out_file = open(filename, "w")
    # fmt: off
    out_file.write("Player Name,Character Name,Class,Level,Current Health,Max Health,Current Spell Slots,Max Spell Slots,Armour,Dexterity,Constitution,Charisma,Wisdom,Intelligence,Strength\n")
    out_file.write(f"{player_name},{character_data[0]},{','.join(character_data[1])},{','.join(character_data[2])}\n")
    # fmt: on
    out_file.close()


def display_character_info(character_data):
    """Displays the character information in a readable format."""
    # fmt: off
    character_name, character_stats, character_ability_scores, character_spell_slots = format_character_info(character_data)
    print(f"\n{character_name}")
    print(f"{SMALL_INDENT}Stats: \n{character_stats}")
    print(f"{SMALL_INDENT}Abilities: \n{character_ability_scores}")
    print(f"{SMALL_INDENT}Spell Slots: \n{character_spell_slots}\n")
    # fmt: on


def format_character_info(character_data):
    """Formats character data for display."""
    # fmt: off
    character_name = f"{SUBMENU_LINE_SEPARATOR}\n{SMALL_INDENT}Name: {character_data[0]}\n{SUBMENU_LINE_SEPARATOR}"
    character_stats = f"\n{MEDIUM_INDENT}Class: {character_data[1][0]} \t Level: {character_data[1][1]} \n{MEDIUM_INDENT}HP: {character_data[1][2]}/{character_data[1][3]} \t\t AC: {character_data[1][6]}\n{SUBMENU_LINE_SEPARATOR}"
    ability_modifiers = [calculate_modifier(int(score)) for score in character_data[2]]
    ability_scores = f"\n{MEDIUM_INDENT}DEX: {character_data[2][0]} + {ability_modifiers[0]}\t CON: {character_data[2][1]} + {ability_modifiers[1]}\t CHA: {character_data[2][2]} + {ability_modifiers[2]} \n{MEDIUM_INDENT}WIS: {character_data[2][3]} + {ability_modifiers[3]}\t INT: {character_data[2][4]} + {ability_modifiers[4]}\t STR: {character_data[2][5]} + {ability_modifiers[5]}\n{SUBMENU_LINE_SEPARATOR}"
    spell_slots = f"\n{MEDIUM_INDENT}Level 1: {character_data[1][4]}/{character_data[1][5]}{LARGE_INDENT}Level 2: 0/0 \n{MEDIUM_INDENT}Level 3: 0/0{LARGE_INDENT}Level 4: 0/0 \n{MEDIUM_INDENT}Level 5: 0/0{LARGE_INDENT}Level 6: 0/0\n{SUBMENU_LINE_SEPARATOR} "
    # fmt: on
    return character_name, character_stats, ability_scores, spell_slots


def display_players(available_player_characters):
    """Displays the list of available players and their characters."""
    # fmt: off
    for i, (player, (character_name, character_stats, character_ability_scores),) in enumerate(available_player_characters.items()):
        print(f"{SMALL_INDENT}Player {i+1}: {player:10} Character: {character_name}")
    # fmt: on


def calculate_modifier(score):
    """Calculates the ability score modifier."""
    return (score - 10) // 2


def calculate_health(constitution_modifier, level):
    """Calculates the health of a character based on class and level."""
    return 10 + (constitution_modifier * 2) + (level * 5)

def calculate_armour_class(dexterity_modifier, base_ac=10):
    """Calculates the armour class of a character."""
    return base_ac + dexterity_modifier

if __name__ == "__main__":
    main()
