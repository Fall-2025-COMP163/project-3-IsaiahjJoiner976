"""
COMP 163 - Project 3: Quest Chronicles
Combat System Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

Handles combat mechanics
"""
import random
from custom_exceptions import (
    InvalidTargetError,
    CombatNotActiveError,
    CharacterDeadError,
    AbilityOnCooldownError
)

# ============================================================================
# ENEMY DEFINITIONS
# ============================================================================

def create_enemy(enemy_type):
    """
    Create an enemy based on type
    
    Example enemy types and stats:
    - goblin: health=50, strength=8, magic=2, xp_reward=25, gold_reward=10
    - orc: health=80, strength=12, magic=5, xp_reward=50, gold_reward=25
    - dragon: health=200, strength=25, magic=15, xp_reward=200, gold_reward=100
    
    Returns: Enemy dictionary
    Raises: InvalidTargetError if enemy_type not recognized
    """
    # TODO: Implement enemy creation
    # Return dictionary with: name, health, max_health, strength, magic, xp_reward, gold_reward
    enemy_stats = {
        "Goblin": {"name": "Goblin", "health": 50, "max_health": 50, "strength": 8, "magic": 2, "xp_reward": 25, "gold_reward": 10},
        "Orc":    {"name": "Orc", "health": 80, "max_health": 80,  "strength": 12,  "magic": 5, "xp_reward": 50, "gold_reward": 25},
        "Dragon":   {"name": "Dragon", "health": 200, "max_health": 200,  "strength": 25, "magic": 15, "xp_reward": 200, "gold_reward": 100}
    }
    if enemy_type not in enemy_stats:
        raise InvalidTargetError(f"ERROR: Invalid {enemy_type} enemy type.")
    base_stats = enemy_stats[enemy_type]
    return base_stats

def get_random_enemy_for_level(character_level):
    """
    Get an appropriate enemy for character's level
    
    Level 1-2: Goblins
    Level 3-5: Orcs
    Level 6+: Dragons
    
    Returns: Enemy dictionary
    """
    # TODO: Implement level-appropriate enemy selection
    # Use if/elif/else to select enemy type
    # Call create_enemy with appropriate type
    if character_level <= 2:
        return create_enemy("Goblin")
    elif character_level <= 5: 
        return create_enemy("Orc")
    else:
        return create_enemy("Dragon")

# ============================================================================
# COMBAT SYSTEM
# ============================================================================

class SimpleBattle:
    """
    Simple turn-based combat system
    
    Manages combat between character and enemy
    """
    
    def __init__(self, character, enemy):
        """Initialize battle with character and enemy"""
        # TODO: Implement initialization
        # Store character and enemy
        # Set combat_active flag
        # Initialize turn counter
        self.character = character
        self.enemy = enemy
        self.combat_active = True
        self.turn_count = 0
        pass
    
    def start_battle(self):
        """
        Start the combat loop
        
        Returns: Dictionary with battle results:
                {'winner': 'player'|'enemy', 'xp_gained': int, 'gold_gained': int}
        
        Raises: CharacterDeadError if character is already dead
        """
        # TODO: Implement battle loop
        # Check character isn't dead
        # Loop until someone dies
        # Award XP and gold if player wins
        if self.character['health'] <= 0:
            raise CharacterDeadError(f"ERROR: Character is already dead.")
        while self.combat_active:
            self.turn_count += 1
            self.player_turn()
            if self.enemy['health'] <= 0:
                self.combat_active = False
                break
            self.enemy_turn()
            if self.character['health'] <= 0:
                self.combat_active = False
                break
        if self.character['health'] > 0:
            winner = "player"
            xp_gained = self.enemy["xp_reward"]
            gold_gained = self.enemy["gold_reward"]
            self.character.gain_experience(self.character, xp_gained)
            self.character.add_gold(self.character, gold_gained)
        else:
            winner = "enemy"
            xp_gained = 0
            gold_gained = 0

        return {
            "winner": winner,
            "xp_gained": xp_gained,
            "gold_gained": gold_gained
        }
    
    def player_turn(self):
        """
        Handle player's turn
        
        Displays options:
        1. Basic Attack
        2. Special Ability (if available)
        3. Try to Run
        
        Raises: CombatNotActiveError if called outside of battle
        """
        # TODO: Implement player turn
        # Check combat is active
        # Display options
        # Get player choice
        # Execute chosen action
        if self.combat_active == False:
            raise CombatNotActiveError(f"ERROR: {self.character['name']} is not in combat.")
        print("\n--- It's your turn! ---")
        is_special_ready = self.turn_count % 2 == 0 and self.turn_count > 0
        print(f"What will {self.character['name']} do?")
        print("1. Basic Attack")
        if is_special_ready:
            print("2. Special Ability")
        print("3. Try to Run")

        valid_choices = ['1', '3']
        if is_special_ready:
            valid_choices.append('2')
        choice = None
        while choice not in valid_choices:
            choice = input("Enter your choice: ").strip()
            if choice not in valid_choices:
                print(f"Invalid choice. Choose one of the options: {', '.join(valid_choices)}")
        if choice == '1':
            print(f"{self.character['name']} attacks!")
            damage = self.calculate_damage(self.character, self.enemy)
            self.apply_damage(self.enemy, damage)
        elif choice == '2':
            action, value, description = use_special_ability(self.character, self.enemy)
            if action == "damage":
                self.apply_damage(self.enemy, value)
                print(description)
            elif action == "healed":
                self.character['health'] = value
                print(description)
            else:
                print(f"Error: Unknown special ability result: {action}")
        elif choice == '3':
            escaped = self.attempt_escape()
            if escaped:
                print(f"{self.character['name']} successfully escaped the battle!")
            else:
                print(f"{self.character['name']} failed to escape the battle!")
        pass
    
    def enemy_turn(self):
        """
        Handle enemy's turn - simple AI
        
        Enemy always attacks
        
        Raises: CombatNotActiveError if called outside of battle
        """
        # TODO: Implement enemy turn
        # Check combat is active
        # Calculate damage
        # Apply to character
        if self.combat_active == False:
            raise CombatNotActiveError(f"ERROR: {self.character['name']} is not in combat.")
            
        print(f"\n--- {self.enemy['name']}'s Turn ---")
        
        damage = self.calculate_damage(self.enemy, self.character)
        self.apply_damage(self.character, damage)
        pass
    
    def calculate_damage(self, attacker, defender):
        """
        Calculate damage from attack
        
        Damage formula: attacker['strength'] - (defender['strength'] // 4)
        Minimum damage: 1
        
        Returns: Integer damage amount
        """
        # TODO: Implement damage calculation
        base_damage = attacker['strength'] - (defender['strength'] // 4)
        if base_damage < 1:
            damage = 1
        else:
            damage = base_damage
        return damage
        
    
    def apply_damage(self, target, damage):
        """
        Apply damage to a character or enemy
        
        Reduces health, prevents negative health
        """
        # TODO: Implement damage application
        print(f"{target['name']} takes {damage} damage!")
        current_health = target['health']
        new_health = current_health - damage
        if new_health < 0:
            target['health'] = 0
        else:
            target['health'] = new_health

        if target['health'] == 0:
            print(f"{target['name']} has been defeated!")
    
    def check_battle_end(self):
        """
        Check if battle is over
        
        Returns: 'player' if enemy dead, 'enemy' if character dead, None if ongoing
        """
        # TODO: Implement battle end check
        if self.enemy['health'] <= 0:
            self.combat_active = False
            return 'player'
        if self.character['health'] <= 0:
            self.combat_active = False
            return 'enemy'
        return None
    
    def attempt_escape(self):
        """
        Try to escape from battle
        
        50% success chance
        
        Returns: True if escaped, False if failed
        """
        # TODO: Implement escape attempt
        # Use random number or simple calculation
        # If successful, set combat_active to False
        if random.random() < 0.5:
            self.combat_active = False
            return True
        else: 
            return False
        pass

# ============================================================================
# SPECIAL ABILITIES
# ============================================================================

def use_special_ability(character, enemy):
    """
    Use character's class-specific special ability
    
    Example abilities by class:
    - Warrior: Power Strike (2x strength damage)
    - Mage: Fireball (2x magic damage)
    - Rogue: Critical Strike (3x strength damage, 50% chance)
    - Cleric: Heal (restore 30 health)
    
    Returns: String describing what happened
    Raises: AbilityOnCooldownError if ability was used recently
    """
    # TODO: Implement special abilities
    # Check character class
    # Execute appropriate ability
    # Track cooldowns (optional advanced feature)
    class_type = character['class'].lower()
    abilities = {
        "warrior": warrior_power_strike,
        "mage": mage_fireball,
        "rogue": rogue_critical_strike,
        "cleric": cleric_heal
    }
    if class_type in abilities:
        ability = abilities[class_type]
        if class_type == "cleric":
            final_health = ability(character)
            description = f"{character['name']} heals themselves for 30 health! Current health: {final_health}/{character['max_health']}"
            return "healed", final_health, description
        else:
            damage = ability(character, enemy)
            description = f"{character['name']} used a special attack dealing {damage} damage!"
            return "damage", damage, description
    return "unknown", 0, "Error: Could not find special ability for this class."
    

def warrior_power_strike(character, enemy):
    """Warrior special ability"""
    # TODO: Implement power strike
    # Double strength damage
    print(f"{character['name']} performs a Power Strike!")
    damage = 2 * character['strength']
    return damage

def mage_fireball(character, enemy):
    """Mage special ability"""
    # TODO: Implement fireball
    # Double magic damage
    print(f"{character['name']} casts Fireball!")
    damage = 2 * character['magic']
    return damage

def rogue_critical_strike(character, enemy):
    """Rogue special ability"""
    # TODO: Implement critical strike
    # 50% chance for triple damage
    print(f"You attempt a Critical Strike...")
    if random.random() < 0.5:
        print(f"Critical Strike hits!")
        damage = 3 * character['strength']
        return damage
    else:
        return damage

def cleric_heal(character):
    """Cleric special ability"""
    # TODO: Implement healing
    # Restore 30 HP (not exceeding max_health)
    amount = 30
    original_health = character["health"]
    max_health = character["max_health"]
    potential_health = original_health + amount
    if potential_health > max_health:
        final_health = max_health
    else:
        final_health = potential_health
    character["health"] = final_health    
    return final_health
    

# ============================================================================
# COMBAT UTILITIES
# ============================================================================

def can_character_fight(character):
    """
    Check if character is in condition to fight
    
    Returns: True if health > 0 and not in battle
    """
    # TODO: Implement fight check
    pass

def get_victory_rewards(enemy):
    """
    Calculate rewards for defeating enemy
    
    Returns: Dictionary with 'xp' and 'gold'
    """
    # TODO: Implement reward calculation
    pass

def display_combat_stats(character, enemy):
    """
    Display current combat status
    
    Shows both character and enemy health/stats
    """
    # TODO: Implement status display
    print(f"\n{character['name']}: HP={character['health']}/{character['max_health']}")
    print(f"{enemy['name']}: HP={enemy['health']}/{enemy['max_health']}")
    pass

def display_battle_log(message):
    """
    Display a formatted battle message
    """
    # TODO: Implement battle log display
    print(f">>> {message}")
    pass

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== COMBAT SYSTEM TEST ===")
    
    # Test enemy creation
    # try:
    #     goblin = create_enemy("goblin")
    #     print(f"Created {goblin['name']}")
    # except InvalidTargetError as e:
    #     print(f"Invalid enemy: {e}")
    
    # Test battle
    # test_char = {
    #     'name': 'Hero',
    #     'class': 'Warrior',
    #     'health': 120,
    #     'max_health': 120,
    #     'strength': 15,
    #     'magic': 5
    # }
    #
    # battle = SimpleBattle(test_char, goblin)
    # try:
    #     result = battle.start_battle()
    #     print(f"Battle result: {result}")
    # except CharacterDeadError:
    #     print("Character is dead!")

