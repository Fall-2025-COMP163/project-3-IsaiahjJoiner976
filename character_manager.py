"""
COMP 163 - Project 3: Quest Chronicles
Character Manager Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This module handles character creation, loading, and saving.
"""

import os
from custom_exceptions import (
    InvalidCharacterClassError,
    CharacterNotFoundError,
    SaveFileCorruptedError,
    InvalidSaveDataError,
    CharacterDeadError
)

# ============================================================================
# CHARACTER MANAGEMENT FUNCTIONS
# ============================================================================

def create_character(name, character_class):
    """
    Create a new character with stats based on class
    
    Valid classes: Warrior, Mage, Rogue, Cleric
    
    Returns: Dictionary with character data including:
            - name, class, level, health, max_health, strength, magic
            - experience, gold, inventory, active_quests, completed_quests
    
    Raises: InvalidCharacterClassError if class is not valid
    """
    # TODO: Implement character creation
    # Validate character_class first
    # Example base stats:
    # Warrior: health=120, strength=15, magic=5
    # Mage: health=80, strength=8, magic=20
    # Rogue: health=90, strength=12, magic=10
    # Cleric: health=100, strength=10, magic=15
    
    # All characters start with:
    # - level=1, experience=0, gold=100
    # - inventory=[], active_quests=[], completed_quests=[]
    
    # Raise InvalidCharacterClassError if class not in valid list
    char_stats = {"name": name, "class": character_class, "level": 1, "experience": 0}
    CLASS_STATS = {
        "Warrior": {"health": 120, "strength": 15, "magic": 5},
        "Mage":    {"health": 80,  "strength": 8,  "magic": 20},
        "Rogue":   {"health": 90,  "strength": 12, "magic": 10},
        "Cleric":  {"health": 100, "strength": 10, "magic": 15},
    }
    if character_class not in CLASS_STATS:
        raise InvalidCharacterClassError(f"ERROR: Invalid {character_class} Class")
    base_stats = CLASS_STATS[character_class]
    char_stats.update(base_stats)
    char_stats["max_health"] = char_stats["health"]
    char_stats["gold"] = 100
    char_stats["inventory"] = []
    char_stats["active_quests"] = []
    char_stats["completed_quests"] = []
    return char_stats

def save_character(character, save_directory="data/save_games"):
    """
    Save character to file
    
    Filename format: {character_name}_save.txt
    
    File format:
    NAME: character_name
    CLASS: class_name
    LEVEL: 1
    HEALTH: 120
    MAX_HEALTH: 120
    STRENGTH: 15
    MAGIC: 5
    EXPERIENCE: 0
    GOLD: 100
    INVENTORY: item1,item2,item3
    ACTIVE_QUESTS: quest1,quest2
    COMPLETED_QUESTS: quest1,quest2
    
    Returns: True if successful
    Raises: PermissionError, IOError (let them propagate or handle)
    """
    # TODO: Implement save functionality
    # Create save_directory if it doesn't exist
    # Handle any file I/O errors appropriately
    # Lists should be saved as comma-separated values
    char_name = character["name"]
    file_name = f"{character_name.lower().replace(" ", "_")}_save.txt"
    full_path = os.path.join(save_directory, file_name)

    try:
        os.makedirs(save_directory, exist_ok=True)
    except PermissionError:
        raise PermissionError(f"Permission denied while attempting to create directory: {save_directory}")
    order = ["name", "class", "level", "health", "max_health", "strength", "magic", "experience", "gold", "inventory", "active_quests", "completed_quests"]
    output_lines = []
    for key in order:
        try:
            value = character[key]
        except KeyError as e:
            raise KeyError(f"Character data is missing the required key {e}. Cannot save.")
        if isinstance(value, list):
            string_list = [str(item) for item in value]
            value_str = ",".join(string_list)
        else:
            value_str = str(value)
        output_lines.append(f"{key.upper()}:{value_str}")
    try:
        with open(full_path, 'w') as file:
            file.write('\n'.join(output_lines))
    except IOError as e:
        raise IOError(f"Error writing save file to {full_path}: {e}")
    return True

def load_character(character_name, save_directory="data/save_games"):
    """
    Load character from save file
    
    Args:
        character_name: Name of character to load
        save_directory: Directory containing save files
    
    Returns: Character dictionary
    Raises: 
        CharacterNotFoundError if save file doesn't exist
        SaveFileCorruptedError if file exists but can't be read
        InvalidSaveDataError if data format is wrong
    """
    # TODO: Implement load functionality
    # Check if file exists → CharacterNotFoundError
    # Try to read file → SaveFileCorruptedError
    # Validate data format → InvalidSaveDataError
    # Parse comma-separated lists back into Python lists
    LIST_KEYS = {"INVENTORY", "ACTIVE_QUESTS", "COMPLETED_QUESTS"}
    INT_KEYS = {"LEVEL", "HEALTH", "MAX_HEALTH", "STRENGTH", "MAGIC", "EXPERIENCE", "GOLD"}
    file_name = f"{character_name.lower().replace(" ", "_")}_save.txt"
    full_path = os.path.join(save_directory, file_name)
    
    if not os.path.exists(full_path):
        raise CharacterNotFoundError(f"No save file found for character: {character_name}")

    try:
        with open(full_path, 'r') as file:
            lines = file.readlines()
    except IOError as e:
        raise SaveFileCorruptedError(f"Error reading save file for {character_name}: {e}")
        
    char_data = {}
    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        if not line:
            continue
        try:
            key_upper, value_str = line.split(':', 1)
            key = key_upper.lower()
            value_str = value_str.strip()
        except ValueError:
            raise InvalidSaveDataError(f"Corrupted format in save file line {line_num}: {line}")
        try:
            if key_upper in LIST_KEYS:
                if value_str:
                    value = value_str.split(',')
                else:
                    value = []
            elif key_upper in INT_KEYS:
                value = int(value_str)
            else:
                value = value_str
        except ValueError:
            raise InvalidSaveDataError(f"Data type error for key '{key_upper}' in save file. Expected integer, got: '{value_str}'")
        char_data[key] = value

    needed_keys = ["name", "class", "health", "max_health"]
    if not all(key in char_data for key in needed_keys):
        raise InvalidSaveDataError(f"Missing essential data keys in file for {character_name}.")

    return char_data
    pass

def list_saved_characters(save_directory="data/save_games"):
    """
    Get list of all saved character names
    
    Returns: List of character names (without _save.txt extension)
    """
    # TODO: Implement this function
    # Return empty list if directory doesn't exist
    # Extract character names from filenames
    if not os.path.exists(save_directory):
        return []

    try:
        filenames = os.listdir(save_directory)
    except Exception:
        return []
    character_names = []
    for file_name in file_names:
        if filename.endswith("_save.txt"):
            underscore_names = fil_ename[:-9]
            space_names = underscore_names.replace("_", " ")
            character_names.append(space_names.title())
    return character_names

def delete_character(character_name, save_directory="data/save_games"):
    """
    Delete a character's save file
    
    Returns: True if deleted successfully
    Raises: CharacterNotFoundError if character doesn't exist
    """
    # TODO: Implement character deletion
    # Verify file exists before attempting deletion
    file_name = f"{character_name.lower().replace(" ", "_")}_save.txt"
    full_path = os.path.join(save_directory, file_name)
    if not os.path.exists(full_path):
        raise CharacterNotFoundError(f"Character save file not found for: {character_name}")
    try:
        os.remove(full_path)
    except OSError as e:
        raise OSError(f"Could not delete file at {full_path}. Details: {e}")
    return True

# ============================================================================
# CHARACTER OPERATIONS
# ============================================================================

def gain_experience(character, xp_amount):
    """
    Add experience to character and handle level ups
    
    Level up formula: level_up_xp = current_level * 100
    Example when leveling up:
    - Increase level by 1
    - Increase max_health by 10
    - Increase strength by 2
    - Increase magic by 2
    - Restore health to max_health
    
    Raises: CharacterDeadError if character health is 0
    """
    # TODO: Implement experience gain and leveling
    # Check if character is dead first
    # Add experience
    # Check for level up (can level up multiple times)
    # Update stats on level up
    if character["health"] <= 0:
        raise CharacterDeadError(f"{character["name"]} is dead and cannot gain experience.")
    character["experience"] += xp_amount
    while True:
        current_level = character["level"]
        level_up_xp = current_level * 100
        if character["experience"] < level_up_xp:
            break
        character["level"] += 1
        character["max_health"] += 10
        character["strength"] += 2
        character["magic"] += 2
        character["health"] == character["max_health"]
        print(f"{character["name"]} has reached level {character["level"]}!")
    return character

def add_gold(character, amount):
    """
    Add gold to character's inventory
    
    Args:
        character: Character dictionary
        amount: Amount of gold to add (can be negative for spending)
    
    Returns: New gold total
    Raises: ValueError if result would be negative
    """
    # TODO: Implement gold management
    # Check that result won't be negative
    # Update character's gold
    pass

def heal_character(character, amount):
    """
    Heal character by specified amount
    
    Health cannot exceed max_health
    
    Returns: Actual amount healed
    """
    # TODO: Implement healing
    # Calculate actual healing (don't exceed max_health)
    # Update character health
    pass

def is_character_dead(character):
    """
    Check if character's health is 0 or below
    
    Returns: True if dead, False if alive
    """
    # TODO: Implement death check
    pass

def revive_character(character):
    """
    Revive a dead character with 50% health
    
    Returns: True if revived
    """
    # TODO: Implement revival
    # Restore health to half of max_health
    pass

# ============================================================================
# VALIDATION
# ============================================================================

def validate_character_data(character):
    """
    Validate that character dictionary has all required fields
    
    Required fields: name, class, level, health, max_health, 
                    strength, magic, experience, gold, inventory,
                    active_quests, completed_quests
    
    Returns: True if valid
    Raises: InvalidSaveDataError if missing fields or invalid types
    """
    # TODO: Implement validation
    # Check all required keys exist
    # Check that numeric values are numbers
    # Check that lists are actually lists
    pass

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== CHARACTER MANAGER TEST ===")
    
    # Test character creation
    # try:
    #     char = create_character("TestHero", "Warrior")
    #     print(f"Created: {char['name']} the {char['class']}")
    #     print(f"Stats: HP={char['health']}, STR={char['strength']}, MAG={char['magic']}")
    # except InvalidCharacterClassError as e:
    #     print(f"Invalid class: {e}")
    
    # Test saving
    # try:
    #     save_character(char)
    #     print("Character saved successfully")
    # except Exception as e:
    #     print(f"Save error: {e}")
    
    # Test loading
    # try:
    #     loaded = load_character("TestHero")
    #     print(f"Loaded: {loaded['name']}")
    # except CharacterNotFoundError:
    #     print("Character not found")
    # except SaveFileCorruptedError:
    #     print("Save file corrupted")

