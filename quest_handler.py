"""
COMP 163 - Project 3: Quest Chronicles
Quest Handler Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This module handles quest management, dependencies, and completion.
"""
from character_manager import (
    gain_experience,
    add_gold
)
from custom_exceptions import (
    QuestNotFoundError,
    QuestRequirementsNotMetError,
    QuestAlreadyCompletedError,
    QuestNotActiveError,
    InsufficientLevelError
)

# ============================================================================
# QUEST MANAGEMENT
# ============================================================================
# Gemini suggests the use .get() to gain attributes without causing KeyErrors rather than directly taking from the character dictionaries
def accept_quest(character, quest_id, quest_data_dict):
    """
    Accept a new quest
    
    Args:
        character: Character dictionary
        quest_id: Quest to accept
        quest_data_dict: Dictionary of all quest data
    
    Requirements to accept quest:
    - Character level >= quest required_level
    - Prerequisite quest completed (if any)
    - Quest not already completed
    - Quest not already active
    
    Returns: True if quest accepted
    Raises:
        QuestNotFoundError if quest_id not in quest_data_dict
        InsufficientLevelError if character level too low
        QuestRequirementsNotMetError if prerequisite not completed
        QuestAlreadyCompletedError if quest already done
    """
    # TODO: Implement quest acceptance
    # Check quest exists
    # Check level requirement
    # Check prerequisite (if not "NONE")
    # Check not already completed
    # Check not already active
    # Add to character['active_quests']
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest ID {quest_id} not found.")
    quest_data = quest_data_dict[quest_id]
    if is_quest_completed(character, quest_id):
        raise QuestAlreadyCompletedError(f"Quest '{quest_id}' is already completed.")
    
    if is_quest_active(character, quest_id):
        raise QuestNotActiveError(f"Quest '{quest_id}' is already active.")
    
    required_level = quest_data.get('required_level', 1)
    if character.get('level', 1) < required_level:
        raise InsufficientLevelError(f"Character level {character.get('level', 1)} is too low. Required level: {required_level}.")
    
    prerequisite_id = quest_data.get('prerequisite', 'NONE')
    if prerequisite_id != 'NONE' and not is_quest_completed(character, prerequisite_id):
        if prerequisite_id not in quest_data_dict:
             raise QuestNotFoundError(f"Prerequisite Quest ID '{prerequisite_id}' not found in game data.")
        prereq_title = quest_data_dict[prerequisite_id].get('title', prerequisite_id)
        raise QuestRequirementsNotMetError(f"Prerequisite quest '{prereq_title}' must be completed first.")
    character['active_quests'].append(quest_id)
    return True

def complete_quest(character, quest_id, quest_data_dict):
    """
    Complete an active quest and grant rewards
    
    Args:
        character: Character dictionary
        quest_id: Quest to complete
        quest_data_dict: Dictionary of all quest data
    
    Rewards:
    - Experience points (reward_xp)
    - Gold (reward_gold)
    
    Returns: Dictionary with reward information
    Raises:
        QuestNotFoundError if quest_id not in quest_data_dict
        QuestNotActiveError if quest not in active_quests
    """
    # TODO: Implement quest completion
    # Check quest exists
    # Check quest is active
    # Remove from active_quests
    # Add to completed_quests
    # Grant rewards (use character_manager.gain_experience and add_gold)
    # Return reward summary
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"{quest_id} not found.")
    if quest_id not in character.get('active_quests', []):
        raise QuestNotActiveError(f"Quest '{quest_id}' is not an active quest")
    quest_data = quest_data_dict[quest_id]

    character['active_quests'].remove(quest_id)
    character['completed_quests'].append(quest_id)
    reward_xp = quest_data.get('reward_xp', 0)
    reward_gold = quest_data.get('reward_gold', 0)
    gain_experience(character, reward_xp)
    add_gold(character, reward_gold)
    return {
        'quest_id': quest_id,
        'reward_xp': reward_xp,
        'reward_gold': reward_gold
    }

def abandon_quest(character, quest_id):
    """
    Remove a quest from active quests without completing it
    
    Returns: True if abandoned
    Raises: QuestNotActiveError if quest not active
    """
    # TODO: Implement quest abandonment
    if quest_id not in character.get('active_quests', []):
        raise QuestNotActiveError(f"Quest '{quest_id}' is not currently active and cannot be abandoned.")
    
    character['active_quests'].remove(quest_id)
    return True

def get_active_quests(character, quest_data_dict):
    """
    Get full data for all active quests
    
    Returns: List of quest dictionaries for active quests
    """
    # TODO: Implement active quest retrieval
    # Look up each quest_id in character['active_quests']
    # Return list of full quest data dictionaries
    active_quests_data = []
    for quest_id in character.get('active_quests', []):
        if quest_id in quest_data_dict:
            active_quests_data.append(quest_data_dict[quest_id])
    return active_quests_data

def get_completed_quests(character, quest_data_dict):
    """
    Get full data for all completed quests
    
    Returns: List of quest dictionaries for completed quests
    """
    # TODO: Implement completed quest retrieval
    completed_quests_data = []
    for quest_id in character.get('completed_quests', []):
        if quest_id in quest_data_dict:
            completed_quests_data.append(quest_data_dict[quest_id])
    return completed_quests_data

def get_available_quests(character, quest_data_dict):
    """
    Get quests that character can currently accept
    
    Available = meets level req + prerequisite done + not completed + not active
    
    Returns: List of quest dictionaries
    """
    # TODO: Implement available quest search
    # Filter all quests by requirements
    available_quests = []
    for quest_id, quest_data in quest_data_dict.items():
        try:
            if can_accept_quest(character, quest_id, quest_data_dict):
                available_quests.append(quest_data)
        except QuestNotFoundError:
            continue
    return available_quests

# ============================================================================
# QUEST TRACKING
# ============================================================================

def is_quest_completed(character, quest_id):
    """
    Check if a specific quest has been completed
    
    Returns: True if completed, False otherwise
    """
    # TODO: Implement completion check
    return quest_id in character.get('completed_quests', [])

def is_quest_active(character, quest_id):
    """
    Check if a specific quest is currently active
    
    Returns: True if active, False otherwise
    """
    # TODO: Implement active check
    return quest_id in character.get('active_quests', [])

def can_accept_quest(character, quest_id, quest_data_dict):
    """
    Check if character meets all requirements to accept quest
    
    Returns: True if can accept, False otherwise
    Does NOT raise exceptions - just returns boolean
    """
    # TODO: Implement requirement checking
    # Check all requirements without raising exceptions
    if quest_id not in quest_data_dict:
        return False
    quest_data = quest_data_dict[quest_id]

    if is_quest_completed(character, quest_id) or is_quest_active(character, quest_id):
        return False
    
    required_level = quest_data.get('required_level', 1)
    if character.get('level', 1) < required_level:
        return False
    
    prerequisite_id = quest_data.get('prerequisite', 'NONE')
    if prerequisite_id != 'NONE':
        if prerequisite_id not in quest_data_dict:
            return False
        if not is_quest_completed(character, prerequisite_id):
            return False
    return True

def get_quest_prerequisite_chain(quest_id, quest_data_dict):
    """
    Get the full chain of prerequisites for a quest
    
    Returns: List of quest IDs in order [earliest_prereq, ..., quest_id]
    Example: If Quest C requires Quest B, which requires Quest A:
             Returns ["quest_a", "quest_b", "quest_c"]
    
    Raises: QuestNotFoundError if quest doesn't exist
    """
    # TODO: Implement prerequisite chain tracing
    # Follow prerequisite links backwards
    # Build list in reverse order
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest ID {quest_id} not found.")
    
    chain = []
    current_id = quest_id
    while current_id and current_id != "NONE":
        chain.append(current_id)
        quest_data = quest_data_dict.get(current_id)
        if not quest_data:
            raise QuestNotFoundError(f"Prerequisite quest {current_id} not found.")
        current_id = quest_data.get('prerequisite', 'NONE')
    return chain[::-1]

# ============================================================================
# QUEST STATISTICS
# ============================================================================

def get_quest_completion_percentage(character, quest_data_dict):
    """
    Calculate what percentage of all quests have been completed
    
    Returns: Float between 0 and 100
    """
    # TODO: Implement percentage calculation
    # total_quests = len(quest_data_dict)
    # completed_quests = len(character['completed_quests'])
    # percentage = (completed / total) * 100
    total_quests = len(quest_data_dict)
    if total_quests == 0:
        return 0.0
    completed_quests = len(character.get('completed_quests', []))
    percentage = (completed_quests / total_quests) * 100
    return round(percentage, 2)

def get_total_quest_rewards_earned(character, quest_data_dict):
    """
    Calculate total XP and gold earned from completed quests
    
    Returns: Dictionary with 'total_xp' and 'total_gold'
    """
    # TODO: Implement reward calculation
    # Sum up reward_xp and reward_gold for all completed quests
    total_xp = 0
    total_gold = 0
    for quest_id in character.get('completed_quests', []):
        quest_data = quest_data_dict.get(quest_id)
        if quest_data:
            total_xp += quest_data.get('reward_xp', 0)
            total_gold += quest_data.get('reward_gold', 0)
    return {
        'total_xp': total_xp,
        'total_gold': total_gold
    }
    pass

def get_quests_by_level(quest_data_dict, min_level, max_level):
    """
    Get all quests within a level range
    
    Returns: List of quest dictionaries
    """
    # TODO: Implement level filtering
    filtered_quests = []
    for quest_id, quest_data in quest_data_dict.items():
        required_level = quest_data.get('required_level', 1)
        if min_level <= required_level <= max_level:
            filtered_quests.append(quest_data)
            
    return filtered_quests

# ============================================================================
# DISPLAY FUNCTIONS
# ============================================================================

def display_quest_info(quest_data):
    """
    Display formatted quest information
    
    Shows: Title, Description, Rewards, Requirements
    """
    # TODO: Implement quest display
    print(f"\n=== {quest_data['title']} ===")
    print(f"Description: {quest_data['description']}")
    # ... etc
    print(f"  Level: {quest_data.get('required_level', 1)}")
    prereq = quest_data.get('prerequisite', 'NONE')
    print(f"  Prerequisite: {prereq}")
    
    print("\n**Rewards:**")
    print(f"  XP: {quest_data.get('reward_xp', 0)}")
    print(f"  Gold: {quest_data.get('reward_gold', 0)}")

def display_quest_list(quest_list):
    """
    Display a list of quests in summary format
    
    Shows: Title, Required Level, Rewards
    """
    # TODO: Implement quest list display
    if not quest_list:
        print("No quests to display.")
        return
    # Suggested detail from Gemini
    print("\n| Title | Req. Level | XP Reward | Gold Reward |")
    print("| :--- | :---: | :---: | :---: |")
    for quest in quest_list:
        title = quest.get('title', 'N/A')
        level = quest.get('required_level', 1)
        xp = quest.get('reward_xp', 0)
        gold = quest.get('reward_gold', 0)
        print(f"| {title} | {level} | {xp} | {gold} |")

def display_character_quest_progress(character, quest_data_dict):
    """
    Display character's quest statistics and progress
    
    Shows:
    - Active quests count
    - Completed quests count
    - Completion percentage
    - Total rewards earned
    """
    # TODO: Implement progress display
    active_count = len(character.get('active_quests', []))
    completed_count = len(character.get('completed_quests', []))
    
    percentage = get_quest_completion_percentage(character, quest_data_dict)
    rewards = get_total_quest_rewards_earned(character, quest_data_dict)
    
    print("\n--- 🗺️ Quest Progress Summary ---")
    print(f"**Active Quests:** {active_count}")
    print(f"**Completed Quests:** {completed_count}")
    print(f"**Completion Percentage:** {percentage}%")
    print(f"**Total XP Earned:** {rewards['total_xp']}")
    print(f"**Total Gold Earned:** {rewards['total_gold']}")

# ============================================================================
# VALIDATION
# ============================================================================

def validate_quest_prerequisites(quest_data_dict):
    """
    Validate that all quest prerequisites exist
    
    Checks that every prerequisite (that's not "NONE") refers to a real quest
    
    Returns: True if all valid
    Raises: QuestNotFoundError if invalid prerequisite found
    """
    # TODO: Implement prerequisite validation
    # Check each quest's prerequisite
    # Ensure prerequisite exists in quest_data_dict
    for quest_id, quest_data in quest_data_dict.items():
        prereq_id = quest_data.get('prerequisite', 'NONE')
        if prereq_id != 'NONE' and prereq_id not in quest_data_dict:
            raise QuestNotFoundError(f"Quest '{quest_id}' has an invalid prerequisite: '{prereq_id}' is not a known quest ID.")
            
    return True
    pass


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== QUEST HANDLER TEST ===")
    
    # Test data
    test_char = {
        'level': 1,
        'active_quests': [],
        'completed_quests': [],
        'experience': 0,
        'gold': 100
    }
    #
    test_quests = {
        'first_quest': {
            'quest_id': 'first_quest',
            'title': 'First Steps',
            'description': 'Complete your first quest',
            'reward_xp': 50,
            'reward_gold': 25,
            'required_level': 1,
            'prerequisite': 'NONE'
        }
    }
    try:
        accept_quest(test_char, 'first_quest', test_quests)
        print("Quest accepted!")
    except QuestRequirementsNotMetError as e:
        print(f"Cannot accept: {e}")

