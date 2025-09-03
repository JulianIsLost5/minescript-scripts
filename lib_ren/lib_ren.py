"""
    Author: JulianIsLost
    Desc: Library for rendering operations
"""
#!python
import system.pyj.minescript as m

# Java class imports
Minecraft = JavaClass("net.minecraft.client.Minecraft") # type: ignore
RenderType = JavaClass("net.minecraft.client.renderer.RenderType") # type: ignore
Blocks = JavaClass("net.minecraft.world.level.block.Blocks") # type: ignore
OverlayTexture = JavaClass("net.minecraft.client.renderer.texture.OverlayTexture") # type: ignore
ShapeRenderer = JavaClass("net.minecraft.client.renderer.ShapeRenderer") # type: ignore
Registries = JavaClass("net.minecraft.core.registries.Registries") # type: ignore
ResourceLocation = JavaClass("net.minecraft.resources.ResourceLocation") # type: ignore
AABB = JavaClass("net.minecraft.world.phys.AABB") # type: ignore
ARGB = JavaClass("net.minecraft.util.ARGB") # type: ignore
DebugRenderer = JavaClass("net.minecraft.client.renderer.debug.DebugRenderer") # type: ignore
Component = JavaClass("net.minecraft.network.chat.Component") # type: ignore
ChatFormatting = JavaClass("net.minecraft.ChatFormatting") # type: ignore

Vec3 = JavaClass("net.minecraft.world.phys.Vec3") # type: ignore


Array = JavaClass("java.lang.reflect.Array") # type: ignore
Clazz = JavaClass("java.lang.Class") # type: ignore
Obj = JavaClass("java.lang.Object") # type: ignore


Float = JavaClass("java.lang.Float") # type: ignore
 
mc = Minecraft.getInstance()

def _get_registry_from_key(key):
        registry_access = mc.level.registryAccess()
        registry = registry_access.lookupOrThrow(key)
        return registry
   
def _get_registry_entry(key, id):
    registry = _get_registry_from_key(key)
    return registry.getValue(ResourceLocation.parse(id))

def _call_private_method(obj, intermediary, *args):
    cls = obj.getClass()
    
    param_types = Array.newInstance(type(Clazz), len(args))
    params = Array.newInstance(type(Obj), len(args))
    
    for i, arg in enumerate(args):
        Array.set(param_types, i, arg.getClass())
        Array.set(params, i, arg)
        
    method = cls.getDeclaredMethod(intermediary, param_types)
    if method is None:
        return 
    
    method.setAccessible(True)
    return method.invoke(obj, params)


# World Rendering Classes
class WorldRendering():
    
    @staticmethod
    def block(context: WorldRenderContext, target_pos: tuple(float, float, float), block: str):
        """
        Render a single block at a specific position in the world.
        
        Args:
            context: The world render context.
            target_pos: 3D coordinates of the block.
            block: Registry ID of the block to render.
        """
        target_pos = Vec3(*target_pos)
        
        poseStack  = context.matrixStack()
        bufferSource = mc.renderBuffers().bufferSource()
    
        dispatcher = mc.getBlockRenderer()
        
        block = _get_registry_entry(Registries.BLOCK, block)
        
        state = block.defaultBlockState()
        camera = context.camera() 
    
        cameraPos = camera.getPosition()
    
        poseStack.pushPose()
        poseStack.translate(
            target_pos.x - cameraPos.x,
            target_pos.y - cameraPos.y,
            target_pos.z - cameraPos.z
        )
    
        dispatcher.renderSingleBlock(state, poseStack, bufferSource, 0xF000F0, OverlayTexture.NO_OVERLAY)
        poseStack.popPose()
    
        bufferSource.endBatch(RenderType.solid())
        
    @staticmethod
    def wireframe(context: WorldRenderContext, bounds: tuple(float, float, float, float, float, float), rgba: tuple(int, int, int, int)):
        """
        Render a wireframe box in the world.
        
        Args:
            context: The world render context.
            bounds: 6-tuple defining the AABB (minX, minY, minZ, maxX, maxY, maxZ).
            rgba: Color in RGBA format (0-255 per channel).
        """
        box = AABB(*bounds)
        
        camera = context.camera()
        poseStack = context.matrixStack()
        multiBufferSource = context.consumers()
        vertexConsumer = multiBufferSource.getBuffer(RenderType.lines())
        
        position = camera.position()
    
        poseStack.pushPose()
        poseStack.translate(-position.x, -position.y, -position.z)

        ShapeRenderer.renderLineBox(poseStack, vertexConsumer, box, Float(rgba[0]/255), Float(rgba[1]/255), Float(rgba[2]/255), Float(rgba[3]/255))
        poseStack.popPose()

    @staticmethod
    def line(context: WorldRenderContext, beginning: tuple(float, float, float), end: tuple(float, float, float), rgba: tuple(int, int, int, int)):
        """
        Draw a line between two points in the world.
        
        Args:
            context: The world render context.
            beginning: 3D coordinates of the start point.
            end: 3D coordinates of the end point.
            rgba: Color in RGBA format (0-255 per channel).
        """
        camera = context.camera()
        poseStack = context.matrixStack()
        multiBufferSource = context.consumers()
        vertexConsumer = multiBufferSource.getBuffer(RenderType.debugLineStrip(10))
        
        position = camera.getPosition()
    
        poseStack.pushPose()
        poseStack.translate(-position.x, -position.y, -position.z)

        poses = poseStack.last().pose()

        vertexConsumer.addVertex(poses, *beginning).setColor(*rgba).setNormal(0, 1, 0)
        _call_private_method(vertexConsumer, "method_60806")
        vertexConsumer.addVertex(poses, *end).setColor(*rgba).setNormal(0, 1, 0)
        _call_private_method(vertexConsumer, "method_60806")
        
        poseStack.popPose()
        
    @staticmethod
    def text(context: WorldRenderContext, target_pos: tuple(float, float, float), text: str, rgba: tuple(int, int, int, int), size: float = 1, visible_trough_objects: bool = False):
        """
        Render floating text in the world.
        
        Args:
            context: The world render context.
            target_pos: 3D coordinates where text will appear.
            text: The string to render.
            rgba: Text color in RGBA format (0-255 per channel).
            size: Scaling factor of the text.
            visible_trough_objects: If True, text is visible through walls/blocks.
        """
        color = ARGB.color(rgba[3], rgba[0], rgba[1], rgba[2])
        
        camera = context.camera()
        poseStack = context.matrixStack()
        multiBufferSource = context.consumers()
    
        cameraPos = camera.position()
        
        poseStack.pushPose()
        poseStack.translate(
            target_pos[0] - cameraPos.x,
            target_pos[1] - cameraPos.y,
            target_pos[2] - cameraPos.z
        )
        poseStack.scale(Float(0.025), Float(0.025), Float(0.025))
        
        DebugRenderer.renderFloatingText(poseStack, multiBufferSource, text, *target_pos, color, size, True, 0, visible_trough_objects)
        
        poseStack.popPose()

    @staticmethod
    def particle(particle_type: ParticleEffect, position: tuple(float, float, float), force: bool = False, canSpawnOnMinimum: bool = False, velocities: tuple(float, float, float) = (0.0, 0.0, 0.0)):
        """
        Spawn a particle effect in the world.
        
        Args:
            particle_type: Particle type from ParticleTypes.
            position: 3D coordinates for particle spawn.
            force: Force spawn regardless of client settings.
            canSpawnOnMinimum: Allow spawn even if particle settings are minimal.
            velocities: Velocity vector for the particle (x, y, z).
        """
        mc.level.addParticle(particle_type, force, canSpawnOnMinimum, *position, *velocities)      
        
class HudRendering():

    @staticmethod
    def text(context: DrawContext, text: str, position: tuple(int, int), rgba: tuple(int, int, int, int), shadow:bool = False, obfsucated:bool = False, strikethrough:bool = False, underline:bool = False, italic:bool = False):
        """
        Renders a text on the HUD.
        
        Args:
            context: The draw context.
            text: The string to render
            position: 2D coordinates where text will appear.
            rgba: Color in RGBA format (0-255 per channel).
            shadow: If text is rendered with shaow
            obfuscated: If text is rendered with this style.
            strikethrough: If text is rendered with this style.
            underline: If text is rendered with this style.
            italic: If text is rendered with this style.
        """
        color = ARGB.color(rgba[3], rgba[0], rgba[1], rgba[2])
        styles = []
        text = Component.literal(text)
    
        if obfsucated:
            styles.append(ChatFormatting.OBFUSCATED)
        if strikethrough:
            styles.append(ChatFormatting.STRIKETHROUGH)
        if underline:
            styles.append(ChatFormatting.UNDERLINE)
        if italic:
            styles.append(ChatFormatting.ITALIC)
    
        if len(styles) > 0:
            for style in styles:
                text = text.withStyle(style)
                
        context.drawString(mc.font, text, *position, color, shadow)
