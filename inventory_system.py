"""
COMP 163 - Project 3: Quest Chronicles
Inventory System Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This module handles inventory management, item usage, and equipment.
"""

from custom_exceptions import (
    InventoryFullError,
    ItemNotFoundError,
    InsufficientResourcesError,
    InvalidItemTypeError
)

# Maximum inventory size
MAX_INVENTORY_SIZE = 20

# ============================================================================
# INVENTORY MANAGEMENT
# ============================================================================

def add_item_to_inventory(character, item_id):
    """
    Add an item to character's inventory
    
    Args:
        character: Character dictionary
        item_id: Unique item identifier
    
    Returns: True if added successfully
    Raises: InventoryFullError if inventory is at max capacity
    """
    # TODO: Implement adding items
    # Check if inventory is full (>= MAX_INVENTORY_SIZE)
    # Add item_id to character['inventory'] list
    if len(character['inventory']) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError(f"Your inventory is full (Max: {MAX_INVENTORY_SIZE}).")
    
    character['inventory'].append(item_id)
    return True

def remove_item_from_inventory(character, item_id):
    """
    Remove an item from character's inventory
    
    Args:
        character: Character dictionary
        item_id: Item to remove
    
    Returns: True if removed successfully
    Raises: ItemNotFoundError if item not in inventory
    """
    # TODO: Implement item removal
    # Check if item exists in inventory
    # Remove item from list
    if item_id in character['inventory']:
        character['inventory'].remove(item_id)
        return True
    else:
        raise ItemNotFoundError(f"{item_id} not found in your inventory")

def has_item(character, item_id):
    """
    Check if character has a specific item
    
    Returns: True if item in inventory, False otherwise
    """
    # TODO: Implement item check
    inventory = character['inventory']
    return item_id in inventory

def count_item(character, item_id):
    """
    Count how many of a specific item the character has
    
    Returns: Integer count of item
    """
    # TODO: Implement item counting
    # Use list.count() method
    inventory = character['inventory']
    return inventory.count(item_id)

def get_inventory_space_remaining(character):
    """
    Calculate how many more items can fit in inventory
    
    Returns: Integer representing available slots
    """
    # TODO: Implement space calculation
    inventory = len(character['inventory'])
    space = MAX_INVENTORY_SIZE - inventory
    return space

def clear_inventory(character):
    """
    Remove all items from inventory
    
    Returns: List of removed items
    """
    # TODO: Implement inventory clearing
    # Save current inventory before clearing
    # Clear character's inventory list
    current_inv = character['inventory']
    removed_inv = list(current_inv)
    current_inv.clear()
    return removed_inv

# ============================================================================
# ITEM USAGE
# ============================================================================

def use_item(character, item_id, item_data):
    """
    Use a consumable item from inventory
    
    Args:
        character: Character dictionary
        item_id: Item to use
        item_data: Item information dictionary from game_data
    
    Item types and effects:
    - consumable: Apply effect and remove from inventory
    - weapon/armor: Cannot be "used", only equipped
    
    Returns: String describing what happened
    Raises: 
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'consumable'
    """
    # TODO: Implement item usage
    # Check if character has the item
    # Check if item type is 'consumable'
    # Parse effect (format: "stat_name:value" e.g., "health:20")
    # Apply effect to character
    # Remove item from inventory
    if item_id not in character['inventory']:
        raise ItemNotFoundError(f"{character['name']} does not have that item!")
    if item_data['TYPE'] != 'consumable':
        raise InvalidItemTypeError(f"That item cannot be consumed!")
    effect = item_data['EFFECT']
    stat_name = effect['stat']
    stat_value = effect['value']
    if stat_name in character:
        if isinstance(character[stat_name], (int, float)):
            character[stat_name] += stat_value
    remove_item_from_inventory(character, item_id)
    return f"{character['name']} gained {stat_value} {stat_name}"

def equip_weapon(character, item_id, item_data):
    """
    Equip a weapon
    
    Args:
        character: Character dictionary
        item_id: Weapon to equip
        item_data: Item information dictionary
    
    Weapon effect format: "strength:5" (adds 5 to strength)
    
    If character already has weapon equipped:
    - Unequip current weapon (remove bonus)
    - Add old weapon back to inventory
    
    Returns: String describing equipment change
    Raises:
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'weapon'
    """
    # TODO: Implement weapon equipping
    # Check item exists and is type 'weapon'
    # Handle unequipping current weapon if exists
    # Parse effect and apply to character stats
    # Store equipped_weapon in character dictionary
    # Remove item from inventory
    if item_id not in character['inventory']:
        raise ItemNotFoundError(f"{item_id} not found in {character['name']}'s inventory.")
    slot_key = 'weapon'
    item_type = item_data['TYPE'].lower()
    if item_type != slot_key:
        raise InvalidItemTypeError(f"'{item_data['NAME']}' is a '{item_type}' not a '{slot_key}'")
    
    effect = item_data['EFFECT']
    stat_name = effect['stat']
    stat_value = effect['value']
    old_weapon = None
    try: 
        old_weapon = character['equipped']['weapon']
    except KeyError:
        pass
    unequip_message = ""
    if old_weapon:
        old_stat_name = stat_name
        old_stat_value = 0
        bonus_key = f'{slot_key}_bonus'
        try:
            equipped_data = character['equipped']
            old_stat_value = equipped_data[bonus_key]
        except KeyError:
            pass
        if old_stat_value != 0 and old_stat_name in character:
            character[old_stat_name] -= old_stat_value
            unequip_message = f"Unequipped {old_weapon}, removing {old_stat_value} {old_stat_name}."
        add_item_to_inventory(character, old_weapon)
    
    if stat_name in character:
        character[stat_name] += stat_value
    if 'equipped' not in character:
        character['equipped'] = {}
    character['equipped'][slot_key] = item_id
    character['equipped'][f'{slot_key}_bonus'] = stat_value
    remove_item_from_inventory(character, item_id)
    equip_message = f"Equipped {item_data['NAME']}, granting {stat_value} {stat_name}."
    # Suggested by Google Gemini. Returns both messages or just equip message
    return unequip_message + (" " if unequip_message else "") + equip_message

def equip_armor(character, item_id, item_data):
    """
    Equip armor
    
    Args:
        character: Character dictionary
        item_id: Armor to equip
        item_data: Item information dictionary
    
    Armor effect format: "max_health:10" (adds 10 to max_health)
    
    If character already has armor equipped:
    - Unequip current armor (remove bonus)
    - Add old armor back to inventory
    
    Returns: String describing equipment change
    Raises:
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'armor'
    """
    # TODO: Implement armor equipping
    # Similar to equip_weapon but for armor
    if item_id not in character['inventory']:
        raise ItemNotFoundError(f"{item_id} not found in {character['name']}'s inventory.")
    slot_key = 'armor'
    item_type = item_data['TYPE'].lower()
    if item_type != slot_key:
        raise InvalidItemTypeError(f"'{item_data['NAME']}' is a '{item_type}' not a '{slot_key}'")
    
    effect = item_data['EFFECT']
    stat_name = effect['stat']
    stat_value = effect['value']
    old_armor = None
    try: 
        old_armor = character['equipped']['armor']
    except KeyError:
        pass
    unequip_message = ""
    if old_armor:
        old_stat_name = stat_name
        old_stat_value = 0
        bonus_key = f'{slot_key}_bonus'
        try:
            equipped_data = character['equipped']
            old_stat_value = equipped_data[bonus_key]
        except KeyError:
            pass
        if old_stat_value != 0 and old_stat_name in character:
            character[old_stat_name] -= old_stat_value
            unequip_message = f"Unequipped {old_armor}, removing {old_stat_value} {old_stat_name}."
        add_item_to_inventory(character, old_armor)
    
    if stat_name in character:
        character[stat_name] += stat_value
    if 'equipped' not in character:
        character['equipped'] = {}
    character['equipped'][slot_key] = item_id
    character['equipped'][f'{slot_key}_bonus'] = stat_value
    remove_item_from_inventory(character, item_id)
    equip_message = f"Equipped {item_data['NAME']}, granting {stat_value} {stat_name}."
    # Suggested by Google Gemini. Returns both messages or just equip message
    return unequip_message + (" " if unequip_message else "") + equip_message

def unequip_weapon(character):
    """
    Remove equipped weapon and return it to inventory
    
    Returns: Item ID that was unequipped, or None if no weapon equipped
    Raises: InventoryFullError if inventory is full
    """
    # TODO: Implement weapon unequipping
    # Check if weapon is equipped
    # Remove stat bonuses
    # Add weapon back to inventory
    # Clear equipped_weapon from character
    slot_key = 'weapon'
    unequipped = None
    old_stat_value = 0
    try:
        unequipped = character['equipped'][slot_key]
    except KeyError:
        return None
    stat_name = 'strength'
    try:
        bonus_key = f'{slot_key}_bonus'
        old_stat_value = character['equipped'][bonus_key]
    except KeyError:
        pass
    if old_stat_value != 0:
        try:
            character[stat_name] -= old_stat_value
        except KeyError:
            pass
    if character['inventory'] >= MAX_INVENTORY_SIZE:
        raise InventoryFullError(f"Your inventory is full (Max: {MAX_INVENTORY_SIZE}).")
    else:
        add_item_to_inventory(character, unequipped)
    try:
        character['equipped'][slot_key] = None
        character['equipped'][f'{slot_key}_bonus'] = 0
    except KeyError:
        pass
    return unequipped

def unequip_armor(character):
    """
    Remove equipped armor and return it to inventory
    
    Returns: Item ID that was unequipped, or None if no armor equipped
    Raises: InventoryFullError if inventory is full
    """
    # TODO: Implement armor unequipping
    slot_key = 'armor'
    unequipped = None
    old_stat_value = 0
    stat_name = 'max_health'
    try:
        unequipped = character['equipped'][slot_key]
    except KeyError:
        return None
    try:
        bonus_key = f'{slot_key}_bonus'
        old_stat_value = character['equipped'][bonus_key]
    except KeyError:
        pass
    if old_stat_value != 0:
        try:
            character[stat_name] -= old_stat_value
        except KeyError:
            pass
    if character['inventory'] >= MAX_INVENTORY_SIZE:
        raise InventoryFullError(f"Your inventory is full (Max: {MAX_INVENTORY_SIZE}).")
    else:
        add_item_to_inventory(character, unequipped)
    try:
        character['equipped'][slot_key] = None
        character['equipped'][f'{slot_key}_bonus'] = 0
    except KeyError:
        pass
    return unequipped
    pass

# ============================================================================
# SHOP SYSTEM
# ============================================================================

def purchase_item(character, item_id, item_data):
    """
    Purchase an item from a shop
    
    Args:
        character: Character dictionary
        item_id: Item to purchase
        item_data: Item information with 'cost' field
    
    Returns: True if purchased successfully
    Raises:
        InsufficientResourcesError if not enough gold
        InventoryFullError if inventory is full
    """
    # TODO: Implement purchasing
    # Check if character has enough gold
    # Check if inventory has space
    # Subtract gold from character
    # Add item to inventory
    cost = item_data['COST']
    try:
        current_gold = character['gold']
    except KeyError:
        current_gold = 0
    if current_gold < cost:
        raise InsufficientResourcesError(f"Not enough gold to buy that item. Required: {cost}, Have: {current_gold}")
    if character['inventory'] >= MAX_INVENTORY_SIZE:
        raise InventoryFullError(f"Your inventory is full (Max: {MAX_INVENTORY_SIZE}).")
    else:
        add_item_to_inventory(character, item_id)
    try:
        character['gold'] -= cost
    except KeyError:
        character['gold'] = 0 - cost
    return True

def sell_item(character, item_id, item_data):
    """
    Sell an item for half its purchase cost
    
    Args:
        character: Character dictionary
        item_id: Item to sell
        item_data: Item information with 'cost' field
    
    Returns: Amount of gold received
    Raises: ItemNotFoundError if item not in inventory
    """
    # TODO: Implement selling
    # Check if character has item
    # Calculate sell price (cost // 2)
    # Remove item from inventory
    # Add gold to character
    if not has_item(character, item_id):
        raise ItemNotFoundError(f"That item is not in inventory to sell.")
    cost = item_data['COST']
    sell_price = cost // 2
    remove_item_from_inventory(character, item_id)
    try:
        current_gold = character['gold']
        character['gold'] = current_gold + sell_price
    except KeyError:
        character['gold'] = sell_price
    return sell_price

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_item_effect(effect_string):
    """
    Parse item effect string into stat name and value
    
    Args:
        effect_string: String in format "stat_name:value"
    
    Returns: Tuple of (stat_name, value)
    Example: "health:20" → ("health", 20)
    """
    # TODO: Implement effect parsing
    # Split on ":"
    # Convert value to integer
    pass

def apply_stat_effect(character, stat_name, value):
    """
    Apply a stat modification to character
    
    Valid stats: health, max_health, strength, magic
    
    Note: health cannot exceed max_health
    """
    # TODO: Implement stat application
    # Add value to character[stat_name]
    # If stat is health, ensure it doesn't exceed max_health
    pass

def display_inventory(character, item_data_dict):
    """
    Display character's inventory in formatted way
    
    Args:
        character: Character dictionary
        item_data_dict: Dictionary of all item data
    
    Shows item names, types, and quantities
    """
    # TODO: Implement inventory display
    # Count items (some may appear multiple times)
    # Display with item names from item_data_dict
    pass

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== INVENTORY SYSTEM TEST ===")
    
    # Test adding items
    # test_char = {'inventory': [], 'gold': 100, 'health': 80, 'max_health': 80}
    # 
    # try:
    #     add_item_to_inventory(test_char, "health_potion")
    #     print(f"Inventory: {test_char['inventory']}")
    # except InventoryFullError:
    #     print("Inventory is full!")
    
    # Test using items
    # test_item = {
    #     'item_id': 'health_potion',
    #     'type': 'consumable',
    #     'effect': 'health:20'
    # }
    # 
    # try:
    #     result = use_item(test_char, "health_potion", test_item)
    #     print(result)
    # except ItemNotFoundError:
    #     print("Item not found")

