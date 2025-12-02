"""
COMP 163 - Project 3: Quest Chronicles
Game Data Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This module handles loading and validating game data from text files.
"""

import os
from custom_exceptions import (
    InvalidDataFormatError,
    MissingDataFileError,
    CorruptedDataError
)

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

def load_quests(filename="data/quests.txt"):
    """
    Load quest data from file
    
    Expected format per quest (separated by blank lines):
    QUEST_ID: unique_quest_name
    TITLE: Quest Display Title
    DESCRIPTION: Quest description text
    REWARD_XP: 100
    REWARD_GOLD: 50
    REQUIRED_LEVEL: 1
    PREREQUISITE: previous_quest_id (or NONE)
    
    Returns: Dictionary of quests {quest_id: quest_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    # TODO: Implement this function
    # Must handle:
    # - FileNotFoundError → raise MissingDataFileError
    # - Invalid format → raise InvalidDataFormatError
    # - Corrupted/unreadable data → raise CorruptedDataError
    required_keys = ["QUEST_ID", "TITLE", "DESCRIPTION", "REWARD_XP", "REWARD_GOLD", "REQUIRED_LEVEL", "PREREQUISITE"]
    all_quests = {}
    try:
        with open(filename, 'r') as file:
            file_content = file.read()
    except FileNotFoundError:
        raise MissingDataFileError(f"Quest file not found at: {filename}")
    except IOError as e:
        raise CorruptedDataError(f"Could not read quest file: {e}")
    quest_blocks = []
    raw_blocks = file_content.split('\n\n')
    for block in raw_blocks:
        clean_block = block.strip()
        if clean_block:
            quest_blocks.append(clean_block)

    for block in quest_blocks:
        quest_data = {}
        lines = block.split('\n')
        for line in lines:
            if ":" in line:
                try:
                    key, value_text = line.split(":", 1)
                    key = key.strip()
                    value = value_text.strip()
                    quest_data[key] = value
                except ValueError:
                    raise InvalidDataFormatError(f"Corrupted key-value line in quest block: {line}")
        if required_keys - set(quest_data.keys()):
            # Suggested by Google Gemini due to my code being flawed and stopping on the first missing key. This goes through and collects all of them.
            missing_keys = [key for key in required_keys if key not in quest_data]
            if missing_keys:
                    raise InvalidDataFormatError(f"Missing required keys in a quest block: {','.join(missing_keys)}")
        quest_id = quest_data['QUEST_ID']
        if quest_id in all_quests:
            raise InvalidDataFormatError(f"Duplicate quest id found: {quest_id}")
        try:
            quest_data['REWARD_XP'] = int(quest_data['REWARD_XP'])
            quest_data['REWARD_GOLD'] = int(quest_data['REWARD_GOLD'])
            quest_data['REQUIRED_LEVEL'] = int(quest_data['REQUIRED_LEVEL'])
        except ValueError:
            raise InvalidDataFormatError(f"Non-integer value found for XP, GOLD, or LEVEL in quest: {quest_id}")
        if quest_data['PREREQUISITE'].upper() == 'NONE':
            quest_data['PREREQUISITE'] = None
            # Google Gemini suggested for redundancy.
            del quest_data['QUEST_ID']
        all_quests[quest_id] = quest_data
    return all_quests

def load_items(filename="data/items.txt"):
    """
    Load item data from file
    
    Expected format per item (separated by blank lines):
    ITEM_ID: unique_item_name
    NAME: Item Display Name
    TYPE: weapon|armor|consumable
    EFFECT: stat_name:value (e.g., strength:5 or health:20)
    COST: 100
    DESCRIPTION: Item description
    
    Returns: Dictionary of items {item_id: item_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    # TODO: Implement this function
    # Must handle same exceptions as load_quests
    required_keys = ["ITEM_ID", "NAME", "TYPE", "EFFECT", "COST", "DESCRIPTION"]
    all_items = {}

    try:
        with open(filename, 'r') as file:
            file_content = file.read()
    except FileNotFoundError:
        raise MissingDataFileError(f"Item file not found at: {filename}")
    except IOError as e:
        raise CorruptedDataError(f"Could not read item file: {e}")
    item_blocks = []
    raw_blocks = file_content.split('\n\n')
    for block in raw_blocks:
        clean_block = block.strip()
        if clean_block:
            item_blocks.append(clean_block)
    for block in item_blocks:
        item_data = {}
        lines = block.split('\n')
        for line in lines:
            if ":" in line:
                try:
                    key, value_text = line.split(":", 1)
                    key = key.strip()
                    value = value_text.strip()
                    item_data[key] = value
                except ValueError:
                    raise InvalidDataFormatError(f"Corrupted key-value line in item block: {line}")
        missing_keys = [key for key in required_keys if key not in item_data]
        if missing_keys:
            raise InvalidDataFormatError(f"Missing required keys in an item block: {', '.join(missing_keys)}")
        item_id = item_data['ITEM_ID']
        if item_id in all_items:
            raise InvalidDataFormatError(f"Duplicate item ID found: {item_id}")
        
        try: 
            item_data['COST'] = int(item_data['COST'])
        except ValueError:
            raise InvalidDataFormatError(f"Non-integer value found for COST in item: {item_id}")
        effect_string = item_data['EFFECT']
        if ":" not in effect_string:
            raise InvalidDataFormatError(f"Invalid EFFECT format in item {item_id}. Must be 'stat:value'.")
        try:
            effect_stat, effect_value = effect_string.split(":", 1)
            item_data['EFFECT'] = {
                "stat": effect_stat.strip(),
                "value": int(effect_value.strip())
            }
        except ValueError:
            raise InvalidDataFormatError(f"Non-integer value found in EFFECT for item: {item_id}")
        del item_data['ITEM_ID']
        all_items[item_id] = item_data
    return all_items

def validate_quest_data(quest_dict):
    """
    Validate that quest dictionary has all required fields
    
    Required fields: quest_id, title, description, reward_xp, 
                    reward_gold, required_level, prerequisite
    
    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields
    """
    # TODO: Implement validation
    # Check that all required keys exist
    # Check that numeric values are actually numbers
    pass

def validate_item_data(item_dict):
    """
    Validate that item dictionary has all required fields
    
    Required fields: item_id, name, type, effect, cost, description
    Valid types: weapon, armor, consumable
    
    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields or invalid type
    """
    # TODO: Implement validation
    pass

def create_default_data_files():
    """
    Create default data files if they don't exist
    This helps with initial setup and testing
    """
    # TODO: Implement this function
    # Create data/ directory if it doesn't exist
    # Create default quests.txt and items.txt files
    # Handle any file permission errors appropriately
    pass

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_quest_block(lines):
    """
    Parse a block of lines into a quest dictionary
    
    Args:
        lines: List of strings representing one quest
    
    Returns: Dictionary with quest data
    Raises: InvalidDataFormatError if parsing fails
    """
    # TODO: Implement parsing logic
    # Split each line on ": " to get key-value pairs
    # Convert numeric strings to integers
    # Handle parsing errors gracefully
    pass

def parse_item_block(lines):
    """
    Parse a block of lines into an item dictionary
    
    Args:
        lines: List of strings representing one item
    
    Returns: Dictionary with item data
    Raises: InvalidDataFormatError if parsing fails
    """
    # TODO: Implement parsing logic
    pass

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== GAME DATA MODULE TEST ===")
    
    # Test creating default files
    # create_default_data_files()
    
    # Test loading quests
    # try:
    #     quests = load_quests()
    #     print(f"Loaded {len(quests)} quests")
    # except MissingDataFileError:
    #     print("Quest file not found")
    # except InvalidDataFormatError as e:
    #     print(f"Invalid quest format: {e}")
    
    # Test loading items
    # try:
    #     items = load_items()
    #     print(f"Loaded {len(items)} items")
    # except MissingDataFileError:
    #     print("Item file not found")
    # except InvalidDataFormatError as e:
    #     print(f"Invalid item format: {e}")

