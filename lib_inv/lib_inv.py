from java import *
from collections import defaultdict
import minescript as m
m.set_default_executor(m.script_loop)

Minecraft = JavaClass("net.minecraft.client.Minecraft")
ItemStack = JavaClass("net.minecraft.world.item.ItemStack")
ClickType = JavaClass("net.minecraft.world.inventory.ClickType")
BlockPos = JavaClass("net.minecraft.core.BlockPos")
Math = JavaClass("java.lang.Math")
ItemStack = JavaClass("net.minecraft.world.item.ItemStack")
Registries = JavaClass("net.minecraft.core.registries.Registries")
ResourceLocation = JavaClass("net.minecraft.resources.ResourceLocation")
Float = JavaClass("java.lang.Float")
Array = JavaClass("java.lang.reflect.Array")
Clazz = JavaClass("java.lang.Class")
HashMap = JavaClass("java.util.HashMap")

def _get_private_field_value(obj, intermediary):
    cls = obj.getClass()
    
    field = cls.getDeclaredField(intermediary)
    field.setAccessible(True)
    
    return field.get(obj)

mc = Minecraft.getInstance()

def click_slot(slot: int, right_button: bool = False, container: bool = True) -> bool:
    """
    Click a slot in the inventory.

    Args:
        slot: Slot index to click.
        right_button: Whether to use right-click (default: False).
        container: Whether to target an open container menu (default: True).
    Returns:
        True if successful, False otherwise.
    """
    if not container:
        container_id = mc.player.containerMenu.containerId     
    else:
        screen = mc.screen
        if screen is None:
            return False
        container_menu = screen.getMenu()
        container_id = container_menu.containerId
    
    mouse_button = 1 if right_button else 0
    mc.gameMode.handleInventoryMouseClick(container_id, slot, mouse_button, ClickType.PICKUP, mc.player)
    
    return True
    
def drop_slot(slot: int, stack: bool = False, container: bool = True) -> bool:
    """
    Drop items from a slot.

    Args:
        slot: Slot index.
        stack: If True, drop the entire stack (default: False).
        container: Whether to use a container menu (default: True).
    Returns:
        True if successful, False otherwise.
    """
    if not container:
        container_id = mc.player.containerMenu.containerId     
    else:
        screen = mc.screen
        if screen is None:
            return False
        container_menu = screen.getMenu()
        container_id = container_menu.containerId
    
    mouse_button = 1 if stack else 0
    mc.gameMode.handleInventoryMouseClick(container_id, slot, mouse_button, ClickType.THROW, mc.player)
    
    return True

def shift_click_slot(slot: int, container: bool = True) -> bool:
    """
    Shift-click an inventory slot (quick move).
    
    Args:
        slot: Slot index.
        container: Whether to use a container menu (default: True).
    Returns:
        True if successful, False otherwise.
    """
    if not container:
        container_id = mc.player.containerMenu.containerId     
    else:
        screen = mc.screen
        if screen is None:
            return False
        container_menu = screen.getMenu()
        container_id = container_menu.containerId
    
    mouse_button = 0
    mc.gameMode.handleInventoryMouseClick(container_id, slot, mouse_button, ClickType.QUICK_MOVE, mc.player)
    
    return True

def swap_slots(slot1: int, slot2: int, container: bool = True) -> bool:
    """
    Swap the contents of two inventory slots.
    
    Args:
        slot1: First slot index.
        slot2: Second slot index.
        container: Whether to use a container menu (default: True).
    Returns:
        True if successful, False otherwise.
    """
    if not container:
        container_id = mc.player.containerMenu.containerId     
    else:
        screen = mc.screen
        if screen is None:
            return False
        container_menu = screen.getMenu()
        container_id = container_menu.containerId
    
    mouse_button = 0
    mc.gameMode.handleInventoryMouseClick(container_id, slot1, mouse_button, ClickType.PICKUP, mc.player)
    mc.gameMode.handleInventoryMouseClick(container_id, slot2, mouse_button, ClickType.PICKUP, mc.player)
    mc.gameMode.handleInventoryMouseClick(container_id, slot1, mouse_button, ClickType.PICKUP, mc.player)
    
    return True

def inventory_hotbar_swap(inv_slot: int, hotbar_slot: int) -> bool:
    """
    Swap an inventory slot with a hotbar slot.
    
    Args:
        inv_slot: Inventory slot index.
        hotbar_slot: Hotbar slot index.
    Returns:
        True if successful, False otherwise.
    """
    mc.gameMode.handleInventoryMouseClick(mc.player.containerMenu.containerId, inv_slot, hotbar_slot, ClickType.SWAP, mc.player)
    
    return True

def click_ui_button(button_index: int) -> bool:
    """
    Click a button in the current UI screen.
    
    Args:
        button_index: Button index.
    Returns:
        True if successful, False otherwise.
    """
    screen = mc.screen
    if screen is None:
        return False
    
    container_menu = screen.getMenu()
    container_id = container_menu.containerId

    mc.gameMode.handleInventoryButtonClick(container_id, button_index)
    return True

def create_recipe_lookup():
    """
    Create a lookup map of craftable recipes from the recipe book.
    
    Returns:
        Lookup map or None if faulty.
    """
    book = mc.player.getRecipeBook()
    if not book:
        return None
    recipes = _get_private_field_value(book, "field_54810")
        
    lookup = HashMap()
        
    it = recipes.entrySet().iterator()
    while it.hasNext():
        entry = it.next()
        value = entry.getValue().display().result().stack().getItem()
        
        lookup.put(str(value), entry.getKey())
        
    return lookup

def craft(item_id: str, lookup, craft_all: bool = False) -> bool:
    """
    Craft an item using the recipe book.

    Args:
        item_id: String identifier of the item.
        lookup: Recipe lookup map from create_recipe_lookup().
        craft_all: If True, craft as many as possible (default: False).
    Returns:
        True if crafting was performed, False otherwise.
    """
    book = mc.player.getRecipeBook()

    screen = mc.screen 
    if screen is None:
        return False
    container_menu = screen.getMenu()
    book_type = container_menu.getRecipeBookType()
    if not book.isOpen(book_type):
        book.setOpen(book_type, True)
    
        if screen:
            param_types = Array.newInstance(Clazz, 0)
        
            cls = screen.getClass()
            while cls is not None:
                try:
                    method = cls.getDeclaredMethod("method_48640", param_types)
                    break
                except:
                    cls = cls.getSuperclass()
            
            method.setAccessible(True)
            method.invoke(screen, param_types)
    # ---------------------------------------- 
    display_id= lookup.get(item_id)
    container_id = container_menu.containerId
    
    mc.gameMode.handlePlaceRecipe(container_id, display_id, craft_all)
    mc.gameMode.handleInventoryMouseClick(container_id, 0, 0, ClickType.QUICK_MOVE, mc.player)
    
    return True

def is_slot_empty(slot: int, container: bool = False) -> bool:
    """
    Check whether a slot is empty.
    
    Args:
        slot: To be checked slot
        container: Whether to use a container menu (default: False).
    Returns:
        True if empty, False otherwise.
    """
    if container:
        screen = mc.screen
        if screen is None:
            return False
        container_menu = screen.getMenu()
    
        if container_menu.getItems().get(slot).isEmpty():
            return True
    else: 
        player = mc.player
        inv = player.getInventory()
        if inv.getItem(slot).isEmpty():
            return True
        
    return False

def get_item_at_slot(slot: int, container: bool = False):
    """
    Get the ItemStack at a given slot.
    
    Args:
        slot: To be retrieved slot
        container: Whether to use a container menu (default: False).
    Returns:
        None if empty, ItemStack otherwise
    """
    if container:
        screen = mc.screen
        if screen is None:
            return None
        container_menu = screen.getMenu()
        slot_stack = container_menu.getItems().get(slot)
    else: 
        player = mc.player
        inv = player.getInventory()
        slot_stack = inv.getItem(slot)
        
    return slot_stack      
    
def get_empty_slots(container: bool = False):
    """
    Return a list of indices for all empty slots.
    
    Args:
        container: Whether to use a container menu (default: False).
    Returns:
        List of empry slot indices.
    """
    empty_slots = []
    
    if container:
        screen = mc.screen
        if screen is None:
            return None
        container_menu = screen.getMenu()
        inv = container_menu.getItems()
        
        for index in range(inv.size()):
            slot_stack = inv.get(index)
            if slot_stack.isEmpty():
                empty_slots.append(index)
    else:
        player = mc.player
        inv = player.getInventory() 
        
        for index in range(inv.getContainerSize()):
            slot_stack = inv.getItem(index)
            if slot_stack.isEmpty():
                empty_slots.append(index)        
            
    return empty_slots

def find_item(item_id: str, container: bool = False):
    """
    Find the first slot containing a specific item.
    
    Args:
        item_id: String identifier of the item.
        container: Whether to use a container menu (default: False).
    Returns:
        Index if found, otherwise None.
    """
    if container:
        screen = mc.screen
        if screen is None:
            return None
        container_menu = screen.getMenu()
        inv = container_menu.getItems()
        
        for index in range(inv.size()):
            slot_stack = inv.get(index)
            if str(slot_stack.getItem()) == item_id:
                return index
    else:
        player = mc.player
        inv = player.getInventory()
    
        for index in range(inv.getContainerSize()):
            slot_stack = inv.getItem(index)
            if str(slot_stack.getItem()) == item_id:
                return index
        
    return None
    
def count_item(item_id: str, container: bool = False) -> int:
    """
    Count the total number of a given item in inventory or container.
    
    Args:
        item_id: String identifier of the item.
        container: Whether to use a container menu (default: False).
    Returns:
        Count of item.
    """
    count = 0
    
    if container:
        screen = mc.screen
        if screen is None:
            return None
        container_menu = screen.getMenu()
        inv = container_menu.getItems()

        for index in range(inv.size()):
            slot_stack = inv.get(index)
            if str(slot_stack.getItem()) == item_id:
                count += slot_stack.getCount()
    else:
        player = mc.player
        inv = player.getInventory()

        for index in range(inv.getContainerSize()):
            slot_stack = inv.getItem(index)
            if str(slot_stack.getItem()) == item_id:
                count += slot_stack.getCount()
                
    return count

def is_inventory_full() -> bool:
    """
    Check whether the player's inventory is completely full.
    
    Returns:
        True if it is full, False otherwise
    """
    player = mc.player
    inv = player.getInventory()
    
    for i in range(35):
        stack = inv.getItem(i)
        if stack.getCount() != stack.getMaxStackSize():
            return False
    return True
    
def merge_stacks(slot1: int, slot2: int, container: bool = True) -> bool:
    """
    Try to merge two stacks if they are the same item type.
    
    Args:
        slot1: First slot index.
        slot2: Second slot index.
        container: Whether to use a container menu (default: True).
    Returns:
        True if successful, False otherwise.
    """
    if container:
        screen = mc.screen
        if screen is None:
            return None
        container_menu = screen.getMenu()
        inv = container_menu.getItems()
        container_id = container_menu.containerId
        
        stack1 = inv.get(slot1)
        stack2 = inv.get(slot2)
    else:   
        inv = mc.player.getInventory()
        container_id = mc.player.containerMenu.containerId 
        
        stack1 = inv.getItem(slot1)
        stack2 = inv.getItem(slot2)
    
    if ItemStack.isSameItem(stack1, stack2) and stack1.getMaxStackSize() >= stack1.getCount() + stack2.getCount():
        mouse_button = 0
        mc.gameMode.handleInventoryMouseClick(container_id, slot2, mouse_button, ClickType.PICKUP, mc.player)
        mc.gameMode.handleInventoryMouseClick(container_id, slot1, mouse_button, ClickType.PICKUP, mc.player)
        return True
        
    return False

def compact_inventory(container: bool = True) -> bool:
    """
    Compact inventory by merging partial stacks of identical items.
    
    Args:
        container: Whether to use a container menu (default: True).
    Returns:
        True if successful, False otherwise.
    """
    def _buid_key(stack):
        item_type = str(stack.getItem())
        component = stack.getComponents()
        component_str = str(component)
        return (item_type, component_str)
    
    if not container:
        inv = mc.player.getInventory()
        container_id = mc.player.containerMenu.containerId     
    else:
        screen = mc.screen
        if screen is None:
            return False
        container_menu = screen.getMenu()
        inv = container_menu.getContainer()
        container_id = container_menu.containerId
        
    grouped = defaultdict(list)
        
    for slot_index in range(inv.getContainerSize()):
        stack = inv.getItem(slot_index)
        if stack.isEmpty():
            continue
        
        key = _buid_key(stack)
        
        grouped[key].append(slot_index)
        
    for key in grouped: 
        if len(grouped[key]) <= 1:
            continue
        
        for slot_index in grouped[key]:
            if not inv.getItem(slot_index).isEmpty():
                main_index = slot_index
                break
            
        for other_index in grouped[key]:
            if other_index == main_index:
                continue
            other_stack = inv.getItem(other_index)
            if other_stack.isEmpty():
                continue
            
            mc.gameMode.handleInventoryMouseClick(container_id, other_index, 0, ClickType.PICKUP, mc.player)
            mc.gameMode.handleInventoryMouseClick(container_id, main_index, 0, ClickType.PICKUP, mc.player)
            
            leftover = inv.getItem(other_index)
            if not leftover.isEmpty():
                mc.gameMode.handleInventoryMouseClick(container_id, other_index, 0, ClickType.PICKUP, mc.player)
        
    return True

def check_for_space(item_id: str, count: int) -> bool:
    """
    Check if there is enough space in the inventory for a given item stack.
    
    Args:
        item_id: String identifier of the item.
        count: Amount of items to fit.
    Returns:
        True if there is enough space, False otherwise.
    """
    def _get_registry_from_key(key):
        registry_access = mc.level.registryAccess()
        registry = registry_access.lookupOrThrow(key)
        return registry
   
    def _get_item_registry_entry(item_id):
        item_registry = _get_registry_from_key(Registries.ITEM)
        return item_registry.getValue(ResourceLocation.parse(item_id))
    
    stack_to_insert = ItemStack(_get_item_registry_entry(item_id), count)
    
    player = mc.player
    inv = player.getInventory()

    for i in range(inv.getContainerSize()):
        slot_stack = inv.getItem(i)
        remaining = stack_to_insert.copy()
        
        if not slot_stack.isEmpty() and ItemStack.isSameItem(slot_stack, remaining):
            max_add = Math.min(slot_stack.getMaxStackSize() - slot_stack.getCount(), remaining.getCount())
            if max_add > 0:
                remaining.shrink(max_add)
        elif slot_stack.isEmpty():
            max_add = Math.min(inv.getMaxStackSize(), remaining.getCount())
            remaining.shrink(max_add)
                
        if remaining.isEmpty():
            return True
            
    return False

def select_best_tool(position: tuple(int, int, int)) -> bool:
    """
    Select the best tool for breaking a block at the given position.
    
    Args:
        position: Position of the block
    Returns:
        True if there is successful, False otherwise.
    """
    position = BlockPos(*position)
    state = mc.level.getBlockState(position)
    inv = mc.player.getInventory()
    
    best_speed = 0
    best_index = None
    
    for index in range(inv.getContainerSize()):
        slot_stack = inv.getItem(index)
        slot_item = slot_stack.getItem()
        speed = slot_item.getDestroySpeed(slot_stack, state)

        if Float.compare(speed, best_speed) > 0 and slot_item.isCorrectToolForDrops(slot_stack, state):
            best_speed = speed
            best_index = index
    
    if best_index is not None:
        inv.pickSlot(best_index)
        return True
    return False
