from java import *
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

mc = Minecraft.getInstance()

def click_slot(slot: int, right_button: bool = False, container: bool = True) -> bool:
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
    mc.gameMode.handleInventoryMouseClick(mc.player.containerMenu.containerId, inv_slot, hotbar_slot, ClickType.SWAP, mc.player)
    
    return True

def is_slot_empty(slot: int) -> bool:
    screen = mc.screen
    if screen is None:
        return False
    container_menu = screen.getMenu()
    
    if container_menu.getSlot(slot).getItem().isEmpty():
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
        slot_stack = container_menu.getSlot(slot).getItem()
    
    return slot_stack
    
def get_empty_slots(container: bool = False):
    empty_slots = []
    
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
        if str(slot_stack.getItem()) == item_id:
            return i
        
    return None
    
def count_item(item_id: str, container: bool = False) -> int:
    if not container:
        player = mc.player
        inv = player.getInventory()
    else:
        screen = mc.screen
        if screen is None:
            return None
        container_menu = screen.getMenu()
        inv = container_menu.getContainer()
        
    count = 0
    
    for i in range(inv.getContainerSize()):
        slot_stack = inv.getItem(i)
        if str(slot_stack.getItem()) == item_id:
            count += slot_stack.getCount()
    return count
    
def is_inventory_full() -> bool:
    player = mc.player
    inv = player.getInventory()
    
    for i in range(35):
        stack = inv.getItem(i)
        if stack.getCount() != stack.getMaxStackSize():
            return False
    return True
    
def merge_stacks(slot1: int, slot2: int, container: bool = True) -> bool:
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
    
    stack1 = inv.getItem(slot1)
    stack2 = inv.getItem(slot2)
    
    if ItemStack.isSameItem(stack1, stack2) and stack1.getMaxStackSize() >= stack1.getCount() + stack2.getCount():
        mouse_button = 0
        mc.gameMode.handleInventoryMouseClick(container_id, slot1, mouse_button, ClickType.PICKUP, mc.player)
        mc.gameMode.handleInventoryMouseClick(container_id, slot2, mouse_button, ClickType.PICKUP, mc.player)
        return True
        
    return False

def check_for_space(item_id: str, count: int) -> bool:
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

def select_best_tool(position) -> bool:
    position = BlockPos(*position)
    state = mc.level.getBlockState(position)
    inv = mc.player.getInventory()
    
    best_speed = 0
    best_index = None
    
    for index in range(inv.getContainerSize()):
        slot_stack = inv.getItem(index)
        slot_item = slot_stack.getItem()
        speed = slot_item.getDestroySpeed(slot_stack, state)
        if speed > best_speed and slot_item.isCorrectToolForDrops(slot_stack, state):
            best_speed = speed
            best_index = index
    
    if best_index is not None:
        inv.pickSlot(best_index)
        return True
    return False
