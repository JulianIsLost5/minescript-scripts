# Lib_Inv

**Version:** 1.5.0\
**Author:** JulianIsLost\
**Date:** 03.09.2025

User-friendly API for performing invenotry operations in Minecraft.  
This module should be imported by other scripts and not run directly.

Big thanks to [maxuser](https://github.com/maxuser0) for creating the mod and [razrcraft](https://github.com/R4z0rX) for bringing light into the darkness of minescript coding
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

- **click_slot(slot: int, right_button: bool = False, container: bool = True) -> bool**

  Clicks on an inventory slot.

  - **slot:** `int` — The slot index to click.
  - **right_button:** `bool` — Whether to use right-click (defaults to `False`).
  - **container:** `bool` — Whether to perform clicks in a container menu instead of the player inventory
  - **returns:** `bool` — `True` if successful, `False` otherwise.
  <sub>Extended on Minescript Plus</sub>
---

- **drop_slot(slot: int, stack: bool = False, container: bool = True) -> bool**

  Drops an item from the specified slot.

  - **slot:** `int` — The slot index to drop from.
  - **stack:** `bool` — Drop the whole stack (`True`) or a single item (`False`).
  - **container:** `bool` — Whether to perform clicks in a container menu instead of the player inventory
  - **returns:** `bool` — `True` if successful, `False` otherwise.

---

- **shift_click_slot(slot: int, container: bool = True) -> bool**

  Performs a shift-click on a slot (moves item between inventories).

  - **slot:** `int` — The slot index to shift-click.
  - **container:** `bool` — Whether to perform clicks in a container menu instead of the player inventory
  - **returns:** `bool` — `True` if successful, `False` otherwise.
  <sub>Extended on Minescript Plus</sub>
---

- **swap_slots(slot1: int, slot2: int, container: bool = True) -> bool**

  Swaps the contents of two inventory slots.

  - **slot1:** `int` — The first slot index.
  - **slot2:** `int` — The second slot index.
  - **container:** `bool` — Whether to perform clicks in a container menu instead of the player inventory
  - **returns:** `bool` — `True` if successful, `False` otherwise.

---

- **inventory_hotbar_swap(inv_slot: int, hotbar_slot: int) -> bool**

  Swaps a slot of the inventory with a slot of the hotbar

  - **inv_slot:** `int` — The slot to swap to the hotbar.
  - **hotbar_slot:** `int` — The slot to swap to the inventory.
  - **returns:** `bool` — `True` if done.
  <sub>Replicated from Minescript Plus</sub>
---

- **create_recipe_lookup() -> HashMap**

  Creates a lookup for crafting recipes. Must be newly created each session.

  - **returns:** `HashMap` — Map that is used by the `craft()` method.

---

- **craft(item_id: str, lookup, craft_all: bool = False) -> bool**

  Performs a crafting operation using the crafting book's recipes.

  - **item_id:** `str` — The item ID of the crafting result.
  - **lookup:** `HashMap` — Lookup returned by `create_recipe_lookup()`.
  - **craft_all:** `int` — Whether to shift click a recipe.
  - **returns:** `bool` — `True` if succesful, `False` if there is no crafting ui open.

---

- **click_ui_button(button_index: int) -> bool**

  Clicks a button in an open ui.

  - **slot:** `int` — The slot index to check.
  - **returns:** `bool` — `True` if succesful, `False` if there is no ui open.

---

- **is_slot_empty(slot: int, container: bool = False) -> bool**

  Checks if a slot is empty.

  - **slot:** `int` — The slot index to check.
  - **container:** `bool` — Whether to check the container menu instead of the player inventory.
  - **returns:** `bool` — `True` if empty, `False` otherwise.

---

- **get_item_at_slot(slot: int, container: bool = False) -> ItemStack | None**

  Gets the item at a given slot.

  - **slot:** `int` — The slot index to check.
  - **container:** `bool` — Whether to check the container menu instead of the player inventory.
  - **returns:** `ItemStack | None` — The item stack at the slot, or `None` if unavailable.

---

- **get_empty_slots(container: bool = False) -> list[int] | None**

  Finds all empty slots in the inventory or container.

  - **container:** `bool` — Whether to check the container menu instead of the player inventory.
  - **returns:** `list[int] | None` — A list of empty slot indices, or `None` if no screen is open.

---

- **find_item(item_id: str, container: bool = False) -> int | None**

  Finds the first slot index containing the given item.

  - **item_id:** `str` — The item ID to search for.
  - **container:** `bool` — Whether to search in the container menu instead of the player inventory.
  - **returns:** `int | None` — The slot index if found, otherwise `None`.
  <sub>Inspired by Minescript Plus</sub>
---

- **count_item(item_id: str, container: bool = False) -> int | None**

  Counts the total number of a specific item.

  - **item_id:** `str` — The item ID to count.
  - **container:** `bool` — Whether to count in the container menu instead of the player inventory.
  - **returns:** `int | None` — The total count of the item, or `None` if no screen is open.
  <sub>Extended on Minescript Plus</sub>
---

- **is_inventory_full() -> bool**

  Checks if the player inventory is completely full.

  - **returns:** `bool` — `True` if full, `False` otherwise.

---

- **merge_stacks(slot1: int, slot2: int, container: bool = True) -> bool**

  Merges two compatible item stacks if possible.

  - **slot1:** `int` — The first slot index.
  - **slot2:** `int` — The second slot index.
  - **container:** `bool` — Whether to merge stacks in a container menu instead of the player inventory
  - **returns:** `bool` — `True` if stacks were merged, `False` otherwise.

---

- **compact_inventory(container: bool = True) -> bool**

  Compact inventory by merging partial stacks of identical items.

  - **container:** `bool` — Whether to compact a container menu instead of the player inventory
  - **returns:** `bool` — `True` when done.

---

- **sort_inventory(container: bool = False) -> bool**

  Sort inventory by merging partial stacks and then sorting by tag and aplhabet.

  - **container:** `bool` — Whether to sort a container menu instead of the player inventory
  - **returns:** `bool` — `True` when done.
  <sub>Special thanks to razrcraft for brainstorming an approach with me</sub>

---

- **check_for_space(item_id: str, count: int) -> bool**

  Checks if there is enough space in the inventory for a given item stack.

  - **item_id:** `str` — The to inserted item's id.
  - **count:** `int` — The to inserted item's count.
  - **returns:** `bool` — `True` if it can fit, `False` otherwise.

---

- **select_best_tool(position: tuple[int, int, int]) -> bool**

  Selects the best tool for breaking the block at a given position.

  - **position:** `tuple[int, int, int]` — The block position (x, y, z).
  - **returns:** `bool` — `True` if a tool was selected, `False` otherwise.


## Useful Links

- [Minecraft Internal Mappings](https://mappings.dev) 
- [Minescript Discord](https://discord.gg/NjcyvrHTze)
- [Minescript Plus](https://github.com/R4z0rX/minescript-scripts/tree/main/Minescript-Plus)

## License

MIT © 2025 JulianIsLost
