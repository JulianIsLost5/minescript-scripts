import system.pyj.minescript as m

# Java class imports
Minecraft = JavaClass("net.minecraft.client.Minecraft") # type: ignore
ARGB = JavaClass("net.minecraft.util.ARGB") # type: ignore
BuiltInRegistries = JavaClass("net.minecraft.core.registries.BuiltInRegistries")
ResourceLocation = JavaClass("net.minecraft.resources.ResourceLocation")
Items = JavaClass("net.minecraft.world.item.Items")
RenderType = JavaClass("net.minecraft.client.renderer.RenderType") # type: ignore
Blocks = JavaClass("net.minecraft.world.level.block.Blocks") # type: ignore
OverlayTexture = JavaClass("net.minecraft.client.renderer.texture.OverlayTexture")
ParticleTypes = JavaClass("net.minecraft.core.particles.ParticleTypes")
 
mc = Minecraft.getInstance()

def get_item_from_blockid(block_id: str):
    id = ResourceLocation.parse(block_id)
    return BuiltInRegistries.ITEM.getValue(id)

# World Rendering Classes
class WorldRendering():
    @staticmethod
    def block(context, target_pos, block):
        poseStack = context.matrixStack()
        bufferSource = mc.renderBuffers().bufferSource()
        
        dispatcher = mc.getBlockRenderer()
        
        blocks_fields = Blocks.getDeclaredFields()
        for blocks_field in blocks_fields:
            if blocks_field.getName() == block:
                state = blocks_field.defaultBlockState()
        
        camera = context.camera()
        camera_pos = camera.getPosition()
        
        poseStack.pushPose()
        poseStack.translate(target_pos.x - camera_pos.x, target_pos.y - camera_pos.y, target_pos.z - camera_pos.z)
        
        dispatcher.renderSingleBlock(state, poseStack, bufferSource, 0xF000F0, OverlayTexture.NO_OVERLAY)
        poseStack.popPose()
        
        bufferSource.endBatch(RenderType.solid())
        
    class Wireframe():
        def __init__(self):
            pass

    class WorldLine():
        def __init__(self):
            pass

    class WorldText():
        def __init__(self):

    @staticmethod
    def particle(x, y, z):
        mc.level.addParticle(ParticleTypes.HEART, x, y, z, 0.0, 0.0, 0.0)

# Hud Rendering 
class HudRendering:
    @staticmethod
    def rectangle(context, position, width, height, color, solid = True):
        left_x_position = position[0]-width*0.5
        top_y_position = position[1]-height*0.5
        right_x_position = position[0]+width*0.5
        bottom_y_position = position[1]+height*0.5
        color = ARGB.color(*color)
        
        if solid is True:
            context.fill(left_x_position, top_y_position, right_x_position, bottom_y_position, color)
        elif solid is False:
            context.renderOutline(left_x_position, top_y_position, width, height, color)

    @staticmethod
    def text(context, text, position, text_color):
        left_x_position = position[0] - mc.font.width(text)*0.5
        text_color = ARGB.color(*text_color)
    
        context.drawString(mc.font, text, left_x_position, position[1], text_color, False)

    # Taken from razrcraft
    @staticmethod
    def item(context, block_id, width, height):
        item = get_item_from_blockid(block_id)
        
        context.renderItem(item, width, height)

    class button():
        def __init__(self, position, width, height, text, click_callback): 
             self.left_x_position = position[0]-width*0.5
             self.top_y_position = position[1]-height*0.5
             self.right_x_position = position[0]+width*0.5
             self.bottom_y_position = position[1]+height*0.5
             self.width = width
             self.height = height
             self.font = mc.font
             self.text_width = font.width(text)
             self.text_height = font.lineHeight
             self.click_callback = click_callback
             m.add_event_listener("mouse", self.check_for_click)
             self.text_color = ARGB.color(255, 0, 0, 0) 
             self.text_shadow = False
             self.text_component = Component.literal(text)
             self.button_color = ARGB.color(125, 0, 0, 0) 
             self.factor = 0.7
        
        def set_text_color(self, text_color):
            self.text_color = ARGB.color(*text_color)
        
        def set_text_shadow(self):
            self.text_shadow = True
        
        def text_italic(self):
            self.text_component = self.text_component.withStyle(ChatFormatting.ITALIC)
        
        def text_bold(self):
            self.text_component = self.text_component.withStyle(ChatFormatting.BOLD)
        
        def text_underline(self):
            self.text_component = self.text_component.withStyle(ChatFormatting.UNDERLINE)
        
        def text_strikethrough(self):
            self.text_component = self.text_component.withStyle(ChatFormatting.STRIKETHROUGH)
    
        def set_button_color(self, button_color):
            self.button_color = ARGB.color(*button_color)
        
        def set_onclick_factor(self, factor):
            self.factor = factor

        def render(self, context):
            context.fill(self.left_x_position, self.top_y_position, self.right_x_position, self.bottom_y_position, self.button_color)
            context.drawString(font, self.text_component, int(self.position[0] - self.text_width*0.5), int(self.position[1] + self.text_height*0.5), self.text_color, False)
    
        def lighten_color(self):
            factor = 1/self.factor
        
            a = ARGB.alpha(self.button_color)
            r = ARGB.red(self.button_color)
            g = ARGB.green(self.button_color)
            b = ARGB.blue(self.button_color)
        
            self.button_color = ARGB.color(a, int(r*factor), int(g*factor), int(b*factor))
        
        def darken_color(self):
            a = ARGB.alpha(self.button_color)
            r = ARGB.red(self.button_color)
            g = ARGB.green(self.button_color)
            b = ARGB.blue(self.button_color)
        
            self.button_color = ARGB.color(a, int(r*self.factor), int(g*self.factor), int(b*self.factor))
    
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
