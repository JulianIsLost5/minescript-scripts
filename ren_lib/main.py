import system.pyj.minescript as m

# Java class imports
Minecraft = JavaClass("net.minecraft.client.Minecraft") # type: ignore
ARGB = JavaClass("net.minecraft.util.ARGB") # type: ignore
BuiltInRegistries = JavaClass("net.minecraft.core.registries.BuiltInRegistries")
ResourceLocation = JavaClass("net.minecraft.resources.ResourceLocation")
Items = JavaClass("net.minecraft.world.item.Items")
 
mc = Minecraft.getInstance()

def get_item_from_blockid(block_id: str):
    id = ResourceLocation.parse(block_id)
    return BuiltInRegistries.ITEM.getValue(id)

# World Rendering Classes
class WorldRendering():
    class Block():
        def __init__(self):
        pass

    class Wireframe():
        def __init__(self):
            pass

    class WorldLine():
        def __init__(self):
            pass

    class WorldText():
        def __init__(self):
            pass

# Hud Rendering 
class HudRendering:
    def rectangle(context, position, width, height, color, solid = True):
        left_x_position = position[0]-width*0.5
        top_y_position = position[1]-height*0.5
        right_x_position = position[0]+width*0.5
        bottom_y_position = position[1]+height*0.5
        color = ARGB.color(*color)
        
        if solid is True:
            context.fill(self.left_x_position, self.top_y_position, self.right_x_position, self.bottom_y_position, self.color)
        elif solid is False:
            context.renderOutline(self.left_x_position, self.top_y_position, self.width, self.height, self.color)

    def text(context, text, position, text_color):
        left_x_position = position[0] - mc.font.width(text)*0.5
        text_color = ARGB.color(*text_color)
    
        context.drawString(mc.font, self.text, left_x_position, position[1], self.text_color, False)

    # Taken from razrcraft
    def item(context, block_id, width, height):
        item = get_item_from_blockid(block_id)
        
        context.renderItem(item, width, height)

    class button():
        def __init__(self, position, width, height, text, text_color, button_color, click_callback): 
            self.left_x_position = position[0]-width*0.5
            self.top_y_position = position[1]-height*0.5
            self.right_x_position = position[0]+width*0.5
            self.bottom_y_position = position[1]+height*0.5
            self.width = width
            self.height = height
            self.text = text
            self.text_color = ARGB.color(*text_color)
            self.button_color = ARGB.color(*button_color)
            self.text_width = mc.font.width(text)
            self.text_height = mc.font.lineHeight
            self.click_callback = click_callback
            m.add_event_listener("mouse", self.check_for_click)

        def render(self, context):
            context.fill(self.left_x_position, self.top_y_position, self.right_x_position, self.bottom_y_position, self.button_color)
            context.drawString(mc.font, self.text, int(self.position[0] - self.text_width*0.5), int(self.position[1] + self.text_height*0.5), self.text_color, False)
    
        def lighten_color(self):
            factor = 1/0.7
        
            a = ARGB.alpha(self.button_color)
            r = ARGB.red(self.button_color)
            g = ARGB.green(self.button_color)
            b = ARGB.blue(self.button_color)
        
            self.button_color = ARGB.color(a, int(r*factor), int(g*factor), int(b*factor))
        
        def darken_color(self):
            factor = 0.7
        
            a = ARGB.alpha(self.button_color)
            r = ARGB.red(self.button_color)
            g = ARGB.green(self.button_color)
            b = ARGB.blue(self.button_color)
        
            self.button_color = ARGB.color(a, int(r*factor), int(g*factor), int(b*factor))
    
        def button_clicked(self):
            self.darken_color()
            self.click_callback()
            m.set_timeout(self.button_unclicked, 250)
    
        def button_unclicked(self):
            self.lighten_color()
    
        def check_for_click(self, event):
            if event.action == 1:
                scale = mc.getWindow().getGuiScale()
        
                x = event.x / scale
                y = event.y / scale        
    
                if self.x_position <= x and x <= self.x_position + self.width and self.y_position <= y and y <= self.y_position + self.height:
                    self.button_clicked()
                
class Cimg():
    def __init__(self):
        pass
