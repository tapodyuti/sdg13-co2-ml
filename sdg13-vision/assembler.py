# assembler.py

from config import WHOLE_HOME_APPLIANCES


def assemble_home_inventory(all_rooms: dict) -> dict:
    """
    Combines all room inventories.
    Removes duplicate whole-home appliances
    like fridge counted in multiple rooms.
    """
    seen_whole_home = set()
    cleaned_rooms = {}

    for room, inventory in all_rooms.items():
        cleaned = {}
        for appliance, count in inventory.items():
            if appliance in WHOLE_HOME_APPLIANCES:
                if appliance not in seen_whole_home:
                    cleaned[appliance] = count
                    seen_whole_home.add(appliance)
            else:
                cleaned[appliance] = count
        cleaned_rooms[room] = cleaned

    return cleaned_rooms


def get_total_inventory(assembled_rooms: dict) -> dict:
    """
    Flattens all rooms into one total inventory.
    """
    total = {}
    for room, inventory in assembled_rooms.items():
        for appliance, count in inventory.items():
            total[appliance] = total.get(appliance, 0) + count
    return total
