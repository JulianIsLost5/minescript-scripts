# Pyjinn Lib_Ren

**Author:** JulianIsLost\

User-friendly API for performing rendering operations in Minecraft using [Minescripts Pyjinn](https://minescript.net/pyjinn/).  
This module should be imported by other scripts and not run directly.

---

## Prerequisites

Before you start, make sure you have:

- **Fabric** mod loader configured
- **Minescript 5.0b5+** installed
- **Mappings** installed

---

## Usage

- Download the **lib_ren.py** file
- Place it directly in the minescript folder
- Import the module into your script:
  
  ```python
  from ren_lib import WorldRendering
  ```
- There is no need to import all classes, just the ones needed
- Use the classes and methods as documented below

---

## Classes & Methods

###  WorldRendering

Classes for rendering in the world

- **block(context: WorldRenderContext, target_pos: tuple(float, float, float), block: str)**
  
  Renders a vanilla block into the world

  ```python
  from lib_ren import WorldRendering

  WorldRenderEvents = JavaClass("net.fabricmc.fabric.api.client.rendering.v1.WorldRenderEvents") # type: ignore
  WorldRenderEventsLast = JavaClass("net.fabricmc.fabric.api.client.rendering.v1.WorldRenderEvents$Last") # type: ignore

  def on_press_key(event):
      if event.action == 0 and event.key == 342:  # ALT
          callback.cancel()

  def on_world_render_last(context):
      WorldRendering.block(context, (10, -60, 4), "minecraft:dirt")

  add_event_listener("key", on_press_key)
  callback = ManagedCallback(on_world_render_last)
  WorldRenderEvents.LAST.register(WorldRenderEventsLast(callback))
  ```

  
- ** wireframe(context: WorldRenderContext, bounds: tuple(float, float, float, float, float, float), rgba: tuple(int, int, int, int))**
  
  Renders a wireframe of custom size and color into the world

  ```python
  from lib_ren import WorldRendering

  WorldRenderEvents = JavaClass("net.fabricmc.fabric.api.client.rendering.v1.WorldRenderEvents") # type: ignore
  WorldRenderEventsLast = JavaClass("net.fabricmc.fabric.api.client.rendering.v1.WorldRenderEvents$Last") # type: ignore

  def on_press_key(event):
      if event.action == 0 and event.key == 342:  # ALT
          callback.cancel()

  def on_world_render_last(context):
      WorldRendering.wireframe(context, (10, -60, 4, 11, -69, 5), (255, 0, 0, 255))

  add_event_listener("key", on_press_key)
  callback = ManagedCallback(on_world_render_last)
  WorldRenderEvents.LAST.register(WorldRenderEventsLast(callback))
  ```
  
- **line(context: WorldRenderContext, beginning: tuple(float, float, float), end: tuple(float, float, float), rgba: tuple(int, int, int, int))**
  
  Renders a colored line between to coordinates into the world

  ```python
  from lib_ren import WorldRendering

  WorldRenderEvents = JavaClass("net.fabricmc.fabric.api.client.rendering.v1.WorldRenderEvents") # type: ignore
  WorldRenderEventsLast = JavaClass("net.fabricmc.fabric.api.client.rendering.v1.WorldRenderEvents$Last") # type: ignore

  def on_press_key(event):
      if event.action == 0 and event.key == 342:  # ALT
          callback.cancel()

  def on_world_render_last(context):
      WorldRendering.line(context, (10, -60, 4), (15, -58, 4), (0, 0, 0, 255))

  add_event_listener("key", on_press_key)
  callback = ManagedCallback(on_world_render_last)
  WorldRenderEvents.LAST.register(WorldRenderEventsLast(callback))
  ```

- **text(context: WorldRenderContext, target_pos: tuple(float, float, float), text: str, rgba: tuple(int, int, int, int), size: float = 1, visible_trough_objects: bool = False)**
  
  Renders colored text into the world at a given position

  ```python
  from lib_ren import WorldRendering

  WorldRenderEvents = JavaClass("net.fabricmc.fabric.api.client.rendering.v1.WorldRenderEvents") # type: ignore
  WorldRenderEventsLast = JavaClass("net.fabricmc.fabric.api.client.rendering.v1.WorldRenderEvents$Last") # type: ignore

  def on_press_key(event):
      if event.action == 0 and event.key == 342:  # ALT
          callback.cancel()

  def on_world_render_last(context):
      WorldRendering.text(context, (10, -60, 4), "Hello World", (0, 0, 0, 255))

  add_event_listener("key", on_press_key)
  callback = ManagedCallback(on_world_render_last)
  WorldRenderEvents.LAST.register(WorldRenderEventsLast(callback))
  ```

- **particle(particle_type: ParticleEffect, position: tuple(float, float, float), force: bool = False, canSpawnOnMinimum: bool = False, velocities: tuple(float, float, float) = (0.0, 0.0, 0.0))**
  
  Renders a particle into the world

  ```python
  from lib_ren import WorldRendering

  ParticleTypes = JavaClass("net.minecraft.core.particles.ParticleTypes") # type: ignore

  WorldRendering.particle(ParticleTypes.HEART, (10, -60, 4))
  ```

## Useful Links

- [Minecraft Internal Mappings](https://mappings.dev) 
- [Minescript Discord](https://discord.gg/NjcyvrHTze)

## License

MIT © 2025 JulianIsLost
