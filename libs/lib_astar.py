from java import *
import minescript as m
m.set_default_executor(m.script_loop)

Minecraft = JavaClass("net.minecraft.client.Minecraft") 
Math = JavaClass("java.lang.Math")
BlockPos = JavaClass("net.minecraft.core.BlockPos")
Anchor = JavaClass("net.minecraft.commands.arguments.EntityAnchorArgument$Anchor")

mc = Minecraft.getInstance()

pyj_embed = eval_pyjinn_script(r"""
Minecraft = JavaClass("net.minecraft.client.Minecraft") 
ClientTickEvents = JavaClass("net.fabricmc.fabric.api.client.event.lifecycle.v1.ClientTickEvents")
ClientTickEventsEndTick = JavaClass("net.fabricmc.fabric.api.client.event.lifecycle.v1.ClientTickEvents$EndTick")
BlockPos = JavaClass("net.minecraft.core.BlockPos")
Anchor = JavaClass("net.minecraft.commands.arguments.EntityAnchorArgument$Anchor")
Math = JavaClass("java.lang.Math")
     
mc = Minecraft.getInstance()           
        
class Node:
        def __init__(self, block, g=0, h=0, parent=None):
            self.block = block           # the position/block
            self.g = g                   # cost from start
            self.h = h                   # heuristic to end
            self.f = g + h               # total cost
            self.parent = parent         # back pointer for path reconstruction

        def __eq__(self, other):
            return self.block.equals(other.block)  # equality by position        

def pathfind(start, end):
    open_list = []
    closed_list = []

    def _h_cost(block):
        return block.getCenter().distanceTo(end.getCenter()) * 10
    
    # setup the pathfind
    start_node = Node(start, g=0, h=_h_cost(start))
    open_list.append(start_node)
   
    for i in range(5000):
        # find the node in open_list with the lowest f cost
        lowest_index = 0
        lowest_f = open_list[0].f

        for i in range(1, len(open_list)):
            if open_list[i].f < lowest_f:
                lowest_f = open_list[i].f
                lowest_index = i

        # remove it from open_list and add to closed_list
        current = open_list[lowest_index]
        del open_list[lowest_index]
        closed_list.append(current) 
        
        # check if target is reached and construct path
        if current.block.equals(end):
            path = []
            while current:
                path.append(current.block)
                current = current.parent
            path.reverse()
            return path
        
        # neighbors exploration
        for x in range(-1, 2):
            for y in range(-1, 2):
                for z in range(-1, 2):
                    neighbour_block = current.block.offset(x, y, z)

                    # skip if ground is air
                    if mc.level.getBlockState(neighbour_block).isAir():
                        continue
                
                    # skip if block above or 2 above is air
                    if not mc.level.getBlockState(neighbour_block.offset(0, 1, 0)).isAir() or not mc.level.getBlockState(neighbour_block.offset(0, 2, 0)).isAir():
                        continue
                
                    # deltas for diagonal checks
                    dx = neighbour_block.getX() - current.block.getX()
                    dz = neighbour_block.getZ() - current.block.getZ()

                    if dx != 0 and dz != 0:
                        # if diagonal is blocked
                        block1 = current.block.offset(dx, 2, 0)
                        block2 = current.block.offset(0, 2, dz)
                        if not mc.level.getBlockState(block1).isAir() or not mc.level.getBlockState(block2).isAir():
                            continue
                
                    neighbour_node = Node(
                        neighbour_block,
                        g=current.g + current.block.getCenter().distanceTo(neighbour_block.getCenter()) * 10,
                        h=_h_cost(neighbour_block),
                        parent=current
                    )

                    # skip the neighbor if already in closed_list
                    skip = False
                    for n in closed_list:
                        if neighbour_node.block.equals(n.block): 
                            skip = True
                            break

                    if skip:
                        continue

                    # check if neighbor is already in open_list
                    existing = None
                    for n in open_list:
                        if n.block.equals(neighbour_node.block): 
                            existing = n
                            break

                    # if not in open_list, add it
                    if existing is None:
                        open_list.append(neighbour_node)
                    else:
                        # if already in open, see if this path is better
                        if neighbour_node.g < existing.g:
                            existing.g = neighbour_node.g
                            existing.f = existing.g + existing.h
                            existing.parent = current 
""")

pathfind_method = pyj_embed.getFunction("pathfind")

def pathfind(start, end):
    return pathfind_method(start, end)

def walk(end):
    path = pathfind(mc.player.blockPosition().offset(0, -1, 0), end)
    node = 0    

    current_target = path.__getattr__("__getitem__")(node).getCenter().add(0, 2, 0)
    
    mc.options.keyUp.setDown(True)
    mc.options.keySprint.setDown(True)
    while True:
        eye_pos = mc.player.getEyePosition()
        vec = eye_pos.vectorTo(current_target)

        if vec.y > 0.3:
            mc.options.keyJump.setDown(True)
        else:
            mc.options.keyJump.setDown(False)
    
        if eye_pos.distanceTo(end.getCenter().add(0, 2, 0)) < 0.6:
            mc.options.keyJump.setDown(False)
            mc.options.keySprint.setDown(False)
            mc.options.keyUp.setDown(False)
            return True
        
        elif vec.horizontalDistance() < 0.6:
            node += 1
            current_target = path.__getattr__("__getitem__")(node).getCenter().add(0, 2, 0)

        mc.player.lookAt(Anchor.EYES, current_target)