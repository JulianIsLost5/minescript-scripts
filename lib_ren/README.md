# Pyjinn Lib_Ren

**Version:** 0.2.3-alpha\
**Author:** JulianIsLost\
**Date:** 15.08.2025

User-friendly API for performing rendering operations in Minecraft using [Minescripts Pyjinn](https://minescript.net/pyjinn/).  
This module should be imported by other scripts and not run directly.

---

## Prerequisites

Before you start, make sure you have:

- **Fabric** mod loader configured
- **Minescript 5.x** installed
- **Mappings** installed

---

## Usage

- Download the **lib_ren.py** file
- Place it directly in the minescript folder
- Import the module into your script:
  
  ```python
  from ren_lib import WorldRendering, HudRendering
  ```
- There is no need to import all classes, just the ones needed
- Use the classes and methods as documented below

---

## Classes & Methods

###  WorldRendering

Classes for rendering in the world

- **block(context, target_pos: Vec3, block: str)**
  
  Renders a vanilla block into the world

  - **context:** `GuiGraphics` — The context passed by the RenderCallback.
  - **target_pos:** `Vec3` - The position of the rendered block.
  - **block:** `str` - Search the block in [this classes’](https://mappings.dev/1.21.8/net/minecraft/world/level/block/Blocks.html) fields.
  
- **Wireframe()**
  Renders a wireframe of custom size into the world
  
- **WorldLine()**
  Renders a line into the world

- **WorldText()**
  Renders a text into the world

### HudRendering

The `HudRendering` class provides methods for drawing shapes, text, and interactive elements on the player's Hud.


- **rectangle(context, position: Tuple[int, int], width: int, height: int, color: Tuple[int, int, int, int], solid: bool = True)**

   Draws a rectangle on the Hud.

   - **context:** `GuiGraphics` — The context passed by the RenderCallback.
   - **position:** `(x, y)` — The center coordinates of the rectangle.
   - **width:** `int` — Width in pixels.
   - **height:** `int` — Height in pixels.
   - **color:** `(alpha, red, green, blue)` — ARGB color values (0–255).
   - **solid:** `bool` — Whether the rectangle is filled (`True`) or outlined (`False`).

   Example:
   ```python
   HudRendering.rectangle(context, (50, 20), 80, 10, (255, 255, 0, 0), True)
   ```
   
- **text(context, text: str, position: Tuple[int, int], text_color: Tuple[int, int, int, int])**
  
   Draws a text on the Hud.
  
   - **context:** `GuiGraphics` — The context passed by the RenderCallback.
   - **text:** `str` - The text to be drawn.
   - **position:** `(x, y)` — The center coordinates of the rectangle.
   - **text_color:** `(alpha, red, green, blue)` — ARGB color values (0–255).

   Example:
   ```python
   HudRendering.text(context, "Example Text", (50, 20), (255, 255, 0, 0))
   ```
  
- **item(context, block_id: str, width: int, height: int)**

  Renders an item on the Hud

  - **context:** `GuiGraphics` — The context passed by the RenderCallback.
  - **block_id:** `minecraft:block` - The internal block id.
  - **width, height:** Icon size.

  Example:
  ```python
  HudRender.item(context, "minecraft:stone", 10, 10)
  ```
  
  Note:
   This method was taken in its entirety from [RazrCraft](https://github.com/R4z0rX)

- **button(position: Tuple[int, int], width: int, height: int, text: str, text_color: Tuple[int, int, int, int], button_color: Tuple[int, int, int, int], click_callback: Callable)**

  Unlike the other Hud methods, `button` is a **subclass** and needs to be instantiated using the constructor. Then its `render()` method needs to be called in the render loop. (Use example below as reference)
   - **position:** `(x, y)` - The center coordinates of the button.
   - **width, height:** Button size.
   - **text:** Label displayed on the button.
   - **text_color:** ARGB for the label text.
   - **button_color** ARGB for the button bsckground.
   - **click_callback** Function called when the button is clicked.
 
   Example:
   ```python
   HudRenderCallback = JavaClass("net.fabricmc.fabric.api.client.rendering.v1.HudRenderCallback") # type: ignore
   
   def clicked():
       print("Clicked!")

   example_button = HudRendering.button((50, 20), 80, 20, "Example Button", (255, 0, 0, 0), (204, 0, 138, 255), clicked)

   def on_hud_render(context, tickDelta):
       example_button.render(context)

   HudRenderCallback.EVENT.register(HudRenderCallback(on_hud_render))
   add_event_listener("tick", lambda e: None)
   ```
  
- **Cimg()**\
  Renders a custom image on the HUD

## Useful Links

- [Minecraft Internal Mappings](https://mappings.dev) 
- [Minescript Discord](https://discord.gg/NjcyvrHTze)

## License

MIT © 2025 JulianIsLost
