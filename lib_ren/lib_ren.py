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
    def block(context: WorldRenderContext, target_pos: tuple(double, double, double), block: str):
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
    def wireframe(context: WorldRenderContext, bounds: tuple(double, double, double, double, double, double), rgba: tuple(int, int, int, int)):
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
    def line(context, beginning, end, rgba):
        camera = context.camera()
        poseStack = context.matrixStack()
        multiBufferSource = context.consumers()
        vertexConsumer = multiBufferSource.getBuffer(RenderType.debugLineStrip(10))
        
        position = camera.position()
    
        poseStack.pushPose()
        poseStack.translate(-position.x, -position.y, -position.z)

        poses = poseStack.last().pose()

        vertexConsumer.addVertex(poses, *beginning).setColor(*rgba).setNormal(0, 1, 0)
        _call_private_method(vertexConsumer, "method_60806")
        vertexConsumer.addVertex(poses, *end).setColor(*rgba).setNormal(0, 1, 0)
        _call_private_method(vertexConsumer, "method_60806")
        
        poseStack.popPose()
        
    @staticmethod
    def text(context, target_pos, text, rgba, size: int = 1, visible_trough_objects: bool = False):
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
    def particle(particle_type, position, force: bool = False, canSpawnOnMinimum: bool = False, velocities = (0.0, 0.0, 0.0)) -> bool:
        """
        particle_type: fields of ParticleTypes
        force: When true, forces the particle to spawn regardless of the client’s particle settings
        canSpawnOnMinimum: When true, this allows the particle to spawn even if the player’s particle settings are set to "Minimal"
        """
        
        mc.level.addParticle(particle_type, force, canSpawnOnMinimum, *position, *velocities)
        return True

# Hud Rendering 
class HudRendering:
    @staticmethod
    def rectangle(context, position, width, height, color, solid = True) -> bool:
        pass

    @staticmethod
    def text(context, text: str, position, text_color) -> bool:
        pass

    @staticmethod
    def item(context, block_id, width, height) -> bool:
        pass
                
