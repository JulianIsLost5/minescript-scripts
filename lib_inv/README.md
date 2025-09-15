# Lib_Inv

**Version:** 1.9.0
**Author:** JulianIsLost  
**Date:** 15.09.2025  

User-friendly API for performing invenotry operations in Minecraft. 
This module should be imported by other scripts and not run directly.  

> Big thanks to [maxuser](https://github.com/maxuser0) for creating the mod and [razrcraft](https://github.com/R4z0rX) for bringing light into the darkness of minescript coding  
> This readme was heavily inspired by [razrcraft](https://github.com/R4z0rX)
---

## Prerequisites

Before you start, make sure you have:

- **Fabric** mod loader configured
- **Minescript 5.0b5** installed (min)
- **Mappings** installed

---

## Usage

- Download the **lib_inv.py** file
- Place it directly in the minescript folder
- Import the module into your script:
  
  ```python
  import lib_inv as lv
  ```
- Use the methods as documented below

---

## Methods

### `Inventory Interaction`

- **click_slot(slot: int, right_button: bool = False, container: bool = True) -> bool**

  Clicks on an inventory slot.  
  *Returns:* `True` if successful, `False` if otherwise.   
  > Extended on Minescript Plus

- **drop_slot(slot: int, stack: bool = False, container: bool = True) -> bool**

  Drops an item from the specified slot.  
  *returns:* `True` if successful, `False` otherwise.

- **shift_click_slot(slot: int, container: bool = True) -> bool**

  Performs a shift-click on a slot (moves item between inventories).  
  *returns:* `True` if successful, `False` otherwise.  
  > Extended on Minescript Plus

- **swap_slots(slot1: int, slot2: int, container: bool = True) -> bool**

  Swaps the contents of two inventory slots.  
  *returns:* `True` if successful, `False` otherwise.


- **inventory_hotbar_swap(inv_slot: int, hotbar_slot: int) -> bool**

  Swaps a slot of the inventory with a slot of the hotbar  
  *returns:* `True` if done.  
  > Extended on Minescript Plus

- **click_ui_button(button_index: int) -> bool**

  Clicks a button in an open ui.  
  *returns:* `True` if succesful, `False` if there is no ui open.

---

### `Inventory Rendering`

- **show_slots() -> bool**

  Renders the indices of all slots in an invenotry on top of them.  
  Useful for understanding the indexing other methods use.  
  *returns:* True  
  > Implementation inspired by Minescript Plus

- **hide_slots() -> bool**

  Unrenders the indices of all slots in an invenotry on top of them.  
  *returns:* True

---

### `Crafting`

- **create_recipe_lookup() -> HashMap**

  Creates a lookup for crafting recipes. Must be newly created each session.  
  *returns:* `HashMap` that is used by the following `craft()` method.


- **craft(item_id: str, lookup, craft_all: bool = False) -> bool**

  Performs a crafting operation using the crafting book's recipes.  
  *returns:* `True` if succesful, `False` if there is no crafting ui open.  
  <u>Note</u>: `lookup` must be the `HashMap` returned by `create_recipe_lookup()`

---

### `Inventory queries`

- **is_slot_empty(slot: int, container: bool = False) -> bool**

  Checks if a slot is empty.  
  *returns:* `True` if empty, `False` otherwise.


- **get_empty_slots(container: bool = False) -> list[int] | None**

  Finds all empty slots in the inventory or container.  
  *returns:* A list of empty slot indices, or `None` if no screen is open.


- **get_item_at_slot(slot: int, container: bool = False) -> ItemStack | None**

  Gets the item at a given slot.  
  *returns:* The `ItemStack` at the slot, or `None` if unavailable.

- **get_durability_of_slot(slot: int, container: bool = False) -> int:**

  Get the durability of an item at a given slot.  
  *returns:* Integer of durabilty.

- **get_durability_of_item(item_stack: ItemStack) -> int:**

  Get the durability of an item at a given slot.  
  *returns:* Integer of durabilty.

- **find_item(item_id: str, container: bool = False) -> int | None**

  Finds the first slot index containing the given item.  
  *returns:* The slot index if found, otherwise `None`.  
  > Extended on Minescript Plus


- **count_item(item_id: str, container: bool = False) -> int | None**

  Counts the total number of a specific item.  
  *returns:* The total count of the item, or `None` if no screen is open.  
  > Extended on Minescript Plus


- **has_item(item_id: str, amount: int = 1, container: bool = False) -> bool:**

  Returns if the container at least holds the given amount of the item.  
  *returns:* `True` if there are at least the amount of items, `False` otherwise.


- **is_inventory_full() -> bool**

  Checks if the player inventory is completely full.  
  *returns:** `True` if full, `False` otherwise.

- **check_for_space(item_id: str, count: int) -> bool**

  Checks if there is enough space in the inventory for a given item stack.  
  *returns:** `True` if it can fit, `False` otherwise.

---

### `Inventory Organisation`

- **merge_stacks(slot1: int, slot2: int, container: bool = True) -> bool**

  Merges two compatible item stacks if possible.  
  *returns:* `True` if stacks were merged, `False` otherwise.


- **compact_inventory(container: bool = True) -> bool**

  Compact inventory by merging partial stacks of identical items.  
  *returns:* `True` when done.


- **sort_inventory(container: bool = False) -> bool**

  Sort inventory by merging partial stacks and then sorting by tag and aplhabet.  
  *returns:* `True` when done.  
  <sub> Unintended behavior might occur, please report it to me</sub>  
  > Special thanks to razrcraft for brainstorming an approach with me

---

### `Misc`

- **select_best_tool(position: tuple[int, int, int]) -> bool**

  Selects the best tool for breaking the block at a given position.  
  *returns:* `True` if a tool was selected, `False` otherwise.

- **find_containers(radius: int | list[int, int, int], return_block_entity: bool = False, return_block_pos: bool = False) -> tuple(int, int, int) | BlockEntity | BlockPos:**

  Finds all container blocks in an area around the player.  
  *returns:* A list of container coordinates or BlockEntities or BlockPos.

- **get_food_level() -> int:**

  Gets the players current food level.  
  *returns:* Integer value of the food level.

- **get_saturation_level() -> int:**

  Gets the players current saturation level.  
  *returns:* Integer value of the saturation level.

---

### `InventoryEvent`
Event system for registering inventory related callbacks (fabric callbacks as template).

## Event Callbacks

| EVENT_TYPE  | Called if  | Passes |
|:----------- |:----------- |:------- |
| ITEM_PICKUP | An item is picked up by the player | ItemStack instance

- **EVENT_TYPE.register(callback: Callable) -> Listener**  
  Registers the callback.   
  *Returns:* A `Listener` instance, which can be manually unregistered.

**Examples:**

Registering an event manually:
```python
from lib_inv import InventoryEvent

def on_pickup(item):
    print(f"Picked up: {item}")

listener = InventoryEvent.ITEM_PICKUP.register(on_pickup)
# unregister
listener.unregister()
```

## Useful Links

- [Minecraft Internal Mappings](https://mappings.dev) 
- [Minescript Discord](https://discord.gg/NjcyvrHTze)
- [Minescript Plus](https://github.com/R4z0rX/minescript-scripts/tree/main/Minescript-Plus)

## License

MIT © 2025 JulianIsLost
