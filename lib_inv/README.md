# Lib_Inv

**Version:** 1.1.0\
**Author:** JulianIsLost\
**Date:** 03.09.2025

User-friendly API for performing invenotry operations in Minecraft.  
This module should be imported by other scripts and not run directly.

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
  - **returns:** `bool` — `True` if successful, `False` otherwise.

---

- **drop_slot(slot: int, stack: bool = False, container: bool = True) -> bool**

  Drops an item from the specified slot.

  - **slot:** `int` — The slot index to drop from.
  - **stack:** `bool` — Drop the whole stack (`True`) or a single item (`False`).
  - **returns:** `bool` — `True` if successful, `False` otherwise.

---

- **shift_click_slot(slot: int, container: bool = True) -> bool**

  Performs a shift-click on a slot (moves item between inventories).

  - **slot:** `int` — The slot index to shift-click.
  - **returns:** `bool` — `True` if successful, `False` otherwise.

---

- **swap_slots(slot1: int, slot2: int, container: bool = True) -> bool**

  Swaps the contents of two inventory slots.

  - **slot1:** `int` — The first slot index.
  - **slot2:** `int` — The second slot index.
  - **returns:** `bool` — `True` if successful, `False` otherwise.

---

- **inventory_hotbar_swap(inv_slot: int, hotbar_slot: int) -> bool**

  Swaps a slot of the inventory with a slot of the hotbar

  - **inv_slot:** `int` — The slot to swap to the hotbar.
  - **hotbar_slot:** `int` — The slot to swap to the inventory.
  - **returns:** `bool` — `True` if done.

---

- **is_slot_empty(slot: int) -> bool**

  Checks if a slot is empty.

  - **slot:** `int` — The slot index to check.
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

---

- **count_item(item_id: str, container: bool = False) -> int | None**

  Counts the total number of a specific item.

  - **item_id:** `str` — The item ID to count.
  - **container:** `bool` — Whether to count in the container menu instead of the player inventory.
  - **returns:** `int | None` — The total count of the item, or `None` if no screen is open.

---

- **is_inventory_full() -> bool**

  Checks if the player inventory is completely full.

  - **returns:** `bool` — `True` if full, `False` otherwise.

---

- **merge_stacks(slot1: int, slot2: int) -> bool**

  Merges two compatible item stacks if possible.

  - **slot1:** `int` — The first slot index.
  - **slot2:** `int` — The second slot index.
  - **returns:** `bool` — `True` if stacks were merged, `False` otherwise.

---

- **check_for_space(stack_to_insert: ItemStack) -> bool**

  Checks if there is enough space in the inventory for a given item stack.

  - **stack_to_insert:** `ItemStack` — The item stack to insert.
  - **returns:** `bool` — `True` if it can fit, `False` otherwise.

---

- **select_best_tool(position: tuple[int, int, int]) -> bool**

  Selects the best tool for breaking the block at a given position.

  - **position:** `tuple[int, int, int]` — The block position (x, y, z).
  - **returns:** `bool` — `True` if a tool was selected, `False` otherwise.


## Useful Links

- [Minecraft Internal Mappings](https://mappings.dev) 
- [Minescript Discord](https://discord.gg/NjcyvrHTze)

## License

MIT © 2025 JulianIsLost
