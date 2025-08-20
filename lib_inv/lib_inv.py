#!python
import system.pyj.minescript as m

Minecraft = JavaClass("net.minecraft.client.Minecraft")
ItemStack = JavaClass("net.minecraft.world.item.ItemStack")
ClickType = JavaClass("net.minecraft.world.inventory.ClickType")
Math = JavaClass("java.lang.Math")

mc = Minecraft.getInstance()

def click_slot(slot: int, right_button: bool = False):
    screen = mc.screen
    if screen is None:
        return False
    container_menu = screen.getMenu()
    
    mouse_button = 1 if right_button else 0
    mc.gameMode.handleInventoryMouseClick(container_menu.containerId, slot, mouse_button, ClickType.PICKUP, mc.player)
    
    return True
    
def drop_slot(slot: int):
    screen = mc.screen
    if screen is None:
        return False
    container_menu = screen.getMenu()
    
    mouse_button = 0
    mc.gameMode.handleInventoryMouseClick(container_menu.containerId, slot, mouse_button, ClickType.THROW, mc.player)
    
    return True

def shift_click_slot(slot: int):
    screen = mc.screen
    if screen is None:
        return False
    container_menu = screen.getMenu()
    
    mouse_button = 0
    mc.gameMode.handleInventoryMouseClick(container_menu.containerId, slot, mouse_button, ClickType.QUICKMOVE, mc.player)
    
    return True

def swap_slots(slot1: int, slot2: int):
    screen = mc.screen
    if screen is None:
        return False
    container_menu = screen.getMenu()
    
    mouse_button = 0
    mc.gameMode.handleInventoryMouseClick(container_menu.containerId, slot1, mouse_button, ClickType.PICKUP, mc.player)
    mc.gameMode.handleInventoryMouseClick(container_menu.containerId, slot2, mouse_button, ClickType.PICKUP, mc.player)
    mc.gameMode.handleInventoryMouseClick(container_menu.containerId, slot1, mouse_button, ClickType.PICKUP, mc.player)
    
    return True

def is_slot_empty(slot: int):
    screen = mc.screen
    if screen is None:
        return False
    container_menu = screen.getMenu()
    
    if container_menu.getSlot(slot).isEmpty():
        return True
        
    return False

def get_item_at_slot(slot: int, container: bool = False):
    if not container:
        player = mc.player
        inv = player.getInventory()
        slot_stack = inv.getItem(slot)
    else: 
        screen = mc.screen
        if screen is None:
            return None
        container_menu = screen.getMenu()
        slot_stack = container_menu.getSlot(slot)
    
    return slot_stack
    
def get_empty_slots():
    player = mc.player
    inv = player.getInventory()
    
    empty_slots = []
    
    for i in range(inv.getContainerSize()):
        slot_stack = inv.getItem(i)
        if slot_stack.isEmpty():
            empty_slots.append(i)
            
    return empty_slots

def find_item(item_id: str, container: bool = False):
    if not container:
        player = mc.player
        inv = player.getInventory()
    else: 
        screen = mc.screen
        if screen is None:
            return None
        container_menu = screen.getMenu()
        inv = container_menu.getContainer()
        
    for i in range(inv.getContainerSize()):
        slot_stack = inv.getItem(i)
        if slot_stack.item == item_id:
            return i
        
    return None
    
def count_item(item_id: str):
    player = mc.player
    inv = player.getInventory()
    
    count = 0
    
    for i in range(inv.getContainerSize()):
        slot_stack = inv.getItem(i)
        if slot_stack.item == item_id:
            count += slot_stack.getCount()
    return count
    
def is_inventory_full():
    player = mc.player
    inv = player.getInventory()
    
    for i in range(35):
        stack = inv.getItem(i)
        if stack.getCount() != stack.getMaxStackSize():
            return False
    return True
    
def merge_stacks(slot1: int, slot2: int):
    screen = mc.screen
    if screen is None:
        return False
    container_menu = screen.getMenu()
    
    stack1 = container_menu.getSlot(slot1)
    stack2 = container_menu.getSlot(slot2)
    
    if ItemStack.isSameItem(stack1, stack2) and stack1.getMaxStackSize() >= stack1.getCount() + stack2.getCount():
        mouse_button = 0
        mc.gameMode.handleInventoryMouseClick(container_menu.containerId, slot1, mouse_button, ClickType.PICKUP, mc.player)
        mc.gameMode.handleInventoryMouseClick(container_menu.containerId, slot2, mouse_button, ClickType.PICKUP, mc.player)
        return True
        
    return False

def compact_inventory():
    player = mc.player
    inv = player.getInventory()
    
    for i in range(inv.getContainerSize()):
        slot_stack_i = inv.getItem(i)
        
        if slot_stack_i.isEmpty():
            continue
        
        for j in range(inv.getContainerSize()):
            if i == j:
                continue
            
            slot_stack_j = inv.getItem(j)
            
            if not ItemStack.isSameItem(slot_stack_i, slot_stack_j):
                continue
            
            transferable = Math.min(slot_stack_i.getCount(), slot_stack_i.getMaxStackSize() - slot_stack_j.getCount())
            if transferable > 0:
                slot_stack_j.grow(transferable)
                slot_stack_i.shrink(transferable)
                
                inv.setItem(j, slot_stack_j)
                inv.setItem(i, slot_stack_i)
                
                if slot_stack_i.isEmpty():
                    break

def check_for_space(stack_to_insert: ItemStack):
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
