from java import *
from collections import defaultdict, OrderedDict
import time
import threading

import minescript as m
m.set_default_executor(m.script_loop)

Minecraft = JavaClass("net.minecraft.client.Minecraft")
ItemStack = JavaClass("net.minecraft.world.item.ItemStack")
ClickType = JavaClass("net.minecraft.world.inventory.ClickType")
BlockPos = JavaClass("net.minecraft.core.BlockPos")
Math = JavaClass("java.lang.Math")
Registries = JavaClass("net.minecraft.core.registries.Registries")
ResourceLocation = JavaClass("net.minecraft.resources.ResourceLocation")
Float = JavaClass("java.lang.Float")
Array = JavaClass("java.lang.reflect.Array")
Clazz = JavaClass("java.lang.Class")
HashMap = JavaClass("java.util.HashMap")
ItemEntity = JavaClass("net.minecraft.world.entity.item.ItemEntity")
GameType = JavaClass("net.minecraft.world.level.GameType")

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
            return None
        container_menu = screen.getMenu()
    else:
        container_menu = mc.player.containerMenu
        
    if container_menu.getItems().get(slot).isEmpty():
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
    else:
        container_menu = mc.player.containerMenu
        
    slot_stack = container_menu.getItems().get(slot)     
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
    else:
        container_menu = mc.player.containerMenu
        
    inv = container_menu.getItems()
        
    for index in range(inv.size()):
        slot_stack = inv.get(index)
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
    else:
        container_menu = mc.player.containerMenu
        
    inv = container_menu.getItems()
        
    for index in range(inv.size()):
        slot_stack = inv.get(index)
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
    else:
        container_menu = mc.player.containerMenu
        
    inv = container_menu.getItems()

    for index in range(inv.size()):
        slot_stack = inv.get(index)
        if str(slot_stack.getItem()) == item_id:
            count += slot_stack.getCount()
                
    return count

def has_item(item_id: str, amount: int = 1, container: bool = False) -> bool:
    """
    Check if an inventory or container contains atleast a set amount of an item.
    
    Args:
        item_id: String identifier of the item.
        amount: The minimum amount of the item.
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
    else:
        container_menu = mc.player.containerMenu
        
    inv = container_menu.getItems()

    for index in range(inv.size()):
        slot_stack = inv.get(index)
        if str(slot_stack.getItem()) == item_id:
            count += slot_stack.getCount()
            if count >= amount:
                return True
            
    return False
    
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
        container_id = container_menu.containerId
    else:   
        container_menu = mc.player.containerMenu
        container_id = mc.player.containerMenu.containerId     
        
    inv = container_menu.getItems()
        
    stack1 = inv.get(slot1)
    stack2 = inv.get(slot2)
    
    if ItemStack.isSameItem(stack1, stack2) and stack1.getMaxStackSize() >= stack1.getCount() + stack2.getCount():
        mouse_button = 0
        mc.gameMode.handleInventoryMouseClick(container_id, slot2, mouse_button, ClickType.PICKUP, mc.player)
        mc.gameMode.handleInventoryMouseClick(container_id, slot1, mouse_button, ClickType.PICKUP, mc.player)
        return True
        
    return False

# internal use only
class Item():
    def __init__(self, stack, slot):
        self.str = str(stack.getItem())
        self.count = stack.getCount()
        self.maxCount = stack.getMaxStackSize()
        self.tag = self._find_relevant_tag(stack)
        self.slot = slot
        self._resolve_no_tag(self.tag)
            
    def _find_relevant_tag(self, item_stack):
        tags = item_stack.getTags().toList()
        for index in range(tags.size()):
            tag = tags.get(index).location()
            tag_path = tag.getPath()
        
            if "/" not in tag_path and "enchantable" not in tag_path and "_" not in tag_path:
                return tag_path
        return None
    
    def _resolve_no_tag(self, tag):
        if not tag and "minecraft:air" not in self.str:
            self.tag = self.str
    
    def move(self, target_slot):
        if self.count == 0 or self.slot == target_slot:
            return False
        if not self.str == target_slot.get_str():
            mc.gameMode.handleInventoryMouseClick(self.get_id(), self.slot.index, 0, ClickType.PICKUP, mc.player)
            mc.gameMode.handleInventoryMouseClick(self.get_id(), target_slot.index, 0, ClickType.PICKUP, mc.player)
            
            if not target_slot.is_empty():
                mc.gameMode.handleInventoryMouseClick(self.get_id(), self.slot.index, 0, ClickType.PICKUP, mc.player)
            
            self.slot.item, target_slot.item = target_slot.item, self.slot.item
            
            self.slot.item.slot = self.slot
            target_slot.item.slot = target_slot
        else:
            mc.gameMode.handleInventoryMouseClick(self.get_id(), self.slot.index, 0, ClickType.PICKUP, mc.player)
            mc.gameMode.handleInventoryMouseClick(self.get_id(), target_slot.index, 0, ClickType.PICKUP, mc.player)
            
            change = Math.min(target_slot.get_max_count() -  target_slot.get_count(), self.count)
            target_slot.item.count += change
            self.slot.item.count -= change
            if self.slot.item.count == 0:
                self.slot.item.str = "minecraft:air"
            else:
                mc.gameMode.handleInventoryMouseClick(self.get_id(), self.slot.index, 0, ClickType.PICKUP, mc.player)
        return True
    
    def find_not_full(self):
        slots = []
        for slot in self.slot.inventory.slots:
            if slot.get_str() == self.str and not slot.item is self and slot.get_count() < slot.get_max_count():
                slots.append(slot)
        return slots
    
    def find_tag(self):
        slots = []
        for slot in self.slot.inventory.slots:
            if slot.get_tag() == self.tag and not slot.item is self:
                slots.append(slot)
                print(slot.item.str)
        return slots
    
    def get_id(self):
        return self.slot.get_id()

# internal use only
class Slot():
    def __init__(self, index, item, inventory):
        self.index = index
        self.item = Item(item, self)
        self.inventory = inventory
        
    def is_empty(self):
        return True if self.item.count == 0 else False
    
    def get_tag(self):
        return self.item.tag
    
    def get_str(self):
        return self.item.str
    
    def get_count(self):
        return self.item.count
    
    def get_max_count(self):
        return self.item.maxCount
    
    def get_id(self):
        return self.inventory.container_id

# internal use only
class Inventory():
    def __init__(self, inventory, container_id):
        try:
            self.slots = [Slot(slot, inventory.getItem(slot), self) for slot in range(inventory.SELECTION_SIZE, inventory.INVENTORY_SIZE)]
            self.first_index = inventory.SELECTION_SIZE
        except:
            self.slots = [Slot(slot, inventory.getItem(slot), self) for slot in range(inventory.getContainerSize())]
            self.first_index = 0
        self.container_id = container_id
    
    def get_slot(self, index):
        for slot in self.slots:
            if slot.index == index:
                return slot
    
    def get_tags(self):
        tags = []
        for slot in self.slots:
            tag = slot.get_tag()
            if tag is not None and tag not in tags:
                tags.append(tag)
        tags.sort()
        return tags
    
    def get_item_names(self):
        names = []
        for slot in self.slots:
            name = slot.get_str()
            if name not in names and "minecraft:air" not in name:
                names.append(name)
        names.sort()
        return names
    
    def get_names_with_tag(self, tag):
        names = []
        for slot in self.slots:
            name = slot.get_str()
            if name not in names and "minecraft:air" not in name and tag == slot.get_tag():
                names.append(name)
        names.sort()
        return names
    
    def items_with_tag(self, tag):
        items = []
        for slot in self.slots:
            if tag == slot.get_tag():
                items.append(slot.item)
        return items
    
    def items_with_name(self, name):
        items = []
        for slot in self.slots:
            if name == slot.get_str():
                items.append(slot.item)
        return items
    
    def compact(self):
        for name in self.get_item_names():
            for item in self.items_with_name(name):
                if item.count < item.maxCount:
                    for slot in item.find_not_full():
                        item.move(slot)
                        if item.count == 0:
                            break

    def sort(self):
        self.compact()
        progress = self.first_index
        for tag in self.get_tags():
            for name in self.get_names_with_tag(tag):
                items_with_name = self.items_with_name(name)
                for i, item in enumerate(items_with_name):
                    if item.count == item.maxCount:
                        item.move(self.get_slot(progress))
                        progress += 1
                    else:
                        target_slot = self.get_slot(progress + len(items_with_name) - 1 - i)
                        item.move(target_slot)
                        if target_slot.index == progress:
                            progress += 1
        return True


def compact_inventory(container: bool = True) -> bool:
    """
    Compact inventory by merging partial stacks of identical items.
    
    Args:
        container: Whether to use a container menu (default: True).
    Returns:
        True if successful, False otherwise.
    """
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
           
    inv = Inventory(inv, container_id)
    return inv.compact()

def sort_inventory(container: bool = False):
    """
    Sort inventory by merging partial stacks and then sorting by tag and aplhabet.
    
    Args:
        container: Whether to use a container menu (default: False).
    Returns:
        True if successful, False otherwise.
    """
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
           
    inv = Inventory(inv, container_id)
    return inv.sort()

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

    for i in range(inv.INVENTORY_SIZE):
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

def select_best_tool(position: list[int, int, int]) -> bool:
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

class _Listener():
    def __init__(self):
        self.registered = False
        self.callback = None
        self.interval = 1/20 # 20 ticks per second
        
    def register(self, callback):
        self.registered = True
        self.callback = callback
        self.thread = threading.Thread(target=self._run_loop)
        self.thread.start()
        
        self.thread.join()

        return self
    
    def unregister(self):
        self.registered = False 
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=1)   
            
class _ItemPickupListener(_Listener):
    def __init__(self):
        self.pickup_map = HashMap()
        super().__init__()
        
    def _can_insert(self, inv, stack_to_insert):
        for i in range(35):
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
        
    def _handle_pickup(self, entity):
        if not self.pickup_map.containsKey(entity):
            self.pickup_map.put(entity, entity.getItem().copy())
            
        it = self.pickup_map.entrySet().iterator()
        while it.hasNext():
            entity = it.next().getKey()
            if (
                not mc.player.gameMode() is GameType.SPECTATOR 
                and mc.player.isAlive() 
                and self._can_insert(mc.player.getInventory(), entity.getItem())
                and not entity.hasPickUpDelay()
                and entity.onGround()
                ):
                if entity.isRemoved():
                    self.callback(self.pickup_map.get(entity))
                    self.pickup_map.remove(entity)
        
    def _run_loop(self):
        while self.registered:
            entities = mc.level.entitiesForRendering()
            try:
                it = entities.iterator()
                while it.hasNext():
                    entity = it.next()
                    if entity.getClass().isAssignableFrom(ItemEntity):
                        if entity.getBoundingBox().intersects(mc.player.getBoundingBox().inflate(1)):
                                self._handle_pickup(entity)            
            except Exception as e:
                pass
                            
            time.sleep(self.interval)

class InventoryEvent():
    ITEM_PICKUP = _ItemPickupListener()
